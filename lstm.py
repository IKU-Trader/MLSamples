# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 21:30:16 2023

@author: IKU-Trader
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../Utilities'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../TechnicalAnalysis'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../CandlestickChart'))

import pandas as pd
from Utils import Utils
from TimeUtils import TimeUtils
from DataBuffer import ResampleDataBuffer
from market_data import gold_data
from CandleChart import CandleChart, BandPlot, makeFig, Colors
from STA import TechnicalAnalysis as ta
from const import const

import torch
import torch.nn as nn
import torch.nn.functionl as F
import torch.optim as optim
import gc


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

def displayChart(data: ResampleDataBuffer):
    t0 = TimeUtils.pyTime(2023, 1, 9, 12, 30, 0, TimeUtils.TIMEZONE_TOKYO)
    t1 = TimeUtils.pyTime(2023, 1, 10, 5, 0, 0, TimeUtils.TIMEZONE_TOKYO)
    time = data.dic[const.TIME]
    n, begin, end = TimeUtils.sliceTime(time, t0, t1)
    if n < 50:
        return
    tohlcv = Utils.sliceDic(data.dic, [const.TIME, const.OPEN, const.HIGH, const.LOW, const.CLOSE], begin, end)
    fig, ax = makeFig(1, 1, (10, 5))
    chart = CandleChart(fig, ax, '')
    chart.drawCandle(tohlcv[0], tohlcv[1], tohlcv[2], tohlcv[3], tohlcv[4])
    
def makeDataset(data: dict):
    time = data[const.TIME]
    Open = data[const.OPEN]
    High = data[const.HIGH]
    Low = data[const.LOW]
    Close = data[const.CLOSE]
    
    n = len(time)
    n_train = int(n * 0.7)
    n_test = n - n_train
    
    train = Close[:n_train]
    test = Close[n_train:]
    
    
def lstm(data: dict):
    device = torch.device('gpu' if torch.cuda.is_available() else 'cpu')
    torch.manual_seed(1)
    


def main():
    ta_params = TAParams()
    data = gold_data(ta_params, [2023], [1], 5)
    dic = data.dic
    time = dic[const.TIME]
    print(time[0], '--', time[-1])
    displayChart(data)
   
    
if __name__ == '__main__':
    main()