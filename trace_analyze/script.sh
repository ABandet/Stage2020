#!/bin/bash

source venv/bin/activate

current_path=$PWD
cd /tmp
starpu_fxt_tool -i prof_file_root_0
cp paje.trace $current_path
cd $current_path

python3 src/main.py paje.trace
python3 src/analyze.py
