#!/usr/bin/env python3

import argparse
import datetime
import os
import sys

from annotate.config import DB_FILE
from annotate.database import export_files_to_csv

db_filename = os.path.splitext(os.path.basename(DB_FILE))[0]
timestamp = datetime.datetime.now().strftime("%Y%m%d%-H%M%S")
default_db = f'{db_filename}-{timestamp}.csv'

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outfile', default=default_db)
args = parser.parse_args()

try:
    with open(args.outfile, 'w') as fh:
        export_files_to_csv(fh)
except IOError as e:
    print(e, file=sys.stderr)
