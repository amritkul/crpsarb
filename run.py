#!/usr/bin/python
import fetcher
import operator
import sys
import time
import Cryptsy
import Queue
import threading

if len(sys.argv) == 2:
    ratio = float(sys.argv[1])
else:
    ratio = 0.3

#GLOBAL THREAD CONTROLLERS
BOOL_RUN_BUYSELL = 1
BOOL_RUN_ARBOPPS = 1

#global data structure


#conservatively estimate profit with 1% total fees (usually less)
fee_ratio = 0.0025

simpleArb       = []
ltcMarkets      = []
btcMarkets      = []
doubleMarkets   = []
outBuff         = {}
Orders          = {}
num_purchase = ()
stack = []
lastitem =[]
t = threading.Thread()


#helper function to format floats
def ff(f):
    return format(f, '.8f')


def buysell(lastitem):
    num_purchasable = (ltc_balance / ltc_lo_sell) * ratio
    
    #currently open buy orders
    #buy_market = fetcher.getOrders(data['buy_marketid'])
    #currently open sell orders
    #sell_market = fetcher.getOrders(data['sell_marketid'])
    buymkt = fetcher.getDepth(lastitem['buy_marketid'])
    buy = buymkt['sell']
    # first sell order on market
    buymktq = buy[0]
    print (buymktq)
    num_purchase = num_purchasable

    buyQ = buymktq[1]
    buyP = buymktq[0]
    sellmkt = fetcher.getDepth(lastitem['sell_marketid'])
    sell = sellmkt ['buy']
    # first buy order on market
    sellmktq = sell[0]
    print (sellmktq)
    sellQ = sellmktq[1]
    sellP = sellmktq[0]
    print (num_purchase)

    total_fees      = (num_purchasable * ltc_lo_sell) * fee_ratio
    total_profit    = ((btc_hi_buy - ltc_lo_sell) * num_purchasable) - total_fees

    # number i can buy
    if (float(buyQ) < float(num_purchase)):
        num_purchase = buyQ 
        print ("adjusted buy num_purchase")
        print (num_purchase)

    # number i can sell    
    if (float(sellQ) < float(num_purchase)):
        num_purchase = sellQ
        ("adjusted sell num_purchase")
        print (num_purchase)

    value = float(num_purchase) * float(lastitem['price buy']) 

    if value > 0.0000001 and total_profit > 0:
        #for elem in sell_market:
        #    print elem 
        #kill current buy orders for this market
            # todo: kill buy multiple buy/sell orders that are still open regardless of loop
        print("boobs")
        r = fetcher.placeOrder(lastitem['buy_marketid'], 'Buy', num_purchase, lastitem['price buy'])
        print(str(r))

        time.sleep(1)

        s = fetcher.placeOrder(lastitem['sell_marketid'], 'Sell', num_purchase , lastitem['price sell'])
        string = str(s)
        print (str(s))

        if(s['success']==("0")):
            for x in range (2):
                time.sleep(1)
                s = fetcher.placeOrder(lastitem['sell_marketid'], 'Sell', num_purchase, lastitem['price sell'])
                print(str(s))
            cancel = fetcher.cancelOrder(r['orderid'])
            print (str(cancel))
        else:
            pass

    print ("Not Profitable")

try:
    print "Fetching market data."
    fetcher.fetchMarketData()
except:
    sys.exit("ERROR: Could not fetch market data.")


print "Processing market data."
for marketName in fetcher.marketData['return']['markets']:
    try:
        
        sn = fetcher.marketData['return']['markets'][marketName]['primarycode']
        marketid = fetcher.marketData['return']['markets'][marketName]['marketid']
    
           
        if fetcher.marketData['return']['markets'][marketName]['secondarycode'] == 'LTC':
            ltcMarkets.append({'market': marketName, 'sn': sn, 'marketid': marketid})
        if fetcher.marketData['return']['markets'][marketName]['secondarycode'] == 'BTC':
            btcMarkets.append({'market': marketName, 'sn': sn, 'marketid': marketid})
    except:
        pass



try:
    print "Fetching LTC price."
    buymkt = fetcher.getDepth(3)
    buy = buymkt['buy']
    buymktq = buy[1]
    #print (buymktq)
    ltc_price = float(buymktq[0])
    #ltc_price = float(fetcher.getLTCPrice())

    print("LTC Price: " + format(ltc_price, '.8f')) 
except:
    print("ERROR: Could not fetch LTC price.")
    pass    

#check for ltc -> btc arb opps or btc -> ltc arb opps
try:
    print "Processing arbitrage opportunities."
    for lmkt in ltcMarkets:
        for bmkt in btcMarkets:
            if lmkt['sn'] == bmkt['sn']:
                print("Checking " + lmkt['sn'] + "...")
                try:
                    balances = fetcher.getAvailBalances()
                    btc_balance = float(balances['BTC'])
                    ltc_balance = float(balances['LTC'])
                    sn              = lmkt['sn']
                    ltc_marketid    = lmkt['marketid']
                    btc_marketid    = bmkt['marketid']
                    btcmkt = fetcher.getDepth((bmkt['marketid']))
                    # first sell order on btc market
                    btcbuy = btcmkt['sell']
                    btcbuymktq = btcbuy[0]
                    btc_lo_sell = float(btcbuymktq[0])
                    btc_lo_sellq = btcbuymktq[1]
                    # first buy order on btc market
                    btcsell = btcmkt ['buy']
                    btcsellmktq = btcsell[0]
                    btc_hi_buy  = float(btcsellmktq[0])
                    btc_hi_buyq  = btcsellmktq[1]

                    ltcmkt = fetcher.getDepth((lmkt['marketid']))
                    # first sell order on ltc market
                    ltcbuy = ltcmkt['sell']
                    ltcbuymktq = ltcbuy[0]
                    ltc_lo_sell = float(ltcbuymktq[0])
                    ltc_lo_sellq = ltcbuymktq[1]
                    # first buy order on ltc market
                    ltcsell = ltcmkt ['buy']
                    ltcsellmktq = ltcsell[0]
                    ltc_hi_buy  = float(ltcsellmktq[0])
                    ltc_hi_buyq  = ltcsellmktq[1]
                    ltc_hi_buy_btc  = ltc_hi_buy * ltc_price
                    ltc_lo_sell_btc = ltc_lo_sell * ltc_price
        #               marketdepth     = depth('marketid')
        #               orders          = marketorders['marketid']
                    print("Comparing buy price of " + ff(ltc_lo_sell) + " LTC to sell price of " + ff(btc_hi_buy) + " BTC")
                    if btc_hi_buy > ltc_lo_sell_btc: 
                        #profit to be made buying for LTC and selling for BTC
                        outBuff       = {
                            'buy_marketid'      : ltc_marketid,
                            'sell_marketid'     : btc_marketid,
                            'price buy'         : ff(ltc_lo_sell),
                            'price sell'        : ff(btc_hi_buy)
                        }
                        stack.append(outBuff)
                        if  len(stack) > 0:
                            try:
                                lastitem = stack.pop()
                                print stack
                                print lastitem
                                print stack
                                t = threading.Thread(target=buysell, args = (lastitem,))
                                t.start()
                                t.join()
                            except:
                                print ("ERROR")
                    print("Comparing buy price of " + ff(btc_lo_sell) + " BTC to sell price of " + ff(ltc_hi_buy) + " LTC")
                    if ltc_hi_buy_btc > btc_lo_sell:
                        #profit to be made buying for BTC and selling for LTC
                        outBuff        = {
                            'buy_marketid'      : btc_marketid,
                            'sell_marketid'     : ltc_marketid,
                            'price buy'         : ff(btc_lo_sell),
                            'price sell'        : ff(ltc_hi_buy)
                        }
                        stack.append(outBuff)
                        if  len(stack) > 0:
                            try:
                                lastitem = stack.pop()
                                print stack
                                print lastitem
                                print stack
                                t = threading.Thread(target=buysell, args = (lastitem,))
                                t.start()
                                t.join()
                            except:
                                print ("ERROR")

                    print("-----------")
                except:
                    pass
except:
    print "Done."



    
    





