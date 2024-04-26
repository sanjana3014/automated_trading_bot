# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:28:44 2020

@author: Sanjana

"""
import ccxt
import pandas as pd 
import urllib3
from bs4 import BeautifulSoup
import talib
#from numpy import array
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from bitmex1 import bitmex1 #taken from https://github.com/mazmex7/BitMEX-API-python which is better than the offical bitmex api    
import calendar
import time
import traceback
import os    #complicated file and file location checking/creating. IGNORE THIS CODE!
from pathlib import Path
path = str(Path(__file__).parent.absolute())
path1=path.replace("\\","\\\\")
import os.path
from os import path #States_Order
if os.name == 'nt': 
    dash='\\\\'
print('windows')
if path.exists(path1+"\\States_Market.txt") == False:
    print('', file=open(path1+"\\States_Market.txt", "w"))
if path.exists(path1+"\\States_Order.txt") == False:
    print('', file=open(path1+"\\States_Order.txt", "w"))
if path.exists(path1+"\\States_Possible.txt") == False:
    print('', file=open(path1+"\\States_Possible.txt", "w"))
if path.exists(path1+"\\States_isOpen.txt") == False:
    print('', file=open(path1+"\\States_isOpen.txt", "w"))
if path.exists(path1+"\\States_SL.txt") == False:
    print('', file=open(path1+"\\States_SL.txt", "w"))
if path.exists(path1+"\\States_TP.txt") == False:
    print('', file=open(path1+"\\States_TP.txt", "w"))
else:
    print('linux')
dash="/"
if path.exists(path1+"/States_Market.txt") == False:
    print('', file=open(path1+"/States_Market.txt", "w"))
if path.exists(path1+"/States_Order.txt") == False:
    print('', file=open(path1+"/States_Order.txt", "w"))
if path.exists(path1+"/States_Possible.txt") == False:
    print('', file=open(path1+"/States_Possible.txt", "w"))
if path.exists(path1+"/States_isOpen.txt") == False:
    print('', file=open(path1+"/States_isOpen.txt", "w"))
if path.exists(path1+"/States_SL.txt") == False:
    print('', file=open(path1+"/States_SL.txt", "w"))
if path.exists(path1+"/States_TP.txt") == False:
    print('', file=open(path1+"/States_TP.txt", "w"))
    
States_Market=path1+dash+"States_Market.txt"
States_Order=path1+dash+"States_Order.txt"
States_Possible=path1+dash+"States_Possible.txt"
States_isOpen=path1+dash+"States_isOpen.txt"
States_SL=path1+dash+"States_SL.txt"
States_TP=path1+dash+"States_TP.txt"
    
while True: 
    try: 
        api_key = '' #your api key
        api_secret = '' #api secret key
        #whenever bitmex_cli is used, 1 api useage instance is tracked by bitmex.  Bitmex only allows 15 api calls per minute
        bitmex_cli = bitmex1(test=False, api_key=api_key, api_secret=api_secret)#this wrapper used due to supporting leverage and the simplicity of creating market/limit orders.  Also  closes orders.
        #creating dataframe that will be used to store candlestick data. 
        df=pd.DataFrame()
        timep= df.append({'time':1}, ignore_index=True)
        timep=timep.iloc[0:0]
        openp= df.append({'open':1}, ignore_index=True)
        openp=openp.iloc[0:0]
        highp= df.append({'high':2}, ignore_index=True)
        highp=highp.iloc[0:0]
        lowp= df.append({'low':3}, ignore_index=True)
        lowp=lowp.iloc[0:0]
        closep= df.append({'close':4}, ignore_index=True)
        closep=closep.iloc[0:0]
        volumep= df.append({'volume':1}, ignore_index=True)
        volumep=volumep.iloc[0:0]
         
         
        bitmex   = ccxt.bitmex({#ccxt bitmex api is used for obtaining candlestick data
            'apiKey': api_key,
            'secret': api_secret,
        })
        ###################################################################################
        #current eth bid&ask scraping from bitmex website due to limited api calls allowed per min
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        http = urllib3.PoolManager()
        response = http.request('GET', 'https://www.bitmex.com/app/trade/XBTUSD')
        soup = BeautifulSoup(response.data,features="lxml")  # Note the use of the .data property
        soup=str(soup)
        soup=soup[(soup.find('BitMEXdotcom">Twitter</a></div></div></div></footer></div></body></html')-9000):]
         
        xbt_bid=float(soup[soup.find('"bidPrice":')+11:soup.find(',"midPrice":')])
        xbt_ask=float(soup[soup.find('"askPrice":')+11:soup.find(',"impactBidPrice":')])
        print('IGNORE ABOVE WARNINGS, COMMON BITMEX API WARNING THAT IS HARMLESS')
        print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        ###################################################################
        ################### GET CANDLESTICK DATA FROM API #################
        ###################################################################
        #get candle data
        print('Downloading Candle Data ...')
        #weird oddity with bitmex, api only accepts epoch time that exactly ends on the 1h second. hacky code used to conform to bitmex (DO NOT TOUCH!)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        http = urllib3.PoolManager()
        response = http.request('GET', 'https://api.kraken.com/0/public/OHLC?pair=BTCUSD&interval=60')
        soup = BeautifulSoup(response.data,features="lxml")  # Note the use of the .data property
        soup=str(soup)
        time_string=soup[50:60]
        time_int=int(time_string)*1000
        candles=str(bitmex.fetch_ohlcv('BTC/USD', timeframe = '5m', since = (time_int+(604800 + 86400+ 86400 + 86400)*1000), limit = 500, params = {}))
        print(candles)
        #converting candles data string to pandas dataframe. data was fetched from ccxt api.
        candles_number=candles.count('.')/5
        print(candles_number)
        while candles_number>0:
            candle_location=candles.find('],')
            candles_placeholder=candles[0:candle_location]
            candles=candles[candle_location+4:]
            print(candles_placeholder)
            getdate_int=candles_placeholder.find(',')
            getdate_string=candles_placeholder[0:getdate_int]
            getdate_string=getdate_string.replace('[','')
            getdate_string=getdate_string.replace(' ','')
            getdate_string=getdate_string[0:10]
            timep.loc[len(timep)]=[getdate_string]
            candles_placeholder=candles_placeholder[getdate_int+1:]
            getopen_int=candles_placeholder.find(',')
            getopen_string=candles_placeholder[0:getopen_int]
            getopen_string=getopen_string.replace(' ','')
            openp.loc[len(openp)]=[getopen_string] 
            candles_placeholder=candles_placeholder[getopen_int+1:]
            gethigh_int=candles_placeholder.find(',')
            gethigh_string=candles_placeholder[0:gethigh_int]
            gethigh_string=gethigh_string.replace(' ','')
            highp.loc[len(highp)]=[gethigh_string]
            candles_placeholder=candles_placeholder[gethigh_int+1:]
            getlow_int=candles_placeholder.find(',')
            getlow_string=candles_placeholder[0:getlow_int]
            getlow_string=getlow_string.replace(' ','')
            lowp.loc[len(lowp)]=[getlow_string]
            candles_placeholder=candles_placeholder[getlow_int+1:]    
            candles_number=candles_number-1
            getclose_int=candles_placeholder.find(',')
            getclose_string=candles_placeholder[0:getclose_int]
            getclose_string=getclose_string.replace(' ','')
            closep.loc[len(closep)]=[getclose_string]
            candles_placeholder=candles_placeholder[getclose_int+1:]    
            candles_placeholder=candles_placeholder.replace(' ','')
            candles_placeholder=candles_placeholder.replace(']','')
            volumep.loc[len(volumep)]=[candles_placeholder]
        ohlcv1h=pd.concat([timep,openp,highp,lowp,closep,volumep],axis=1)
        ohlcv1h=ohlcv1h.apply(pd.to_numeric)
        ohlcv1h.to_csv(path1+dash+'ohlc.csv', encoding='utf-8', index=False)
        df = pd.read_csv('ohlc.csv')
        #Set the date as the index for the data
        #saving candledata to csv, can be used graphing purposes(wont be used right now):
        #https://www.techtrekking.com/how-to-plot-simple-and-candlestick-chart-using-python-pandas-matplotlib/
        print('done')
        print('===========STATE OF THE ALGO================')
        print(ohlcv1h)
        ###################################################################
        ######################Preparing States#############################
        ###################################################################
        bitmex_balance=str(bitmex.fetch_balance())
        print(bitmex_balance)
        if "'used': 0.0," not in bitmex_balance:
            print('YES', file=open(States_isOpen, "w"))
        else:
            print('NO', file=open(States_isOpen, "w"))
        """
        market_statetxt = open(States_Market, 'r')  # Open the file for reading.
        market_state = str(market_statetxt.readlines())
        market_state=market_state.replace('[','')
        market_state=market_state.replace("'","")
        market_state=market_state.replace("n","")
        market_state=market_state.replace("\\","")
        market_state=market_state.replace("]","")
        print(market_state , ' current market state')
        order_statetxt = open(States_Order, 'r')  # Open the file for reading.
        order_state = str(order_statetxt.readlines())
        order_state=order_state.replace('[','')
        order_state=order_state.replace("'","")
        order_state=order_state.replace("n","")
        order_state=order_state.replace("\\","")
        order_state=order_state.replace("]","")
        print(order_state , ' current order state')
        order_possibletxt = open(States_Possible, 'r')  # Open the file for reading.
        order_possible = str(order_possibletxt.readlines())
        order_possible=order_possible.replace('[','')
        order_possible=order_possible.replace("'","")
        order_possible=order_possible.replace("n","")
        order_possible=order_possible.replace("\\","")
        order_possible=order_possible.replace("]","")
        print(order_possible , ' current is_order_possible')
        order_isopentxt = open(States_isOpen, 'r')  # Open the file for reading.
        order_isopen = str(order_isopentxt.readlines())
        order_isopen=order_isopen.replace('[','')
        order_isopen=order_isopen.replace("'","")
        order_isopen=order_isopen.replace("n","")
        order_isopen=order_isopen.replace("\\","")
        order_isopen=order_isopen.replace("]","")
        print(order_isopen, ' current order_isOpen')
        order_SL=str(order_SLtxt.readlines())
        order_SL=order_SL.replace('[','')
        order_SL=order_SL.replace("'","")
        order_SL=order_SL.replace("n","")
        order_SL=order_SL.replace("\\","")
        order_SL=order_SL.replace("]","")
        if (order_SL) == '':
            print('no SL')
        else:
            order_SL=float(order_SL)
            order_SL=round(order_SL)
            print(str(order_SL) ,' is SL')
        order_TPtxt = open(States_TP, 'r')
        order_TP = str(order_TPtxt.readlines())
        order_TP=order_TP.replace('[','')
        order_TP=order_TP.replace("'","")
        order_TP=order_TP.replace("n","")
        order_TP=order_TP.replace("\\","")
        order_TP=order_TP.replace("]","")
        if (order_TP) == '':
            print('no TP')
        else:
            order_TP=float(order_TP)
            order_TP=round(order_TP, 2)
            print(str(order_TP), ' is TP')
        """
        print('============================================')
        bitmex_balance=str(bitmex.fetch_balance())
        bitmex_balance_int=bitmex_balance.find("'total': {'BTC")
        new_string=bitmex_balance[bitmex_balance_int:]
        new_string=new_string.replace("'total': {'BTC': ","")
        print(new_string)
        print('~~~~~~~~~~~~~~~~~~~~~~~')
        new_string=new_string[:new_string.find(",")]
        new_string=new_string.replace("}","")
        new_string=new_string.replace(",","")
        #new_string=new_string[:new_string.find(",")]
        balance_float=float(new_string)
        print('===========BALANCE==========================')
        print(balance_float, ' is the current bitcoin balance')
        xbt_contract=balance_float/(((xbt_bid+xbt_ask)/2)/1000000)
        xbt_contract=int(xbt_contract)
        xbt_contract=int((xbt_contract*2)-(0.02*xbt_contract))
        #print(xbt_contract, ' is the amount of contracts you can buy with 2x leverage')
        print('============================================')
        ###################################################################
        ################### MATH CODE / INDICATOR CALCS ###################
        ###################################################################
        psar = talib.SAR(np.array(ohlcv1h.high), np.array(ohlcv1h.low), acceleration=0.02, maximum=0.2)
        macd, signal, hist = talib.MACD(np.array(ohlcv1h.close), fastperiod=12, slowperiod=26, signalperiod=9)
        current_price=(xbt_bid+xbt_ask)/2
        ###################################################################
        #Start of algo logic
        #CRITICAL PART OF ALGO:
        #DEBUG MENU
        debug=False
        if False:#SET TO FALSE TO PREVENT DEBUGGING (ADJUST VALUES FOR ALGORITHM TESTING, KEEP FALSE WHEN YOU WANT TO STOP TESTING FOR LIVE TRADING)
            debug=True
            print('===========DEBUGGING STATE OF ALGO==========')
            df = df.set_index(pd.DatetimeIndex(df['Date'].values))
            #Show the dataframe
            df
            # Visually Show The Stock Price(s)
            # Create the title
            title = 'Close Price History    '
            #Get the stocks
            my_statistics = df
            #Create and plot the graph
            plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
            plt.plot( my_statistics['Close'],  label='Close')#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
            plt.xticks(rotation=45) 
            plt.title(title)
            plt.xlabel('Date',fontsize=18)
            plt.ylabel('Price USD ($)',fontsize=18)
            plt.show()
            slow_macd = df.Close.ewm(span=26, adjust=False).mean()
            fast_macd = df.Close.ewm(span=12, adjust=False).mean()
            MACD = slow_macd - fast_macd
            order_check='NO'
            signal = MACD.ewm(span=9, adjust=False).mean()
            df['MACD'] = MACD 
            df['Signal Line'] = signal
            #order_TP=185
            #order_SL=173 #Not all states are going to be used for this simple trading bot, this is just an example and your real algos should be very complicated hence why there should be many states of tracking
            order_isopen='NO'
            order_possible='NO'
            order_state='LONG'
            market_state='NO'
            print('Current MACD: '+str(slow_macd))   
            print('Previous MACD: '+str(fast_macd))
            print('Current Price: '+str(current_price))
            print(order_check, ' current order_isOpen')
            #print(str(order_TP), ' current SL')
            #print(str(order_SL), ' current TP')
            print(order_isopen, ' current order_isOpen')
            print(order_state, ' current order state')
            order_SL= current_price - (2/100)*current_price
            print('============================================')
        print('===========STATE OF THE MARKET==============')
        #print('XBT/USD Bid: '+str(xbt_bid))
        #print('XBT/USD Ask: '+str(xbt_ask))
        #n= len(signal)
        #for i in range(0, n):
        if 'MACD' > 'Signal Line' and order_isopen=="YES" and order_state == "SHORT":
            if 'order_Price' > 'current_price':
                close_order=bitmex_cli.Order.Order_new(symbol='XBTUSD',ordType = 'Market',execInst ='Close', text='kekClose').result()
                print('Closed the previous SHORT Order')
                print('Opened Market Long Order with 1x leverage')
                print('updating states: isOpen==Yes, States_Order==Long')
                open_order = bitmex_cli.Order.Order_new(symbol='XBTUSD', ordType = 'Market', orderQty=(xbt_contract*(-1))/2, text='kekOpen').result()
                set_leverage=bitmex_cli.Position.Position_updateLeverage(symbol='XBTUSD', leverage=1 ).result()
                open_remainder_leveraged = bitmex_cli.Order.Order_new(symbol='XBTUSD', ordType = 'Market', orderQty=(xbt_contract*(-1))/2, text='kekOpen').result()
        elif 'MACD' > 'Signal Line' and order_isopen=="NO":
                print('Opened Market Long Order with 1x leverage')
                print('updating states: isOpen==Yes, States_Order==Long')
                open_order = bitmex_cli.Order.Order_new(symbol='XBTUSD', ordType = 'Market', orderQty=(xbt_contract*(-1))/2, text='kekOpen').result()
                set_leverage=bitmex_cli.Position.Position_updateLeverage(symbol='XBTUSD', leverage=1 ).result()
                open_remainder_leveraged = bitmex_cli.Order.Order_new(symbol='XBTUSD', ordType = 'Market', orderQty=(xbt_contract*(-1))/2, text='kekOpen').result()
        elif 'MACD' < 'Signal Line' and order_isopen=="YES" and order_state=="LONG":
                close_order=bitmex_cli.Order.Order_new(symbol='XBTUSD',ordType = 'Market',execInst ='Close', text='kekClose').result()
                print('Closed the previous LONG Order')
                print('Opened Market Short Order with 1x leverage')
                print('updating states: isOpen==Yes, States_Order==Short')
                open_order = bitmex_cli.Order.Order_new(symbol='XBTUSD', ordType = 'Market', orderQty=(xbt_contract*(-1))/2, text='kekOpen').result()
                set_leverage=bitmex_cli.Position.Position_updateLeverage(symbol='XBTUSD', leverage=1 ).result()
                open_remainder_leveraged = bitmex_cli.Order.Order_new(symbol='XBTUSD', ordType = 'Market', orderQty=(xbt_contract*(-1))/2, text='kekOpen').result()
        elif 'MACD' < 'Signal Line' and order_isopen=="NO":
                     print('Opened Market Short Order with 1x leverage')
                     print('updating states: isOpen==Yes, States_Order==Short')
                     open_order = bitmex_cli.Order.Order_new(symbol='XBTUSD', ordType = 'Market', orderQty=(xbt_contract*(-1))/2, text='kekOpen').result()
                     set_leverage=bitmex_cli.Position.Position_updateLeverage(symbol='XBTUSD', leverage=1 ).result()
                     open_remainder_leveraged = bitmex_cli.Order.Order_new(symbol='XBTUSD', ordType = 'Market', orderQty=(xbt_contract*(-1))/2, text='kekOpen').result()
                     order_Price= bitmex_cli.Position.Position_currentCost.result()
        if order_isopen=="YES":
            if order_state == "LONG":
                print('current long order is open')
                if current_price <= float(order_SL):
                    print('Stop loss reached!!! :(')
                    close_order=bitmex_cli.Order.Order_new(symbol='XBTUSD',ordType = 'Market',execInst ='Close', text='kekClose').result()
                else:
                    display_SL=float(order_SL)
                    print('you are $'+str(round(current_price-display_SL, 2))+' from hitting the stop loss')
                    
            elif order_state == "SHORT":
                if current_price >= float(order_SL):
                    print('Stop loss reached!!! :(')
                    close_order=bitmex_cli.Order.Order_new(symbol='XBTUSD',ordType = 'Market',execInst ='Close', text='kekClose').result()
                else:
                    display_SL=float(order_SL)
                    print('you are $'+str(round(display_SL-current_price, 2))+' from hitting the stop loss')
        print('============================================')
        ###################################################
        #if debug==True:
            #'''
            #print('', file=open(States_TP, "w"))
            #print('', file=open(States_SL, "w"))#print can be used to write states to files
            #print('', file=open(States_isOpen, "w"))
            #print('', file=open(States_Order, "w"))
            #'''
        ###################################################
        time.sleep(10)#sleep code, probably best to sleep for 15-30 seconds. Only allowed 15 api calls per minute, we are using 6 api calls every loop of this algo.   
    except Exception as e:#always have exceptions while scripts loop for long periods of time. Script can crash if internet connection is lost without exceptions.
         print(str(e))
         print(traceback.format_exc())
'''
    import urllib3
    from bs4 import BeautifulSoup
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()
    response = http.request('GET', ' https://www.coingecko.com/en/coins/bitcoin')
    xbt_string = BeautifulSoup(response.data,features="lxml")  # Note the use of the .data property
    xbt_string=str(xbt_string)
    xbt_string=eth_string[xbt_string.find('{"@type":"Offer","price":"'):xbt_string.find('","priceCurrency":"USD"}}')]
    xbt_string=float(xbt_string[26:])
    print(xbt_string)
'''

