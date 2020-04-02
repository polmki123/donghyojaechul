import pandas as pd 
import pymysql
import itertools
from datetime import datetime


print('START TIME : ',str(datetime.now())[10:19] )

conn = pymysql.connect(host='localhost', port=3306, user='KDHJ', passwd='0217', db='STOCK_DB', charset='utf8')

#  [Symbol, date, 매출액, 배당, 상장주식수, 영업이익, 영업활동으로인한현금흐름, 이익잉여금, 자본금, 종가, 주가, 지배주주순이익, 총부채, 총자본, 투자활동으로인한현금흐름]


# 포괄손익계산서
# 매출액 단위(천원)
temp["매출액 100억 이상"] = temp["매출액"] > 매출액

sql= ("select Symbol from ystock" +
      "where date = %s" %(오늘) +
        "and %s >= 매출액" %(매출액))
result = pd.read_sql_query(sql,conn)

#영업이익 3개년 모두 0 이상
temp["영업이익 3년동안 0 이상"] = (temp["영업이익"] > 영업이익) & (temp["영업이익 1Y lag"] > 영업이익_1Y_lag) & (temp["영업이익 2Y lag"] > 영업이익_2Y_lag)

sql= ("Select Symbol" +
      "from ( 	select Symbol,  count(* ) as 만족년도" +
       "from ystock " +
        "where date between %s and  %s " % (오늘, n년전) +
          "and 영업이익 >= %s" % (영업이익량) +
          "group by Symbol" +
            ") A" + 
      "where 만족년도 >= %s " % (n) )
result = pd.read_sql_query(sql,conn)


# 영업이익률 증가
temp["영업이익률 3년동안 증가"] = (temp["영업이익률"] > temp["영업이익률 1Y lag"]) &  (temp["영업이익률"] > temp["영업이익률 2Y lag"]) &  (temp["영업이익률 1Y lag"] > temp["영업이익률 2Y lag"])

sql= ("Select Symbol" +
      "from ( 	select Symbol,  count(* ) as 만족년도" +
       "from dstock " +
        "where date between %s and  %s " % (오늘, n년전) +
          "and 영업이익 >= %s" % (영업이익량) +
          "group by Symbol" +
            ") A" + 
      "where 만족년도 >= %s " % (n) )
result = pd.read_sql_query(sql,conn)

# 매출액 3년 동안 증가
temp["매출액 3년동안 증가"] = (temp["매출액"] > temp["매출액 1Y lag"]) &  (temp["매출액"] > temp["매출액 2Y lag"]) &  (temp["매출액 1Y lag"] > temp["매출액 2Y lag"])

temp["자본잠식 없음"] = temp["총자본"] > 총자본

# 부채비율
temp["부채비율"] = temp["총부채"] / temp["총자본"]
temp["부채비율 150% 이하"] = temp["부채비율"] < 부채비율

# 자본금
temp["자본금 증가율"] = (temp["자본금"] - temp["자본금 1Y lag"]) / temp["자본금 1Y lag"]
temp["자본금 변동없음"] = temp["자본금 증가율"].abs() < 자본금증가율

# 이익잉여금

temp["이익잉여금이 3년동안 증가"] = (temp["이익잉여금"] > temp["이익잉여금 1Y lag"]) &  (temp["이익잉여금"] > temp["이익잉여금 2Y lag"]) &  (temp["이익잉여금 1Y lag"] > temp["이익잉여금 2Y lag"])


## 현금흐름표

# 영업활동현금흐름
temp["영업활동으로인한현금흐름 판별"] = temp["영업활동으로인한현금흐름"] > 영업활동으로인한현금흐름
temp["3년 중 2년 이상 영업활동으로인한현금흐름 0 초과"] = (temp["영업활동으로인한현금흐름 판별"].rolling(3).sum() > 2)

# 투자활동현금흐름
temp["투자활동으로인한현금흐름 판별"] = temp["투자활동으로인한현금흐름"] < 투자활동으로인한현금흐름
temp["3년 중 2년 이상 투자활동으로인한현금흐름 0 미만"] = (temp["투자활동으로인한현금흐름 판별"].rolling(3).sum() > 2)

## 배당
temp["배당존재"] = temp["배당"] > 배당 
temp["배당이 3년동안 증가"] =(temp["배당"] > temp["배당 1Y lag"]) &  (temp["배당"] > temp["배당 2Y lag"]) &  (temp["배당 1Y lag"] > temp["배당 2Y lag"])

## 기타
# ROE가 5% 이상(수익성)
temp["ROE"] = temp["지배주주순이익"] / temp["총자본"]
temp["ROE 5퍼 이상"]  = temp["ROE"] > ROE