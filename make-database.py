#!/usr/bin/env python

import sys

from annotate.database import create_database

create_database(sys.argv[1])
