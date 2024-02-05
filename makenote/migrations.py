import sqlite3
import os
import datetime
from makenote.dbmanager import make_book, add_note
import configparser
import shutil
import json

def list_tables(sqlite_cursor: sqlite3.Cursor):
    try:
        # get list of tables
        records = sqlite_cursor.execute(
            'SELECT name from sqlite_master where type= "table"')
        
        tables = []

        for r in records:
            tables.append(r[0])
        
        return tables
    # if there was an error, print error text and exit
    except sqlite3.OperationalError as error_text:
        print(error_text)
        exit(1)

def show_table(sqlite_cursor, table_name):
    try:
        # get records from sqlite
        records = sqlite_cursor.execute(f"SELECT * FROM {table_name};")
        # print them all
        i = 0
        records_list = []
        for r in records:
            records_list.append((r[0], r[1]))

        return records_list
    # if there was an error, print error text and exit
    except sqlite3.OperationalError as error_text:
        print(error_text)
        exit(1)

def merge_databases(cursor1:sqlite3.Cursor, cursor2:sqlite3.Cursor, cursor_out:sqlite3.Cursor):

    def add_table(cursor_in, cursor_out, table_name):
        cursor_out.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (date datetime, note text)''')
        table_data = cursor_in.execute(f"select * from {table_name};").fetchall()

        for entry in table_data:
            cursor_out.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (entry[0], entry[1]))
  

    def merge_tables(cursor1:sqlite3.Cursor, cursor2:sqlite3.Cursor, cursor_out:sqlite3.Cursor, table_name):


        table_1 = cursor1.execute(f"select * from {table_name};").fetchall()
        table_2 = cursor2.execute(f"select * from {table_name};").fetchall()

        table_out = []
        last_index_table2 = 0
        for entry_1 in table_1:
            for entry_2 in table_2[last_index_table2:]:
                # print(x[0], y[0], x[0] > y[0])
                if entry_1[0] > entry_2[0]:
                    table_out.append(entry_2)
                    # print(i)
                    last_index_table2 += 1
                else:
                    break
            table_out.append(entry_1)
        for entry_2 in table_2[last_index_table2:]:
            table_out.append(entry_2)


        cursor_out.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (date datetime, note text)''')
        for entry in table_out:
            cursor_out.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (entry[0], entry[1]))
    

    tables_1 = cursor1.execute('SELECT name from sqlite_master where type= "table"').fetchall()
    tables_2 = cursor2.execute('SELECT name from sqlite_master where type= "table"').fetchall()
    for table_name in tables_1:
        if table_name in tables_2:
            merge_tables(cursor1, cursor2, cursor_out, table_name[0])
        else:
            add_table(cursor1, cursor_out, table_name[0])
    
    for table_name in tables_2:
        if table_name not in tables_1:
            add_table(cursor2, cursor_out, table_name[0])


def convert_old_db_to_new(old_database_filename:str, new_database_directory_name:str):

    cur_old = sqlite3.Connection(old_database_filename).cursor()
    tables = list_tables(cur_old)

    os.makedirs(os.path.dirname(new_database_directory_name), exist_ok=True)
    for table_name in tables:
        make_book(new_database_directory_name, table_name)
        entries = show_table(cur_old, table_name)
        for date, note in entries:
            date_and_time = datetime.datetime.fromisoformat(date)
            add_note(new_database_directory_name, table_name, note, date_and_time=date_and_time)
            print(date_and_time, date)


def is_db_version1(database_filename):
    # print(database_filename)
    cur = sqlite3.Connection(database_filename).cursor()
    tables = list_tables(cur)
    for table in tables:
        records = cur.execute(f"SELECT * FROM {table};")
        for r in records:
            if len(r) == 2:
                return True
    return False



def check_for_old_dbs(database_directory:str)->list:
    old_files = []
    for filename in os.listdir(database_directory):
        if filename.endswith('.db'):
            file_path = os.path.realpath(os.path.join(database_directory, filename))
            if is_db_version1(file_path):
                old_files.append(file_path)
    return old_files

def convert_diaryFile_version_1(database_directory):
    database_directory = os.path.realpath(database_directory)
    os.makedirs(database_directory, exist_ok=True)
    if 'diaryFile.db' in os.listdir(database_directory):
        old_file_path = os.path.realpath(os.path.join(database_directory, 'diaryFile.db'))
        new_file_path = os.path.realpath(os.path.join(database_directory, 'diaryFile.db.bak'))
        shutil.move(old_file_path, new_file_path)
        convert_old_db_to_new(new_file_path, database_directory)

def migrate_version_2(database_filename):
    con = sqlite3.Connection(database_filename)
    cur = con.cursor()

    metadata_encoded = cur.execute("select * from metadata;").fetchone()[0]
    metadata = json.loads(metadata_encoded.decode("utf-8"))

    book_name = metadata["name"]

    cur.execute(f"SELECT rowid FROM {book_name} order by rowid DESC LIMIT 1;")
    n = cur.fetchone()[0]

    for i in range(1, n+1):
        cur.execute(f"""UPDATE {book_name} SET number = "{i}" LIMIT {i-1},{1};""")

    con.commit()


def migrate_all_version_2_if_needed(database_directory):
    for filename in os.listdir(database_directory):
        if filename.endswith('.db'):
            database_filename = os.path.realpath(os.path.join(database_directory, filename))
            con = sqlite3.Connection(database_filename)
            cur = con.cursor()

            metadata_encoded = cur.execute("select * from metadata;").fetchone()[0]
            metadata = json.loads(metadata_encoded.decode("utf-8"))
            book_name = metadata["name"]

            if metadata["version"] == "makenote V2":
                migrate_version_2(database_filename)
                metadata["version"] = "makenote V4"
                metadata_encoded = bytes(json.dumps(metadata), "utf-8")
                cur.execute(f"""UPDATE metadata SET metadata = ? ;""", (metadata_encoded,))
                con.commit()



def migrate_if_needed(config_filename):
    config = configparser.ConfigParser()
    config.read(config_filename)
    # database file is stored here.

    # migrate version 1 to 2
    if config['DATABASE'].getfloat('last_version') < 2.0:
        diaryFileDir = os.path.abspath(config['FILES']['diaryFileDir'].replace("~/", f'{os.getenv("HOME")}/'))
        convert_diaryFile_version_1(diaryFileDir)
        config['DATABASE']['last_version'] = "2.0"
        config.write(open(config_filename, 'w'))
        print("database migration from v1.0 to v2.0 done")

    # migrate version 2 to 4
    if config['DATABASE'].getfloat('last_version') < 3.0:
        diaryFileDir = os.path.abspath(config['FILES']['diaryFileDir'].replace("~/", f'{os.getenv("HOME")}/'))
        migrate_all_version_2_if_needed(diaryFileDir)
        config['DATABASE']['last_version'] = "4.0"
        config.write(open(config_filename, 'w'))
        print("database migration from v2.0 to v4.0 done")

