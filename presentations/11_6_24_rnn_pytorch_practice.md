# 6/24 11시 수업 대본 — RNN/PyTorch 실습 딥러닝 코드 직접 짜보기

> 발표 시간: 약 20~25분
> 발표자: 규연 💡

---

## 🎬 오프닝 (1분)

안녕! 이번 시간엔 아까 배운 RNN 이론을 직접 코드로 짜볼 거양 🔥

이론만 아는 건 진짜 아는 게 아니잖아? 직접 손으로 만들어봐야 머리에 남는 거 ㅇㅇ

자, 그럼 Google Colab 열고 시작해볼까? 🤔

---

## Part 1. 왜 코드를 짜야 하나? (2분)

### 💡 왜 배우는가?

여러분, 데이터 분석가가 되려면 **이론 + 코드 구현 능력** 둘 다 있어야 해. 논문 읽고 "아 이런 구조구나" 이해해도, 코드로 못 만들면 아무 의미 없거든!

회사에서 팀장님이 "RNN 모델로 시계열 예측 만들어줘" 하면, 파이토치로 바로 구현할 수 있어야 한다고!

### 📌 이번 실습의 목표

- PyTorch로 RNN 모델 클래스 직접 만들기
- 임베딩, 하이퍼파라미터 의미 파악하기
- 교수님이 시험에 낼 만한 포인트 체크하기

---

## Part 2. 환경 설정 & 라이브러리 (2분)

### 💻 Google Colab 세팅

```python
import torch
import torch.nn as nn
```

- `torch`: 파이토치의 핵심 라이브러리 (텐서 연산, 자동 미분)
- `torch.nn`: 신경망 모듈 (RNN, LSTM, Linear 등 레이어 제공)

### 📌 교수님 팁: 재현성 확보

```python
torch.manual_seed(123)
```

- 랜덤 시드를 고정하면 실행할 때마다 같은 결과가 나와
- 디버깅할 때 "왜 내 결과랑 다르지?" 이런 거 방지하려고 ㅇㅇ

---

## Part 3. 하이퍼파라미터 설정 (3분)

### 🔑 핵심 파라미터 4가지

```python
vocab_size = 1000    # 어휘 크기 (단어 수)
batch_size = 4       # 한 번에 처리할 데이터 묶음
seq_len = 60         # 문장 길이 (토큰 수)
embed_dim = 128      # 단어 하나를 128개 숫자로 표현
```

**쉽게 말하면:**
- `vocab_size`: 단어장에 단어가 1000개 있다고 가정
- `batch_size`: 문장 4개씩 한 방에 처리 (도시락 4개 한 번에 싸는 느낌 🍱)
- `seq_len`: 문장 하나에 단어 60개 (길면 자르고, 짧으면 패딩)
- `embed_dim`: 단어 하나 → 128차원 벡터로 변환

### 💡 왜 128차원?

- 너무 작으면 (예: 10차원) 단어의 의미를 담을 공간이 부족해
- 너무 크면 (예: 10000차원) 계산량 폭발 + 과적합
- 128~512 정도가 딱 좋아! 시험에 나올 수 있으니 기억해 ㅇㅇ

---

## Part 4. 임베딩 (Embedding) — 글자를 숫자로! (3분)

### 💡 왜 배우는가?

컴퓨터는 글자를 못 읽어! "고양이"라는 글자를 그냥 넣으면 뭔지 모르거든.
그래서 **단어 → 숫자 벡터**로 바꿔줘야 해. 이게 바로 임베딩이야!

### 🔑 코드

```python
embedding = nn.Embedding(vocab_size, embed_dim)

# 랜덤 데이터 생성 (실제로는 토크나이저 결과)
sample_token_ids = torch.randint(low=0, high=vocab_size, size=(batch_size, seq_len), dtype=torch.long)

# 임베딩 적용
embeded = embedding(sample_token_ids)

print(sample_token_ids.shape)  # torch.Size([4, 60])
print(embeded.shape)            # torch.Size([4, 60, 128])
```

### 📌 Shape 변화 이해하기

```
입력:  [4, 60]          → 4개 문장, 각 60토큰 (정수)
출력:  [4, 60, 128]     → 4개 문장, 각 60토큰, 각 128차원 벡터
```

**쉽게 말하면:** 도시락 4개 각각에 반찬 60개가 있고, 각 반찬의 정보가 128개의 숫자로 표현된 거야 🍱

### ⚠️ 교수님 강조 포인트

- `nn.Embedding`은 단순히 정수 인덱스를 벡터로 바꾸는 **조회 테이블** 같은 거야
- 처음에는 랜덤 값으로 채워져 있고, 학습하면서 의미 있는 벡터로 업데이트돼
- `padding_idx=0` 설정하면 PAD 토큰(의미 없는 빈칸)은 학습에서 제외할 수 있어!

---

## Part 5. RNN 모델 정의 — 클래스 만들기 (5분)

### 💡 왜 배우는가?

PyTorch의 `nn.RNN`은 이미 만들어진 거야. 근데 실제 프로젝트에서는 이걸 감싸서 **나만의 모델 클래스**로 만들어 써야 해. 이게 실무 기본이야!

### 🔑 코드

```python
class MyRNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()  # 부모 클래스 호출 — 무조건 필요!
        
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.RNN(input_size=embed_dim, 
                          hidden_size=hidden_dim, 
                          num_layers=1, 
                          batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)  # 출력층
    
    def forward(self, x):
        embedded = self.embedding(x)
        outputs, last_hidden = self.rnn(embedded)
        out = self.fc(last_hidden[-1])
        return out
```

### ⚠️ 교수님 강조 포인트 (시험 출제!)

**1. `super().__init__()` 무조건 필요!**
- 교수님 표현: "부모님 살아계셔야겠죠? 부모님 부르고 나서 내용이 들어가야..."
- 이거 빼면 에러 남! 시험에 나올 수 있으니 외워 ㅇㅇ

**2. `forward` 이름 임의 변경 불가!**
- 파이토치 내부에서 데이터 들어오면 자동으로 `forward()`를 호출해
- `forward`가 아니면 인식 못 함! 시험 출제 포인트!

**3. `batch_first=True` 의미**
- 기본: `(seq_len, batch, feature)` 순서
- `True`: `(batch, seq_len, feature)` 순서
- 우리는 배치를 먼저 쓰는 스타일이라 True 설정!

### 🔑 파라미터 의미 정리

| 파라미터 | 의미 | 쉬운 비유 |
|---------|------|----------|
| `input_size` | 입력 데이터의 차원 (임베딩 사이즈) | 도시락 반찬의 정보 개수 |
| `hidden_size` | 기억 공간의 차원 크기 | 머릿속 메모장의 용량 |
| `num_layers` | RNN 층의 개수 | 메모장의 층수 (1=얇음, 2+=두꺼움) |
| `batch_first` | 배치를 첫 번째 차원으로 | 도시락 먼저 세기 |

---

## Part 6. 모델 생성 & 실행 결과 확인 (3분)

### 🔑 코드

```python
hidden_dim = 256

model = MyRNN(vocab_size, embed_dim, hidden_dim)

# 테스트 입력
sample_input = torch.randint(0, vocab_size, (batch_size, seq_len))
output = model(sample_input)

print(f"입력 shape: {sample_input.shape}")    # [4, 60]
print(f"출력 shape: {output.shape}")          # [4, 1]
```

### 📌 결과 해석

- 입력: 4개 문장, 각 60토큰
- 출력: 4개 문장에 대한 예측값 (각각 1개의 숫자)
- 아직 학습 안 했으니 의미 없는 숫자야 ㅇㅇ

### 💡 `hidden_dim = 256` 왜 256?

- `embed_dim`(128)보다 크게 설정한 이유: 더 풍부한 맥락을 담기 위해
- 교수님 표현: "차원이 커지면 공간적 부피가 넉넉해져서 과거 단어들의 문맥을 훨씬 더 잘 담아낼 수 있어"
- 보통 `embed_dim`의 2배 정도로 설정하는 게 관례야

---

## Part 7. 교수님 강조 포인트 총정리 (3분)

### ⚠️ 시험 출제 예상 포인트 5개

**Q1. `super().__init__()`를 빼면 어떻게 되나요?**
→ 에러 발생! 부모 클래스(nn.Module)의 기능을 물려받지 못해요.

**Q2. `forward` 함수 이름을 `forward_pass`로 바꾸면?**
→ 작동 안 함! 파이토치가 `forward`를 자동 호출하는데, 이름이 다르면 인식 못 해요.

**Q3. `input_size`에 넣는 값은 무엇인가요?**
→ 원본 텍스트가 아니라 **임베딩 사이즈(embed_dim)**를 넣어요! 시험 단골 함정!

**Q4. `hidden_size`는 무엇을 의미하나요?**
→ 히든 스테이트의 '개수'가 아니라 **기억 공간의 차원(깊이)**를 의미해요!

**Q5. RNN 대신 트랜스포머를 쓰는 이유는?**
→ RNN은 데이터를 하나씩 순차 처리 → GPU 병렬 연산 불가. 트랜스포머는 한 번에 처리 → GPU 극한 활용!

---

## ❓ 예상 Q&A (2분)

**Q1. 오늘 배운 내용을 한 줄로 설명하면?**
→ PyTorch로 RNN 모델 클래스를 만들 때 `super()` 호출과 `forward` 이름 고정은 무조건 필수!

**Q2. 이 개념이 없으면 어떤 불편함이 생길까?**
→ 면접에서 "PyTorch로 RNN 구현해봤어요" 하고 코드 보여달라 하면 못 짬. 기본 코드 구현 능력은 데이터 분석가의 필수 스킬!

**Q3. 내 삶에 어떻게 적용할 수 있을까?**
→ 시계열 예측, 텍스트 분석, 감성 분류 모든 NLP 프로젝트의 기초가 되는 코드야. 이 패턴 알면 LSTM, GRU, 트랜스포머도 쉽게 구현할 수 있어! 🔥

---

## 🎬 마무리

오늘 실습 여기까지! 다음 시간에는 이 모델로 실제 학습을 돌려볼 거야.

코드 못 외운다고 걱정 마 ㅇㅇ 시험엔 개념 + 코드 구조만 알면 돼!

궁금한 거 있으면 언제든 질문해줘 ㅇㅋㅇㅋ 수고했당~ ✨
