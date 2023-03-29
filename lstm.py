# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 21:30:16 2023

@author: IKU-Trader
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../Utilities'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../SequentialTechnicalAnalysis'))


import pandas as pd
from Utils import Utils
from TimeUtils import TimeUtils
from DataBuffer import ResampleDataBuffer

#from CandleChart import CandleChart, BandPlot, gridFig, Colors
from STA import TechnicalAnalysis as ta

TIME = 'time'
OPEN = 'open'
HIGH = 'high'
LOW = 'low'
CLOSE = 'close'
VOLUME = 'volume'


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

def dataset(dir_path: str, year: int, month_list: list):
    files = []
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
    
def candles2dic(candles):
    is_volume = (len(candles[0]) > 5)
    if is_volume:
        time, op, hi, lo, cl, vol = candles2tohlc(candles)
    else:
        time, op, hi, lo, cl = candles2tohlc(candles)
    dic = {}
    dic[TIME] = time
    dic[OPEN] = op
    dic[HIGH] = hi
    dic[LOW] = lo
    dic[CLOSE] = cl
    if is_volume:
        dic[VOLUME] = vol
    return dic

def TAParams():
    trend_params = {ta.MA_KEYS:['SMA5', 'SMA20', 'SMA60'], ta.THRESHOLD:0.05}
    patterns = {
                    ta.SOURCE: 'MA_TREND',
                    ta.PATTERNS:[
                            [[ta.NO_TREND, ta.UPPER_TREND], 1, 0],
                            [[ta.UPPER_SUB_TREND, ta.UPPER_TREND], 1, 0],
                            [[ta.NO_TREND, ta.LOWER_TREND], 2, 0],
                            [[ta.LOWER_SUB_TREND, ta.LOWER_TREND], 2, 0]
                            ]
                }

    params = [
                [ta.SMA, {ta.WINDOW: 5}, 'SMA5'],
                [ta.SMA, {ta.WINDOW: 20}, 'SMA20'],
                [ta.SMA, {ta.WINDOW: 60}, 'SMA60'],
                [ta.MA_TREND_BAND, trend_params, 'MA_TREND'],
                [ta.PATTERN_MATCH, patterns, 'SIGNAL']
            ]
    return params
def main(dir_path: str, year: int):
    candles = dataset(dir_path, year, [1, 2])
    tohlc = candles2tohlc(candles)
    ta_params = TAParams()
    buffer = ResampleDataBuffer(tohlc, ta_params, interval_minutes=5)
    dic = buffer.dic
    print(dic.keys())
    
    
    print(len(candles))
        
    
    
    
    
    
    
if __name__ == '__main__':
    main('./data/gold', 2023)