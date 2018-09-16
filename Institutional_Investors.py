#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 19:11:30 2018

@author: cheating
"""
#繪圖用
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
import datetime
from io import StringIO
import pandas as pd
    
###############################################################################
#                              股票機器人 籌碼面分析                            #
###############################################################################

# 畫出籌碼面圖
def stockII(stocknumber):
    
    sumstock=[]
    stockdate=[]
    for i in range(11,0,-1):
        date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=i),'%Y%m%d') #先設定要爬的時間
        r = requests.get('http://www.tse.com.tw/fund/T86?response=csv&date='+date+'&selectType=ALLBUT0999') #要爬的網站
        if r.text != '\r\n': #有可能會沒有爬到東西，有可能是六日
            get = pd.read_csv(StringIO(r.text), header=1).dropna(how='all', axis=1).dropna(how='any') # 把交易所的csv資料載下來
            get=get[get['證券代號']==stocknumber] # 找到我們要搜尋的股票
            if len(get) >0:
                get['三大法人買賣超股數'] = get['三大法人買賣超股數'].str.replace(',','').astype(float) # 去掉','這個符號把它轉成數字
                stockdate.append(date)
                sumstock.append(get['三大法人買賣超股數'].values[0])
#    if len(stockdate) >0:
#        ### 開始畫圖 ###
#        plt.bar(stockdate, sumstock) 
#        plt.xticks(fontsize=10,rotation=90)
#        plt.axhline(0, color='c', linewidth=1) # 繪製0的那條線
#        plt.title('Institutional Investors', fontsize=20)
#        plt.xlabel("Day", fontsize=15)
#        plt.ylabel("Quantity", fontsize=15)
#        plt.show()
#        plt.savefig('showII.png') #存檔
#        plt. close() # 殺掉記憶體中的圖片
#        #開始利用imgur幫我們存圖片，以便於等等發送到手機
#        return Imgur.showImgur('showII')
#    else:
#        # 找不到這個股票也回傳"失敗"這張圖
#        return 'https://i.imgur.com/RFmkvQX.jpg' 
    