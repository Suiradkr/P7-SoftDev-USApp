"""Tests for loading clubs and competitions from the JSON data files.

The autouse fixture in conftest patches `server.get_clubs` /
`server.get_competitions`, not the provider's own functions, so these tests
exercise the real files in the `data` folder.
"""
from datetime import datetime

import provider

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def test_get_clubs_reads_the_json_file():
    """Every club is loaded with a name, an email and a numeric points balance"""
    clubs = provider.get_clubs()

    assert len(clubs) > 0
    for club in clubs:
        assert {"name", "email", "points"} <= set(club)
        assert club["name"]
        assert "@" in club["email"]
        assert club["points"].isdigit()

    # Secretaries log in by email, so those must be unique
    emails = [club["email"] for club in clubs]
    assert len(emails) == len(set(emails))


def test_get_competitions_reads_the_json_file():
    """Every competition is loaded with a name, a parsable date and its spots"""
    competitions = provider.get_competitions()

    assert len(competitions) > 0
    for competition in competitions:
        assert {"name", "date", "spotsAvailable"} <= set(competition)
        assert competition["name"]
        assert competition["spotsAvailable"].isdigit()
        # Raises ValueError if the stored format ever drifts
        datetime.strptime(competition["date"], DATE_FORMAT)
