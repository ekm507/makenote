"""Regression tests: missing databases directory must not crash the CLI.

`table_exists()` (used by the CLI before offering to create a notebook) calls
`get_books_list()`, which passed the directory straight to `os.listdir()`.
On a fresh setup — or after the databases directory was removed — that
raised an unhandled `FileNotFoundError` instead of reporting "no notebooks".
"""
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_DIR))

from makenote.dbmanager import get_books_list, table_exists


def test_get_books_list_missing_directory(tmp_path):
    assert get_books_list(str(tmp_path / 'no-such-dir')) == []


def test_table_exists_missing_directory(tmp_path):
    assert table_exists(str(tmp_path / 'no-such-dir'), 'journals') is False


def test_table_exists_after_make_book(tmp_path):
    from makenote.dbmanager import make_book

    make_book(str(tmp_path), 'journals')
    assert table_exists(str(tmp_path), 'journals') is True
    assert get_books_list(str(tmp_path)) == ['journals']
