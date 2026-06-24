## 6_18 15시 수업 학습 노트

### 1. 강의 핵심 요약

오늘의 수업은 PyTorch를 활용한 신경망 모델 개발 및 학습 과정에 초점을 맞추었습니다. 강사는 모델을 함수화하고, CUDA/CPU 환경 설정을 포함하여 학습 및 검증 단계를 위한 코드를 상세히 구현했습니다. 특히 CrossEntropyLoss와 Adam Optimizer를 사용하여 손실을 계산하고 모델 파라미터를 업데이트하는 전체 훈련 루프를 체계적으로 설명하고 직접 실행하며 손실 값의 변화를 확인했습니다.

### 2. 화면 연계 타임라인 노트

*   **00:00:00 - 00:00:29**:
    *   강의 시작. 모델을 함수화하여 재사용성을 높이는 방법을 설명합니다. `model = SimpleLinearModel_02(...)` 코드가 화면에 보입니다.
    *   함수로 모델을 생성하면 용이하다고 언급하며, 함수명을 길게 만들어 가독성을 높입니다.
    *   `input_size`와 `num_classes`를 파라미터로 받는 함수로 모델 생성을 변경합니다.

*   **00:00:30 - 00:00:59**:
    *   `def create_simple_linear_model(input_size, num_classes):` 함수 정의를 시작합니다.
    *   이 함수는 `SimpleLinearModel_02`를 인스턴스화하고 반환합니다. 이전에 만든 모델 객체를 함수 내에서 생성하여 반환하도록 변경합니다.
    *   `model = SimpleLinearModel_02(input_size=input_size, num_classes=num_classes)`
    *   `return model`

*   **00:01:00 - 00:01:29**:
    *   함수 정의가 완료된 모습. 이제 이 함수를 호출하면 모델이 생성됩니다.
    *   변수명을 `model`로 통일하여 명확하게 합니다.
    *   `model = create_simple_linear_model(input_size=28, num_classes=10)`
    *   `model = model.to(device)` 코드를 추가하여 생성된 모델을 설정된 디바이스로 옮깁니다.

*   **00:01:30 - 00:01:59**:
    *   모델 생성 및 디바이스 할당 코드가 화면에 보입니다.
    *   이제 `create_simple_linear_model` 함수만 호출하면 모델을 얻을 수 있습니다.

*   **00:02:00 - 00:02:29**:
    *   디바이스 설정에 대한 설명입니다. 모델을 쿠다(GPU) 환경 또는 CPU 환경에 올리는 방법입니다.
    *   `device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')` 코드를 추가하여 GPU 사용 가능 여부에 따라 디바이스를 자동으로 설정합니다.

*   **00:02:30 - 00:03:29**:
    *   디바이스 설정 코드가 포함된 모습. 강사는 `torch.cuda.is_available()` 함수를 사용하여 쿠다 환경 사용 가능 여부를 확인한다고 설명합니다.
    *   만약 쿠다를 사용할 수 있다면 `'cuda'`로 설정하고, 그렇지 않다면 `'cpu'`로 설정합니다.
    *   이 설정에 따라 모델은 GPU 또는 CPU에서 동작하게 됩니다.

*   **00:03:30 - 00:04:00**:
    *   모델을 생성하고 디바이스에 올리는 과정을 함수화한 코드가 화면에 보입니다.
    *   `model = create_simple_linear_model(input_size=28, num_classes=10)`
    *   `model = model.to(device)`

*   **00:04:01 - 00:04:30**:
    *   생성된 모델에 `to(device)`를 적용하여 디바이스에 올리는 코드입니다.
    *   모델이 생성되면 리니어 레이어(Linear layer)와 같은 구성 요소들이 모두 생성된 상태를 의미합니다. 아직 데이터는 입력되지 않았지만, 신경망 구조는 완성된 것입니다.

*   **00:04:31 - 00:05:00**:
    *   완성된 모델을 `to(device)`를 통해 디바이스에 등록하는 코드입니다. 이렇게 하면 모델이 설정된 하드웨어 환경(GPU 또는 CPU)에서 동작하게 됩니다.

*   **00:05:01 - 00:05:30**:
    *   `model = model.to(device)` 최종 코드.
    *   이제 학습(Training) 단계로 넘어갑니다.

*   **00:05:31 - 00:06:00**:
    *   "Training Loop" 다이어그램이 화면에 보입니다. 이 다이어그램은 PyTorch의 학습 과정을 시각적으로 보여줍니다.
    *   주요 단계: Forward Pass -> Loss 계산 -> Optimizer Gradient 초기화 -> Gradient 계산 (Backward) -> 학습 파라미터 업데이트.
    *   강사는 이 다이어그램을 기반으로 앞으로 진행할 학습 코드의 흐름을 설명합니다.

*   **00:06:01 - 00:06:30**:
    *   모델이 이미 생성되었으므로 이제부터 학습을 진행합니다.
    *   `# 1 epoch 동안 train dataset을 미니 배치 단위로 모델을 학습 시킴` 이라는 주석이 보입니다.

*   **00:06:31 - 00:07:00**:
    *   `def train_step():` 함수 정의를 시작합니다.
    *   이 함수는 한 에포크(epoch) 동안 트레인 데이터셋을 미니 배치 단위로 모델을 학습시키는 역할을 합니다.

*   **00:07:01 - 00:07:30**:
    *   `for batch_idx, (images, labels) in enumerate(train_loader):` 루프를 통해 `train_loader`에서 배치 인덱스, 이미지, 라벨을 가져옵니다.
    *   `enumerate`를 사용하면 인덱스(`batch_idx`)도 함께 얻을 수 있습니다.

*   **00:07:31 - 00:08:00**:
    *   이미지와 라벨을 디바이스로 옮기는 코드입니다.
    *   `images = images.to(device)`
    *   `labels = labels.to(device)`

*   **00:08:01 - 00:08:30**:
    *   모델을 통해 예측(`pred`)을 수행하는 코드입니다. `pred = model(images)`
    *   이는 모델의 `forward` 함수를 암시적으로 호출합니다.
    *   손실 계산 주석 `# loss 계산` 이 보입니다.

*   **00:08:31 - 00:09:00**:
    *   손실 함수 `loss_fn`을 사용하여 예측값과 실제 라벨 간의 손실을 계산합니다.
    *   `loss_fn = nn.CrossEntropyLoss()`를 미리 정의해 둡니다.

*   **00:09:01 - 00:09:30**:
    *   손실 계산 코드가 화면에 보입니다.
    *   `loss = loss_fn(pred, labels)`
    *   Optimizer 초기화 주석 `# optimizer 초기화` 이 보입니다.

*   **00:09:31 - 00:10:00**:
    *   옵티마이저를 정의하는 코드입니다.
    *   `from torch.optim import Adam`
    *   `optimizer = Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))`
    *   `model.parameters()`는 학습할 가중치(weights)와 편향(biases)을 옵티마이저에 전달합니다. `lr`은 학습률, `betas`는 Adam 옵티마이저의 모멘텀 계수입니다.

*   **00:10:01 - 00:10:30**:
    *   옵티마이저 정의 코드가 화면에 보입니다.
    *   `optimizer.zero_grad()`는 이전 배치에서 계산된 그래디언트를 초기화하는 역할을 합니다.

*   **00:10:31 - 00:11:00**:
    *   `loss.backward()`를 호출하여 역전파(backpropagation)를 통해 모든 학습 가능한 파라미터에 대한 그래디언트(기울기)를 계산합니다.

*   **00:11:01 - 00:11:30**:
    *   `optimizer.step()`을 호출하여 계산된 그래디언트를 기반으로 모델의 파라미터(가중치와 편향)를 업데이트합니다.
    *   이것으로 한 배치에 대한 학습 파라미터 업데이트가 완료됩니다.

*   **00:11:31 - 00:12:00**:
    *   학습 진행 상황을 출력하는 조건문입니다.
    *   `if batch_idx % 100 == 0:` (100번째 배치마다)
    *   `print(f'{batch_idx+1}번째 batch gradient 적용, loss={loss.item()}')`
    *   손실 값을 출력하여 학습이 잘 진행되고 있는지 모니터링합니다.

*   **00:12:01 - 00:12:30**:
    *   `train_step` 함수 전체 코드.
    *   `train_step()` 함수는 리턴 값이 없습니다. 학습만 수행하고 결과는 내부적으로 출력됩니다.

*   **00:12:31 - 00:13:00**:
    *   전체 에포크(epochs)를 설정하고 훈련을 시작합니다.
    *   `EPOCHS = 10` (10 에포크 동안 학습)
    *   `model.train()`을 호출하여 모델을 훈련 모드로 설정합니다. (Dropout, BatchNorm 등이 훈련 모드로 작동)

*   **00:13:01 - 00:13:30**:
    *   `for epoch in range(EPOCHS):` 루프를 통해 설정된 에포크 수만큼 반복합니다.
    *   `print(f'######{epoch+1}번째 train 시작')` 에포크 시작 메시지를 출력합니다.
    *   `train_step()` 함수를 호출하여 한 에포크 동안의 학습을 진행합니다.

*   **00:13:31 - 00:14:00**:
    *   훈련이 시작되고 각 배치마다 손실 값이 출력되는 모습이 화면에 보입니다.
    *   손실 값이 점차 감소하는 것을 확인할 수 있습니다.

*   **00:14:01 - 00:14:30**:
    *   훈련 과정에서 손실 값이 계속 출력되고 있습니다.
    *   손실 값은 처음에는 높았다가 점차 낮아지는 경향을 보이지만, 때로는 등락을 반복하기도 합니다.

*   **00:14:31 - 00:15:00**:
    *   훈련 진행 중. `h100`과 같은 고성능 GPU를 사용하면 빠르게 진행되지만, CPU나 다른 환경에서는 더 오래 걸릴 수 있다고 언급합니다.

*   **00:15:01 - 00:15:30**:
    *   10 에포크 훈련이 완료된 모습입니다.
    *   처음 시작 시 손실 값(`3, 4, 5`)과 비교하여 마지막 에포크에서는 손실 값이 `1, 2` 정도로 크게 줄어들었음을 확인할 수 있습니다.

*   **00:15:31 - 00:16:00**:
    *   손실 값 감소 확인. 모델이 학습되었음을 시사합니다.

*   **00:16:01 - 00:16:30**:
    *   이제 검증(Validation) 단계로 넘어갑니다.
    *   검증을 위한 `val_step` 함수를 정의합니다.
    *   `def val_step():`

*   **00:16:31 - 00:17:00**:
    *   검증 단계에서는 그래디언트 계산이 필요 없으므로 `with torch.no_grad():` 블록을 사용합니다.
    *   이는 메모리 사용량을 줄이고 계산 속도를 빠르게 하며, 학습된 가중치가 실수로 업데이트되는 것을 방지합니다.

*   **00:17:01 - 00:17:30**:
    *   `for batch_idx, (images, labels) in enumerate(val_loader):` 루프를 통해 `val_loader`에서 배치 인덱스, 이미지, 라벨을 가져옵니다. (이전에 `train_loader`를 `val_loader`로 변경)
    *   이미지와 라벨을 디바이스로 옮기는 코드는 동일합니다.

*   **00:17:31 - 00:18:00**:
    *   검증 단계에서는 `optimizer.zero_grad()`, `loss.backward()`, `optimizer.step()` 같은 코드는 필요 없습니다. 오직 예측 및 손실 계산만 수행합니다.
    *   손실 값 출력은 `valid loss`로 변경합니다.

*   **00:18:01 - 00:18:30**:
    *   `val_step` 함수 전체 코드.
    *   `val_loader`를 사용하고 `torch.no_grad()` 블록 내에서 그래디언트 관련 코드를 제거한 모습입니다.

*   **00:18:31 - 00:19:00**:
    *   이제 훈련 루프 내에서 검증 단계를 추가합니다.
    *   `model.eval()`을 호출하여 모델을 검증 모드로 설정합니다. (Dropout, BatchNorm 등이 검증 모드로 작동)
    *   `val_step()` 함수를 호출하여 검증을 진행합니다.

*   **00:19:01 - 00:19:30**:
    *   훈련 및 검증을 동시에 실행하는 코드입니다.
    *   각 에포크마다 훈련을 먼저 수행하고, 이어서 검증을 수행합니다.

*   **00:19:31 - 00:20:00**:
    *   훈련/검증 시작. 훈련 과정과 동일하게 각 배치마다 손실 값이 출력됩니다.

*   **00:20:01 - 00:20:30**:
    *   훈련 중인 손실 값.

*   **00:20:31 - 00:21:00**:
    *   훈련 및 검증이 진행되는 과정. 검증 손실(`valid loss`)도 함께 출력됩니다.

*   **00:21:01 - 00:21:30**:
    *   훈련과 검증이 모두 완료된 모습입니다.
    *   손실 값이 점차 줄어들었음을 다시 한번 확인합니다.

*   **00:21:31 - 00:22:00**:
    *   훈련 및 검증 완료 후 손실 값의 변화를 보여줍니다.

*   **00:22:01 - 00:22:30**:
    *   손실 값 확인. 모델이 잘 학습되었음을 보여줍니다.
    *   하지만 단순히 손실 값만으로는 모델의 성능을 정확히 평가하기 어렵다고 언급합니다.

*   **00:22:31 - 00:23:00**:
    *   손실 값으로만은 충분하지 않으며, 정확도(Accuracy)와 같은 다른 지표를 활용하여 모델 성능을 평가해야 한다고 설명합니다.
    *   다음 단계에서는 그래프 표현과 정확도 비교를 진행할 것이라고 예고합니다.

### 3. 핵심 개념 및 코드/공식 정리

**1. Simple Linear Model 생성 함수**
*   **목적**: 모델 생성 로직을 함수로 캡슐화하여 재사용성과 코드 가독성을 높입니다.
*   **코드**:
    ```python
    def create_simple_linear_model(input_size, num_classes):
        model = SimpleLinearModel_02(input_size=input_size, num_classes=num_classes)
        model = model.to(device) # 모델을 설정된 디바이스로 이동
        return model
    ```
*   **`SimpleLinearModel_02` (모델 정의)**:
    ```python
    class SimpleLinearModel_02(nn.Module):
        def __init__(self, input_size, num_classes=10):
            super().__init__()
            self.flatten = nn.Flatten()
            self.linear_01 = nn.Linear(in_features=input_size * input_size, out_features=200)
            self.act_01 = nn.ReLU()
            self.linear_02 = nn.Linear(in_features=200, out_features=100)
            self.act_02 = nn.ReLU()
            self.linear_03 = nn.Linear(in_features=100, out_features=num_classes)

        def forward(self, x):
            x = self.flatten(x)
            x = self.act_01(self.linear_01(x))
            x = self.act_02(self.linear_02(x))
            output = self.linear_03(x)
            return output
    ```

**2. 디바이스 설정**
*   **목적**: 모델과 데이터를 GPU(CUDA) 또는 CPU 중 어떤 장치에서 연산할지 지정합니다.
*   **코드**:
    ```python
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    ```
*   **설명**: `torch.cuda.is_available()`을 통해 GPU 사용 가능 여부를 확인하고, 가능하면 'cuda'를, 아니면 'cpu'를 사용합니다.

**3. 학습 루프 (Training Loop)의 주요 구성 요소**
*   **`train_step()` 함수**: 한 에포크 동안 트레인 데이터셋을 미니 배치 단위로 학습시키는 함수.
    *   **데이터 로드**: `for batch_idx, (images, labels) in enumerate(train_loader):`
    *   **데이터 디바이스 이동**: `images = images.to(device)`, `labels = labels.to(device)`
    *   **순전파 (Forward Pass)**: `pred = model(images)`
    *   **손실 계산 (Loss Calculation)**: `loss = loss_fn(pred, labels)`
    *   **그래디언트 초기화**: `optimizer.zero_grad()`
    *   **역전파 (Backward Pass)**: `loss.backward()` (그래디언트 계산)
    *   **파라미터 업데이트**: `optimizer.step()` (가중치 업데이트)
*   **`val_step()` 함수 (검증 루프)**:
    *   **`with torch.no_grad():`**: 검증 단계에서는 그래디언트 계산 및 가중치 업데이트가 불필요하므로, 이 컨텍스트 매니저를 사용하여 메모리 효율을 높이고 실수로 가중치가 변경되는 것을 방지합니다.
    *   **데이터 로드**: `for batch_idx, (images, labels) in enumerate(val_loader):` (훈련 데이터 대신 검증 데이터 사용)
    *   **손실 계산**: `loss = loss_fn(pred, labels)`
    *   **그래디언트 관련 코드 제거**: `optimizer.zero_grad()`, `loss.backward()`, `optimizer.step()`은 검증 시 사용하지 않습니다.

**4. 손실 함수 (Loss Function)**
*   **종류**: `nn.CrossEntropyLoss()`
*   **설명**: 분류(classification) 문제에 주로 사용되는 손실 함수입니다. 예측된 로짓(logits)과 실제 라벨(정답 클래스 인덱스)을 비교하여 손실을 계산합니다. 내부적으로 Softmax와 NLLLoss가 결합되어 있습니다.
*   **코드**: `loss_fn = nn.CrossEntropyLoss()`

**5. 옵티마이저 (Optimizer)**
*   **종류**: `torch.optim.Adam`
*   **설명**: 모델의 학습 가능한 파라미터(가중치와 편향)를 업데이트하여 손실을 최소화하는 알고리즘입니다. Adam은 적응형 학습률(adaptive learning rate)을 사용하는 인기 있는 옵티마이저입니다.
*   **코드**: `optimizer = Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))`
    *   `model.parameters()`: 학습할 모델의 모든 파라미터를 가져옵니다.
    *   `lr=0.001`: 학습률(Learning Rate)을 0.001로 설정합니다.
    *   `betas=(0.9, 0.999)`: Adam 옵티마이저의 모멘텀(momentum) 계수입니다.

**6. 모델 모드 설정**
*   **`model.train()`**: 모델을 훈련 모드로 전환합니다. Dropout 레이어와 BatchNorm 레이어 등이 훈련 시와 다르게 동작하도록 설정됩니다.
*   **`model.eval()`**: 모델을 평가(검증) 모드로 전환합니다. Dropout은 비활성화되고 BatchNorm은 학습된 통계량을 사용합니다.

**7. 전체 훈련 및 검증 루프**
*   **코드**:
    ```python
    EPOCHS = 10
    # ... loss_fn, optimizer 정의 ...

    for epoch in range(EPOCHS):
        model.train() # 모델을 훈련 모드로 설정
        print(f'######{epoch+1}번째 train 시작')
        train_step()

        model.eval() # 모델을 검증 모드로 설정
        print(f'######{epoch+1}번째 validation 시작')
        val_step()
    ```

### 4. 학습 퀴즈

1.  모델 학습 시 `optimizer.zero_grad()`, `loss.backward()`, `optimizer.step()`이 각각 어떤 역할을 하는지 설명해 보세요.
2.  `model.train()`과 `model.eval()` 모드를 전환하는 이유는 무엇이며, 각 모드에서 모델의 동작에 어떤 차이가 발생할 수 있나요?
3.  검증(validation) 단계에서 `with torch.no_grad():`를 사용하는 주된 목적은 무엇인가요?