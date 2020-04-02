import pandas as pd 
import pymysql
import itertools
from datetime import datetime


print('START TIME : ',str(datetime.now())[10:19] )

conn = pymysql.connect(host='localhost', port=3306, user='KDHJ', passwd='0217', db='STOCK_DB', charset='utf8')

#  [Symbol, date, 거래량, 고가, 저가, 종가, 주가, 주식수]


# 소형주 필터
final["시총 500억 이하"] = final["시가총액"] < 50000000000
final["시총 1000억 이하"] = final["시가총액"] < 100000000000
final["시총 1500억 이하"] = final["시가총액"] < 150000000000

sql= ("select Symbol from dstock" +
      "where date = %s" %(오늘) +
      "and %s >= 종가 * 주식수" %(시가총액))
result = pd.read_sql_query(sql,conn)


# 대형주 필터
final["시총 1500억 이상"] = final["시가총액"] > 150000000000
final["시총 3000억 이상"] = final["시가총액"] > 300000000000
final["시총 5000억 이상"] = final["시가총액"] > 500000000000
final["시총 1조 이상"] = final["시가총액"] > 1000000000000
final["시총 2조 이상"] = final["시가총액"] > 2000000000000

sql= ("select Symbol from dstock" +
      "where date = %s" %(오늘) +
      "and %s <= 종가 * 주식수" %(시가총액))
result = pd.read_sql_query(sql,conn)

# 시가 120일 이내 비교 
final["10일 10% 이하 상승"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) < 0.1
final["10일 20% 이하 상승"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) < 0.2
final["10일 30% 이하 상승"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) < 0.3
final["10일 40% 이하 상승"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) < 0.4
final["10일 50% 이하 상승"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) < 0.5
final["10일 60% 이하 상승"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) < 0.6
final["10일 70% 이하 상승"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) < 0.7
final["10일 80% 이하 상승"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) < 0.8
final["10일 90% 이하 상승"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) < 0.9
final["10일 100% 이하 상승"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) < 1

sql= ("Select Symbol " +
      "from (" +
        "select Symbol, 주가 " +
        "from dstock" + 
        "where date = %s"  %(오늘)+
            ") A, "+
        "select Symbol, 주가"+
        "from dstock"+
        "where date = %s" %(n일전 )+
            ") B," +
      "where A.Symbol = B.Symbol"+
          "and A.주가 > B.주가"+
          "and A.주가 < B.주가 * %s  " %(1 + 상승률  ))
result = pd.read_sql_query(sql,conn)

# 하락체크
final["10일 10% 이하 하락"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) > -0.1
final["10일 20% 이하 하락"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) > -0.2
final["10일 30% 이하 하락"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) > -0.3
final["10일 40% 이하 하락"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) > -0.4
final["10일 50% 이하 하락"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) > -0.5
final["10일 60% 이하 하락"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) > -0.6
final["10일 70% 이하 하락"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) > -0.7
final["10일 80% 이하 하락"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) > -0.8
final["10일 90% 이하 하락"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) > -0.9
final["10일 100% 이하 하락"] = ((final["주가"] - final["주가 10days lag"]) / final["주가 10days lag"]) > -1

sql= ("Select Symbol " +
      "from (" +
        "select Symbol, 주가 " +
        "from dstock" + 
        "where date = %s"  %(오늘)+
            ") A, "+
        "select Symbol, 주가"+
        "from dstock"+
        "where date = %s" %(n일전 )+
            ") B," +
      "where A.Symbol = B.Symbol"+
          "and A.주가 < B.주가"+
          "and A.주가 < B.주가 * %s  " %(1 - 하락율 ))
result = pd.read_sql_query(sql,conn)

# 대금 이하
final["10일 평균거래량 10억 이하"] = final["거래량 10days rolling mean"] < 1000000000
final["20일 평균거래량 10억 이하"] = final["거래량 20days rolling mean"] < 1000000000
final["30일 평균거래량 10억 이하"] = final["거래량 30days rolling mean"] < 1000000000
final["40일 평균거래량 10억 이하"] = final["거래량 40days rolling mean"] < 1000000000
final["50일 평균거래량 10억 이하"] = final["거래량 50days rolling mean"] < 1000000000
final["60일 평균거래량 10억 이하"] = final["거래량 60days rolling mean"] < 1000000000
final["70일 평균거래량 10억 이하"] = final["거래량 70days rolling mean"] < 1000000000
final["80일 평균거래량 10억 이하"] = final["거래량 80days rolling mean"] < 1000000000
final["90일 평균거래량 10억 이하"] = final["거래량 90days rolling mean"] < 1000000000
final["100일 평균거래량 10억 이하"] = final["거래량 100days rolling mean"] < 1000000000

sql= ("Select Symbol" +
      "from ( 	select Symbol,  AVG(거래량 ) as 평균거래량" +
       "from dstock " +
        "where date between %s and  %s " % (오늘, n일전) +
        "group by Symbol" +
            ") A" + 
      "where 평균거래량 <= %s " % (평균거래량) )
result = pd.read_sql_query(sql,conn)


# 대금 이상
final["10일 평균거래량 100억 이상"] = final["거래량 10days rolling mean"] > 10000000000
final["20일 평균거래량 100억 이상"] = final["거래량 20days rolling mean"] > 10000000000
final["30일 평균거래량 100억 이상"] = final["거래량 30days rolling mean"] > 10000000000
final["40일 평균거래량 100억 이상"] = final["거래량 40days rolling mean"] > 10000000000
final["50일 평균거래량 100억 이상"] = final["거래량 50days rolling mean"] > 10000000000
final["60일 평균거래량 100억 이상"] = final["거래량 60days rolling mean"] > 10000000000
final["70일 평균거래량 100억 이상"] = final["거래량 70days rolling mean"] > 10000000000
final["80일 평균거래량 100억 이상"] = final["거래량 80days rolling mean"] > 10000000000
final["90일 평균거래량 100억 이상"] = final["거래량 90days rolling mean"] > 10000000000
final["100일 평균거래량 100억 이상"] = final["거래량 100days rolling mean"] > 10000000000

sql= ("Select Symbol" +
      "from ( 	select Symbol,  AVG(거래량 ) as 평균거래량" +
       "from dstock " +
        "where date between %s and  %s " % (오늘, n일전) +
        "group by Symbol" +
            ") A" + 
      "where 평균거래량 >= %s " % (평균거래량) )
result = pd.read_sql_query(sql,conn)

# 고가 판정
#고가영역필터
final["10일 고가 5% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 0.05
final["10일 고가 10% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 0.1
final["10일 고가 15% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 0.15
final["10일 고가 20% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 0.2
final["10일 고가 30% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 0.3
final["10일 고가 40% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 0.4
final["10일 고가 50% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 0.5
final["10일 고가 60% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 0.6
final["10일 고가 70% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 0.7
final["10일 고가 80% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 0.8
final["10일 고가 90% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 0.9
final["10일 고가 100% 이상"] = (final["고가 10days rolling max"] - final["주가"]) / final["주가"] > 1

sql= ("Select Symbol" +
      "from ( 	select Symbol,  MAX(고가 ) as 최고가" +
       "from dstock " +
        "where date between %s and  %s " % (오늘, n일전) +
        "group by Symbol" +
            ") A" + 
            "( 	select Symbol,  주가" +
       "from dstock " +
        "where date = %s " % (오늘) +
            ") B" +
      "where A.Symbol = B.Symbol" +
      "and A.최고가 >= B.주가 * %s " % (1 + 상승률) )
result = pd.read_sql_query(sql,conn)


# 5% 임의로 정함 -- 추후 개량
final["10일 최저가 영역"] = (final["주가"] - final["저가 10days rolling min"])/ final["주가"] < 0.05
final["20일 최저가 영역"] = (final["주가"] - final["저가 20days rolling min"])/ final["주가"] < 0.05
final["30일 최저가 영역"] = (final["주가"] - final["저가 30days rolling min"])/ final["주가"] < 0.05
final["40일 최저가 영역"] = (final["주가"] - final["저가 40days rolling min"])/ final["주가"] < 0.05
final["50일 최저가 영역"] = (final["주가"] - final["저가 50days rolling min"])/ final["주가"] < 0.05
final["60일 최저가 영역"] = (final["주가"] - final["저가 60days rolling min"])/ final["주가"] < 0.05
final["70일 최저가 영역"] = (final["주가"] - final["저가 70days rolling min"])/ final["주가"] < 0.05
final["80일 최저가 영역"] = (final["주가"] - final["저가 80days rolling min"])/ final["주가"] < 0.05
final["90일 최저가 영역"] = (final["주가"] - final["저가 90days rolling min"])/ final["주가"] < 0.05
final["100일 최저가 영역"] = (final["주가"] - final["저가 100days rolling min"])/ final["주가"] < 0.05

sql= ("Select Symbol" +
      "from ( 	select Symbol,  MIN(저가 ) as 최저가" +
       "from dstock " +
        "where date between %s and  %s " % (오늘, n일전) +
        "group by Symbol" +
            ") A" + 
            "( 	select Symbol,  주가" +
       "from dstock " +
        "where date = %s " % (오늘) +
            ") B" +
      "where A.Symbol = B.Symbol" +
      "and A.최저가 <= B.주가 * %s " % (1 - 하락률) )
result = pd.read_sql_query(sql,conn)