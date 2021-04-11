# makenote
a command line tool for making diary or journals.

<div dir="rtl">
یک ابزار خط فرمان برای نوشتن یادداشت‌ها، نوشته‌های روزمره، گزارش‌کار و غیره.

برای دیدن توضیحات فارسی به فایل [fa.README.md](./fa.README.md) نگاه کنید.
</div>

## installation

first clone this repo :

```bash
git clone 'https://github.com/ekm507/makenote.git'
```

then run `install.sh` as __root__ :
```bash
./install.sh
```

## usage

### creating tables

this tool uses different tables for storing notes.  
for example you can classify your notes in "journals", "tasks", "work", etc.

to create a table, run this:
```bash
makenote -create <table_name>
```
in which `<table_name>` is the name of table you want to be created.

### adding notes

to add note to a specified table, run this:
```bash
makenote +<table_name> <note_text>
```
in which note text is the note you want to be added.

this tool can also get input from stdin. so you can add notes like this:
```bash
echo "I installed makenote tool" | makenote +journals
```

if you do not specify table_name, then note will be stored in default table which is `journals`.

### listing tables

to get a list of tables you have created, run this:
```bash
makenote -list
```

### showing records

to see the notes you have stored in a table, run this:
```bash
makenote -show <table_name>
```
if you do not specify table_name, the default table will be shown.
