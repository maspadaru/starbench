#!/bin/bash

# Assumes it will find chasebench in ../../chasebench

SCRIPTS_DIR=scripts
BENCHMARK_DIR=benchmark
CHASE_DATA_DIR=benchmark/data/chase
CHASE_PROGRAM_DIR=benchmark/program/chase
LARS_DATA_DIR=benchmark/data/lars
LARS_PROGRAM_DIR=benchmark/program/lars
PREMADE_DIR=premade/program/lars

rm -rf $BENCHMARK_DIR
mkdir -p $CHASE_DATA_DIR 
mkdir -p $CHASE_PROGRAM_DIR 
mkdir -p $LARS_DATA_DIR 
mkdir -p $LARS_PROGRAM_DIR 
cp $PREMADE_DIR/* $LARS_PROGRAM_DIR/
cd $SCRIPTS_DIR/
./all_data_gen.sh
./cbconvert.sh
cd ..
