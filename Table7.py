__author__ = 'runwei_zhang'
import csv
import pandas as pd
import numpy as np
from numpy.linalg import inv
import os

def Mainevent(companyList):
    df0 = pd.read_csv('data/last_table.csv')
    carbon_price =  df0['eua price'].interpolate().values
    oil_price = df0['crude oil'].interpolate().values
    gas_price = df0['natural gas'].interpolate().values
    Nlen = 0
    Tlen =456
    for firmid,firmgroup in df.groupby('Firmid'):
        if not firmgroup['Dprice'].isnull().values.any() and firmid in companyList:
            Nlen += 1
    mA = np.zeros((Nlen*Tlen,Nlen*2+4),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    if Nlen>0:
        for firmid,firmgroup in df.groupby('Firmid'):
            # print firmgroup['Dprice']
            if not firmgroup['Dprice'].isnull().values.any() and firmid in companyList:
                mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
                mA[i*Tlen:(i+1)*Tlen,i+Nlen] = firmgroup['Dmarket'].values
                mA[i*Tlen:(i+1)*Tlen,2*Nlen] = firmgroup['Event'].values
                mA[i*Tlen:(i+1)*Tlen,2*Nlen+1] = carbon_price
                mA[i*Tlen:(i+1)*Tlen,2*Nlen+2] = oil_price
                mA[i*Tlen:(i+1)*Tlen,2*Nlen+3] = gas_price
                vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
                i += 1
        tmpp = inv(mA.T.dot(mA)).dot(mA.T)
        # tmpp = np.dot(tmpp2,)
        Xhat = tmpp.dot(vb)
        gamma = Xhat[-4:]
        print gamma
        return Nlen,gamma
    else:
        return 0,0


def p2f(x):
    return float(x.strip('%'))/100


if __name__ == "__main__":
    df = pd.read_csv('data/data.csv')
    Nlen = 0
    Tlen = 456
    allcompany = {'cna','d_rwex','d_swvx','e_ctg','e_enag','e_ibe','e_ree','g_ppc','i_a2a','i_enel','i_hera','m_fort','ng','p_ecp','uu'}
    ukcompany = {'cna','uu','ng'}
    spancompany = {'e_ctg','e_enag','e_ibe','e_ree'}
    germancompany ={'d_rwex','d_swvx'}
    italycompany = {'i_a2a','i_enel','i_hera'}
    Mainevent(germancompany)

