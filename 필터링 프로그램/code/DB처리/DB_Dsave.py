import pandas as pd
from sqlalchemy import create_engine
import pymysql
# MySQL Connector using pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

engine = create_engine("mysql+mysqldb://KDHJ:"+"0217"+"@localhost/STOCK_DB", encoding='utf-8')
conn = engine.connect()

df = pd.read_csv("data/일별 주식.csv", encoding = "ms949")

계정명 = df["Item Name "].drop_duplicates().tolist()

바꿀계정명 = ["주가", "고가", "저가", "거래량", "종가", "주식수"]

temp = {}

for 계정 in range(len(계정명)):
    temp[계정명[계정]] = 바꿀계정명[계정]
    print(계정명[계정]+ "     ->     " +  바꿀계정명[계정])

df = df.replace({"Item Name ": temp})

df = df.set_index(['Symbol', "Item Name "])
시간변환 = pd.to_datetime(df.columns)

시간변환 = 시간변환.strftime("%Y-%m-%d")
시간변환 = 시간변환.rename("date")
df.columns = pd.to_datetime(시간변환)
df = df.stack().swaplevel().unstack()


for 계정 in df.columns:
    df[계정] = df[계정].str.replace(',', "")

df = df.astype(float)


df.to_sql(name='dstock', con=engine, if_exists='append')