import pandas as pd
import datetime

class Year_Filter():
  def __init__(self): 
    df = pd.read_csv("..\\..\\data\\연도별 재무.csv", encoding = "ms949")
    A = df[(df["Kind"] == "NFS-IFRS(C)") & (df["Item Name "] == "매출액(천원)")]
    df.loc[A.index, "Item Name "] = "매출액(연결)"
    계정명 = df["Item Name "].drop_duplicates().tolist()
    바꿀계정명 = ["연결매출","매출액", "영업이익", "지배주주순이익", "총자본", "총부채", "자본금", "이익잉여금", 
                    "영업활동으로인한현금흐름", "투자활동으로인한현금흐름", "배당", "주가", "종가", "상장주식수"]

    for 계정 in range(len(계정명)):
        temp[계정명[계정]] = 바꿀계정명[계정]
        print(계정명[계정]+ "     ->     " +  바꿀계정명[계정])
    df = df.replace({"Item Name ": temp})
    df = df.drop("Kind", axis=1)
    df = df.set_index(['Symbol', "Item Name "])
    시간변환 = pd.to_datetime(df.columns)
    시간변환 = 시간변환.strftime("%Y")
    시간변환 = 시간변환.rename("date")
    df.columns = 시간변환
    df = df.stack().swaplevel().unstack()


    for 계정 in df.columns:
        df[계정] = df[계정].str.replace(',', "")

    df = df.astype(float)
    df["ROE"] = df["지배주주순이익"] /  df["총자본"]
    df["영업이익률"] = df["영업이익"] / df["매출액"]
    
    lag_1year = df.groupby(["Symbol"]).transform(lambda x : x.shift(1))
    lag_2year = df.groupby(["Symbol"]).transform(lambda x : x.shift(2))
    lag_3year = df.groupby(["Symbol"]).transform(lambda x : x.shift(3))
    lag_4year = df.groupby(["Symbol"]).transform(lambda x : x.shift(4))

    self.year_filter = [] 
    self.df = df
    self.lag_1year = self.lag_year_df(lag_1year, 1)
    self.lag_2year = self.lag_year_df(lag_2year, 2)
    self.lag_3year = self.lag_year_df(lag_3year, 3)
    self.lag_4year = self.lag_year_df(lag_4year, 4)

  def lag_year_df(self, df, lag_year):
      data= df.copy()
      new_index_list = []
      for index in data.columns:
          new_index = index + " " + str(lag_year) + "Y lag"
          new_index_list.append(new_index)


      data.columns = new_index_list
      
      return data
# 시가총액 비율
# 이런 식으로 재무데이터와 주가 데이터가 혼합
# 이걸 할 수가 없네

#     temp["순이익시총비율 0.1이상"] = (temp["지배주주순이익"] / temp["시가총액"])  > 0.1
#     temp["영업이익시총비율 0.1이상"] = (temp["영업이익"] / temp["시가총액"]) > 0.1

# 영업이익 1Y lag와 비교하던지


## 재무상태표
# 자본잠식

  def YEAR_UI_FITER(매출액, 영업이익, 영업이익_1Y_lag, 영업이익_2Y_lag ):
    필터조건 = ["매출액 100억 이상", "영업이익 3년동안 0 이상", "영업이익률 3년동안 증가", "매출액 3년동안 증가",  
        "자본잠식 없음", "부채비율 150% 이하", "자본금 변동없음", 
        "이익잉여금이 3년동안 증가","3년 중 2년 이상 영업활동으로인한현금흐름 0 초과",
        "3년 중 2년 이상 투자활동으로인한현금흐름 0 미만","배당존재", "배당이 3년동안 증가","ROE 5퍼 이상"]
    temp = {}
    temp["시가총액"] = temp["상장주식수"] * temp["종가"]

    # 포괄손익계산서
    # 매출액 단위(천원)
    temp["매출액 100억 이상"] = temp["매출액"] > 매출액

    #영업이익 3개년 모두 0 이상
    temp["영업이익 3년동안 0 이상"] = (temp["영업이익"] > 영업이익) & (temp["영업이익 1Y lag"] > 영업이익_1Y_lag) & (temp["영업이익 2Y lag"] > 영업이익_2Y_lag)

    # 영업이익률 증가
    temp["영업이익률 3년동안 증가"] = (temp["영업이익률"] > temp["영업이익률 1Y lag"]) &  (temp["영업이익률"] > temp["영업이익률 2Y lag"]) &  (temp["영업이익률 1Y lag"] > temp["영업이익률 2Y lag"])

    # 매출액 3년 동안 증가
    temp["매출액 3년동안 증가"] = (temp["매출액"] > temp["매출액 1Y lag"]) &  (temp["매출액"] > temp["매출액 2Y lag"]) &  (temp["매출액 1Y lag"] > temp["매출액 2Y lag"])

    temp["자본잠식 없음"] = temp["총자본"] > 총자본

    # 부채비율
    temp["부채비율"] = temp["총부채"] / temp["총자본"]
    temp["부채비율 150% 이하"] = temp["부채비율"] < 부채비율

    # 자본금
    temp["자본금 증가율"] = (temp["자본금"] - temp["자본금 1Y lag"]) / temp["자본금 1Y lag"]
    temp["자본금 변동없음"] = temp["자본금 증가율"].abs() < 0.05

    # 이익잉여금

    temp["이익잉여금이 3년동안 증가"] = (temp["이익잉여금"] > temp["이익잉여금 1Y lag"]) &  (temp["이익잉여금"] > temp["이익잉여금 2Y lag"]) &  (temp["이익잉여금 1Y lag"] > temp["이익잉여금 2Y lag"])


    ## 현금흐름표

    # 영업활동현금흐름
    temp["영업활동으로인한현금흐름 판별"] = temp["영업활동으로인한현금흐름"] > 0
    temp["3년 중 2년 이상 영업활동으로인한현금흐름 0 초과"] = (temp["영업활동으로인한현금흐름 판별"].rolling(3).sum() > 2)

    # 투자활동현금흐름
    temp["투자활동으로인한현금흐름 판별"] = temp["투자활동으로인한현금흐름"] < 0
    temp["3년 중 2년 이상 투자활동으로인한현금흐름 0 미만"] = (temp["투자활동으로인한현금흐름 판별"].rolling(3).sum() > 2)

    ## 배당
    temp["배당존재"] = temp["배당"] > 0 
    temp["배당이 3년동안 증가"] =(temp["배당"] > temp["배당 1Y lag"]) &  (temp["배당"] > temp["배당 2Y lag"]) &  (temp["배당 1Y lag"] > temp["배당 2Y lag"])

    ## 기타
    # ROE가 5% 이상(수익성)
    temp["ROE"] = temp["지배주주순이익"] / temp["총자본"]
    temp["ROE 5퍼 이상"]  = temp["ROE"] > 0.05

    year_filter = temp[필터조건]

    self.year_filter = year_filter.reset_index().set_index(["date", "Symbol"]).sort_index()

    year_filter.to_csv("year_filter.csv", encoding = "ms949")

    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d")

    get_ref_year = assign_year(now)

    year_filter.loc[get_ref_year].head()

  def assign_year(self, date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    year = date.year
    month = date.month
    
    if month > 3:
        ref_year = year - 1
        
    else:
        ref_year = year - 2
        
    return str(ref_year)

      