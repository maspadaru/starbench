'''
This script generates tuples that can be used for benchmarking. 
Values are in random order, for instance:
    << p(11, 42), q(3, 62), p(88, 4), q(38, 11) >>
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


def gen_const(len_rnd):
    return ''.join(random.choice(string.digits) for _ in range(len_rnd))

def gen_const_vect(pred, arity, len_rnd):
    vect = []
    for i in range(arity):
        constant_value = gen_const(len_rnd)
        vect.append(constant_value)
    return vect

def gen_stream(end_time, fact_flow, num_pred, arity):
    len_rnd = len(str(fact_flow)) - 1
    if len_rnd == 0:
        len_rnd = 1
    pred_id = 0 
    dict_pred_id = {}
    dict_pred_id[0] = 'p'
    dict_pred_id[1] = 'q'
    dict_pred_id[2] = 'r'
    dict_pred_id[3] = 's'
    dict_pred_id[4] = 't'
    dict_pred_id[5] = 'u'
    dict_pred_id[6] = 'v'
    dict_pred_id[7] = 'w'
    print("%s %s" % (0, end_time-1))
    random.seed()
    for i in range(end_time):
        for j in range(fact_flow):
            pred_id = j % num_pred
            pred = dict_pred_id[pred_id]
            vect = gen_const_vect(pred, arity, len_rnd)
            var = ' '.join(vect)
            print("%s %s" % (pred, var))
        print("")

def main():
    if (len(sys.argv) < 4):
        print ('Usage: python gen_bench.py end_time fact_flow num_pred arity')
    else:
        gen_stream(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))


if __name__ == '__main__':
    main()
