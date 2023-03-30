# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:35:02 2023

@author: IKU
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../Utilities'))

from Utils import Utils
from TimeUtils import TimeUtils
from DataBuffer import ResampleDataBuffer
from const import const

def readFile(path):
    f = open(path, encoding='sjis')
    line = f.readline()
    line = f.readline()
    tohlc = []
    while line:
        values = line.split(',')
        s = values[0]
        t = TimeUtils.pyTime(int(s[0:4]), int(s[4:6]), int(s[6:8]), int(s[8:10]), int(s[10:12]), 0, TimeUtils.TIMEZONE_TOKYO)
        o = float(values[1])
        h = float(values[2])
        l = float(values[3])
        c = float(values[4])
        tohlc.append([t, o, h, l, c])
        line = f.readline()
    f.close()
    return tohlc

def candles2tohlc(candles):
    is_volume = (len(candles[0]) > 5)
    times = []
    op = []
    hi = []
    lo = []
    cl = []
    vol = []
    for candle in candles:
        times.append(candle[0])
        op.append(candle[1])
        hi.append(candle[2])
        lo.append(candle[3])
        cl.append(candle[4])
        if is_volume:
            vol.append(candle[5])
    if is_volume:
        return [times, op, hi, lo, cl, vol]
    else:
        return [times, op, hi, lo, cl]
    
def getCandles(year_list: int, month_list: list):
    dir_path = '../MarketData/gold'
    files = []
    for year in year_list:
        for m in month_list:
            path = os.path.join(dir_path, str(year) + str(m).zfill(2))
            if os.path.exists(path):
                l = Utils.fileList(path, '*.csv')
                if len(l) > 0:
                    files += l                
    tohlc = []
    for file in files:
       d = readFile(file)
       tohlc += d     
    candles = sorted(tohlc, key=lambda s: s[0])
    return candles

def gold_data(ta_params, years, months, interval_minutes):
    candles = getCandles(years, months)
    tohlc = candles2tohlc(candles)
    data = ResampleDataBuffer(tohlc, ta_params, interval_minutes)
    return data
   
    
    