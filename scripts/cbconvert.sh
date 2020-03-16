#!/bin/bash

# Assumes it will find chasebench in ../../chasebench

DATA_DIR=../benchmark/data/chase
PROGRAM_DIR=../benchmark/program/chase

convert () {
    TIME=$1
    WINDOW=$2
    BOX=$3
    DIAMOND=$4
    EVENT=$5
    python cbparse.py S $TIME \
        ../../chasebench/scenarios/deep/100/data/ \
        > $DATA_DIR/deep100_${TIME}.stream
    python cbparse.py T $WINDOW $BOX $DIAMOND $EVENT \
        ../../chasebench/scenarios/deep/100/dependencies/ \
        > $PROGRAM_DIR/deep100_${WINDOW}_${BOX}_${DIAMOND}_${EVENT}.star
}

mkdir -p $DATA_DIR 
mkdir -p $PROGRAM_DIR 
convert 5 2 100 0 0
convert 5 2 0 100 0
convert 5 2 100 0 100
convert 5 2 0 100 100

