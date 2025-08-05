#!/bin/bash

# download and unpack G2P models
mkdir -p data/g2p-nb
wget -P download -c https://github.com/Sprakbanken/g2p-nb/releases/download/v2.0/models.zip
unzip -o download/models.zip
mv models/*.fst data/g2p-nb

# download audio datasets
wget -P data/nb_samtale/data -c --content-disposition "https://huggingface.co/datasets/Sprakbanken/nb_samtale/resolve/2ebb4dd9ca819a3443d4759516b09a531bb54976/data/test_metadata.jsonl?download=true"
wget -P data/nb_samtale/data -c --content-disposition "https://huggingface.co/datasets/Sprakbanken/nb_samtale/resolve/2ebb4dd9ca819a3443d4759516b09a531bb54976/data/train_metadata.jsonl?download=true"
wget -P data/nb_samtale/data -c --content-disposition "https://huggingface.co/datasets/Sprakbanken/nb_samtale/resolve/2ebb4dd9ca819a3443d4759516b09a531bb54976/data/validation_metadata.jsonl?download=true"
wget -P download -c --content-disposition "https://huggingface.co/datasets/Sprakbanken/nb_samtale/resolve/2ebb4dd9ca819a3443d4759516b09a531bb54976/data/test_bm_1.tar.gz?download=true"
wget -P download -c --content-disposition "https://huggingface.co/datasets/Sprakbanken/nb_samtale/resolve/2ebb4dd9ca819a3443d4759516b09a531bb54976/data/test_nn_1.tar.gz?download=true"
wget -P download -c --content-disposition "https://huggingface.co/datasets/Sprakbanken/nb_samtale/resolve/2ebb4dd9ca819a3443d4759516b09a531bb54976/data/train_bm_1.tar.gz?download=true"
wget -P download -c --content-disposition "https://huggingface.co/datasets/Sprakbanken/nb_samtale/resolve/2ebb4dd9ca819a3443d4759516b09a531bb54976/data/train_nn_1.tar.gz?download=true"
wget -P download -c --content-disposition "https://huggingface.co/datasets/Sprakbanken/nb_samtale/resolve/2ebb4dd9ca819a3443d4759516b09a531bb54976/data/validation_bm_1.tar.gz?download=true"
wget -P download -c --content-disposition "https://huggingface.co/datasets/Sprakbanken/nb_samtale/resolve/2ebb4dd9ca819a3443d4759516b09a531bb54976/data/validation_nn_1.tar.gz?download=true"

# unpack audio datasets
tar -xzf download/test_bm_1.tar.gz -C data/nb_samtale
tar -xzf download/test_nn_1.tar.gz -C data/nb_samtale
tar -xzf download/train_bm_1.tar.gz -C data/nb_samtale
tar -xzf download/train_nn_1.tar.gz -C data/nb_samtale
# the file ending of these is a lie, they are just tar files.
tar -xf download/validation_bm_1.tar.gz -C data/nb_samtale
tar -xf download/validation_nn_1.tar.gz -C data/nb_samtale

# create audio database
cd data/nb_samtale
python make_wordlist.py
cd -

# download and prepare pronunciation database
wget -P download -c https://www.nb.no/sbfil/uttaleleksikon/nb_uttale_leksika.zip
unzip -o download/nb_uttale_leksika.zip -d data
cd data/nb_uttale_leksika
python create_sql_db.py
cd -

# clean up
rm -rf download models data/nb_samtale/*.jsonl data/nb_uttale_leksika/*.csv
