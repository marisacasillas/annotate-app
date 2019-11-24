from datetime import datetime

from .dbcontext import dbconn


class File(object):

    def __init__(self, row):
        self.id = int(row['id'])
        self.name = row['name']
        self.annotation = row['annotation'] or u''
        self.complete = int(row['complete']) == 1
        self.user = row['user']
        self.completed_at = row['completed_at']

    def save(self, user):
        with dbconn() as db:
            q = """
                UPDATE `files` SET
                    annotation = ?,
                    complete = 1,
                    userid = (SELECT `id` FROM `users` WHERE `name` = ?),
                    completed_at = datetime('now', 'localtime')
                WHERE `id` = ?
            """
            p = (self.annotation, user, self.id)
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


def next_incomplete():
    with dbconn() as db:
        q = """
            SELECT *, NULL AS `user`
            FROM `files`
            WHERE NOT `complete`
            ORDER BY `name` ASC
            LIMIT 1
        """
        r = db.execute(q).fetchone()
        if r is not None:
            return File(r)
        return None


def around(fileid):
    context = {}
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


def user_stats(name):
    with dbconn() as db:
        q = """
            SELECT
                CASE
                WHEN date(f.`completed_at`, 'localtime')
                    = date('now', 'localtime') THEN 'user_today'
                ELSE 'user_complete'
                END AS 'stat',
                COUNT(*) AS 'count'
            FROM `files` f
            JOIN `users` u ON
                u.`id` = f.`userid`
                AND u.`name` = ?
            WHERE f.`complete`
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
            FROM `files` 
            WHERE NOT `complete`
        """
        return db.execute(q).fetchone()['remaining']
