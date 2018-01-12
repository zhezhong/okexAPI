from OkcoinFutureAPI import OKCoinFuture
from OkcoinSpotAPI import OKCoinSpot
import logging
import time
import json
import os
import pandas as pd
import datetime  
import time  
#import talib as tbs
#import jhtalib as jt
import statsmodels.api as sm
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import numpy as np
import pandas as pd
from time import sleep
order_id_list = []

#from TradeAccountAPI import TradeAccount


# 初始化apikey，secretkey,url
fileName = 'key.json'
#path = os.path.abspath(os.path.dirname(__file__))
#print(file)
#fileName = os.path.join(path, fileName)
# 解析json文件
with open(fileName) as data_file:
    setting = json.load(data_file)
    data_file.close()
apikey = str(setting['apiKey'])
secretkey = str(setting['secretKey'])
okcoinRESTURL = 'www.okex.com'
# 期货API
context = OKCoinFuture(okcoinRESTURL, apikey, secretkey)
okcoinSpot = OKCoinSpot(okcoinRESTURL, apikey, secretkey)

# 网格交易法则
security = ['eth_usd','btc_usd']
#period = ['this_week','next_week','quarter']
symbol ='eth_usd'
contractType='this_week'
unit_volume = 10
timeframe = '1hour'
#三天
limit = '72'
context.last_price = 1100
def price_to_df(symbol,contractType,frequency,count):
    #print(symbol,contractType,frequency,count)
    price = context.future_kline(symbol,contractType,type=frequency,size=count)
    #print(price)
    df = pd.DataFrame(columns  = ['timestamp','open','high','low','close','volume','coin_amount'])
    i=0
    for k in price:
        df.loc[i,:]=k
        i = i+1
    return df
def net_work_trading(context):
    while True:
        #okcoinFuture.get_all_future_position(security,period)
        context.tick = context.future_ticker(symbol,contractType)['ticker']
        context.price= context.tick['last']
        context.bar = price_to_df(symbol,contractType,frequency=timeframe,count=72)
        #print(context.bar)
        context.high = max(context.bar['high'])
        context.low  = min(context.bar['low'])
        #print(type(context.price))
        #print(context.high)
        # 价格越高， cof 越小。
        cof = 20*(context.high-context.price)/(context.high-context.low)
        #价格越靠近边界，仓位越轻
        #价格在上方，
        #if cof>0.75:
        # 越接近两端，volume 越小
        volume  =int((10-abs(cof-10))*unit_volume)
        #print('high:',context.high,'low:',context.low,'price:',context.price,volume)

        #print(price)
        if (context.price>context.last_price*1.005):
            # 向上突破一个单元格
            context.last_price = context.price
            print('向上突破，先开一多')
            print('high:',context.high,'low:',context.low,'price:',context.price,'cof:',cof)
            context.open_long(symbol,contractType,price=context.tick['last'],amount=volume,matchType=0,leverRate=20)
            context.close_long(symbol,contractType,price=context.tick['last']*1.005,amount=volume,matchType=0,leverRate=20)
            # 在顶部，存在回调可能性。可以做空。
            
            if(cof<4):
                print('在顶部，存在回调，可以补一空仓')
                print('high:',context.high,'low:',context.low,'price:',context.price,'cof:',cof)
                context.open_short(symbol,contractType,price=context.tick['last'],amount=volume,matchType=0,leverRate=20)
                context.close_short(symbol,contractType,price=context.tick['last']*0.995,amount=volume,matchType=0,leverRate=20)
            # 顶部突破，强势上涨，开打多头
            if(cof<1):
                print('在顶部，强势突破')
                context.open_long(symbol,contractType,price=context.tick['last'],amount=volume*5,matchType=0,leverRate=20)
                
        if (context.price<context.last_price*0.995):
            # 向上突破一个单元格
            #价格越靠近边界，仓位越轻
            #价格在上方，
            #if cof>0.75:
            if cof>15:
                print('#在底部 ，只做多，不做空。不设置止损')
                print('high:',context.high,'low:',context.low,'price:',context.price,'cof:',cof)
                context.open_long(symbol,contractType,price=context.tick['last'],amount=volume,matchType=0,leverRate=20)
            else:
                print('在中间，多空斗，')
                print('high:',context.high,'low:',context.low,'price:',context.price,'cof:',cof)
                context.open_long(symbol,contractType,price=context.tick['last'],amount=volume,matchType=0,leverRate=20)
                context.close_long(symbol,contractType,price=context.tick['last']*1.005,amount=volume,matchType=0,leverRate=20)
                context.open_short(symbol,contractType,price=context.tick['last'],amount=volume,matchType=0,leverRate=20)
                context.close_short(symbol,contractType,price=context.tick['last']*0.995,amount=volume,matchType=0,leverRate=20)
            if cof<2:
                print('顶部出现回调，平多仓。')
                context.close_long(symbol,contractType,price=context.tick['last']*1.005,amount=volume,matchType=0,leverRate=20)
            context.last_price = context.price
            
        sleep(10)
    return 0
if __name__ == '__main__':
    net_work_trading(context)