#!/bin/bash
set -Eeuo pipefail
set -x  # print commands

cd movrec
python3 -m venv env
./bin/install
./bin/movrecrun
cd ..