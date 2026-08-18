from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

from provider import get_clubs, get_competitions

app = Flask(__name__)
# You should change the secret key in production!
app.secret_key = "something_special"

# A club may enter at most 12 athletes in any one competition
MAX_SPOTS_PER_COMPETITION = 12


@app.route("/")
def index():
    """Homepage"""
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    """Use the session object to store the club information across requests"""

    clubs = get_clubs()
    email = request.form["email"]

    matching_clubs = [item for item in clubs if item["email"] == email]
    if not matching_clubs:
        flash("Sorry, that email was not found.")
        return render_template("index.html"), 401

    club = matching_clubs[0]
    session["club"] = club

    return redirect(url_for("summary"))


@app.route("/summary")
def summary():
    """Custom "homepage" for logged in users"""

    club = session["club"]
    competitions = get_competitions()

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>")
def book(competition):
    """Book spots in a competition page"""
    club = session["club"]

    competitions = get_competitions()
    matching_comps = [comp for comp in competitions if comp["name"] == competition]

    found_competition = matching_comps[0]

    if found_competition:
        return render_template("booking.html", club=club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for("summary"))


@app.route("/book", methods=["POST"])
def book_spots():
    """This page is only accessible through a POST request (form validation)"""
    club = session["club"]
    competitions = get_competitions()

    matching_comps = [
        comp for comp in competitions if comp["name"] == request.form["competition"]
    ]

    competition = matching_comps[0]

    spots_required = int(request.form["spots"])

    if spots_required <= 0:
        flash("You must book at least one spot.")
        return redirect(url_for("summary"))

    if spots_required > MAX_SPOTS_PER_COMPETITION:
        abort(403)

    if spots_required > int(club["points"]):
        abort(403)

    competition["spotsAvailable"] = int(competition["spotsAvailable"]) - spots_required
    club["points"] = int(club["points"]) - spots_required
    session["club"] = club  # persist the new balance for later requests
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/logout")
def logout():
    """We delete session data in order to log the user out"""
    del session["club"]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
