#!/bin/bash
set -Eeuo pipefail
set -x  # print commands

cd movrec
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 calculate.py
cd ..