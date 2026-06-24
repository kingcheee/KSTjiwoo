# 🎤 6/11 수업 발표 대본 (30분) — 로지스틱 회귀 & 앙상블 & K-Means

---

## 📌 오프닝 (3분)

안녕! 오늘은 **6월 11일 수업** 내용을 정리해볼 거야.

이번 수업은 **분류 모델의 핵심**을 다뤘어. 로지스틱 회귀부터 앙상블(랜덤 포레스트, 그레디언트 부스팅), 그리고 비지도 학습 K-Means까지!

오늘 발표 한 줄 요약하면?

**"확률로 분류하고, 집단 지성으로 성능 끌어올리고, 정답 없이 그룹 찾기!"** 🔥

그럼 시작해보자!

---

## Part 1. 데이터 분할 & 하이퍼파라미터 튜닝 (5분)

### 🤔 왜 배우는가?

모델을 만들 때 **Train/Test 분리만으로는 부족해**. 하이퍼파라미터 튜닝을 하려면 중간 검증이 필요해!

### 핵심 개념

**데이터 3분할** ⭐ (교수님 강조)
- **Train (훈련)**: 모델이 학습하는 데이터
- **Validation (검증)**: 하이퍼파라미터 튜닝용 중간 모의고사
- **Test (테스트)**: 최종 성능 평가
- 💡 **비유**: 수능 전 실력을 점검하는 **모의고사**!

**교차 검증 (Cross Validation)**
- 데이터를 K개로 나눠서 번갈아가며 검증
- 적은 데이터로도 다양한 조합으로 평가 가능

**GridSearchCV vs RandomSearchCV**
- **GridSearchCV**: 모든 조합을 다 계산 (정확 but 느림)
- **RandomSearchCV**: 랜덤하게 조합 탐색 (빠르지만 최적 보장 못 함)

### 핵심 코드

```python
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score

# ⭐ 3분할: Train / Validation / Test
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5)

# GridSearchCV로 최적 하이퍼파라미터 찾기
from sklearn.ensemble import RandomForestClassifier
params = {'n_estimators': [50, 100, 200], 'max_depth': [3, 5, 10]}
grid = GridSearchCV(RandomForestClassifier(), params, cv=5)
grid.fit(X_train, y_train)
print(f'최적 파라미터: {grid.best_params_}')
```

### ⭐ 교수님 강조 포인트
> "하이퍼파라미터 튜닝을 하려면 반드시 Validation 데이터셋이 필요하다!"

---

## Part 2. 로지스틱 회귀 (Logistic Regression) (8분)

### 🤔 왜 배우는가?

선형회귀는 **숫자 예측**이잖아. 이번엔 **분류(카테고리 예측)**를 해보자!

### 핵심 개념

**시그모이드 함수 (Sigmoid)** ⭐⭐
- 💡 **비유**: 0점 아니면 100점이 아닌, **부드러운 확률 점수표**!
- 직선 대신 S자 곡선으로 0~1 사이 **확률값**을 반환
- 미분 가능 → 성능 향상 → **딥러닝에서도 동일하게 적용!**

**로지스틱 회귀** ⭐
- 💡 **비유**: O/X 퀴즈의 달인!
- 시그모이드 함수로 확률을 구하고, 임계값(0.5)으로 분류
- 교수님: "0과 1 사이의 **확률**을 리턴한다는 점이 매우 중요!"

**임계값(Threshold) & 트레이드오프**
- 임계값을 0.5 → 0.3으로 낮추면: 재현율 ↑, 정밀도 ↓
- 임계값을 0.5 → 0.7로 높이면: 정밀도 ↑, 재현율 ↓
- **ROC 곡선**: 성능을 시각적으로 한눈에 파악!

### 실제 활용
- 의료 진단: 검사 수치로 암 여부 예측
- 마케팅: 고객 데이터로 구매 여부 예측
- 타이타닉: 승객 데이터로 생존 여부 예측

### 핵심 코드

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# 로지스틱 회귀
lr = LogisticRegression(solver='lbfgs', random_state=0)
lr.fit(X_train, y_train)

# ⭐ 확률 예측 (0~1 사이 값)
y_proba = lr.predict_proba(X_test)[:, 1]

# ROC 곡선
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'ROC (AUC = {roc_auc:.2f})')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()
```

### ⭐ 교수님 강조 포인트
> "시그모이드 함수가 미분이 가능하고 확률을 리턴한다는 사실이 매우 중요! 나중에 딥러닝에서도 동일하게 적용되는 내용!"

> "임계값을 어떻게 설정하느냐에 따라 정밀도와 재현율이 반비례하게 변해요!"

---

## Part 3. 앙상블 학습 (Ensemble Learning) (10분)

### 🤔 왜 배우는가?

하나의 모델보다 **여러 모델을 합치면** 더 좋아지지 않을까? 그게 앙상블!

### 핵심 개념

**랜덤 포레스트 (Random Forest)** ⭐
- 💡 **비유**: 다수결로 정답을 찾는 **집단 지성**!
- 수백 개의 결정 트리를 만들어서 다수결 투표
- 개별 트리가 잘못되어도 전체 숲이 보완
- 교수님: **"집단 지성"이라는 단어로 수차례 반복 강조!**

**그레디언트 부스팅 (Gradient Boosting)** ⭐⭐
- 💡 **비유**: 퀀 문제만 계속 파고드는 **오답 노트**!
- 이전 모델의 **오차(잔차)**를 다음 모델이 순차적으로 보정
- 잔차가 0이 될 때까지 점진적으로 강화
- 교수님: **"딥러닝 제외하고 현존 머신러닝 중 성능이 가장 좋은 끝판왕!"**

### 실제 활용

| 모델 | 활용 |
|---|---|
| 랜덤 포레스트 | 고객 분류, 이미지 분류, 추천 시스템 |
| 그레디언트 부스팅 | 수치 예측, 고성능 예측 모델, 대회용 |

### 핵심 코드

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# ⭐ 랜덤 포레스트 (집단 지성!)
rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf.fit(X_train, y_train)
print(f'랜덤 포레스트 정확도: {rf.score(X_test, y_test):.2f}')

# ⭐ 그레디언트 부스팅 (오답 노트!)
gb = GradientBoostingClassifier(
    n_estimators=100, learning_rate=0.05, max_depth=3, subsample=0.8
)
gb.fit(X_train, y_train)
print(f'그레디언트 부스팅 정확도: {gb.score(X_test, y_test):.2f}')
```

### ⭐ 교수님 강조 포인트
> "랜덤 포레스트는 **집단 지성**이에요. 개별 트리의 실수도 집단의 힘으로 보완해요!"

> "그레디언트 부스팅은 **잔차를 0이 될 때까지 보정**해 나가는 방식! 딥러닝 제외하고 성능이 가장 좋은 끝판왕!"

---

## Part 4. 데이터 전처리 & K-Means 군집화 (4 min)

### 핵심 개념

**데이터 전처리 (타이타닉 실습)**
- 결측치 처리: 중간값으로 채우기
- 로그 변환: 쏠린 데이터를 완만하게 만들기
- 원핫 인코딩: 카테고리 데이터를 0과 1로 변환

**K-Means 군집화** ⭐
- 💡 **비유**: 끼리끼리 모이는 **동아리 짜기**!
- 정답(라벨)이 없는 **비지도 학습**
- 중심점(K개) → 가까운 데이터 묶기 → 중심점 이동 → 반복
- **K값 선택이 매우 중요!**

### 실제 활용
- 고객 세그먼테이션: 성향별 그룹 분류
- 이상 탐지: 신용카드 부정 사용 탐지
- 뉴스 기사 자동 분류

### 핵심 코드

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# 가상 데이터 생성
X, y = make_blobs(n_samples=1500, centers=3, random_state=42)

# K-Means (K=3)
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)
labels = kmeans.labels_

# 시각화
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
            c='red', marker='x', s=200)
plt.show()
```

### ⭐ 교수님 강조 포인트
> "K-Means는 **정답이 없는 비지도 학습**이에요! 유사한 특징을 가진 데이터들끼리 거리 기반으로 스스로 그룹을 묶어요!"

> "분류할 그룹의 개수인 **K값을 몇 개로 설정하느냐가 굉장히 중요**해요!"

---

## 📋 핵심 요약 (2분)

1. **로지스틱 회귀** = 시그모이드 함수로 확률 기반 분류!
2. **랜덤 포레스트** = 집단 지성으로 다수결 분류!
3. **그레디언트 부스팅** = 오답 노트로 순차 보정!
4. **K-Means** = 정답 없이 비슷한 것끼리 그룹 짜기!

---

## ❓ 예상 Q&A

**Q1. 시그모이드 함수가 왜 중요한가?**
→ 미분이 가능하고 0~1 사이 확률을 리턴! 딥러닝에서도 동일하게 적용!

**Q2. 랜덤 포레스트 vs 그레디언트 부스팅 차이?**
→ 랜덤 포레스트는 병렬 다수결(집단 지성), 그레디언트 부스팅은 순차 보정(오답 노트)!

**Q3. K-Means에서 K값을 잘못 선택하면?**
→ 그룹이 너무 많거나 적어서 의미 없는 분류가 됨. 엘보우 기법으로 최적 K를 찾아야 해!

**Q4. 데이터 분석가에게 가장 중요한 앙상블은?**
→ 그레디언트 부스팅! 딥러닝 제외하고 성능이 가장 좋은 끝판왕!

---

*발표 대본 v1.0 | 규연이가 만들었당 🐣*
