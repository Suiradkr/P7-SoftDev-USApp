from datetime import datetime, timedelta

import pytest

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Dates are computed relative to "now" so the fixtures never go stale:
# "Spring Festival" is always upcoming and "Fall Classic" always in the past.
FUTURE_DATE = (datetime.now() + timedelta(days=365)).strftime(DATE_FORMAT)
PAST_DATE = (datetime.now() - timedelta(days=365)).strftime(DATE_FORMAT)


def mock_clubs():
    """Static data to mock clubs"""
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]


def mock_competitions():
    """Static data to mock competitions"""
    return [
        {
            "name": "Spring Festival",
            "date": FUTURE_DATE,
            "spotsAvailable": "25",
        },
        {
            "name": "Fall Classic",
            "date": PAST_DATE,
            "spotsAvailable": "13",
        },
        # Deliberately low capacity, to exercise the "not enough spots" guard
        {
            "name": "Sold Out Sprint",
            "date": FUTURE_DATE,
            "spotsAvailable": "3",
        },
    ]


@pytest.fixture(autouse=True)
def mock_data_provider(monkeypatch):
    """
    This fixture will be automatically used in test functions.

    We patch `server.get_clubs`, because that's where the get_clubs function is used.
    """

    monkeypatch.setattr("server.get_clubs", mock_clubs)
    monkeypatch.setattr("server.get_competitions", mock_competitions)
