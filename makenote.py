#!/usr/bin/python3
import sys
import time
import os
import sqlite3
import datetime

# database file is stored here.
diaryFileName = f'{os.getenv("HOME")}/.diaryFile.db'

# default table name
default_table_name = 'journals'

# this program can do a few things. action mode tells it what to do!
action_mode = 'make note'

# connect to sqlite file
con = sqlite3.connect(diaryFileName)
# define a cursor to execute commands
cur = con.cursor()

# get note text to write into database.
try:
    # get note text from args if provided
    note_text = ' '.join(sys.argv[1:])
except IndexError:
    # if note text is not provided in args, get it from stdin.
    note_text = ''.join(sys.stdin.readlines())[:-1]


if action_mode == 'make note':
    pass
