## 📚 6월 18일 11시 수업 학습 노트

### 💡 강의 핵심 요약

오늘의 강의는 PyTorch를 활용하여 자신만의 선형 신경망 모델(`LinearModel`)을 구축하는 방법에 중점을 두었습니다. 강사님은 모델의 기본 구조를 정의하고, 은닉층과 활성화 함수(ReLU)를 추가하며, 데이터가 모델을 통해 순방향으로 전파되는 과정을 코드로 구현하는 방법을 상세히 설명했습니다. 특히 `torchinfo` 라이브러리를 활용하여 모델의 구조와 파라미터 수를 시각적으로 확인하는 방법까지 다루며, 사용자 정의 모델 생성의 전반적인 과정을 이해할 수 있도록 이끌었습니다.

---

### ⏳ 화면 연계 타임라인 노트

*   **00:00 - 00:18**: 강의 시작. PyTorch 라이브러리 `torch`와 `torch.nn`을 `nn`으로 임포트하는 코드가 화면에 보입니다. 강사님은 수업 전반에 대한 개요를 설명하며, 사용자 정의 모델 생성의 중요성을 강조합니다.

*   **00:19 - 00:30**: `Custom Model` 생성을 위한 `LinearModel` 클래스 정의가 시작됩니다.
    *   **코드**:
        ```python
        # Custom Model 생성
        class LinearModel(nn.Module):
            def __init__(self, num_classes=10):
        ```
    *   **설명**: `nn.Module`을 상속받아 새로운 클래스를 만듭니다. `__init__` 함수는 클래스 인스턴스가 생성될 때 초기화하는 역할을 하며, `num_classes`는 출력 클래스 수를 나타내는 매개변수로 기본값은 10입니다.

*   **00:31 - 01:20**: `__init__` 함수 내에서 부모 클래스의 생성자를 호출하는 `super().__init__()`의 중요성이 설명됩니다. `self`는 현재 객체 인스턴스를 의미하며, 객체 자신에게 속한 변수나 메서드에 접근할 때 사용됩니다. 강사님은 `붕어빵 틀` 비유를 통해 이 과정을 쉽게 설명합니다.

*   **01:21 - 01:34**: `self`는 `LinearModel` 클래스의 인스턴스 그 자체를 의미한다고 다시 한번 강조됩니다. 처음에는 낯설게 느껴질 수 있으나, 익숙해질 것이라고 언급합니다.

*   **01:35 - 01:45**: `num_classes`는 모델의 최종 출력 계층의 크기를 결정하는 중요한 요소임을 설명합니다.

*   **01:46 - 02:29**: `super().__init__()` 호출의 필요성에 대해 상세히 설명합니다. 부모 클래스인 `nn.Module`이 가지고 있는 중요한 기능들을 초기화하는 역할을 하며, 이를 호출하지 않으면 모델이 제대로 작동하지 않습니다. 이 과정이 마치 부모님을 불러와서 상속받는 것과 같다고 비유합니다.

*   **02:30 - 03:09**: 화면이 "활성화 함수(Activation Function)" 슬라이드로 전환됩니다. 강사님은 신경망의 계층 구조(입력층, 은닉층, 출력층)와 각 계층 간의 연결을 설명하며, 이 구조를 코드로 구현할 것이라고 언급합니다.

*   **03:10 - 03:29**: 활성화 함수 중 `ReLU`에 대한 설명을 합니다. 일반적으로 은닉층에 많이 사용되며, 비선형성을 추가하는 역할을 강조합니다.

*   **03:30 - 04:00**: 모델의 계층을 정의하기 시작합니다. 첫 번째 선형 계층을 `self.linear_01`로 정의할 준비를 합니다.

*   **04:01 - 04:30**: 첫 번째 선형 계층(`linear_01`)을 `nn.Linear`로 초기화하는 코드를 작성합니다.
    *   **코드**: `self.linear_01 = nn.Linear(`
    *   **설명**: `nn.Linear`는 완전 연결 계층(Fully Connected Layer)을 생성하는 PyTorch 모듈입니다.

*   **04:31 - 05:00**: `nn.Linear` 모듈의 매개변수인 `in_features`와 `out_features`에 대해 설명합니다. `in_features`는 입력 특성의 수를, `out_features`는 출력 특성의 수를 의미합니다.

*   **05:01 - 06:00**: 첫 번째 선형 계층의 `in_features`를 784로, `out_features`를 100으로 설정합니다. 784는 28x28 크기의 이미지를 평탄화(flatten)했을 때의 픽셀 수와 같으며, 100은 첫 번째 은닉층의 뉴런 수를 임의로 설정한 것입니다.
    *   **코드**: `self.linear_01 = nn.Linear(in_features=784, out_features=100)`

*   **06:01 - 07:00**: 화면의 신경망 다이어그램을 보며 입력층(784)에서 첫 번째 은닉층(100)으로 데이터가 전달되는 과정을 다시 한번 설명합니다.

*   **07:01 - 08:31**: 첫 번째 선형 계층의 출력에 적용할 활성화 함수 `ReLU`를 정의합니다.
    *   **코드**: `self.relu_01 = nn.ReLU()`
    *   **설명**: `ReLU`는 비선형성을 도입하여 모델이 더 복잡한 패턴을 학습할 수 있게 합니다.

*   **08:32 - 11:11**: 두 번째 선형 계층(`linear_02`)을 정의합니다. `in_features`는 이전 계층의 `out_features` 값인 100이 되고, `out_features`는 최종 출력 클래스 수인 `num_classes` (10)가 됩니다.
    *   **코드**: `self.linear_02 = nn.Linear(in_features=100, out_features=num_classes)`

*   **11:12 - 14:30**: `forward` 메서드를 정의하기 시작합니다. 이 메서드는 데이터가 모델의 각 계층을 통과하는 순서를 정의하며, 모델의 순방향 전파(forward pass)를 구현합니다. `def forward(self, x):` 코드가 작성됩니다.
    *   **설명**: `x`는 입력 데이터를 의미합니다.

*   **14:31 - 17:30**: `forward` 메서드 내에서 데이터(`x`)가 `linear_01`, `relu_01`, `linear_02`를 순차적으로 통과하도록 연결합니다.
    *   **코드**:
        ```python
        def forward(self, x):
            x = self.linear_01(x)
            x = self.relu_01(x)
            output = self.linear_02(x)
            return output
        ```
    *   **설명**: 입력 `x`는 첫 번째 선형 계층을 거쳐 `ReLU` 활성화 함수를 통과한 후, 두 번째 선형 계층을 거쳐 최종 `output`을 생성합니다.

*   **17:31 - 18:00**: `return output`으로 모델의 최종 출력을 반환합니다. 이로써 `LinearModel` 클래스의 정의가 완료됩니다.

*   **18:01 - 20:30**: 모델에 입력할 임의의 텐서(`input_tensor`)를 생성합니다.
    *   **코드**: `input_tensor = torch.rand(size=(64, 784))`
    *   **설명**: `torch.rand`는 주어진 크기의 난수로 채워진 텐서를 생성합니다. `(64, 784)`는 64개의 샘플(배치 크기)과 각 샘플당 784개의 특성(픽셀)을 의미합니다. 이는 모델에 대한 더미 입력으로 사용됩니다.
    *   **출력**: `print(input_tensor.size())` → `torch.Size([64, 784])`

*   **20:31 - 21:00**: `LinearModel` 클래스의 객체(`linear_model`)를 생성합니다. 이 과정에서 `__init__` 메서드가 호출되어 모델의 계층들이 초기화됩니다.
    *   **코드**: `linear_model = LinearModel(num_classes=10)`

*   **21:01 - 23:09**: 객체 생성 시 `num_classes=10`이 `__init__` 함수로 전달되어 모델의 마지막 계층 출력이 10개 클래스에 대응하도록 설정됩니다.

*   **23:10 - 25:35**: `input_tensor`를 `linear_model`에 직접 전달하여 순방향 전파를 실행하고 모델의 예측(`output_tensor`)을 얻습니다.
    *   **코드**: `output_tensor = linear_model(input_tensor)`
    *   **설명**: `linear_model(input_tensor)`는 내부적으로 `forward` 메서드를 호출합니다.

*   **25:36 - 28:00**: 모델의 출력 텐서 크기를 확인합니다.
    *   **코드**: `print(output_tensor.size())`
    *   **출력**: `torch.Size([64, 10])`
    *   **설명**: 64는 입력 배치 크기, 10은 `num_classes`로 설정한 출력 클래스 수를 나타냅니다.

*   **28:01 - 32:00**: 모델의 `weight` 값을 직접 확인하려 시도하지만, `linear_model.weight`는 직접적인 속성이 아니므로 에러가 발생합니다. 대신 각 계층의 `weight`에 접근해야 합니다 (`linear_model.linear_01.weight`).

*   **32:01 - 34:30**: 첫 번째 선형 계층의 `weight`의 크기를 확인합니다.
    *   **코드**: `print(linear_model.linear_01.weight.shape)`
    *   **출력**: `torch.Size([100, 784])`
    *   **설명**: 이는 첫 번째 선형 계층이 784개의 입력과 100개의 출력을 가지고 있음을 보여줍니다. 마찬가지로 두 번째 계층의 `weight` 크기도 확인합니다.
    *   **코드**: `print(linear_model.linear_02.weight.shape)`
    *   **출력**: `torch.Size([10, 100])`

*   **34:31 - 35:30**: `torchinfo` 라이브러리를 설치합니다.
    *   **코드**: `!pip install torchinfo`
    *   **설명**: `torchinfo`는 PyTorch 모델의 상세한 요약을 제공하여 구조, 출력 형태, 파라미터 수 등을 한눈에 볼 수 있게 해줍니다.

*   **35:31 - 36:30**: `torchinfo`에서 `summary` 함수를 임포트하고, `linear_model`에 대한 요약을 생성합니다.
    *   **코드**:
        ```python
        from torchinfo import summary
        summary(model=linear_model, input_size=(64, 784),
                col_names=['input_size', 'output_size', 'num_params'],
                row_settings=['var_names', 'depth'],
                depth=3 # verbose=1 or 2
               )
        ```
    *   **설명**: `input_size`는 모델에 전달될 입력 데이터의 크기를, `col_names`는 요약에 포함될 열의 이름을, `row_settings`는 행 구성 방식을, `depth`는 보여줄 계층의 깊이를 지정합니다.

*   **36:31 - 37:52**: `summary` 함수 실행 결과를 분석합니다.
    *   **출력**: 모델의 계층 구조(`Linear_01`, `ReLU_01`, `Linear_02`), 각 계층의 입력/출력 형태, 파라미터 수 등이 깔끔하게 정리되어 표시됩니다.
        *   `Linear_01`: Input `[64, 784]`, Output `[64, 100]`, Params `78,500`
        *   `ReLU_01`: Input `[64, 100]`, Output `[64, 100]`, Params `0`
        *   `Linear_02`: Input `[64, 100]`, Output `[64, 10]`, Params `1,010`
    *   **총 파라미터 수**: `Total params: 79,510`
    *   **설명**: `ReLU`는 학습 가능한 파라미터가 없으므로 0개로 표시됩니다. 각 `nn.Linear` 계층의 파라미터 수는 입력 뉴런 수 * 출력 뉴런 수 + 출력 뉴런 수(바이어스)로 계산됩니다. 이처럼 `torchinfo`를 통해 모델의 전체 구조와 파라미터 수를 한눈에 파악할 수 있음을 강조합니다. 강사님은 ChatGPT의 파라미터 수(1750억 개)와 비교하며 모델의 복잡성을 예시로 듭니다.

---

### 🧠 핵심 개념 및 코드/공식 정리

1.  **PyTorch `nn.Module`**:
    *   **설명**: 모든 신경망 모듈의 기본 클래스입니다. PyTorch에서 모델을 정의할 때는 항상 `nn.Module`을 상속받아야 합니다.
    *   **주요 기능**: `__init__` (초기화), `forward` (순방향 전파) 메서드를 구현해야 합니다. 파라미터(`nn.Parameter`)와 자식 모듈(`nn.Module`)을 자동으로 추적합니다.

2.  **`super().__init__()`**:
    *   **설명**: 상속받은 부모 클래스(`nn.Module`)의 `__init__` 메서드를 호출하여 초기화하는 과정입니다. 이는 부모 클래스에 정의된 중요한 기능(예: 파라미터 관리, 모듈 등록)들이 올바르게 설정되도록 보장합니다.

3.  **`self` 키워드**:
    *   **설명**: 클래스 인스턴스 자신을 참조하는 매개변수입니다. `__init__` 메서드 내에서 `self.변수명` 형태로 인스턴스 변수를 정의하거나, `self.메서드명()` 형태로 인스턴스 메서드를 호출할 때 사용됩니다.

4.  **`torch.nn.Linear` (완전 연결 계층)**:
    *   **설명**: 입력과 출력 사이의 선형 변환($y = xA^T + b$)을 적용하는 계층입니다.
    *   **매개변수**:
        *   `in_features` (int): 입력 텐서의 크기 (특성 수).
        *   `out_features` (int): 출력 텐서의 크기 (뉴런 수).
    *   **코드 예시**: `self.linear_01 = nn.Linear(in_features=784, out_features=100)`
    *   **파라미터 계산**: `(in_features * out_features) + out_features` (바이어스)

5.  **`torch.nn.ReLU` (활성화 함수)**:
    *   **설명**: Rectified Linear Unit. 입력값이 0보다 작으면 0을, 0보다 크면 입력값을 그대로 출력하는 비선형 활성화 함수입니다.
    *   **수식**: $f(x) = \max(0, x)$
    *   **코드 예시**: `self.relu_01 = nn.ReLU()`
    *   **특징**: 학습 가능한 파라미터가 없습니다.

6.  **`forward` 메서드**:
    *   **설명**: `nn.Module`을 상속받은 클래스에서 반드시 구현해야 하는 메서드입니다. 모델에 입력 데이터가 주어졌을 때, 이 데이터가 어떤 순서로 계층들을 통과하여 최종 출력을 생성할지 정의합니다.
    *   **코드 예시**:
        ```python
        def forward(self, x):
            x = self.linear_01(x)
            x = self.relu_01(x)
            output = self.linear_02(x)
            return output
        ```

7.  **`torch.rand`**:
    *   **설명**: 0과 1 사이의 균일 분포에서 난수로 채워진 텐서를 생성합니다. 모델에 대한 임의의 입력 데이터를 생성할 때 유용합니다.
    *   **코드 예시**: `input_tensor = torch.rand(size=(64, 784))`

8.  **`torchinfo.summary`**:
    *   **설명**: PyTorch 모델의 구조, 각 계층의 입/출력 형태, 파라미터 수(학습 가능한/불가능한), 총 파라미터 수, 모델의 메모리 사용량 등을 한눈에 볼 수 있도록 요약해주는 유용한 도구입니다.
    *   **설치**: `!pip install torchinfo`
    *   **사용법**:
        ```python
        from torchinfo import summary
        summary(model=linear_model, input_size=(64, 784),
                col_names=['input_size', 'output_size', 'num_params'],
                row_settings=['var_names', 'depth'])
        ```
    *   **주요 출력**:
        *   `Input Shape`: 각 계층에 들어오는 데이터의 형태
        *   `Output Shape`: 각 계층에서 나가는 데이터의 형태
        *   `Param #`: 각 계층이 가지고 있는 학습 가능한 파라미터 수
        *   `Total params`: 모델 전체의 총 파라미터 수

---

### ❓ 학습 퀴즈

1.  PyTorch에서 사용자 정의 신경망 모델을 생성할 때, 반드시 상속받아야 하는 기본 클래스의 이름은 무엇이며, 이 클래스의 `__init__` 메서드를 호출해야 하는 이유는 무엇인가요?
2.  다음 `nn.Linear` 계층의 파라미터 수는 몇 개이며, `in_features`와 `out_features`는 각각 어떤 의미를 가지나요?
    `nn.Linear(in_features=256, out_features=128)`
3.  `torchinfo.summary` 함수를 사용하여 모델을 요약했을 때, `ReLU` 활성화 함수의 `Param #`이 항상 0으로 표시되는 이유는 무엇인가요?