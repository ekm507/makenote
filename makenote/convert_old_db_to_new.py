import sqlite3
import os



def list_tables(sqlite_cursor: sqlite3.Cursor):
    try:
        # get list of tables
        records = sqlite_cursor.execute(
            'SELECT name from sqlite_master where type= "table"')
        # print them
        for r in records:
            print(r[0])
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
        for r in records:
            i += 1
            print(i, end="  ")

            # if style number 1 is selected
            if show_style == 1:
                # replace that utf representation of نیم‌فاصله with itself
                r[1].replace('\u200c', ' ')
                # remove miliseconds from date and time and print a in a stylized format
                print(f'{r[0][:10]}   {r[0][10:18]}    {r[1]}')
            
            elif show_style == 2:
                print(f'\u001b[36m{r[0][:10]} {r[0][10:18]}\u001b[0m  {r[1]}')

            # if no show style is specified
            else:
                # print in python default style of printing
                print(r)
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
    pass