#!/usr/bin/python
# -*- coding: utf-8 -*-
# 用于访问OKCOIN 期货REST API
from HttpMD5Util import buildMySign, httpGet, httpPost
import logging
import time
import json
import os
import pandas as pd
import pandas.stats.moments
import numpy as np
import sys
from datetime import datetime


class OKCoinFuture:
    def __init__(self, url, apikey, secretkey):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey

    # OKCOIN期货行情信息
    
    def future_devolve(self,symbol,type='2',amount='0.01'):
        FUTURE_DEPTH_RESOURCE = "/api/v1/future_devolve.do"
        params = {
            'symbol':symbol,
            'type':type,
            'amount':amount,
        }
        params['api_key'] = self.__apikey
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_DEPTH_RESOURCE, params)

    def future_ticker(self, symbol, contractType):
        FUTURE_TICKER_RESOURCE = "/api/v1/future_ticker.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        print(params)
        return httpGet(self.__url, FUTURE_TICKER_RESOURCE, params)

    # OKCoin期货市场深度信息
    def future_depth(self, symbol, contractType, size):
        FUTURE_DEPTH_RESOURCE = "/api/v1/future_depth.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        if size:
            params += '&size=' + size if params else 'size=' + size
        return httpGet(self.__url, FUTURE_DEPTH_RESOURCE, params)

    # OKCoin期货交易记录信息
    def future_trades(self, symbol, contractType):
        FUTURE_TRADES_RESOURCE = "/api/v1/future_trades.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        return httpGet(self.__url, FUTURE_TRADES_RESOURCE, params)

    # OKCoin期货指数
    def future_index(self, symbol):
        FUTURE_INDEX = "/api/v1/future_index.do"
        params = ''
        if symbol:
            params = 'symbol=' + symbol
        return httpGet(self.__url, FUTURE_INDEX, params)

    # 获取美元人民币汇率
    def exchange_rate(self):
        EXCHANGE_RATE = "/api/v1/exchange_rate.do"
        return httpGet(self.__url, EXCHANGE_RATE, '')

    # 获取预估交割价
    def future_estimated_price(self, symbol):
        FUTURE_ESTIMATED_PRICE = "/api/v1/future_estimated_price.do"
        params = ''
        if symbol:
            params = 'symbol=' + symbol
        return httpGet(self.__url, FUTURE_ESTIMATED_PRICE, params)

    # 获取虚拟合约的K线信息
    def future_kline(self, symbol, contractType, type, size=0, since=0):
        #print(symbol,contractType,type,size)
        FUTURE_USERINFO = "/api/v1/future_kline.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        if type:
            params += '&type=' + type if params else 'type=' + type
        params += '&size=' + str(size) + '&since=' + str(since)
        #print('-------',params)
        return httpGet(self.__url, FUTURE_USERINFO, params)

    # 获取当前可用合约总持仓量
    def future_hold_amount(self, symbol, contractType):
        FUTURE_USERINFO = "/api/v1/future_hold_amount.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        return httpGet(self.__url, FUTURE_USERINFO, params)

    # 获取合约最高买价和最低卖价
    def future_price_limit(self, symbol, contractType):
        FUTURE_USERINFO = "/api/v1/future_price_limit.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        return httpGet(self.__url, FUTURE_USERINFO, params)

    # 期货全仓账户信息
    def future_userinfo(self):
        FUTURE_USERINFO = "/api/v1/future_userinfo.do?"
        params = {}
        params['api_key'] = self.__apikey
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_USERINFO, params)

    # 期货全仓持仓信息
    def future_position(self, symbol, contractType):
        FUTURE_POSITION = "/api/v1/future_position.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_POSITION, params)

    # 期货下单
    def future_trade(self, symbol, contractType, price='', amount='', tradeType='', matchPrice='', leverRate=''):
        FUTURE_TRADE = "/api/v1/future_trade.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'amount': amount,
            'type': tradeType,
            'match_price': matchPrice,
            'lever_rate': leverRate
        }
        _type ={
            1:'open long',
            2:'open short',
            3:'close long',
            4:'close short',
        }
        if price:
            params['price'] = price
        params['sign'] = buildMySign(params, self.__secretkey)
        ans = httpPost(self.__url, FUTURE_TRADE, params)
        f=open(symbol+contractType+'order.log','a')
        f.write(str(datetime.now())+ans+_type[int(tradeType)] + ' '+str(symbol)+' '+str(contractType)+'  '+ str(amount)+'at'+ str(price)+'\n')
        f.close()
        return ans
            

    # 期货批量下单
    def future_batchTrade(self, symbol, contractType, orders_data, leverRate):
        FUTURE_BATCH_TRADE = "/api/v1/future_batch_trade.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'orders_data': orders_data,
            'lever_rate': leverRate
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_BATCH_TRADE, params)
    
    # 期货取消所有限价单
    def close_all_limit_orderbook(self,symbol,contractType):
        with open(symbol+contractType+'order.log') as f:
            for line in f:
                sub =line.find('order_id')
                if (sub != -1):
                    order_id = int(line[sub+10:sub+21])
                    res =self.future_cancel(symbol,contractType,order_id)
                    #print(res)
        return 0
    

    # 期货取消订单
    def future_cancel(self, symbol, contractType, orderId):
        FUTURE_CANCEL = "/api/v1/future_cancel.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'order_id': orderId
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_CANCEL, params)

    # 期货获取订单信息
    def future_orderinfo(self, symbol, contractType, orderId, status='', currentPage='', pageLength=''):
        FUTURE_ORDERINFO = "/api/v1/future_order_info.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'order_id': orderId,
            'status': status,
            'current_page': currentPage,
            'page_length': pageLength
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_ORDERINFO, params)
    # 所有限价单信息
    #def get_all_limitorder(self,symbol,contractType):
    #    with open(symbol+contractType+'order.log') as f:
    ##           sub =line.find('order_id')
    #            if (sub != -1):
    #                order_id = int(line[sub+10:sub+21])
    #                res =self.(symbol,contractType,order_id)
     #   

    # 期货逐仓账户信息
    def future_userinfo_4fix(self):
        FUTURE_INFO_4FIX = "/api/v1/future_userinfo_4fix.do?"
        params = {'api_key': self.__apikey}
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_INFO_4FIX, params)

    # 期货逐仓持仓信息
    def future_position_4fix(self, symbol, contractType, type1):
        FUTURE_POSITION_4FIX = "/api/v1/future_position_4fix.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'type': type1
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_POSITION_4FIX, params)
    def open_long(self,symbol,period,price,amount,matchType=0,leverRate=20):
        return self.future_trade(symbol,period, price,amount, '1', matchType,leverRate)
    def close_long(self,symbol,period,price,amount,matchType=0,leverRate=20):
        return self.future_trade(symbol,period, price,amount, '3', matchType,leverRate)
    def open_short(self,symbol,period,price,amount,matchType=0,leverRate=20):
        return self.future_trade(symbol,period, price,amount, '2', matchType,leverRate)
    def close_short(self,symbol,period,price,amount,matchType=0,leverRate=20):
        return self.future_trade(symbol,period, price,amount, '4', matchType,leverRate)
    def get_future_userinfo_df(self):
        futinfo = self.future_userinfo()
        #print(futinfo)
        futinfo = json.loads(futinfo)
        df = pd.DataFrame()
        for k,v in futinfo['info'].items():
            for _k,_v in v.items():
                df.loc[k,_k]= _v
        return df
    def get_all_future_position(self,security,period):
        df = pd.DataFrame()
        i=0
        for se in security:
            for per in period:
                df.loc[i,'symbol'] = se
                df.loc[i,'period'] = per
                df.loc[i,'current_price']=self.future_ticker(se,per)['ticker']['last']
                tmp = json.loads(self.future_position(se,per))
                try:
                    for k,v in tmp['holding'][0].items():
                        df.loc[i,k] = v
                except:
                    pass

                else:
                    pass    
                i=i+1
        df = df.fillna(0)
        return df

    def close_all_position(self,security,period):
        info = self.get_all_future_position(security,period)
        for i in info.index:
            symbol = str(info.loc[i,'symbol'])
            _period = str(info.loc[i,'period'])
            price  = self.future_ticker(symbol,_period)['ticker']['last']
            leverRate=20
            matchType = 0

            long_mount = int(info.loc[i,'buy_available'])
            short_mount= int(info.loc[i,'sell_available'])
            self.close_long(symbol,_period,price,long_mount,matchType,leverRate)
            self.close_short(symbol,_period,price,short_mount,matchType,leverRate)
        return self.get_all_future_position(security,period)['buy_available']
    #
    # price: pd.DataFrame ,only DataFrame have shift 
    # n window 窗口长度
    # power1 短均线 n
    # power2 长均线 n值
    def KAMA(self,price, n=10, pow1=2, pow2=30):
        ''' kama indicator '''    
        ''' accepts pandas dataframe of prices '''

        absDiffx = abs(price - price.shift(1) )  

        ER_num = abs( price - price.shift(n) )
        ER_den = pandas.stats.moments.rolling_sum(absDiffx,n)
        ER = ER_num / ER_den

        sc = ( ER*(2.0/(pow1+1)-2.0/(pow2+1.0))+2/(pow2+1.0) ) ** 2.0


        answer = np.zeros(sc.size)
        N = len(answer)
        first_value = True

        for i in range(N):
            print('-----',sc)
            if sc[i] != sc[i]:
                answer[i] = np.nan
            else:
                if first_value:
                    answer[i] = price[i]
                    first_value = False
                else:
                    answer[i] = answer[i-1] + sc[i] * (price[i] - answer[i-1])
        return answer