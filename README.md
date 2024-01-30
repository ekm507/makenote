[نسخه فارسی این سند](./fa.README.md)

makenote
---

a command line tool for making diary or journals.

# installation

there are a few methods for installation

## using pip
easiest way is to install it using pip:

1. install package
```bash
pip install makenote
```

for some new Gnu distros you need to use `pipx`.

```bash
pipx install makenote
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

# usage


## adding notes

to add note to a specified notebook, run this:
```bash
makenote [-t <notebook_name>] <note_text>
```

in which note text is the note you want to be added.

for example:
```bash
makenote I am reading page 754 of the book
```

if you run this tool with no text, it will get note text from a simple prompt editor. write your text and then hit `Alt+Enter` or `ctrl+D`.

```
$ makenote

it was a great day.
I had a pizza with my friend. (ctrl+D)

1728 - Tue, 10 Bah 1402 18:55:25 - journals - note saved!
```

if you do not specify notebook name, then note will be stored in default notebook which is `journals`. you can change it in config file.



## creating notebooks

this tool uses different notebooks for storing notes.  
for example you can classify your notes in "journals", "tasks", "work", etc.

to create a notebook, run this:
```bash
makenote --create <notebook_name>
```
in which `<notebook_name>` is the name of notebook you want to be created.

## listing notebooks

to get a list of notebooks you have created, run this:
```bash
makenote --list
```

## showing records

to see the notes you have stored in a notebook, run this:
```bash
makenote --show
```

if you do not specify notebook name, the default notebook will be shown. you can specify it with `-t` switch:

```bash
makenote --show -t <notebook>
```

## getting help

run command below to get a list of switches:

```bash
makenote -h
```


# export all notes
database file is stored in path below:

`~/.local/share/makenote/databases/diaryFile.db`

for backing notes up, just copy the file into somewhere.

for restoring, just copy the `diaryFile.db` into the path.