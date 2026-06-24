# 🎤 6/12 수업 발표 대본 (30분) — 앙상블 복습 & K-Means & PCA

---

## 📌 오프닝 (3분)

안녕! 오늘은 **6월 12일 수업** 내용을 정리해볼 거야.

이번 수업은 **앙상블 복습 + K-Means 군집화 + PCA 차원 축소**까지, 머신러닝의 핵심 기법들을 집중적으로 다뤘어!

오늘 발표 한 줄 요약하면?

**"집단 지성으로 예측하고, 정답 없이 그룹 짜고, 차원을 줄여 핵심 추출하기!"** 🔥

그럼 시작해보자!

---

## Part 1. 앙상블 모델 복습 (8분)

### 🤔 왜 배우는가?

하나의 모델보다 **여러 모델을 합치면** 더 좋아지지 않을까? 그게 앙상블!

### 핵심 개념

**랜덤 포레스트 (Random Forest)** ⭐
- 💡 **비유**: 100명이 모여 다수결로 투표하는 **집단 지성**!
- 나무 100그루를 심어서 각각 학습시키고 다수결로 최종 결정
- 한 그루가 잘못되어도 전체 숲이 보완

**그레디언트 부스팅 (Gradient Boosting)** ⭐⭐
- 💡 **비유**: 친구의 실수를 다음 친구가 계속 고쳐주는 **이어달리기**!
- 첫 번째 모델의 오차(잔차)를 두 번째 모델이 보정
- 세 번째 모델이 두 번째의 오차를 또 보정 → 잔차가 0이 될 때까지!
- 교수님: **"딥러닝 제외하고 현존 머신러닝 중 성능이 가장 좋은 끝판왕!"**

**하이퍼파라미터 튜닝 (GridSearchCV)**
- 앙상블 모델도 `GridSearchCV`로 최적 파라미터 찾기 가능!
- `n_estimators`, `max_depth`, `learning_rate` 등을 조합해서 최적값 탐색

### 실제 활용
- 고객 이탈 예측, 구매 예측, 수치 예측 등 거의 모든 분류/회귀 문제
- 팀 프로젝트 시 **1인 1모델 정책**: 각자 다른 모델을 돌려서 성능 비교!

### 핵심 코드

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV

# ⭐ 랜덤 포레스트
rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf.fit(X_train, y_train)

# ⭐ 그레디언트 부스팅
gb = GradientBoostingClassifier(
    n_estimators=100, learning_rate=0.05, max_depth=3, subsample=0.8
)
gb.fit(X_train, y_train)

# ⭐ GridSearchCV로 하이퍼파라미터 튜닝
params = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 10],
    'learning_rate': [0.01, 0.05, 0.1]
}
grid = GridSearchCV(GradientBoostingClassifier(), params, cv=5, scoring='accuracy')
grid.fit(X_train, y_train)
print(f'최적 파라미터: {grid.best_params_}')
print(f'최적 정확도: {grid.best_score_:.2f}')
```

### ⭐ 교수님 강조 포인트
> "그레디언트 부스팅은 딥러닝 제외하고 성능이 가장 좋은 끝판왕!"

> "팀 프로젝트 때 1인 1모델 정책을 추천해요. 각자 다른 모델을 돌려서 성능을 비교하면 설득력 있는 보고서를 만들 수 있어요!"

---

## Part 2. K-Means 군집화 (Clustering) (8 min)

### 🤔 왜 배우는가?

지금까지는 **정답이 있는** 데이터로 학습했잖아. 이번엔 **정답 없이** 데이터를 그룹화하는 방법!

### 핵심 개념

**K-Means 군집화** ⭐⭐
- 💡 **비유**: 운동장에서 끼리끼리 그룹 만들기 놀이!
- 정답(라벨)이 없는 **비지도 학습**
- 교수님: **"어렸을 때 게임하는 거랑 거의 수준이 비슷해요!"**

**작동 원리**
1. 임의의 중심점(Centroid) K개를 랜덤으로 배치
2. 각 데이터를 가장 가까운 중심점의 그룹에 할당
3. 그룹의 진짜 중심으로 중심점을 이동
4. 중심점이 더 이상 이동하지 않을 때까지 반복!

**K값 선택의 중요성** ⭐
- K가 너무 작으면: 의미 없는 분류
- K가 너무 크면: 과적합
- **엘보우 기법(Elbow Method)**으로 최적 K를 찾아야 함!

### 실제 활용
- 고객 세그먼테이션: 성향별 그룹 분류
- 이상 탐지: 신용카드 부정 사용 탐지
- 뉴스 기사 자동 분류

### 핵심 코드

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# 가상 데이터 생성
X, y = make_blobs(n_samples=1500, centers=3, random_state=42)

# K-Means (K=3)
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)
labels = kmeans.labels_

# 시각화
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.5)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            c='red', marker='X', s=200, label='Centroids')
plt.legend()
plt.show()
```

### ⭐ 교수님 강조 포인트
> "K-Means는 **정답이 없는 비지도 학습**이에요! 유사한 특징을 가진 데이터들끼리 거리 기반으로 스스로 그룹을 묶어요!"

> "분류할 그룹의 개수인 **K값을 몇 개로 설정하느냐가 굉장히 중요**해요!"

---

## Part 3. PCA (주성분 분석) & 차원 축소 (7 min)

### 🤔 왜 배우는가?

데이터의 특징(차원)이 너무 많으면 **모델이 느려지고 과적합**이 발생해. 차원을 줄이면서도 핵심 정보는 유지하는 방법!

### 핵심 개념

**차원의 저주 (Curse of Dimensionality)** ⭐
- 💡 **비유**: 우주가 너무 넓어서 별끼리 부딪히지 않는 현상!
- 차원이 늘어나면 공간이 기하급수적으로 넓어져서 데이터가 텅텅 비게 됨
- 거리의 개념이 희미해지고, 정확도가 크게 떨어짐

**PCA (주성분 분석)** ⭐⭐
- 💡 **비유**: 오렌지 27개를 짜서 만든 **엑기스 주스**!
- 27개의 오렌지(피처)를 짜서 1~2개의 주스병(주성분)에 담는 것
- 원래 형태는 사라지지만, **핵심 정보량(분산)**은 그대로 유지!
- 교수님: "27개 피처를 2개로 줄였는데도 정확도가 77.5% → 72.5%로 밖에 안 떨어졌어요!"

### 실제 활용
- 피처가 수십~수백 개일 때 전처리 단계로 활용
- 데이터 시각화 (고차원 → 2차원/3차원으로 축소)
- 노이즈 제거 및 모델 학습 속도 향상

### 핵심 코드

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# ⭐ 스케일링 먼저! (PCA는 스케일에 민감)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA로 2차원으로 축소
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# 설명된 분산 비율
print(f'주성분 1이 설명하는 분산: {pca.explained_variance_ratio_[0]:.2%}')
print(f'주성분 2가 설명하는 분산: {pca.explained_variance_ratio_[1]:.2%}')
print(f'총 설명 분산: {sum(pca.explained_variance_ratio_):.2%}')

# 시각화
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', alpha=0.5)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()
```

### ⭐ 교수님 강조 포인트
> "27개 피처를 PCA로 2개로 줄였는데도 정확도가 77.5%에서 72.5%로 밖에 안 떨어졌어요! 이게 PCA의 힘이에요!"

---

## Part 4. 실전 활용 & 미니 프로젝트 (4 min)

### 💡 데이터 분석가가 가장 먼저 흡수해야 할 것

1. **앙상블 모델** → 거의 모든 분류/회귀 문제의 주력 모델
2. **K-Means** → 정답 없는 데이터 탐색, 고객 세그먼테이션
3. **PCA** → 피처가 많을 때 전처리 필수 도구

### 미니 프로젝트 가이드
- 4인 1조, 1박 2일 동안 머신러닝 전 과정 구현
- **1인 1모델 정책**: 각자 다른 모델을 돌려서 성능 비교
- 흐름: 데이터 수집 → EDA → 전처리 → 모델링 → 성능 평가 → 시각화 보고서

### 활용 예시

| 개념 | 활용 |
|---|---|
| 랜덤 포레스트 | 고객 이탈 예측, 구매 예측 |
| 그레디언트 부스팅 | 수치 예측, 고성능 모델 |
| K-Means | 고객 세그먼테이션, 이상 탐지 |
| PCA | 차원 축소, 데이터 시각화, 노이즈 제거 |

---

## 📋 핵심 요약 (2분)

1. **앙상블** = 집단 지성(랜덤 포레스트) + 이어달리기(그레디언트 부스팅)!
2. **K-Means** = 정답 없이 비슷한 것끼리 그룹 짜기!
3. **PCA** = 27개 오렌지를 짜서 2개 주스병에 담는 엑기스 추출!
4. **차원의 저주** = 우주가 너무 넓어서 별끼리 안 부딪히는 현상!

---

## ❓ 예상 Q&A

**Q1. 랜덤 포레스트 vs 그레디언트 부스팅 차이?**
→ 랜덤 포레스트는 병렬 다수결(집단 지성), 그레디언트 부스팅은 순차 보정(이어 달리기)!

**Q2. K-Means에서 K값을 잘못 선택하면?**
→ 그룹이 너무 많거나 적어서 의미 없는 분류. 엘보우 기법으로 최적 K를 찾아야 해!

**Q3. PCA를 쓰면 정보가 손실되지 않나?**
→ 일부 손실은 있지만, 핵심 정보량(분산)은 최대한 보존! 27개 → 2개로 줄여도 정확도 저하는 5% 정도!

**Q4. 팀 프로젝트에서 어떤 모델을 쓰면 좋은가?**
→ 1인 1모델 정책! 로지스틱 회귀, 랜덤 포레스트, 그레디언트 부스팅을 각자 돌려서 성능을 비교하면 설득력 있는 보고서 완성!

---

*발표 대본 v1.0 | 규연이가 만들었당 🐣*
