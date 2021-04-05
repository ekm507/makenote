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

if action_mode == 'make note':
    pass
