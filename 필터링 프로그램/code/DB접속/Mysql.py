import pandas
import pymysql
from datetime import datetime


print('START TIME : ',str(datetime.now())[10:19] )

db = pymysql.connect(host='localhost', port=3306, user='KDHJ', passwd='0217', db='STOCK_DB', charset='utf8')


sql="select * from index_test"

result = pandas.read_sql_query(sql,conn)
result.to_csv(r'pandas_output.csv',index=False)

print('END TIME : ',str(datetime.now())[10:19] )

conn.close()