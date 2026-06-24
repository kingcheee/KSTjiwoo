## 6_19 17시 수업 학습 노트

### 1. 강의 핵심 요약

6_19 17시 수업은 다가오는 딥러닝 커리큘럼(CNN, RNN, Transformer, YOLO, Agent)을 소개하며 다양한 딥러닝 분야에 대한 이해를 넓혔습니다. 이어서 보스턴 주택 가격 데이터셋을 활용하여 MLP 모델을 구축하고 학습하는 실습을 진행하며 데이터 전처리(스케일링), 모델 정의, 학습 및 평가 과정을 상세히 다루었습니다. 강사는 이론과 실습을 병행하여 수강생들이 딥러닝의 실제 적용 가능성과 문제 해결 능력을 키울 수 있도록 지도했습니다.

---

### 2. 화면 연계 타임라인 노트

-   **00:00 - 00:20: 딥러닝의 가능성 및 머신러닝 대체 가능성**
    *   강사는 딥러닝이 기존 머신러닝의 접근 방식을 대체할 수 있으며, 특정 부분에서는 월등하게 높은 점수를 받을 수 있다고 설명합니다. 모든 상황에 해당하지는 않지만, 현재 딥러닝이 많은 분야에서 활용되는 이유라고 강조합니다.
    *   [화면 캡처 타임스탬프: 00:00:00] 코랩 환경 및 강의 화면이 보임.

-   **00:20 - 00:35: 다음 주 스케줄 - CNN, RNN**
    *   **월요일 (CNN):** 다음 주 월요일에는 CNN(Convolutional Neural Network)을 다룰 예정이며, 이때 정규화(Normalization), 드롭아웃(Dropout) 등 기존 머신러닝에서 다루지 못했던 내용들을 보충할 것이라고 언급합니다.
    *   **화요일 (RNN):** RNN(Recurrent Neural Network)을 학습하며 토크나이저(Tokenizer), 임베딩(Embedding)과 같은 자연어 처리(NLP)의 기본 개념들을 다룰 예정입니다. 현재 RNN은 성능 문제로 자연어 처리에는 잘 사용되지 않으며, 주로 시계열 분석에 활용될 것이라고 설명합니다.

-   **00:35 - 00:50: 다음 주 스케줄 - Transformer, YOLO**
    *   **수요일 (Transformer):** 트랜스포머(Transformer) 모델을 다룰 예정입니다. 트랜스포머 알고리즘이 방대하고 무겁기 때문에, 미리 학습된(pre-trained) BERT 모델을 활용할 것입니다. 그 전에 트랜스포머의 아키텍처(구조)를 상세하게 설명하여 이해를 도울 것이라고 말합니다.
    *   **목요일 (YOLO):** 객체 추출/인식과 관련된 YOLO 모델을 다룹니다. 마찬가지로 미리 학습된 YOLO 모델을 활용하여 실습을 진행할 예정입니다.

-   **00:50 - 01:25: 에이전트 및 학습 방향성 설명**
    *   목요일까지 딥러닝 커리큘럼을 마무리하고, 그다음 주에는 에이전트(Agent) 관련 내용을 약 2주간 진행할 것이라고 예고합니다.
    *   데이터 분석 분야의 광범위함을 언급하며, 컴퓨터 비전 등 다양한 영역을 다루는 이유가 적용 가능성(적용해 볼 수 있는 여지)을 높이기 위함이라고 설명합니다.
    *   수동적인 학습이 아닌, 실제 적용해보고 응용해보는 것이 중요하다고 강조합니다.

-   **01:25 - 01:45: 보스턴 주택 가격 예측 실습 시작**
    *   간단한 보스턴 주택 가격 예측 과제에 대한 코드를 미리 제공했음을 언급하며, 실습을 진행합니다.
    *   [화면 캡처 타임스탬프: 00:00:30] 주피터 노트북에 보스턴 주택 가격 예측 코드(`boston_price.csv` 데이터 로드 및 `boston_df.head()` 출력)가 나타남. `import pandas as pd`, `import numpy as np`, `import torch`, `import torch.nn as nn` 등의 라이브러리 임포트가 확인됩니다.

-   **01:45 - 02:30: 데이터 로드 및 초기 탐색**
    *   `boston_df = pd.read_csv('./data/boston_price.csv')` 코드를 통해 `boston_price.csv` 파일을 `boston_df`에 로드합니다.
    *   `boston_df.head()`를 실행하여 데이터셋의 상위 5개 행을 출력하고 구조를 확인합니다. CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT, PRICE 등 총 14개 컬럼과 그 값들을 볼 수 있습니다.
    *   [화면 캡처 타임스탬프: 00:01:00], [화면 캡처 타임스탬프: 00:01:30], [화면 캡처 타임스탬프: 00:02:00], [화면 캡처 타임스탬프: 00:02:30] 지속적으로 데이터 헤드 부분이 화면에 나타남.

-   **02:30 - 03:00: 데이터 형태 확인 및 피처(X), 타겟(y) 분리**
    *   `boston_df.shape`를 통해 데이터셋의 형태가 `(506, 14)`임을 확인합니다 (506개 행, 14개 컬럼).
    *   타겟 변수인 'PRICE'를 제외한 나머지 13개 컬럼을 피처(X)로 설정합니다: `X = boston_df.drop('PRICE', axis=1).values`.
    *   'PRICE' 컬럼을 타겟(y)으로 설정하고, `reshape(-1, 1)`을 사용하여 1차원 배열을 2차원(열 벡터)으로 변환합니다: `y = boston_df['PRICE'].values.reshape(-1, 1)`.
    *   `print(X.shape, y.shape)`를 통해 X는 `(506, 13)`, y는 `(506, 1)` 형태임을 확인합니다.
    *   [화면 캡처 타임스탬프: 00:06:01] `boston_df.shape` 및 `X, y` 분리 코드가 나타남.

-   **03:00 - 03:30: `reshape(-1, 1)` 설명**
    *   강사는 `reshape(-1, 1)`을 사용하는 이유에 대해 질문하고, 1차원 데이터를 2차원 형태로 변환하기 위함임을 설명합니다. 이는 PyTorch 모델의 입력 형식 요구사항을 맞추기 위함입니다.

-   **03:30 - 03:45: 학습/테스트 데이터 분할 (train/test split)**
    *   `sklearn.model_selection`의 `train_test_split`을 사용하여 데이터를 학습(train) 세트와 테스트(test) 세트로 나눕니다.
    *   `test_size=0.2`로 전체 데이터의 20%를 테스트 세트로 할당하고, `random_state=42`로 일관된 분할을 보장합니다.
    *   분할 결과: `X_train.shape`는 `(404, 13)`, `X_test.shape`는 `(102, 13)`, `y_train.shape`는 `(404, 1)`, `y_test.shape`는 `(102, 1)`임을 확인합니다.
    *   [화면 캡처 타임스탬프: 00:09:02] `train_test_split` 코드가 보임.

-   **03:45 - 04:00: 데이터 스케일링 (StandardScaler)**
    *   피처(X) 값들의 스케일이 제각각("들쭉날쭉")이므로, `sklearn.preprocessing`의 `StandardScaler`를 사용하여 데이터를 표준화합니다.
    *   `X_train`에 대해 `scaler.fit_transform()`을 적용하여 학습 데이터의 평균과 표준편차로 스케일링하고, `X_test`에는 학습 데이터의 `scaler`를 사용하여 `scaler.transform()`만 적용합니다.
    *   [화면 캡처 타임스탬프: 00:09:02] `StandardScaler` 코드가 보임.

-   **04:00 - 04:15: 타겟(y) 스케일링 여부 논의**
    *   강사는 X 값들이 들쭉날쭉하여 스케일링이 필요함을 설명하고, y 값(PRICE)도 스케일링을 해야 하는지에 대해 질문합니다. 이 예제에서는 y를 스케일링하지 않지만, 필요한 경우 y도 스케일링할 수 있음을 언급합니다.

-   **04:15 - 04:45: 텐서 변환 및 MLP 모델 정의**
    *   스케일링된 NumPy 배열 데이터를 PyTorch 모델에 입력하기 위해 `torch.FloatTensor()`를 사용하여 텐서(Tensor)로 변환합니다 (`X_train_t`, `y_train_t`, `X_test_t`, `y_test_t`).
    *   간단한 MLP(Multi-Layer Perceptron) 모델인 `BostonNet` 클래스를 정의합니다.
        *   `nn.Module`을 상속받아 PyTorch 모델의 기본 구조를 따릅니다.
        *   `__init__` 메서드에서 `nn.Sequential`을 사용하여 여러 레이어를 순차적으로 구성합니다:
            *   입력 레이어 (`nn.Linear(in_dim, 64)`)
            *   활성화 함수 (`nn.ReLU()`)
            *   은닉 레이어 (`nn.Linear(64, 32)`)
            *   활성화 함수 (`nn.ReLU()`)
            *   출력 레이어 (`nn.Linear(32, 1)`)
        *   `forward` 메서드에서는 입력 `x`를 `self.net`에 통과시켜 최종 출력을 반환합니다.
    *   [화면 캡처 타임스탬프: 00:09:32] 텐서 변환 코드와 `BostonNet` 클래스 정의 코드가 보임.

-   **04:45 - 05:15: 모델 인스턴스화, 손실 함수, 옵티마이저 설정**
    *   `model = BostonNet(X_train.shape[1])`을 통해 `BostonNet` 모델 인스턴스를 생성합니다. `X_train.shape[1]`은 입력 피처의 개수(13)를 나타냅니다.
    *   회귀 문제이므로 `nn.MSELoss()`를 손실 함수(criterion)로 설정합니다 (Mean Squared Error).
    *   `torch.optim.Adam(model.parameters(), lr=0.01)`을 사용하여 Adam 옵티마이저를 설정하고, 학습률(learning rate)을 0.01로 지정합니다.
    *   [화면 캡처 타임스탬프: 00:11:33] 모델, 손실 함수, 옵티마이저 설정 코드가 보임.

-   **05:15 - 05:45: 모델 학습 (Training Loop) 및 검증**
    *   총 200 에포크(epochs) 동안 모델을 학습시킵니다.
    *   각 에포크마다:
        *   `model.train()`: 모델을 학습 모드로 설정합니다.
        *   `optimizer.zero_grad()`: 이전 스텝에서 계산된 기울기(gradient)를 초기화합니다.
        *   `pred = model(X_train_t)`: 학습 데이터를 모델에 통과시켜 예측값을 얻습니다.
        *   `loss = criterion(pred, y_train_t)`: 예측값과 실제 타겟값 사이의 손실을 계산합니다.
        *   `loss.backward()`: 역전파를 통해 모델 파라미터에 대한 기울기를 계산합니다.
        *   `optimizer.step()`: 옵티마이저를 사용하여 모델 파라미터를 업데이트합니다.
        *   학습 손실(`train_losses`)을 기록합니다.
        *   `model.eval()`: 모델을 평가 모드로 설정합니다.
        *   `with torch.no_grad()`: 기울기 계산을 비활성화하여 메모리 사용량을 줄이고 연산 속도를 높입니다.
        *   `val_pred = model(X_test_t)`: 검증 데이터를 모델에 통과시켜 예측값을 얻습니다.
        *   `val_loss = criterion(val_pred, y_test_t)`: 검증 손실(`val_losses`)을 계산하고 기록합니다.
        *   20 에포크마다 학습 손실과 검증 손실을 출력하여 학습 진행 상황을 모니터링합니다.
    *   [화면 캡처 타임스탬프: 00:12:33] 학습 루프 코드가 보임.

-   **05:45 - 06:15: 최종 성능 평가 (RMSE, R2 Score)**
    *   학습이 완료된 모델의 최종 성능을 평가합니다.
    *   `model.eval()` 및 `with torch.no_grad()` 상태에서 테스트 데이터(`X_test_t`)를 사용하여 최종 예측값을 얻습니다: `pred = model(X_test_t).numpy()`.
    *   RMSE (Root Mean Squared Error)와 R2 Score를 계산합니다.
    *   `rmse = np.sqrt(mean_squared_error(y_test, pred))`
    *   `r2 = r2_score(y_test, pred)`
    *   최종 RMSE와 R2 Score 값을 출력합니다.
    *   [화면 캡처 타임스탬프: 00:14:34] 성능 평가 코드가 보임.

-   **06:15 - 06:45: 학습/검증 손실 그래프 출력**
    *   `matplotlib.pyplot`을 사용하여 학습 손실(`train_losses`)과 검증 손실(`val_losses`)을 그래프로 시각화합니다.
    *   두 손실 곡선을 한 그래프에 그려 학습 과정에서의 모델 성능 변화를 직관적으로 파악할 수 있도록 합니다. 이를 통해 모델의 과적합(overfitting) 또는 과소적합(underfitting) 여부를 판단할 수 있습니다.
    *   `plt.tight_layout()`과 `plt.show()`를 호출하여 그래프를 최적화하고 화면에 표시합니다.
    *   [화면 캡처 타임스탬프: 00:15:04] 손실 그래프 코드가 보이며, 생성된 `Training & Validation Loss` 그래프가 화면에 나타남.

-   **06:45 - 07:00: 수업 마무리 및 향후 학습 안내**
    *   강사는 이번 실습을 통해 딥러닝 기본 과정을 마무리하고, 다음 주부터는 실제적인 응용 모델들을 다룰 것임을 다시 한번 강조하며 수업을 마칩니다.
    *   [화면 캡처 타임스탬프: 00:16:35] 최종 그래프가 화면에 보임.

---

### 3. 핵심 개념 및 코드/공식 정리

#### 3.1. 필요한 라이브러리 임포트

```python
import pandas as pd
import numpy as np
import torch
import torch.nn as nn # PyTorch 신경망 모듈
from sklearn.model_selection import train_test_split # 데이터 분할
from sklearn.preprocessing import StandardScaler # 데이터 표준화
from sklearn.metrics import r2_score, mean_squared_error # 성능 지표
import matplotlib.pyplot as plt # 그래프 시각화
```

#### 3.2. 데이터 로드 및 전처리

-   **데이터 로드:**
    ```python
    boston_df = pd.read_csv('./data/boston_price.csv')
    boston_df.head()
    # 출력: 데이터셋 상위 5개 행
    boston_df.shape
    # 출력: (506, 14)
    ```

-   **피처(X)와 타겟(y) 분리:**
    -   `boston_df.drop('PRICE', axis=1)`: 'PRICE' 컬럼을 제외한 모든 컬럼을 X (피처)로 사용합니다. `axis=1`은 컬럼 기준 삭제를 의미합니다.
    -   `.values`: Pandas DataFrame을 Numpy 배열로 변환합니다.
    -   `boston_df['PRICE']`: 'PRICE' 컬럼을 y (타겟)으로 사용합니다.
    -   `.reshape(-1, 1)`: 1차원 배열(예: `[1, 2, 3]`)을 2차원 열 벡터(예: `[[1], [2], [3]]`)로 변환합니다. 이는 PyTorch 모델이 일반적으로 2차원 이상(배치 크기, 피처 수)의 입력을 기대하기 때문에 필수적입니다.
    ```python
    X = boston_df.drop('PRICE', axis=1).values
    y = boston_df['PRICE'].values.reshape(-1, 1)
    print(X.shape, y.shape) # (506, 13) (506, 1)
    ```

-   **학습/테스트 데이터 분할:**
    -   `train_test_split(X, y, test_size=0.2, random_state=42)`: 전체 데이터의 20%를 테스트 세트로, 80%를 학습 세트로 분할합니다. `random_state`를 고정하여 항상 동일한 분할 결과를 얻습니다.
    ```python
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # 출력: ((404, 13), (102, 13), (404, 1), (102, 1))
    ```

-   **데이터 스케일링 (StandardScaler):**
    -   `StandardScaler()`: 각 피처의 평균을 0, 표준편차를 1로 조정하여 데이터를 표준 정규 분포에 가깝게 만듭니다. 이는 모델 학습 시 특정 피처의 값 범위가 다른 피처에 비해 너무 커서 모델 학습에 부정적인 영향을 미치는 것을 방지합니다.
    -   `fit_transform(X_train)`: `X_train` 데이터의 평균과 표준편차를 학습(fit)하고, 이를 이용해 `X_train`을 변환(transform)합니다.
    -   `transform(X_test)`: `X_test` 데이터는 `X_train`에서 학습한 평균과 표준편차를 그대로 사용하여 변환합니다. 테스트 데이터는 학습 데이터의 통계치를 따라야 합니다.
    ```python
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    ```

-   **PyTorch 텐서 변환:**
    -   `torch.FloatTensor()`: Numpy 배열을 PyTorch의 FloatTensor 타입으로 변환합니다. 딥러닝 모델은 이 텐서 타입을 입력으로 받습니다.
    ```python
    X_train_t = torch.FloatTensor(X_train)
    y_train_t = torch.FloatTensor(y_train)
    X_test_t = torch.FloatTensor(X_test)
    y_test_t = torch.FloatTensor(y_test)
    ```

#### 3.3. MLP (Multi-Layer Perceptron) 모델 정의

-   **`BostonNet` 클래스:**
    -   `nn.Module`을 상속받아 PyTorch 신경망 모듈로 정의합니다.
    -   `__init__(self, in_dim)`: 모델의 레이어들을 정의하는 생성자입니다.
        -   `super().__init__()`: 부모 클래스(`nn.Module`)의 생성자를 호출합니다.
        -   `self.net = nn.Sequential(...)`: 여러 레이어를 순차적으로 연결하는 컨테이너입니다.
            -   `nn.Linear(in_dim, 64)`: 입력 `in_dim`에서 64개의 뉴런으로 연결되는 선형 레이어입니다.
            -   `nn.ReLU()`: 활성화 함수로 ReLU(Rectified Linear Unit)를 사용합니다. `max(0, x)` 함수로 비선형성을 추가합니다.
            -   `nn.Linear(64, 32)`: 64개의 뉴런에서 32개의 뉴런으로 연결되는 선형 레이어입니다.
            -   `nn.Linear(32, 1)`: 32개의 뉴런에서 1개의 출력 뉴런으로 연결되는 선형 레이어입니다 (주택 가격 예측이므로 최종 출력은 1개).
    -   `forward(self, x)`: 모델의 순전파(forward pass)를 정의하는 메서드입니다. 입력 `x`가 `self.net`에 정의된 레이어들을 순차적으로 통과합니다.
    ```python
    class BostonNet(nn.Module):
        def __init__(self, in_dim):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(in_dim, 64),
                nn.ReLU(),
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Linear(32, 1)
            )

        def forward(self, x):
            return self.net(x)
    ```

#### 3.4. 학습 설정

-   **모델 인스턴스 생성:**
    -   `model = BostonNet(X_train.shape[1])`: `X_train`의 피처 개수(13)를 입력 차원으로 하여 `BostonNet` 모델을 생성합니다.

-   **손실 함수 (Criterion):**
    -   `nn.MSELoss()`: 회귀 문제에서 가장 흔히 사용되는 손실 함수인 평균 제곱 오차(Mean Squared Error)를 계산합니다. `(예측값 - 실제값)^2`의 평균입니다.
    ```python
    criterion = nn.MSELoss()
    ```

-   **옵티마이저 (Optimizer):**
    -   `torch.optim.Adam(model.parameters(), lr=0.01)`: Adam 옵티마이저를 사용합니다. `model.parameters()`는 모델의 모든 학습 가능한 파라미터(가중치와 편향)를 옵티마이저에 전달합니다. `lr=0.01`은 학습률(learning rate)을 0.01로 설정합니다. 학습률은 파라미터 업데이트의 크기를 조절합니다.
    ```python
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    ```

#### 3.5. 모델 학습 및 검증

-   **학습 루프:**
    ```python
    epochs = 200
    train_losses = []
    val_losses = []

    for epoch in range(epochs):
        # --- 학습 단계 ---
        model.train() # 모델을 학습 모드로 설정
        optimizer.zero_grad() # 이전 에포크에서 계산된 기울기 초기화
        pred = model(X_train_t) # 순전파: 예측값 계산
        loss = criterion(pred, y_train_t) # 손실 계산 (MSE)
        loss.backward() # 역전파: 기울기 계산
        optimizer.step() # 파라미터 업데이트
        train_losses.append(loss.item()) # 학습 손실 기록

        # --- 검증 단계 ---
        model.eval() # 모델을 평가 모드로 설정
        with torch.no_grad(): # 기울기 계산 비활성화 (메모리 및 속도 효율)
            val_pred = model(X_test_t) # 검증 데이터로 예측
            val_loss = criterion(val_pred, y_test_t) # 검증 손실 계산
            val_losses.append(val_loss.item()) # 검증 손실 기록

        if (epoch + 1) % 20 == 0: # 20 에포크마다 손실 출력
            print(f"[{epoch + 1:3d}] | Train Loss: {loss.item():.4f} | Val Loss: {val_loss.item():.4f}")
    ```

-   **학습 단계 핵심 요소:**
    -   `model.train()`: 모델의 `Dropout`이나 `BatchNorm`과 같은 레이어가 학습 모드에서 작동하도록 설정합니다.
    -   `optimizer.zero_grad()`: PyTorch는 기본적으로 기울기를 누적하므로, 각 학습 스텝 시작 전에 이전 기울기를 0으로 초기화해야 합니다.
    -   `loss.backward()`: 현재 손실(`loss`)을 기준으로 모델 파라미터에 대한 기울기를 계산합니다.
    -   `optimizer.step()`: 계산된 기울기를 바탕으로 옵티마이저가 모델의 가중치와 편향을 업데이트합니다.

-   **검증 단계 핵심 요소:**
    -   `model.eval()`: 모델의 `Dropout`이나 `BatchNorm`과 같은 레이어가 평가 모드에서 작동하도록 설정합니다 (예: Dropout은 비활성화).
    -   `with torch.no_grad()`: 이 블록 내에서는 텐서에 대한 모든 연산에서 기울기 계산이 비활성화됩니다. 이는 메모리 사용량을 줄이고, 계산 속도를 높여 평가 시 효율적입니다.

#### 3.6. 성능 평가 및 시각화

-   **성능 평가 (RMSE, R2 Score):**
    -   RMSE (Root Mean Squared Error): 예측 오차의 크기를 나타내는 지표입니다. 값이 작을수록 모델의 성능이 좋습니다.
        $\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$
    -   R2 Score (Coefficient of Determination): 모델이 종속 변수(타겟)의 분산을 얼마나 잘 설명하는지 나타내는 지표입니다. 0과 1 사이의 값을 가지며, 1에 가까울수록 모델의 설명력이 높습니다.
    ```python
    model.eval()
    with torch.no_grad():
        pred = model(X_test_t).numpy() # 테스트 데이터 예측, numpy 배열로 변환
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)
    print(f"[최종 성능] RMSE: {rmse:.4f} | R2: {r2:.4f}")
    ```

-   **학습/검증 손실 그래프:**
    -   `matplotlib.pyplot`을 사용하여 학습 손실과 검증 손실의 변화를 시각화합니다. 이 그래프를 통해 모델이 잘 학습되고 있는지, 과적합이 발생하고 있는지 등을 확인할 수 있습니다.
    -   `train_losses`와 `val_losses` 리스트에 저장된 값을 X축(에포크), Y축(손실)으로 하여 선 그래프를 그립니다.
    ```python
    fig, axes = plt.subplots(1, 1, figsize=(8, 5))
    axes.plot(train_losses, label='Train Loss')
    axes.plot(val_losses, label='Val Loss')
    axes.set_xlabel('Epoch')
    axes.set_ylabel('Loss')
    axes.legend() # 범례 표시
    plt.tight_layout() # 그래프 레이아웃 자동 조절
    plt.show() # 그래프 출력
    ```

---

### 4. 학습 퀴즈

1.  본 강의의 보스턴 주택 가격 예측 실습에서 `y = boston_df['PRICE'].values.reshape(-1, 1)` 코드를 통해 타겟 변수 `y`를 1차원에서 2차원 열 벡터로 변환한 이유는 무엇인지 설명하시오.
2.  `StandardScaler`를 사용하여 피처(X)를 스케일링하는 과정에서 `X_train`에는 `fit_transform`을 사용하고 `X_test`에는 `transform`만 사용하는 이유를 설명하시오.
3.  PyTorch 딥러닝 모델의 학습 루프 내에서 `optimizer.zero_grad()`, `loss.backward()`, `optimizer.step()` 세 가지 메서드의 역할과 순서에 대해 설명하시오.