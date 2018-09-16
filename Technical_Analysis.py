# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 17:29:13 2018

@author: cheating
"""
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader import data
import fix_yahoo_finance as yf # yahoo專用的拿來拉股票資訊
import datetime
import talib #技術分析專用
import matplotlib.pyplot as plt # 繪圖專用
import mpl_finance as mpf # 專門用來畫蠟燭圖的
import pylab as pl  # 讓圖片的文字可以旋轉
import Imgur

###############################################################################
#                              股票機器人 技術面分析                            #
###############################################################################

def TheConstructor(userstock):
    # 設定要的資料時間
    start = datetime.datetime.now() - datetime.timedelta(days=365) #先設定要爬的時間
    end = datetime.date.today()
    
    # 與yahoo請求
    pd.core.common.is_list_like = pd.api.types.is_list_like
    yf.pdr_override()
    
    # 取得股票資料
    stock = data.get_data_yahoo(userstock+'.TW', start, end)
    return stock


#---------------------------------------- 股票K線圖 ------------------------------------

def stock_Candlestick(userstock):
    stock=TheConstructor(userstock)
    
    fig = plt.figure(figsize=(24, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xticks(range(0, len(stock.index), 5))
    ax.set_xticklabels(stock.index[::5])
    plt.xticks(fontsize=10,rotation=90)
    mpf.candlestick2_ochl(ax, stock['Open'], stock['Close'], stock['High'], stock['Low'],
                         width=0.5, colorup='r', colordown='green',
                         alpha=0.6)
    plt.title("Candlestick_chart") # 標題設定
    plt.grid()
    plt.savefig('Candlestick_chart.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
    
    return Imgur.showImgur('Candlestick_chart')#開始利用imgur幫我們存圖片，以便於等等發送到手機

#---------------------------------------- KD指標 ------------------------------------
def stock_KD(userstock):
    stock=TheConstructor(userstock)
    
    ret = pd.DataFrame(list(talib.STOCH(stock['High'], stock['Low'], stock['Close']))).transpose()
    ret.columns=['K','D']
    ret.index = stock['Close'].index

    ### 開始畫圖 ###
    ret.plot(color=['#5599FF','#66FF66'], linestyle='dashed')

    stock['Close'].plot(secondary_y=True,color='#FF0000')
    plt.title("KD") # 標題設定
    plt.show()
    plt.savefig('KD.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
    
    return Imgur.showImgur('KD')#開始利用imgur幫我們存圖片，以便於等等發送到手機
#-------------------------------- 移動平均線（Moving Average）------------------------------------
def stock_MA(userstock):
    stock=TheConstructor(userstock)
    
    ret = pd.DataFrame(talib.SMA(stock['Close'],10), columns= ['10-day average']) #10日移動平均線
    ret = pd.concat([ret,pd.DataFrame(talib.SMA(stock['Close'],20), columns= ['20-day average'])], axis=1) #10日移動平均線
    ret = pd.concat([ret,pd.DataFrame(talib.SMA(stock['Close'],60), columns= ['60-day average'])], axis=1) #10日移動平均線

    ### 開始畫圖 ###
    ret.plot(color=['#5599FF','#66FF66','#FFBB66'], linestyle='dashed')
    stock['Close'].plot(secondary_y=True,color='#FF0000')
    plt.title("Moving_Average") # 標題設定
    plt.show()
    plt.savefig('Moving_Average.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
    return Imgur.showImgur('Moving_Average')#開始利用imgur幫我們存圖片，以便於等等發送到手機    

#-------------------- 指數平滑異同移動平均線（Moving Average Convergence / Divergence）------------------------------------
def stock_MACD(userstock):
    stock=TheConstructor(userstock)
    ret=pd.DataFrame()

    ret['MACD'],ret['MACDsignal'],ret['MACDhist'] = talib.MACD(stock['Close'],fastperiod=6, slowperiod=12, signalperiod=9)

    ### 開始畫圖 ###
    ret.plot(color=['#5599FF','#66FF66','#FFBB66'], linestyle='dashed')
    stock['Close'].plot(secondary_y=True,color='#FF0000')
    plt.title("Relative_Strength_Index") # 標題設定
    plt.show()
    plt.savefig('Relative_Strength_Index.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
    return Imgur.showImgur('Relative_Strength_Index')#開始利用imgur幫我們存圖片，以便於等等發送到手機 
    
#------------------------ 能量潮指標（On Balance Volume）------------------------------------
def stock_OBV(userstock):
    stock=TheConstructor(userstock)
    ret = pd.DataFrame(talib.OBV(stock['Close'], stock['Volume']), columns= ['OBV'])

    ### 開始畫圖 ###
    ret.plot(color=['#5599FF'], linestyle='dashed')
    stock['Close'].plot(secondary_y=True,color='#FF0000')
    plt.title("On_Balance_Volume") # 標題設定
    plt.show()
    plt.savefig('On_Balance_Volume.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
    return Imgur.showImgur('On_Balance_Volume')#開始利用imgur幫我們存圖片，以便於等等發送到手機 
    
#------------------------ 威廉指數（Williams Overbought）------------------------------------
def stock_William(userstock):
    stock=TheConstructor(userstock)
    ret = pd.DataFrame(talib.WILLR(stock['High'], stock['Low'], stock['Open']), columns= ['Williams'])

    ### 開始畫圖 ###
    ret.plot(color=['#5599FF'], linestyle='dashed')
    stock['Close'].plot(secondary_y=True,color='#FF0000')
    plt.title("Williams_Overbought") # 標題設定
    plt.show()
    plt.savefig('Williams_Overbought.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
    return Imgur.showImgur('Williams_Overbought')#開始利用imgur幫我們存圖片，以便於等等發送到手機 
    
#------------------------ 平均真實區域指標（Average True Range）------------------------------------
def stock_ATR(userstock):
    stock=TheConstructor(userstock)
    ret = pd.DataFrame(talib.ATR(stock['High'], stock['Low'], stock['Close']), columns= ['Average True Range'])

    ### 開始畫圖 ###
    ret.plot(color=['#5599FF'], linestyle='dashed')
    stock['Close'].plot(secondary_y=True,color='#FF0000')
    plt.title("Average_True_Range") # 標題設定
    plt.show()
    plt.savefig('Average_True_Range.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
    return Imgur.showImgur('Average_True_Range')#開始利用imgur幫我們存圖片，以便於等等發送到手機 
    
#------------------------ 平均趨向指標（Average Directional Indicator）------------------------------------
def stock_ADX(userstock):
    stock=TheConstructor(userstock)
    ret = pd.DataFrame(talib.ADX(stock['High'], stock['Low'], stock['Close']), columns= ['Average True Range'])

    ### 開始畫圖 ###
    ret.plot(color=['#5599FF'], linestyle='dashed')
    stock['Close'].plot(secondary_y=True,color='#FF0000')
    plt.title("Average_Directional_Indicator") # 標題設定
    plt.show()
    plt.savefig('Average_Directional_Indicator.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
    return Imgur.showImgur('Average_Directional_Indicator')#開始利用imgur幫我們存圖片，以便於等等發送到手機 
    
#------------------------ 相對強弱指數（Relative Strength Index）------------------------------------
def stock_RSI(userstock):
    stock=TheConstructor(userstock)
    # RSI的天數設定一般是6, 12, 24
    ret = pd.DataFrame(talib.RSI(stock['Close'],24), columns= ['Relative Strength Index'])

    ### 開始畫圖 ###
    ret.plot(color=['#5599FF'], linestyle='dashed')
    stock['Close'].plot(secondary_y=True,color='#FF0000')
    plt.title("Relative_Strength_Index") # 標題設定
    plt.show()
    plt.savefig('Relative_Strength_Index.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
    return Imgur.showImgur('Relative_Strength_Index')#開始利用imgur幫我們存圖片，以便於等等發送到手機 
    
#------------------------ 資金流動指標（Money Flow Index）------------------------------------
def stock_MFI(userstock):
    stock=TheConstructor(userstock)
    ret = pd.DataFrame(talib.MFI(stock['High'],stock['Low'],stock['Close'],stock['Volume'], timeperiod=14), columns= ['Money Flow Index'])

    ### 開始畫圖 ###
    ret.plot(color=['#5599FF'], linestyle='dashed')
    stock['Close'].plot(secondary_y=True,color='#FF0000')
    plt.title("Money_Flow_Index") # 標題設定
    plt.show()
    plt.savefig('Money_Flow_Index.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
    return Imgur.showImgur('Money_Flow_Index')#開始利用imgur幫我們存圖片，以便於等等發送到手機 
    
#------------ 接收者操作特徵曲線（Receiver Operating Characteristic Curve）------------------------------------
def stock_ROC(userstock):
    stock=TheConstructor(userstock)
    ret = pd.DataFrame(talib.ROC(stock['Close'], timeperiod=10), columns= ['Receiver Operating Characteristic curve'])

    ### 開始畫圖 ###
    ret.plot(color=['#5599FF'], linestyle='dashed')
    stock['Close'].plot(secondary_y=True,color='#FF0000')
    plt.title("Receiver_Operating_Characteristic_Curve") # 標題設定
    plt.show()
    plt.savefig('Receiver Operating Characteristic curve.png') #存檔
    plt. close() # 殺掉記憶體中的圖片
    return Imgur.showImgur('Receiver Operating Characteristic curve')#開始利用imgur幫我們存圖片，以便於等等發送到手機 
    