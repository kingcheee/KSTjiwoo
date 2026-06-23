# 🎤 데이터시각화/머신러닝 수업 발표 대본 (20분)

---

## 📌 오프닝 (2분)

안녕! 오늘은 **데이터시각화/머신러닝** 수업 내용을 정리해볼 거야.

이 수업은 6월 2일부터 6월 17일까지 총 6번에 걸쳐 진행됐어.
데이터 전처리부터 시각화, 머신러닝 알고리즘, 그리고 딥러닝 기초까지 아우르는 엄청 알찬 수업이었지!

오늘 발표 한 줄 요약하면?

**"데이터를 다루고, 시각화하고, 머신러닝 모델로 예측하는 전체 파이프라인"** 🔥

그럼 시작해보자!

> 📄 **교수님 강조 포인트 PDF 페이지 가이드**
> - 유클리드 거리: 6월12일.pdf p.67
> - 시그모이드 함수: 6월11일.pdf p.61
> - 선형회귀 y=wx+b: 6월8일.pdf p.16
> - StandardScaler: 6월9일.pdf (Colab 실습)
> - 텐서 중요성: 6월17일.pdf p.20
> - reshape/argmax: 6월17일.pdf (Colab 실습)
> - 밸리데이션 데이터셋: 6월11일.pdf p.52

---

## Part 1. 데이터 전처리 & 시각화 (4분)

### 🤔 왜 이걸 배우는데?

아무리 좋은 모델이 있어도 **데이터가 엉망이면 결과도 엉망**이야.
요리하기 전에 재료를 손질하는 것과 같아! 🧑‍🍳

### 핵심 개념

**결측치 처리** ⭐
- 데이터에 빈 값이 있으면 모델이 학습을 못 해
- `dropna()` → 결측치가 있는 행/열 제거
- `fillna()` → 특정 값으로 채우기
- `replace()` → 특정 값을 다른 값으로 변경

**피처 엔지니어링 (Feature Engineering)** ⭐
- 기존 변수에서 **새로운 정보를 만들어내는** 작업
- 비유: 주어진 재료로 새로운 소스를 만드는 거 🍝
- 예: 넷플릭스 시청 등급을 연령대 그룹으로 변환

**데이터 시각화**
- Matplotlib + Seaborn으로 데이터를 **눈으로 확인**
- 산점도, 파이 차트, 히트맵 등

### 핵심 코드

```python
# 결측치 확인 & 처리
life[main_features].isna().sum()       # 결측치 개수 확인
life.dropna(inplace=True)              # 결측치 행 제거

# 피처 엔지니어링
age_group_dic = {'G': 'All', 'TV-G': 'All', 'TV-Y': 'All'}
netflix['age_group'] = netflix['rating'].map(age_group_dic)

# 데이터 시각화
import matplotlib.pyplot as plt
import seaborn as sns

plt.scatter(x, y)                      # 산점도
plt.pie(data, labels=labels, autopct='%.1f%%', startangle=90)  # 파이 차트
sns.heatmap(cm, annot=True, fmt='d')   # 혼동 행렬 히트맵
```

### ⭐ 교수님 강조 포인트
> "데이터를 이해하는 데 시간을 보내셔야 합니다. 데이터를 불러오고 → 훑어보고 → 결측치 처리하고 → 그다음 학습하는 순서!"

---

## Part 2. 머신러닝 기초 — 선형회귀 & 분류 (4분)

### 🤔 왜 이걸 배우는데?

머신러닝의 **가장 기본**이 되는 알고리즘들이야.
이걸 모르면 딥러닝도 못 해! 기초 체력이라고 생각해 💪

### 핵심 개념

**머신러닝 파이프라인** ⭐
1. 데이터 로드
2. 데이터 파악 (EDA)
3. Train/Test 데이터 분할
4. 모델 학습
5. 평가

**선형회귀 (Linear Regression)** 📄 6월8일.pdf p.16
- `y = wx + b` — 직선으로 데이터 관계 표현
- **W(가중치)**: 기울기, **b(편향)**: 절편 ⭐
- 교수님: **"딥러닝에서도 가장 기본이 되는 알고리즘이에요. W와 B가 의미하는 바와 그래프를 꼭 잘 기억해달라고 부탁했습니다"**

![선형회귀 y=wx+b 슬라이드](C:\Users\sxeyc\Downloads\수업\머신러닝_이미지\선형회귀_y_wx_b_6월8일_p16.png)

**평가 지표**
- **MSE (Mean Squared Error)**: 오차의 제곱 평균 — 작을수록 좋음
- **R² Score (결정계수)**: 1에 가까울수록 좋음

**KNN (K-Nearest Neighbors)** ⭐
- 가장 가까운 K개의 이웃을 보고 다수결로 분류
- 비유: "내 이웃 7명 중 5명이 강아지라고 하면 나도 강아지" 🐶

**로지스틱 회귀 (Logistic Regression)** 📄 6월11일.pdf p.61
- 시그모이드 함수로 0~1 사이 **확률**을 반환
- 교수님: **"시그모이드 함수가 매우 중요하다. 미분이 가능하고 확률을 리턴한다는 사실!"**
- 이진 분류 (0 또는 1) 문제에 사용

![시그모이드 함수 슬라이드](C:\Users\sxeyc\Downloads\수업\머신러닝_이미지\시그모이드_함수_6월11일_p61.png)

### 핵심 코드

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=84)

# 선형회귀
regr = LinearRegression()
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)
print('결정계수: {:.2f}'.format(r2_score(y_test, y_pred)))

# KNN
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors=7, weights='uniform')
clf.fit(X_train, y_train)

# 로지스틱 회귀
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

sc = StandardScaler()
X_train = sc.fit_transform(X_train)  # ⭐ fit_transform
X_test = sc.transform(X_test)         # ⭐ transform만!

lr = LogisticRegression(solver='lbfgs', random_state=0)
lr.fit(X_train, y_train)
y_pred_proba = lr.predict_proba(X_test)  # 확률 예측
```

### ⭐ 교수님 강조 포인트
> **"`StandardScaler` 쓸 때 훈련 데이터에는 `fit_transform()`, 테스트 데이터에는 `transform()`만! 반드시 이렇게 해야 합니다"** 📄 6월9일.pdf

---

## Part 3. 분류 성능 평가 & 앙상블 (4분)

### 🤔 왜 이걸 배우는데?

모델이 "잘 맞춘다"는 걸 **어떻게 수치로 증명**할까?
그리고 **여러 모델을 합치면** 더 좋아지지 않을까?

### 핵심 개념

**혼동 행렬 (Confusion Matrix)** ⭐
- 예측 vs 실제를 표로 정리
- **정밀도 (Precision)**: "내가 양성이라고 한 것 중 진짜 양성 비율"
- **재현율 (Recall)**: "진짜 양성 중 내가 맞춘 비율"
- 둘은 **트레이드오프** 관계! ↑ 하나가 올라가면 ↓ 하나가 내려감

**앙상블 (Ensemble)** ⭐
- 여러 모델의 **집단 지성**으로 성능 UP
- 비유: 한 명의 의사보다 **10명의 의사가 진단**하면 더 정확하지? 👨‍⚕️

**랜덤 포레스트 (Random Forest)**
- 결정 트리를 여러 개 만들어 **다수결 투표**
- 데이터를 **복원 추출** (Bagging)해서 각 트리 학습

**그래디언트 부스팅 (Gradient Boost)** ⭐
- 이전 트리의 **오차(잔차)**를 다음 트리가 순차적으로 보정
- 교수님: "하나의 트리만으로는 부족하니까, 오차를 줄여가면서 학습하는 거예요"

### 핵심 코드

```python
# 랜덤 포레스트
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0)
rf.fit(X_train, y_train)

# 그래디언트 부스팅
from sklearn.ensemble import GradientBoostingClassifier
gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.05, max_depth=3, subsample=0.8)
gb.fit(X_train, y_train)
```

### ⭐ 교수님 강조 포인트
> **"하이퍼파라미터 튜닝을 하려면 반드시 밸리데이션(검증) 데이터셋이 필요하다! 모의고사 치는 것처럼, 테스트 전에 중간 검증하는 거예요"** 📄 6월11일.pdf p.52

![밸리데이션 데이터셋 슬라이드](C:\Users\sxeyc\Downloads\수업\머신러닝_이미지\밸리데이션_데이터셋_6월11일_p52.png)

---

## Part 4. 비지도 학습 & 교차 검증 (3분)

### 🤔 왜 이걸 배우는데?

지금까지는 **정답이 있는** 데이터로 학습했잖아.
이번엔 **정답 없이** 데이터를 그룹화하는 방법!

### 핵심 개념

**K-Means 클러스터링** 📄 6월12일.pdf p.67
- 정답(라벨) 없이 데이터를 **유사도**로 그룹화
- **유클리드 거리**로 데이터 간 거리 계산
- 교수님: **"유클리드 거리 공식은 굉장히 중요하다고 세 번이나 반복했습니다. 나중에 자연어 처리 임베딩에서도 똑같이 나옵니다. 꼭 기억하세요!"**

![유클리드 거리 슬라이드](C:\Users\sxeyc\Downloads\수업\머신러닝_이미지\유클리드_거리_6월12일_p67.png)

**엘보우 기법 (Elbow Method)**
- 최적의 클러스터 개수(K)를 찾는 방법
- 그래프에서 "꺾이는 지점"이 최적 K

**교차 검증 (Cross Validation)** ⭐
- 데이터가 적을 때 훈련 데이터를 **여러 조각**으로 나눠서 반복 학습/검증
- `GridSearchCV`로 최적 하이퍼파라미터 조합 찾기

### 핵심 코드

```python
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer

# 엘보우 기법으로 최적 K 찾기
model = KMeans()
visualizer = KElbowVisualizer(model, k=(2, 10))
visualizer.fit(data)
visualizer.show()

# K-Means
model = KMeans(n_clusters=4)
model.fit(data)
labels = model.labels_

# 교차 검증 + GridSearchCV
from sklearn.model_selection import GridSearchCV
params = {'n_estimators': [50, 100], 'max_depth': [3, 5]}
grid = GridSearchCV(RandomForestClassifier(), params, cv=5)
grid.fit(X_train, y_train)
print('최적 파라미터:', grid.best_params_)
```

---

## Part 5. 딥러닝 기초 — PyTorch 텐서 (3분)

### 🤔 왜 이걸 배우는데?

머신러닝 다음엔 **딥러닝**이야!
딥러닝의 기본 단위인 **텐서**를 이해해야 GPU에서 연산할 수 있어.

### 핵심 개념

**텐서 (Tensor)** 📄 6월17일.pdf p.20
- GPU에서 병렬 연산을 위한 **다차원 배열**
- Numpy 배열과 비슷하지만 **GPU 연산** 가능
- 교수님: **"텐서 환경 이해가 너무너무 중요합니다. 바탕화면에 깔아두고 눈에 익히세요!"**

![텐서 차원축 슬라이드](C:\Users\sxeyc\Downloads\수업\머신러닝_이미지\텐서_차원축_6월17일_p20.png)

**Numpy ↔ 텐서 변환** ⭐
- CPU(Numpy)와 GPU(Tensor)는 **서로 연산이 안 됨**
- 교수님: "둘 간의 데이터 변환 방법을 아는 것이 **굉장히 중요**합니다"

**차원 변환** 📄 6월17일.pdf (Colab 실습)
- `reshape` / `view`: 텐서 형태 변환 — **"정말 많이 사용하니까 꼭 기억하세요!"**
- `dim=0`: 행 방향, `dim=1`: 열 방향 연산
- `argmax`: 가장 큰 값의 **인덱스(위치)** 반환 — **"많이 쓰이니 꼭 기억!"**

### 핵심 코드

```python
import torch
import numpy as np

# 텐서 생성
t = torch.rand(3, 4)           # 0~1 균일 분포
t = torch.randint(0, 10, (3,4)) # 정수 랜덤
t = torch.randn(3, 4)          # 정규 분포

# Numpy ↔ Tensor 변환
arr = np.array([1, 2, 3])
t = torch.from_numpy(arr)      # Numpy → Tensor
arr2 = t.cpu().numpy()         # Tensor → Numpy (GPU에 있으면 cpu() 먼저!)

# 차원 변환
t = torch.arange(12)
t2 = t.reshape(3, 4)           # 형태 변환
t3 = t.unsqueeze(0)            # 차원 추가
t4 = t.squeeze()               # 차원 제거

# dim 이해
t = torch.tensor([[1, 2, 3],
                  [4, 5, 6]])
print(t.sum(dim=0))  # 행 방향 합 → [5, 7, 9]
print(t.sum(dim=1))  # 열 방향 합 → [6, 15]

# argmax
print(t.argmax(dim=1))  # 각 행에서 최대값의 인덱스 → [2, 2]
```

### ⭐ 교수님 강조 포인트
> **"수학 공식 자체를 깊게 파기보다는, 데이터의 흐름(차원 변환)과 각 알고리즘의 원리를 직관적으로 이해하고 암기할 것!"**

---

## 📋 핵심 요약 (1분)

오늘 배운 거 딱 3줄 요약! ✅

1. **데이터 전처리**: 결측치 처리 + 피처 엔지니어링 + 시각화
2. **머신러닝**: 선형회귀 → KNN → 로지스틱 → 앙상블 → K-Means
3. **PyTorch 텐서**: GPU 연산의 기본, reshape/argmax/dim **꼭 외우기!**

---

## ❓ 예상 Q&A

**Q1. 오늘 배운 내용을 한 줄로 설명하면?**
→ 데이터를 전처리하고, 다양한 머신러닝 알고리즘으로 예측하고, 딥러닝을 위한 텐서 기초까지 배웠다!

**Q2. 유클리드 거리가 왜 중요한가?** 📄 6월12일.pdf p.67
→ K-Means에서 데이터 간 거리를 계산하는 기본 공식이고, 나중에 자연어 처리 임베딩에서도 똑같이 나온다. 교수님이 **세 번**이나 강조하셨음!

**Q3. StandardScaler에서 fit_transform과 transform을 구분하는 이유?** 📄 6월9일.pdf
→ 훈련 데이터에서 평균/표준편차를 학습(fit)하고, 테스트 데이터는 그 기준을 그대로 적용(transform)해야 데이터 누수가 발생하지 않는다!

---

## 🔜 다음 수업 예고

다음 시간에는 본격적으로:
- **PyTorch nn.Module**로 딥러닝 모델 만들기
- **학습 루프** 구현 (순전파/역전파)
- **CNN, RNN, Transformer** 등 심화 모델

오늘 배운 텐서가 모든 걸 위한 **기초 체력**이니까 열심히 복습해두자! 💪

---

*발표 대본 v1.0 | 규연이가 만들었당 🐣*
