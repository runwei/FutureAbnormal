__author__ = 'runwei_zhang'
import csv
import pandas as pd
import numpy as np
from numpy.linalg import inv
import os

def replaceStock(name,naceid):
    df = pd.read_csv('data/NACE2/%s.csv'%naceid)
    Nlen = 0
    Tlen =456
    df = df[df.Firmid ==name]
    print df



def partitionNACE():
    df = pd.read_csv('data/data.csv',usecols=['Firmid','Realdate','Nace2','Event','Bigevent', 'Upevent', 'Bigeventcount','Dmarket', 'Dprice','Nace'],low_memory=False)
    df = df.groupby('Firmid').filter(lambda x: len(x) ==456)
    for naceid,nacegroup in df.groupby('Nace2'):
        Nlen = 0
        # for firmid,firmgroup in nacegroup.groupby('Firmid'):
        #     if not firmgroup['Dprice'].isnull().values.any():
        #         Nlen += 1
        nacegroup.to_csv('data/Nace2/%s.csv'%naceid)

def MaineventSE(naceid=0,starttime=None,endtime=None):
    if naceid ==0:
        df = pd.read_csv('data/data.csv')
    else:
        df = pd.read_csv('data/NACE2/%s.csv'%naceid)
    print "naceid:", naceid
    Nlen = 0
    Tlen = 0
    for firmid,firmgroup in df.groupby('Firmid'):
        Tlen = len(firmgroup[(firmgroup['Realdate']>=starttime) &  (firmgroup['Realdate']<=endtime)])
        if not firmgroup['Dprice'].isnull().values.any():
            Nlen += 1
    mA = np.zeros((Nlen*Tlen,Nlen*2+1),float)
    vb = np.zeros(Nlen*Tlen)
    i = 0
    # print "naceid: ", naceid, "observations: ", Nlen
    if Nlen>0:
        for firmid,firmgroup in df.groupby('Firmid'):
            # print firmgroup['Dprice']
            if not firmgroup['Dprice'].isnull().values.any():
                if starttime is not None and endtime is not None:
                    firmgroup = firmgroup[(firmgroup['Realdate']>=starttime) &  (firmgroup['Realdate']<=endtime)]
                mA[i*Tlen:(i+1)*Tlen,i] = np.ones(Tlen)
                mA[i*Tlen:(i+1)*Tlen,i+Nlen] = firmgroup['Dmarket'].values
                mA[i*Tlen:(i+1)*Tlen,2*Nlen] = firmgroup['Event'].values
                # print firmgroup['Dprice'].values
                vb[i*Tlen:(i+1)*Tlen] = [p2f(x) for x in firmgroup['Dprice'].values]
                i += 1
        tmpp = inv(mA.T.dot(mA)).dot(mA.T)
        # tmpp = np.dot(tmpp2,)
        Xhat = tmpp.dot(vb)
        gamma = Xhat[-1]
        return Nlen,gamma
    else:
        return 0,0

def p2f(x):
    return float(x.strip('%'))/100

def Table2():
    columns = ['naceid','12 months','6 months','Preevent','Bigevent']
    timestamps = {
        '12 months': [16736,17100],
        '6 months': [16826,17006],
        'Preevent': [16553,16920],
        'Bigevent': [16909,16957]
    }
    df = pd.DataFrame(columns=columns)
    # for i in os.listdir('data/Nace2/'):
    #     if i.endswith(".csv"):
    #         naceid = i.split('.')[0]
    #         mlist = [int(naceid)]
    #         for key in timestamps:
    #             Nlen,maingamma = MaineventSE(naceid,timestamps[key][0],timestamps[key][1])
    #             if Nlen>0:
    #                 mlist.append(maingamma)
    #         if len(mlist)== len(columns):
    #             df.loc[len(df.index)] = mlist
    naceid = 0
    mlist = [int(naceid)]
    for key in timestamps:
        Nlen,maingamma = MaineventSE(naceid,timestamps[key][0],timestamps[key][1])
        if Nlen>0:
            mlist.append(maingamma)
    if len(mlist)== len(columns):
        df.loc[len(df.index)] = mlist
    df = df.sort(columns="12 months")
    df.to_csv(path_or_buf='Table2.csv',index=False,sep =',',float_format='%.3f')



if __name__ == "__main__":
    # with open('data/data2.csv') as csvfile:
    #     reader = csv.reader(csvfile,delimiter=',')
    #     for i in xrange(0,100):
    #         row = next(reader)
    #         print row
    # preprocess()
    # partitionNACE()
    Table2()
    # LinearRegression('19')
