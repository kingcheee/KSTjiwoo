"""
===========================================================
📌 Pandas 기초 — 스터디 발표용 치트시트
===========================================================
목표: 엑셀처럼 데이터를 다루는 판다스의 핵심 기능 익히기
시간: 발표 약 4분분량
===========================================================
"""

import pandas as pd
import numpy as np

# ==========================================================
# 1. Series와 DataFrame — 판다스의 기본 구조
# ==========================================================
# 비유: Series = 📋 엑셀의 한 열, DataFrame = 📊 엑셀 시트 전체

# Series 생성 (1차원)
# 비유: 엑셀에서 딱 하나의 열을 똑 떼어낸 것
ages = pd.Series([25, 30, 35, 40], name="나이")
print(ages)
# 0    25
# 1    30
# 2    35
# 3    40
# Name: 나이, dtype: int64

# 인덱스 지정
ages.index = ["규연", "지우", "민수", "수진"]
print(ages["규연"])  # 25

# DataFrame 생성 (2차원)
# 비유: 엑셀 스프레드시트 그 자체!
data = {
    "이름": ["규연", "지우", "민수", "수진"],
    "나이": [25, 27, 30, 28],
    "도시": ["광주", "서울", "부산", "대전"],
    "점수": [90, 85, 92, 78]
}
df = pd.DataFrame(data)
print(df)
#    이름  나이  도시  점수
# 0  규연  25  광주  90
# 1  지우  27  서울  85
# 2  민수  30  부산  92
# 3  수진  28  대전  78

# 기본 정보 확인
print(df.shape)       # (4, 4)  → 4행 4열
print(df.dtypes)      # 각 열의 데이터 타입
print(df.columns)     # 열 이름 목록
print(df.index)       # 인덱스 목록


# ==========================================================
# 2. 데이터 읽기/저장 — CSV 파일 다루기
# ==========================================================

# CSV 파일 읽기 (가장 많이 사용!)
# df = pd.read_csv("netflix.csv", encoding="utf-8")

# CSV 파일 저장
# df.to_csv("output.csv", index=False, encoding="utf-8")

# 엑셀 파일 읽기/저장
# df = pd.read_excel("data.xlsx")
# df.to_excel("output.xlsx", index=False)

# 데이터 미리보기
print(df.head())      # 처음 5행 (기본값)
print(df.head(3))     # 처음 3행
print(df.tail())      # 마지막 5행
print(df.sample(2))   # 랜덤으로 2행 추출


# ==========================================================
# 3. 데이터 선택 및 필터링 — 원하는 데이터만 쏙쏙
# ==========================================================
# 비유: 거름망으로 원하는 것만 걸러내기

# --- 열 선택 ---
print(df["이름"])           # 하나의 열 → Series 반환
print(df[["이름", "점수"]])  # 여러 열 → DataFrame 반환

# --- 행 선택 (loc vs iloc) ---
# loc: 이름(라벨)으로 찾기 — 비유: 주소로 찾기 🏠
print(df.loc[0])            # 인덱스 0번 행
print(df.loc[0:2])          # 인덱스 0~2번 행 (끝 포함!)
print(df.loc[0, "이름"])    # 0행 "이름"열 → "규연"

# iloc: 위치(숫자)로 찾기 — 비유: 줄 번호로 찾기 🔢
print(df.iloc[0])           # 첫 번째 행
print(df.iloc[0:3])         # 0~2번째 행 (끝 미포함!)
print(df.iloc[0, 1])        # 0행 1열 → 25

# --- 조건부 필터링 ---
# 비유: 거름망에 조건을 걸어서 원하는 것만 통과시키기
high_score = df[df["점수"] >= 90]
print(high_score)
#    이름  나이  도시  점수
# 0  규연  25  광주  90
# 2  민수  30  부산  92

# 여러 조건 결합 (&: 그리고, |: 또는)
result = df[(df["점수"] >= 85) & (df["나이"] < 30)]
print(result)
#    이름  나이  도시  점수
# 0  규연  25  광주  90
# 1  지우  27  서울  85

# isin(): VIP 명단 확인 — 특정 값들 중에 있는지
# 비유: 출입 명부에 이름이 있는지 확인 📋
cities = ["광주", "서울"]
filtered = df[df["도시"].isin(cities)]
print(filtered)
#    이름  나이  도시  점수
# 0  규연  25  광주  90
# 1  지우  27  서울  85

# 문자열 조건 (포함, 시작, 끝)
# df[df["이름"].str.contains("연")]  # "연"이 포함된 이름
# df[df["도시"].str.startswith("서")]  # "서"로 시작하는 도시


# ==========================================================
# 4. 결측치 처리 — 빠진 데이터 대처하기
# ==========================================================
# 비유: 🧩 이 빠진 퍼즐 조각 — 버릴까? 메울까?

# 결측치가 있는 데이터 만들기
df_missing = pd.DataFrame({
    "이름": ["규연", "지우", None, "수진"],
    "점수": [90, None, 85, None],
    "도시": ["광주", "서울", "부산", "대전"]
})

# 결측치 확인
print(df_missing.isnull())       # True/False로 결측치 위치 확인
print(df_missing.isnull().sum())  # 열별 결측치 개수
# 이름    1
# 점수    2
# 도시    0

# 결측치 비율 계산
missing_ratio = df_missing.isnull().sum() / len(df_missing) * 100
print(missing_ratio)

# 전략 1: 결측치 삭제 (5% 미만일 때 추천)
df_dropped = df_missing.dropna()  # 결측치가 있는 행 전체 삭제
print(df_dropped)

# 특정 열에 결측치가 있을 때만 삭제
df_dropped_col = df_missing.dropna(subset=["점수"])

# 전략 2: 결측치 채우기 (5~20%일 때 추천)
# 비유: 빈 구멍을 비슷한 조각으로 메우기
df_filled = df_missing.copy()
df_filled["점수"] = df_filled["점수"].fillna(df_filled["점수"].mean())  # 평균으로 채우기
print(df_filled)

# 다양한 채우기 방법
# df["점수"].fillna(df["점수"].median())  # 중앙값으로 채우기
# df["점수"].fillna(df["점수"].mode()[0]) # 최빈값으로 채우기
# df["점수"].fillna(0)                    # 0으로 채우기
# df["점수"].fillna(method="ffill")       # 앞의 값으로 채우기 (forward fill)
# df["점수"].fillna(method="bfill")       # 뒤의 값으로 채우기 (backward fill)

# 전략 3: 열 자체 제거 (20% 이상 결측일 때)
# df_missing.drop(columns=["점수"])


# ==========================================================
# 5. 데이터 추가/삭제/수정
# ==========================================================

df = pd.DataFrame({
    "이름": ["규연", "지우", "민수"],
    "점수": [90, 85, 92]
})

# 열 추가
df["등급"] = ["A", "B", "A"]
df["등여부"] = df["점수"] >= 90  # 조건으로 열 추가

# 행 추가
new_row = pd.DataFrame({"이름": ["수진"], "점수": [78], "등급": ["C"], "등여부": False})
df = pd.concat([df, new_row], ignore_index=True)

# 열 삭제
df = df.drop(columns=["등여부"])

# 값 수정
df.loc[0, "점수"] = 95  # 규연의 점수를 95로 변경

# 열 이름 변경
df = df.rename(columns={"점수": "성적"})


# ==========================================================
# 6. groupby — 그룹별 분석
# ==========================================================
# 비유: 🍎🍐🍇 과일을 종류별로 바구니에 나눠 담고, 각 바구니의 평균 무게 재기

# 넷플릭스 데이터 예시 (가상 데이터)
netflix = pd.DataFrame({
    "title": ["오징어게임", "기묘한이야기", "더글로리", "D.P.", "마블영화"],
    "type": ["TV Show", "TV Show", "TV Show", "TV Show", "Movie"],
    "duration_min": [60, 50, 55, 45, 120],
    "rating": [9.0, 8.7, 8.5, 8.8, 7.5]
})

# type별 평균 duration
type_avg = netflix.groupby("type")["duration_min"].mean()
print(type_avg)
# type
# Movie       120.0
# TV Show      52.5

# 여러 통계를 한 번에
type_stats = netflix.groupby("type").agg({
    "duration_min": ["mean", "min", "max"],
    "rating": ["mean", "count"]
})
print(type_stats)

# 그룹별 필터링: 평균 점수가 8.5 이상인 타입만
high_rated = netflix.groupby("type").filter(lambda x: x["rating"].mean() >= 8.5)
print(high_rated)


# ==========================================================
# 7. describe() — 데이터 종합 건강 검진
# ==========================================================
# 비종: 🏥 건강 검진 리포트 한 장에 모든 정보 요약

print(df.describe())
#              점수
# count   4.000000  ← 데이터 개수
# mean   86.250000  ← 평균
# std     7.500000  ← 표준편차
# min    78.000000  ← 최솟값
# 25%    83.250000  ← 1사분위수
# 50%    87.500000  ← 중앙값
# 75%    92.750000  ← 3사분위수
# max    95.000000  ← 최댓값

# 문자열 열 포함
print(df.describe(include="all"))


# ==========================================================
# 8. 정렬과 순위
# ==========================================================

# 정렬
df_sorted = df.sort_values("점수", ascending=False)  # 점수 내림차순
print(df_sorted)

# 여러 기준 정렬
# df.sort_values(["등급", "점수"], ascending=[True, False])

# 순위
df["순위"] = df["점수"].rank(ascending=False)


# ==========================================================
# 9. 실전 예시 — 타이타닉 데이터 분석 흐름
# ==========================================================

# 타이타닉 데이터 로드 (seaborn 내장 데이터셋)
# import seaborn as sns
# titanic = sns.load_dataset("titanic")

# 분석 흐름 예시:
# 1. 데이터 확인
# titanic.head()
# titanic.info()
# titanic.describe()

# 2. 결측치 확인
# titanic.isnull().sum()

# 3. 결측치 처리
# titanic["age"].fillna(titanic["age"].median(), inplace=True)
# titanic["embarked"].fillna(titanic["embarked"].mode()[0], inplace=True)

# 4. 생존율 분석
# survival_by_class = titanic.groupby("pclass")["survived"].mean()
# survival_by_sex = titanic.groupby("sex")["survived"].mean()

# 5. 필터링
# survivors = titanic[titanic["survived"] == 1]
# first_class_female = titanic[(titanic["pclass"] == 1) & (titanic["sex"] == "female")]


print("✅ Pandas 기초 치트시트 끝!")
print("다음 파일: 04_matplotlib_basics.py → ")
