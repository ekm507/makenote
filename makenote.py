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

# note will be added to this table
table_name = default_table_name

# this program can do a few things. action mode tells it what to do!
action_mode = 'make note'

# connect to sqlite file
con = sqlite3.connect(diaryFileName)
# define a cursor to execute commands
cur = con.cursor()

# get note text to write into database.
if len(sys.argv) > 1:

    # if note should be inserted into a specific table
    if sys.argv[1][0] == '+':
        # get table name
        table_name = sys.argv[1][1:]
        if len(sys.argv) > 2:
            # get note text from args if provided
            note_text = ' '.join(sys.argv[2:])
        else:
            # if note text is not provided in args, get it from stdin.
            note_text = ''.join(sys.stdin.readlines())[:-1]
    else:
        # get note text from args if provided
        note_text = ' '.join(sys.argv[1:])

# if there is no args
else:
    # if note text is not provided in args, get it from stdin.
    note_text = ''.join(sys.stdin.readlines())[:-1]

# get date and time
date_and_time = datetime.datetime.now()

# if you are commanded to insert a note into database
if action_mode == 'make note':
    try:
        # insert (date, note) into database.
        cur.execute(f"INSERT INTO {table_name} VALUES ('{date_and_time}','{note_text}')")

    # if there is an error, print error text and exit.
    except sqlite3.OperationalError as error_text:
        print(error_text)
        exit(1)

# commit all changes in the database so they are saved.
con.commit()

# close the database file
con.close()
