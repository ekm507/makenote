import sys
import os
import sqlite3
import datetime
import argparse
import shutil
import configparser
import jdatetime
from makenote import dbmanager
from makenote.dbmanager import *
from makenote.convert_old_db_to_new import migrate_if_needed

# read config file
# TODO: try to read config from another local dir first. then go to default file

from makenote import __version__

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

migrate_if_needed(config_filename)

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
                    help="show notes from certain category", nargs='?', const=-1, type=int ,metavar='CATEGORY')
parser.add_argument("-C", '--category', dest='set_category',
                    help="set category of notes", default=-1, type=int ,metavar='CATEGORY')
parser.add_argument("-T", '--tail', dest='tail',
                    help="show last items of table", nargs='?', type=int,const=10, metavar='LIMIT')
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
# parser.add_argument("-q", "--query",  help="search for text. in regex",
#                     default=None, dest='query')
parser.add_argument("text",  help="text", default=None, nargs='*')

parser.add_argument("-u", "--update",  help="edit note. add entry number. last note is edited if no number is given",
                    default=None, const="-1", nargs="?", metavar='note_id', type=int)
parser.add_argument('-V', '--version', action='version', version="%(prog)s "+__version__)
args = parser.parse_args()





os.makedirs(os.path.dirname(diaryFileDir), exist_ok=True)
# connect to sqlite file

if args.show is not None:
    show_table_with_category(diaryFileDir, args.table_name, category=args.set_category)
elif args.tail:
    tail_show_table(diaryFileDir, args.table_name, limit=args.tail)
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

elif args.set_category != -1:
    if args.update is not None:
        set_category(diaryFileDir, args.table_name, args.update, args.set_category)

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
        if args.update:
            previous_text = get_note(diaryFileDir, args.table_name, args.update)
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
