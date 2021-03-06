#!/usr/bin/python
# -*- coding: utf-8 -*-
# 用于访问OKCOIN 币币交易Api REST API
from HttpMD5Util import buildMySign, httpGet, httpPost
import logging
import time
import json
import os
import shutil
import pandas as pd
import pandas.stats.moments
import numpy as np
import sys
from datetime import datetime

# !/usr/bin/python
# -*- coding: utf-8 -*-
# 用于访问OKCOIN 现货REST API
from HttpMD5Util import buildMySign, httpGet, httpPost


class OKCoinBibi:

    def __init__(self, url, apikey, secretkey):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey

    #use 获取OKCOIN现货行情信息  公开的，不要Api。
    def ticker(self, symbol=''):
        TICKER_RESOURCE = "/api/v1/ticker.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return httpGet(self.__url, TICKER_RESOURCE, params)

    # use 获取OKCOIN现货市场深度
    def depth(self, symbol='', size=5):
        DEPTH_RESOURCE = "/api/v1/depth.do"
        params=''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if size:
            params += '&size=' + size if params else 'size=' + size
        return httpGet(self.__url, DEPTH_RESOURCE, params)

    # use获取OKCOIN现货历史交易信息
    def trades(self, symbol=''):
        TRADES_RESOURCE = "/api/v1/trades.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return httpGet(self.__url, TRADES_RESOURCE, params)

    # use 获取货币合约K线信息
    def kline(self, symbol, type, size=0, since=0):
        # print(symbol,contractType,type,size)
        FUTURE_USERINFO = "/api/v1/kline.do"
        params = {
            'symbol':symbol,
            'type':type,# frequenncy
            'size':size,
            'since':since,
        }
        params=''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if type:
            params += '&type=' + type if params else 'type=' + type
        if size:
            params += '&size=' + size if params else 'size=' + size
        if since:
            params += '&since=' + since if params else 'since=' + since
        
        # print('-------',params)
        return httpGet(self.__url, FUTURE_USERINFO, params)

    # use获取用户现货账户信息
    def userinfo(self):
        USERINFO_RESOURCE = "/api/v1/userinfo.do"
        params = {}
        params['api_key'] = self.__apikey
        params['sign'] = buildMySign(params, self.__secretkey)
        #print(params)
        return httpPost(self.__url, USERINFO_RESOURCE, params)

    # use币币交易交易
    def trade(self, symbol, tradeType, price, amount):
        TRADE_RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'type': tradeType # buy sell buy_market,sell_market
        }
        if price:
            params['price'] = price
        if amount:
            params['amount'] = amount

        params['sign'] = buildMySign(params, self.__secretkey)
        ans=httpPost(self.__url, TRADE_RESOURCE, params)
        #print(params)
        f=open(symbol+'order.log','a')
        f.write(str(datetime.now())+str(ans)+'__'+symbol+'__'+tradeType+'__'+str(price)+'__'+str(amount)+'\n')
        #+_type[int(tradeType)] + ' '+str(symbol)+' '+str(contractType)+'  '+ str(amount)+'at'+ str(price)+'\n')
        f.close()
        return ans
    # 现货批量下单
    def batchTrade(self, symbol, tradeType, orders_data):
        BATCH_TRADE_RESOURCE = "/api/v1/batch_trade.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'type': tradeType,
            'orders_data': orders_data
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, BATCH_TRADE_RESOURCE, params)

    # 现货取消订单
    def cancelOrder(self, symbol, orderId):
        CANCEL_ORDER_RESOURCE = "/api/v1/cancel_order.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'order_id': orderId
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, CANCEL_ORDER_RESOURCE, params)

    # 现货订单信息查询
    def orderinfo(self, symbol, orderId):
        ORDER_INFO_RESOURCE = "/api/v1/order_info.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'order_id': orderId
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, ORDER_INFO_RESOURCE, params)

    # 现货批量订单信息查询
    # 需要用到orders info 了。哈哈哈，批量订单查询。
    def ordersinfo(self, symbol, orderId, tradeType):
        ORDERS_INFO_RESOURCE = "/api/v1/orders_info.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'order_id': orderId,
            'type': tradeType
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, ORDERS_INFO_RESOURCE, params)

    
    # 现货获得历史订单信息
    def orderHistory(self, symbol, status, currentPage, pageLength):
        ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'status': status,
            'current_page': currentPage,
            'page_length': pageLength
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, ORDER_HISTORY_RESOURCE, params)
    
    def close_all_limit_orderbook(self,symbol):
        if(os.path.exists(symbol+'order.log')):
            shutil.copyfile(symbol+'order.log',symbol+'order.log.bak')
        else:
            shutil.copyfile(symbol+'order.log.bak',symbol+'order.log')
            shutil.copyfile(symbol+'order.log',symbol+'order.log.bak')
           
        
           
        with open(symbol+'order.log') as f:
            for line in f:
                sub =line.find('order_id')
                if (sub != -1):
                    order_id = int(line[sub+10:sub+16])
                    res =self.cancelOrder(symbol,order_id)
                    f=open(symbol+'_order.log.bak','a')
                    f.write(str(line))
                    f.close()
        os.remove(symbol+'order.log')
        #print(res)
        return 0
    #close_all_limit_orderbook('wrc_eth')
    #close_all_limit_orderbook('wrc_btc')
    #kline price to df
    def price_to_df(self,symbol,frequency,count):
        price = self.kline(symbol,frequency,count)
        df = pd.DataFrame(columns  = ['timestamp','open','high','low','close','volume'])
        i=0
        for k in price:
            df.loc[i,:]=k
            i = i+1
        return df
    # actually if you canceled all orderbook,them you can delete this orderbook file ,so this function  is note
    # nesscary ,and you should keep a bak before you cancel in case interrupte this order book file.
    def clean_order_cache(symbol_list):
        for _symbol in symbol_list:
            #shutil.copyfile(_symbol+'order.log.bak',_symbol+'order.log')
            shutil.copyfile(_symbol+'order.log',_symbol+'order.log.bak')
            sleep(0.2)
            count=0
            with open(_symbol+'order.log.bak') as f:
                for line in f:
                    sub = line.find('order_id')
                    try:
                        if (sub != -1):
                            order_id = int(line[sub+10:sub+16])
                            res =json.loads(bibi.orderinfo(symbol,order_id))
                            order_info = res['orders'][0]
                            if(order_info['status']>-1 and order_info['status']<2):
                                f=open(_symbol+'_order_cache.log','a')
                                f.write(str(line))
                                f.close()
                            count = count+1
                    except:
                        pass
        os.remove(_symbol+'order.log')
        return count
#clean_order_cache(symbol_list=['wrc_btc'])



    # use获取美元人民币汇率
    def exchange_rate(self):
        EXCHANGE_RATE = "/api/v1/exchange_rate.do"
        return httpGet(self.__url, EXCHANGE_RATE, '')