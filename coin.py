from binance.client import Client
import datetime
import collections
from binance.enums import *
from binance.exceptions import *


api_key = ""
api_secret = ""
client = Client(api_key, api_secret)

#取得配列の内訳
#[OpenTime,Open,High,Low,Close,Volume,CloseTime,QuoteAssetVolume,NumberOfTrades,TakerBuyBaseAssetVolume,TakerBuyQuoteAssetVolume,Ignore]

def date_cul(servertime): #サーバータイムを日付に変換する
    time = float(servertime) / 1000
    dt = datetime.datetime.fromtimestamp(time)
    return dt

def time_cul(date): #日付をサーバータイムに変換する
    time = date.timestamp() * 1000
    return time

def maxmin_all():
    max,min = maxmin_month()
    j = 0
    hourA = []
    hourB = []
    hourX = []
    hourN = []
    #print(max)
    for i in max:
        #最大最小値の毎時だけ取得
        hourA.append(min[j][0].hour)
        hourB.append(max[j][0].hour)
        j = j + 1
    day = max[j-1][0] - max[0][0] + datetime.timedelta(days=2)  #何日間統計したか
    print("統計日数：",day.days,"日")
    hourN = collections.Counter(hourA).most_common()
    hourX = collections.Counter(hourB).most_common()
    print("最多最安時間：",hourN[0][0],"時(",hourN[0][1],"回)")
    print("最多最高時間：", hourX[0][0], "時(", hourX[0][1], "回)")
    #print("HOUR:", hourA)

def maxmin_month():
    #klines = client.get_historical_klines("XEMUSDT", Client.KLINE_INTERVAL_1HOUR, "31 Jan, 2021", "1 Mar, 2021")
    klines = client.get_historical_klines("XEMUSDT", KLINE_INTERVAL_1HOUR, "28 Feb, 2020")
    # 配列変数初期化
    j = 0
    dt1 = datetime.datetime(2020, 12, 1, 0, 0, 0, 0)
    dt2 = datetime.datetime(2021, 3, 1, 0, 0, 0, 0)
    su1 = int(time_cul(dt1))
    su2 = int(time_cul(dt2))
    allmax = []
    allmin = []
    for i in klines:
        openP = []
        openT = []
        if len(klines)> j: kl = int(klines[j][0])
        if (kl >= su1 and kl < su2):
            for k in range(24):
                # 取得ごとの最大最小価格を取得
                if len(klines) > j:
                    openP.append(klines[j][1])
                    openT.append(klines[j][0])
                j = j + 1
            # 配列内の最大最小値を取得
            maxC = []
            minC = []
            maxA = max(openP)
            minA = min(openP)
            # 配列内の最大最小値の位置を取得
            maxS = openP.index(maxA)
            minS = openP.index(minA)

            maxTime = date_cul(openT[maxS])
            minTime = date_cul(openT[minS])

            maxC.append(maxTime)
            maxC.append(maxA)
            minC.append(minTime)
            minC.append(minA)

            allmax.append(maxC)
            allmin.append(minC)

            print("MAXTIME：",maxTime , "Price:", maxA, "MINTIME：",minTime ,"Price:", minA)
        else:
            j = j + 1
    return allmax,allmin





def max_min():
    #ローソク足取得
    klines = client.get_historical_klines("XEMUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")


    #現在のサーバータイムを取得
    time_res = client.get_server_time()
    print(date_cul(float(time_res["serverTime"])))

    #配列変数初期化
    maxP = []
    openT = []
    minP = []
    j = 0

    for i in klines:
        # 取得ごとの最大最小価格を取得
        maxP.append(klines[j][2])
        minP.append(klines[j][3])
        openT.append(klines[j][0])
        j = j + 1

    #配列内の最大最小値を取得
    maxA = max(maxP)
    minA = min(minP)
    #配列内の最大最小値の位置を取得
    maxS = maxP.index(maxA)
    minS = minP.index(minA)

    print("MAXTIME：",date_cul(klines[maxS][0]),"Price:",maxA)
    print("MINTIME：",date_cul(klines[minS][0]),"Price:",minA)


if __name__ == '__main__':
    maxmin_all()
