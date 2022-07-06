
''' CAHNGES I NEED:
1 ::
    If the Close price is above the Moving Avarage, I want to catch only BUY Signals.
    If the Close price is below the Moving Avarage, I want to catch only SELL Signals.
    
2 ::
    When a Signal comes (for example: the orange indicator in the Plot reach the -20 limit or the -90),
    I want the position be opened when when the Signal comes back below the -20 or above the -90. 
    CHECK THE IMAGE PLEASE '''


# TRY WORK WITH JUPYTER NOTEBOOK

# -----------------------------------------------------------    

''' L I B R A R I E S '''
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas_ta as ta

from math import floor
from termcolor import colored as cl

plt.rcParams['figure.figsize'] = (20,10)
plt.style.use('fivethirtyeight')

# -----------------------------------------------------------  

''' G R A B   D A T A '''
# 3600 candles 
# 5 min each candle
df = pd.read_csv('ETH 5.csv')
df['open_time'] = pd.to_datetime(df['open_time'], unit='s')
df.rename(columns={'open_time': 'datetime'}, inplace=True)
df.set_index('datetime')

# ----------------------------------------------------------- 

''' C A L C U L A T E   I N D I C A T O R '''
def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = -100 * ((highh - close) / (highh - lowl))
    return wr

df['W_R'] = get_wr(df['high'], df['low'], df['close'], 14)
df = df.dropna()

# Add moving avarage 200
df['sma200'] = ta.sma(df['close'], length=200)
df['sma200'].fillna(value=df['close'][0:150].mean(), inplace=True)

# -----------------------------------------------------------

''' PLOT DATA AND INDICATOR '''
ax1 = plt.subplot2grid((11,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((11,1), (6,0), rowspan = 5, colspan = 1)
ax1.plot(df['close'], linewidth = 2)
# ax1.plot(df['sma200'], linewidth = 2)

ax1.set_title('BTC CLOSING PRICE')
ax2.plot(df['W_R'], color = 'orange', linewidth = 2)
ax2.axhline(-10, linewidth = 1.5, linestyle = '--', color = 'green')
ax2.axhline(-90, linewidth = 1.5, linestyle = '--', color = 'red')
ax2.set_title('ETH W_R INDICATOR')
plt.show()

# -----------------------------------------------------------

''' S T R A T E G Y '''
def implement_wr_strategy(prices, wr):

    buy_price = []
    sell_price = []
    wr_signal = []
    signal = 0
    # IF SIGNAL 1 MEANS BUY
    # IF SIGNAL -1 MEANS SELL

    for i in range(len(wr)):

        # If the indicator reach -90, BUY
        if wr.iloc[i-1] > -90 and wr.iloc[i] < -90:
            if signal != 1:
                
                buy_price.append(prices.iloc[i])
                sell_price.append(np.nan)
                signal = 1
                wr_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                wr_signal.append(0)

        # If the indicator reach -10, SELL
        elif wr.iloc[i-1] < -10 and wr.iloc[i] > -10:
            if signal != -1:
                
                buy_price.append(np.nan)     
                sell_price.append(prices.iloc[i])
                signal = -1
                wr_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                wr_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            wr_signal.append(0)
    
    return buy_price, sell_price, wr_signal

buy_price, sell_price, wr_signal = implement_wr_strategy(df['close'], df['W_R'])

# -----------------------------------------------------------

''' PLOT THE BUY AND SELL SIGNALS '''
sma200 = ta.sma(df['close'], length=200)

ax1 = plt.subplot2grid((11,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((11,1), (6,0), rowspan = 5, colspan = 1)
ax1.plot( df['close'], linewidth = 2)
ax1.plot(sma200, linewidth = 2)

ax1.plot(df.index, buy_price, marker = '^', markersize = 12, linewidth = 0, color = 'green', label = 'BUY SIGNAL')
ax1.plot(df.index, sell_price, marker = 'v', markersize = 12, linewidth = 0, color = 'r', label = 'SELL SIGNAL')
ax1.legend()
ax1.set_title('BTC TRADING SIGNALS')
ax2.plot(df['W_R'], color = 'orange', linewidth = 2)
ax2.axhline(-10, linewidth = 1.5, linestyle = '--', color = 'grey')
ax2.axhline(-90, linewidth = 1.5, linestyle = '--', color = 'grey')
ax2.set_title('BTC WILLIAMS %R 14')
plt.show()



