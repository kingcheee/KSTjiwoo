"""
===========================================================
📌 Pandas 기초 — 시험공부 발표용 코드
===========================================================
강조: DataFrame, 결측치 처리, 필터링, groupby가 핵심!
===========================================================
"""

import pandas as pd
import numpy as np

# ==========================================================
# 1. Series와 DataFrame 생성
# ==========================================================

# Series: 1차원 (엑셀의 한 열)
ages = pd.Series([25, 30, 35], name="나이")
print(ages)

# DataFrame: 2차원 (엑셀 시트 전체)
# 딕셔너리 → DataFrame 변환 ⭐
data = {
    "c0": [1, 2, 3],
    "c1": [4, 5, 6],
    "c2": [7, 8, 9]
}
df = pd.DataFrame(data)
print(df)
#    c0  c1  c2
# 0   1   4   7
# 1   2   5   8
# 2   3   6   9

# ⚠️ 딕셔너리 키 = 컬럼명, 값 = 데이터


# ==========================================================
# 2. 데이터 불러오기 & 훑어보기 ⭐
# ==========================================================

# CSV 파일 불러오기
# df = pd.read_csv("netflix.csv", encoding="utf-8")

# 가상 데이터로 실습
netflix = pd.DataFrame({
    "title": ["오징어게임", "기묘한이야기", "더글로리", "D.P.", "마블영화"],
    "type": ["TV Show", "TV Show", "TV Show", "TV Show", "Movie"],
    "duration": [60, 50, 55, 45, 120],
    "rating": [9.0, 8.7, 8.5, 8.8, 7.5],
    "release_year": [2021, 2016, 2022, 2021, 2019]
})

# head(): 상위 5행 미리보기
print(netflix.head())
print(netflix.head(3))  # 상위 3행

# shape: 데이터 크기 (행, 열)
print(netflix.shape)  # (5, 5)

# info(): 전체 요약 정보 ⭐
# 컬럼명, 데이터 타입, 결측치 여부를 한눈에!
print(netflix.info())


# ==========================================================
# 3. 결측치 처리 ⭐ 매우 중요!
# ==========================================================

# 결측치가 있는 데이터 만들기
df_missing = pd.DataFrame({
    "title": ["오징어게임", None, "더글로리"],
    "director": ["황동혁", "더프브라더스", None],
    "rating": [9.0, 8.7, None]
})

# isna(): 결측치 확인
print(df_missing.isna())
#     title  director  rating
# 0   False     False   False
# 1    True     False   False
# 2   False      True    True

# isna().sum(): 열별 결측치 개수 ⭐
print(df_missing.isna().sum())
# title       1
# director    1
# rating      1

# fillna(): 결측치 채우기
df_missing["rating"] = df_missing["rating"].fillna(0)  # 0으로 채우기
df_missing["title"] = df_missing["title"].fillna("No Data")  # 문자열로 채우기

# dropna(): 결측치 제거
df_clean = df_missing.dropna()  # 결측치가 있는 행 전체 삭제

# ⚠️ 중요 옵션!
# axis=1: 결측치가 포함된 열 전체 제거
# subset=['director']: director 열에 결측치가 있는 행만 제거
# inplace=True: 원본 데이터에 영구 반영 (반드시 같이 사용!)
# df.dropna(subset=['director'], inplace=True)


# ==========================================================
# 4. 데이터 필터링 ⭐ 매우 중요!
# ==========================================================

# 마스크 방식 필터링
# 조건을 [] 안에 넣으면 True인 행만 추출!
recent = netflix[netflix["release_year"] > 2020]
print(recent)
#      title     type  duration  rating  release_year
# 0  오징어게임  TV Show        60     9.0          2021
# 2   더글로리  TV Show        55     8.5          2022
# 3     D.P.  TV Show        45     8.8          2021

# 여러 조건 결합 (&: 그리고, |: 또는)
# ⚠️ 각 조건을 괄호로 감싸야 함!
result = netflix[(netflix["release_year"] > 2020) & (netflix["rating"] > 8.7)]
print(result)

# query() 함수 — SQL처럼 직관적 필터링 ⭐
# 강사님: "SQL의 WHERE 조건절처럼 매우 직관적!"
result2 = netflix.query("release_year > 2020 and rating > 8.7")
print(result2)

# 특정 열 추출 — ⚠️ 대괄호 두 개([[]]) 사용!
print(netflix[["title", "rating"]])  # DataFrame 형태로 출력
# netflix["title"] → Series (1차원)
# netflix[["title"]] → DataFrame (2차원, 표 형태)


# ==========================================================
# 5. groupby() — 그룹별 통계 ⭐ 중요!
# ==========================================================
# 비유: 과일을 종류별로 바구니에 나눠 담고, 각 바구니의 평균 무게 재기

# type별 평균 duration
type_duration = netflix.groupby("type")["duration"].mean()
print(type_duration)
# type
# Movie       120.0
# TV Show      52.5

# type별 여러 통계
type_stats = netflix.groupby("type").agg({
    "duration": ["mean", "min", "max"],
    "rating": ["mean", "count"]
})
print(type_stats)


# ==========================================================
# 6. 텍스트 조작 ⭐ 중요!
# ==========================================================

# str.contains: 특정 단어 포함 여부
# case=False: 대소문자 무시, na=False: 결측치 에러 방지
squid = netflix[netflix["title"].str.contains("오징어", case=False, na=False)]
print(squid)

# str.split + expand=True: 텍스트 분리
# 예: "Action, Drama, Thriller" → 3개 열로 분리
genres = pd.DataFrame({
    "title": ["오징어게임", "기묘한이야기"],
    "listed_in": ["Action, Drama", "Drama, Horror, Sci-Fi"]
})
split_genres = genres["listed_in"].str.split(", ", expand=True)
print(split_genres)
#          0      1       2
# 0   Action  Drama    None
# 1   Drama  Horror  Sci-Fi

# .stack(): 여러 열 → 단일 열로 쌓기
stacked = split_genres.stack()
print(stacked)
# 0  0     Action
#    1      Drama
# 1  0      Drama
#    1     Horror
#    2    Sci-Fi

# value_counts(): 장르별 개수 집계
genre_counts = stacked.value_counts()
print(genre_counts)
# Drama      2
# Action     1
# Horror     1
# Sci-Fi     1


# ==========================================================
# 7. 피처 엔지니어링 — 새로운 변수 만들기 ⭐
# ==========================================================
# 기존 변수를 활용해 분석에 유용한 새로운 정보를 생성!

# .map() 함수로 값 매핑
age_group_dic = {
    "TV-MA": "성인",
    "TV-14": "청소년",
    "TV-PG": "전체관람",
    "R": "성인",
    "PG-13": "청소년"
}
netflix_df = pd.DataFrame({
    "title": ["오징어게임", "기묘한이야기", "더글로리"],
    "rating": ["TV-MA", "TV-14", "TV-MA"]
})
netflix_df["age_group"] = netflix_df["rating"].map(age_group_dic)
print(netflix_df)
#      title rating age_group
# 0  오징어게임  TV-MA        성인
# 1  기묘한이야기  TV-14      청소년
# 2   더글로리  TV-MA        성인

# 전처리 데이터 저장
# netflix_df.to_csv("netflix_processed.csv", index=False, encoding="utf-8")


print("✅ Pandas 기초 끝!")
