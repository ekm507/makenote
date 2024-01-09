#!/bin/bash

python3 -m pip install -r requirements.txt
cp bin/makenote ~/.local/bin/makenote
mkdir -p ~/.local/share/makenote
cp makenote/makenote.conf ~/.local/share/makenote/