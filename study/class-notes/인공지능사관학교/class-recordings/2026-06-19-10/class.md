## 6_19 10시 PyTorch 선형 모델 학습 수업 노트

### 1. 강의 핵심 요약

6월 19일 10시 수업은 PyTorch를 사용하여 FashionMNIST 데이터셋을 위한 간단한 선형 모델(다층 퍼셉트론)을 구축하고 학습하는 과정을 다룹니다. 모델 정의, 데이터 로딩, 그리고 훈련 및 검증 에폭 구현을 통해 PyTorch 기본 워크플로우를 이해하는 데 중점을 둡니다. 특히, `tqdm`을 활용한 학습 진행 상황 시각화 및 `matplotlib`을 이용한 학습 곡선(손실, 정확도) 플로팅 방법까지 실습합니다.

### 2. 화면 연계 타임라인 노트

*   **00:00:00 - 00:00:20**: `SimpleLinearModel_02` 클래스의 `forward` 함수와 `linear_03` 레이어 정의 코드가 화면에 보이며, 모델 출력 `(32, 10)`의 형태가 주석으로 표시되어 있습니다.
*   **00:00:20 - 00:02:41**: 새로운 Google Colab 노트북을 열고 런타임을 연결하는 과정이 진행됩니다. "450_신경망3.ipynb"라는 제목의 노트북이 생성됩니다.
*   **00:02:41 - 00:03:01**:
    *   **오디오**: 강사는 데이터를 가져와야 하므로 데이터 로딩 코드부터 작성했다고 설명합니다. FashionMNIST 데이터셋을 사용하며, `root`, `train`, `download`, `transform=ToTensor()` 파라미터에 대해 설명합니다.
    *   **화면**: `torchvision`에서 `datasets`와 `transforms`, `torch.utils.data`에서 `DataLoader`를 import 하는 코드와 FashionMNIST 데이터셋을 로딩하는 코드가 보입니다. `train_data`의 길이는 `60000`, `shape`는 `torch.Size([60000, 28, 28])`로 출력됩니다.
    ```python
    from torchvision import datasets, transforms
    from torch.utils.data import DataLoader
    import torch

    train_data = datasets.FashionMNIST(root='data', train=True, download=True, transform=transforms.ToTensor())
    val_data = datasets.FashionMNIST(root='data', train=False, download=True, transform=transforms.ToTensor())
    print(len(train_data))
    # 60000
    print(train_data.data.shape) # .data를 추가해야 (N,H,W) 반환
    # torch.Size([60000, 28, 28])
    ```
*   **00:03:01 - 00:03:21**:
    *   **오디오**: `BATCH_SIZE`를 32로 설정하고 `DataLoader`를 사용하여 `train_loader`와 `val_loader`를 생성하는 과정을 설명합니다. `shuffle=True`와 `num_workers=4`의 의미를 언급합니다.
    *   **화면**: `BATCH_SIZE = 32`와 `DataLoader` 인스턴스 생성 코드가 나타납니다.
    ```python
    BATCH_SIZE = 32
    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
    ```
*   **00:03:21 - 00:03:41**:
    *   **오디오**: `DataLoader`에서 하나의 배치를 가져와 이미지와 라벨의 형태를 확인하는 방법을 설명합니다.
    *   **화면**: `next(iter(train_loader))`를 통해 첫 번째 배치를 가져오고, `images.shape`와 `labels.shape`를 출력하는 코드가 실행됩니다. 출력 결과는 `torch.Size([32, 1, 28, 28])`와 `torch.Size([32])`입니다.
    ```python
    images, labels = next(iter(train_loader))
    print(images.shape, labels.shape)
    # torch.Size([32, 1, 28, 28]) torch.Size([32])
    ```
*   **00:03:41 - 00:05:22**:
    *   **오디오**: 이전 시간에 구성했던 `SimpleLinearModel_02` 모델의 구조를 다시 설명합니다. 세 개의 `nn.Linear` 레이어와 `F.relu` 활성화 함수를 사용하여 다층 퍼셉트론을 구현했다고 언급합니다. 인풋이 28x28 픽셀 이미지 32장이 배치로 들어오는 형태라고 설명합니다.
    *   **화면**: `SimpleLinearModel_02` 클래스 정의 코드가 나타납니다. `__init__`에서 `nn.Linear` 레이어 세 개를 정의하고, `forward` 메서드에서 `torch.flatten`, `F.relu`를 적용하는 로직이 포함되어 있습니다.
    ```python
    import torch.nn as nn
    import torch.nn.functional as F

    class SimpleLinearModel_02(nn.Module):
        def __init__(self, input_size, num_classes=10):
            super().__init__()
            self.linear_01 = nn.Linear(in_features=input_size*input_size, out_features=200)
            self.linear_02 = nn.Linear(in_features=200, out_features=100)
            self.linear_03 = nn.Linear(in_features=100, out_features=num_classes)

        def forward(self, x): # (32, 1, 28, 28)
            x = torch.flatten(x, start_dim=1, end_dim=-1)
            x = F.relu(self.linear_01(x))
            x = F.relu(self.linear_02(x))
            output = self.linear_03(x)
            return output # (32, 10)
    ```
*   **00:05:22 - 00:07:23**:
    *   **오디오**: 모델을 인스턴스화하고, 샘플 이미지 배치를 모델에 통과시켜 출력 형태를 확인합니다. `input_size`와 `num_classes`를 28과 10으로 설정하여 모델을 생성합니다.
    *   **화면**: `INPUT_SIZE = 28`, `NUM_CLASSES = 10` 정의 후, `SimpleLinearModel_02` 인스턴스를 생성하고 이미지에 대한 출력을 계산한 뒤, 출력(`output.shape`)이 `torch.Size([32, 10])`임을 확인합니다.
    ```python
    INPUT_SIZE = 28
    NUM_CLASSES = 10
    model_02 = SimpleLinearModel_02(input_size=INPUT_SIZE, num_classes=NUM_CLASSES)
    output = model_02(images)
    print(output.shape)
    # torch.Size([32, 10])
    ```
*   **00:07:23 - 00:08:23**:
    *   **오디오**: 모델 생성 코드를 함수로 묶어(`create_simple_linear_model`) 재사용성을 높입니다. GPU 사용 가능 여부를 확인하여 `device`를 설정하고, 모델을 해당 디바이스로 옮깁니다. 손실 함수로 `nn.CrossEntropyLoss()`를 정의하고 `Adam` 옵티마이저를 import 합니다.
    *   **화면**:
    ```python
    def create_simple_linear_model(input_size, num_classes=10):
        model = SimpleLinearModel_02(input_size=input_size, num_classes=num_classes)
        return model

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = create_simple_linear_model(input_size=28, num_classes=10)
    model.to(device)

    loss_fn = nn.CrossEntropyLoss()
    from torch.optim import Adam
    ```
*   **00:08:23 - 00:21:28**:
    *   **오디오**: `create_simple_linear_model` 함수로 생성된 모델의 구조를 출력하여 확인합니다.
    *   **화면**: `print(model)` 코드가 실행되고, 모델의 각 `nn.Linear` 레이어(linear_01, linear_02, linear_03)의 `in_features`, `out_features`, `bias` 정보가 출력됩니다.
*   **00:21:28 - 00:22:08**:
    *   **오디오**: "모델이 준비됐고, 데이터도 준비됐고, 이제 학습시키는 코드를 만들 것"이라고 언급하며, `tqdm` 라이브러리를 import 합니다.
    *   **화면**: `from tqdm import tqdm` 코드가 추가됩니다.
*   **00:22:08 - 00:24:49**:
    *   **오디오**: `Trainer` 클래스의 `__init__` 메서드를 설명합니다. 이 메서드는 모델, 손실 함수, 옵티마이저, 훈련/검증 데이터 로더, 디바이스를 받아 초기화하며 모델을 지정된 디바이스로 옮깁니다.
    *   **화면**: `Trainer` 클래스와 `__init__` 메서드가 정의됩니다.
    ```python
    class Trainer:
        def __init__(self, model, loss_fn, optimizer, train_loader, val_loader, device=None):
            self.model = model.to(device)
            self.loss_fn = loss_fn
            self.optimizer = optimizer
            self.train_loader = train_loader
            self.val_loader = val_loader
            self.device = device
    ```
*   **00:24:49 - 00:32:52**:
    *   **오디오**: `train_epoch` 메서드를 정의하며, 모델을 `train` 모드로 설정하고 `tqdm`으로 진행률 표시줄을 생성하는 과정을 설명합니다. 각 배치에서 입력(`inputs`)과 목표(`targets`)를 디바이스로 옮기는 코드를 작성합니다.
    *   **화면**: `train_epoch` 메서드의 초기 부분이 작성됩니다.
    ```python
    def train_epoch(self, epoch):
        self.model.train()
        with tqdm(total=len(self.train_loader), desc=f'Epoch {epoch+1} [Training...]', leave=True) as progress_bar:
            for batch_idx, (inputs, targets) in enumerate(self.train_loader):
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)
    ```
*   **00:32:52 - 00:39:54**:
    *   **오디오**: 학습의 핵심 단계인 순방향(`outputs = self.model(inputs)`), 손실 계산(`loss = self.loss_fn(outputs, targets)`), 옵티마이저 초기화(`zero_grad`), 역전파(`loss.backward()`), 가중치 업데이트(`optimizer.step()`)를 설명합니다. `tqdm` 진행률 표시줄 업데이트 및 배치 손실을 postfix로 표시하는 로직을 추가합니다.
    *   **화면**: `train_epoch` 메서드 내부의 완전한 학습 루프 코드가 작성됩니다.
    ```python
                outputs = self.model(inputs)
                loss = self.loss_fn(outputs, targets)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                progress_bar.update(1)
                if batch_idx % 20 == 0:
                    progress_bar.set_postfix({'Batch Loss': loss.item()})
                # 마지막 배치에서 최종 손실을 표시
                if (batch_idx + 1) == len(self.train_loader):
                    progress_bar.set_postfix({'Batch Loss': loss.item()})
    ```
*   **00:39:54 - 00:43:56**:
    *   **오디오**: `validate_epoch` 메서드를 정의합니다. 유효성 검사 로더가 없으면 `None`을 반환하도록 하고, 모델을 `eval()` 모드로 설정합니다. `torch.no_grad()` 컨텍스트 매니저를 사용하여 기울기 계산을 비활성화하여 메모리와 시간을 절약하는 이유를 설명합니다.
    *   **화면**: `validate_epoch` 메서드의 초기 부분이 작성됩니다. 학습 에폭과 유사하게 `tqdm`을 사용하지만, `optimizer` 관련 코드는 없습니다.
    ```python
    def validate_epoch(self, epoch):
        if not self.val_loader:
            return None
        self.model.eval()
        with tqdm(total=len(self.val_loader), desc=f'Epoch {epoch+1} [Validating...]', leave=True) as progress_bar:
            with torch.no_grad():
                for batch_idx, (inputs, targets) in enumerate(self.val_loader):
                    inputs = inputs.to(self.device)
                    targets = targets.to(self.device)
                    outputs = self.model(inputs)
                    loss = self.loss_fn(outputs, targets)
                    # (이후 루프 내 코드 추가 예정)
    ```
*   **00:43:56 - 00:48:53**:
    *   **오디오**: `validate_epoch` 메서드의 나머지 부분을 설명합니다. `train_epoch`과 유사하게 손실을 계산하고 `tqdm`을 업데이트하지만, 모델 파라미터를 업데이트하는 역전파 및 `optimizer.step()` 과정은 생략됩니다.
    *   **화면**: `validate_epoch` 메서드의 루프 내부 코드가 완성됩니다.
    ```python
                    progress_bar.update(1)
                    if batch_idx % 20 == 0:
                        progress_bar.set_postfix({'Batch Loss': loss.item()})
                    if (batch_idx + 1) == len(self.val_loader):
                        progress_bar.set_postfix({'Batch Loss': loss.item()})
    ```
*   **04:53:05 - 07:18:45**: 화면에 이전 모델 정의 코드(`SimpleLinearModel_02`)가 계속 표시됩니다. 강사의 설명 없이 잠시 정지된 상태로 보입니다. (별도 활동 또는 내부 준비 시간)
*   **07:18:45 - 07:22:45**:
    *   **오디오**: `Trainer` 클래스에 `train`이라는 메인 학습 메서드를 추가한다고 설명합니다. 이 메서드는 여러 에폭을 반복하면서 `train_epoch`와 `validate_epoch`를 호출합니다.
    *   **화면**: `train` 메서드가 `Trainer` 클래스에 추가됩니다.
    ```python
    # Trainer 클래스 내부에 추가
    def train(self, epochs):
        for epoch in range(epochs):
            self.train_epoch(epoch)
            self.validate_epoch(epoch)
    ```
*   **07:22:45 - 07:24:05**:
    *   **오디오**: 메인 함수 블록(`if __name__ == '__main__':`)을 만들어서 `Trainer`를 인스턴스화하고 실제 학습을 시작하는 과정을 설명합니다.
    *   **화면**: 메인 실행 블록이 작성됩니다.
    ```python
    if __name__ == '__main__':
        # device, model, loss_fn 정의 (이전 코드 활용)
        optimizer = Adam(model.parameters(), lr=0.001) # 옵티마이저 정의 추가
        trainer = Trainer(model, loss_fn, optimizer, train_loader, val_loader, device=device)
        epochs = 10
        trainer.train(epochs)
    ```
*   **07:24:05 - 07:38:05**:
    *   **오디오**: 코드가 실행되며 학습이 진행되는 것을 확인할 수 있다고 말합니다.
    *   **화면**: `tqdm` 진행률 표시줄이 나타나며, 훈련 에폭과 검증 에폭의 손실이 실시간으로 표시됩니다.
*   **07:38:05 - 07:44:05**:
    *   **오디오**: 학습이 완료되었다고 알립니다.
    *   **화면**: 모든 에폭의 학습이 완료된 후 `tqdm` 출력이 멈춥니다.
*   **07:44:05 - 07:46:05**:
    *   **오디오**: 정확도를 계산하는 헬퍼 함수 `_calculate_accuracy`를 추가한다고 설명합니다. 예측된 클래스와 실제 라벨을 비교하여 정확도를 구하는 원리를 설명합니다.
    *   **화면**: `Trainer` 클래스 내부에 `_calculate_accuracy` 메서드가 추가됩니다.
    ```python
    # Trainer 클래스 내부에 추가
    def _calculate_accuracy(self, outputs, targets):
        _, predicted = torch.max(outputs, 1)
        correct = (predicted == targets).sum().item()
        total = targets.size(0)
        accuracy = correct / total
        return accuracy
    ```
*   **07:46:05 - 07:54:05**:
    *   **오디오**: `validate_epoch` 메서드에서 총 손실과 총 정확도를 누적하여 기록하는 부분을 설명합니다.
    *   **화면**: `validate_epoch` 메서드 내부에 `total_loss`와 `total_accuracy` 변수가 초기화되고, 루프 내에서 각 배치에 대한 손실과 정확도가 누적됩니다.
    ```python
    # validate_epoch 메서드 내부 (루프 진입 전)
    total_loss = 0
    total_accuracy = 0
    # validate_epoch 메서드 내부 (루프 안)
    total_loss += loss.item()
    total_accuracy += self._calculate_accuracy(outputs, targets)
    ```
*   **07:54:05 - 08:00:05**:
    *   **오디오**: `validate_epoch` 루프가 끝난 후 평균 손실과 평균 정확도를 계산하고 `tqdm`의 postfix로 표시한 뒤, 이 값들을 반환하도록 설명합니다.
    *   **화면**: `validate_epoch` 메서드 루프 종료 후 평균 계산 및 postfix 설정 코드가 추가됩니다.
    ```python
    # validate_epoch 메서드 내부 (루프 종료 후)
    avg_loss = total_loss / len(self.val_loader)
    avg_accuracy = total_accuracy / len(self.val_loader)
    progress_bar.set_postfix({'Avg Loss': avg_loss, 'Avg Acc': avg_accuracy})
    return avg_loss, avg_accuracy
    ```
*   **08:00:05 - 08:14:05**:
    *   **오디오**: `train_epoch` 메서드에서도 `validate_epoch`와 동일하게 총 손실과 총 정확도를 누적하고, 루프 종료 후 평균을 계산하여 `tqdm` postfix로 표시한 뒤 반환하도록 수정하는 과정을 설명합니다.
    *   **화면**: `train_epoch` 메서드 내부에 `total_loss`, `total_accuracy` 초기화 및 루프 내 누적, 루프 종료 후 평균 계산 및 postfix 설정 코드가 추가됩니다.
    ```python
    # train_epoch 메서드 내부 (루프 진입 전)
    total_loss = 0
    total_accuracy = 0
    # train_epoch 메서드 내부 (루프 안)
    total_loss += loss.item()
    total_accuracy += self._calculate_accuracy(outputs, targets)
    # train_epoch 메서드 내부 (루프 종료 후)
    avg_loss = total_loss / len(self.train_loader)
    avg_accuracy = total_accuracy / len(self.train_loader)
    progress_bar.set_postfix({'Avg Loss': avg_loss, 'Avg Acc': avg_accuracy})
    return avg_loss, avg_accuracy
    ```
*   **08:14:05 - 08:16:05**:
    *   **오디오**: `train` 메서드에서 `train_epoch`와 `validate_epoch`의 반환 값을 변수에 저장하도록 수정합니다.
    *   **화면**: `train` 메서드 내부에 반환 값을 할당하는 코드가 추가됩니다.
    ```python
    # train 메서드 내부
    train_loss, train_acc = self.train_epoch(epoch)
    val_loss, val_acc = self.validate_epoch(epoch)
    ```
*   **08:16:05 - 08:29:45**:
    *   **오디오**: 수정된 코드를 실행하며, 이제 학습 진행 상황과 함께 정확도까지 잘 표시되는 것을 확인할 수 있다고 말합니다.
    *   **화면**: `tqdm` 진행률 표시줄에 `Avg Loss`와 `Avg Acc`가 훈련 및 검증 에폭 모두에 대해 표시됩니다.
*   **08:29:45 - 10:04:45**: 화면이 잠시 멈추거나 이전 코드를 스크롤하는 등의 활동이 이어집니다.
*   **10:04:45 - 10:08:45**:
    *   **오디오**: 학습 과정을 저장할 수 있도록 `Trainer` 클래스에 리스트 변수(`train_losses`, `train_accuracies`, `val_losses`, `val_accuracies`)를 추가하고, 각 에폭이 끝날 때마다 해당 값들을 리스트에 추가한다고 설명합니다.
    *   **화면**: `Trainer` 클래스의 `__init__` 메서드에 `self.train_losses` 등 리스트 초기화 코드가, `train` 메서드 내부에 `append` 코드가 추가됩니다.
    ```python
    # Trainer.__init__ 메서드 내부에 추가
    self.train_losses = []
    self.train_accuracies = []
    self.val_losses = []
    self.val_accuracies = []
    # Trainer.train 메서드 루프 내부에 추가
    self.train_losses.append(train_loss)
    self.train_accuracies.append(train_acc)
    self.val_losses.append(val_loss)
    self.val_accuracies.append(val_acc)
    ```
*   **10:08:45 - 10:16:45**:
    *   **오디오**: 수정된 코드를 다시 실행하며, 학습이 완료되었다고 언급합니다.
    *   **화면**: 학습이 다시 진행되고 `tqdm` 진행률이 표시됩니다.
*   **10:16:45 - 10:24:45**:
    *   **오디오**: `matplotlib.pyplot`을 사용하여 학습된 손실과 정확도 추이를 시각화하는 코드를 추가한다고 설명합니다. 훈련 손실/정확도와 검증 손실/정확도를 각각 플로팅하여 비교합니다.
    *   **화면**: `matplotlib.pyplot` 및 `numpy` import 후, `plt.figure`, `plt.subplot`, `plt.plot`, `plt.title`, `plt.xlabel`, `plt.ylabel`, `plt.legend`, `plt.tight_layout`, `plt.show()`를 사용하여 두 개의 그래프(Loss, Accuracy)를 그리는 코드가 추가됩니다.
    ```python
    import matplotlib.pyplot as plt
    import numpy as np # 혹시 모를 numpy 사용을 위해

    # ... (Trainer 인스턴스 생성 및 학습 코드) ...

    # Plotting
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(trainer.train_losses, label='Train Loss')
    plt.plot(trainer.val_losses, label='Validation Loss')
    plt.title('Loss over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(trainer.train_accuracies, label='Train Accuracy')
    plt.plot(trainer.val_accuracies, label='Validation Accuracy')
    plt.title('Accuracy over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.tight_layout()
    plt.show()
    ```
*   **10:24:45 - 10:28:45**:
    *   **오디오**: 최종 학습이 완료되었고, 학습된 결과를 보면 손실이 줄어들고 정확도가 올라가는 것을 그래프를 통해 확인할 수 있다고 설명합니다.
    *   **화면**: 학습 완료 후 생성된 손실 및 정확도 그래프가 표시됩니다. 그래프는 훈련 손실과 검증 손실이 에폭이 지남에 따라 감소하는 추세와 훈련 정확도 및 검증 정확도가 증가하는 추세를 보여줍니다.

### 3. 핵심 개념 및 코드/공식 정리

#### 3.1. `SimpleLinearModel_02` 모델 정의

FashionMNIST 이미지 분류를 위한 다층 퍼셉트론(MLP) 모델입니다.

```python
import torch.nn as nn
import torch.nn.functional as F

class SimpleLinearModel_02(nn.Module):
    def __init__(self, input_size, num_classes=10):
        super().__init__()
        # 첫 번째 선형 레이어: 28*28 픽셀 -> 200 특징
        self.linear_01 = nn.Linear(in_features=input_size*input_size, out_features=200)
        # 두 번째 선형 레이어: 200 특징 -> 100 특징
        self.linear_02 = nn.Linear(in_features=200, out_features=100)
        # 세 번째(출력) 선형 레이어: 100 특징 -> num_classes (10개의 클래스)
        self.linear_03 = nn.Linear(in_features=100, out_features=num_classes)

    def forward(self, x): # 입력 x 형태: (batch_size, 1, 28, 28)
        # 이미지를 1D 벡터로 평탄화 (28*28 = 784)
        x = torch.flatten(x, start_dim=1, end_dim=-1) # (batch_size, 784)
        # 첫 번째 선형 레이어와 ReLU 활성화 함수
        x = F.relu(self.linear_01(x)) # (batch_size, 200)
        # 두 번째 선형 레이어와 ReLU 활성화 함수
        x = F.relu(self.linear_02(x)) # (batch_size, 100)
        # 최종 출력 레이어
        output = self.linear_03(x) # (batch_size, num_classes)
        return output
```

*   **`nn.Module`**: 모든 PyTorch 신경망 모듈의 기본 클래스입니다. 사용자 정의 모델은 이 클래스를 상속받아야 합니다.
*   **`__init__(self, ...)`**: 모델의 레이어와 구성 요소를 정의합니다.
    *   `super().__init__()`: 부모 클래스 `nn.Module`의 생성자를 호출합니다.
    *   `nn.Linear(in_features, out_features)`: 입력 특징 수와 출력 특징 수를 지정하는 선형 변환 레이어입니다.
*   **`forward(self, x)`**: 모델의 순방향 연산(데이터가 모델을 통과하는 방식)을 정의합니다.
    *   `torch.flatten(x, start_dim=1, end_dim=-1)`: 입력 텐서 `x`를 지정된 차원(`start_dim`부터 `end_dim`까지)을 평탄화합니다. 이미지 데이터 `(Batch, Channel, Height, Width)`를 `(Batch, Channel * Height * Width)` 형태로 만듭니다. 여기서 채널은 1, 높이/너비는 28이므로 `(Batch, 1*28*28)`이 됩니다.
    *   `F.relu(input)`: ReLU(Rectified Linear Unit) 활성화 함수를 적용합니다. 음수 값을 0으로 만들고 양수 값을 그대로 유지합니다. `nn.functional` 모듈에서 제공합니다.

#### 3.2. 데이터 로딩 및 전처리

```python
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# FashionMNIST 데이터셋 로딩
train_data = datasets.FashionMNIST(root='data', train=True, download=True, transform=transforms.ToTensor())
val_data = datasets.FashionMNIST(root='data', train=False, download=True, transform=transforms.ToTensor())

# 데이터 로더 설정
BATCH_SIZE = 32
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
```

*   **`torchvision.datasets.FashionMNIST`**: FashionMNIST 데이터셋을 자동으로 다운로드하고 로드하는 클래스입니다.
    *   `root='data'`: 데이터셋이 저장될 로컬 디렉토리 경로.
    *   `train=True/False`: 훈련(True) 또는 검증(False) 데이터셋을 로드할지 지정.
    *   `download=True`: `root` 경로에 데이터셋이 없으면 다운로드.
    *   `transform=transforms.ToTensor()`: PIL Image 형태의 이미지를 PyTorch 텐서로 변환하고 픽셀 값을 [0, 1] 범위로 정규화합니다.
*   **`torch.utils.data.DataLoader`**: 데이터셋을 배치 단위로 묶어 모델에 공급하는 반복자(iterator)를 생성합니다.
    *   `batch_size`: 한 번에 처리할 샘플의 수.
    *   `shuffle=True`: 각 에폭마다 데이터를 무작위로 섞습니다.
    *   `num_workers=4`: 데이터를 로드하는 데 사용할 서브프로세스의 수. CPU 코어 수에 따라 적절히 설정합니다.

#### 3.3. `Trainer` 클래스를 이용한 학습 및 검증 루프

모델 학습의 전체 과정을 관리하는 클래스입니다.

```python
from tqdm import tqdm
import torch.optim as optim
import matplotlib.pyplot as plt

class Trainer:
    def __init__(self, model, loss_fn, optimizer, train_loader, val_loader, device=None):
        self.model = model.to(device) # 모델을 지정된 디바이스로 이동
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device

        # 학습 과정 기록을 위한 리스트 초기화
        self.train_losses = []
        self.train_accuracies = []
        self.val_losses = []
        self.val_accuracies = []

    def _calculate_accuracy(self, outputs, targets):
        # 모델 출력에서 가장 높은 확률을 가진 클래스 인덱스 (예측값) 가져오기
        _, predicted = torch.max(outputs, 1)
        # 예측값과 실제값(targets)이 일치하는 개수 계산
        correct = (predicted == targets).sum().item()
        # 전체 샘플 수
        total = targets.size(0)
        # 정확도 계산
        accuracy = correct / total
        return accuracy

    def train_epoch(self, epoch):
        self.model.train() # 모델을 훈련 모드로 설정 (Dropout, BatchNorm 등이 활성화됨)
        total_loss = 0
        total_accuracy = 0
        # tqdm을 이용하여 진행률 바 표시
        with tqdm(total=len(self.train_loader), desc=f'Epoch {epoch+1} [Training...]', leave=True) as progress_bar:
            for batch_idx, (inputs, targets) in enumerate(self.train_loader):
                inputs = inputs.to(self.device) # 입력 데이터를 디바이스로 이동
                targets = targets.to(self.device) # 목표 라벨을 디바이스로 이동

                outputs = self.model(inputs) # 순방향 전달 (Forward pass)
                loss = self.loss_fn(outputs, targets) # 손실 계산

                self.optimizer.zero_grad() # 이전 기울기 초기화
                loss.backward() # 역전파 (Backward pass): 기울기 계산
                self.optimizer.step() # 옵티마이저 스텝: 모델 파라미터 업데이트

                total_loss += loss.item()
                total_accuracy += self._calculate_accuracy(outputs, targets)

                progress_bar.update(1) # 진행률 바 업데이트
                if batch_idx % 20 == 0 or (batch_idx + 1) == len(self.train_loader): # 20 배치마다 또는 마지막 배치에서 손실 표시
                    progress_bar.set_postfix({'Batch Loss': loss.item()})
        
        avg_loss = total_loss / len(self.train_loader)
        avg_accuracy = total_accuracy / len(self.train_loader)
        progress_bar.set_postfix({'Avg Loss': avg_loss, 'Avg Acc': avg_accuracy})
        return avg_loss, avg_accuracy

    def validate_epoch(self, epoch):
        if not self.val_loader: # 유효성 검사 로더가 없으면 None 반환
            return None
        self.model.eval() # 모델을 평가 모드로 설정 (Dropout, BatchNorm 등이 비활성화됨)
        total_loss = 0
        total_accuracy = 0
        with tqdm(total=len(self.val_loader), desc=f'Epoch {epoch+1} [Validating...]', leave=True) as progress_bar:
            with torch.no_grad(): # 기울기 계산 비활성화 (메모리 및 시간 절약)
                for batch_idx, (inputs, targets) in enumerate(self.val_loader):
                    inputs = inputs.to(self.device)
                    targets = targets.to(self.device)

                    outputs = self.model(inputs)
                    loss = self.loss_fn(outputs, targets)

                    total_loss += loss.item()
                    total_accuracy += self._calculate_accuracy(outputs, targets)

                    progress_bar.update(1)
                    if batch_idx % 20 == 0 or (batch_idx + 1) == len(self.val_loader): # 20 배치마다 또는 마지막 배치에서 손실 표시
                        progress_bar.set_postfix({'Batch Loss': loss.item()})
        
        avg_loss = total_loss / len(self.val_loader)
        avg_accuracy = total_accuracy / len(self.val_loader)
        progress_bar.set_postfix({'Avg Loss': avg_loss, 'Avg Acc': avg_accuracy})
        return avg_loss, avg_accuracy

    def train(self, epochs):
        for epoch in range(epochs):
            train_loss, train_acc = self.train_epoch(epoch)
            val_loss, val_acc = self.validate_epoch(epoch)
            
            # 에폭별 결과 저장
            self.train_losses.append(train_loss)
            self.train_accuracies.append(train_acc)
            self.val_losses.append(val_loss)
            self.val_accuracies.append(val_acc)
```

*   **`self.model.train()`**: 모델을 훈련 모드로 설정합니다. `nn.Dropout` 레이어가 활성화되고, `nn.BatchNorm` 레이어가 배치 통계를 업데이트합니다.
*   **`self.model.eval()`**: 모델을 평가 모드로 설정합니다. `nn.Dropout` 레이어가 비활성화되고, `nn.BatchNorm` 레이어가 훈련 시 학습된 통계(이동 평균 및 분산)를 사용합니다.
*   **`torch.no_grad()`**: 이 컨텍스트 매니저 내부에서는 PyTorch가 기울기를 계산하거나 저장하지 않습니다. 이는 평가 단계에서 메모리 사용량을 줄이고 계산 속도를 높이는 데 유용합니다.
*   **`self.optimizer.zero_grad()`**: 각 학습 배치마다 이전에 계산된 기울기 값을 0으로 초기화합니다.
*   **`loss.backward()`**: 계산된 손실(`loss`)을 기준으로 모델 파라미터들의 기울기를 계산합니다.
*   **`self.optimizer.step()`**: `backward()` 호출 후 계산된 기울기를 사용하여 모델의 파라미터(가중치)를 업데이트합니다.
*   **`tqdm`**: 반복문의 진행률을 시각적으로 표시하는 라이브러리입니다. `desc` 인자로 설명 텍스트를, `set_postfix`로 추가 정보를 표시할 수 있습니다.
*   **`_calculate_accuracy`**: 모델의 출력을 소프트맥스(또는 로짓)로 간주하여 가장 높은 값의 인덱스를 예측 클래스로 사용하고, 실제 타겟과 비교하여 정확도를 계산합니다.

#### 3.4. 메인 실행 블록 및 시각화

```python
if __name__ == '__main__':
    # 모델, 손실 함수, 옵티마이저 정의 (이전 코드에서 가져옴)
    model = create_simple_linear_model(input_size=28, num_classes=10)
    model.to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=0.001)

    trainer = Trainer(model, loss_fn, optimizer, train_loader, val_loader, device=device)
    epochs = 10
    trainer.train(epochs) # 학습 시작

    # 학습 과정 시각화
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1) # 1행 2열 중 첫 번째 플롯
    plt.plot(trainer.train_losses, label='Train Loss')
    plt.plot(trainer.val_losses, label='Validation Loss')
    plt.title('Loss over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 2, 2) # 1행 2열 중 두 번째 플롯
    plt.plot(trainer.train_accuracies, label='Train Accuracy')
    plt.plot(trainer.val_accuracies, label='Validation Accuracy')
    plt.title('Accuracy over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.tight_layout() # 서브플롯 간의 간격 자동 조절
    plt.show() # 그래프 표시
```

*   **`if __name__ == '__main__':`**: 파이썬 스크립트가 직접 실행될 때만 내부 코드가 실행되도록 하는 표준 관용구.
*   **`matplotlib.pyplot`**: 파이썬에서 그래프를 그리는 데 사용되는 라이브러리입니다.
    *   `plt.figure(figsize=(...))`: 그래프의 전체 크기를 설정합니다.
    *   `plt.subplot(rows, cols, index)`: 여러 개의 플롯을 한 화면에 그릴 때 사용합니다.
    *   `plt.plot(x_values, y_values, label=...)`: 데이터를 선 그래프로 그립니다.
    *   `plt.title(...)`, `plt.xlabel(...)`, `plt.ylabel(...)`: 그래프의 제목 및 축 레이블을 설정합니다.
    *   `plt.legend()`: 각 선에 대한 범례를 표시합니다.
    *   `plt.tight_layout()`: 플롯 요소들이 겹치지 않도록 자동으로 조정합니다.
    *   `plt.show()`: 생성된 그래프를 화면에 표시합니다.

### 4. 학습 퀴즈

1.  `SimpleLinearModel_02` 클래스의 `forward` 메서드에서 `torch.flatten(x, start_dim=1, end_dim=-1)`이 `(32, 1, 28, 28)` 형태의 입력 `x`를 어떻게 변환하고, 이 변환이 필요한 이유를 설명하시오.
2.  `Trainer` 클래스의 `train_epoch`와 `validate_epoch` 메서드에서 `self.model.train()`과 `self.model.eval()`의 역할 및 `torch.no_grad()` 컨텍스트 매니저를 `validate_epoch`에서 사용하는 이유를 설명하시오.
3.  PyTorch에서 FashionMNIST 데이터셋을 로드할 때 `transforms.ToTensor()`를 적용하는 주된 목적은 무엇이며, 이 변환을 통해 데이터가 어떤 형태로 바뀌게 되는지 서술하시오.