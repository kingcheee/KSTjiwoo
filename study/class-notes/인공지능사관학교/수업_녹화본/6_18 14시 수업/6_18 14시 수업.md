## 6_18 14시 수업 학습 노트: PyTorch 선형 모델 구조 최적화

### 1. 강의 핵심 요약

이번 6_18 14시 수업은 PyTorch를 활용하여 간단한 선형 신경망 모델(`SimpleLinearModel`)의 구현을 최적화하는 데 중점을 둡니다. 강사는 모델의 `__init__` 메서드에서 레이어를 정의하고 `forward` 메서드에서 이를 호출하는 대신, `forward` 메서드 내에서 `torch.flatten` 및 `torch.nn.functional.relu`와 같은 함수형 API를 직접 사용하여 코드를 더 간결하고 명확하게 만드는 방법을 시연했습니다. 핵심 메시지는 모델의 기능적 동일성을 유지하면서 코드의 가독성과 유연성을 높이는 다양한 구현 전략을 이해하는 것입니다.

---

### 2. 화면 연계 타임라인 노트

*   **00:00:00 - 00:00:30 (화면):** Google Colab 환경에서 `INPUT_SIZE = 28`, `NUM_CLASSES = 10`으로 설정된 초기 코드 화면. `torchinfo` 라이브러리가 설치되어 있으며, `model_01 = SimpleLinearModel_01(...)`로 모델이 정의된 후 `summary(model=model_01, input_size=(1, 1, 28, 28), ...)`를 통해 모델 요약 정보가 출력되어 있습니다.
    *   **음성:** 강사가 학생들이 이전 코드를 실행했는지 확인하며, 진행 상황을 체크하고 필요한 경우 대기하겠다고 말합니다.
*   **00:00:31 - 00:02:20 (화면):** `summary` 출력 결과가 화면에 지속됩니다. `Flatten`, `Linear(1-2)`, `ReLU(act_01)`, `Linear(2-3)`, `ReLU(act_02)`, `Linear(3-4)` 레이어들이 순서대로 보이며, 각 레이어의 입력/출력 형태 및 파라미터 수가 표시됩니다. `Flatten` 후 `[1, 784]`, `Linear(1-2)` 후 `[1, 200]`, `Linear(2-3)` 후 `[1, 100]`, `Linear(3-4)` 후 `[1, 10]`으로 형태가 변환되는 것을 볼 수 있습니다. 총 파라미터는 `178,110`개입니다.
    *   **음성:** 강사가 `summary` 출력을 보며 `Flatten` 레이어가 `(1, 1, 28, 28)` 형태의 입력을 받아 `(1, 784)`로 평탄화하는 과정을 설명합니다. 이는 이미지 픽셀 `28*28 = 784`를 하나의 1차원 벡터로 만드는 과정입니다. 이어서 `Linear` 레이어들이 특성 차원을 `784 -> 200 -> 100 -> 10`으로 줄여나가는 것을 설명하고, 최종적으로 `178,110`개의 파라미터가 생성되었음을 확인시켜줍니다.
*   **00:02:20 - 00:04:30 (화면):** `model_01`의 `forward` 메서드 코드가 화면에 잠시 나타납니다. `x = self.flatten(x)`, `x = self.act_01(x)` 등의 코드가 보입니다.
    *   **음성:** 강사가 이전까지의 내용에 대한 이해도를 다시 확인하고, 학생들이 원하면 코드를 공유해주겠다고 제안합니다. 실제 코드를 채팅창에 보내줍니다.
*   **00:04:31 - 00:05:30 (음성):** 강사가 `model_01`의 `__init__` 메서드에서 `self.flatten = nn.Flatten()` 및 `self.act_01 = nn.ReLU()`와 같이 레이어를 인스턴스화하고, `forward` 메서드에서 이를 `self.flatten(x)`처럼 호출하는 방식을 상기시킵니다.
*   **00:05:31 - 00:06:30 (화면):** 새로운 클래스 `SimpleLinearModel_02`의 정의가 시작됩니다. `__init__` 메서드에서 `self.flatten`과 `self.act_01/02` 부분이 제거됩니다. `self.linear_01`, `self.linear_02`, `self.linear_03`만 남아 있습니다.
    *   **음성:** `SimpleLinearModel_02`를 생성할 것이며, 기존 모델과 동일하게 `input_size`와 `num_classes`를 사용하지만, 내부 구조는 변경될 것임을 설명합니다. `Flatten`과 `ReLU` 레이어를 `__init__`에서 제거하는 이유를 설명하며, `forward` 메서드에서 직접 처리하기 위함이라고 밝힙니다.
*   **00:06:31 - 00:08:00 (화면):** `SimpleLinearModel_02`의 `forward` 메서드에서 `x = self.flatten(x)` 부분이 `x = torch.flatten(x, start_dim=1, end_dim=-1)`으로 변경됩니다.
    *   **음성:** `forward` 메서드 내에서 `self.flatten(x)` 대신 `torch.flatten(x, start_dim=1, end_dim=-1)`을 사용하는 방법을 설명합니다. `start_dim=1`은 첫 번째 차원(배치 크기)을 유지하고 두 번째 차원부터 평탄화하라는 의미이며, `end_dim=-1`은 마지막 차원까지 평탄화하라는 의미임을 강조합니다. 이는 `(32, 1, 28, 28)` 형태의 입력에서 `(32, 784)` 형태로 평탄화하는 것과 동일합니다.
*   **00:08:01 - 00:10:30 (화면):** `import torch.nn.functional as F` 문이 추가되고, `x = self.act_01(x)` 부분이 `x = F.relu(self.linear_01(x))`으로 변경됩니다. 두 번째 `ReLU`도 `x = F.relu(self.linear_02(x))`으로 변경됩니다.
    *   **음성:** `ReLU` 활성화 함수를 `__init__`에 인스턴스화하는 대신, `torch.nn.functional` 모듈을 `F`로 임포트하여 `F.relu(self.linear_01(x))`와 같이 `forward` 메서드에서 직접 함수로 호출하는 방법을 설명합니다. 이는 `linear_01`의 출력을 `ReLU` 함수에 파라미터로 전달하는 것과 동일하다고 강조합니다.
*   **00:10:31 - 00:13:25 (화면):** `SimpleLinearModel_02`의 최종 `forward` 메서드 코드가 완성됩니다.
    ```python
    import torch.nn.functional as F # 추가됨

    class SimpleLinearModel_02(nn.Module):
        # ... __init__은 Linear 레이어만 정의
        def forward(self, x):
            x = torch.flatten(x, start_dim=1, end_dim=-1) # 수정됨
            x = F.relu(self.linear_01(x)) # 수정됨
            x = F.relu(self.linear_02(x)) # 수정됨
            output = self.linear_03(x)
            return output
    ```
    *   **음성:** 강사는 이렇게 변경된 코드가 `model_01`과 기능적으로 동일하며, `__init__` 메서드가 간결해지고 `forward` 메서드가 더 명시적이고 가독성이 높아졌다고 설명합니다.
*   **00:13:26 - 00:15:25 (화면):** `model_02 = SimpleLinearModel_02(input_size=INPUT_SIZE, num_classes=NUM_CLASSES)` 코드가 나타나 `model_02` 객체를 생성합니다. 이어서 `images, labels = next(iter(train_loader))` 코드로 데이터 로더에서 이미지 배치를 가져옵니다. `print(images.shape, labels.shape)` 출력으로 `torch.Size([32, 1, 28, 28])`과 `torch.Size([32])`가 보입니다.
    *   **음성:** `model_02`를 생성한 후, 이전에 사용했던 `train_loader`에서 `images`와 `labels`를 가져와 형태를 확인합니다. `(32, 1, 28, 28)`은 32개의 흑백 이미지(28x28) 배치임을 의미합니다.
*   **00:15:26 - 00:16:25 (화면):** `output = model_02(images)` 코드로 모델에 이미지를 입력하고, `print(output.shape)` 결과로 `torch.Size([32, 10])`이 출력됩니다.
    *   **음성:** `model_02`에 `images`를 입력했을 때, 최종 `output`의 형태가 `(32, 10)`이 되는 것을 확인합니다. 이는 32개의 각 이미지에 대해 10개의 클래스에 대한 예측 값이 출력되었음을 의미하며, 모델이 정상적으로 작동하고 있음을 보여줍니다.
*   **00:16:26 - 00:18:00 (화면):** `summary(model=model_02, input_size=(1, 1, 28, 28))` 코드를 실행하여 `model_02`의 요약을 다시 확인합니다. `summary` 출력에는 `Flatten`과 `ReLU`가 더 이상 명시적인 레이어로 나타나지 않고 `Linear` 레이어들만 보입니다.
    *   **음성:** `model_02`의 `summary`를 확인하며, `Flatten`과 `ReLU`가 목록에 보이지 않는 이유가 `forward` 메서드에서 함수형 API를 직접 사용했기 때문이라고 설명합니다. 강사는 이 방식이 코드를 더욱 "심플"하게 만든다고 강조합니다.
*   **00:18:01 - 00:19:50 (음성):** 강사는 `ReLU` 레이어가 `summary`에 나타나기를 원한다면 `__init__`에서 `nn.ReLU()`로 정의해야 한다고 덧붙이며, 이는 기능의 차이가 아닌 표현 방식의 차이임을 다시 한번 강조합니다.

---

### 3. 핵심 개념 및 코드/공식 정리

**1. 모델 구조 변경의 배경**
*   **목표:** PyTorch 모델의 `__init__` 메서드를 간결하게 유지하고, `forward` 메서드 내에서 레이어의 기능을 함수형 API로 직접 호출하여 코드의 가독성 및 유연성을 높입니다.
*   **이전 방식 (`SimpleLinearModel_01`):**
    ```python
    import torch.nn as nn

    class SimpleLinearModel_01(nn.Module):
        def __init__(self, input_size, num_classes=10):
            super().__init__()
            self.flatten = nn.Flatten() # nn.Module로 정의
            self.linear_01 = nn.Linear(in_features=input_size * input_size, out_features=200)
            self.act_01 = nn.ReLU() # nn.Module로 정의
            self.linear_02 = nn.Linear(in_features=200, out_features=100)
            self.act_02 = nn.ReLU() # nn.Module로 정의
            self.linear_03 = nn.Linear(in_features=100, out_features=num_classes)

        def forward(self, x):
            x = self.flatten(x) # 객체 호출
            x = self.linear_01(x)
            x = self.act_01(x) # 객체 호출
            x = self.linear_02(x)
            x = self.act_02(x) # 객체 호출
            output = self.linear_03(x)
            return output
    ```

**2. `torch.flatten` (함수형 Flatten)**
*   **설명:** `nn.Flatten` 모듈 객체를 `__init__`에서 선언하지 않고, `forward` 메서드에서 `torch` 라이브러리에 내장된 `flatten` 함수를 직접 호출하는 방식입니다.
*   **장점:**
    *   `__init__` 메서드를 간결하게 만듭니다.
    *   `start_dim` 및 `end_dim` 인수를 통해 평탄화할 차원의 범위를 정확하게 제어할 수 있습니다.
    *   `torchinfo.summary` 출력 시 Flatten 레이어가 명시적으로 나타나지 않아 구조가 더 간결하게 보일 수 있습니다.
*   **코드 (`SimpleLinearModel_02`의 `forward` 내):**
    ```python
    x = torch.flatten(x, start_dim=1, end_dim=-1)
    ```
    *   `start_dim=1`: 텐서의 두 번째 차원(인덱스 1)부터 평탄화를 시작합니다. (첫 번째 차원, 즉 배치 크기는 유지).
    *   `end_dim=-1`: 텐서의 마지막 차원까지 평탄화를 수행합니다.

**3. `torch.nn.functional.relu` (`F.relu`) (함수형 ReLU)**
*   **설명:** `nn.ReLU` 모듈 객체를 `__init__`에서 선언하지 않고, `torch.nn.functional` 모듈을 임포트(`import torch.nn.functional as F`)한 후 `forward` 메서드에서 `F.relu` 함수를 직접 호출하는 방식입니다.
*   **장점:**
    *   `__init__` 메서드를 간결하게 만듭니다.
    *   활성화 함수를 파라미터로 전달하는 형태로 코드를 구성할 수 있어 표현의 유연성이 높아집니다.
    *   `torchinfo.summary` 출력 시 ReLU 레이어가 명시적으로 나타나지 않아 구조가 더 간결하게 보일 수 있습니다.
*   **코드 (`SimpleLinearModel_02`의 `forward` 내):**
    ```python
    import torch.nn.functional as F # 추가

    # ...

    x = F.relu(self.linear_01(x))
    x = F.relu(self.linear_02(x))
    ```

**4. `SimpleLinearModel_02` 최종 코드:**
```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleLinearModel_02(nn.Module):
    def __init__(self, input_size, num_classes=10):
        super().__init__()
        # Flatten과 ReLU는 __init__에서 정의하지 않고 forward에서 직접 호출합니다.
        self.linear_01 = nn.Linear(in_features=input_size * input_size, out_features=200)
        self.linear_02 = nn.Linear(in_features=200, out_features=100)
        self.linear_03 = nn.Linear(in_features=100, out_features=num_classes)

    def forward(self, x):
        # Flatten 대신 torch.flatten 사용 (배치 차원 유지)
        x = torch.flatten(x, start_dim=1, end_dim=-1)
        # Linear 레이어를 통과시킨 후 F.relu로 활성화
        x = F.relu(self.linear_01(x))
        x = F.relu(self.linear_02(x))
        # 마지막 Linear 레이어는 분류 문제의 최종 출력으로, 활성화 함수는 보통 손실 함수(CrossEntropyLoss) 내에 포함됩니다.
        output = self.linear_03(x)
        return output

# 모델 인스턴스화
INPUT_SIZE = 28
NUM_CLASSES = 10
model_02 = SimpleLinearModel_02(input_size=INPUT_SIZE, num_classes=NUM_CLASSES)

# 예시 입력 이미지 (32개 배치, 1채널, 28x28)
# 실제 데이터 로더에서 가져온다고 가정
images = torch.randn(32, 1, 28, 28)

# 모델에 이미지 입력 및 출력 형태 확인
output = model_02(images)
print(output.shape) # 예상 출력: torch.Size([32, 10])

# 모델 요약 확인 (Flatten과 ReLU는 명시적으로 나타나지 않음)
from torchinfo import summary
summary(model=model_02, input_size=(1, 1, 28, 28))
```

---

### 4. 학습 퀴즈

1.  `nn.Flatten`과 `torch.flatten`의 주요 차이점은 무엇이며, 각각 어떤 상황에 더 적합하게 사용될 수 있나요?
2.  `SimpleLinearModel_02`에서 `forward` 메서드 내에 `torch.flatten(x, start_dim=1, end_dim=-1)`와 `F.relu()`를 사용하는 방식이 `nn.Flatten()` 및 `nn.ReLU()`를 `__init__`에 선언하여 사용하는 방식과 비교했을 때 어떤 장점(또는 단점)이 있나요?
3.  주어진 `SimpleLinearModel_02`에 `torch.Size([64, 1, 28, 28])` 크기의 이미지가 입력되었을 때, 최종 `output` 텐서의 크기는 어떻게 될 것이며 그 이유는 무엇인가요?