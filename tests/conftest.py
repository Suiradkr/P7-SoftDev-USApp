from datetime import datetime, timedelta

import pytest

import provider

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Dates are computed relative to "now" so the fixtures never go stale:
# "Spring Festival" is always upcoming and "Fall Classic" always in the past.
FUTURE_DATE = (datetime.now() + timedelta(days=365)).strftime(DATE_FORMAT)
PAST_DATE = (datetime.now() - timedelta(days=365)).strftime(DATE_FORMAT)


def build_clubs():
    """Fresh club data for a single test"""
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]


def build_competitions():
    """Fresh competition data for a single test"""
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
    The provider's own functions are left alone, so tests/test_provider.py still
    reads the real JSON files.

    Each test gets its own data, but every call within a test returns the *same*
    objects, mirroring the in-memory provider. Returning a fresh list per call
    would silently discard whatever a booking wrote.
    """

    clubs = build_clubs()
    competitions = build_competitions()

    def mock_get_clubs():
        """Return the same club list for every call in this test"""
        return clubs

    def mock_get_competitions():
        """Return the same competition list for every call in this test"""
        return competitions

    monkeypatch.setattr("server.get_clubs", mock_get_clubs)
    monkeypatch.setattr("server.get_competitions", mock_get_competitions)
    # The booking ledger lives for the whole process, so clear it per test
    provider.reset_bookings()
