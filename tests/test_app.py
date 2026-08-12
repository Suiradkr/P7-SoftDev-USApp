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


def test_login_unknown_email():
    """An unknown email should not crash; it returns to the homepage with a message"""
    with app.test_client() as c:
        resp = c.post(
            "/login", data={"email": "nobody@example.com"}, follow_redirects=True
        )
        # We should be back on the homepage, not crashed (no 500)
        assert request.path == "/"
        assert resp.status_code == 200
        # The error message is shown to the user
        assert "Sorry, that email was not found." in resp.data.decode()
