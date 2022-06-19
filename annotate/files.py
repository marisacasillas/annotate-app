from datetime import datetime

from .dbcontext import dbconn


class File(object):

    def __init__(self, row):
        self.id = int(row['id'])
        self.name = row['name']
        self.transcription = row['transcription']
        self.word = row['word']
        self.audio_quality = row['audio_quality']
        self.onset_accuracy = row['onset_accuracy']
        self.offset_accuracy = row['offset_accuracy']
        self.word_present = row['word_present']
        self.correct_wordform = row['correct_wordform']
        self.speaker = row['speaker']
        self.addressee = row['addressee']
        self.checked = int(row['checked'])
        self.checked_at = row['checked_at']
        self.user = row['user']

    def save(self, user):
        with dbconn() as db:
            if self.checked == 1:
                update_checked_at = "datetime('now', 'localtime')"
            else:
                update_checked_at = 'NULL'
            q = f"""
                UPDATE `files` SET
                    audio_quality = ?,
                    onset_accuracy = ?,
                    offset_accuracy = ?,
                    word_present = ?,
                    correct_wordform = ?,
                    speaker = ?,
                    addressee = ?,
                    checked = ?,
                    checked_at = {update_checked_at},
                    userid = (SELECT `id` FROM `users` WHERE `name` = ?)
                WHERE `id` = ?
            """
            p = (self.audio_quality, self.onset_accuracy, self.offset_accuracy, self.word_present,
                    self.correct_wordform, self.speaker, self.addressee, self.checked, user,
                    self.id)
            db.execute(q, p)
            self.user = user


def iter_files():
    with dbconn() as db:
        q = """
            SELECT f.*, u.`name` AS `user`
            FROM `files` f
            LEFT JOIN `users` u ON u.`id` = f.`userid`
        """
        for r in db.execute(q):
            yield File(r)


def load_file(fileid):
    with dbconn() as db:
        q = """
            SELECT f.*, u.`name` AS `user`
            FROM `files` f
            LEFT JOIN `users` u ON u.`id` = f.`userid`
            WHERE f.`id` = ?
            LIMIT 1
        """
        p = (fileid,)
        r = db.execute(q, p).fetchone()
        return File(r)


def around(fileid):
    context = dict(prev=None, current=None, next=None)
    with dbconn() as db:
        q = """
            SELECT f.*, u.`name` AS `user`
            FROM `files` f
            LEFT JOIN `users` u ON u.`id` = f.`userid`
            WHERE f.`id` BETWEEN ? AND ?
        """
        p = (fileid - 1, fileid + 1)
        rows = db.execute(q, p).fetchall()
    for r in rows:
        if r['id'] < fileid:
            key = 'prev'
        elif r['id'] == fileid:
            key = 'current'
        else:
            key = 'next'
        context[key] = File(r)
    return context


def prev_unchecked(fileid):
    context = {}
    with dbconn() as db:
        q = """
            SELECT f.*, u.`name` AS `user`
            FROM `files` f
            LEFT JOIN `users` u ON u.`id` = f.`userid`
            WHERE NOT f.`checked` AND f.`id` < ?
            ORDER BY f.`id` DESC
            LIMIT 1
        """
        p = (fileid,)
        r = db.execute(q, p).fetchone()
        if r is not None:
            return File(r)
        return None


def last_unchecked():
    context = {}
    with dbconn() as db:
        q = """
            SELECT f.*, u.`name` AS `user`
            FROM `files` f
            LEFT JOIN `users` u ON u.`id` = f.`userid`
            WHERE NOT f.`checked`
            ORDER BY f.`id` DESC
            LIMIT 1
        """
        r = db.execute(q).fetchone()
        if r is not None:
            return File(r)
        return None


def next_unchecked(fileid):
    context = {}
    with dbconn() as db:
        q = """
            SELECT f.*, u.`name` AS `user`
            FROM `files` f
            LEFT JOIN `users` u ON u.`id` = f.`userid`
            WHERE NOT f.`checked` AND f.`id` > ?
            ORDER BY f.`id` ASC
            LIMIT 1
        """
        p = (fileid,)
        r = db.execute(q, p).fetchone()
        if r is not None:
            return File(r)
        return None


def user_stats(name):
    with dbconn() as db:
        q = """
            SELECT
                CASE
                WHEN date(f.`checked_at`, 'localtime')
                    = date('now', 'localtime') THEN 'user_today'
                ELSE 'user_complete'
                END AS 'stat',
                COUNT(*) AS 'count'
            FROM `files` f
            JOIN `users` u ON u.`id` = f.`userid` AND u.`name` = ?
            WHERE f.`checked`
            GROUP BY `stat`
        """
        stats = {
            'user_today': 0,
            'user_complete': 0,
            'remaining': remaining()
        }
        for r in db.execute(q, (name,)).fetchall():
            stat = r['stat']
            stats[stat] = r['count']
        stats['user_complete'] += stats['user_today']
        return stats

def remaining():
    with dbconn() as db:
        q = """
            SELECT COUNT(*) AS 'remaining'
            FROM `files` f
            WHERE NOT f.`checked`
        """
        return db.execute(q).fetchone()['remaining']
