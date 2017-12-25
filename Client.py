#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# 客户端调用，用于查看API返回结果

from OkcoinSpotAPI import OKCoinSpot
from OkcoinFutureAPI import OKCoinFuture
import logging
import time
import json
import os
import pandas as pd

# 初始化apikey，secretkey,url
fileName = 'key.json'
path = os.path.abspath(os.path.dirname(__file__))
fileName = os.path.join(path, fileName)
# 解析json文件
with open(fileName) as data_file:
    setting = json.load(data_file)
    data_file.close()
apikey = str(setting['apiKey'])
secretkey = str(setting['secretKey'])
okcoinRESTURL = 'www.okex.com'

# 现货API
okcoinSpot = OKCoinSpot(okcoinRESTURL, apikey, secretkey)

# 期货API
okcoinFuture = OKCoinFuture(okcoinRESTURL, apikey, secretkey)

spotinfo = okcoinSpot.userinfo()
spotinfo = json.loads(spotinfo)
freeamount = 0
freezedamount = 0
if spotinfo['result']:
    freeinfo = spotinfo['info']['funds']['free']
    freezedinfo = spotinfo['info']['funds']['freezed']
    for symbol in freeinfo:
        if float(freeinfo[symbol]) != 0:
            if symbol == 'btc':
                quote = 1.0
            elif symbol == 'usdt':
                quote = 1.0 / float(okcoinSpot.ticker('btc_usdt')['ticker']['last'])
            else:
                quote = float(okcoinSpot.ticker(symbol + '_btc')['ticker']['last'])
            freeamount += float(freeinfo[symbol]) * quote
            freezedamount += float(freezedinfo[symbol]) * quote

            pass

spotamount = freezedamount + freeamount
btcquote = 110000
print('Okex')
print('SpotAccount')
print('BTC: ' + str(spotamount))
print('RMB: ' + str(btcquote * spotamount))

# tradeinfo = okcoinFuture.future_trades(symbol=symbol, contractType='this_week')

futinfo = okcoinFuture.future_userinfo()
futinfo = json.loads(futinfo)
accountrights = 0

if futinfo['result']:
    futaccount = futinfo['info']
    for symbol in futaccount:
        if symbol == 'btc':
            accountrights += futaccount[symbol]['account_rights']
        else:
            quote = float(okcoinSpot.ticker(symbol + '_btc')['ticker']['last'])
            accountrights += futaccount[symbol]['account_rights'] * quote

print('FutAccount')
print('BTC: ' + str(accountrights))
print('RMB: ' + str(btcquote * accountrights))

pass
# symbol = 'etc_usd'
# contracttype = 'quarter'
# contractmultiplier = 10
# timeinteval = 10  # seconds
# leverage = '20'
# fee = -0.00025
# ratio = 0.001
# amount = 1
# ordertype = {"openlong": 1, "openshort": 2, "closelong": 3, "closeshort": 4}
#
# orderinfo = pd.DataFrame(columns=["symbol", "contracttype", "price", "amount", "ordertype"])
# position = []
# print("Started...")
# while True:
#     try:
#         posinfo = okcoinFuture.future_position(symbol, contracttype)
#         posinfo = json.loads(posinfo)
#         if posinfo['result']:
#             position = posinfo['holding'][0]
#
#         # query orderinfo
#         queryorderinfo = okcoinFuture.future_orderinfo(symbol, contracttype, '-1', '1', '0', '50')
#         queryorderinfo = json.loads(queryorderinfo)
#
#         if queryorderinfo['result']:
#             for order in queryorderinfo['orders']:
#                 orderinfo.loc[order['order_id']] = [order['symbol'], contracttype, order['price'], order['amount'],
#                                                     order['type']]
#         ordernum = max(sum(orderinfo['ordertype'] == 1) + sum(orderinfo['ordertype'] == 4),
#                        sum(orderinfo['ordertype'] == 2) + sum(orderinfo['ordertype'] == 3))
#
#         if ordernum < 50:
#             futureticker = okcoinFuture.future_ticker(symbol, contracttype)
#             ticker = futureticker['ticker']
#             ask = round(ticker['last'] * (1 + ratio), 3)
#             bid = round(ticker['last'] * (1 - ratio), 3)
#             # profit = (contractmultiplier / bid - contractmultiplier / ask) * amount*ticker['last'] - fee * amount * contractmultiplier * 2
#
#             if position['buy_available'] > amount:
#                 orderstatus = okcoinFuture.future_trade(symbol, contracttype, price=ask, amount=amount,
#                                                         tradeType=ordertype['closelong'], matchPrice='0',
#                                                         leverRate=leverage)
#                 orderstatus = json.loads(orderstatus)
#                 if orderstatus['result']:
#                     position['buy_available'] = position['buy_available'] - amount
#                     orderinfo.loc[orderstatus['order_id']] = [symbol, contracttype, ask, amount, ordertype['closelong']]
#             else:
#                 orderstatus = okcoinFuture.future_trade(symbol, contracttype, price=ask, amount=amount,
#                                                         tradeType=ordertype['openshort'], matchPrice='0',
#                                                         leverRate=leverage)
#                 orderstatus = json.loads(orderstatus)
#                 if orderstatus['result']:
#                     orderinfo.loc[orderstatus['order_id']] = [symbol, contracttype, ask, amount, ordertype['openshort']]
#
#             if position['sell_available'] > amount:
#                 orderstatus = okcoinFuture.future_trade(symbol, contracttype, price=bid, amount=amount,
#                                                         tradeType=ordertype['closeshort'], matchPrice='0',
#                                                         leverRate=leverage)
#                 orderstatus = json.loads(orderstatus)
#                 if orderstatus['result']:
#                     position['sell_available'] = position['sell_available'] - amount
#                     orderinfo.loc[orderstatus['order_id']] = [symbol, contracttype, bid, amount,
#                                                               ordertype['closeshort']]
#             else:
#                 orderstatus = okcoinFuture.future_trade(symbol, contracttype, price=bid, amount=amount,
#                                                         tradeType=ordertype['openlong'], matchPrice='0',
#                                                         leverRate=leverage)
#                 orderstatus = json.loads(orderstatus)
#                 if orderstatus['result']:
#                     orderinfo.loc[orderstatus['order_id']] = [symbol, contracttype, bid, amount, ordertype['openlong']]
#
#     except Exception as e:
#         logging.exception(e)
#
#     time.sleep(timeinteval)

# print (u' 现货行情 ')
# print (okcoinSpot.ticker('ltc_btc'))

# print (u' 现货深度 ')
# print (okcoinSpot.depth('btc_usd'))

# print (u' 现货历史交易信息 ')
# print (okcoinSpot.trades())

# print (u' 用户现货账户信息 ')
# print (okcoinSpot.userinfo())

# print (u' 现货下单 ')
# print (okcoinSpot.trade('ltc_usd','buy','0.1','0.2'))

# print (u' 现货批量下单 ')
# print (okcoinSpot.batchTrade('ltc_usd','buy','[{price:0.1,amount:0.2},{price:0.1,amount:0.2}]'))

# print (u' 现货取消订单 ')
# print (okcoinSpot.cancelOrder('ltc_usd','18243073'))

# print (u' 现货订单信息查询 ')
# print (okcoinSpot.orderinfo('ltc_usd','18243644'))

# print (u' 现货批量订单信息查询 ')
# print (okcoinSpot.ordersinfo('ltc_usd','18243800,18243801,18243644','0'))

# print (u' 现货历史订单信息查询 ')
# print (okcoinSpot.orderHistory('ltc_usd','0','1','2'))

# print(u' 期货行情信息')
# print(okcoinFuture.future_ticker('ltc_usd', 'this_week'))

# print (u' 期货市场深度信息')
# print (okcoinFuture.future_depth('btc_usd','this_week','6'))

# print (u'期货交易记录信息')
# print (okcoinFuture.future_trades('ltc_usd','this_week'))

# print (u'期货指数信息')
# print (okcoinFuture.future_index('ltc_usd'))

# print (u'美元人民币汇率')
# print (okcoinFuture.exchange_rate())

# print (u'获取预估交割价')
# print (okcoinFuture.future_estimated_price('ltc_usd'))

# print(u'获取虚拟合约的K线信息')
# print(okcoinFuture.future_kline('ltc_usd', 'this_week', '1min', '50'))

# print(u'获取当前可用合约总持仓量')
# print(okcoinFuture.future_hold_amount('ltc_usd', 'this_week'))
#
# print(u'获取合约坐高买价和最低卖价格')
# print(okcoinFuture.future_price_limit('ltc_usd', 'this_week'))
#
# print(u'获取全仓账户信息')
# print(okcoinFuture.future_userinfo())
#
# print(u'获取全仓持仓信息')
# print(okcoinFuture.future_position('ltc_usd', 'this_week'))

# print (u'期货下单')
# print(okcoinFuture.future_trade('etc_usd', 'this_week', '0.1', '1', '1', '0', '20'))

# print (u'期货批量下单')
# print (okcoinFuture.future_batchTrade('ltc_usd','this_week','[{price:0.1,amount:1,type:1,match_price:0},{price:0.1,amount:3,type:1,match_price:0}]','20'))

# print (u'期货取消订单')
# print (okcoinFuture.future_cancel('ltc_usd','this_week','47231499'))

# print (u'期货获取订单信息')
# print (okcoinFuture.future_orderinfo('ltc_usd','this_week','47231812','0','1','2'))

# print (u'期货逐仓账户信息')
# print (okcoinFuture.future_userinfo_4fix())

# print (u'期货逐仓持仓信息')
# print (okcoinFuture.future_position_4fix('ltc_usd','this_week',1))
