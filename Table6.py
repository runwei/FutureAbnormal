__author__ = 'runwei_zhang'
import csv
import pandas as pd
import numpy as np
from numpy.linalg import inv
import math
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
    mA = np.zeros((Nlen*Tlen,Nlen*2+7),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not isinstance(firmgroup['Mktcap'].values[0], basestring):
            flag  = math.isnan(float(firmgroup['Mktcap'].values[0]))
            if not flag and not firmgroup['Dprice'].isnull().values.any() and not firmgroup['Allow'].isnull().values.any() and not firmgroup['Emit'].isnull().values.any():
                print float(firmgroup['Mktcap'].values[0])
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
                mA[i*Tlen:(i+1)*Tlen,6+2*Nlen] = np.multiply((firmgroup['Allow'].values-firmgroup['Emit'].values)/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
                i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-7:]
    print gamma
    return gamma


def Column2(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+7),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not isinstance(firmgroup['Mktcap'].values[0], basestring):
            flag  = math.isnan(float(firmgroup['Mktcap'].values[0]))
            if not flag and not firmgroup['Dprice'].isnull().values.any() and not firmgroup['Allow'].isnull().values.any() and not firmgroup['Emit'].isnull().values.any():
                print float(firmgroup['Mktcap'].values[0])
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
                mA[i*Tlen:(i+1)*Tlen,6+2*Nlen] = np.multiply(firmgroup['Allow'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
                i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-7:]
    print gamma
    return gamma

def Column3(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+7),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not isinstance(firmgroup['Mktcap'].values[0], basestring):
            flag  = math.isnan(float(firmgroup['Mktcap'].values[0]))
            if not flag and not firmgroup['Dprice'].isnull().values.any() and not firmgroup['Allow'].isnull().values.any() and not firmgroup['Emit'].isnull().values.any():
                print float(firmgroup['Mktcap'].values[0])
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
                mA[i*Tlen:(i+1)*Tlen,6+2*Nlen] = np.multiply(firmgroup['Emit'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
                i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-7:]
    print gamma
    return gamma

def Column4(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+8),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not isinstance(firmgroup['Mktcap'].values[0], basestring):
            flag  = math.isnan(float(firmgroup['Mktcap'].values[0]))
            if not flag and not firmgroup['Dprice'].isnull().values.any() and not firmgroup['Allow'].isnull().values.any() and not firmgroup['Emit'].isnull().values.any():
                print float(firmgroup['Mktcap'].values[0])
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
                mA[i*Tlen:(i+1)*Tlen,6+2*Nlen] = np.multiply(firmgroup['Allow'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                mA[i*Tlen:(i+1)*Tlen,7+2*Nlen] = np.multiply(firmgroup['Emit'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
                i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-8:]
    print gamma
    return gamma

def Column6(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+8),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not isinstance(firmgroup['Mktcap'].values[0], basestring):
            flag  = math.isnan(float(firmgroup['Mktcap'].values[0]))
            if not flag and not firmgroup['Dprice'].isnull().values.any() and not firmgroup['Allow'].isnull().values.any() and not firmgroup['Emit'].isnull().values.any():
                print float(firmgroup['Mktcap'].values[0])
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

                if firmgroup['Nace2'].values[0]== 40:
                    elec, other = 1,0
                else:
                    elec, other = 0,1
                mA[i*Tlen:(i+1)*Tlen,6+2*Nlen] = np.multiply(elec*firmgroup['Allow'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                mA[i*Tlen:(i+1)*Tlen,7+2*Nlen] = np.multiply(other*firmgroup['Allow'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
                i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-8:]
    print gamma
    return gamma

def Column7(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+8),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not isinstance(firmgroup['Mktcap'].values[0], basestring):
            flag  = math.isnan(float(firmgroup['Mktcap'].values[0]))
            if not flag and not firmgroup['Dprice'].isnull().values.any() and not firmgroup['Allow'].isnull().values.any() and not firmgroup['Emit'].isnull().values.any():
                print float(firmgroup['Mktcap'].values[0])
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

                if firmgroup['Nace2'].values[0]== 40:
                    elec, other = 1,0
                else:
                    elec, other = 0,1
                mA[i*Tlen:(i+1)*Tlen,6+2*Nlen] = np.multiply(elec*firmgroup['Emit'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                mA[i*Tlen:(i+1)*Tlen,7+2*Nlen] = np.multiply(other*firmgroup['Emit'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
                i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-8:]
    print gamma
    return gamma

def Column5(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+8),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not isinstance(firmgroup['Mktcap'].values[0], basestring):
            flag  = math.isnan(float(firmgroup['Mktcap'].values[0]))
            if not flag and not firmgroup['Dprice'].isnull().values.any() and not firmgroup['Allow'].isnull().values.any() and not firmgroup['Emit'].isnull().values.any():
                print float(firmgroup['Mktcap'].values[0])
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

                if firmgroup['Nace2'].values[0]== 40:
                    elec, other = 1,0
                else:
                    elec, other = 0,1
                mA[i*Tlen:(i+1)*Tlen,6+2*Nlen] = np.multiply(elec*(firmgroup['Allow'].values-firmgroup['Emit'].values)/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                mA[i*Tlen:(i+1)*Tlen,7+2*Nlen] = np.multiply(other*(firmgroup['Allow'].values-firmgroup['Emit'].values)/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
                i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-8:]
    print gamma
    return gamma

def Column8(df,Nlen,Tlen):
    mA = np.zeros((Nlen*Tlen,Nlen*2+10),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        if not isinstance(firmgroup['Mktcap'].values[0], basestring):
            flag  = math.isnan(float(firmgroup['Mktcap'].values[0]))
            if not flag and not firmgroup['Dprice'].isnull().values.any() and not firmgroup['Allow'].isnull().values.any() and not firmgroup['Emit'].isnull().values.any():
                print float(firmgroup['Mktcap'].values[0])
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

                if firmgroup['Nace2'].values[0]== 40:
                    elec, other = 1,0
                else:
                    elec, other = 0,1
                mA[i*Tlen:(i+1)*Tlen,6+2*Nlen] = np.multiply(elec*firmgroup['Allow'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                mA[i*Tlen:(i+1)*Tlen,7+2*Nlen] = np.multiply(elec*firmgroup['Emit'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                mA[i*Tlen:(i+1)*Tlen,8+2*Nlen] = np.multiply(other*firmgroup['Allow'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                mA[i*Tlen:(i+1)*Tlen,9+2*Nlen] = np.multiply(other*firmgroup['Emit'].values/float(firmgroup['Mktcap'].values[0])/1e6,firmgroup['Event'].values)
                vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
                i += 1
    tmpp = inv(mA.T.dot(mA)).dot(mA.T)
    Xhat = tmpp.dot(vb)
    gamma = Xhat[-10:]
    print gamma
    return gamma



def p2f(x):
    return float(x.strip('%'))/100


if __name__ == "__main__":
    # with open('data/data2.csv') as csvfile:
    #     reader = csv.reader(csvfile,delimiter=',')
    #     for i in xrange(4000,4300):
    #         row = next(reader)
    #         print row

    df = pd.read_csv('data/data.csv')
    Nlen = 0
    Tlen =456
    for firmid,firmgroup in df.groupby('Firmid'):
        if not isinstance(firmgroup['Mktcap'].values[0], basestring):
            flag  = math.isnan(float(firmgroup['Mktcap'].values[0]))
            if not flag and not firmgroup['Dprice'].isnull().values.any() and not firmgroup['Allow'].isnull().values.any() and not firmgroup['Emit'].isnull().values.any():
                Nlen += 1
    print Nlen
    Column8(df,Nlen,Tlen)
