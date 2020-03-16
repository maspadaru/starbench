'''
This script generates some random tuples that can be used for benchmarking. 
All atoms have the same predicate, all values are sequential:
    << p(1, 2), p(2, 3), p(4, 5), p(5, 6) >>
Example use:
    python gen.py 1 1 > input.txt
'''

import random
import string
import sys
import os


def gen_const_vect(current):
    vect = []
    vect.append(str(current))
    vect.append(str(current+1))
    return vect

def gen_stream(end_time, fact_flow):
    pred = 'p'
    print("%s %s" % (0, end_time-1))
    for i in range(end_time):
        current = 0
        for j in range(fact_flow):
            vect = gen_const_vect(current)
            current += 1
            var = ' '.join(vect)
            print("%s %s" % (pred, var))
        print("")

def main():
    if (len(sys.argv) < 3):
        print ('Usage: python gen_bench.py end_time fact_flow')
    else:
        gen_stream(int(sys.argv[1]), int(sys.argv[2]))


if __name__ == '__main__':
    main()
