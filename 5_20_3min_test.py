from ccxt import okcoinusd

from OkcoinFutureAPI import OKCoinFuture
import logging
import time
import json
import os
import pandas as pd
import datetime
import time
import talib as tbs
# import jhtalib as jt
import statsmodels.api as sm
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np
import numpy as np
import pandas as pd

order_id_list = []

# from TradeAccountAPI import TradeAccount


# 初始化apikey，secretkey,url
fileName = 'key.json'
# path = os.path.abspath(os.path.dirname(__file__))
# print(file)
# fileName = os.path.join(path, fileName)
# 解析json文件
with open(fileName) as data_file:
    setting = json.load(data_file)
    data_file.close()
apikey = str(setting['apiKey'])
secretkey = str(setting['secretKey'])
okcoinRESTURL = 'www.okex.com'
# 期货API
okcoinFuture = OKCoinFuture(okcoinRESTURL, apikey, secretkey)


def price_to_df(symbol, period, frequency, count):
    price = okcoinFuture.future_kline(symbol, period, frequency, count)
    df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'coin_amount'])
    i = 0
    for k in price:
        df.loc[i, :] = k
        i = i + 1
    return df


#print(u'获取虚拟合约的K线信息')
symbol_list =['btc_usd']
period_list =['next_week','this_week']
frequency='3min'
count= 500
# print (u'获取预估交割价')
# print (okcoinFuture.future_estimated_price('ltc_usd'))
#1min : 1分钟
#3min : 3分钟
#5min : 5分钟
#15min : 15分钟
#30min : 30分钟
#1day : 1日
#3day : 3日
#1week : 1周
#1hour : 1小时
#2hour : 2小时
#4hour : 4小时
#6hour : 6小时
#12hour : 12小时
tag = True
a=0
while tag:
    for symbol in symbol_list:
        for period in period_list: 
            time.sleep(100)
            ans= pd.DataFrame()
            data_n = price_to_df(symbol,period, frequency,count)
            ans['close'] = data_n['close'].apply(np.float)
            ans['sma5'] = tbs.SMA(np.array(ans['close']),10)
            ans['sma20'] = tbs.SMA(np.array(ans['close']),40)

            #考夫曼均线系统
            #ans['AMA1'] = okcoinFuture.KAMA(ans['close'],10,4,30)
            #ans['AMA2'] = okcoinFuture.KAMA(ans['close'],20,8,60)
            #ans.plot(figsize=[40,40])
            #print(ans)
            if(a>10):
                print('listening')
                a=0
            else:
                a = a+1
            price = okcoinFuture.future_ticker(symbol,period)['ticker']['last']
            # 五单位均线，向上突破 20 单位均线 开仓做多。
            if ans.loc[count-1,'sma5'] >ans.loc[count-1,'sma20'] and ans.loc[count-3,'sma5']< ans.loc[count-3,'sma20']:
                print('open_long')
                okcoinFuture.close_all_position([symbol],[period])
                okcoinFuture.open_long(symbol,period,price,1,0,20)
            elif ans.loc[count-1,'sma5'] <ans.loc[count-1,'sma20'] and ans.loc[count-3,'sma5']> ans.loc[count-3,'sma20']:
                okcoinFuture.close_all_position([symbol],[period])