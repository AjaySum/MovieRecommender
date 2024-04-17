cd movrec
./bin/install
python3 preprocess.py movies_dataset.csv
python3 similarities.py
python3 calculate.py
cd ..