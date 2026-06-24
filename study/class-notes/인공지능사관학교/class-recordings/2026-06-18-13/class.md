다음은 6월 18일 13시 수업에 대한 상세 학습 노트입니다.

---

# 6_18 13시 수업 학습 노트

## 1. 강의 핵심 요약

이번 6월 18일 13시 수업은 PyTorch를 활용한 딥러닝 모델 구축의 기초를 다룹니다. 특히 `nn.Module`을 이용한 신경망 모델 정의, 데이터 준비 과정(Dataset, DataLoader), 그리고 신경망 학습의 핵심인 Training Loop의 각 단계를 상세히 설명합니다. 또한, Fashion MNIST 데이터셋을 예시로 들어 실제 코드 구현과 텐서(배열)의 차원 이해를 강조하며 실습 위주의 학습을 진행합니다.

## 2. 화면 연계 타임라인 노트

*   **00:00:00 - 00:00:40**
    *   **화면:** Google Colab 환경에서 Python 코드가 실행된 결과가 보입니다.
        *   `print(train_data.shape)`의 출력으로 `torch.Size([60000, 28, 28])`이 표시됩니다.
        *   `BATCH_SIZE = 32`로 설정 후 `DataLoader`를 사용하여 `train_loader`와 `val_loader`를 생성하는 코드가 보입니다. 이때 `num_workers=4` 설정에 대한 경고 메시지(`UserWarning: This DataLoader will create 4 worker processes...`)가 나타납니다.
        *   `images, labels = next(iter(train_loader))` 코드를 통해 첫 번째 배치 데이터를 가져온 후, `print(images.shape, labels.shape)`의 출력으로 `torch.Size([32, 1, 28, 28])` (이미지)와 `torch.Size([32])` (레이블)이 표시됩니다.
    *   **내용:** 이 초기 화면은 PyTorch `DataLoader`를 통해 Fashion MNIST와 같은 이미지 데이터셋을 로드하고 배치(batch) 형태로 처리했을 때의 텐서(Tensor) 차원을 보여주는 예시입니다. `num_workers` 설정은 데이터 로딩을 병렬 처리하여 효율을 높이지만, 특정 환경에서는 경고가 발생할 수 있음을 보여줍니다.

*   **00:00:40 - 00:01:20**
    *   **화면:** "nn.Module"이라는 제목의 PDF 슬라이드가 보입니다.
        *   `nn.Module`이 PyTorch에서 신경망의 구성 요소(Layer, Container)들의 기본 클래스(base class)임을 설명하고 있습니다.
        *   **주요 기능:**
            *   모듈화 기반으로 서브 모델들을 효과적으로 생성 지원.
            *   파라미터 자동 등록 및 관리.
            *   `forward()` 메서드 및 동적 계산 그래프 제공.
            *   `train()`, `eval()` 모드 제공.
            *   Device(cuda, cpu) 전환 제공.
        *   오른쪽에는 `class LinearModel(nn.Module)`의 예시 코드가 있습니다. `__init__`에서 `nn.Linear`와 `nn.ReLU`를 선언하고, `forward`에서 `x`를 통과시키는 과정을 보여줍니다.
    *   **내용:** PyTorch에서 신경망을 정의하는 가장 기본적인 빌딩 블록인 `nn.Module`에 대한 설명입니다. 모델을 구성하고 관리하며 순전파(forward pass)를 정의하는 핵심 클래스임을 강조합니다.

*   **00:01:20 - 00:03:21**
    *   **화면:** "서브 모델"이라는 제목의 PDF 슬라이드가 보입니다.
        *   `SimpleBlock(nn.Module)`과 `LinearModel(nn.Module)`의 두 가지 클래스 예시가 나란히 제시됩니다.
        *   `SimpleBlock`은 `nn.Linear`와 `nn.ReLU`를 묶어 하나의 재사용 가능한 블록으로 만든 예시입니다.
        *   `LinearModel`은 이러한 `SimpleBlock`을 내부적으로 사용하거나, `nn.Sequential`을 통해 여러 레이어를 순차적으로 구성하는 방법을 보여줍니다.
    *   **내용:** 신경망 모델을 모듈화하고 재사용 가능한 서브 모델(또는 블록)을 만드는 방법을 설명합니다. 이는 복잡한 신경망을 효율적으로 구성하고 관리하는 데 중요한 개념입니다.

*   **00:03:21 - 00:04:01**
    *   **화면:** "Custom 모델 주요 메서드"라는 제목의 PDF 슬라이드가 보입니다.
        *   `class LinearModel(nn.Module)` 코드와 함께 `__init__` 및 `forward` 메서드의 역할이 상세히 설명됩니다.
        *   **`__init__` (초기화 변수들):**
            *   반드시 명시적으로 부모 클래스 `nn.Module`의 `__init__`을 호출해야 합니다 (`super().__init__()`).
            *   모델에서 사용될 Layer, 서브 모델 선언.
            *   모델에서 사용될 인스턴스 변수 선언.
        *   **`forward` (모델 입력변수):**
            *   입력 `tensor`가 `layer`들을 거치면서 어떻게 처리되고 계산될지 순전파 로직을 정의합니다.
            *   모델 객체는 `Callable object`이며, `model(input_tensor)` 형태로 호출될 때 이 `forward` 메서드가 실행됩니다.
            *   입력 `tensor`를 받아서 출력 `tensor`를 반환해야 합니다 ("반드시 output tensor 반환" 강조).
            *   모델에 `forward`가 호출될 때 PyTorch는 **Computation Graph**를 생성합니다.
        *   하단에 `LinearModel`을 사용하는 예시 코드가 있습니다: `input_tensor = torch.rand(size=(64, 784))`, `linear_model = LinearModel(num_classes=10)`, `output_tensor = linear_model(input_tensor)`.
    *   **내용:** `nn.Module`을 상속받아 커스텀 모델을 만들 때 필수적으로 구현해야 하는 `__init__`과 `forward` 메서드의 역할과 중요성을 자세히 설명합니다. 특히 `forward` 메서드가 Computation Graph 생성과 관련됨을 강조합니다.

*   **00:04:01 - 00:04:42**
    *   **화면:** "Pytorch Layer"라는 제목의 PDF 슬라이드가 보입니다.
        *   PyTorch의 내장 레이어들을 사용하여 신경망을 손쉽게 만들 수 있음을 설명합니다.
        *   복잡한 텐서 연산과 학습 파라미터 구성을 쉽게 제공하며, 학습 파라미터의 자동 미분 기능이 수행됩니다.
        *   `nn.Module`을 상속받아 생성되는 다양한 레이어 유형이 나열됩니다:
            *   `nn.Linear`: Fully Connected Layer
            *   `nn.Conv2d`: Convolutional Layer
            *   `nn.ReLU`, `nn.Sigmoid`: Activation (function) Layer
            *   `nn.MaxPool2d`: Pooling Layer
            *   `nn.BatchNorm2d`: Normalization Layer
        *   `nn.Linear`, `nn.Conv2d`, `nn.ReLU`, `nn.Sigmoid`에는 밑줄이 그어져 있습니다.
    *   **내용:** PyTorch가 제공하는 다양한 `nn` 모듈 내의 레이어들을 소개하고, 이들이 신경망 구축을 얼마나 용이하게 하는지 설명합니다.

*   **00:04:42 - 00:05:22**
    *   **화면:** "Pytorch 모델 구축"이라는 제목과 함께 딥러닝 모델 구축의 전체 워크플로우를 보여주는 다이어그램이 보입니다.
        *   **데이터 준비 (DATA):** 데이터 전처리, Augmentation, Normalization, Tensor 변환, Dataset, DataLoader.
        *   **네트워크 모델 생성:** Custom 모델 작성, Pretrained 모델 활용.
        *   **학습 수행:** Loss, Optimizer, Training Loop, 검증.
        *   **예측 및 평가:** 모델 테스트 예측, 모델 테스트 평가 (빨간색 동그라미로 강조).
        *   **최적화:** 하이퍼 파라미터 튜닝, 모델 재구성, Augmentation 변경 (빨간색 동그라미로 강조).
    *   **내용:** PyTorch를 이용한 딥러닝 프로젝트의 전반적인 라이프사이클을 개괄적으로 설명합니다. 각 단계의 주요 요소들을 시각적으로 제시하여 전체적인 흐름을 이해할 수 있도록 돕습니다. 특히 예측 및 평가와 최적화 부분이 강조되어 있습니다.

*   **00:05:22 - 00:06:02**
    *   **화면:** "Fashion MNIST 모델"이라는 제목과 함께 Fashion MNIST 데이터셋의 이미지 그리드가 보입니다.
        *   다양한 의류 이미지가 흑백으로 배열되어 있습니다.
        *   오른쪽 상단에 "lab"이라고 손글씨로 적혀 있습니다.
    *   **내용:** 이번 수업에서 활용할 예시 데이터셋인 Fashion MNIST를 시각적으로 소개합니다. 이는 실제 코드를 통해 다룰 데이터임을 암시합니다.

*   **00:06:02 - 00:06:42**
    *   **화면:** "배열(텐서) 차원"이라는 제목의 PDF 슬라이드가 보입니다.
        *   **정형 데이터:** 테이블 형태의 데이터를 2차원(`(samples, features)`)으로 설명.
        *   **Grayscale 이미지:** 단일 흑백 이미지를 2차원(`(height, width)`)으로 설명.
        *   **RGB 이미지:** 컬러 이미지를 3차원(`(height, width, channels)`)으로 설명.
        *   각 그림 아래에 손글씨로 "2차원" 또는 "3차원"이 적혀 있습니다.
    *   **내용:** 데이터의 종류(정형 데이터, 흑백 이미지, 컬러 이미지)에 따른 텐서의 차원(dimension)을 설명합니다. (이 부분은 뒤에서 PyTorch `DataLoader`의 출력 형태에 맞춰 다시 한번 더 정확하게 설명됩니다.)

*   **00:06:42 - 00:07:23**
    *   **화면:** "Cross Entropy Loss"라는 제목의 PDF 슬라이드가 보입니다.
        *   신경망의 최종 출력인 `logit`이 `Softmax` 또는 `Sigmoid`를 통해 `예측 확률`로 변환되는 과정이 시각적으로 표현됩니다.
        *   `예측 확률`($\hat{y}_i$)과 `실제 값`($y_i$)을 비교하여 `Cross Entropy Loss`를 계산하고, 이 Loss 값이 `Gradient Descent` 계산에 사용됨을 보여줍니다.
        *   **Multi Class일 경우 Cross Entropy Loss 공식:**
            $L = -\frac{1}{m}\sum_{i=1}^{m} y_i \cdot \log(\hat{y}_i)$
        *   **Binary Class일 경우 Binary Cross Entropy Loss 공식:**
            $L = -\frac{1}{m}\sum_{i=1}^{m} [y_i \cdot \log(\hat{y}_i) + (1 - y_i) \cdot \log(1 - \hat{y}_i)]$
        *   PyTorch에서는 Categorical Cross Entropy Loss를 Cross Entropy Loss로 통칭한다고 설명합니다.
    *   **내용:** 분류 문제에서 널리 사용되는 Cross Entropy Loss의 개념, 계산 방식, 그리고 Multi-Class와 Binary Class 상황에서의 공식을 설명합니다.

*   **00:07:23 - 00:08:03**
    *   **화면:** 손실 함수의 3D 표면을 보여주는 그래프가 나타납니다.
        *   그래프에는 `Local Minima` (지역 최솟값), `Global Minima` (전역 최솟값), `Saddle Point` (안장점)가 표시되어 있습니다.
        *   텍스트는 "보다 최적으로 GD를 적용"해야 하며, "최소 Loss로 보다 빠르고 안정적으로 수렴할 수 있는 기법 적용 필요"라고 설명합니다.
        *   다음 슬라이드 주제가 "Optimizer"임을 암시합니다.
    *   **내용:** 최적화 과정에서 손실 함수가 가질 수 있는 다양한 형태와 그에 따른 최적화의 어려움(지역 최솟값, 안장점)을 시각적으로 설명합니다. 이를 극복하기 위한 최적화 기법(Optimizer)의 필요성을 강조합니다.

*   **00:08:03 - 00:15:25**
    *   **화면:** "Training Loop"라는 제목의 PDF 슬라이드가 보입니다. 이 슬라이드에 많은 손글씨와 강조 표시가 추가됩니다.
        *   **핵심 메시지:** PyTorch의 신경망 생성 및 학습(Training) 로직은 `Loosely Coupled` (느슨하게 연결)되어 있습니다.
        *   **Training 로직 설명:** 모델의 출력 텐서 값을 Loss 함수 및 Optimizer를 이용하여 backpropagation 기반으로 Weight(가중치) 파라미터를 Update 수행. 데이터의 batch 단위로 반복 수행하며, 전체 학습 데이터를 epochs 지정된 횟수만큼 수행.
        *   **좌측 다이어그램:** `Data` -> `Forward Pass` -> `= Loss?` -> `Backward Pass` -> `Update Network`의 흐름을 보여줍니다.
        *   **우측 Mini-batch loop 상세 단계 (코드 블록):**
            1.  **`Forward Pass`**: `outputs = model(inputs)` (입력 데이터를 모델에 넣어 예측값을 얻는 과정. `model(inputs)`와 연결됨).
            2.  **`Loss 계산`**: `loss = loss_fn(outputs, targets)` (모델의 예측값과 실제 레이블을 비교하여 손실 값을 계산).
            3.  **`Optimizer gradient 초기화`**: `optimizer.zero_grad()` (이전 학습 스텝에서 누적된 기울기(gradient)를 0으로 초기화. `X` 표시로 제거를 강조).
            4.  **`Gradient 계산`**: `loss.backward()` (계산된 손실(`loss`)을 사용하여 역전파(backpropagation)를 통해 모델의 각 파라미터에 대한 기울기를 계산. 화살표로 연결됨).
            5.  **`학습 파라미터 업데이트`**: `optimizer.step()` (계산된 기울기를 사용하여 모델의 가중치(`W`)를 업데이트. `W-`와 화살표로 설명됨).
        *   `Epoch loop`와 `Mini-batch loop`가 큰 동그라미로 묶여있어 학습의 반복 구조를 나타냅니다.
    *   **내용:** 신경망 학습의 핵심인 Training Loop의 각 단계를 매우 상세하고 시각적으로 설명합니다. Forward Pass, Loss 계산, Backward Pass, 그리고 Optimizer를 통한 가중치 업데이트가 어떻게 유기적으로 연결되는지 강조합니다.

*   **00:15:25 - 00:17:26**
    *   **화면:** Google Colab 환경에서 강사가 우측 상단의 "연결" 드롭다운 메뉴를 클릭하여 "세션 관리"로 이동합니다. 이후 런타임이 재시작되고 빈 코드 셀이 나타납니다.
    *   **내용:** Colab 런타임을 재시작하는 과정을 보여줍니다. 이는 보통 이전 실행으로 인한 메모리 초기화나 환경 설정 변경 시 수행됩니다.

*   **00:17:26 - 00:20:07**
    *   **화면:** 다시 "Training Loop" PDF 슬라이드로 돌아옵니다. 이전과 동일한 내용이며, 추가적인 필기나 강조는 없습니다.
    *   **내용:** 앞서 설명했던 Training Loop 개념을 다시 한번 복습하거나 강조하는 시간으로 추정됩니다.

*   **00:25:31 - 00:26:51**
    *   **화면:** Google Colab 코드 셀에서 PyTorch 데이터 로딩에 필요한 모듈들을 임포트하는 코드를 작성합니다.
        ```python
        from torchvision import datasets
        from torchvision.transforms import ToTensor
        from torch.utils.data import DataLoader
        ```
    *   **내용:** 데이터셋을 불러오고 텐서로 변환하며, 배치 형태로 효율적으로 로딩하기 위한 필수적인 PyTorch 라이브러리 임포트 과정을 보여줍니다.

*   **00:26:51 - 00:28:52**
    *   **화면:** Colab 코드 셀에서 Fashion MNIST 데이터셋을 로드하는 코드를 작성합니다.
        ```python
        train_data = datasets.FashionMNIST(root='data', train=True, download=True, transform=ToTensor())
        val_data = datasets.FashionMNIST(root='data', train=False, download=True, transform=ToTensor())
        ```
    *   **내용:** `torchvision.datasets.FashionMNIST`를 사용하여 학습(train) 데이터와 검증(validation) 데이터를 로컬 'data' 폴더에 다운로드하고, `ToTensor()`를 통해 PyTorch 텐서 형식으로 변환하는 과정을 보여줍니다. `train=True`는 학습용, `train=False`는 검증용 데이터를 의미합니다.

*   **00:28:52 - 00:30:53**
    *   **화면:** Colab에서 Google Drive를 마운트하는 코드를 입력하고 실행합니다.
        ```python
        from google.colab import drive
        drive.mount('/content/drive')
        ```
        이후 Google Drive 인증을 위한 팝업창이 나타나고, 사용자가 인증을 진행하는 화면이 잠시 보입니다.
    *   **내용:** Colab 환경에서 외부 저장소(Google Drive)에 접근하여 데이터를 저장하거나 불러오기 위해 드라이브를 마운트하는 과정을 시연합니다.

*   **00:30:53 - 00:32:13**
    *   **화면:** 파일 탐색기에서 'data' 폴더가 생성된 것을 확인할 수 있습니다. 이어서 코드 셀에서 `print(len(val_data))`를 실행하고, 출력 결과로 `10000`이 표시됩니다.
    *   **내용:** Fashion MNIST 검증 데이터셋의 개수가 10,000개임을 확인합니다.

*   **00:32:13 - 00:33:34**
    *   **화면:** 코드 셀에서 `print(len(train_data))`를 실행하고, 출력 결과로 `60000`이 표시됩니다. 이어서 `print(train_data.data.shape)`를 실행하고, 출력 결과로 `torch.Size([60000, 28, 28])`이 표시됩니다.
    *   **내용:** Fashion MNIST 학습 데이터셋의 개수가 60,000개이며, 각 이미지는 28x28 픽셀 크기임을 확인합니다. `train_data.data.shape`는 데이터셋 내 이미지들의 전체 텐서 차원을 나타냅니다 (이미지 수, 높이, 너비).

*   **00:33:34 - 00:35:35**
    *   **화면:** `BATCH_SIZE = 32`를 정의한 후 `DataLoader`를 생성하는 코드를 작성합니다.
        ```python
        BATCH_SIZE = 32
        train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
        val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
        ```
        다시 `num_workers=4` 설정에 대한 경고 메시지가 나타납니다.
    *   **내용:** 학습 효율을 위해 `BATCH_SIZE`를 설정하고, `DataLoader`를 사용하여 학습 및 검증 데이터를 배치 단위로 섞어서(`shuffle=True`) 로드할 준비를 합니다. `num_workers`를 설정하여 데이터 로딩을 병렬 처리합니다.

*   **00:35:35 - 00:39:36**
    *   **화면:** 코드 셀에서 `images, labels = next(iter(train_loader))` 코드를 실행하여 `train_loader`에서 첫 번째 이미지 배치와 해당 레이블 배치를 가져옵니다.
        이어서 `print(images.shape, labels.shape)`를 실행하고, 출력 결과로 `torch.Size([32, 1, 28, 28])`와 `torch.Size([32])`가 표시됩니다.
    *   **내용:** `DataLoader`가 반환하는 데이터의 실제 차원을 확인합니다. `images`는 (배치 크기, 채널 수, 이미지 높이, 이미지 너비) 형태이며, `labels`는 (배치 크기) 형태임을 명확히 보여줍니다. Fashion MNIST는 흑백 이미지이므로 채널 수는 1입니다.

*   **00:39:36 - 00:40:56**
    *   **화면:** 다시 "배열(텐서) 차원" PDF 슬라이드로 돌아옵니다. 이전 슬라이드에서 설명했던 차원 개념을 PyTorch `DataLoader`의 출력 형태에 맞춰 수정 및 보완하여 설명합니다.
        *   **Grayscale 이미지:** 이전에는 2차원이라고 설명했지만, 이제 **3차원 (Batch_Size, Height, Width)**으로 설명합니다. (실제 PyTorch에서는 보통 Channel 차원이 1로 포함되어 4차원 `(Batch, Channel, Height, Width)`이 되지만, 여기서는 Grayscale 이미지를 단일 채널로 간주하고 Batch 차원을 추가한 형태로 설명하는 것으로 보입니다.)
        *   **RGB 이미지:** 이전에는 3차원이라고 설명했지만, 이제 **4차원 (Batch_Size, Channel, Height, Width)**으로 설명합니다.
        *   각 그림 아래에 손글씨로 "3차원" 또는 "4차원"이 새로이 적혀 있습니다.
    *   **내용:** PyTorch의 `DataLoader`가 데이터를 배치(Batch) 형태로 제공할 때, 데이터의 차원이 어떻게 구성되는지 (특히 Batch 차원과 Channel 차원의 위치)를 명확히 설명합니다. 이는 딥러닝 모델에 데이터를 입력할 때 매우 중요한 개념입니다.

*   **00:40:56 - 00:43:37**
    *   **화면:** 다시 Colab 환경으로 돌아와 `DataLoader`에서 얻은 `images.shape` (`torch.Size([32, 1, 28, 28])`) 결과를 다시 한번 보여주며, 방금 설명한 텐서 차원 개념과 실제 코드 결과가 일치함을 강조합니다.
    *   **내용:** 코드 실행 결과와 이론적인 차원 설명을 연결하여 수강생들의 이해를 돕습니다. Batch, Channel, Height, Width의 순서가 명확하게 인지되도록 합니다.

## 3. 핵심 개념 및 코드/공식 정리

### 3.1. PyTorch `nn.Module`과 모델 구축

*   **`nn.Module`**: PyTorch에서 모든 신경망 모듈(레이어, 커스텀 모델 등)의 기반 클래스입니다.
    *   **주요 역할:**
        *   신경망 레이어 및 전체 모델 정의.
        *   모델 파라미터(가중치, 편향) 자동 등록 및 관리.
        *   `forward()` 메서드를 통해 순전파 로직 정의.
        *   학습(train) 및 평가(eval) 모드 전환 기능.
        *   CPU/GPU 간 모델 이동(`.to(device)`) 지원.
    *   **주요 메서드:**
        *   `__init__(self, ...)`:
            *   반드시 `super().__init__()`를 호출하여 부모 클래스 초기화.
            *   모델에서 사용할 레이어(`nn.Linear`, `nn.Conv2d` 등)나 다른 `nn.Module` 서브클래스(서브 모델)를 인스턴스 변수로 선언.
        *   `forward(self, x)`:
            *   입력 텐서 `x`가 모델의 각 레이어를 어떻게 통과하여 최종 출력 텐서를 생성하는지 정의.
            *   호출 가능한 객체(`model(input)`) 형태로 모델이 사용될 때 이 메서드가 실행됩니다.
            *   계산 그래프(Computation Graph)가 이 과정에서 동적으로 생성됩니다.
            *   **반드시** 최종 출력 텐서를 반환해야 합니다.

*   **예시 `LinearModel` 구조:**
    ```python
    import torch.nn as nn

    class LinearModel(nn.Module):
        def __init__(self, num_classes=10):
            super().__init__() # 반드시 부모 클래스 초기화
            self.linear_01 = nn.Linear(in_features=784, out_features=100)
            self.relu_01 = nn.ReLU()
            self.linear_02 = nn.Linear(in_features=100, out_features=num_classes)

        def forward(self, x):
            x = self.linear_01(x)
            x = self.relu_01(x)
            output = self.linear_02(x)
            return output
    ```

*   **PyTorch Layer 종류 (예시):**
    *   `nn.Linear`: Fully Connected Layer
    *   `nn.Conv2d`: Convolutional Layer
    *   `nn.ReLU`, `nn.Sigmoid`: Activation Function Layer
    *   `nn.MaxPool2d`: Pooling Layer
    *   `nn.BatchNorm2d`: Normalization Layer

### 3.2. 데이터 준비 (Fashion MNIST 예시)

*   **`torchvision.datasets`**: 다양한 표준 데이터셋을 제공합니다.
*   **`torchvision.transforms.ToTensor()`**: PIL Image나 NumPy 배열을 PyTorch 텐서로 변환하고, 픽셀 값을 [0, 255]에서 [0.0, 1.0]으로 정규화합니다.
*   **`torch.utils.data.DataLoader`**: Dataset을 래핑하여 데이터에 대한 이터러블(iterable)을 제공합니다.
    *   `batch_size`: 한 번에 로드할 샘플의 수.
    *   `shuffle`: 에폭마다 데이터를 섞을지 여부. 학습 시에는 `True`로 설정하여 모델의 일반화 성능을 향상시킵니다.
    *   `num_workers`: 데이터 로딩을 병렬로 처리할 워커 프로세스의 수. I/O 작업이 많을 때 학습 속도를 높일 수 있습니다. (CPU 코어 수에 맞게 설정하거나, Colab 환경에서는 경고를 피하기 위해 0 또는 작은 값으로 설정하기도 합니다.)

*   **데이터 로딩 코드:**
    ```python
    from torchvision import datasets
    from torchvision.transforms import ToTensor
    from torch.utils.data import DataLoader

    # FashionMNIST 데이터셋 로드
    train_data = datasets.FashionMNIST(
        root='data',          # 데이터가 저장될 경로
        train=True,           # 학습 데이터셋
        download=True,        # 데이터가 없으면 다운로드
        transform=ToTensor()  # 데이터를 PyTorch 텐서로 변환
    )
    val_data = datasets.FashionMNIST(
        root='data',
        train=False,          # 검증 데이터셋
        download=True,
        transform=ToTensor()
    )

    print(f"학습 데이터 개수: {len(train_data)}") # 예: 60000
    print(f"검증 데이터 개수: {len(val_data)}") # 예: 10000
    print(f"학습 데이터 원본 텐서 shape: {train_data.data.shape}") # 예: torch.Size([60000, 28, 28])

    BATCH_SIZE = 32

    # DataLoader 생성
    train_loader = DataLoader(
        train_data,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=4
    )
    val_loader = DataLoader(
        val_data,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=4
    )

    # DataLoader에서 한 배치(batch) 데이터 가져오기
    images, labels = next(iter(train_loader))
    print(f"이미지 배치 shape: {images.shape}") # 예: torch.Size([32, 1, 28, 28])
    print(f"레이블 배치 shape: {labels.shape}") # 예: torch.Size([32])
    ```

### 3.3. 배열 (텐서) 차원 이해

데이터의 차원은 딥러닝 모델 설계에 매우 중요합니다.

*   **정형 데이터 (Tabular Data):**
    *   일반적으로 2차원: `(샘플 수, 특성 수)`
*   **Grayscale 이미지 (흑백 이미지):**
    *   단일 이미지: `(높이, 너비)` (2차원)
    *   PyTorch `DataLoader`에서 배치 처리 시: `(Batch_Size, Channel, Height, Width)`
        *   여기서 `Channel`은 1 (흑백)이므로: `(Batch_Size, 1, Height, Width)` (4차원)
        *   강의 슬라이드에서는 (Batch_Size, Height, Width)를 3차원으로 설명하며 채널을 묵시적으로 포함하기도 함.
*   **RGB 이미지 (컬러 이미지):**
    *   단일 이미지: `(높이, 너비, 채널)` (3차원) 또는 PyTorch의 경우 `(채널, 높이, 너비)`
    *   PyTorch `DataLoader`에서 배치 처리 시: `(Batch_Size, Channel, Height, Width)` (4차원)
        *   여기서 `Channel`은 3 (빨강, 초록, 파랑)이므로: `(Batch_Size, 3, Height, Width)`

### 3.4. Cross Entropy Loss

*   **목적:** 분류 모델의 성능을 측정하는 손실 함수. 주로 모델의 예측 확률 분포와 실제 레이블의 확률 분포 간의 차이를 계산.
*   **작동 방식:**
    1.  신경망의 최종 출력 `logit`을 `Softmax` (다중 클래스) 또는 `Sigmoid` (이진 클래스)를 통해 `예측 확률`($\hat{y}_i$)로 변환.
    2.  `예측 확률`($\hat{y}_i$)과 `실제 값`($y_i$)을 비교하여 손실($L$)을 계산.
*   **공식:**
    *   **Multi Class (Categorical Cross Entropy Loss):**
        $L = -\frac{1}{m}\sum_{i=1}^{m} y_i \cdot \log(\hat{y}_i)$
        (여기서 $m$은 샘플 수, $y_i$는 실제 클래스 (원-핫 인코딩), $\hat{y}_i$는 예측 확률)
    *   **Binary Class (Binary Cross Entropy Loss):**
        $L = -\frac{1}{m}\sum_{i=1}^{m} [y_i \cdot \log(\hat{y}_i) + (1 - y_i) \cdot \log(1 - \hat{y}_i)]$
        (여기서 $m$은 샘플 수, $y_i$는 실제 값 (0 또는 1), $\hat{y}_i$는 예측 확률)
*   **PyTorch에서의 명칭:** PyTorch에서는 Categorical Cross Entropy Loss를 일반적으로 "Cross Entropy Loss"로 지칭합니다.

### 3.5. Training Loop (학습 반복)

신경망 학습의 핵심 프로세스로, `Epoch loop`와 `Mini-batch loop`로 구성됩니다.

*   **Training Loop의 5단계 (Mini-batch loop 기준):**
    1.  **Forward Pass**: `outputs = model(inputs)`
        *   **목적:** 입력 데이터(`inputs`)를 신경망 모델(`model`)에 통과시켜 예측값(`outputs`)을 생성합니다.
    2.  **Loss 계산 (Loss Calculation)**: `loss = loss_fn(outputs, targets)`
        *   **목적:** 모델의 예측값(`outputs`)과 실제 정답 레이블(`targets`)을 비교하여 모델의 성능을 나타내는 손실 값(`loss`)을 계산합니다.
    3.  **Optimizer Gradient 초기화 (Optimizer Gradient Initialization)**: `optimizer.zero_grad()`
        *   **목적:** 이전 학습 스텝에서 계산되어 Optimizer에 누적되어 있을 수 있는 모든 파라미터의 기울기(`gradient`)를 0으로 초기화합니다. 이는 현재 스텝의 기울기가 이전 스텝의 기울기와 합쳐지지 않도록 방지합니다.
    4.  **Gradient 계산 (Gradient Calculation)**: `loss.backward()`
        *   **목적:** 계산된 손실(`loss`)을 사용하여 역전파(Backpropagation) 알고리즘을 통해 모델의 각 학습 가능한 파라미터(가중치, 편향)에 대한 기울기를 계산합니다.
    5.  **학습 파라미터 업데이트 (Parameter Update)**: `optimizer.step()`
        *   **목적:** 계산된 기울기를 바탕으로 Optimizer가 모델의 가중치와 편향을 업데이트하여 손실을 최소화하는 방향으로 모델을 개선합니다.

## 4. 학습 퀴즈

1.  PyTorch에서 신경망 모델을 구축할 때 모든 레이어와 커스텀 모델의 기반이 되는 클래스는 무엇이며, 이 클래스가 제공하는 주요 기능 중 `__init__` 메서드와 `forward` 메서드의 각각의 역할은 무엇인지 설명하시오.
2.  `torchvision.datasets.FashionMNIST`를 사용하여 데이터를 로드하고 `torch.utils.data.DataLoader`로 배치 데이터를 준비할 때, `transform=ToTensor()`의 역할과 `DataLoader`에서 `num_workers` 인자를 사용하는 목적, 그리고 이 인자 사용 시 발생할 수 있는 일반적인 경고 메시지는 무엇입니까?
3.  PyTorch 신경망 학습의 핵심인 Training Loop (Mini-batch loop)의 다섯 가지 주요 단계를 순서대로 나열하고, 각 단계에서 어떤 코드가 주로 사용되며 해당 코드의 목적이 무엇인지 간략히 설명하시오.

---