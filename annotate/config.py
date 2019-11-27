import os

DB_FILE = os.path.join('var', 'database.db')

# Back up the database after completing N annotations (based solely on the
# annotation number). So, if it were set to 5, we'd create a backup after
# setting an annotation for file 5, file 10, file 15, and so on.
DB_BACKUP_DIR = os.path.join('var', 'backups')
BACKUP_EVERY_N = 500

MP3_GLOB = os.path.join('static', 'snippets', '*.mp3')

USERS = set([u'usuario1', u'usuario2'])

# A priority list of languages to use for UI messages. The first language for
# which a message is available will be used (no matter the locale, English is
# always the final fallback). Use a code matching one of the directory names
# directly under ./locale/
LANGUAGES = ['es']
