#!/bin/bash
ln -s /usr/bin/makenote "$(pwd)"/makenote.py
makenote -create journals
