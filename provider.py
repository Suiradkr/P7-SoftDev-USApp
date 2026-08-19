import json
from pathlib import Path

DATA_FOLDER = "data"


def _json_from_file(filename, key):
    """Helper method - loads JSON from 'filename' and return whatever is at the 'key'"""
    filepath = Path(__file__).parent / DATA_FOLDER / filename
    with open(filepath) as fp:
        data = json.load(fp)
        return data[key]


# Load the data once at startup and keep it in memory. Views mutate these
# same list objects (e.g. deducting booked spots), so changes persist across
# requests for the lifetime of the process.
_clubs = _json_from_file("clubs.json", "clubs")
_competitions = _json_from_file("competitions.json", "competitions")


def get_clubs():
    """Return the in-memory list of clubs"""
    return _clubs


def get_competitions():
    """Return the in-memory list of competitions"""
    return _competitions


# Spots each club has already booked in each competition, keyed by
# (club name, competition name). Held in memory like the data above, so it
# lasts for the lifetime of the process.
_bookings = {}


def get_booked_spots(club_name, competition_name):
    """How many spots this club has already booked in this competition"""
    return _bookings.get((club_name, competition_name), 0)


def record_booking(club_name, competition_name, spots):
    """Add spots to this club's running total for the competition"""
    key = (club_name, competition_name)
    _bookings[key] = _bookings.get(key, 0) + spots


def reset_bookings():
    """Forget every recorded booking (used to isolate tests)"""
    _bookings.clear()
