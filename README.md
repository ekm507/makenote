[نسخه فارسی این سند](./fa.README.md)

makenote
---

a command line tool for making diary or journals.

[![asciicast](https://asciinema.org/a/eOzmHs0kk7qFZeuWyHE8HezaJ.svg)](https://asciinema.org/a/eOzmHs0kk7qFZeuWyHE8HezaJ)

# installation

## using pip

1. build the package

```bash
pip install setuptools wheel
git clone 'https://github.com/ekm507/makenote'
cd makenote
python3 setup.py bdist_wheel

```

2. install the package
```bash
pip install ./dist/*.whl
```

## without pip (old method)

1. clone this repo and `cd` into it.
2. run `install_local.sh`
3. add `~/.local/bin` to `PATH` if needed.


<!-- old method
### pre-requirements

first make sure dependancies for this tool are satisfied.  
this tool needs sqlite3 to run. in debian based distributions, install it with this:

```bash
apt install sqlite3
```

### install

first clone this repo :

```bash
git clone 'https://github.com/ekm507/makenote.git'
```

then run `install.sh` as __root__ :
```bash
./install.sh
``` -->

## usage

### creating tables

this tool uses different tables for storing notes.  
for example you can classify your notes in "journals", "tasks", "work", etc.

to create a table, run this:
```bash
makenote --create <table_name>
```
in which `<table_name>` is the name of table you want to be created.

### adding notes

to add note to a specified table, run this:
```bash
makenote -t <table_name> <note_text>
```
in which note text is the note you want to be added.

this tool can also get input from stdin. so you can add notes like this:
```bash
echo "I installed makenote tool" | makenote --table journals
```

if you do not specify table_name, then note will be stored in default table which is `journals`.

### listing tables

to get a list of tables you have created, run this:
```bash
makenote --list
```

### showing records

to see the notes you have stored in a table, run this:
```bash
makenote --show <table_name>
```
<!-- if you do not specify table_name, the default table will be shown. -->
