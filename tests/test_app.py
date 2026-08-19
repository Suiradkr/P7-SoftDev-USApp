from flask import request

from server import app


def test_homepage():
    """Test the homepage works (HTTP status 200 OK)"""
    with app.test_client() as c:
        resp = c.get("/")
        assert resp.status_code == 200


def test_login():
    """Tests a login action"""
    with app.test_client() as c:
        resp = c.post(
            "/login", data={"email": "john@simplylift.co"}, follow_redirects=True
        )
        # We should be redirected to the summary page
        assert request.path == "/summary"
        # The status code should be 200 OK
        assert resp.status_code == 200
        # The email of the user logged in is displayed on the page
        assert "john@simplylift.co" in resp.data.decode()
        # ...along with the number of points available for their club
        assert "Points available: 13" in resp.data.decode()


def test_login_unknown_email():
    """An unknown email is rejected with HTTP 401 and an error message"""
    with app.test_client() as c:
        resp = c.post("/login", data={"email": "nobody@example.com"})
        # Unauthorized, not crashed (no 500)
        assert resp.status_code == 401
        # The error message is shown to the user
        assert "Sorry, that email was not found." in resp.data.decode()


def test_points_board_is_public():
    """Any user, even not logged in, can see every club and its points"""
    with app.test_client() as c:
        resp = c.get("/clubs")
        assert resp.status_code == 200
        page = resp.data.decode()
        # Every club from the mock data is listed with its points
        for name, points in [
            ("Simply Lift", "13"),
            ("Iron Temple", "4"),
            ("She Lifts", "12"),
        ]:
            assert name in page
            assert points in page


def test_points_board_linked_from_homepage():
    """The homepage links to the public points board"""
    with app.test_client() as c:
        resp = c.get("/")
        assert "/clubs" in resp.data.decode()


def test_booking_more_than_points_is_forbidden():
    """Booking more spots than the club has points returns HTTP 403"""
    with app.test_client() as c:
        # Iron Temple has 4 points (see conftest mock)
        c.post("/login", data={"email": "admin@irontemple.com"})
        resp = c.post(
            "/book", data={"competition": "Spring Festival", "spots": "5"}
        )
        assert resp.status_code == 403


def test_valid_booking_deducts_points():
    """A valid booking succeeds and reduces the club's points by the spots booked"""
    with app.test_client() as c:
        # Iron Temple has 4 points; booking 2 should leave 2
        c.post("/login", data={"email": "admin@irontemple.com"})
        resp = c.post(
            "/book", data={"competition": "Spring Festival", "spots": "2"}
        )
        assert resp.status_code == 200
        assert "Points available: 2" in resp.data.decode()
        # The competition loses the same number of spots (25 -> 23)
        assert "Number of spots available: 23" in resp.data.decode()


def test_booking_more_than_twelve_spots_is_forbidden():
    """A club cannot book more than 12 spots in a competition (HTTP 403)"""
    with app.test_client() as c:
        # Simply Lift has 13 points, so points are not the limiting factor here
        c.post("/login", data={"email": "john@simplylift.co"})
        resp = c.post(
            "/book", data={"competition": "Spring Festival", "spots": "13"}
        )
        assert resp.status_code == 403


def test_booking_exactly_twelve_spots_is_allowed():
    """Booking the maximum of 12 spots is still permitted"""
    with app.test_client() as c:
        # Simply Lift has 13 points, enough to book 12 spots
        c.post("/login", data={"email": "john@simplylift.co"})
        resp = c.post(
            "/book", data={"competition": "Spring Festival", "spots": "12"}
        )
        assert resp.status_code == 200
        assert "Points available: 1" in resp.data.decode()


def test_booking_past_competition_is_forbidden():
    """A club cannot book spots in a competition that has already taken place"""
    with app.test_client() as c:
        # "Fall Classic" is dated in the past (see conftest)
        c.post("/login", data={"email": "john@simplylift.co"})
        resp = c.post("/book", data={"competition": "Fall Classic", "spots": "1"})
        assert resp.status_code == 403


def test_booking_page_for_past_competition_is_forbidden():
    """The booking form itself is not reachable for a past competition"""
    with app.test_client() as c:
        c.post("/login", data={"email": "john@simplylift.co"})
        resp = c.get("/book/Fall Classic")
        assert resp.status_code == 403


def test_booking_zero_or_negative_spots_is_rejected():
    """Booking zero or negative spots is rejected without changing points"""
    with app.test_client() as c:
        # Iron Temple has 4 points
        c.post("/login", data={"email": "admin@irontemple.com"})
        resp = c.post(
            "/book",
            data={"competition": "Spring Festival", "spots": "0"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert "You must book at least one spot." in resp.data.decode()
        # Points are unchanged
        assert "Points available: 4" in resp.data.decode()


def test_booking_page_for_unknown_competition_returns_404():
    """The booking page for a competition that does not exist returns HTTP 404"""
    with app.test_client() as c:
        c.post("/login", data={"email": "john@simplylift.co"})
        resp = c.get("/book/Does Not Exist")
        assert resp.status_code == 404


def test_booking_unknown_competition_returns_404():
    """Posting a booking for an unknown competition returns HTTP 404"""
    with app.test_client() as c:
        c.post("/login", data={"email": "john@simplylift.co"})
        resp = c.post(
            "/book", data={"competition": "Does Not Exist", "spots": "1"}
        )
        assert resp.status_code == 404


def test_booking_more_spots_than_available_is_forbidden():
    """A club cannot book more spots than the competition has left (HTTP 403)"""
    with app.test_client() as c:
        # Iron Temple has 4 points; "Sold Out Sprint" only has 3 spots left,
        # so points and the 12-spot cap are not the limiting factor here.
        c.post("/login", data={"email": "admin@irontemple.com"})
        resp = c.post(
            "/book", data={"competition": "Sold Out Sprint", "spots": "4"}
        )
        assert resp.status_code == 403


def test_booking_exactly_the_available_spots_is_allowed():
    """Booking every remaining spot is permitted and empties the competition"""
    with app.test_client() as c:
        c.post("/login", data={"email": "admin@irontemple.com"})
        resp = c.post(
            "/book", data={"competition": "Sold Out Sprint", "spots": "3"}
        )
        assert resp.status_code == 200
        assert "Number of spots available: 0" in resp.data.decode()


def test_booking_page_displays_the_form():
    """A logged in user opening a competition sees the booking form"""
    with app.test_client() as c:
        c.post("/login", data={"email": "john@simplylift.co"})
        resp = c.get("/book/Spring Festival")
        assert resp.status_code == 200
        page = resp.data.decode()
        assert "Spring Festival" in page
        # The form and its spots input are present
        assert 'name="spots"' in page
        assert 'action="/book"' in page


def test_logout_clears_the_session():
    """Logging out ends the session and returns the user to the homepage"""
    with app.test_client() as c:
        c.post("/login", data={"email": "john@simplylift.co"})
        resp = c.get("/logout", follow_redirects=True)
        assert resp.status_code == 200
        assert "Please enter your secretary email" in resp.data.decode()
        # The club is no longer held in the session
        with c.session_transaction() as sess:
            assert "club" not in sess


def test_twelve_spot_limit_is_cumulative_per_competition():
    """Repeat bookings cannot take a club past 12 spots in one competition"""
    with app.test_client() as c:
        # Simply Lift has 13 points, so points alone would allow a 13th spot
        c.post("/login", data={"email": "john@simplylift.co"})
        first = c.post(
            "/book", data={"competition": "Spring Festival", "spots": "12"}
        )
        assert first.status_code == 200
        # The 13th spot would take the running total past the cap
        second = c.post(
            "/book", data={"competition": "Spring Festival", "spots": "1"}
        )
        assert second.status_code == 403


def test_twelve_spot_limit_is_tracked_per_competition():
    """Spots booked in one competition do not count against another"""
    with app.test_client() as c:
        c.post("/login", data={"email": "john@simplylift.co"})
        c.post("/book", data={"competition": "Spring Festival", "spots": "12"})
        # A different competition still has the club's full allowance
        resp = c.post(
            "/book", data={"competition": "Sold Out Sprint", "spots": "1"}
        )
        assert resp.status_code == 200
