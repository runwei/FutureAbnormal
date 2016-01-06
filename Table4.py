__author__ = 'runwei_zhang'

import csv
import pandas as pd
import numpy as np
from numpy.linalg import inv
import os

def partitionNACE():
    df = pd.read_csv('data/data.csv')
    df = df[:100]
    print df


def Table4():
    pass

if __name__ == "__main__":
    with open('data/data2.csv') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for i in xrange(0,100):
            row = next(reader)
            print row