import pandas as pd 
import pymysql
import itertools
from datetime import datetime


print('START TIME : ',str(datetime.now())[10:19] )

conn = pymysql.connect(host='localhost', port=3306, user='KDHJ', passwd='0217', db='STOCK_DB', charset='utf8')

#  [symbol, date, 매출액, 배당, 상장주식수, 영업이익, 영업활동으로인한현금흐름, 이익잉여금, 자본금, 종가, 주가, 지배주주순이익, 총부채, 총자본, 투자활동으로인한현금흐름]