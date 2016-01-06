__author__ = 'runwei_zhang'
import csv
import pandas as pd
import numpy as np
from numpy.linalg import inv
import os


def p2f(x):
    return float(x.strip('%'))/100

def MainEventCompany(firmid,df):
    Nlen = 1
    Tlen = 456
    mA = np.zeros((Nlen*Tlen,Nlen*2+1),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    gamma = 9999999999
    if not df['Dprice'].isnull().values.any():
        mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
        mA[i*Tlen:(i+1)*Tlen,i+Nlen] = df['Dmarket'].values
        mA[i*Tlen:(i+1)*Tlen,2*Nlen] = df['Event'].values
        vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in df['Dprice'].values]
        i += 1
        tmpp = inv(mA.T.dot(mA)).dot(mA.T)
        # tmpp = np.dot(tmpp2,)
        Xhat = tmpp.dot(vb)
        gamma = Xhat[-1]
        print firmid,gamma
    return gamma

def CounterEventCompany(firmid,df):
    Nlen = 1
    Tlen = 456
    mA = np.zeros((Nlen*Tlen,Nlen*2+1),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    gamma = 9999999999
    if not df['Dprice'].isnull().values.any():
        mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
        mA[i*Tlen:(i+1)*Tlen,i+Nlen] = df['Dmarket'].values
        mA[i*Tlen:(i+1)*Tlen,2*Nlen] = df['Upevent'].values
        vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in df['Dprice'].values]
        i += 1
        tmpp = inv(mA.T.dot(mA)).dot(mA.T)
        # tmpp = np.dot(tmpp2,)
        Xhat = tmpp.dot(vb)
        gamma = Xhat[-1]
        print firmid,gamma
    return gamma

def Table3():
    naceid = 40
    df = pd.read_csv('data/NACE2/%s.csv'%naceid)
    columns = ['StockID', 'Main event','Counter event']
    res = pd.DataFrame(columns=columns)
    for firmid,firmgroup in df.groupby('Firmid'):
        countergamma = CounterEventCompany(firmid,firmgroup)
        maingamma = MainEventCompany(firmid,firmgroup)
        res.loc[len(res.index)] = [firmid,maingamma,countergamma]

    res = res.sort(columns="Main event")
    res.to_csv(path_or_buf='Table3.csv',index=False,sep =',',float_format='%.3f')


if __name__ == "__main__":
    Table3()