# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:22:12 2018

@author: aaaaa
"""

from datetime import datetime
import pandas as pd

###############################################################################
#                       股票機器人 基本面分析（簡易板）                         #
###############################################################################

### 現在時間處裡 ###
now = datetime.now() #現在的時間
year = now.strftime("%Y") #抓今年


def Fundamental_Analysis(stock='2330')
	### 由於財報出來的時間不一定，因此直接從第四季開始一個一個抓抓看，嘗試抓到最新的 ###
	for season in range(4,0,-1):
	    ### 先與網站請求抓到每天的報價資料 ###
	    url = 'http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=' + stock + '&SYEAR=' + year + '&SSEASON=' + str(season) + '&REPORT_ID=C'
	    getdata=pd.read_html(url,encoding='utf16',header=0)
	    
	    if len(getdata) > 1: #如果數量大於1，代表有捉到資料
	        break #跳出迴圈
	        
	### 如果四季都查完，還是'查無資料'，代表是在年初，要抓前一年第四季 ###
	if len(getdata) == 1:
	    url = 'http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=' + stock + '&SYEAR=' + str(int(year)-1) + '&SSEASON=4&REPORT_ID=C'
	    getdata=pd.read_html(url,encoding='utf16',header=0)

	del getdata[0] #殺掉第一個，因為第一個沒有意義
	len(getdata) #看看有幾個鰾表
	getdata[0]['想查詢的項目'] #看看會計項目
