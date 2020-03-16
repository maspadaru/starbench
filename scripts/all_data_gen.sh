#!/bin/bash

DATA_DIR=../benchmark/data/lars
mkdir -p $DATA_DIR 

pypy gen_seq.py 1000 1000 1 2 > $DATA_DIR/seq_1k_1k_1_2.stream
pypy gen_seq.py 100 100 1 2 > $DATA_DIR/seq_100_100_1_2.stream
pypy gen_seq.py 100 1000 1 2 > $DATA_DIR/seq_100_1k_1_2.stream
pypy gen_seq.py 1000 1000 2 2 > $DATA_DIR/seq_1k_1k_2_2.stream
pypy gen_seq.py 10 100 2 2 > $DATA_DIR/seq_10_100_2_2.stream
pypy gen_seq.py 10 1000 2 2 > $DATA_DIR/seq_10_1k_2_2.stream
pypy gen_seq.py 10 10000 2 2 > $DATA_DIR/seq_10_10k_2_2.stream
pypy gen_seq.py 10 100000 2 2 > $DATA_DIR/seq_10_100k_2_2.stream
pypy gen_seq.py 100 1000 2 2 > $DATA_DIR/seq_100_1k_2_2.stream
