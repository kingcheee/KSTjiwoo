# 🎤 파이썬 데이터 분석 기초 — 시험공부 발표 대본

> 📌 **주제**: 파이썬 데이터 분석 기초 (Python → NumPy → Pandas → 시각화)
> 📌 **대상**: 시험 준비하는 스터디 친구들
> 📌 **소요 시간**: 약 20분
> 📌 **자료 출처**: NotebookLM "시험공부 노트북" (5/27 ~ 6/2 수업, 10개 소스)
> 📌 **⭐ 표시**: 강사님이 중요하다고 강조한 내용

---

## 🎬 오프닝 (1분)

> 안녕! 오늘 시험공부 발표 레전드로 준비했당 🔥
>
> 5월 27일부터 6월 2일까지 6번의 수업 내용을 전부 정리했어.
> 강사님이 **"중요하다!"** 하고 강조한 것들은 ⭐ 표시 해놨으니까 특히 집중해!
>
> 오늘 발표 흐름:
> 1. **파이썬 기초** (5/27) — 리스트 컴프리헨션 ⭐
> 2. **NumPy** (5/28~29) — 마스크 필터링 ⭐, 행렬 곱셈 ⭐
> 3. **Pandas** (5/29~6/1) — 결측치 처리 ⭐, 필터링 ⭐, groupby ⭐
> 4. **시각화 & 프로젝트** (6/2) — 피처 엔지니어링 ⭐, 텍스트 조작 ⭐
>
> 그럼 시작할게 ㅇㅇ

---

## 📖 Part 1. 파이썬 기초 (5월 27일, 4분)

### 1-1. print() 함수 — 출력 제어

> 가장 기본적인 출력 함수야. 근데 속성을 알면 더 유용해!

```python
# 기본 출력
print("안녕!")  # 자동으로 줄바꿈됨

# end 속성: 줄바꿈 없이 이어서 출력
print("Hello", end=" ")
print("World")  # Hello World

# sep 속성: 여러 값 사이에 구분자 넣기
print("사과", "바나나", "포도", sep=" → ")
# 사과 → 바나나 → 포도
```

### 1-2. f-string — 문자열 포매팅

> **실무에서 가장 많이 쓰이는 방식**이야!

```python
name = "규연"
age = 25
print(f"나의 이름은 {name} 입니다. 나이는 {age} 입니다.")

# f-string 안에서 연산도 가능!
print(f"10년 후 나이: {age + 10}")  # 10년 후 나이: 35
```

### 1-3. 조건문 — if, elif, else

> ⚠️ **두 가지 주의사항이 있어!**

**주의 1: 들여쓰기(Indentation)가 매우 중요!**
> 파이썬은 들여쓰기로 코드 블록을 구분해. 탭(Tab) 사용에 주의해야 해!

**주의 2: 조건 순서가 매우 중요! ⭐**
> **범위가 작은 것부터 시작해서 넓은 쪽으로 내려가며 작성**해야 해!

```python
score = 85

# ✅ 올바른 순서: 작은 범위 → 큰 범위
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"      # ← 85는 여기 해당!
elif score >= 70:
    grade = "C"
else:
    grade = "F"

# ❌ 잘못된 순서 (시험에 나올 수 있어!)
if score >= 70:      # 85 >= 70 → True! 여기서 멈춤!
    grade = "C"      # 결과: C등급 (틀린 답!)
elif score >= 80:    # 절대 실행 안 됨!
    grade = "B"
```

> 💡 **in 연산자**도 자주 써!
> 특정 값이 리스트 안에 있는지 확인할 때 유용해.

```python
pocket = ["money", "phone", "keys"]
if "money" in pocket:
    print("택시를 타자!")  # 주머니에 돈이 있으면 True
```

### 1-4. 반복문 — while, for

> 강사님: **"while문보다 for문이 훨씬 더 중요하다!"** ⭐

**while문**: 반복 횟수가 불명확할 때
```python
# 패턴: 초기식 → 조건식 → 실행문 → 증감식
count = 1
while count <= 5:
    print(f"{count}번째")
    count += 1  # ⚠️ 증감식 없으면 무한 루프!
```

**for문**: 코딩에서 가장 많이 쓰이는 반복문! ⭐
```python
# range() 함수 연동
total = 0
for num in range(1, 101):  # 1~100까지
    total += num
print(total)  # 5050

# 리스트 연동
fruits = ["사과", "바나나", "포도"]
for fruit in fruits:
    print(f"오늘의 과일: {fruit}")
```

### 1-5. 리스트 컴프리헨션 (List Comprehension) ⭐⭐⭐ 가장 중요!

> 강사님: **"가장 중요하다고 거듭 강조된 핵심 문법!"** 🔥
>
> 기존 방식: 빈 리스트 만들고 → for문 돌리고 → append로 추가 (3줄)
> 컴프리헨션: **단 한 줄로 압축!** (1줄)

```python
# 기존 방식 (3줄)
result = []
for x in range(1, 6):
    result.append(x * 3)
print(result)  # [3, 6, 9, 12, 15]

# 리스트 컴프리헨션 (1줄!) ⭐
result = [x * 3 for x in range(1, 6)]
print(result)  # [3, 6, 9, 12, 15]
```

**구조**: `[표현식 for 변수 in 반복가능한객체]`

**if 조건 추가 가능!**
```python
# 1~10 중 짝수만 제곱해서 새 리스트
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(even_squares)  # [4, 16, 36, 64, 100]

# 실전: 문자열 리스트에서 길이 3 이상인 것만
words = ["hi", "hello", "hey", "world", "py"]
long_words = [w for w in words if len(w) >= 3]
print(long_words)  # ['hello', 'hey', 'world']
```

> 💡 **시험 팁**: 리스트 컴프리헨션은 시험에 거의 무조건 나와!
> 패턴을 외워두면 좋아: `[표현식 for 변수 in 범위 if 조건]`

---

## 📖 Part 2. NumPy — 빠른 숫자 계산 (5월 28~29일, 5분)

### 2-1. NumPy가 왜 필요해?

> 파이썬 리스트의 한계를 극복하기 위해 만들어진 라이브러리야!

```python
# 파이썬 리스트: * 2는 반복!
python_list = [1, 2, 3, 4, 5]
print(python_list * 2)
# [1,2,3,4,5,1,2,3,4,5] ← 반복만 됨! 😱

# NumPy 배열: * 2는 각 요소에 곱하기!
import numpy as np
numpy_array = np.array([1, 2, 3, 4, 5])
print(numpy_array * 2)
# [2 4 6 8 10] ← 진짜 계산! ✅
```

> 비유: 파이썬 리스트 = 🧍 한 사람이 계산, NumPy = 🏭 공장 자동화 라인

### 2-2. 배열 생성

```python
# 리스트 → NumPy 배열
arr = np.array([1, 2, 3, 4, 5])

# 2차원 배열 (행렬)
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])
print(matrix.shape)  # (2, 3) → 2행 3열

# 특별한 배열 생성
np.zeros((3, 4))       # 3×4 영행렬
np.ones((2, 3))        # 2×3 모두 1
np.arange(12)          # [0, 1, 2, ..., 11]
np.linspace(0, 1, 5)   # [0.0, 0.25, 0.5, 0.75, 1.0]

# ⚠️ arange vs linspace 차이! (시험 출제 포인트!)
# arange: 간격 기준 → np.arange(0, 10, 2) = [0, 2, 4, 6, 8]
# linspace: 개수 기준 → np.linspace(0, 10, 5) = [0, 2.5, 5, 7.5, 10]

# reshape: 배열 형태 변경
arr = np.arange(12)
reshaped = arr.reshape(3, 4)  # 12개 요소 → 3행 4열
```

### 2-3. 원소별(Element-wise) 연산 ⭐

> NumPy를 사용하는 가장 큰 이유!

```python
arr = np.array([1, 2, 3, 4, 5])

# 사칙연산 모두 원소별로 적용
print(arr + 10)   # [11 12 13 14 15]
print(arr * 3)    # [ 3  6  9 12 15]
print(arr ** 2)   # [ 1  4  9 16 25]

# 비교 연산
print(arr > 3)    # [False False False  True  True]
```

### 2-4. 행렬 곱셈 (@ 연산자) ⭐

```python
A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])

# @ 연산자: 행렬 곱셈
C = A @ B
print(C)
# [[19 22]
#  [43 50]]
```

### 2-5. 마스크(Mask) 필터링 ⭐⭐⭐ 매우 중요!

> 강사님: **"실무에서 정말 많이 쓰이는 방법!"** 🔥
> 비유: 불리언 마스크 = 거름망 (True인 것만 통과!)

```python
data = np.array([10, 20, 30, 40, 50])

# 조건을 적용하면 True/False 배열(마스크)이 생성됨
mask = data > 30
print(mask)       # [False False  True  True  True]

# 마스크를 인덱스에 넣으면 True인 것만 추출!
print(data[mask])  # [40 50]

# 한 줄로 줄이면!
print(data[data > 30])  # [40 50]
```

**실전 예시: 스팸 메일 필터링**
```python
# 0 = 정상, 1 = 스팸 (2열이 스팸 여부)
emails = np.array([
    [100, 200, 0],  # 정상
    [50, 300, 1],   # 스팸
    [80, 150, 0],   # 정상
    [30, 400, 1],   # 스팸
])

# 2열이 0인 (정상 메일) 데이터만 추출
normal_mask = emails[:, 2] == 0
normal_emails = emails[normal_mask]
print(normal_emails)
# [[100 200   0]
#  [ 80 150   0]]
```

### 2-6. 정수 배열 인덱싱

> 원하는 특정 위치의 데이터들만 선택적으로 뽑아내는 방법!

```python
arr = np.array([10, 20, 30, 40, 50])

# 인덱스 배열로 원하는 위치의 값 뽑기
indices = [0, 2, 4]
print(arr[indices])  # [10 30 50]
```

### 2-7. 집계 함수 & 축(axis)

```python
arr = np.array([10, 20, 30, 40, 50])
print(arr.sum())    # 150
print(arr.mean())   # 30.0
print(arr.max())    # 50
print(arr.std())    # 표준편차

# 축(axis) 기준 집계
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
print(matrix.sum(axis=0))  # [12 15 18] ← 열 합계
print(matrix.sum(axis=1))  # [ 6 15 24] ← 행 합계
```

> 💡 **NumPy 핵심 정리**:
> - 원소별 연산이 기본!
> - 마스크 필터링은 실무에서 엄청 많이 써 ⭐
> - arange vs linspace 차이 구분할 것!

---

## 📖 Part 3. Pandas — 데이터 전처리 (5월 29일~6월 1일, 6분)

### 3-1. Series와 DataFrame

> Pandas는 **엑셀(Excel)이나 데이터베이스의 테이블과 같은 2차원 표 형태의 데이터를 가공하고 처리하는 데 아주 최적화된 라이브러리**야!

| 구조 | 비유 | 설명 |
|------|------|------|
| **Series** | 엑셀의 한 열 | 1차원 배열 |
| **DataFrame** | 엑셀 시트 전체 | 2차원 표 (여러 Series의 모음) |

```python
import pandas as pd

# Series: 1차원
ages = pd.Series([25, 30, 35], name="나이")

# DataFrame: 2차원 — 딕셔너리로 만들기! ⭐
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
```

> ⚠️ **딕셔너리 → DataFrame 변환 규칙** (시험 출제 포인트!)
> - 딕셔너리의 **키(Key)** = 컬럼명(열 이름)
> - 딕셔너리의 **값(Value)** = 해당 컬럼의 데이터

### 3-2. 데이터 불러오기 & 훑어보기 ⭐

```python
# CSV 파일 불러오기
# df = pd.read_csv("netflix.csv", encoding="utf-8")

# head(): 상위 5행 미리보기
df.head()      # 기본 5행
df.head(3)     # 상위 3행

# shape: 데이터 크기 (행, 열)
df.shape       # (200, 12) → 200행 12열

# info(): 전체 요약 정보 ⭐
# 컬럼명, 데이터 타입, 결측치 여부를 한눈에!
df.info()
```

### 3-3. 결측치(Missing Value) 처리 ⭐⭐⭐ 매우 중요!

> 강사님: **"실제 데이터를 다룰 때 가장 중요한 작업 중 하나!"** 🔥
> 비유: 🧩 이 빠진 퍼즐 — 버릴까? 메울까?

**결측치 확인**
```python
# isna(): True/False로 결측치 위치 확인
df.isna()

# isna().sum(): 열별 결측치 개수 ⭐
df.isna().sum()
# title       1
# director    5
# rating      2
```

**결측치 처리 전략 3가지** ⭐

| 전략 | 상황 | 함수 |
|------|------|------|
| **삭제** | 결측치 5% 미만 | `dropna()` |
| **대체** | 결측치 5~20% | `fillna()` |
| **열 제거** | 결측치 20% 이상 | `dropna(axis=1)` |

```python
# fillna(): 결측치 채우기
df["rating"] = df["rating"].fillna(0)           # 0으로 채우기
df["title"] = df["title"].fillna("No Data")     # 문자열로 채우기

# dropna(): 결측치 제거
df.dropna()                                     # 결측치가 있는 행 전체 삭제

# ⚠️ 중요 옵션들! (시험 출제 포인트!)
df.dropna(axis=1)                    # 결측치가 포함된 열 전체 제거
df.dropna(subset=["director"])       # director 열에 결측치가 있는 행만 제거
df.dropna(subset=["director"], inplace=True)  # 원본에 영구 반영! ⭐
```

> ⚠️ **inplace=True** 옵션을 함께 사용해야 원본 데이터에 결과가 영구적으로 반영돼!
> 이거 안 붙이면 원본은 그대로야!

### 3-4. 데이터 필터링 ⭐⭐⭐ 매우 중요!

> 강사님: **"방대한 데이터에서 원하는 정보만 골라내는 분석의 핵심 기술!"** 🔥

**마스크 방식 필터링**
```python
# 조건을 [] 안에 넣으면 True인 행만 추출!
recent = netflix[netflix["release_year"] > 2020]

# 여러 조건 결합 (&: 그리고, |: 또는)
# ⚠️ 각 조건을 괄호로 감싸야 함!
result = netflix[(netflix["release_year"] > 2020) & (netflix["rating"] > 8.7)]
```

**query() 함수 — SQL처럼 직관적! ⭐**
> 강사님: **"SQL의 WHERE 조건절처럼 매우 직관적으로 데이터를 추출할 수 있는 강력한 함수!"**

```python
# 마스크 방식
netflix[(netflix["release_year"] > 2020) & (netflix["rating"] > 8.7)]

# query() 방식 (더 직관적!) ⭐
netflix.query("release_year > 2020 and rating > 8.7")
```

**특정 열 추출 — ⚠️ 대괄호 두 개! ⭐**
```python
# 강사님: "반드시 대괄호를 두 개([[]]) 겹쳐서 사용해야 한다고 거듭 강조!"

netflix["title"]     # → Series (1차원)
netflix[["title"]]   # → DataFrame (2차원, 표 형태) ⭐
netflix[["title", "rating"]]  # → 여러 열 동시에 추출
```

### 3-5. groupby() — 그룹별 통계 ⭐⭐

> 강사님: **"특정 컬럼을 기준으로 데이터를 묶어 통계값을 구할 때 활용!"**
> 비유: 과일을 종류별로 바구니에 나눠 담고, 각 바구니의 평균 무게 재기

```python
# type별 평균 duration
netflix.groupby("type")["duration"].mean()
# type
# Movie       120.0
# TV Show      52.5

# 여러 통계를 한 번에
netflix.groupby("type").agg({
    "duration": ["mean", "min", "max"],
    "rating": ["mean", "count"]
})
```

### 3-6. 텍스트 조작 ⭐⭐ 중요!

> 강사님: **"텍스트 내부에 포함된 특정 문자를 검색하거나, 묶여 있는 데이터를 분리 및 재배치하는 고도화된 기술!"**

**str.contains — 텍스트 검색**
```python
# 'title'에서 특정 단어를 포함하는 행만 필터링
# case=False: 대소문자 무시
# na=False: 결측치가 에러를 일으키는 것을 방지
netflix[netflix["title"].str.contains("Squid Game", case=False, na=False)]
```

**str.split + expand=True — 데이터 분리**
```python
# "Action, Drama, Thriller" → 3개 열로 분리
genres = netflix["listed_in"].str.split(", ", expand=True)
#          0      1       2
# 0   Action  Drama  Thriller
# 1   Drama  Horror     None
```

**stack() — 여러 열 → 단일 열로 쌓기**
```python
# 분리된 여러 열을 행 방향으로 차곡차곡 쌓기
stacked = genres.stack()
# 그 후 value_counts()로 장르별 개수 집계!
genre_counts = stacked.value_counts()
```

### 3-7. 피처 엔지니어링 (Feature Engineering) ⭐⭐

> 강사님: **"기존에 존재하는 변수(컬럼)를 활용하여 분석 목적에 맞는 새로운 정보를 추가로 생성하는 과정!"**

```python
# .map() 함수로 값 매핑
age_group_dic = {
    "TV-MA": "성인",
    "TV-14": "청소년",
    "TV-PG": "전체관람",
    "R": "성인",
    "PG-13": "청소년"
}

# 기존 rating 컬럼 → 새로운 age_group 컬럼 생성
netflix["age_group"] = netflix["rating"].map(age_group_dic)
print(netflix[["title", "rating", "age_group"]])
#      title rating age_group
# 0  오징어게임  TV-MA        성인
# 1  기묘한이야기  TV-14      청소년

# 전처리 데이터 저장
# netflix.to_csv("netflix_processed.csv", index=False, encoding="utf-8")
```

> 💡 **Pandas 핵심 정리**:
> - 결측치 처리: `isna().sum()` → `fillna()` / `dropna()` ⭐
> - 필터링: 마스크 방식 + `query()` ⭐
> - 열 추출: 대괄호 두 개 `[[]]` ⭐
> - `inplace=True` 옵션 반드시 기억!
> - `groupby()` + 집계 함수 조합

---

## 📖 Part 4. 시각화 & 프로젝트 (6월 2일, 4분)

### 4-1. Matplotlib — 파이 차트 (Pie Chart) ⭐

> 넷플릭스 데이터에서 type(Movie vs TV Show) 비율을 시각화!

```python
import matplotlib.pyplot as plt

type_counts = netflix["type"].value_counts()

fig, ax = plt.subplots(figsize=(8, 6))

ax.pie(
    type_counts.values,           # 데이터 값
    labels=type_counts.index,     # 라벨
    autopct='%0.f%%',             # 비율 표시 (소수점 없이) ⭐
    startangle=90,                # 시작 각도 ⭐
    explode=(0.05, 0.05),         # 조각 간격 띄우기 ⭐
    colors=["#FF6B6B", "#4ECDC4"],  # 색상 지정
    shadow=True                   # 그림자 효과 ⭐
)

ax.set_title("넷플릭스 콘텐츠 타입 비율")
plt.suptitle("Netflix Content Analysis", fontsize=16, fontweight="bold")  # 큰 제목
plt.show()
```

> 💡 **주요 속성 정리**:
> - `autopct`: 비율 표시 형식
> - `startangle`: 시작 각도
> - `explode`: 조각 간격
> - `shadow`: 그림자 효과
> - `suptitle()`: 더 큰 제목 추가

### 4-2. Seaborn — 수평 막대 그래프 (Bar Plot) ⭐

> Matplotlib보다 조금 더 세련된 디자인을 제공하는 Seaborn!

```python
import seaborn as sns

# 장르별 개수 데이터 준비
genre_counts = stacked.value_counts()

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(
    x=genre_counts.values,     # x축: 개수
    y=genre_counts.index,      # y축: 장르 이름
    hue=genre_counts.index,    # 막대마다 다른 색상 ⭐
    palette="RdGy",            # 컬러 테마 ⭐
    ax=ax
)

ax.set_xlabel("Count")
ax.set_ylabel("Genre")
ax.set_title("장르별 콘텐츠 수")
plt.show()
```

> 💡 **Seaborn 주요 속성**:
> - `hue`: 막대마다 다른 색상 적용
> - `palette`: 컬러 테마 ('RdGy', 'coolwarm' 등)
> - `figsize=(12, 6)`: 가로로 긴 차트

### 4-3. 그래프 선택 가이드

```
🥧 파이 차트 (Matplotlib) → 비율 보기 (전체 중 각 부분의 占比)
📊 막대 그래프 (Seaborn)  → 범주 간 비교 (순위, 개수 등)
📈 선 그래프               → 추이/트렌드 보기
🌡️ 히트맵                 → 상관관계 보기
📦 박스플롯               → 분포 + 이상치 확인

Matplotlib: 기본 시각화 (세밀한 제어 가능)
Seaborn: 세련된 디자인 (통계 시각화에 강점)
```

---

## 🎯 핵심 요약 (딱 5줄)

1. **파이썬**: 리스트 컴프리헨션 ⭐ = `[표현식 for 변수 in 범위 if 조건]` — 가장 중요한 문법!

2. **NumPy**: 원소별 연산 + 마스크 필터링 ⭐ — `data[data > 30]` 으로 조건에 맞는 데이터만 쏙!

3. **Pandas**: 결측치 처리 ⭐ (`isna().sum()` → `fillna()`/`dropna()`) + 필터링 ⭐ (`query()`) + 열 추출 `[[]]` ⭐

4. **Pandas 옵션**: `inplace=True` 없으면 원본 변경 안 됨! `subset`으로 특정 열 지정 삭제!

5. **시각화**: Matplotlib 파이차트 (`autopct`, `explode`, `startangle`) + Seaborn 막대그래프 (`hue`, `palette`)

---

## 📝 시험 출제 포인트 체크리스트

> 강사님이 강조한 것들 중 시험에 나올 가능성 높은 것들!

- [ ] **리스트 컴프리헨션** — 문법 구조, if 조건 추가
- [ ] **조건문 순서** — 작은 범위 → 큰 범위 (반대로 하면 에러!)
- [ ] **arange vs linspace** — 간격 기준 vs 개수 기준
- [ ] **마스크 필터링** — `data[condition]` 패턴
- [ ] **딕셔너리 → DataFrame** — 키=컬럼명, 값=데이터
- [ ] **결측치 처리** — `isna().sum()`, `fillna()`, `dropna()`
- [ ] **inplace=True** — 원본 반영 옵션
- [ ] **열 추출** — `df["col"]` vs `df[["col"]]` 차이
- [ ] **query()** — SQL처럼 필터링
- [ ] **groupby()** — 그룹별 집계
- [ ] **대괄호 두 개** `[[]]` — DataFrame 형태로 추출
- [ ] **파이차트 속성** — `autopct`, `startangle`, `explode`
- [ ] **Seaborn hue, palette** — 색상 다르게, 컬러 테마

---

## ❓ 예상 질문 & 답변

**Q1. arange와 linspace의 차이는?**
> arange는 "간격" 기준 (0, 2, 4, 6...), linspace는 "개수" 기준 (0~10을 5개로 나눠!). 시험에 나올 수 있어!

**Q2. 결측치 처리 순서는?**
> 1단계: `isna().sum()`으로 결측치 파악 → 2단계: 비율에 따라 `fillna()` 또는 `dropna()` 선택 → 3단계: `inplace=True`로 원본 반영!

**Q3. df["col"]과 df[["col"]]의 차이는?**
> `df["col"]`은 Series(1차원), `df[["col"]]`은 DataFrame(2차원, 표 형태). 강사님이 "반드시 대괄호 두 개 사용"이라고 강조했어!

**Q4. query() 함수 왜 써?**
> 마스크 방식보다 직관적! SQL의 WHERE 조건절처럼 쓸 수 있어. `df.query("age > 20 and score > 80")` 이렇게!

---

## 🏁 마무리

> 오늘 발표 여기까지야!
>
> 5월 27일부터 6월 2일까지의 수업 내용을 전부 정리했어.
> 강사님이 **중요하다고 강조한 것들**은 ⭐ 표시 해놓았으니까 특히 집중해서 봐!
>
> 그리고 모든 코드는 **PY 폴더**에 정리해놨어:
> - `01_python_basics.py` — 파이썬 기초 (리스트 컴프리헨션 포함)
> - `02_numpy_basics.py` — NumPy 핵심 (마스크 필터링 포함)
> - `03_pandas_basics.py` — Pandas 핵심 (결측치, 필터링, groupby)
> - `04_visualization.py` — Matplotlib + Seaborn 시각화
>
> 주석이 상세하게 달려있으니까 복습할 때 참고해!
>
> 시험 잘 보자 여러분! 화이팅! 🎉

---

*발표 대본 v1.0 | 작성일: 2026-06-22 | 작성: 규연 💙*
*자료 출처: NotebookLM "시험공부 노트북" (5/27~6/2 수업, 10개 소스) 기반*
*⭐ 표시: 강사님이 중요하다고 강조한 내용*
*코드 파일: PY 폴더 참조*
