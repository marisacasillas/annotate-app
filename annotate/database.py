import itertools
import os
import shutil
import sqlite3
from datetime import datetime
from glob import iglob

from .config import DB_FILE, DB_BACKUP_DIR, MP3_GLOB, USERS


def user_exists(name):
    return name.lower() in USERS

def create_database():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE `users` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `name` TEXT NOT NULL
        )""")
    cur.execute("""
        CREATE TABLE `files` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `name` TEXT NOT NULL,
            `annotation` TEXT,
            `complete` BOOL DEFAULT 0,
            `completed_at` TIMESTAMP,
            `userid` INTEGER REFERENCES `users` (`id`)
                ON DELETE SET NULL ON UPDATE SET NULL
        )""")
    populate_users(cur)
    populate_files(cur)
    con.commit()
    con.close()


def populate_users(cur):
    def users():
        for u in USERS:
            yield (u,)
    q = """INSERT INTO `users` (`name`) VALUES (?)"""
    cur.executemany(q, users())


def populate_files(cur):
    def files():
        for f in iglob(MP3_GLOB):
            base = os.path.basename(f)
            without_ext = os.path.splitext(base)[0]
            yield (without_ext,)
    q = """INSERT INTO `files` (`name`) VALUES (?)"""
    for chunk in chunk_iter(files(), 500):
        cur.executemany(q, chunk)


def backup_database():
    backup_file = '{}.db'.format(datetime.now().strftime('%Y-%m-%d-%H%M'))
    backup_path = os.path.join(DB_BACKUP_DIR, backup_file)
    shutil.copyfile(DB_FILE, backup_path)


def chunk_iter(itr, size):
    """Chunk an iterable blocks of "size" each, except for the last chunk,
    which may have fewer elements.
    """
    itr = iter(itr)
    chunk = tuple(itertools.islice(itr, size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(itr, size))
