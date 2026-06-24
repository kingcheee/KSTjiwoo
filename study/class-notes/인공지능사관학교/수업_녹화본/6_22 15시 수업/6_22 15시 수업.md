## 6_22 15시 수업 학습 노트: CNN Global Average Pooling 적용

### 1. 강의 핵심 요약

오늘의 강의는 Convolutional Neural Network (CNN) 모델에서 피처 맵을 완전 연결 계층(Fully Connected Layer)에 연결하는 두 가지 방법, 즉 **Flatten** 방식과 **Global Average Pooling (GAP)** 방식을 비교 분석합니다. 강사님은 특히 PyTorch의 `nn.AdaptiveAvgPool2d(output_size=(1,1))`를 활용한 GAP 구현 방법을 상세히 설명하며, 이 방식이 모델을 더욱 간결하고 유연하게 만들 뿐만 아니라 다양한 입력 크기에 대한 견고성을 제공한다는 핵심 메시지를 전달합니다. Flatten 방식이 고정된 입력 크기를 요구하는 반면, GAP는 각 채널의 대표값을 1x1 크기로 줄여 `in_features`를 고정시킴으로써 모델의 확장성과 효율성을 크게 향상시킵니다.

---

### 2. 화면 연계 타임라인 노트

*   **00:00:00 - 00:05:00**:
    *   **화면:** `SimpleCNN_01` 모델의 `summary` 테이블이 표시됩니다. 특히 `Flatten (flatten)` 레이어의 `Input Shape`이 `[1, 64, 14, 14]`이고 `Output Shape`이 `[1, 12544]`임을 보여줍니다.
    *   **내용:** 강사님은 기존 `SimpleCNN_01` 모델에서 `(64, 14, 14)` 크기의 피처 맵이 `Flatten` 레이어를 통해 `12544`개의 값으로 평탄화(flatten)되는 과정을 설명합니다. 이 많은 숫자가 다음 레이어로 전달되어야 함을 강조합니다.

*   **00:05:00 - 00:20:00**:
    *   **화면:** "CNN Global Average Pooling"이라는 제목의 PDF 슬라이드가 나타나며, Flatten 방식(좌측)과 GAP 방식(우측)의 시각적 비교가 포함되어 있습니다. Flatten 방식은 `feature maps` 다음에 `Fully connected layers`가 오고, GAP 방식은 `feature maps` 다음에 `GAP`를 거쳐 `Fully connected layers`로 이어집니다.
    *   **내용:** `(64, 14, 14)`와 같은 원본 피처 맵이 Flatten을 거치면 `12544`개라는 방대한 양이 되며, 이는 계산 복잡성을 야기합니다. 강사님은 이 문제를 해결하기 위해 `Global Average Pooling`을 도입할 것임을 시사합니다.

*   **00:20:00 - 00:35:00**:
    *   **내용:** `12,544`개라는 많은 숫자를 처리하는 것이 번거롭고, `connection pool layer` (아마도 pooling layer)를 계산하는 과정이 복잡하다고 언급합니다.

*   **00:35:00 - 00:53:00**:
    *   **화면:** 다시 PDF 슬라이드 "CNN Global Average Pooling"이 표시되며, GAP 방식의 단순화된 구조를 강조합니다.
    *   **내용:** `Global Average Pooling`이 적용된 모델 구조가 시각적으로 훨씬 간편하고 깔끔하게 보인다고 설명하며, 모델의 연결이 단순해짐을 강조합니다.

*   **00:53:00 - 01:13:00**:
    *   **화면:** PDF 슬라이드에서 `GAP` 박스 안에 `Pytorch에서는 AdaptiveAveragePool2d(output_size=(1,1))로 GAP 적용`이라는 문구가 명확히 보입니다.
    *   **내용:** GAP는 각 피처 맵의 "대표 평균값"만 추출하여 `1x1` 크기로 만듦으로써, 방대한 데이터를 하나로 응축하고 바로 다음 레이어(다이다이)로 연결할 수 있어 모델이 훨씬 효율적이고 간결해진다고 설명합니다.

*   **01:13:00 - 01:45:00**:
    *   **화면:** 다시 Colab의 `SimpleCNN_01` 코드와 `summary` 테이블이 있는 화면으로 돌아옵니다. 이후 기존 `SimpleCNN_01` 클래스를 복사하여 `SimpleCNN_02`로 이름을 변경하는 과정이 나타납니다.
    *   **내용:** 강사님은 앞에서 설명한 GAP의 장점을 실제 코드로 구현하기 위해 기존 모델(`SimpleCNN_01`)을 복사하여 `SimpleCNN_02` 클래스를 만들고 수정할 준비를 합니다.

*   **01:45:00 - 02:35:00**:
    *   **화면:** `SimpleCNN_02` 클래스 내 `__init__` 메서드에서 `self.flatten = nn.Flatten()` 라인이 주석 처리되고, `self.adapt_pool = nn.AdaptiveAvgPool2d(`를 입력하는 장면이 보입니다. PyTorch의 `nn` 모듈 내 다양한 `Adaptive` 풀링 옵션(`AdaptiveAvgPool2d`, `AdaptiveMaxPool2d` 등) 목록이 팝업으로 나타납니다.
    *   **내용:** `Flatten` 레이어를 제거하고, `nn.AdaptiveAvgPool2d`를 사용하여 `Global Average Pooling`을 구현할 것임을 밝힙니다.

*   **02:35:00 - 03:27:00**:
    *   **화면:** `self.adapt_pool = nn.AdaptiveAvgPool2d(output_size=(1,1))` 코드가 완성됩니다.
    *   **내용:** `output_size=(1,1)`로 설정하여 각 피처 맵을 `1x1` 크기의 단일 값으로 줄이는 GAP의 핵심 동작을 정의합니다. 이렇게 함으로써 데이터가 Flatten된 것처럼 1차원 벡터 형태로 준비됨을 설명합니다.

*   **03:27:00 - 04:19:00**:
    *   **화면:** `self.classifier = nn.Linear(in_features=64, out_features=num_classes)` 코드가 보입니다.
    *   **내용:** `AdaptiveAvgPool2d`의 출력은 각 피처 맵이 `1x1`로 압축된 형태이므로, 이전 `Conv2d` 레이어의 `out_channels` 수(여기서는 64)가 `nn.Linear` 레이어의 `in_features` 값이 됩니다. Flatten 방식의 `12544`개와 달리 `64`개로 크게 줄어드는 것을 강조합니다.

*   **04:19:00 - 05:34:00**:
    *   **화면:** `forward` 메서드 내에서 `x = self.flatten(x)` 라인이 주석 처리되고, `x = self.adapt_pool(x)`와 `x = torch.flatten(x, start_dim=1)`이 추가됩니다.
    *   **내용:** `AdaptiveAvgPool2d`는 `(batch_size, channels, 1, 1)` 형태의 출력을 내므로, 이를 `nn.Linear`에 넣기 위해서는 배치 차원을 제외한 나머지 차원(`channels`, `1`, `1`)을 평탄화해야 합니다. `torch.flatten(x, start_dim=1)`을 사용하여 배치 차원(`start_dim=0`)은 유지하고 그 다음부터 평탄화하여 `(batch_size, channels)` 형태로 만듭니다.

*   **05:34:00 - 06:16:00**:
    *   **화면:** `SimpleCNN_02` 모델에 대한 테스트 코드(`input = torch.randn(...)`, `output = simple_cnn02(input)`, `print(output.shape)`)와 `summary` 함수 호출 코드를 `SimpleCNN_02`에 맞춰 수정합니다.
    *   **내용:** 변경된 모델을 테스트하기 위해 기존 테스트 코드를 수정하고, 모델의 출력 형태와 `summary`를 통해 변경 사항을 확인하겠다고 안내합니다.

*   **06:16:00 - 07:32:00**:
    *   **화면:** `summary(model=simple_cnn02, input_size=(1, 3, 32, 32))` 실행 결과가 나타납니다. `AdaptiveAvgPool2d` 레이어의 `Output Shape`이 `[1, 64, 1, 1]`이고, 그 다음 `torch.flatten`의 `Output Shape`이 `[1, 64]`이며, `Linear` 레이어의 최종 `Output Shape`이 `[1, 10]`임을 보여줍니다.
    *   **내용:** `AdaptiveAvgPool2d` 적용 후 최종 출력이 `(1, 10)`으로 나옴을 확인합니다. `summary`를 통해 `(14, 14)` 크기의 피처 맵이 `AdaptiveAvgPool2d`를 거쳐 `(1, 1)`로 줄어들고, `torch.flatten`을 통해 `64`개의 특성으로 평탄화되는 과정을 시각적으로 확인시켜 줍니다.

*   **07:32:00 - 08:35:00**:
    *   **화면:** `summary` 결과에서 `AdaptiveAvgPool2d (adapt_pool)` 레이어의 `Input Shape`이 `[1, 64, 6, 6]`이고 `Output Shape`이 `[1, 64, 1, 1]`임을 강조하며, `torch.flatten` 레이어의 `Input Shape` `[1, 64, 1, 1]`이 `Output Shape` `[1, 64]`로 변환되는 부분을 명확히 보여줍니다.
    *   **내용:** 강사님은 `AdaptiveAvgPool2d(output_size=(1,1))`가 실제로는 이전 레이어에서 나온 `(6, 6)` 크기(예시로)를 `(1, 1)`로 변환하는 역할을 수행하며, 각 채널의 정보를 단일 대표값으로 압축한다고 다시 한번 설명합니다. 이후 `torch.flatten(x, start_dim=1)`이 `(1, 64, 1, 1)` 형태를 `(1, 64)` 형태로 변환하여 `Linear` 레이어에 적합하게 만든다는 점을 재차 강조합니다.

*   **08:35:00 - 10:12:00**:
    *   **내용:** `AdaptiveAvgPool2d`의 핵심 기능은 각 채널당 단 하나의 대표값(1x1)만 남기는 것이며, 이는 `14x14`였던 것을 `1x1`로 압축하는 "혁신"적인 변화라고 설명합니다. 결과적으로 `Linear` 레이어는 고정된 `64`개의 `in_features`를 받게 됩니다.

*   **10:12:00 - 10:52:00**:
    *   **내용:** `AdaptiveAvgPool2d`의 가장 큰 장점 중 하나는 **입력 데이터의 크기에 유연하게 대응**한다는 점을 강조합니다. 예를 들어, `(1, 3, 32, 32)` 대신 `(1, 3, 64, 64)`와 같은 더 큰 이미지를 입력으로 주더라도 모델이 에러 없이 동작함을 설명합니다. 이는 `AdaptiveAvgPool2d`가 항상 `1x1` 출력을 보장하기 때문입니다.

*   **10:52:00 - 12:35:00**:
    *   **화면:** `input = torch.randn(1, 3, 64, 64)`로 변경하여 `summary`를 실행한 결과가 나타납니다. 첫 번째 `MaxPool2d`의 `Output Shape`이 `[1, 32, 30, 30]`이고, 두 번째 `MaxPool2d`의 `Output Shape`이 `[1, 64, 14, 14]` (또는 다른 중간 값)로 변경됨을 보여줍니다. 그러나 `AdaptiveAvgPool2d`의 `Output Shape`은 여전히 `[1, 64, 1, 1]`이고, `torch.flatten`의 `Output Shape`은 `[1, 64]`로 고정됨을 시각적으로 확인시켜 줍니다.
    *   **내용:** `(64, 64)` 입력 시에도 중간 레이어의 피처 맵 크기는 변경되지만(`32 -> 64` 또는 `30x30 -> 14x14` 등으로), `AdaptiveAvgPool2d`가 항상 `1x1`의 공간 차원으로 압축해주므로 최종 `in_features`는 변함없이 `64`로 유지됩니다. 강사님은 이 "계산할 필요도 없는" 유연성이 GAP의 핵심이라고 다시 한번 강조하며, 매 숫자에 민감하게 반응하기보다 전체적인 구조와 흐름을 이해할 것을 당부합니다.

*   **12:35:00 - 13:05:00**:
    *   **내용:** 지금까지의 내용을 정리하며, GAP의 핵심적인 장점들을 다시 한번 언급합니다.

*   **13:05:00 - 19:15:00**:
    *   **내용:** 강사님이 `SimpleCNN_01`의 `summary` 내용을 바탕으로 각 레이어의 입력-출력 변화를 처음부터 다시 상세하게 설명합니다.
    *   **`SimpleCNN_01` (Flatten 사용) 기준:**
        *   **초기 입력:** `[1, 3, 32, 32]` (배치, 채널, 높이, 너비)
        *   **`conv_1` (nn.Conv2d, out_channels=32):** `[1, 32, 30, 30]` (커널 3x3, 스트라이드 1, 패딩 없음으로 32-2=30)
        *   **`pool` (nn.MaxPool2d, kernel_size=2):** `[1, 32, 15, 15]` (30/2=15. *강의 슬라이드에서는 14,14로 표시되어 있으나, 일반적인 MaxPool2d 동작은 15,15. 여기서는 일반적인 계산을 설명함*)
        *   **`conv_2` (nn.Conv2d, in_channels=32, out_channels=64):** `[1, 64, 13, 13]` (커널 3x3, 스트라이드 1, 패딩 없음으로 15-2=13)
        *   **`pool` (nn.MaxPool2d, kernel_size=2):** `[1, 64, 6, 6]` (13/2=6.5 이나 MaxPool은 버림. 6. *강의 슬라이드에서는 14,14로 표시되어 있음*)
        *   **`flatten` (nn.Flatten):** `[1, 64 * 6 * 6]` -> `[1, 2304]` (채널 64 * 6 * 6 = 2304)
        *   **`Linear` (nn.Linear, in_features=2304):** `[1, 10]`
    *   **`SimpleCNN_02` (AdaptiveAvgPool2d 사용) 기준 (강의 흐름에 따라 실제 Colab summary와 일치하도록 다시 설명):**
        *   **초기 입력:** `[1, 3, 32, 32]`
        *   **`conv_1` (out_channels=32):** `[1, 32, 30, 30]`
        *   **`pool` (MaxPool2d):** `[1, 32, 14, 14]` (Colab summary 기준)
        *   **`conv_2` (out_channels=64):** `[1, 64, 12, 12]` (Colab summary 기준)
        *   **`pool` (MaxPool2d):** `[1, 64, 6, 6]` (Colab summary 기준)
        *   **`adapt_pool` (nn.AdaptiveAvgPool2d(output_size=(1,1))):** `[1, 64, 1, 1]` (6x6 피처 맵이 1x1로 압축)
        *   **`torch.flatten(x, start_dim=1)`:** `[1, 64]` (1x1로 압축된 64개 채널을 1차원 벡터로 변환)
        *   **`Linear` (nn.Linear, in_features=64):** `[1, 10]`
    *   **핵심:** `AdaptiveAvgPool2d`는 이전 레이어의 출력 공간 크기(`6x6`이든 `30x30`이든)에 관계없이 항상 `channels x 1 x 1` 형태로 만듭니다. 이로 인해 `Linear` 레이어의 `in_features`는 `channels` 수(`64`)로 고정되어, 모델이 입력 크기에 유연해집니다.

*   **19:15:00 - 22:08:00**:
    *   **내용:** 강사님은 다시 한번 각 레이어의 역할과 출력 형태 변화를 강조하며, 특히 `AdaptiveAvgPool2d`가 제공하는 유연성과 간결성에 대한 중요성을 반복적으로 설명합니다. "숫자에 민감하지 말고, 흐름을 이해하라"는 조언을 다시 합니다.

---

### 3. 핵심 개념 및 코드/공식 정리

#### 1. Flatten vs. Global Average Pooling (GAP)

*   **Flatten:**
    *   **설명:** 다차원 피처 맵(예: `[batch_size, channels, height, width]`)을 단일 1차원 벡터(예: `[batch_size, channels * height * width]`)로 변환하여 완전 연결 계층(Fully Connected Layer, `nn.Linear`)의 입력으로 사용합니다.
    *   **단점:** Flatten 이후의 `nn.Linear` 계층은 고정된 `in_features`를 요구하므로, 모델의 입력 이미지 크기가 변경되면 전체 모델 구조(특히 `Linear` 계층의 `in_features`)도 함께 수정해야 하는 번거로움이 있습니다. 또한, 많은 수의 파라미터가 발생할 수 있습니다.
    *   **예시 출력 형태:** `[1, 64, 14, 14]` -> `[1, 12544]` (64 * 14 * 14 = 12544)

*   **Global Average Pooling (GAP):**
    *   **설명:** 각 피처 맵의 모든 공간적 위치(height, width)에 대한 평균을 계산하여 해당 피처 맵을 단일 값으로 줄이는 풀링 기법입니다.
    *   **장점:**
        *   **파라미터 감소:** `nn.Linear` 계층의 `in_features`가 피처 맵의 채널 수(`channels`)로 고정되므로, 파라미터 수가 크게 줄어 오버피팅을 방지하고 모델 복잡성을 낮춥니다.
        *   **입력 크기 유연성:** 피처 맵의 공간 차원(height, width)이 어떻든 항상 `1x1` 크기로 압축되므로, 모델은 다양한 크기의 입력 이미지에 대해 동일한 `nn.Linear` 계층을 사용할 수 있습니다. 이는 모델 설계의 유연성을 높입니다.
        *   **해석 가능성:** 각 `1x1` 값은 해당 피처 맵의 "활성화 강도"를 나타내는 것으로 해석될 수 있어, 모델의 투명성을 높이는 데 기여합니다.
    *   **PyTorch 구현:** `nn.AdaptiveAvgPool2d(output_size=(1,1))`

#### 2. `nn.AdaptiveAvgPool2d(output_size=(1,1))`

*   **역할:** Adaptive Average Pooling을 수행하는 계층으로, `output_size=(1,1)`로 설정하면 Global Average Pooling 역할을 합니다.
*   **입력 형태:** `[batch_size, channels, H_in, W_in]`
*   **출력 형태 (output_size=(1,1) 시):** `[batch_size, channels, 1, 1]`
*   **특징:** `H_in`과 `W_in`의 크기에 상관없이 항상 `1x1`의 공간 차원으로 출력을 생성합니다.

#### 3. `torch.flatten(x, start_dim=1)`

*   **역할:** `nn.AdaptiveAvgPool2d(output_size=(1,1))`의 출력 형태(`[batch_size, channels, 1, 1]`)를 `nn.Linear` 계층의 입력에 적합한 `[batch_size, channels]` 형태로 평탄화합니다.
*   **`start_dim=1`의 의미:** 배치(batch) 차원(`start_dim=0`)은 유지하고, 그 다음 차원(`channels`, `1`, `1`)부터 평탄화를 시작하라는 지시입니다.

#### 4. `SimpleCNN_02` 모델 코드 (핵심 부분)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchinfo import summary # 모델 요약 정보 제공

NUM_INPUT_CHANNELS = 3

class SimpleCNN_02(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        # 첫 번째 합성곱 계층: 3채널 입력 -> 32채널 출력
        self.conv_1 = nn.Conv2d(in_channels=NUM_INPUT_CHANNELS, out_channels=32, kernel_size=3, stride=1)
        # 두 번째 합성곱 계층: 32채널 입력 -> 64채널 출력
        self.conv_2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1)
        # Max Pooling 계층: 2x2 커널로 피처 맵 크기 절반으로 축소
        self.pool = nn.MaxPool2d(kernel_size=2)
        
        # Global Average Pooling 계층 (Flatten 대체)
        # 입력 피처 맵의 H, W와 관계없이 출력을 1x1로 만듦
        self.adapt_pool = nn.AdaptiveAvgPool2d(output_size=(1,1))
        
        # 분류를 위한 완전 연결 계층 (Linear)
        # GAP 후에는 in_features가 피처 맵의 채널 수(64)와 같아짐
        self.classifier = nn.Linear(in_features=64, out_features=num_classes) 

    def forward(self, x):
        # 첫 번째 합성곱 및 ReLU 활성화
        x = F.relu(self.conv_1(x))
        # Max Pooling
        x = self.pool(x)
        # 두 번째 합성곱 및 ReLU 활성화
        x = F.relu(self.conv_2(x))
        # Max Pooling
        x = self.pool(x)
        
        # Global Average Pooling 적용
        x = self.adapt_pool(x)
        # (batch_size, channels, 1, 1) 형태를 (batch_size, channels) 형태로 평탄화
        x = torch.flatten(x, start_dim=1) 
        
        # 최종 분류
        x = self.classifier(x)
        return x

# 모델 요약 예시 (다양한 입력 크기 테스트)
# 32x32 입력:
# summary(SimpleCNN_02(), input_size=(1, NUM_INPUT_CHANNELS, 32, 32)) 
# 출력 형태 예시: MaxPool2d -> [1, 64, 6, 6], adapt_pool -> [1, 64, 1, 1], flatten -> [1, 64], Linear -> [1, 10]

# 64x64 입력 (모델이 유연하게 동작):
# summary(SimpleCNN_02(), input_size=(1, NUM_INPUT_CHANNELS, 64, 64))
# 출력 형태 예시: MaxPool2d -> [1, 64, 30, 30], adapt_pool -> [1, 64, 1, 1], flatten -> [1, 64], Linear -> [1, 10]
```

---

### 4. 학습 퀴즈

1.  `nn.Flatten()`과 `nn.AdaptiveAvgPool2d(output_size=(1,1))`은 CNN에서 완전 연결 계층(`nn.Linear`)에 입력하기 전 피처 맵을 처리하는 방식입니다. 두 방식의 주요 차이점 두 가지와 각각의 장단점을 설명해 보세요.
2.  `nn.AdaptiveAvgPool2d(output_size=(1,1))` 계층의 출력 형태가 `[batch_size, channels, 1, 1]`일 때, 이를 `nn.Linear` 계층의 `in_features`로 사용하기 위해 `torch.flatten(x, start_dim=1)`을 적용하는 이유와 `start_dim=1`의 의미를 설명해 보세요.
3.  `SimpleCNN_02` 모델에 `(1, 3, 32, 32)` 크기의 이미지를 입력했을 때, `self.adapt_pool` 계층 직전의 `x` (즉, 두 번째 `self.pool`의 출력)의 형태와 `self.adapt_pool` 계층 직후의 `x` (즉, `torch.flatten` 직전)의 형태를 각각 예측해 보세요. (강의 내용 및 `summary` 표 참고)