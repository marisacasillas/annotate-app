#!/usr/bin/env python3

import argparse
import sys

from imco.session import ImcoSession

parser = argparse.ArgumentParser()
parser.add_argument('workdir', help="workdir containing database.db to convert")
parser.add_argument('-o', '--outfile', default='database.csv')
args = parser.parse_args()

try:
    s = ImcoSession(args.workdir)
    with open(args.outfile, 'w') as fh:
        s.export_to_csv(fh)
except IOError as e:
    print(e, file=sys.stderr)