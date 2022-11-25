[نسخه فارسی این سند](./fa.README.md)

makenote
---

a command line tool for making diary or journals.

[![asciicast](https://asciinema.org/a/eOzmHs0kk7qFZeuWyHE8HezaJ.svg)](https://asciinema.org/a/eOzmHs0kk7qFZeuWyHE8HezaJ)

# installation

there are a few methods for installation

## using pip
easiest way is to install it using pip:

1. install package
```bash
pip install makenote
```

2. add `~/.local/bin` to path if needed. ([help](https://linuxize.com/post/how-to-add-directory-to-path-in-linux/))

## build for pip

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
3. add `~/.local/bin` to path if needed. ([help](https://linuxize.com/post/how-to-add-directory-to-path-in-linux/))


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

# usage


## adding notes

to add note to a specified table, run this:
```bash
makenote [-t <table_name>] <note_text>
```

in which note text is the note you want to be added.

for example:
```bash
makenote I am reading page 754 of the book
```

this tool can also get input from stdin. so you can add notes like this:
```bash
echo "I installed makenote tool" | makenote --table journals
```

if you do not specify table_name, then note will be stored in default table which is `journals`.



## creating tables

this tool uses different tables for storing notes.  
for example you can classify your notes in "journals", "tasks", "work", etc.

to create a table, run this:
```bash
makenote --create <table_name>
```
in which `<table_name>` is the name of table you want to be created.

## listing tables

to get a list of tables you have created, run this:
```bash
makenote --list
```

## showing records

to see the notes you have stored in a table, run this:
```bash
makenote --show [<table_name>]
```
if you do not specify table_name, the default table will be shown.

## getting help

run:

```bash
makenote -h
```