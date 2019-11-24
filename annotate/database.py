import csv
import itertools
import os
import shutil
import sqlite3

from datetime import datetime
from glob import iglob

from .config import DB_FILE, DB_BACKUP_DIR, MP3_GLOB, USERS
from .files import iter_files


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


def export_files_to_csv(fh):
    writer = csv.writer(fh)
    writer.writerow(['user', 'complete', 'completed_at',
        'filename', 'annotation'])
    for f in iter_files():
        r = [f.user, int(f.complete), f.completed_at, f.name, f.annotation]
        writer.writerow(r)


def chunk_iter(itr, size):
    """Chunk an iterable blocks of "size" each, except for the last chunk,
    which may have fewer elements.
    """
    itr = iter(itr)
    chunk = tuple(itertools.islice(itr, size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(itr, size))
