"""Insta485 development configuration."""
import pathlib
# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'
# Database file is var/insta485.sqlite3
SEARCH_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DATABASE_FILENAME = SEARCH_ROOT/'var'/'film.sqlite3'
SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/recommend/"
]
