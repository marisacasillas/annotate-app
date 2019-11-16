import os


DB_FILE = os.path.join('var', 'database.db')

DB_BACKUP_DIR = os.path.join('var', 'backups')

# Back up the database after completing N annotations (based solely on the
# annotation number). So, if it were set to 5, we'd create a backup after
# setting an annotation for file 5, file 10, file 15, and so on.
BACKUP_EVERY_N = 500

MP3_GLOB = os.path.join('static', 'snippets', '*.mp3')

USERS = set([u'usuario1', u'usuario2'])
