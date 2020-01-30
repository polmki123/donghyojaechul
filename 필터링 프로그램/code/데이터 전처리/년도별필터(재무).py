#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# # 데이터를 불러온다

# In[135]:


df = pd.read_csv("..\\..\\data\\donghyojaechul_yearly_financial_5years.csv", encoding = "ms949")


# # 데이터의 계정이름을 사용하기 쉬운 계정이름으로 변환

# In[136]:


계정명 = df["Item Name "].drop_duplicates().tolist()


# In[137]:


바꿀계정명 = ["매출액", "영업이익", "지배주주순이익", "총자본", "총부채", "자본금", "이익잉여금", 
                 "영업활동으로인한현금흐름", "투자활동으로인한현금흐름", "배당", "주가", "상장주식수"]


# In[138]:


temp = {}

for 계정 in range(len(계정명)):
    temp[계정명[계정]] = 바꿀계정명[계정]
    print(계정명[계정]+ "     ->     " +  바꿀계정명[계정])


# ### 바뀐 계정 할당

# In[139]:


df = df.replace({"Item Name ": temp})


# ### df타입을 실수로 변환

# In[140]:


### 컬럼의 2014-12-31 string 포맷을 datetime 포맷으로 바꾼 후 데이터프레임을 회사명과 시간의 이중 인덱스로 바꿔줌


# In[141]:


df = df.set_index(['Symbol', "Item Name "])
시간변환 = pd.to_datetime(df.columns)

시간변환 = 시간변환.strftime("%Y-%m-%d")
시간변환 = 시간변환.rename("date")
df.columns = pd.to_datetime(시간변환)
df = df.stack().swaplevel().unstack()


# In[142]:


df


# ### df type 실수로 변환

# In[143]:


for 계정 in df.columns:
    df[계정] = df[계정].str.replace(',', "")

df = df.astype(float)


# ### 생성하는 지표

# In[144]:


df["시가총액"] = df["주가"] * df["상장주식수"]


# In[145]:


df["ROE"] = df["지배주주순이익"] /  df["총자본"]


# # 필터링 조건들을 생성한다

# In[146]:


company_list = df.index.levels[0]


# In[149]:


new_data = []
for company in company_list:
    temp = df.loc[company]
    
    ## 포괄손익계산서
    # 매출액 100억이상
    temp["매출액 100억 이상"] = temp["매출액"] > 10000000000
    
    #영업이익 3개년 모두 0 이상
    temp["영업이익 0 이상"] = temp["영업이익"] > 0 
    temp["영업이익 1년전 0 이상"] = temp["영업이익"].shift(1) > 0 
    temp["영업이익 2년전 0 이상"] = temp["영업이익"].shift(2) > 0 
    temp["영업이익 3년동안 0 이상"] = (temp["영업이익 0 이상"] > 0) & (temp["영업이익 1년전 0 이상"] > 0) & (temp["영업이익 2년전 0 이상"] > 0)
    
    # 매출액 3년 동안 증가
    
    temp["매출액이 과거 1년&2년전 보다 크다"] = (temp["매출액"] > temp["매출액"].shift(1)) & (temp["매출액"] > temp["매출액"].shift(2))
    temp["과거 1년전 매출액이 2년전 매출액보다 크다"] = temp["매출액"].shift(1) > temp["매출액"].shift(2)
    temp["매출액 3년동안 증가"] = temp["매출액이 과거 1년&2년전 보다 크다"] & temp["과거 1년전 매출액이 2년전 매출액보다 크다"]    
    
    # 시가총액 비율
    temp["순이익시총비율 0.1이상"] = (temp["지배주주순이익"] / temp["시가총액"])  > 0.1
    temp["영업이익시총비율 0.1이상"] = (temp["영업이익"] / temp["시가총액"]) > 0.1
    
    
    
    ## 재무상태표
    # 자본잠식
    temp["자본잠식 없음"] = temp["총자본"] > 0
    
    # 부채비율
    temp["부채비율"] = temp["총부채"] / temp["총자본"]
    temp["부채비율 150% 이하"] = temp["부채비율"] < 1.5
    temp["부채비율 감소추세"] = (temp["부채비율"] < temp["부채비율"].shift(1)) & (temp["부채비율"] < temp["부채비율"].shift(2))
    
    # 자본금
    temp["자본금 증가율"] = (temp["자본금"] - temp["자본금"].shift(1)) / temp["자본금"].shift(1)
    temp["자본금 변동없음"] = temp["자본금 증가율"].abs() < 0.05
    
    # 이익잉여금
    temp["이익잉여금이 과거 1년&2년전 보다 크다"] = (temp["이익잉여금"] > temp["이익잉여금"].shift(1)) & (temp["이익잉여금"] > temp["이익잉여금"].shift(2))
    temp["과거 1년전 이익잉여금이 2년전 이익잉여금보다 크다"] = temp["이익잉여금"].shift(1) > temp["이익잉여금"].shift(2)
    temp["이익잉여금이 3년동안 증가"] = temp["이익잉여금이 과거 1년&2년전 보다 크다"] & temp["과거 1년전 이익잉여금이 2년전 이익잉여금보다 크다"]

    
    ## 현금흐름표
    
    temp["영업활동으로인한현금흐름 판별"] = temp["영업활동으로인한현금흐름"] > 0
    temp["3년 중 2년 이상 영업활동으로인한현금흐름 0 이상"] = (temp["영업활동으로인한현금흐름 판별"].rolling(3).sum() > 2)
    
    ## 배당
    temp["배당존재"] = temp["배당"] > 0 
    temp["배당이 과거 1년&2년전 보다 크다"] = (temp["배당"] > temp["배당"].shift(1)) & (temp["배당"] > temp["배당"].shift(2))
    temp["과거 1년전 배당이 2년전 배당보다 크다"] = temp["배당"].shift(1) > temp["배당"].shift(2)
    temp["배당이 3년동안 증가"] = temp["배당이 과거 1년&2년전 보다 크다"] & temp["과거 1년전 배당이 2년전 배당보다 크다"]
    
    
    ## 기타
    
    # ROE가 5% 이상
    temp["ROE 5퍼 이상"]  = temp["ROE"] > 0.05
    
    
    temp["Symbol"] = company
    temp = temp.reset_index()
    temp = temp.set_index(["Symbol", "date"])
    
    new_data.append(temp)  


# In[150]:


old = pd.DataFrame()
for company_data in new_data:
    old = pd.concat([old, company_data])


# In[151]:


필터조건 = ["매출액 100억 이상", "영업이익 3년동안 0 이상", "매출액 3년동안 증가", "순이익시총비율 0.1이상", 
        "영업이익시총비율 0.1이상","자본잠식 없음", "부채비율 150% 이하", "부채비율 감소추세", "자본금 변동없음", 
        "이익잉여금이 3년동안 증가","3년 중 2년 이상 영업활동으로인한현금흐름 0 이상", "배당존재", "배당이 3년동안 증가",
       "ROE 5퍼 이상"]


# In[152]:


년도별조건 = old[필터조건]


# In[153]:


년도별조건.to_csv("year_filter.csv", encoding = "ms949")


# In[ ]:




