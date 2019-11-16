import sqlite3
from contextlib import contextmanager

from . import database


connection = None


@contextmanager
def dbconn(commit=True):
    global connection
    if connection is None:
        connection = sqlite3.connect(
                database.DB_FILE,
                detect_types=sqlite3.PARSE_DECLTYPES)
        connection.row_factory = sqlite3.Row
    yield connection
    if commit:
        connection.commit()
