## 6월 22일 14시 수업 학습 노트

### 1. 강의 핵심 요약

오늘 수업은 PyTorch를 활용한 Convolutional Neural Network(CNN)의 핵심 구성 요소들을 상세히 다루었습니다. 특히 다채널 컨볼루션의 원리와 필터 수 결정 방식, 그리고 Feature Map의 크기 변화를 제어하는 Padding과 Pooling 기법의 중요성이 강조되었습니다. 이러한 개념들을 바탕으로 간단한 CNN 모델 아키텍처를 직접 설계하고, 각 레이어의 출력 형태와 파라미터 변화를 확인하며 딥러닝 모델의 기본 구조를 이해하는 데 초점을 맞췄습니다.

### 2. 화면 연계 타임라인 노트

*   **00:00:00 - 00:00:29 (화면 캡처: 00:00:00 - 다채널 적용)**
    *   **주제:** 다채널 Convolution 적용
    *   **설명:** 입력 Feature Map의 채널 수가 3개(예: RGB)라면, Convolution 필터의 채널 수도 3개여야 함을 설명합니다. 출력 Feature Map의 채널 수는 필터의 개수에 따라 결정되며, 단일 필터의 채널 수와는 관계없다고 강조합니다. 화면에서는 입력 Feature Map(3채널)에 2개의 필터(각각 3채널)를 적용하여 2개의 출력 Feature Map이 생성되는 과정을 보여줍니다.
*   **00:00:30 - 00:00:59 (화면 캡처: 00:00:30 - Pooling)**
    *   **주제:** Pooling 개념 소개
    *   **설명:** Pooling에 대한 내용은 잠시 뒤에 자세히 다룰 것이라고 언급하며 화면 슬라이드의 Max Pooling과 Average Pooling 예시를 빠르게 스캔합니다. Pooling을 통해 Feature Map의 크기가 줄어들고(downsampling) 있음이 시각적으로 표현됩니다.
*   **00:01:00 - 00:02:00 (화면 캡처: 00:01:00, 00:01:31 - Colab 환경 준비)**
    *   **설명:** Google Colab 환경을 열고, 이전에 작업했던 `450_CNN.ipynb` 파일을 로드하는 과정을 보여줍니다. 강사는 이미 450번의 실습을 진행했음을 언급합니다.
*   **00:02:01 - 00:03:00 (화면 캡처: 00:02:01, 00:02:31 - 기본 라이브러리 임포트)**
    *   **코드:**
        ```python
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        ```
    *   **설명:** PyTorch 라이브러리인 `torch`, 신경망 모듈 `torch.nn`, 그리고 함수형 인터페이스 `torch.nn.functional`를 임포트합니다.
*   **00:03:00 - 00:04:00 (화면 캡처: 00:03:01, 00:03:31 - 입력 텐서 생성)**
    *   **코드:** `input_tensor = torch.randn(3, 28, 28)`
    *   **설명:** 3개의 채널(예: RGB), 가로 28, 세로 28 크기를 가진 랜덤 값의 텐서를 생성합니다. 이는 28x28 크기의 RGB 이미지를 가정합니다.
    *   **코드:** `print(input_tensor.shape)` 실행 결과 `torch.Size([3, 28, 28])`이 출력됨을 확인합니다.
*   **00:04:00 - 00:05:00 (화면 캡처: 00:04:01, 00:04:31 - 첫 번째 Conv2d 레이어 정의)**
    *   **코드:** `con_lay_01 = nn.Conv2d(in_channels=3, out_channels=8, kernel_size=5, stride=1)`
    *   **설명:**
        *   `in_channels=3`: 입력 텐서의 채널 수에 맞춰 3으로 설정합니다.
        *   `out_channels=8`: 8개의 필터를 사용하여 8개의 출력 Feature Map을 생성하겠다는 의미입니다 (임의 설정).
        *   `kernel_size=5`: 5x5 크기의 컨볼루션 커널(필터)을 사용합니다.
        *   `stride=1`: 필터가 한 칸씩 이동합니다.
*   **00:05:00 - 00:06:00 (화면 캡처: 00:05:02, 00:05:32 - Conv2d 레이어 적용)**
    *   **코드:** `output_tensor = con_lay_01(input_tensor)`
    *   **설명:** 정의된 첫 번째 컨볼루션 레이어 `con_lay_01`에 `input_tensor`를 적용합니다.
*   **00:06:00 - 00:07:00 (화면 캡처: 00:06:02, 00:06:32 - 출력 텐서 형태 확인 및 계산 공식 소개)**
    *   **코드:** `print(output_tensor.shape)` 실행 결과 `torch.Size([8, 24, 24])`가 출력됨을 확인합니다.
    *   **개념:** 컨볼루션 연산 후 Feature Map의 크기 계산 공식.
    *   **공식:** `(입력크기 - 커널크기 + 2 * 패딩) / 스트라이드 + 1`
*   **00:07:00 - 00:09:00 (화면 캡처: 00:07:02, 00:08:33 - 계산 공식 적용 예시)**
    *   **계산:** `(28 - 5 + 2 * 0) / 1 + 1 = 24`
    *   **설명:** 입력 크기 28, 커널 크기 5, 패딩 0, 스트라이드 1을 공식에 대입하여 가로/세로 크기가 24로 줄어드는 것을 확인합니다. 채널 수는 `out_channels`로 지정한 8개가 됩니다.
*   **00:09:00 - 00:10:00 (화면 캡처: 00:09:03, 00:10:03 - 채널 수 증가의 의미)**
    *   **설명:** CNN에서 레이어가 깊어질수록 채널 수가 증가하는 경향이 있는데, 이는 초반에는 윤곽선과 같은 대략적인 특징을 추출하지만, 깊어질수록 물체 고유의 특이점(디테일, 질감)과 같은 구체적이고 본질적인 특징을 추출하기 위함이라고 설명합니다. 채널 수가 늘어남에 따라 특징 맵의 깊이도 깊어진다고 강조합니다.
*   **00:10:00 - 00:11:00 (화면 캡처: 00:10:03, 00:11:04 - 공간 차원 감소와 채널 깊이 심화)**
    *   **설명:** 컨볼루션 레이어를 거칠수록 가로/세로 공간 차원은 줄어들고, 채널의 깊이는 더 깊어지는 패턴을 설명합니다.
*   **00:11:00 - 00:12:00 (화면 캡처: 00:11:04, 00:12:04 - 다음 레이어 준비)**
    *   **설명:** 이러한 계산 방식은 초기 학습 단계에서 이해를 돕기 위함이며, 실제 코드 작성 시에는 PyTorch가 내부적으로 처리해 줄 것이라고 언급합니다.
*   **00:12:00 - 00:13:00 (화면 캡처: 00:12:04, 00:13:04 - 두 번째 Conv2d 레이어 정의)**
    *   **코드:** `con_lay_02 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, stride=1)`
    *   **설명:**
        *   `in_channels=8`: 이전 레이어의 `out_channels`인 8에 맞춰 설정합니다.
        *   `out_channels=16`: 16개의 필터(임의 설정).
        *   `kernel_size=3`: 3x3 커널.
        *   `stride=1`.
*   **00:13:00 - 00:14:00 (화면 캡처: 00:13:04, 00:14:04 - 두 번째 Conv2d 레이어 적용 및 결과 확인)**
    *   **코드:** `output_02 = con_lay_02(output_01)`
    *   **코드:** `print(output_02.shape)` 실행 결과 `torch.Size([16, 22, 22])`가 출력됨을 확인합니다.
    *   **계산:** `(24 - 3 + 2 * 0) / 1 + 1 = 22`로, 가로/세로 크기가 다시 22로 줄어들고 채널 수는 16개가 됩니다.
*   **00:14:00 - 00:15:00 (화면 캡처: 00:14:04, 00:15:05 - Padding 개념과 `padding='same'` 옵션)**
    *   **개념:** Padding은 입력 이미지 가장자리에 0을 추가하여 컨볼루션 후 Feature Map의 공간 차원 감소를 방지하거나 제어하는 기법입니다.
    *   **설명:** `padding=1`을 적용하면 출력 크기가 커지고, `kernel_size=5`일 때 `padding=2`를 적용하면 입력과 동일한 크기의 Feature Map을 유지할 수 있음을 수식으로 보여줍니다.
    *   **`padding='same'`:** PyTorch에서는 `padding='same'` 옵션을 통해 자동으로 패딩 값을 계산하여 입력과 동일한 크기의 출력을 얻을 수 있습니다.
*   **00:15:00 - 00:16:00 (화면 캡처: 00:15:05, 00:15:41 - Max Pooling 개념 설명)**
    *   **개념:** Pooling은 Feature Map의 특정 영역에서 대표 값(최댓값 또는 평균값)을 추출하여 크기를 줄이는(다운샘플링) 연산입니다.
    *   **목적:** 계산량을 줄이고, 모델의 위치 변화에 대한 불변성(translational invariance)을 높여 더욱 견고한 특징을 추출하기 위함입니다.
    *   **Max Pooling:** 지정된 커널 크기 내에서 최댓값을 추출하는 방식.
*   **00:16:00 - 00:17:00 (화면 캡처: 00:16:05, 00:16:42 - Max Pooling 레이어 적용)**
    *   **코드:** `pool_layer_01 = nn.MaxPool2d(kernel_size=2)`
    *   **설명:** `kernel_size=2`인 Max Pooling 레이어를 정의합니다. `stride`가 명시되지 않으면 `kernel_size`와 동일하게 설정되어 Feature Map의 가로/세로 크기를 절반으로 줄입니다.
    *   **코드:** `output_02 = pool_layer_01(output_01)`
    *   **코드:** `print(output_01.shape, output_02.shape)` 실행 결과 `torch.Size([12, 28, 28]) torch.Size([12, 14, 14])`가 출력됨을 확인합니다. (강의에서는 `output_01`을 `con_layer_01`의 출력으로 가정하고 `28x28`을 `14x14`로 줄이는 예시를 보여줌)
*   **00:17:00 - 00:18:00 (화면 캡처: 00:17:05, 00:18:00 - `torchinfo` 라이브러리 설치)**
    *   **코드:** `!pip install torchinfo`
    *   **코드:** `from torchinfo import summary`
    *   **설명:** 모델의 구조와 각 레이어의 출력 형태, 파라미터 수 등을 쉽게 확인하기 위한 `torchinfo` 라이브러리를 설치하고 임포트합니다.
*   **00:18:00 - 00:19:00 (화면 캡처: 00:18:00, 00:18:45 - CNN 모델 클래스 정의 시작)**
    *   **코드:**
        ```python
        NUM_INPUT_CHANNELS = 3
        class SimpleCNN_01(nn.Module):
            def __init__(self, num_classes=10):
                super().__init__()
                self.conv_1 = nn.Conv2d(in_channels=NUM_INPUT_CHANNELS, out_channels=32, kernel_size=3, stride=1)
                self.conv_2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1)
                self.pool = nn.MaxPool2d(kernel_size=2)
                # ... (이어짐)
        ```
    *   **설명:** `nn.Module`을 상속받는 `SimpleCNN_01` 클래스를 정의하기 시작합니다. `__init__` 메서드 내에서 첫 번째 Conv2d, 두 번째 Conv2d, MaxPool2d 레이어를 정의합니다.
*   **00:19:00 - 00:20:00 (화면 캡처: 00:19:16, 00:19:46 - Flatten 및 Fully Connected Layer 개념)**
    *   **개념:** Feature Extraction (컨볼루션 및 풀링) 단계를 거친 3차원 Feature Map을 1차원 벡터로 "평탄화(Flatten)"해야 합니다.
    *   **목적:** 평탄화된 데이터를 분류를 위한 Fully Connected(Dense) Layer의 입력으로 사용하기 위함입니다.
    *   **설명:** 일반적인 CNN 구조는 Convolution -> ReLU -> Max Pooling -> Flatten -> Fully Connected Layer -> Softmax Activation 순으로 진행됩니다.
*   **00:20:00 - 00:21:00 (화면 캡처: 00:20:16, 00:20:46 - CNN 모델 클래스 정의 계속)**
    *   **코드 (SimpleCNN_01 `__init__` 이어서):**
        ```python
                self.flatten = nn.Flatten()
                self.fc1 = nn.Linear(64 * 12 * 12, num_classes) # Corrected based on summary output
        ```
    *   **코드 (SimpleCNN_01 `forward`):**
        ```python
            def forward(self, x):
                x = self.conv_1(x)
                x = F.relu(x)
                x = self.conv_2(x)
                x = F.relu(x)
                x = self.pool(x)
                x = self.flatten(x)
                x = self.fc1(x)
                return x
        ```
    *   **설명:** Flatten 레이어를 추가하여 3D Feature Map을 1D 벡터로 변환하고, 이를 입력으로 받는 `nn.Linear` (Fully Connected Layer)를 정의합니다. `64 * 12 * 12`는 이전 풀링 레이어의 출력 형태(`[1, 64, 12, 12]`)를 기반으로 계산된 Flatten 된 벡터의 크기입니다.
*   **00:21:00 - 00:22:00 (화면 캡처: 00:21:16, 00:21:46 - 모델 인스턴스화 및 요약)**
    *   **코드:**
        ```python
        model = SimpleCNN_01(num_classes=10)
        summary(model, input_size=(1, NUM_INPUT_CHANNELS, 28, 28))
        ```
    *   **설명:** 정의한 `SimpleCNN_01` 클래스로 모델 객체를 생성하고, `torchinfo.summary`를 사용하여 모델의 전체 구조와 각 레이어의 출력 형태, 파라미터 수를 시각적으로 확인합니다. 배치 사이즈 1을 가진 3채널 28x28 이미지를 입력으로 가정합니다.
*   **00:22:00 - 00:23:00 (화면 캡처: 00:22:16, 00:22:46 - 모델 요약 결과 확인)**
    *   **결과 분석:**
        *   `Conv2d-1` (Input: 1,3,28,28): Output Shape `[1, 32, 26, 26]`
        *   `Conv2d-2` (Input: 1,32,26,26): Output Shape `[1, 64, 24, 24]`
        *   `MaxPool2d-3` (Input: 1,64,24,24): Output Shape `[1, 64, 12, 12]`
        *   `Flatten-4` (Input: 1,64,12,12): Output Shape `[1, 9216]` (즉, `64 * 12 * 12`)
        *   `Linear-5` (Input: 1,9216): Output Shape `[1, 10]`
    *   **설명:** 각 레이어를 거치면서 Feature Map의 크기가 어떻게 변하는지, Flatten을 통해 1차원 벡터로 변환되는 과정, 그리고 최종적으로 10개의 클래스로 분류되는 Linear 레이어까지의 흐름을 확인합니다.
*   **00:23:00 - 00:24:00 (화면 캡처: 00:23:16, 00:23:46 - 손실 함수 및 옵티마이저 정의)**
    *   **코드:**
        ```python
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        ```
    *   **설명:** 다중 클래스 분류에 적합한 `nn.CrossEntropyLoss`를 손실 함수로, `Adam` 옵티마이저를 사용하여 모델 파라미터를 최적화하도록 설정합니다.
*   **00:24:00 - 00:25:00 (화면 캡처: 00:24:16, 00:24:46 - 코드 설명 마무리)**
    *   **설명:** 여기까지 CNN 모델을 정의하고 학습에 필요한 기본 설정들을 마쳤습니다.

### 3. 핵심 개념 및 코드/공식 정리

#### 3.1. 컨볼루션 레이어 (`nn.Conv2d`)

*   **목적:** 이미지에서 특징(Feature)을 추출합니다. 필터(커널)를 사용하여 입력 이미지의 지역적인 패턴을 감지합니다.
*   **주요 파라미터:**
    *   `in_channels`: 입력 Feature Map의 채널 수 (예: RGB 이미지는 3).
    *   `out_channels`: 출력 Feature Map의 채널 수 (사용할 필터의 개수).
    *   `kernel_size`: 컨볼루션 필터의 크기 (예: 3x3 커널은 3).
    *   `stride`: 필터가 움직이는 보폭 (기본값 1).
    *   `padding`: 입력 이미지 주변에 0을 추가하여 출력 크기를 조절 (기본값 0).
*   **출력 Feature Map 크기 계산 공식:**
    ```
    출력크기 = (입력크기 - 커널크기 + 2 * 패딩) / 스트라이드 + 1
    ```
*   **예시 코드:**
    ```python
    import torch.nn as nn
    con_lay_01 = nn.Conv2d(in_channels=3, out_channels=8, kernel_size=5, stride=1, padding=0)
    # 입력: torch.Size([3, 28, 28]) -> 출력: torch.Size([8, 24, 24])
    # 계산: (28 - 5 + 2*0) / 1 + 1 = 24
    ```

#### 3.2. 활성화 함수 (`F.relu`)

*   **목적:** 신경망에 비선형성을 도입하여 복잡한 패턴 학습 능력을 부여합니다.
*   **ReLU (Rectified Linear Unit):** `f(x) = max(0, x)`
*   **예시 코드:**
    ```python
    import torch.nn.functional as F
    x = F.relu(x) # 컨볼루션 레이어 출력 후 적용
    ```

#### 3.3. 풀링 레이어 (`nn.MaxPool2d`)

*   **목적:** Feature Map의 공간적 크기를 줄여(다운샘플링) 계산량을 감소시키고, 모델이 위치 변화에 덜 민감하도록(translational invariance) 만듭니다.
*   **Max Pooling:** 지정된 `kernel_size` 영역 내에서 최댓값을 추출합니다.
*   **주요 파라미터:**
    *   `kernel_size`: 풀링 윈도우의 크기 (예: 2x2 풀링은 2).
    *   `stride`: 풀링 윈도우가 움직이는 보폭 (명시하지 않으면 `kernel_size`와 동일하게 설정됨).
*   **예시 코드:**
    ```python
    pool_layer_01 = nn.MaxPool2d(kernel_size=2)
    # 입력: torch.Size([12, 28, 28]) -> 출력: torch.Size([12, 14, 14])
    # 계산: 28 / 2 = 14 (stride가 kernel_size와 같을 경우)
    ```

#### 3.4. 패딩 (Padding)

*   **목적:** 컨볼루션 연산으로 인해 Feature Map의 공간 차원이 줄어드는 것을 방지하거나 조절합니다.
*   **`padding='same'`:** 입력 Feature Map과 동일한 공간 크기의 출력 Feature Map을 얻기 위해 필요한 패딩 값을 자동으로 계산하여 적용합니다.
*   **예시 코드:**
    ```python
    # padding=1 적용 시 (kernel_size=3, stride=1) 입력과 동일한 크기 유지
    con_layer = nn.Conv2d(in_channels=X, out_channels=Y, kernel_size=3, stride=1, padding=1)
    # 또는
    con_layer = nn.Conv2d(in_channels=X, out_channels=Y, kernel_size=3, stride=1, padding='same')
    ```

#### 3.5. Flatten 레이어 (`nn.Flatten`)

*   **목적:** 컨볼루션 및 풀링 레이어를 거쳐 생성된 다차원(3D) Feature Map을 1차원 벡터로 평탄화합니다.
*   **필요성:** 평탄화된 데이터는 Fully Connected Layer(MLP)의 입력으로 사용될 수 있습니다.
*   **예시 코드:**
    ```python
    flatten_layer = nn.Flatten()
    # 입력: torch.Size([배치크기, 채널, 높이, 너비])
    # 출력: torch.Size([배치크기, 채널 * 높이 * 너비])
    ```

#### 3.6. CNN 모델 (`SimpleCNN_01`) 구조

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchinfo import summary # 모델 요약을 위해 필요

NUM_INPUT_CHANNELS = 3 # 입력 이미지의 채널 수 (예: RGB)

class SimpleCNN_01(nn.Module):
    def __init__(self, num_classes=10): # num_classes: 최종 분류할 클래스 수
        super().__init__() # nn.Module의 생성자 호출

        # 첫 번째 컨볼루션 레이어
        # 입력 채널: NUM_INPUT_CHANNELS (3), 출력 채널: 32, 커널 크기: 3x3
        self.conv_1 = nn.Conv2d(in_channels=NUM_INPUT_CHANNELS, out_channels=32, kernel_size=3, stride=1)
        
        # 두 번째 컨볼루션 레이어
        # 입력 채널: 32 (이전 레이어의 출력 채널), 출력 채널: 64, 커널 크기: 3x3
        self.conv_2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1)
        
        # 맥스 풀링 레이어
        # 커널 크기: 2x2. 스트라이드는 기본적으로 커널 크기와 동일하게 설정되어,
        # Feature Map의 가로/세로 크기를 절반으로 줄임
        self.pool = nn.MaxPool2d(kernel_size=2)
        
        # Flatten 레이어: 다차원 Feature Map을 1차원 벡터로 평탄화
        self.flatten = nn.Flatten()
        
        # Fully Connected (선형) 레이어
        # 입력: (이전 Feature Map의 채널 수 * 높이 * 너비) -> 모델 요약에서 확인된 값 9216
        # 출력: num_classes (최종 분류할 클래스 수)
        self.fc1 = nn.Linear(64 * 12 * 12, num_classes) 
        # 참고: 64*12*12는 28x28 입력 이미지와 위 conv/pool 설정에 대한 계산 결과임
        # (Input 28x28) -> Conv1 (k=3, s=1, p=0) -> 26x26
        #              -> Pool1 (k=2, s=2) -> 13x13 (여기까지 32채널)
        # (Input 13x13) -> Conv2 (k=3, s=1, p=0) -> 11x11
        #              -> Pool2 (k=2, s=2) -> 5x5 (여기는 64채널)
        # --> 다시 계산: conv1(3,32,k=3,s=1)->26x26, pool1(k=2)->13x13, conv2(32,64,k=3,s=1)->11x11, pool2(k=2)->5x5 -> Flatten 64*5*5 = 1600
        # Model summary shows 9216, which means the calculations should be:
        # conv1(3,32,k=3,s=1) -> 26x26
        # pool (k=2) -> 13x13 (this is MaxPool2d with kernel_size=2 implicitly means stride=2)
        # conv2(32,64,k=3,s=1) -> 11x11 (from 13x13)
        # pool (k=2) -> 5x5
        # The summary from the lecture actually matches: 
        # Conv1: [1, 32, 26, 26]
        # Conv2: [1, 64, 24, 24] - This implies padding was 'same' or different calculations. Let's use the actual summary output.
        # MaxPool2d-3 (Input: 1,64,24,24): Output Shape [1, 64, 12, 12] 
        # This means the conv2 output (before pool) was 24x24, not 11x11.
        # So: Conv1(28x28) -> 26x26
        #     Conv2(26x26, k=3, s=1, p='same') -> 26x26 (if padding was 'same') or just plain Conv2 (k=3, s=1) -> 24x24
        #     Pool (24x24, k=2) -> 12x12
        # So 64 * 12 * 12 = 9216 is correct for this specific summary.
        # I'll use the final value from summary `9216`.

    def forward(self, x):
        # 첫 번째 컨볼루션 -> ReLU 활성화
        x = self.conv_1(x)
        x = F.relu(x)
        
        # 두 번째 컨볼루션 -> ReLU 활성화
        x = self.conv_2(x)
        x = F.relu(x)
        
        # 맥스 풀링
        x = self.pool(x)
        
        # 평탄화
        x = self.flatten(x)
        
        # Fully Connected 레이어
        x = self.fc1(x)
        
        return x

# 모델 인스턴스화 및 요약
model = SimpleCNN_01(num_classes=10)
summary(model, input_size=(1, NUM_INPUT_CHANNELS, 28, 28))

# 손실 함수 및 옵티마이저 정의
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

### 4. 학습 퀴즈

1.  CNN에서 입력 Feature Map의 채널 수가 3일 때, Conv2d 레이어의 `in_channels` 값은 얼마로 설정해야 하며, `out_channels`는 어떤 의미를 갖나요?
2.  `input_size=32`, `kernel_size=5`, `stride=1`, `padding=0`인 Conv2d 레이어를 통과한 후의 Feature Map 크기(가로/세로)는 얼마인가요? 계산 과정을 설명하세요.
3.  Max Pooling과 Padding의 주요 목적은 각각 무엇이며, PyTorch 코드에서 `padding='same'`은 어떤 기능을 제공하나요?