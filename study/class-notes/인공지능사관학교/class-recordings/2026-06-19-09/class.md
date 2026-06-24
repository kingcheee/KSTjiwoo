# 6월 19일 9시 수업 학습 노트

## 1. 강의 핵심 요약

이번 6월 19일 9시 수업은 PyTorch를 활용한 딥러닝 모델 구축의 전반적인 과정을 다루었습니다. 데이터 준비 (전처리, 증강, 정규화, 텐서 변환, DataLoader 사용), 모델 생성 (커스텀 모델, 레이어 구성), 학습 수행 (Loss, Optimizer, Training Loop), 예측 및 평가, 최적화 단계로 구성되는 파이토치 모델 구축 흐름을 배우고, 특히 데이터 로딩 및 모델 클래스 정의, 순전파 및 역전파 과정의 핵심 코드와 개념을 상세히 학습했습니다. `nn.CrossEntropyLoss`와 `Adam` 옵티마이저의 역할과 작동 방식을 이해하고, `model.train()`과 `model.eval()` 모드의 중요성을 강조했습니다.

## 2. 화면 연계 타임라인 노트

### 00:00:00 - 00:00:19: Fashion MNIST 모델 소개
*   **강의 주제:** `Fashion MNIST 모델`은 PyTorch에서 제공하는 데이터셋으로, 이전에 사이킷런에서 데이터를 가져왔던 것과 유사하게 활용됩니다.

### 00:00:20 - 00:00:39: PyTorch 모델 구축 과정 개요
*   **화면:** `Pytorch 모델 구축` 슬라이드 (데이터 준비, 네트워크 모델 생성, 학습 수행, 예측 및 평가, 최적화).
*   **강의:** PyTorch 모델 구축 과정은 머신러닝 모델 구축과 유사한 패턴을 가집니다.
*   **데이터 준비:** 데이터 전처리, Augmentation(증강), Normalization(정규화), Tensor 변환이 필요합니다.
*   **학습 수행:** `Loss` 함수와 `Optimizer`를 사용하며, `Training Loop`를 통해 학습을 진행합니다.

### 00:00:40 - 00:00:59: 데이터 준비의 핵심: Tensor 변환 및 DataLoader
*   **화면:** `Tensor 변환` 및 `Dataset, DataLoader` 항목이 강조됩니다.
*   **강의:** `Normalization`과 함께 데이터를 `Tensor` 형태로 변환하는 과정이 중요하며, `Dataset`과 `DataLoader` 객체가 필수적으로 요구됩니다.

### 00:01:00 - 00:01:25: PyTorch와 Scikit-learn의 차이점
*   **강의:** PyTorch는 Scikit-learn과 달리 데이터를 `Tensor`로 변환하고 `Dataset`, `DataLoader`를 통해 사전에 준비해야 하는 차이점이 있습니다.

### 00:01:26 - 00:01:47: 모델 생성 및 학습 유형
*   **화면:** `네트워크 모델 생성` 항목이 강조됩니다.
*   **강의:** 데이터 준비 후 `Custom 모델`을 직접 작성하거나, `Pretrained 모델`을 활용하여 모델을 생성합니다. 다음 주에는 Pretrained 모델 활용에 대해 학습 예정입니다.

### 00:01:48 - 00:02:02: 학습 수행의 기본 요소
*   **화면:** `학습 수행` 항목이 강조됩니다.
*   **강의:** 학습은 `Training Loop` 내에서 `Loss` 함수와 `Optimizer`를 사용하여 이루어집니다.

### 00:02:03 - 00:02:24: 가중치 업데이트와 Loss의 역할
*   **강의:** 모델의 `가중치(Weight)`를 업데이트하기 위해서는 `Loss` 값을 알아야 합니다. `Loss`는 예측과 실제값 사이의 차이를 나타내며, 이 차이를 바탕으로 가중치를 얼마나 업데이트할지 결정합니다.

### 00:02:25 - 00:03:18: Optimizer의 필요성: 경사 하강법의 한계
*   **화면:** Loss Landscape(손실 지형) 그림이 표시되며, 여러 개의 국소 최저점(Local Minima)이 강조됩니다.
*   **강의:** `Optimizer`는 경사 하강법(Gradient Descent)이 국소 최저점에 갇히는 문제를 해결하고, 전역 최저점(Global Minima)을 더 효율적으로 찾아 학습을 돕는 역할을 합니다.

### 00:03:19 - 00:03:33: Adam Optimizer 사용
*   **강의:** `Gradient`를 더 잘 처리하기 위해 `Adam` 옵티마이저를 사용합니다.

### 00:03:34 - 00:03:53: Training Loop: Epochs의 반복 학습
*   **강의:** `Training Loop`는 한 번만 도는 것이 아니라, 여러 `Epochs`(전체 데이터셋을 한 번 처리하는 단위)를 통해 반복 학습을 수행합니다. 이는 공부를 여러 번 반복하는 것과 같습니다.

### 00:03:54 - 00:04:13: 검증(Validation)의 중요성
*   **강의:** 학습 중간에 `검증(Validation)` 또는 `테스트(Test)` 데이터셋을 사용하여 모델의 성능을 평가합니다. 이는 과적합을 방지하고 모델의 일반화 능력을 확인하는 과정입니다.

### 00:04:14 - 00:04:35: 모델 구축의 전체 과정 요약
*   **화면:** `예측 및 평가`, `최적화` 항목이 강조됩니다.
*   **강의:** 모델 구축은 데이터 준비부터 모델 생성, 학습, 예측, 평가, 최적화에 이르는 일련의 과정입니다.

### 00:04:36 - 00:04:43: Tensor의 차원 이해
*   **화면:** `배열 (텐서) 차원` 슬라이드 (정형 데이터, Grayscale 이미지, RGB 이미지).
*   **강의:** 데이터는 `텐서(Tensor)` 형태로 표현되며, 차원(Dimension)을 가집니다 (예: 스칼라(0차원), 벡터(1차원), 2차원(행렬), 3차원(RGB 이미지)).

### 00:05:02 - 00:05:15: Fashion MNIST 데이터 로딩
*   **화면:** `from torchvision import datasets`, `from torchvision.transforms import ToTensor` 코드가 보입니다.
*   **강의:** `torchvision.datasets.FashionMNIST`를 사용하여 Fashion MNIST 데이터셋을 다운로드합니다.

### 00:05:16 - 00:05:48: 데이터 변환 (`ToTensor`) 및 저장 경로
*   **화면:** `root='data'`, `train=True`, `download=True`, `transform=ToTensor()`가 강조됩니다.
*   **강의:** 데이터는 'data' 폴더에 저장되고, `ToTensor()` 변환을 통해 픽셀 값이 [0, 1] 범위의 텐서로 정규화됩니다.

### 00:05:49 - 00:06:04: 검증 데이터셋 준비
*   **화면:** `val_data = datasets.FashionMNIST(root='data', train=False, ...)` 코드가 강조됩니다.
*   **강의:** `train=False`로 설정하여 모델 훈련에 사용되지 않는 별도의 검증(테스트) 데이터셋을 준비합니다.

### 00:06:05 - 00:06:26: 훈련 데이터셋의 크기와 차원 확인
*   **화면:** `print(len(train_data))` 결과 `60000`, `print(train_data.shape)` 결과 `torch.Size([60000, 28, 28])`.
*   **강의:** 훈련 데이터셋은 6만 개의 이미지로 구성되며, 각 이미지는 28x28 픽셀 크기를 가집니다.

### 00:06:27 - 00:06:48: DataLoader 사용 이유: 이미지 처리 단위
*   **강의:** `DataLoader`를 사용하는 이유는 신경망이 단일 이미지가 아닌 여러 이미지를 묶은 `배치(Batch)` 단위로 처리하여 효율성을 높이기 위함입니다. 이미지의 채널(예: RGB) 개념도 언급됩니다.

### 00:06:49 - 00:07:20: Grayscale 이미지의 스케일
*   **강의:** 흑백(Grayscale) 이미지는 스케일(채널)이 1이며, RGB 이미지는 R, G, B 세 가지 스케일을 가집니다.

### 00:07:21 - 00:07:42: 이미지 차원과 배치 사이즈 정의
*   **화면:** `BATCH_SIZE = 32`, `batch_size=BATCH_SIZE` 코드가 강조됩니다.
*   **강의:** 이미지 크기는 28x28 픽셀이며, `BATCH_SIZE = 32`는 한 번에 32개의 이미지를 처리함을 의미합니다.

### 00:07:43 - 00:08:11: 배치 사이즈(Batch Size)의 의미
*   **강의:** `BATCH_SIZE`는 훈련 시 여러 이미지를 묶어 처리하는 단위이며, 32는 32장의 이미지를 한 묶음으로 처리한다는 뜻입니다.

### 00:08:12 - 00:08:42: PyTorch에서 배치 사이즈의 위치
*   **화면:** `print(images.shape, labels.shape)` 결과 `torch.Size([32, 1, 28, 28])` 및 `torch.Size([32])`.
*   **강의:** PyTorch에서 `BATCH_SIZE`는 텐서의 가장 첫 번째 차원(예: `[배치_크기, 채널, 높이, 너비]`)으로 오며, PyTorch는 이를 자동으로 인식합니다.

### 00:08:43 - 00:09:11: 배치 사이즈의 지속성 및 데이터 셔플링
*   **화면:** `shuffle=True`, `num_workers=4` 코드가 강조됩니다.
*   **강의:** `BATCH_SIZE`는 모델 연산에서 계속 유지됩니다. `shuffle=True`는 각 에포크마다 데이터를 무작위로 섞어 모델이 데이터 순서에 의존하는 것을 방지합니다. `num_workers`는 데이터 로딩을 병렬 처리합니다.

### 00:09:12 - 00:09:40: 셔플링의 필요성: 라벨 정렬 문제
*   **강의:** 데이터의 라벨(정답)이 특정 순서로 정렬되어 있을 수 있으므로(예: 0번 라벨 이미지들, 1번 라벨 이미지들), `shuffle=True`는 이러한 정렬을 해소하여 모델의 편향된 학습을 막습니다.

### 00:09:41 - 00:10:11: DataLoader를 통한 데이터 준비 요약
*   **강의:** `DataLoader`는 `train_loader`와 `val_loader` 두 가지 객체를 생성하며, 이들은 배치 단위로 데이터를 제공하고 순서대로 접근할 수 있는 `이터레이터(Iterator)` 형태로 작동합니다.

### 00:10:12 - 00:11:11: 배치 데이터의 구성: 이미지와 라벨
*   **화면:** `images.shape`는 `torch.Size([32, 1, 28, 28])`, `labels.shape`는 `torch.Size([32])`.
*   **강의:** 각 배치는 32개의 이미지(`[32, 1, 28, 28]`)와 32개의 해당 라벨(`[32]`)로 구성됩니다. `next()` 함수로 한 묶음의 배치를 가져올 수 있습니다.

### 00:11:12 - 00:12:04: 데이터 준비 단계의 최종 검증
*   **강의:** 데이터 준비는 모델 구축의 첫 단계로 매우 중요합니다. `shape`, `size()`, `view()` 함수를 사용하여 텐서의 차원을 계속 확인해야 다음 작업이 가능합니다.

### 00:12:05 - 00:12:34: 모델 클래스 정의 (`nn.Module`)
*   **화면:** `class SimpleLinearModel_01(nn.Module):` 코드가 보입니다.
*   **강의:** `nn.Module`을 상속받아 모델 클래스를 정의하며, 모델의 각 계층(레이어)을 `__init__` 메서드 내에서 개별적으로 정의합니다 (예: `nn.Linear`, `nn.ReLU`).

### 00:12:35 - 00:12:55: 이미지 데이터 평탄화 (`nn.Flatten`)
*   **화면:** `self.flatten = nn.Flatten()` 코드가 강조됩니다.
*   **강의:** `nn.Flatten()`은 다차원 이미지 데이터를 1차원 벡터로 변환하여 완전 연결(Fully Connected) 레이어에 입력할 수 있도록 합니다.

### 00:12:56 - 00:13:15: 첫 번째 Linear Layer의 입력 크기
*   **화면:** `input_size*input_size` (28*28) 코드가 강조됩니다.
*   **강의:** `Flatten` 레이어를 거치면 28x28 픽셀 이미지가 784개의 1차원 벡터로 변환되며, 이 값이 첫 번째 `nn.Linear` 레이어의 입력으로 들어갑니다.

### 00:13:16 - 00:14:10: Hidden Layer 출력 크기 설정
*   **화면:** `out_features=200`이 강조됩니다.
*   **강의:** 히든 레이어의 출력 크기(예: 200, 100)는 사용자가 직접 설정하는 하이퍼파라미터입니다. 정해진 값은 없으며, 일반적으로 실험을 통해 적절한 '추세'를 따릅니다.

### 00:14:11 - 00:15:28: Hidden Layer 크기 조정의 추세
*   **강의:** 완전 연결 레이어에서는 보통 레이어의 뉴런 수를 점진적으로 줄여나가거나 유지하는 추세가 있습니다. 급격한 변화는 모델 성능 저하로 이어질 수 있습니다.

### 00:15:29 - 00:16:17: 모델 구조 설계: 경험과 참고
*   **강의:** 모델의 레이어 크기나 개수에 대한 '정답'은 없으며, 다른 성공적인 모델들을 참고하고 경험을 통해 결정하는 경우가 많습니다.

### 00:16:18 - 00:17:00: 레이어 간 데이터 흐름: 입력과 출력
*   **화면:** `out_features=200`이 다음 레이어의 `in_features=200`으로 이어지는 것이 강조됩니다.
*   **강의:** 한 레이어의 출력이 다음 레이어의 입력이 되는 방식으로 데이터가 흐르며, 최종 출력 레이어의 `out_features`는 분류할 클래스(10개)의 개수와 일치합니다.

### 00:17:01 - 00:18:18: `__init__`과 `forward`의 역할 분리
*   **강의:** `__init__` 메서드에서는 모델의 각 레이어(구성 요소)를 '정의'만 하고, 실제 데이터가 이 레이어들을 통해 어떻게 흐르고 변환되는지는 `forward` 메서드에서 '연결'하고 '정의'합니다.

### 00:18:19 - 00:19:19: 순전파(Forward Pass)의 상세 과정
*   **화면:** `def forward(self, x):` 부분의 코드가 강조됩니다. (`x = self.flatten(x)`, `x = self.linear_01(x)`, `x = self.act_01(x)` 등)
*   **강의:** `forward` 메서드에서 입력 `x`는 `Flatten`을 거쳐 1차원 벡터가 되고, 각 `Linear` 레이어와 `ReLU` 활성화 함수를 순차적으로 통과하며 변환됩니다. 이 정의를 통해 레이어들이 연결됩니다.

### 00:19:20 - 00:20:14: PyTorch Custom Model의 3가지 핵심 규칙
*   **강의:**
    1.  `nn.Module` 클래스를 상속받습니다.
    2.  `__init__` 메서드와 `forward` 메서드를 반드시 구현합니다.
    3.  `__init__` 메서드 내에서 `super().__init__()`를 호출합니다.
    이 규칙들은 PyTorch 프레임워크 사용의 필수 조건입니다.

### 00:20:15 - 00:20:48: 모델 객체 생성 (인스턴스화)
*   **화면:** `model_01 = SimpleLinearModel_01(input_size=INPUT_SIZE, num_classes=NUM_CLASSES)` 코드가 강조됩니다.
*   **강의:** 정의된 모델 클래스(`SimpleLinearModel_01`)는 '붕어빵 틀'과 같으며, 실제 사용하기 위해서는 이 틀로부터 '붕어빵'에 해당하는 `객체(Object)` 또는 `인스턴스(Instance)`를 생성해야 합니다.

### 00:20:49 - 00:21:23: 파이썬에서 객체 생성 방식
*   **강의:** 파이썬에서는 `객체명 = 클래스명()` 형태로 객체를 생성하며, 이 과정에서 자동으로 `__init__` 메서드가 호출됩니다.

### 00:21:24 - 00:22:04: 모델 생성 후 상태: '빈 깡통'
*   **화면:** `summary(model=model_01, ...)` 코드가 보입니다.
*   **강의:** 모델을 생성(객체화)하는 것은 모델의 구조를 설정하는 것이며, 아직 학습되거나 실행되지 않은 '빈 깡통' 상태입니다.

### 00:22:05 - 00:22:50: 두 번째 모델: `F.relu`를 이용한 간결한 활성화 함수 처리
*   **화면:** `class SimpleLinearModel_02(nn.Module):` 코드가 소개됩니다.
*   **강의:** 두 번째 모델(`SimpleLinearModel_02`)에서는 `__init__`에서 활성화 함수를 별도 레이어로 정의하지 않고, `forward` 메서드 내에서 `torch.nn.functional.relu`(줄여서 `F.relu`)를 직접 호출하여 사용합니다. 이는 코드를 더 간결하게 만듭니다.

### 00:22:51 - 00:23:58: `F.relu` 사용 예시
*   **화면:** `x = F.relu(self.linear_01(x))` 코드가 강조됩니다.
*   **강의:** `F.relu(선형_레이어_결과)`와 같이 사용하여 활성화 함수를 적용할 수 있으며, 이는 `nn.ReLU()`를 별도 레이어로 사용하는 것과 동일한 결과를 줍니다.

### 00:23:59 - 00:25:25: 모델 실행: 이미지 입력과 예측 출력
*   **화면:** `output = model_02(images)` 및 `print(output.shape)` 결과 `torch.Size([32, 10])`.
*   **강의:** `model_02(images)`를 호출하면 `forward` 메서드가 실행되어 이미지 배치를 처리하고, 10개의 클래스에 대한 예측값(출력 텐서)을 반환합니다. 출력 텐서의 크기는 `[배치_크기, 클래스_개수]`입니다.

### 00:25:26 - 00:26:08: 모델 초기화 및 디바이스 설정 함수
*   **화면:** `create_simple_linear_model` 함수 정의 및 `device = torch.device(...)`, `model = model.to(device)` 코드가 보입니다.
*   **강의:** 모델 생성 과정을 함수로 만들어 재사용성을 높였습니다. 모델을 훈련시키기 전, `CUDA`(GPU) 사용 가능 여부를 확인하고 모델을 해당 디바이스로 이동시킵니다.

### 00:26:09 - 00:27:09: Cross Entropy Loss의 기본 개념 및 계산
*   **화면:** `Cross Entropy Loss` 슬라이드에 공식 및 계산 예시(`CE = -log(0.9) = 0.105`).
*   **강의:** `nn.CrossEntropyLoss()`는 주로 다중 클래스 분류에 사용되는 손실 함수입니다. 정답 클래스의 예측 확률에 대해 음의 로그를 취하는 방식으로 계산됩니다.

### 00:27:10 - 00:28:01: Softmax와 Cross Entropy Loss의 관계
*   **화면:** `Softmax activation function` 및 `Probabilities`가 합이 1이 되는 것을 보여주는 슬라이드.
*   **강의:** `Cross Entropy Loss`는 `Softmax` 활성화 함수를 통해 나온 확률값(각 클래스에 대한 예측 확률)을 입력으로 사용하여 손실을 계산합니다.

### 00:28:02 - 00:29:08: Cross Entropy Loss의 특징: 잘못된 예측에 대한 높은 패널티
*   **화면:** `Cross Entropy Loss` 그래프가 표시되며, 잘못된 예측에 대한 손실이 기하급수적으로 증가하는 것을 보여줍니다.
*   **강의:** `Cross Entropy Loss`는 모델이 실제 정답과 크게 다른 예측을 하거나, 틀린 예측에 대해 높은 확신을 보일 경우 매우 큰 손실을 부여하여 강력하게 패널티를 줍니다.

### 00:29:09 - 00:32:08: Cross Entropy Loss 계산 예시
*   **화면:** Softmax 예측값과 실제값의 불일치에 따른 CE 계산 예시가 제시됩니다.
*   **강의:** 모델이 정답이 아닌 클래스에 높은 확률을 부여했을 때, `Cross Entropy Loss`는 매우 큰 값을 가집니다. 이는 모델이 잘못된 예측에 대해 더 큰 책임을 지고 학습하도록 유도합니다.

### 00:32:09 - 00:34:12: Cross Entropy Loss의 목적
*   **강의:** `Cross Entropy Loss`는 모델이 예측에 대해 더 정확하고 확신을 가질 수 있도록 학습을 유도하는 것이 주된 목적입니다.

### 00:34:13 - 00:35:10: Training Loop의 구조
*   **화면:** `Training Loop` 플로우차트 (Epoch loop -> Mini-batch loop -> Forward Pass -> Loss Calculation -> Optimizer gradient initialization -> Backward Pass -> Parameter update).
*   **강의:** `Training Loop`는 `Epoch` 단위로 반복되며, 각 `Epoch` 내에서는 `Mini-batch` 단위로 데이터가 처리됩니다.

### 00:35:11 - 00:36:59: `train_step()` 함수: 데이터 이동, 순전파, 손실 계산
*   **화면:** `def train_step():` 코드 스니펫. `images.to(device)`, `labels.to(device)`, `pred = model(images)` 부분이 강조됩니다.
*   **강의:** `train_step()` 함수 내에서 이미지와 라벨을 모델과 동일한 디바이스로 이동시키고, `model(images)`를 호출하여 `순전파(Forward Pass)`를 수행하고 `손실(Loss)`을 계산합니다.

### 00:37:00 - 00:37:40: `train_step()` 함수: 손실 계산 및 옵티마이저 초기화
*   **화면:** `loss = loss_fn(pred, labels)` 및 `optimizer.zero_grad()` 코드가 강조됩니다.
*   **강의:** 계산된 예측값과 실제 라벨을 바탕으로 `Loss`를 계산하고, 다음 `역전파`를 위해 `Optimizer`의 `Gradient`를 `0`으로 초기화(`zero_grad()`)합니다.

### 00:37:41 - 00:38:59: `train_step()` 함수: 역전파 및 가중치 업데이트
*   **화면:** `loss.backward()` 및 `optimizer.step()` 코드가 강조됩니다.
*   **강의:** `loss.backward()`는 `역전파(Backpropagation)`를 수행하여 모델의 모든 파라미터에 대한 `Gradient`를 계산하고, `optimizer.step()`은 계산된 `Gradient`를 사용하여 모델의 `가중치(Weight)`를 업데이트합니다.

### 00:39:00 - 00:39:11: `train_step()` 함수: 손실 값 출력
*   **강의:** 현재 `Loss` 값을 출력하여 학습 진행 상황을 모니터링합니다.

### 00:39:12 - 00:40:00: `val_step()` 함수: 검증 과정의 특징
*   **화면:** `def val_step():` 코드 스니펫. `optimizer.zero_grad()`, `loss.backward()`, `optimizer.step()`이 생략된 것이 보입니다.
*   **강의:** `val_step()` 함수는 `검증(Evaluation)`만을 위한 것으로, 훈련 과정이 아니므로 `Gradient` 계산이나 파라미터 업데이트를 위한 코드는 포함되지 않고 오직 손실 계산만 수행합니다.

### 00:40:01 - 00:41:12: 주 학습 루프: `Epoch` 반복과 모드 전환
*   **화면:** `for epoch in range(EPOCHS):` 루프와 `model.train()`, `model.eval()` 코드가 강조됩니다.
*   **강의:** 전체 학습 루프는 정의된 `EPOCHS` 수만큼 반복됩니다. 각 `Epoch` 시작 시 `model.train()`으로 훈련 모드를, `val_step()` 전에는 `model.eval()`로 평가 모드를 설정합니다.

### 00:41:13 - 00:42:00: Loss만으로 평가의 한계 및 Accuracy의 필요성
*   **강의:** `Loss` 값의 감소만으로는 모델이 과적합되었는지, 실제 예측 성능이 얼마나 좋은지 판단하기 어렵습니다. 따라서 `Accuracy`와 같은 추가적인 지표를 함께 확인해야 합니다.

## 3. 핵심 개념 및 코드/공식 정리

### 1. PyTorch 모델 구축 과정 (PyTorch 모델 구축 슬라이드 기반)
*   **데이터 준비:** 데이터 전처리, Augmentation(데이터 증강), Normalization(데이터 정규화), Tensor 변환, Dataset/DataLoader 객체 생성.
*   **네트워크 모델 생성:** Custom 모델 작성 또는 Pretrained 모델 활용.
*   **학습 수행:** Loss 함수, Optimizer 선택, Training Loop 실행 (검증 평가 포함).
*   **예측 및 평가:** 모델 테스트 예측, 모델 테스트 평가.
*   **최적화:** 하이퍼파라미터 튜닝, 모델 재구성, Augmentation 변경.

### 2. 데이터 로딩 및 전처리 (00:05:02 - 00:11:11)
*   **데이터셋 다운로드:**
    ```python
    from torchvision import datasets
    from torchvision.transforms import ToTensor

    # 훈련 데이터셋
    train_data = datasets.FashionMNIST(
        root='data',           # 데이터를 저장할 경로
        train=True,            # 훈련 데이터셋임을 명시
        download=True,         # 데이터셋이 없으면 다운로드
        transform=ToTensor()   # 데이터를 텐서로 변환 (0~1 범위로 정규화 포함)
    )

    # 검증 데이터셋 (테스트 데이터셋)
    val_data = datasets.FashionMNIST(
        root='data',
        train=False,           # 검증 데이터셋임을 명시
        download=True,
        transform=ToTensor()
    )
    ```
*   **데이터셋 크기 및 차원 확인:**
    ```python
    print(len(train_data))        # 출력: 60000 (훈련 데이터 개수)
    print(train_data.shape)       # 출력: torch.Size([60000, 28, 28]) (6만개, 28x28 이미지)
    ```
*   **DataLoader 설정:**
    ```python
    from torch.utils.data import DataLoader

    BATCH_SIZE = 32 # 한 번에 처리할 이미지 묶음(배치) 크기

    train_loader = DataLoader(
        train_data,
        batch_size=BATCH_SIZE,
        shuffle=True,          # 데이터를 에포크마다 섞음 (편향 방지)
        num_workers=4          # 데이터 로딩 병렬 처리 (속도 향상)
    )

    val_loader = DataLoader(
        val_data,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=4
    )
    ```
*   **배치 데이터 확인:**
    ```python
    # 첫 번째 배치 데이터 가져오기
    images, labels = next(iter(train_loader))

    # 이미지와 라벨의 차원 확인
    print(images.shape, labels.shape)
    # 출력: torch.Size([32, 1, 28, 28]) (32개 이미지, 1채널(흑백), 28x28 픽셀)
    #       torch.Size([32]) (32개 라벨)
    ```

### 3. PyTorch Custom Model (`nn.Module`) 정의 (00:12:24 - 00:20:14)

*   **기본 구조:**
    ```python
    import torch
    import torch.nn as nn
    import torch.nn.functional as F # 활성화 함수를 간결하게 사용하기 위함

    class SimpleLinearModel_02(nn.Module): # nn.Module 상속 필수
        def __init__(self, input_size, num_classes):
            super().__init__() # 부모 클래스(__init__) 호출 필수

            self.flatten = nn.Flatten() # 다차원 입력을 1차원으로 평탄화

            # 히든 레이어 1: 입력 784 (28*28) -> 출력 200
            self.linear_01 = nn.Linear(in_features=input_size*input_size, out_features=200)
            # 히든 레이어 2: 입력 200 -> 출력 100
            self.linear_02 = nn.Linear(in_features=200, out_features=100)
            # 출력 레이어: 입력 100 -> 출력 num_classes (10)
            self.linear_03 = nn.Linear(in_features=100, out_features=num_classes)

        def forward(self, x): # 데이터가 모델을 통과하는 순서 정의 (순전파)
            x = self.flatten(x)          # 이미지 평탄화
            x = self.linear_01(x)        # 첫 번째 선형 계층
            x = F.relu(x)                # ReLU 활성화 함수 적용 (F.relu 사용)
            x = self.linear_02(x)        # 두 번째 선형 계층
            x = F.relu(x)                # ReLU 활성화 함수 적용
            output = self.linear_03(x)   # 최종 출력 계층
            return output
    ```
*   **`nn.Flatten()`:** 이미지 데이터를 1차원 벡터로 변환 (예: `[32, 1, 28, 28]` -> `[32, 784]`).
*   **`nn.Linear(in_features, out_features)`:** 완전 연결 계층. `in_features`는 이전 레이어의 출력 크기, `out_features`는 현재 레이어의 출력 크기.
*   **`F.relu(x)`:** ReLU 활성화 함수를 적용. `nn.ReLU()` 레이어를 `__init__`에서 정의하고 `forward`에서 사용하는 대신, `torch.nn.functional` 모듈의 `F.relu`를 직접 사용할 수 있습니다.

### 4. 옵티마이저 (`Adam`) 및 손실 함수 (`CrossEntropyLoss`) (00:27:10 - 00:34:32)
*   **모델 디바이스 설정:**
    ```python
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') # GPU 사용 가능 여부 확인
    model = SimpleLinearModel_02(input_size=28, num_classes=10) # 모델 객체 생성
    model = model.to(device) # 모델을 GPU 또는 CPU로 이동
    ```
*   **손실 함수 (`nn.CrossEntropyLoss`):**
    ```python
    loss_fn = nn.CrossEntropyLoss()
    ```
    *   **특징:** 주로 다중 클래스 분류에 사용됩니다.
    *   **계산 방식:** 예측된 `Softmax` 확률과 실제 라벨을 비교하여 손실을 계산합니다.
    *   **장점:** 잘못된 예측, 특히 틀린 예측에 대해 높은 확신을 보일 경우 매우 큰 손실을 부여하여, 모델이 더 정확하고 확신 있는 예측을 하도록 유도합니다. (00:28:02 - 00:32:08 참고)
*   **옵티마이저 (`torch.optim.Adam`):**
    ```python
    import torch.optim as optim
    optimizer = optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))
    ```
    *   **역할:** `Gradient`를 효율적으로 업데이트하여 Loss 값을 최소화하는 데 기여합니다.
    *   **`model.parameters()`:** 옵티마이저가 최적화할 모델의 모든 학습 가능한 파라미터(가중치와 편향)를 지정합니다.
    *   **`lr` (learning rate):** 학습률. `Gradient`를 따라 가중치를 얼마나 크게 업데이트할지 결정합니다.
    *   **`betas`:** Adam 옵티마이저의 내부 파라미터로, `Gradient`의 1차 및 2차 모멘트 추정에 사용됩니다.

### 5. Training Loop의 핵심 단계 (00:35:11 - 00:38:59)
*   **`train_step()` 함수 내부:**
    1.  **데이터 디바이스 이동:**
        ```python
        images = images.to(device)
        labels = labels.to(device)
        ```
    2.  **순전파 (Forward Pass):**
        ```python
        pred = model(images) # 모델에 이미지 입력 후 예측값 계산
        ```
    3.  **손실 계산:**
        ```python
        loss = loss_fn(pred, labels) # 예측값과 실제 라벨로 손실 계산
        ```
    4.  **옵티마이저 Gradient 초기화:**
        ```python
        optimizer.zero_grad() # 이전 단계의 Gradient를 초기화
        ```
        *   **이유:** `Gradient`는 누적되므로, 새로운 `Gradient` 계산 전에 반드시 초기화해야 합니다.
    5.  **역전파 (Backward Pass):**
        ```python
        loss.backward() # Loss를 바탕으로 모든 학습 가능한 파라미터의 Gradient 계산
        ```
        *   **역할:** 손실을 줄이기 위해 각 파라미터가 얼마나 기여했는지 계산하는 과정입니다.
    6.  **파라미터 업데이트:**
        ```python
        optimizer.step() # 계산된 Gradient를 사용하여 모델 파라미터 업데이트
        ```
        *   **역할:** 모델의 가중치와 편향을 학습률과 옵티마이저 알고리즘에 따라 조정합니다.

### 6. 주 학습 루프 (Main Training Loop) (00:40:01 - 00:41:12)
*   **Epoch 반복:**
    ```python
    EPOCHS = 10 # 전체 데이터셋을 10번 반복 학습
    for epoch in range(EPOCHS):
        # 훈련 모드 설정
        model.train() # 모델을 훈련 모드로 설정 (예: Dropout 활성화)
        train_step()  # 훈련 스텝 실행

        # 평가 모드 설정
        model.eval()  # 모델을 평가 모드로 설정 (예: Dropout 비활성화)
        val_step()    # 검증 스텝 실행
    ```
*   **`model.train()`:** 모델을 훈련 모드로 전환. `Dropout`과 같은 특정 레이어들이 훈련 시에만 활성화됩니다.
*   **`model.eval()`:** 모델을 평가 모드로 전환. `Dropout`이 비활성화되고 배치 정규화(Batch Normalization)의 통계가 고정됩니다.

## 4. 학습 퀴즈

1.  PyTorch에서 모델 클래스를 정의할 때 반드시 포함되어야 하는 세 가지 핵심 규칙은 무엇인가요?
2.  `DataLoader`를 사용할 때 `shuffle=True` 옵션이 중요한 이유는 무엇이며, `num_workers`는 어떤 역할을 하나요?
3.  `train_step()` 함수 내에서 `optimizer.zero_grad()`, `loss.backward()`, `optimizer.step()` 세 줄의 코드가 순서대로 실행되는 각 단계의 구체적인 역할과 목적을 설명하세요.