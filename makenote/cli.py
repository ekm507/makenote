import sys
import os
import sqlite3
import datetime
import argparse
import shutil
import configparser
import jdatetime

import dbmanager
from dbmanager import *


# read config file
# TODO: try to read config from another local dir first. then go to default file

__version__ = "2.0"

possible_config_filenames = [
    "./makenote.conf",
    os.path.expanduser('~') + ".local/share/makenote/makenote.conf",
    os.path.dirname(__file__)+'/makenote.conf',
]
for possible_name in possible_config_filenames:
    if not os.path.exists(possible_name):
        continue
    else:
        config_filename = possible_name
        
config = configparser.ConfigParser()
config.read(config_filename)

# database file is stored here.
diaryFileDir = os.path.abspath(config['FILES']['diaryFileDir'].replace("~/", f'{os.getenv("HOME")}/'))

default_table_name = config['FILES']['default_table_name']
# default table name

show_jalali = config['SHOW_STYLE'].getboolean('show_jalali')

if sys.stdout.isatty() == True:
    # this number is like an option for how the show record output is styled
    show_style = 2
else:
    show_style = 1


parser = argparse.ArgumentParser(prefix_chars='-', prog='makenote',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='add notes to diary or show them',
                                 epilog='''examples:
    makenote -t journals it was a nice day today!
    makenote -show journals''')

parser.add_argument("-s", '--show', dest='show',
                    help="table to show", nargs='?', const=default_table_name, metavar='TABLE_NAME')
parser.add_argument("-T", '--tail', dest='tail',
                    help="show last 10 items of table", nargs='?', const=default_table_name, metavar='TABLE_NAME')
# parser.add_argument("-d", '--default', dest='default',
#                     help="set default table", default=None)
parser.add_argument("-c", '--create', dest='create_table',
                    help="create table", default=None, metavar='TABLE_NAME')
parser.add_argument("-l", '--list', dest='list_tables',
                    help="list tables", default=None, action="store_true")
parser.add_argument("-t", "--table", dest="table_name", help="table for notes",
                    default=default_table_name)
parser.add_argument("-m", "--merge",  help="merge two databases",
                    default=None, nargs=3, metavar=('FIRST','SECOND','OUTPUT'))
parser.add_argument("-x", "--export",  help="export database into file",
                    default=None, metavar='FILENAME')
parser.add_argument("-i", "--import",  help="import database",
                    default=None, dest='import_file', metavar='FILENAME')
parser.add_argument("text",  help="text", default=None, nargs='*')

parser.add_argument("-u", "--update",  help="edit note. add entry number. last note is edited if no number is given",
                    default=None, const="-1", nargs="?", metavar='note_id', type=int)
parser.add_argument('-V', '--version', action='version', version="%(prog)s "+__version__)
args = parser.parse_args()





os.makedirs(os.path.dirname(diaryFileDir), exist_ok=True)
# connect to sqlite file

if args.show:
    show_table(diaryFileDir, args.show)
elif args.tail:
    tail_show_table(diaryFileDir, args.tail, limit=10)
elif args.list_tables:
    list_tables(diaryFileDir)
elif args.create_table:
    make_book(diaryFileDir, args.create_table)
elif args.export:
    shutil.copy(diaryFileName, args.export)
    print(f'exported to {os.path.realpath(args.export)}')
elif args.import_file:
    import_database(args.import_file, diaryFileName)

elif args.merge:
    firstdb, seconddb, outdb = args.merge
    merge_databases_by_name(firstdb, seconddb, outdb)
# elif args.default:
#     default_table_name = args.default
#     table_name = args.default

else:

    # note will be added to this table
    table_name = args.table_name
    if not table_exists(diaryFileDir, table_name):
        print(f'table {table_name} does not exist')
        print('do you want to create it? (y/N)')
        do_you_want_to_create = input()
        if do_you_want_to_create.lower() in ['y', 'yes']:
            make_book(diaryFileDir, table_name)
        else:
            exit(1)

    if len(args.text) > 0:
        note_text = ' '.join(args.text)
    else:
        previous_text = ''
            
        try:
            from prompt_toolkit import prompt
            from prompt_toolkit import PromptSession
            from prompt_toolkit.key_binding import KeyBindings
            session = PromptSession()
            bindings = KeyBindings()
            @bindings.add('c-d')
            def _(event):
                " Exit when `c-d` is pressed. "
                session.history.append_string(event.app.current_buffer.text)
                event.app.exit(result=event.app.current_buffer.text)

            note_text = prompt(multiline=True, default=previous_text, key_bindings=bindings)
        except KeyboardInterrupt:
            exit(1)

    if args.update:
        update_entry(diaryFileDir, args.table_name, args.update, note_text)
    else:
        add_note(diaryFileDir, table_name, note_text)
