from datetime import datetime

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from provider import (
    get_booked_spots,
    get_clubs,
    get_competitions,
    record_booking,
)

app = Flask(__name__)
# You should change the secret key in production!
app.secret_key = "something_special"

# A club may enter at most 12 athletes in any one competition
MAX_SPOTS_PER_COMPETITION = 12

# Format used for competition dates in the JSON data
COMPETITION_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def is_in_past(competition):
    """True if the competition's start date has already passed"""
    starts_at = datetime.strptime(competition["date"], COMPETITION_DATE_FORMAT)
    return starts_at < datetime.now()


# Make the helper available to templates so past events can hide their book link
app.jinja_env.globals["is_in_past"] = is_in_past


def current_club():
    """The logged in club, resolved from the shared data on every request.

    The session stores only the email, so the club's points have a single
    source of truth. Holding a copy in the session meant a booking updated
    that copy and left the shared record untouched.
    """
    email = session["club_email"]
    matching = [club for club in get_clubs() if club["email"] == email]

    if not matching:
        abort(401)

    return matching[0]


@app.route("/")
def index():
    """Homepage"""
    return render_template("index.html")


@app.route("/clubs")
def clubs_board():
    """Public board listing every club and its available points (no login needed)"""
    return render_template("clubs.html", clubs=get_clubs())


@app.route("/login", methods=["POST"])
def login():
    """Use the session object to store the club information across requests"""

    clubs = get_clubs()
    email = request.form["email"]

    matching_clubs = [item for item in clubs if item["email"] == email]
    if not matching_clubs:
        flash("Sorry, that email was not found.")
        return render_template("index.html"), 401

    session["club_email"] = matching_clubs[0]["email"]

    return redirect(url_for("summary"))


@app.route("/summary")
def summary():
    """Custom "homepage" for logged in users"""

    club = current_club()
    competitions = get_competitions()

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>")
def book(competition):
    """Book spots in a competition page"""
    club = current_club()

    competitions = get_competitions()
    matching_comps = [comp for comp in competitions if comp["name"] == competition]

    if not matching_comps:
        abort(404)

    found_competition = matching_comps[0]

    if is_in_past(found_competition):
        abort(403)

    spots_remaining = MAX_SPOTS_PER_COMPETITION - get_booked_spots(
        club["name"], found_competition["name"]
    )

    return render_template(
        "booking.html",
        club=club,
        competition=found_competition,
        spots_remaining=spots_remaining,
    )


@app.route("/book", methods=["POST"])
def book_spots():
    """This page is only accessible through a POST request (form validation)"""
    club = current_club()
    competitions = get_competitions()

    matching_comps = [
        comp for comp in competitions if comp["name"] == request.form["competition"]
    ]

    if not matching_comps:
        abort(404)

    competition = matching_comps[0]

    if is_in_past(competition):
        abort(403)

    try:
        spots_required = int(request.form["spots"])
    except ValueError:
        flash("Please enter a whole number of spots.")
        return redirect(url_for("summary"))

    if spots_required <= 0:
        flash("You must book at least one spot.")
        return redirect(url_for("summary"))

    already_booked = get_booked_spots(club["name"], competition["name"])

    if already_booked + spots_required > MAX_SPOTS_PER_COMPETITION:
        abort(403)

    if spots_required > int(club["points"]):
        abort(403)

    if spots_required > int(competition["spotsAvailable"]):
        abort(403)

    competition["spotsAvailable"] = int(competition["spotsAvailable"]) - spots_required
    club["points"] = int(club["points"]) - spots_required
    record_booking(club["name"], competition["name"], spots_required)
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/logout")
def logout():
    """We delete session data in order to log the user out"""
    del session["club_email"]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
