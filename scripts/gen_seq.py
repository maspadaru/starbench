'''
This script generates tuples that can be used for benchmarking. 
Values are in sequential order, for instance:
    << p(1, 2), q(1, 2), p(3, 4), q(3, 4) >>
The total number of tuples generated can be set using arguments.
Each tuple has a random predicate from the set: ('p', 'q', 'r', 's', 't', 
'u', 'v', 'w').
All predicates have the same arity, specified by the user in a command line 
arguments. 
The generated tuples are printed to stdin, separated by a new line character.
Time-points are separated by a blank line.
In order to generate a file useful for benchmarking, redirect this output to 
a file.
Example use:
    python gen_bench.py 1 1 1 1 > input.txt
'''

import random
import string
import sys
import os

dict_const = {}
dict_pred_id = {}

def init_dict_const(num_pred):
    for i in range(num_pred):
        dict_const[i] = 0

def gen_const_vect(pred, arity):
    vect = []
    for i in range(arity):
        constant_value = dict_const[pred]
        vect.append(str(constant_value))
        dict_const[pred] += 1
    return vect

def gen_stream(end_time, fact_flow, num_pred, arity):
    pred_id = 0 
    dict_pred_id[0] = 'p'
    dict_pred_id[1] = 'q'
    dict_pred_id[2] = 'r'
    dict_pred_id[3] = 's'
    dict_pred_id[4] = 't'
    dict_pred_id[5] = 'u'
    dict_pred_id[6] = 'v'
    dict_pred_id[7] = 'w'

    print("%s %s" % (0, end_time-1))

    for i in range(end_time):
        init_dict_const(num_pred)
        for j in range(fact_flow):
            pred_id = j % num_pred
            pred = dict_pred_id[pred_id]
            vect = gen_const_vect(pred_id, arity)
            var = ' '.join(vect)
            print("%s %s" % (pred, var))
        print("")

def main():
    if (len(sys.argv) < 5):
        print ('Usage: python gen_bench.py end_time fact_flow num_pred arity')
    else:
        gen_stream(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))


if __name__ == '__main__':
    main()
