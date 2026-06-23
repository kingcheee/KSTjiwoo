# 🎤 6/19 PyTorch 딥러닝 수업 발표 대본 (20분)

---

## 📌 오프닝 (2분)

안녕! 오늘은 6월 19일 수업 내용을 정리해볼 거야.

오늘 수업 한 줄 요약하면?

**"PyTorch로 딥러닝 모델 만들어서 학습시키고, 결과 확인하기"** 🔥

총 4시간 동안 9시, 10시, 13시, 17시 이렇게 나눠서 진행했어.
- 9시: 파이토치 기초 + 모델 구축
- 10시: 학습 루프 실습
- 13시: 결과 시각화 + 과적합 분석
- 17시: 회귀 모델 실습

그럼 시작해보자!

---

## Part 1. 데이터 준비하기 (3분)

### 🤔 왜 이걸 배우는데?

너가 핸드폰으로 사진 찍으면 자동으로 "강아지", "고양이" 이렇게 분류되잖아?
그게 다 **딥러닝 모델** 덕분이야. 근데 모델한테 학습시키려면 **데이터를 준비**해야지!

### 핵심 개념

**Tensor** — PyTorch에서 데이터를 다루는 기본 단위야.
일반 숫자 리스트를 PyTorch가 이해할 수 있는 형태로 바꿔주는 거야.
→ 비유하자면: 레고 블록을 조립하기 전에 **규격 맞추는 작업** 🧱

**DataLoader** — 데이터를 배치(Batch) 단위로 묶어서 모델한테 나눠주는 역할.
→ 비유: 도시락 싸는 거! 한 번에 다 먹으면 배부르니까 **적당한 양씩 나눠서** 싸주는 거야 🍱

### 핵심 코드

```python
from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader

# 데이터셋 다운로드 & 텐서 변환
train_data = datasets.FashionMNIST(
    root='data', train=True, download=True, transform=ToTensor()
)
val_data = datasets.FashionMNIST(
    root='data', train=False, download=True, transform=ToTensor()
)

# DataLoader: 배치 크기 32, 훈련 데이터는 섞기
BATCH_SIZE = 32
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False)
```

### ⭐ 포인트
- `shuffle=True` → 훈련 데이터는 섞어야 모델이 **순서 외우는 거 방지**
- `ToTensor()` → 이미지를 PyTorch 텐서로 변환

---

## Part 2. 모델 만들기 — nn.Module (4분)

### 🤔 왜 이걸 배우는데?

딥러닝 모델의 **설계도**를 만드는 거야.
건물 지을 때 설계도 없으면 못 짓잖아? 모델도 마찬가지!

### 핵심 개념

**nn.Module** — PyTorch에서 모델 만들 때 반드시 상속받아야 하는 클래스야.
→ 비유: 자동차 공장의 **기본 설계 도면**. 이걸 베이스로 내 차를 만드는 거 🚗

모델 만드는 **3가지 규칙**:
1. `nn.Module` 상속받기
2. `__init__`에서 레이어 정의하기
3. `forward`에서 데이터 흐름 정의하기

### 핵심 코드

```python
import torch.nn as nn
import torch.nn.functional as F

class SimpleLinearModel_02(nn.Module):
    def __init__(self, input_size, num_classes=10):
        super().__init__()
        # 28x28 = 784 입력 → 200 → 100 → 10개 출력
        self.linear_01 = nn.Linear(input_size*input_size, 200)
        self.linear_02 = nn.Linear(200, 100)
        self.linear_03 = nn.Linear(100, num_classes)

    def forward(self, x):
        x = torch.flatten(x, start_dim=1)  # 이미지를 1차원으로 펴기
        x = F.relu(self.linear_01(x))      # 첫 번째 레이어 + 활성화
        x = F.relu(self.linear_02(x))      # 두 번째 레이어 + 활성화
        output = self.linear_03(x)         # 최종 출력
        return output
```

### ⭐ 포인트
- `nn.Linear` → 선형 변환 (입력 → 출력 연결)
- `F.relu` → 활성화 함수. 음수를 0으로 바꿔주는 역할. **비유: 문 열고 닫기** 🚪 (양수면 통과, 음수면 차단)
- `torch.flatten` → 2D 이미지를 1D 벡터로 평탄화

---

## Part 3. 학습 시키기 — Training Loop (4분)

### 🤔 왜 이걸 배우는데?

모델을 만들었으면 **학습**시켜야지! 이게 딥러닝의 핵심이야.

### 핵심 개념

**학습의 3단계** ⭐ (시험 출제 포인트!)
1. `optimizer.zero_grad()` → 이전 기울기 초기화 (초기화 안 하면 기울기 쌓여서 망함)
2. `loss.backward()` → 역전파. 오차를 바탕으로 각 파라미터의 기울기 계산
3. `optimizer.step()` → 옵티마이저로 가중치 업데이트

→ 비유: 시험 보고 **틀린 문제 분석**해서 **다음에 안 틀리도록** 공부하는 과정 📝

**순전파 vs 역전파**
- 순전파: 입력 → 모델 → 예측값 (앞으로 전파)
- 역전파: 오차 → 기울기 계산 → 가중치 수정 (뒤로 전파)

### 핵심 코드

```python
class Trainer:
    def train_epoch(self, epoch):
        self.model.train()  # 학습 모드!
        total_loss = 0

        for inputs, targets in self.train_loader:
            # 순전파
            outputs = self.model(inputs)
            loss = self.loss_fn(outputs, targets)

            # 역전파 & 업데이트
            self.optimizer.zero_grad()  # 기울기 초기화
            loss.backward()             # 역전파
            self.optimizer.step()       # 가중치 업데이트

            total_loss += loss.item()

    def validate_epoch(self, epoch):
        self.model.eval()  # 평가 모드!
        with torch.no_grad():  # 기울기 계산 비활성화
            for inputs, targets in self.val_loader:
                outputs = self.model(inputs)
                loss = self.loss_fn(outputs, targets)
```

### ⭐ 포인트
- `model.train()` → 학습 모드 (Dropout 등 활성화)
- `model.eval()` → 평가 모드 (Dropout 비활성화, 일관된 결과)
- `torch.no_grad()` → 평가 시 기울기 계산 안 함 → **메모리 절약 + 속도 향상**

---

## Part 4. 결과 보기 — 시각화 & 과적합 (3분)

### 🤔 왜 이걸 배우는데?

학습이 잘 됐는지 **눈으로 확인**해야지!
그래프 안 보면 "모델이 공부를 하는 건지 노는 건지" 모름 😂

### 핵심 개념

**과적합 (Overfitting)** ⭐
- 훈련 데이터는 잘 맞추는데, 새로운 데이터는 못 맞추는 현상
- 비유: **시험 문제집만 외워서** 실제 시험에서 새 문제 나오면 못 푸는 거 📖

**판단 방법:**
- 훈련 손실 ↓ + 검증 손실 ↑ = 과적합 의심!
- 훈련 정확도 ↑ + 검증 정확도 정체/↓ = 과적합!

### 핵심 코드

```python
import matplotlib.pyplot as plt

def show_history(history, metric='acc'):
    if metric == 'loss':
        train_key, val_key = 'train_loss', 'val_loss'
    else:
        train_key, val_key = 'train_acc', 'val_acc'

    plt.plot(history[train_key], label='train')
    plt.plot(history[val_key], label='valid')
    plt.legend()
    plt.show()

# 사용
show_history(history, metric='loss')  # 손실 그래프
show_history(history, metric='acc')   # 정확도 그래프
```

### ⭐ 포인트
- 그래프에서 **train과 valid가 벌어지면** 과적합 신호!
- 이때는 데이터 늘리기, Dropout 추가, 에폭 줄이기 등을 시도

---

## Part 5. 회귀 모델 — BostonNet (3분)

### 🤔 왜 이걸 배우는데?

지금까지는 **분류** (옷 종류 맞추기) 했잖아.
이번엔 **회귀** — 연속된 숫자 맞추기 (집 값 예측) 🏠

### 핵심 개념

**분류 vs 회귀**
| | 분류 (Classification) | 회귀 (Regression) |
|---|---|---|
| 목적 | 범주 예측 | 숫자 예측 |
| 예시 | 옷 종류 (10개) | 집 가격 (연속값) |
| 출력 | 클래스 개수만큼 | 1개 |
| 손실함수 | CrossEntropyLoss | MSELoss |

**데이터 스케일링 (StandardScaler)** ⭐
- 각 피처(특성)의 값 범위가 제각각일 때 맞춰주는 작업
- 비유: 시험 점수를 100점 만점으로 **통일**하는 거 (어느 과목은 50점 만점, 어느 과목은 100점 만점이면 공정하지 않잖아)

### 핵심 코드

```python
from sklearn.preprocessing import StandardScaler

# 데이터 스케일링
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # 훈련 데이터: fit + transform
X_test = scaler.transform(X_test)         # 테스트 데이터: transform만!

# 회귀 모델
class BostonNet(nn.Module):
    def __init__(self, in_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)  # 출력 1개 (집 값)
        )

    def forward(self, x):
        return self.net(x)

# 손실 함수: MSELoss (평균 제곱 오차)
criterion = nn.MSELoss()
```

### ⭐ 포인트
- `fit_transform`은 훈련 데이터만! 테스트 데이터는 `transform`만
- 회귀 평가 지표: **RMSE** (오차), **R² Score** (설명력)

---

## 📋 핵심 요약 (1분)

오늘 배운 거 딱 3줄 요약! ✅

1. **nn.Module**로 모델 만들고, **DataLoader**로 데이터 준비하기
2. **학습 3단계**: zero_grad → backward → step (이거 외워!)
3. **model.train()/eval()** 구분하고, **torch.no_grad()**로 평가 효율 높이기

---

## ❓ 예상 Q&A

**Q1. 오늘 배운 내용을 한 줄로 설명하면?**
→ PyTorch로 딥러닝 모델을 만들고 학습시키는 전체 파이프라인을 배웠다!

**Q2. 이 개념이 없으면 어떤 불편함이 생길까?**
→ 모델을 아무리 복잡하게 만들어도 학습 루프를 못 짜면 그냥 빈 껍데기. 데이터 스케일링 안 하면 학습이 불안정해서 좋은 결과 못 얻어 😱

**Q3. 내 삶에 어떻게 적용할 수 있을까?**
→ 이미지 분류, 가격 예측, 추천 시스템 등 요즘 AI 서비스의 기본 원리야. 이걸 베이스로 CNN, RNN, Transformer까지 나아갈 수 있어! 🚀

---

## 🔜 다음 주 예고

다음 주부터는 본격적으로:
- **CNN** (합성곱 신경망) — 이미지 처리의 왕 👑
- **RNN** (순환 신경망) — 시계열, 텍스트 처리
- **Transformer** — 요즘 대세! GPT의 기반
- **YOLO** — 실시간 객체 탐지
- **Agent** — AI가 스스로 행동하는 에이전트

기대되지? ㅎㅎ 오늘 배운 게 모든 걸 위한 **기초 체력**이니까 열심히 복습해두자! 💪

---

*발표 대본 v1.0 | 규연이가 만들었당 🐣*
