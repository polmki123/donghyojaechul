#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# # 데이터를 불러온다

# In[2]:


df = pd.read_csv("..\\..\\data\\donghyojaechul_daily_stock_2years.csv", encoding = "ms949")


# # 데이터의 계정이름을 사용하기 쉬운 계정이름으로 변환

# In[3]:


계정명 = df["Item Name "].drop_duplicates().tolist()


# In[4]:


계정명


# In[5]:


바꿀계정명 = ["주가", "고가", "저가", "거래량"]


# In[6]:


temp = {}

for 계정 in range(len(계정명)):
    temp[계정명[계정]] = 바꿀계정명[계정]
    print(계정명[계정]+ "     ->     " +  바꿀계정명[계정])


# ### 바뀐 계정 할당

# In[7]:


df = df.replace({"Item Name ": temp})


# ### df타입을 실수로 변환

# In[8]:


### 컬럼의 2014-12-31 string 포맷을 datetime 포맷으로 바꾼 후 데이터프레임을 회사명과 시간의 이중 인덱스로 바꿔줌


# In[9]:


df = df.set_index(['Symbol', "Item Name "])
시간변환 = pd.to_datetime(df.columns)

시간변환 = 시간변환.strftime("%Y-%m-%d")
시간변환 = 시간변환.rename("date")
df.columns = pd.to_datetime(시간변환)
df = df.stack().swaplevel().unstack()


# ### df type 실수로 변환

# In[10]:


for 계정 in df.columns:
    df[계정] = df[계정].str.replace(',', "")

df = df.astype(float)


# # 필터링 조건들을 생성한다

# In[11]:


company_list = df.index.levels[0]


# In[12]:


new_data = []
for company in company_list:
    temp = df.loc[company]
    
    # 급격한 상승 있었는지 필터
    temp["10거래일 10% 이하 상승"] = (temp["주가"] - temp["주가"].shift(10)) / temp["주가"].shift(10) < 0.1
    temp["40거래일 50% 이하 상승"] = (temp["주가"] - temp["주가"].shift(30)) / temp["주가"].shift(30) < 0.5
    temp["80거래일 100% 이하 상승"] = (temp["주가"] - temp["주가"].shift(80)) / temp["주가"].shift(80) < 1

    # 최저가 영역 필터

    temp["30거래일 최저가 영역"] = (temp["주가"]  - temp["주가"].rolling(30).min()) / temp["주가"] < 0.05
    temp["60거래일 최저가 영역"] = (temp["주가"]  - temp["주가"].rolling(60).min()) / temp["주가"] < 0.05
    temp["90거래일 최저가 영역"] = (temp["주가"]  - temp["주가"].rolling(90).min()) / temp["주가"] < 0.1

    # 거래량 필터
    temp["20일 평균거래량 10억 이하"] = temp["거래량"].rolling(20).mean() < 1000000000
    temp["20일 평균거래량 20억 이하"] = temp["거래량"].rolling(20).mean() < 2000000000

    temp["60일 평균거래량 10억 이하"] = temp["거래량"].rolling(60).mean() < 1000000000
    temp["60일 평균거래량 20억 이하"] = temp["거래량"].rolling(60).mean() < 2000000000

    temp["100일 평균거래량 10억 이하"] = temp["거래량"].rolling(100).mean() < 1000000000
    temp["100일 평균거래량 20억 이하"] = temp["거래량"].rolling(100).mean() < 2000000000
    
    
    temp["Symbol"] = company
    temp = temp.reset_index()
    temp = temp.set_index(["Symbol", "date"])
    
    new_data.append(temp)  


# In[13]:


old = pd.DataFrame()
for company_data in new_data:
    old = pd.concat([old, company_data])


# In[14]:


필터조건 = ["10거래일 10% 이하 상승","40거래일 50% 이하 상승","80거래일 100% 이하 상승", 
        "30거래일 최저가 영역", "60거래일 최저가 영역", "90거래일 최저가 영역",
       "20일 평균거래량 10억 이하","20일 평균거래량 20억 이하","60일 평균거래량 10억 이하","60일 평균거래량 20억 이하",
       "100일 평균거래량 10억 이하","100일 평균거래량 20억 이하"]


# In[15]:


년도별조건 = old[필터조건]


# In[16]:


년도별조건.to_csv("daily_stock_filter.csv", encoding = "ms949")


# In[ ]:




