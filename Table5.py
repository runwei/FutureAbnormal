__author__ = 'runwei_zhang'

__author__ = 'runwei_zhang'
import csv
import pandas as pd
import numpy as np
from numpy.linalg import inv
import os

def partitionNACE():
    df = pd.read_csv('data/data.csv',usecols=['Firmid','Realdate','Nace2','Event','Bigevent', 'Upevent', 'Bigeventcount','Dmarket', 'Dprice','Nace'],low_memory=False)
    df = df.groupby('Firmid').filter(lambda x: len(x) ==456)
    for naceid,nacegroup in df.groupby('Nace2'):
        Nlen = 0
        # for firmid,firmgroup in nacegroup.groupby('Firmid'):
        #     if not firmgroup['Dprice'].isnull().values.any():
        #         Nlen += 1
        nacegroup.to_csv('data/Nace2/%s.csv'%naceid)



def Column1(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+1),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not firmgroup['Dprice'].isnull().values.any():
            mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
            mA[i*Tlen:(i+1)*Tlen,i+Nlen] = firmgroup['Dmarket'].values
            mA[i*Tlen:(i+1)*Tlen,2*Nlen] = firmgroup['Event'].values
            vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
            i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    # tmpp = np.dot(tmpp2,)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-1]
    print gamma
    return gamma

def Column2(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+2),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not firmgroup['Dprice'].isnull().values.any():
            mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
            mA[i*Tlen:(i+1)*Tlen,i+Nlen] = firmgroup['Dmarket'].values
            mA[i*Tlen:(i+1)*Tlen,2*Nlen] = firmgroup['Event'].values
            mA[i*Tlen:(i+1)*Tlen,1+2*Nlen] = np.multiply(firmgroup['Do'].values,firmgroup['Event'].values)
            vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
            i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-2:]
    print gamma
    return gamma

def Column3(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+2),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not firmgroup['Dprice'].isnull().values.any():
            mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
            mA[i*Tlen:(i+1)*Tlen,i+Nlen] = firmgroup['Dmarket'].values
            mA[i*Tlen:(i+1)*Tlen,2*Nlen] = firmgroup['Event'].values
            mA[i*Tlen:(i+1)*Tlen,1+2*Nlen] = np.multiply(firmgroup['Di'].values,firmgroup['Event'].values)
            vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
            i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-2:]
    print gamma
    return gamma

def Column4(df,Nlen,Tlen,misdict):
    mA = np.zeros((Nlen*Tlen,Nlen*2+3),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not firmgroup['Dprice'].isnull().values.any():
            mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
            mA[i*Tlen:(i+1)*Tlen,i+Nlen] = firmgroup['Dmarket'].values
            mA[i*Tlen:(i+1)*Tlen,2*Nlen] = firmgroup['Event'].values
            eu = firmgroup['Conc'].values
            where_are_NaNs = np.isnan(eu)
            eu[where_are_NaNs] = 0
            mis = []
            for x in firmgroup['Nace2'].values:
                print x,misdict[x]
                mis.append(misdict[x])
            # mis = firmgroup['Dumconc'].values
            # where_are_NaNs = np.isnan(mis)
            # mis[where_are_NaNs] = 0
            mA[i*Tlen:(i+1)*Tlen,1+2*Nlen] = np.multiply(eu,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,2+2*Nlen] = np.multiply(mis,firmgroup['Event'].values)
            vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
            i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-3:]
    print gamma
    return gamma

def Column5(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+3),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not firmgroup['Dprice'].isnull().values.any():
            mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
            mA[i*Tlen:(i+1)*Tlen,i+Nlen] = firmgroup['Dmarket'].values
            mA[i*Tlen:(i+1)*Tlen,2*Nlen] = firmgroup['Event'].values
            mA[i*Tlen:(i+1)*Tlen,1+2*Nlen] = np.multiply(firmgroup['Do'].values,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,2+2*Nlen] = np.multiply(firmgroup['Di'].values,firmgroup['Event'].values)
            vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
            i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-3:]
    print gamma
    return gamma

def Column6(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+6),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not firmgroup['Dprice'].isnull().values.any():
            mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
            mA[i*Tlen:(i+1)*Tlen,i+Nlen] = firmgroup['Dmarket'].values
            mA[i*Tlen:(i+1)*Tlen,2*Nlen] = firmgroup['Event'].values
            eu = firmgroup['Conc'].values
            where_are_NaNs = np.isnan(eu)
            eu[where_are_NaNs] = 0
            mis = firmgroup['Dumconc'].values
            where_are_NaNs = np.isnan(mis)
            mis[where_are_NaNs] = 0
            mA[i*Tlen:(i+1)*Tlen,1+2*Nlen] = np.multiply(firmgroup['Do'].values,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,2+2*Nlen] = np.multiply(eu,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,3+2*Nlen] = np.multiply(mis,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,4+2*Nlen] = np.multiply(np.multiply(eu,firmgroup['Event'].values),firmgroup['Do'].values)
            mA[i*Tlen:(i+1)*Tlen,5+2*Nlen] = np.multiply(np.multiply(mis,firmgroup['Event'].values),firmgroup['Do'].values)

            vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
            i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-6:]
    print gamma
    return gamma

def Column7(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+6),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not firmgroup['Dprice'].isnull().values.any():
            mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
            mA[i*Tlen:(i+1)*Tlen,i+Nlen] = firmgroup['Dmarket'].values
            mA[i*Tlen:(i+1)*Tlen,2*Nlen] = firmgroup['Event'].values
            eu = firmgroup['Conc'].values
            where_are_NaNs = np.isnan(eu)
            eu[where_are_NaNs] = 0
            mis = firmgroup['Dumconc'].values
            where_are_NaNs = np.isnan(mis)
            mis[where_are_NaNs] = 0
            mA[i*Tlen:(i+1)*Tlen,1+2*Nlen] = np.multiply(firmgroup['Di'].values,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,2+2*Nlen] = np.multiply(eu,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,3+2*Nlen] = np.multiply(mis,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,4+2*Nlen] = np.multiply(np.multiply(eu,firmgroup['Event'].values),firmgroup['Di'].values)
            mA[i*Tlen:(i+1)*Tlen,5+2*Nlen] = np.multiply(np.multiply(mis,firmgroup['Event'].values),firmgroup['Di'].values)
            vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
            i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-6:]
    print gamma
    return gamma

def Column8(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+9),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not firmgroup['Dprice'].isnull().values.any():
            mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
            mA[i*Tlen:(i+1)*Tlen,i+Nlen] = firmgroup['Dmarket'].values
            mA[i*Tlen:(i+1)*Tlen,2*Nlen] = firmgroup['Event'].values
            eu = firmgroup['Conc'].values
            where_are_NaNs = np.isnan(eu)
            eu[where_are_NaNs] = 0
            mis = firmgroup['Dumconc'].values
            where_are_NaNs = np.isnan(mis)
            mis[where_are_NaNs] = 0
            mA[i*Tlen:(i+1)*Tlen,1+2*Nlen] = np.multiply(firmgroup['Do'].values,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,2+2*Nlen] = np.multiply(firmgroup['Di'].values,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,3+2*Nlen] = np.multiply(eu,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,4+2*Nlen] = np.multiply(mis,firmgroup['Event'].values)
            mA[i*Tlen:(i+1)*Tlen,5+2*Nlen] = np.multiply(np.multiply(eu,firmgroup['Event'].values),firmgroup['Do'].values)
            mA[i*Tlen:(i+1)*Tlen,6+2*Nlen] = np.multiply(np.multiply(mis,firmgroup['Event'].values),firmgroup['Do'].values)
            mA[i*Tlen:(i+1)*Tlen,7+2*Nlen] = np.multiply(np.multiply(eu,firmgroup['Event'].values),firmgroup['Di'].values)
            mA[i*Tlen:(i+1)*Tlen,8+2*Nlen] = np.multiply(np.multiply(mis,firmgroup['Event'].values),firmgroup['Di'].values)
            vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
            i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-9:]
    print gamma
    return gamma


def p2f(x):
    return float(x.strip('%'))/100


if __name__ == "__main__":
    # with open('data/data2.csv') as csvfile:
    #     reader = csv.reader(csvfile,delimiter=',')
    #     for i in xrange(0,100):
    #         row = next(reader)
    #         print row

    df = pd.read_csv('data/data.csv')
    Nlen = 0
    Tlen =456
    for firmid,firmgroup in df.groupby('Firmid'):
        if not firmgroup['Dprice'].isnull().values.any():
            Nlen += 1

    with open('data/NoEE.csv') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=',')
        misdict =dict()
        for row in reader:
            misdict[int(row['NACE'])]=float(row['NoEE'])
    Column4(df,Nlen,Tlen,misdict)
