안녕하세요! 6_18 16시 수업 학습 노트입니다.

---

## 📅 6_18 16시 수업 학습 노트

### 1. 강의 핵심 요약

이번 6_18 16시 수업은 PyTorch를 활용한 간단한 선형 신경망 모델 구축 및 학습 과정을 다룹니다. FashionMNIST 데이터셋을 이용해 DataLoader를 설정하고, 모델의 `__init__` 및 `forward` 메서드 구현을 통해 모델의 구성과 데이터 흐름을 이해합니다. 최종적으로 손실 함수(CrossEntropyLoss)와 옵티마이저(Adam)를 활용하여 모델을 훈련하고 평가하는 기본적인 딥러닝 워크플로우를 실습합니다.

### 2. 화면 연계 타임라인 노트

- **00:00:00 - 00:00:15 (데이터 로딩 및 준비)**
    - `torchvision.datasets.FashionMNIST`를 사용하여 FashionMNIST 데이터셋을 불러옵니다. `root='data'`는 데이터를 저장할 경로를 지정하고, `train=True`는 훈련 데이터, `train=False`는 검증(Validation) 데이터를 가져옵니다. `download=True`로 데이터가 없으면 다운로드하며, `transform=ToTensor()`로 이미지를 텐서 형태로 변환합니다.
    - `train_data`는 60,000개의 이미지와 라벨을, `val_data`는 10,000개의 이미지와 라벨을 포함합니다.
    - 화면 캡처 [00:00:00]에 해당 코드가 명확히 보입니다.

- **00:00:15 - 00:00:40 (데이터셋 크기 확인)**
    - `len(train_data)`를 출력하여 훈련 데이터의 개수가 `60000`임을 확인합니다.
    - `train_data.data.shape`를 출력하여 훈련 데이터의 형태가 `torch.Size([60000, 28, 28])`임을 확인합니다. 이는 6만 개의 28x28 픽셀 흑백 이미지임을 의미합니다.

- **00:00:40 - 00:01:30 (DataLoader 설정)**
    - `BATCH_SIZE = 32`로 배치 크기를 설정합니다.
    - `torch.utils.data.DataLoader`를 사용하여 `train_loader`와 `val_loader`를 생성합니다.
    - `shuffle=True`는 데이터를 에포크마다 섞어주어 모델이 특정 순서에 의존하지 않도록 합니다.
    - `num_workers=4`는 데이터를 로드할 때 4개의 서브프로세스를 사용하여 병렬 처리하여 데이터 로딩 속도를 높입니다.
    - 화면 캡처 [00:00:50]에서 해당 코드를 볼 수 있습니다.

- **00:01:30 - 00:02:00 (첫 번째 배치 데이터 확인)**
    - `images, labels = next(iter(train_loader))` 코드를 사용하여 `train_loader`에서 첫 번째 배치(32개)의 이미지와 라벨을 가져옵니다.
    - `print(images.shape, labels.shape)`를 통해 이미지의 형태가 `torch.Size([32, 1, 28, 28])` (배치 크기, 채널 수, 높이, 너비)이고 라벨의 형태가 `torch.Size([32])` (배치 크기)임을 확인합니다.
    - 화면 캡처 [00:01:41]에서 코드와 실행 결과를 확인할 수 있습니다.

- **00:02:00 - 00:02:40 (모델 정의 - `SimpleLinearModel_01`의 `__init__`)**
    - `nn.Module`을 상속받는 `SimpleLinearModel_01` 클래스를 정의합니다.
    - `__init__` 메서드에서 모델의 구성 요소를 정의합니다.
        - `self.flatten = nn.Flatten()`: 2D 이미지 데이터를 1D 벡터로 변환하는 레이어입니다.
        - `self.linear_01 = nn.Linear(in_features=input_size*input_size, out_features=200)`: 첫 번째 선형 레이어로, 입력 특징 수는 28*28=784, 출력 특징 수는 200입니다.
        - `self.act_01 = nn.ReLU()`: 첫 번째 활성화 함수 (ReLU)입니다.
        - `self.linear_02 = nn.Linear(in_features=200, out_features=100)`: 두 번째 선형 레이어입니다.
        - `self.act_02 = nn.ReLU()`: 두 번째 활성화 함수 (ReLU)입니다.
        - `self.linear_03 = nn.Linear(in_features=100, out_features=num_classes)`: 최종 출력 선형 레이어로, 출력 특징 수는 `num_classes` (10개)입니다.
    - 화면 캡처 [00:02:21]에서 `__init__` 구현을 볼 수 있습니다.

- **00:02:40 - 00:04:10 (모델 정의 - `SimpleLinearModel_01`의 `forward`)**
    - `forward` 메서드에서 데이터가 모델을 통과하는 순서를 정의합니다.
    - 입력 `x`는 `self.flatten`을 통해 평탄화되고, 이후 `linear_01`, `act_01`, `linear_02`, `act_02`, `linear_03` 순으로 연결됩니다.
    - 최종 `output`은 `linear_03`의 결과입니다.
    - 화면 캡처 [00:02:41]에서 `forward` 구현을 볼 수 있습니다.

- **00:04:10 - 00:05:20 (모델 생성 및 `__init__` 동작 방식)**
    - `INPUT_SIZE = 28`과 `NUM_CLASSES = 10`을 정의합니다.
    - `model_01 = SimpleLinearModel_01(input_size=INPUT_SIZE, num_classes=NUM_CLASSES)` 코드를 통해 모델 객체를 생성합니다. 이때 `__init__` 함수가 호출되어 모델의 레이어들이 초기화됩니다.
    - 강사는 `__init__` 함수가 모델 생성 시 구성 요소를 만드는 역할을 한다고 강조합니다.
    - 화면 캡처 [00:04:53]에서 모델 생성 코드를 볼 수 있습니다.

- **00:05:20 - 00:06:00 (모델 구조 요약 및 `ReLU` 레이어 정의의 문제점)**
    - `torchinfo.summary`를 사용하여 `model_01`의 상세 구조를 확인합니다. `input_size=(1, 1, 28, 28)`은 단일 이미지의 입력 형태를 가정합니다.
    - 출력된 요약은 각 레이어의 `Output Shape`, `Params #`, `trainable` 여부를 보여줍니다. `Flatten` 다음 `Linear(in_features=784, out_features=200)`의 파라미터 수가 계산되는 것을 확인할 수 있습니다.
    - 강사는 `nn.ReLU()`와 같은 활성화 함수를 별도의 레이어(Module)로 `__init__`에 정의하면 코드가 길어지고 복잡해질 수 있다는 문제점을 언급합니다. `ReLU`는 학습 가능한 파라미터가 없기 때문에 굳이 `nn.Module` 객체로 만들 필요가 없다고 설명합니다.
    - 화면 캡처 [00:05:33]에서 `summary` 출력 결과를 확인할 수 있습니다.

- **00:06:00 - 00:07:00 (모델 정의 - `SimpleLinearModel_02`의 `forward` 개선)**
    - `SimpleLinearModel_01`의 문제점을 개선한 `SimpleLinearModel_02`를 정의합니다.
    - `__init__`에서는 `nn.Linear`와 같은 학습 가능한 파라미터를 가진 레이어만 정의합니다.
    - `forward` 메서드에서 `torch.nn.functional` 모듈의 `F.relu` 함수를 사용하여 활성화 함수를 적용합니다. 이는 `nn.ReLU()` 인스턴스를 만들 필요 없이 함수 호출로 활성화 처리가 가능하게 합니다.
    - `x = torch.flatten(x, start_dim=1, end_dim=-1)`: `nn.Flatten` 대신 `torch.flatten`을 `forward`에 직접 사용하며, `start_dim=1, end_dim=-1`로 배치 차원(0번째)을 제외한 나머지 차원(1, 28, 28)을 평탄화합니다.
    - 강사는 `F.relu`를 사용하면 코드가 더 간결하고 가독성이 높아진다고 설명합니다.
    - 화면 캡처 [00:06:04]에서 `SimpleLinearModel_02` 코드를 확인할 수 있습니다.

- **00:07:00 - 00:07:40 (`SimpleLinearModel_02` 실행 및 출력 확인)**
    - `model_02 = SimpleLinearModel_02(input_size=INPUT_SIZE, num_classes=NUM_CLASSES)`로 새로운 모델 객체를 생성합니다.
    - `output = model_02(images)` 코드를 실행하면 `model_02` 객체의 `forward` 메서드가 자동으로 호출됩니다.
    - `print(output.shape)`를 통해 최종 출력 형태가 `torch.Size([32, 10])` (배치 크기, 클래스 개수)임을 확인합니다.
    - 강사는 `model_02(images)`가 호출되면 `forward` 함수가 호출된다고 강조합니다.
    - 화면 캡처 [00:07:04]에서 코드와 출력 결과를 확인할 수 있습니다.

- **00:07:40 - 00:11:40 (`forward`에서 `torch.flatten` 상세 설명)**
    - 강사는 `forward` 함수 내에서 `x = torch.flatten(x, start_dim=1, end_dim=-1)`의 동작 원리를 자세히 설명합니다.
    - 입력 `x`의 형태가 `(32, 1, 28, 28)`일 때, `start_dim=1`은 두 번째 차원(인덱스 1)부터 평탄화를 시작하고, `end_dim=-1`은 마지막 차원(인덱스 -1)까지 평탄화합니다.
    - 즉, 배치 차원(인덱스 0, 크기 32)을 제외하고 `1 * 28 * 28 = 784`로 평탄화되어 `(32, 784)` 형태의 텐서가 생성됩니다. 이렇게 평탄화된 데이터가 첫 번째 선형 레이어의 입력으로 들어갑니다.
    - 최종 출력은 다시 `(32, 10)`이 됩니다.
    - 이 부분이 매우 중요하므로 반복하여 설명합니다.
    - 화면 캡처 [00:10:36]와 [00:11:37]에서 입력 및 출력 형태에 대한 주석을 볼 수 있습니다.

- **00:11:40 - 00:12:10 (모델 생성 함수화)**
    - 모델을 생성할 때마다 동일한 코드를 반복하는 것을 방지하기 위해 `create_simple_linear_model` 함수를 정의합니다.
    - 이 함수는 `SimpleLinearModel_02` 객체를 생성하고 리턴합니다.
    - 함수를 호출하면 간편하게 모델 객체를 얻을 수 있습니다.
    - 화면 캡처 [00:11:57]에서 해당 함수 코드를 확인할 수 있습니다.

- **00:12:10 - 00:12:50 (디바이스 설정, 손실 함수, 옵티마이저 정의)**
    - `device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')` 코드로 GPU 사용 가능 여부에 따라 디바이스를 설정합니다.
    - `model = create_simple_linear_model(input_size=INPUT_SIZE, num_classes=NUM_CLASSES)`로 모델을 생성하고, `model = model.to(device)`로 모델을 해당 디바이스로 옮깁니다.
    - `loss_fn = nn.CrossEntropyLoss()`: 다중 클래스 분류에 적합한 Cross Entropy Loss 함수를 정의합니다.
    - `optimizer = Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))`: 모델의 학습 가능한 파라미터(`model.parameters()`)를 사용하여 Adam 옵티마이저를 정의합니다. `lr`은 학습률(Learning Rate)입니다.
    - 화면 캡처 [00:12:18]에서 [00:12:58]까지 해당 코드들을 볼 수 있습니다.

- **00:12:50 - 00:14:50 (훈련 단계 함수 `train_step` 정의)**
    - `train_step` 함수는 한 에포크의 훈련 과정을 정의합니다.
    - `for batch_idx, (images, labels) in enumerate(train_loader):`를 통해 `train_loader`에서 배치 단위로 이미지와 라벨을 가져옵니다.
    - `images = images.to(device)`, `labels = labels.to(device)`: 데이터를 현재 설정된 디바이스(GPU/CPU)로 옮깁니다.
    - `pred = model(images)`: 모델에 이미지를 입력하여 예측값(`pred`)을 얻습니다. 이는 `model` 객체의 `forward` 메서드를 호출합니다.
    - `loss = loss_fn(pred, labels)`: 예측값과 실제 라벨을 비교하여 손실을 계산합니다.
    - `optimizer.zero_grad()`: 이전 스텝에서 계산된 기울기를 0으로 초기화합니다. (필수)
    - `loss.backward()`: 손실에 대한 역전파를 수행하여 모델의 모든 학습 가능한 파라미터에 대한 기울기(gradient)를 계산합니다.
    - `optimizer.step()`: 계산된 기울기를 사용하여 모델의 파라미터를 업데이트합니다.
    - `print` 문을 통해 `batch_idx`에 따른 손실 값을 출력합니다.
    - 강사는 이 과정이 한 번의 학습 업데이트(가중치 갱신)를 구성한다고 설명합니다.
    - 화면 캡처 [00:13:08]에서 [00:14:49]까지 `train_step` 코드를 확인할 수 있습니다.

- **00:14:50 - 00:15:20 (훈련 루프 및 검증 단계 함수 `val_step` 정의)**
    - `EPOCHS = 10`으로 총 10번의 에포크를 설정합니다.
    - `for epoch in range(EPOCHS):` 루프를 통해 모델을 훈련합니다.
    - `model.train()`: 모델을 훈련 모드로 설정합니다. (Dropout 등 훈련 시에만 활성화되는 레이어 동작)
    - `train_step()`: 훈련 단계를 실행합니다.
    - `model.eval()`: 모델을 평가 모드로 설정합니다. (Dropout 등 비활성화)
    - `val_step()`: 검증 단계를 실행합니다. `val_step` 내부에서는 `with torch.no_grad():`를 사용하여 기울기 계산을 비활성화합니다. 이는 검증 시에는 파라미터를 업데이트할 필요가 없으므로 메모리 사용량과 계산 속도를 최적화합니다.
    - 화면 캡처 [00:14:59]와 [00:15:09]에서 훈련 루프와 `val_step` 코드를 볼 수 있습니다.

- **00:15:20 - 00:17:10 (에포크(Epoch)의 개념 설명)**
    - 강사는 에포크가 무엇인지 상세히 설명합니다.
    - **1 에포크 = 전체 훈련 데이터셋을 한 번 완전히 학습하는 과정**을 의미합니다.
    - FashionMNIST 훈련 데이터는 6만 개, 배치 크기는 32이므로, 한 에포크당 `60000 / 32 = 1875`번의 배치 학습이 일어납니다.
    - 만약 `EPOCHS = 10`으로 설정하면, 전체적으로 `1875 * 10 = 18750`번의 파라미터 업데이트(학습)가 수행됩니다.
    - 에포크 수는 모델의 성능, 데이터셋 크기, 학습 시간 등을 고려하여 조절하며, 반드시 10번이 정답은 아닙니다. 자신의 '성능'에 따라 에포크 수를 정해야 한다고 강조합니다.
    - 학습 진행 상황 출력을 통해 배치별 손실 변화를 보여줍니다.
    - 화면 캡처 [00:15:50]에서 `EPOCHS = 10`을 확인할 수 있습니다.

---

### 3. 핵심 개념 및 코드/공식 정리

#### 3.1. 데이터셋 및 데이터 로딩
- **`torchvision.datasets.FashionMNIST`**: FashionMNIST 데이터셋을 불러오는 함수.
  - `root='data'`: 데이터 저장 경로.
  - `train=True/False`: 훈련/테스트 데이터 지정.
  - `download=True`: 데이터가 없으면 다운로드.
  - `transform=ToTensor()`: PIL Image를 PyTorch Tensor로 변환.
- **`torch.utils.data.DataLoader`**: 데이터셋을 효율적으로 로드하는 유틸리티.
  - `batch_size`: 한 번에 처리할 데이터 샘플의 수.
  - `shuffle=True`: 에포크마다 데이터를 섞음.
  - `num_workers`: 데이터 로딩을 위한 병렬 프로세스 수.
  ```python
  from torchvision import datasets, transforms
  from torch.utils.data import DataLoader

  BATCH_SIZE = 32
  train_data = datasets.FashionMNIST(root='data', train=True, download=True, transform=transforms.ToTensor())
  val_data = datasets.FashionMNIST(root='data', train=False, download=True, transform=transforms.ToTensor())

  train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
  val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)

  images, labels = next(iter(train_loader))
  print(images.shape, labels.shape) # 예: torch.Size([32, 1, 28, 28]) torch.Size([32])
  ```

#### 3.2. PyTorch 모델 정의 (`nn.Module`)
- **`nn.Module`**: 모든 PyTorch 신경망 모델의 기본 클래스. 상속받아 `__init__`과 `forward` 메서드를 구현해야 함.
- **`__init__(self, ...)`**: 모델의 레이어와 컴포넌트들을 정의.
- **`forward(self, x)`**: 입력 `x`가 모델을 통과하는 데이터 흐름을 정의.

#### 3.3. 주요 레이어 및 활성화 함수
- **`nn.Flatten()` / `torch.flatten(input, start_dim, end_dim)`**: 입력 텐서의 차원을 평탄화 (flatten).
  - `nn.Flatten()`는 `forward`에서 `input`을 받아서 `start_dim=1`부터 평탄화.
  - `torch.flatten`은 더욱 유연하게 `start_dim`과 `end_dim`을 지정하여 특정 범위의 차원만 평탄화 가능. 배치 차원을 유지하려면 `start_dim=1, end_dim=-1` 사용.
  ```python
  # nn.Flatten 사용 (SimpleLinearModel_01)
  self.flatten = nn.Flatten()
  x = self.flatten(x)

  # torch.flatten 사용 (SimpleLinearModel_02)
  x = torch.flatten(x, start_dim=1, end_dim=-1)
  # 예: 입력 (32, 1, 28, 28) -> 출력 (32, 784)
  ```
- **`nn.Linear(in_features, out_features)`**: 선형 변환 (Dense Layer 또는 Fully Connected Layer).
  - `in_features`: 입력 특징의 수.
  - `out_features`: 출력 특징의 수.
  ```python
  self.linear_01 = nn.Linear(in_features=INPUT_SIZE*INPUT_SIZE, out_features=200)
  ```
- **`nn.ReLU()` / `F.relu(input)`**: Rectified Linear Unit (ReLU) 활성화 함수. 입력이 0보다 작으면 0, 크면 입력을 그대로 반환.
  - `nn.ReLU()`: `__init__`에서 객체로 생성하여 사용.
  - `F.relu()`: `torch.nn.functional` 모듈에서 함수로 직접 호출. 파라미터가 없는 활성화 함수에 권장.
  ```python
  # nn.ReLU 사용 (SimpleLinearModel_01)
  self.act_01 = nn.ReLU()
  x = self.act_01(x)

  # F.relu 사용 (SimpleLinearModel_02)
  from torch.nn import functional as F
  x = F.relu(self.linear_01(x))
  ```

#### 3.4. 모델 클래스 정의 예시
```python
import torch
import torch.nn as nn
from torch.nn import functional as F # F.relu를 사용하기 위해 임포트

class SimpleLinearModel_02(nn.Module):
    def __init__(self, input_size, num_classes=10):
        super().__init__()
        # 학습 가능한 파라미터가 있는 레이어만 __init__에 정의
        self.linear_01 = nn.Linear(in_features=input_size*input_size, out_features=200)
        self.linear_02 = nn.Linear(in_features=200, out_features=100)
        self.linear_03 = nn.Linear(in_features=100, out_features=num_classes)

    def forward(self, x): # x: (Batch_Size, 1, 28, 28)
        # 배치 차원(0)을 제외하고 1*28*28을 784로 평탄화
        x = torch.flatten(x, start_dim=1, end_dim=-1) # x: (Batch_Size, 784)
        x = F.relu(self.linear_01(x)) # x: (Batch_Size, 200)
        x = F.relu(self.linear_02(x)) # x: (Batch_Size, 100)
        output = self.linear_03(x)      # output: (Batch_Size, 10)
        return output
```

#### 3.5. 훈련 관련 구성 요소
- **`torch.device('cuda' if torch.cuda.is_available() else 'cpu')`**: GPU(CUDA) 사용 가능 여부에 따라 학습 장치 설정.
- **`model.to(device)`**: 모델을 지정된 장치(CPU/GPU)로 이동.
- **`nn.CrossEntropyLoss()`**: 다중 클래스 분류를 위한 손실 함수. `LogSoftmax`와 `NLLLoss`를 결합한 형태.
- **`torch.optim.Adam(model.parameters(), lr, betas)`**: Adam 옵티마이저.
  - `model.parameters()`: 모델의 학습 가능한 모든 파라미터.
  - `lr` (learning rate): 학습률.
  - `betas`: Adam 알고리즘의 지수 이동 평균 계수.
- **`optimizer.zero_grad()`**: 옵티마이저에 저장된 모든 학습 가능한 파라미터의 기울기(gradient)를 0으로 초기화.
- **`loss.backward()`**: 손실에 대한 역전파를 수행하여 모델의 파라미터들에 대한 기울기를 계산.
- **`optimizer.step()`**: 계산된 기울기를 사용하여 모델의 파라미터들을 업데이트.

#### 3.6. 훈련/평가 모드 및 기울기 비활성화
- **`model.train()`**: 모델을 훈련 모드로 설정. `Dropout`이나 `BatchNorm`과 같은 레이어가 훈련 시 활성화됨.
- **`model.eval()`**: 모델을 평가 모드로 설정. `Dropout`이 비활성화되고 `BatchNorm`은 학습된 통계량을 사용.
- **`with torch.no_grad():`**: 이 블록 내에서는 기울기 계산을 비활성화. 평가 시 메모리 효율성과 속도 향상을 위해 사용.

#### 3.7. 에포크(Epoch)
- **에포크**: 전체 훈련 데이터셋을 모델이 한 번 완전히 학습하는 과정.
- `(총 훈련 데이터 개수) / (배치 크기)` = 한 에포크당 배치 반복 횟수.
- 예: 60,000개 데이터, 배치 크기 32 -> `60000 / 32 = 1875`번의 배치가 한 에포크.

---

### 4. 학습 퀴즈

1.  **PyTorch 모델의 `__init__`과 `forward` 메서드의 주요 역할은 무엇이며, `SimpleLinearModel_01`과 `SimpleLinearModel_02`에서 `nn.ReLU()`와 `F.relu()`를 사용하는 방식의 차이점을 설명하세요.**
2.  **FashionMNIST 데이터셋(`torch.Size([60000, 28, 28])`)을 `BATCH_SIZE = 32`로 DataLoader를 통해 로드했을 때, `SimpleLinearModel_02`의 `forward` 메서드에서 `x = torch.flatten(x, start_dim=1, end_dim=-1)` 코드가 `x`의 형태를 어떻게 변화시키는지 상세히 설명하세요.**
3.  **PyTorch 훈련 루프에서 `optimizer.zero_grad()`, `loss.backward()`, `optimizer.step()` 세 가지 연산이 정확히 어떤 순서로, 왜 실행되어야 하는지 설명하세요.**