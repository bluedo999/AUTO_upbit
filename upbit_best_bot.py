import myUpbit
import time
import pyupbit
import ende_key
import my_key
import line_alert
import json

simpleEnDecrypt = myUpbit.SimpleEnDecrypt(ende_key.ende_key)
Upbit_AccessKey = simpleEnDecrypt.decrypt(my_key.upbit_access)
Upbit_ScretKey = simpleEnDecrypt.decrypt(my_key.upbit_secret)
upbit = pyupbit.Upbit(Upbit_AccessKey, Upbit_ScretKey)
BTC_Portion = 0.25
BTC_Ticker = "KRW-BTC"
ETH_Portion = 0.15
ETH_Ticker = "KRW-ETH"
Best_Alt_Portion = 0.15 
BestCoinList = ['KRW-ADA','KRW-DOT','KRW-AVAX','KRW-SOL','KRW-MATIC','KRW-ALGO','KRW-MANA','KRW-LINK','KRW-BAT','KRW-ATOM']
Each_BestCoin_Portion = Best_Alt_Portion / float(len(BestCoinList))
print("Each_BestCoin_Portion : ", Each_BestCoin_Portion)
ALT_Atype_Portion = 0.08
ALT_Btype_Portion = 0.08
DolPa_Coin = 0.14
MaxDolPaCoinCnt = 5.0
Each_DolPa_Portion = DolPa_Coin / MaxDolPaCoinCnt
DolPaCoinList = list()
dolpha_type_file_path = "./DolPaCoin.json"
try:
    with open(dolpha_type_file_path, "r") as json_file:
        DolPaCoinList = json.load(json_file)
except Exception as e:
    print("Exception:", e)
time_info = time.gmtime()
hour = time_info.tm_hour
min = time_info.tm_min
print(hour,min)
Cash_Portion = 0.15
ALT_Atype_MaxCnt = 2.0
ALT_Atype_Greed_Gap = 0.2
ALT_Atype_First_Buy_Rate = 0.2
AltAtypeList = list()
atype_file_path = "./AltATypeCoin.json"
try:
    with open(atype_file_path, "r") as json_file:
        AltAtypeList = json.load(json_file)
except Exception as e:
    print("Exception:", e)
ALT_Btype_MaxCnt = 3.0
ALT_Btype_Greed_Gap = 0.4
ALT_Btype_First_Buy_Rate = 0.1
AltBtypeList = list()
btype_file_path = "./AltBTypeCoin.json"
try:
    with open(btype_file_path, "r") as json_file:
        AltBtypeList = json.load(json_file)
except Exception as e:
    print("Exception:", e)
Tickers = pyupbit.get_tickers("KRW")
MinimunCash = 5000.0
#MinimunGap =  0.03
Target_Revenue_Rate = 1.1
balances = upbit.get_balances()
TotalMoney = myUpbit.GetTotalMoney(balances)
TotalRealMoney = myUpbit.GetTotalRealMoney(balances)
TotalRevenue = (TotalRealMoney - TotalMoney) * 100.0/ TotalMoney
print("-----------------------------------------------")
print ("Total Money:", myUpbit.GetTotalMoney(balances))
print ("Total Real Money:", myUpbit.GetTotalRealMoney(balances))
print ("Total Revenue", TotalRevenue)
print("-----------------------------------------------")
ALT_Atype_CoinMaxMoney = ((TotalRealMoney * ALT_Atype_Portion) / ALT_Atype_MaxCnt)
ALT_Atype_FirstEnterMoney = ALT_Atype_CoinMaxMoney * ALT_Atype_First_Buy_Rate
if ALT_Atype_FirstEnterMoney < MinimunCash * 2.5:
    ALT_Atype_FirstEnterMoney = MinimunCash * 2.5
ALT_Atype_TotalWaterMoney = ALT_Atype_CoinMaxMoney * (1.0 - ALT_Atype_First_Buy_Rate)
ALT_Atype_Greed_Money = (MinimunCash * 1.5)
ALT_Atype_Maximun_Greed_Cnt = ALT_Atype_TotalWaterMoney / ALT_Atype_Greed_Money
print ("->ALT_Atype_CoinMaxMoney:", ALT_Atype_CoinMaxMoney)
print ("->ALT_Atype_FirstEnterMoney", ALT_Atype_FirstEnterMoney)
print ("->ALT_Atype_TotalWaterMoney", ALT_Atype_TotalWaterMoney)
print ("->ALT_Atype_Maximun_Greed_Cnt", ALT_Atype_Maximun_Greed_Cnt)
print ("->ALT_Atype_Greed_Money", ALT_Atype_Greed_Money)
print("-----------------------------------------------")
ALT_Btype_CoinMaxMoney = ((TotalRealMoney * ALT_Btype_Portion) / ALT_Btype_MaxCnt)
ALT_Btype_FirstEnterMoney = ALT_Btype_CoinMaxMoney * ALT_Btype_First_Buy_Rate
if ALT_Btype_FirstEnterMoney < MinimunCash * 2.5:
    ALT_Btype_FirstEnterMoney = MinimunCash * 2.5
ALT_Btype_TotalWaterMoney = ALT_Btype_CoinMaxMoney * (1.0 - ALT_Btype_First_Buy_Rate)
ALT_Btype_Greed_Money = (MinimunCash * 1.5)
ALT_Btype_Maximun_Greed_Cnt = ALT_Btype_TotalWaterMoney / ALT_Btype_Greed_Money
print ("->ALT_Btype_CoinMaxMoney:", ALT_Btype_CoinMaxMoney)
print ("->ALT_Btype_FirstEnterMoney", ALT_Btype_FirstEnterMoney)
print ("->ALT_Btype_TotalWaterMoney", ALT_Btype_TotalWaterMoney)
print ("->ALT_Btype_Maximun_Greed_Cnt", ALT_Btype_Maximun_Greed_Cnt)
print ("->ALT_Btype_Greed_Money", ALT_Btype_Greed_Money)
print("-----------------------------------------------")
print("len(AltAtypeList)",len(AltAtypeList))
print("len(AltBtypeList)",len(AltBtypeList))
if myUpbit.IsHasCoin(balances,BTC_Ticker) == True:
    NowCoinTotalMoney = myUpbit.GetCoinNowRealMoney(balances,BTC_Ticker)
    Rate = NowCoinTotalMoney / TotalRealMoney
    print("--------------> BTC rate : ", Rate)
    if Rate != BTC_Portion:
        GapRate = BTC_Portion - Rate
        print("--------------> BTC Gaprate : ", GapRate)
        GapMoney = TotalRealMoney * abs(GapRate)
        if GapRate < 0:
            if GapMoney >=  MinimunCash * 1.2 and abs(GapRate) >= (BTC_Portion / 20.0): 
                print("--------------> SELL BITCOIN!!!!")
                revenue_rate = myUpbit.GetRevenueRate(balances,BTC_Ticker)
                if revenue_rate > Target_Revenue_Rate:
                    GapAmt = GapMoney / pyupbit.get_current_price(BTC_Ticker)
                    balances = myUpbit.SellCoinMarket(upbit,BTC_Ticker,GapAmt)
                    line_alert.SendMessage("ReBalance !!! : " + BTC_Ticker + " by SELL:" )
        else:
            if GapMoney >=  MinimunCash and abs(GapRate) >= (BTC_Portion / 20.0):
                balances = myUpbit.BuyCoinMarket(upbit,BTC_Ticker,GapMoney)
                line_alert.SendMessage("ReBalance !!! : " + BTC_Ticker + " by BUY:" )
                print("--------------> BUY BITCOIN!!!!")
else:
    if BTC_Portion > 0:
        BtcMoney = TotalRealMoney * BTC_Portion
        if BtcMoney < MinimunCash:
            BtcMoney = MinimunCash
        balances = myUpbit.BuyCoinMarket(upbit,BTC_Ticker,BtcMoney)
        print("--------------> BUY BITCOIN!!!!")
if myUpbit.IsHasCoin(balances,ETH_Ticker) == True:
    NowCoinTotalMoney = myUpbit.GetCoinNowRealMoney(balances,ETH_Ticker)
    Rate = NowCoinTotalMoney / TotalRealMoney
    print("--------------> ETH rate : ", Rate)
    if Rate != ETH_Portion:
        GapRate = ETH_Portion - Rate
        print("--------------> ETH Gaprate : ", GapRate)
        GapMoney = TotalRealMoney * abs(GapRate)
        if GapRate < 0:
            if GapMoney >=  MinimunCash * 1.2 and abs(GapRate) >= (ETH_Portion / 20.0):
                revenue_rate = myUpbit.GetRevenueRate(balances,ETH_Ticker)
                if revenue_rate > Target_Revenue_Rate:
                    GapAmt = GapMoney / pyupbit.get_current_price(ETH_Ticker)
                    balances = myUpbit.SellCoinMarket(upbit,ETH_Ticker,GapAmt)
                    line_alert.SendMessage("ReBalance !!! : " + ETH_Ticker + " by SELL:" )
                    print("--------------> SELL Eherium!!!!")
        else:
            if GapMoney >=  MinimunCash and abs(GapRate) >= (ETH_Portion / 20.0):
                balances = myUpbit.BuyCoinMarket(upbit,ETH_Ticker,GapMoney)
                line_alert.SendMessage("ReBalance !!! : " + ETH_Ticker + " by BUY:" )
                print("--------------> BUY Eherium!!!!")
else:
    if ETH_Portion > 0:
        EthMoney = TotalRealMoney * ETH_Portion
        if EthMoney < MinimunCash:
            EthMoney = MinimunCash
        balances = myUpbit.BuyCoinMarket(upbit,ETH_Ticker,EthMoney)
        print("--------------> BUY Eherium!!!!")
print("----------------BUY LOGIC------------------------")
for ticker in BestCoinList:
    try: 
        if myUpbit.IsHasCoin(balances,ticker) == True:
            print("")
            MustAdjust = False
            if myUpbit.CheckCoinInList(AltAtypeList,ticker) == True or myUpbit.CheckCoinInList(AltBtypeList,ticker) == True:
                myUpbit.CancelCoinOrder(upbit,ticker)
                MustAdjust = True
            if myUpbit.CheckCoinInList(AltAtypeList,ticker) == True:
                AltAtypeList.remove(ticker)
                with open(atype_file_path, 'w') as outfile:
                    json.dump(AltAtypeList, outfile)
            if myUpbit.CheckCoinInList(AltBtypeList,ticker) == True:
                AltBtypeList.remove(ticker)
                with open(btype_file_path, 'w') as outfile:
                    json.dump(AltBtypeList, outfile)
            NowCoinTotalMoney = myUpbit.GetCoinNowRealMoney(balances,ticker)
            Rate = NowCoinTotalMoney / TotalRealMoney
            print("---BEST-------> ",ticker, " rate : ",  Rate)
            if Rate != Each_BestCoin_Portion:
                GapRate = Each_BestCoin_Portion - Rate
                print("---BEST-------> ",ticker," Gaprate : ", GapRate)
                GapMoney = TotalRealMoney * abs(GapRate)
                if GapRate < 0:
                    if GapMoney >=  MinimunCash * 1.2 and abs(GapRate) >= (Each_BestCoin_Portion / 20.0):
                        revenue_rate = myUpbit.GetRevenueRate(balances,ticker)
                        if revenue_rate > Target_Revenue_Rate or MustAdjust == True:
                            GapAmt = GapMoney / pyupbit.get_current_price(ticker)
                            balances = myUpbit.SellCoinMarket(upbit,ticker,GapAmt)
                            print("----BEST------> SELL ",ticker,"!!!!")
                            line_alert.SendMessage("ReBalance !!! : " + ticker + " by SELL:" )
                else:
                    if GapMoney >=  MinimunCash and abs(GapRate) >= (Each_BestCoin_Portion / 20.0):
                        balances = myUpbit.BuyCoinMarket(upbit,ticker,GapMoney)
                        print("-----BEST------> BUY ",ticker,"!!!!")
                        line_alert.SendMessage("ReBalance !!! : " + ticker + " by BUY:" )
        else:
            if Each_BestCoin_Portion > 0:
                AltMoney = TotalRealMoney * Each_BestCoin_Portion
                if AltMoney < MinimunCash:
                    AltMoney = MinimunCash
                balances = myUpbit.BuyCoinMarket(upbit,ticker,AltMoney)
                print("--------------> BUY ", ticker, "!!!!")
    except Exception as e:
        print("Exception:", e)
top_file_path = "./UpbitTopCoinList.json"
TopCoinList = list()
try:
    with open(top_file_path, "r") as json_file:
        TopCoinList = json.load(json_file)
except Exception as e:
    TopCoinList = myUpbit.GetTopCoinList("day",30)
    print("Exception:", e)
LovelyCoinList = ['KRW-MED','KRW-BORA','KRW-WAVES','KRW-VET','KRW-THETA','KRW-ALGO','KRW-TRX','KRW-NEAR','KRW-DOT','KRW-XRP','KRW-ADA','KRW-SOL','KRW-DOGE','KRW-MATIC','KRW-ATOM','KRW-LTC','KRW-LINK','KRW-BCH','KRW-XLM','KRW-MANA','KRW-SAND','KRW-AXS','KRW-XTZ','KRW-AVAX','KRW-AAVE','KRW-ETC','KRW-BAT']
revenue_file_path = "./RevenueDict.json"
revenueDic = dict() #딕셔너리다!!!
try:
    with open(revenue_file_path, "r") as json_file:
        revenueDic = json.load(json_file)
except Exception as e:
    print("Exception :", e)
maup_file_path = "./MaUpDict.json"
maupList = list() #
try:
    with open(maup_file_path, "r") as json_file:
        maupList = json.load(json_file)
except Exception as e:
    print("Exception :", e)
for ticker in Tickers:
    try: 
        if hour == 0 and min < 4:
            if myUpbit.CheckCoinInList(maupList,ticker) == True:
                if myUpbit.IsHasCoin(balances,ticker) == False:
                    maupList.remove(ticker)
                    with open(maup_file_path, 'w') as outfile:
                        json.dump(maupList, outfile)
            if myUpbit.CheckCoinInList(DolPaCoinList,ticker) == True:
                if myUpbit.IsHasCoin(balances,ticker) == False:
                    DolPaCoinList.remove(ticker)
                    with open(dolpha_type_file_path, 'w') as outfile:
                        json.dump(DolPaCoinList, outfile)
                else:
                    if myUpbit.CheckCoinInList(LovelyCoinList,ticker) == False:
                        revenue_rate = myUpbit.GetRevenueRate(balances,ticker)
                        if revenue_rate < Target_Revenue_Rate:
                            myUpbit.CancelCoinOrder(upbit,ticker)
                            balances = myUpbit.SellCoinMarket(upbit,ticker,upbit.get_balance(ticker))
                            DolPaCoinList.remove(ticker)
                            with open(dolpha_type_file_path, 'w') as outfile:
                                json.dump(DolPaCoinList, outfile)
                            line_alert.SendMessage("DOLPA End CUT!!! : " + ticker + " Revenue:" + str(revenue_rate) )
    except Exception as e:
        print("---:", e)
print("----------------BUY LOGIC------------------------")
for ticker in TopCoinList:
    try: 
        print("---->" , ticker)
        if myUpbit.CheckCoinInList(DolPaCoinList,ticker) == True:   
            continue
        if myUpbit.CheckCoinInList(BestCoinList,ticker) == True:
            continue
        if myUpbit.IsHasCoin(balances,ticker) == True:
            continue
        if myUpbit.CheckCoinInList(LovelyCoinList,ticker) == True:
            print("---------> Target Coin ---> ", ticker)
            time.sleep(0.05)
            df = pyupbit.get_ohlcv(ticker,interval="day")
            ma5_before3 = myUpbit.GetMA(df,5,-3)
            ma5_before = myUpbit.GetMA(df,5,-2)
            ma5_now = myUpbit.GetMA(df,5,-1)
            now_price = pyupbit.get_current_price(ticker)
            IsUpTrend = False
            if ma5_before3 < ma5_before < ma5_now < now_price:
                IsUpTrend = True
            time.sleep(0.05)
            df_5 = pyupbit.get_ohlcv(ticker,interval="minute5")
            rsi_before4 = myUpbit.GetRSI(df_5,14,-4)
            rsi_before3 = myUpbit.GetRSI(df_5,14,-3)
            rsi_before = myUpbit.GetRSI(df_5,14,-2)
            print ("rsi14 --> ",rsi_before4,rsi_before3,rsi_before)
            ma5_before2 = myUpbit.GetMA(df_5,5,-3)
            ma5_before = myUpbit.GetMA(df_5,5,-2)
            ma5_now = myUpbit.GetMA(df_5,5,-1)
            print ("ma5 --> ",ma5_before2,ma5_before,ma5_now)
            ma10_before2 = myUpbit.GetMA(df_5,10,-3)
            ma10_before = myUpbit.GetMA(df_5,10,-2)
            ma10_now = myUpbit.GetMA(df_5,10,-1)
            print ("ma10 --> ",ma10_before2,ma10_before,ma10_now)
            ma20_before2 = myUpbit.GetMA(df_5,20,-3)
            ma20_before = myUpbit.GetMA(df_5,20,-2)
            ma20_now = myUpbit.GetMA(df_5,20,-1)
            print ("ma20 --> ",ma20_before2,ma20_before,ma20_now)
            ma60_before2 = myUpbit.GetMA(df_5,60,-3)
            ma60_before = myUpbit.GetMA(df_5,60,-2)
            ma60_now = myUpbit.GetMA(df_5,60,-1)
            print ("ma60 --> ",ma60_before2,ma60_before,ma60_now)
            if (rsi_before4 > rsi_before3 and rsi_before3 < rsi_before and rsi_before3 <= 30.0) or (rsi_before < 70.0 and myUpbit.CheckCoinInList(maupList,ticker) == False and ma5_before2 < ma5_before and ma10_before2 < ma10_before and ma20_before2 < ma20_before and ma60_before2 < ma60_before and ma60_now < ma20_now < ma10_now < ma5_now < now_price):
                print("IN Target!!!")
                bAlreadyBTypeBuyDone = False
                if len(AltBtypeList) < ALT_Btype_MaxCnt:
                    balances = myUpbit.BuyCoinMarket(upbit,ticker,ALT_Btype_FirstEnterMoney)
                    if (ma5_before2 < ma5_before and ma10_before2 < ma10_before and ma20_before2 < ma20_before and ma60_before2 < ma60_before and ma60_now < ma20_now < ma10_now < ma5_now < now_price):
                        maupList.append(ticker)
                        with open(maup_file_path, 'w') as outfile:
                            json.dump(maupList, outfile)
                    revenueDic[ticker] = 0
                    with open(revenue_file_path, 'w') as outfile:
                        json.dump(revenueDic, outfile)
                    bAlreadyBTypeBuyDone = True
                    AltBtypeList.append(ticker)
                    with open(btype_file_path, 'w') as outfile:
                        json.dump(AltBtypeList, outfile)
                    avgPrice = myUpbit.GetAvgBuyPrice(balances,ticker)
                    coin_volume = upbit.get_balance(ticker)
                    target_price =  avgPrice * (1.0 + (Target_Revenue_Rate/100.0))
                    myUpbit.SellCoinLimit(upbit,ticker,target_price,coin_volume * 0.5)
                    total_water_money = ALT_Btype_TotalWaterMoney
                    water_money = ALT_Btype_Greed_Money
                    for i in range(1,int(ALT_Btype_Maximun_Greed_Cnt)+1):
                        water_price = avgPrice * (1.0 - ((ALT_Btype_Greed_Gap/100.0) * i))
                        print("----> water_price",water_price)
                        water_volume = water_money / water_price
                        myUpbit.BuyCoinLimit(upbit,ticker,water_price,water_volume)
                        time.sleep(0.2)
                        total_water_money -= water_money
                        if total_water_money < MinimunCash:
                            break
                        if i % 3 == 0:
                            water_money *= 2
                        if total_water_money < water_money:
                            water_money = total_water_money
                    line_alert.SendMessage("DANTA B START : " + ticker)
                if IsUpTrend == True and bAlreadyBTypeBuyDone == False:
                    if len(AltAtypeList) < ALT_Atype_MaxCnt:
                        balances = myUpbit.BuyCoinMarket(upbit,ticker,ALT_Atype_FirstEnterMoney)
                        if (ma5_before2 < ma5_before and ma10_before2 < ma10_before and ma20_before2 < ma20_before and ma60_before2 < ma60_before and ma60_now < ma20_now < ma10_now < ma5_now < now_price):
                            maupList.append(ticker)
                            with open(maup_file_path, 'w') as outfile:
                                json.dump(maupList, outfile)
                        revenueDic[ticker] = 0
                        with open(revenue_file_path, 'w') as outfile:
                            json.dump(revenueDic, outfile)
                        AltAtypeList.append(ticker)
                        with open(atype_file_path, 'w') as outfile:
                            json.dump(AltAtypeList, outfile)
                        avgPrice = myUpbit.GetAvgBuyPrice(balances,ticker)
                        coin_volume = upbit.get_balance(ticker)
                        target_price =  avgPrice * (1.0 + (Target_Revenue_Rate/100.0))
                        myUpbit.SellCoinLimit(upbit,ticker,target_price,coin_volume * 0.5)
                        total_water_money = ALT_Atype_TotalWaterMoney
                        water_money = ALT_Atype_Greed_Money
                        for i in range(1,int(ALT_Atype_Maximun_Greed_Cnt)+1):
                            water_price = avgPrice * (1.0 - ((ALT_Atype_Greed_Gap/100.0) * i))
                            print("----> water_price",water_price)
                            water_volume = water_money / water_price 
                            myUpbit.BuyCoinLimit(upbit,ticker,water_price,water_volume)
                            time.sleep(0.2)
                            total_water_money -= water_money
                            if total_water_money < MinimunCash:
                                break
                            if i % 3 == 0:
                                water_money *= 2
                            if total_water_money < water_money:
                                water_money = total_water_money
                        line_alert.SendMessage("DANTA A START : " + ticker)
    except Exception as e:
        print("---:", e)
print("--------------------------------------------------")
print("--------------------------------------------------")
tralling_stop_rate = 0.3
print("----------------SELL LOGIC------------------------")
for ticker in Tickers:
    try: 
        print("---->" , ticker)
        if myUpbit.CheckCoinInList(BestCoinList,ticker) == True:
            continue
        if myUpbit.CheckCoinInList(DolPaCoinList,ticker) == True:   
            continue
        if myUpbit.IsHasCoin(balances,ticker) == True and ticker != BTC_Ticker and ticker != ETH_Ticker:
            revenue_rate = myUpbit.GetRevenueRate(balances,ticker)
            print("---------> Has coin : ", ticker, " revenue_rate --> ", revenue_rate)
            if revenueDic[ticker] >= Target_Revenue_Rate:
                if revenueDic[ticker] - tralling_stop_rate > revenue_rate:
                    myUpbit.CancelCoinOrder(upbit,ticker)
                    balances = myUpbit.SellCoinMarket(upbit,ticker,upbit.get_balance(ticker))
                    if myUpbit.CheckCoinInList(AltAtypeList,ticker) == True:
                        AltAtypeList.remove(ticker)
                        with open(atype_file_path, 'w') as outfile:
                            json.dump(AltAtypeList, outfile)
                        line_alert.SendMessage("DANTA A END : " + ticker)
                    if myUpbit.CheckCoinInList(AltBtypeList,ticker) == True:
                        AltBtypeList.remove(ticker)
                        with open(btype_file_path, 'w') as outfile:
                            json.dump(AltBtypeList, outfile)
                        line_alert.SendMessage("DANTA B END : " + ticker)
            avgPrice = myUpbit.GetAvgBuyPrice(balances,ticker)
            target_price =  avgPrice * (1.0 + (Target_Revenue_Rate/100.0)) 
            orders_data = upbit.get_order(ticker)
            for order in orders_data:
                if order['side'] == 'ask' :
                    if float(order['price']) != float(pyupbit.get_tick_size(target_price)):
                        upbit.cancel_order(order['uuid'])
                        time.sleep(0.2)
                        coin_volume = upbit.get_balance(ticker)
                        myUpbit.SellCoinLimit(upbit,ticker,target_price,coin_volume * 0.5)
            if revenueDic[ticker] < revenue_rate:
                revenueDic[ticker] = revenue_rate 
                with open(revenue_file_path, 'w') as outfile:
                    json.dump(revenueDic, outfile)
    except Exception as e:
        print("---:", e)
print("--------------------------------------------------")
print("--------------------------------------------------")
print("----------------DOLPHA LOGIC------------------------")
dolpha_tralling_stop_rate = 0.5
for ticker in Tickers:
    try: 
        print("---->" , ticker)
        if myUpbit.CheckCoinInList(BestCoinList,ticker) == True or ticker == BTC_Ticker or ticker == ETH_Ticker:
            continue
        if myUpbit.CheckCoinInList(AltAtypeList,ticker) == True or myUpbit.CheckCoinInList(AltBtypeList,ticker) == True:
            continue
        if myUpbit.IsHasCoin(balances,ticker) == True and myUpbit.CheckCoinInList(DolPaCoinList,ticker) == True:
            print("DOLPHA sell")
            revenue_rate = myUpbit.GetRevenueRate(balances,ticker)
            print("---------> Has coin : ", ticker, " revenue_rate --> ", revenue_rate)
            if revenueDic[ticker] >= Target_Revenue_Rate:
                if revenueDic[ticker] - dolpha_tralling_stop_rate > revenue_rate:
                    myUpbit.CancelCoinOrder(upbit,ticker)
                    balances = myUpbit.SellCoinMarket(upbit,ticker,upbit.get_balance(ticker))
                    line_alert.SendMessage("DOLPA End!!! : " + ticker + " Revenue:" + str(revenue_rate) )
            if revenueDic[ticker] < revenue_rate:
                revenueDic[ticker] = revenue_rate 
                with open(revenue_file_path, 'w') as outfile:
                    json.dump(revenueDic, outfile)
        else:
            if myUpbit.CheckCoinInList(TopCoinList,ticker) == True: 
                print("DOLPHA buy")
                print("!!!!! Target Coin!!! :",ticker)
                time.sleep(0.05)
                df = pyupbit.get_ohlcv(ticker,interval="day")
                rsi_before = myUpbit.GetRSI(df,14,-2)
                ma5_now = myUpbit.GetMA(df,5,-1)
                Range = (float(df['high'][-2]) - float(df['low'][-2])) * 0.5
                target_price = float(df['close'][-2]) + Range
                now_price = float(df['close'][-1])
                print(now_price , " > ", target_price)
                if now_price >=  target_price and len(DolPaCoinList) < MaxDolPaCoinCnt and myUpbit.CheckCoinInList(DolPaCoinList,ticker) == False and rsi_before < 50 and ma5_now <= now_price:
                    print("!!!!!!!!!!!!!!!First Buy GoGoGo!!!!!!!!!!!!!!!!!!!!!!!!")
                    if Each_DolPa_Portion > 0:
                        DolPaMoney = TotalRealMoney * Each_DolPa_Portion
                        if DolPaMoney < MinimunCash:
                            DolPaMoney = MinimunCash
                        balances = myUpbit.BuyCoinMarket(upbit,ticker,DolPaMoney)
                        revenueDic[ticker] = 0
                        with open(revenue_file_path, 'w') as outfile:
                            json.dump(revenueDic, outfile)
                        DolPaCoinList.append(ticker)
                        with open(dolpha_type_file_path, 'w') as outfile:
                            json.dump(DolPaCoinList, outfile)
                        avgPrice = myUpbit.GetAvgBuyPrice(balances,ticker)
                        coin_volume = upbit.get_balance(ticker)
                        minimun_target_price =  avgPrice * (1.0 + (Target_Revenue_Rate/100.0))
                        minimun2_target_price =  avgPrice * (1.0 + (Target_Revenue_Rate * 2.0/100.0))
                        First_target_price = avgPrice + Range * 0.5
                        if First_target_price < minimun_target_price:
                            First_target_price = minimun_target_price
                        Second_target_price = avgPrice + Range
                        if Second_target_price < minimun2_target_price:
                            Second_target_price = minimun2_target_price
                        myUpbit.SellCoinLimit(upbit,ticker,First_target_price,coin_volume * 0.25)
                        myUpbit.SellCoinLimit(upbit,ticker,Second_target_price,coin_volume * 0.25)
                        line_alert.SendMessage("DOLPA START : " + ticker)
    except Exception as e:
        print("---:", e)