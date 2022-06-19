import csv
import itertools
import os
import shutil
import sqlite3

from datetime import datetime

from .config import DB_FILE, DB_BACKUP_DIR, USERS
from .files import iter_files


class FileNotFoundError(IOError):
    pass


def user_exists(name):
    return name.lower() in USERS


def create_database(transcription_csv_path):
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
            `transcription` TEXT NOT NULL,
            `word` TEXT NOT NULL,
            `audio_quality` INTEGER NOT NULL DEFAULT 1,
            `onset_accuracy` INTEGER NOT NULL DEFAULT 1,
            `offset_accuracy` INTEGER NOT NULL DEFAULT 1,
            `word_present` BOOL NOT NULL DEFAULT 1,
            `correct_wordform` BOOL NOT NULL DEFAULT 1,
            `speaker` CHARACTER(1) NOT NULL DEFAULT 'A',
            `addressee` CHARACTER(1) NOT NULL DEFAULT 'C',
            `checked` BOOL NOT NULL DEFAULT 0,
            `checked_at` TIMESTAMP,
            `userid` INTEGER REFERENCES `users` (`id`)
                ON DELETE SET NULL ON UPDATE SET NULL
        )""")
    populate_users(cur)
    populate_files(cur, transcription_csv_path)
    con.commit()
    con.close()


def populate_users(cur):
    def users():
        for u in USERS:
            yield (u,)
    q = """INSERT INTO `users` (`name`) VALUES (?)"""
    cur.executemany(q, users())


def populate_files(cur, transcription_csv_path):
    def files():
        for tr in iter_transcriptions(transcription_csv_path):
            if not os.path.isfile(f"static/snippets/{tr['filename']}"):
                raise FileNotFoundError(tr['filename'])
            without_ext = os.path.splitext(tr['filename'])[0]
            yield (without_ext, tr['transcription'], tr['word'])
    q = """INSERT INTO `files` (`name`, `transcription`, `word`) VALUES (?, ?, ?)"""
    for chunk in chunk_iter(files(), 500):
        cur.executemany(q, chunk)


def iter_transcriptions(csv_path):
    with open(csv_path) as csvfile:
        yield from csv.DictReader(csvfile)


def backup_database():
    backup_file = '{}.db'.format(datetime.now().strftime('%Y-%m-%d-%H%M'))
    backup_path = os.path.join(DB_BACKUP_DIR, backup_file)
    shutil.copyfile(DB_FILE, backup_path)


def export_files_to_csv(fh):
    writer = csv.writer(fh)
    writer.writerow(['user', 'checked', 'checked_at', 'filename', 'transcription', 'word',
        'audio_quality', 'onset_accuracy', 'offset_accuracy', 'word_present', 'correct_wordform',
        'speaker', 'addressee',
        ])
    for f in iter_files():
        r = [f.user, f.checked, f.checked_at, f.name, f.transcription, f.word, f.audio_quality,
                f.onset_accuracy, f.offset_accuracy, f.word_present, f.correct_wordform, f.speaker,
                f.addressee]
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
