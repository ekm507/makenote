#!/usr/bin/python3
import sys
import os
import sqlite3
import datetime
import argparse


# default table name
default_table_name = 'journals'

parser = argparse.ArgumentParser(prefix_chars='-', prog='makenote',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='add notes to diary or show them',
                                 epilog='''examples:
    makenote +journals it was a nice day today!
    makenote -show journals''')

parser.add_argument("-s", '--show', dest='show',
                    help="table to show", default=None)
parser.add_argument("-d", '--default', dest='default',
                    help="set default table", default=None)
parser.add_argument("-l", '--list', dest='list_tables',
                    help="list tables", default=None, action="store_true")
parser.add_argument("table_name",  help="+table for notes (starts with +)",
                    default=default_table_name, nargs='?')
parser.add_argument("text",  help="text", default=None, nargs='*')

args = parser.parse_args()


def add_note(sqlite_cursor, table_name, note_text):
    
    date_and_time = datetime.datetime.now()

    sqlite_cursor.execute(
        f"INSERT INTO {table_name} VALUES ('{date_and_time}','{note_text}')")

    # let user know it works
    print(f'{datetime.datetime.ctime(date_and_time)} - {table_name} - note saved!')


def show_table(sqlite_cursor, table_name):
    try:
        # get records from sqlite
        records = sqlite_cursor.execute(f"SELECT * FROM {table_name};")
        # print them all
        for r in records:

            # if style number 1 is selected
            if show_style == 2:
                # replace that utf representation of نیم‌فاصله with itself
                r[1].replace('\u200c', ' ')
                # remove miliseconds from date and time and print a in a stylized format
                print(f'{r[0][:10]}   {r[0][10:18]}    {r[1]}')
            # if no show style is specified
            else:
                # print in python default style of printing
                print(r)
    # if there was an error, print error text and exit
    except sqlite3.OperationalError as error_text:
        print(error_text)
        exit(1)

def table_exists(sqlite_cursor: sqlite3.Cursor, table_name) -> bool:
    query = 'SELECT name from sqlite_master where type= "table"'
    # query = f"SELECT tableName FROM sqlite_master WHERE type='table' AND tableName='{table_name}';"
    records = sqlite_cursor.execute(query)
    # print([t for t in tables])
    tables = [record[0] for record in records]
    return table_name in tables


def make_table(sqlite_cursor: sqlite3.Cursor, table_name):
    try:
        # create the table!
        sqlite_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
                    (date datetime, note text)''')
        # tell the user it was successful
        print(f'table {table_name} created!')
    except sqlite3.OperationalError as error_text:
        print(error_text)
        exit(1)

def list_tables(sqlite_cursor: sqlite3.Cursor):
    try:
        # get list of tables
        records = cur.execute(
            'SELECT name from sqlite_master where type= "table"')
        # print them
        for r in records:
            print(r[0])
    # if there was an error, print error text and exit
    except sqlite3.OperationalError as error_text:
        print(error_text)
        exit(1)



# database file is stored here.
diaryFileName = f'{os.getenv("HOME")}/.diaryFile.db'

# this number is like an option for how the show record output is styled
show_style = 1

# note will be added to this table
table_name = args.table_name

# connect to sqlite file
con = sqlite3.connect(diaryFileName)
# define a cursor to execute commands
cur = con.cursor()

if args.show:
    show_table(cur, args.show)
    exit(0)
elif args.list_tables:
    list_tables(cur)
    exit(0)
elif args.default:
    default_table_name = args.default
    table_name = args.default
else:
    if len(args.text) > 0:
        note_text = ' '.join(args.text)
    else:
        note_text = ''.join(sys.stdin.readlines())[:-1]

    add_note(cur, table_name, note_text)
    exit(0)

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
    # if you are commanded to create a table
    elif sys.argv[1] == '-create':
        try:
            # get table name
            table_name = sys.argv[2]
            # program should create a table then.
            action_mode = 'create table'
        # if table name is not provided, then exit
        except IndexError:
            exit(1)

    # if you are commanded to show records
    elif sys.argv[1] == '-show':
        # see if table name is provided. if not, default shall be used
        if len(sys.argv) > 2:
            table_name = sys.argv[2]
        # set action mode
        action_mode = 'show records'

    # if you are commanded to list tables
    elif sys.argv[1] == '-list':
        action_mode = 'list tables'

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
        cur.execute(
            f"INSERT INTO {table_name} VALUES ('{date_and_time}','{note_text}')")
        # let user know it works
        print(f'{datetime.datetime.ctime(date_and_time)} - {table_name} - note saved!')

    # if there is an error, print error text and exit.
    except sqlite3.OperationalError as error_text:
        print(error_text)
        exit(1)

# if you are commanded to create a table
elif action_mode == 'create table':
    try:
        # create the table!
        cur.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
                    (date datetime, note text)''')
        # tell the user it was successful
        print(f'table {table_name} created!')
    except sqlite3.OperationalError as error_text:
        print(error_text)
        exit(1)

# if you are commanded to show records
elif action_mode == 'show records':
    try:
        # get records from sqlite
        records = cur.execute(f"SELECT * FROM {table_name};")
        # print them all
        for r in records:

            # if style number 1 is selected
            if show_style == 1:
                # replace that utf representation of نیم‌فاصله with itself
                r[1].replace('\u200c', ' ')
                # remove miliseconds from date and time and print a in a stylized format
                print(f'{r[0][:10]}   {r[0][10:18]}    {r[1]}')
            # if no show style is specified
            else:
                # print in python default style of printing
                print(r)
    # if there was an error, print error text and exit
    except sqlite3.OperationalError as error_text:
        print(error_text)
        exit(1)

elif action_mode == 'list tables':
    try:
        # get list of tables
        records = cur.execute(
            'SELECT name from sqlite_master where type= "table"')
        # print them
        for r in records:
            print(r[0])
    # if there was an error, print error text and exit
    except sqlite3.OperationalError as error_text:
        print(error_text)
        exit(1)


# commit all changes in the database so they are saved.
con.commit()

# close the database file
con.close()
