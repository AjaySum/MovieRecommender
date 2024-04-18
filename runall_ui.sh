#!/bin/bash
set -Eeuo pipefail
set -x  # print commands

cd movrec
./bin/movrecrun
cd ..