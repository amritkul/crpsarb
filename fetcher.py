import time
import Cryptsy

#time to hold in cache, in seconds - this only applies for google AppEngine
ttc = 5

lastFetchTime = 0

cryptsy_pubkey = "6d1176c65a8cfebcc6c639fa927b27d5d6ead4d3"
cryptsy_privkey = "53e36aee267a948b30b241c7a785ea09fe1abc5047e9f5d8677a8c7eda5edf68163ca758936e9fed"

def fetchMarketData():
    global lastFetchTime
    global cryptsy_pubkey
    global cryptsy_privkey
    global cryptsyHandle
    global marketData

    if getCachedTime():
        cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
        marketData = cryptsyHandle.getMarketDataV2()
        try:
            if marketData['success'] == 1:
                lastFetchTime = time.time()
        except:
            fetchMarketData()

"""def serverdatetime():
    info = fetcher.getinfo()
    daytime = str(info['serverdatetime'])
    date = datetime.datetime(daytime[0:9])
    time = datetime.datetime(daytime[11:17])
    return (date, time)
"""
            
def getMarketData():
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    r = cryptsyHandle.getMarketDataV2()
    return r['return']
        
def getLTCPrice():
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    r = cryptsyHandle.getSingleMarketData(3)
    try:
        return r['return']['markets']['LTC']['sellorders'][0]['price']
    except:
        getLTCPrice()

def getInformation():
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    r = cryptsyHandle.getInfo()
    return r['return']

"""def getCurrencyPrice(marketid):
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    r = cryptsyHandle.getSingleMarketData(marketid)
    try:
        return r['return']['markets'][data['marketid']]['sellorders'][0]['price']
    except:
        getCurrencyPrice()
"""
def getAvailBalances():
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    r = cryptsyHandle.getInfo()
    return r['return']['balances_available']


def getHoldBalances():
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    r = cryptsyHandle.getInfo()
    return r['return']['balances_hold']


def getOrders(marketid):
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    r = cryptsyHandle.myOrders(marketid)
    return r ['return']

def marketTrans(marketid, limit=1):
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    r = cryptsyHandle.myTrades(marketid)
    return r ['return']

def getDepth(marketid):
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    r = cryptsyHandle.depth(marketid)
    return r ['return']

def placeOrder(marketid, ordertype, quantity, price):
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    return cryptsyHandle.createOrder(marketid, ordertype, quantity, price)

def cancelMarketOrders(self, marketid):
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    return cryptsyHandle.cancelMarketOrders(marketid)
    
def cancelOrder(orderid):
    global cryptsyHandle
    cryptsyHandle = Cryptsy.Cryptsy(cryptsy_pubkey, cryptsy_privkey)
    return cryptsyHandle.cancelOrder(orderid)
    
def getCachedTime():
    return (time.time() - lastFetchTime) > ttc
