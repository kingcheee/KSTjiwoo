# 🔥 6/23 Transformer/BERT 수업 복습 자료

> 규연이가 정리했당 | 데이터 분석반 딥러닝 심화 과정

---

## 📌 한 줄 요약

**"텍스트를 컴퓨터가 이해할 수 있는 숫자로 바꾸고, Transformer가 문맥을 파악하는 법"**

---

## Part 1. 딥러닝 기본 활성화 함수 복습 (14시 초반)

### 🤔 왜 다시 배우는가?
NLP 들어가기 전에, 신경망 학습의 근본인 활성화 함수를 먼저 짚고 넘어가야 해

### 핵심 3개 활성화 함수

| 함수 | 쓰이는 곳 | 역할 |
|------|----------|------|
| **ReLU** | 은닉층 (중간 계층) | 기울기 소실 문제 완화, 비선형성 부여 |
| **Sigmoid** | 출력층 (이진 분류) | 0~1 확률로 변환 (긍정/부정 같은 두 가지 분류) |
| **Softmax** | 출력층 (다중 분류) | 여러 클래스의 확률 분포로 변환 |

### 기울기 소실 (Gradient Vanishing) ⭐

계층이 깊어질수록 기울기가 0에 수렴하는 문제!

```
0.5 × 0.5 × 0.5 × ... (계속 곱하면) → 0에 수렴!
```

- **시그모이드 함수**의 문제점: 미분값 최대 0.25 → 여러 레이어 거치면 0이 됨
- **ReLU**가 해결: 0보다 큰 입력은 기울기 그대로 통과 → `f(x) = max(0, x)`

### 활성화 함수 적용 위치 규칙 ✅
- **중간 은닉층**: ReLU 사용
- **최종 출력층**: 
  - 이진 분류 → Sigmoid
  - 다중 분류 → Softmax

---

## Part 2. NLP 발전 역사

### 타임라인

```
2010년 이전: 규칙 기반 + 통계 기반 (번역 품질 쓰레기 수준 😂)
    ↓
2014년: RNN, LSTM 등장 (기울기 소실 문제 개선)
    ↓
2017년: ⭐ Transformer 등장! → "Attention is All You Need"
    ↓
2022년: ChatGPT, Gemini 등장 → 대중화
```

### NLP 발전 3요소

1. **토큰화 (Tokenization)**: 문장을 작은 단위로 자르기
2. **임베딩 (Embedding)**: 토큰을 숫자 벡터로 변환
3. **딥러닝 모델**: 벡터를 학습해서 문맥 이해 (RNN → Transformer)

---

## Part 3. 토큰화 (Tokenization) ⭐

### 🤔 왜 필요해?
컴퓨터는 텍스트를 이해 못 해. 텍스트를 **숫자로 바꿔야** 학습할 수 있어!

### 토큰화 4단계

1. **텍스트 정규화**: 소문자 변환, 특수문자/이모지 제거
2. **토큰 분할**: 공백, 문장 부호 기준으로 분리
3. **어휘 사전 매핑**: 각 토큰에 고유 숫자 ID 부여
4. **후처리**: 특수 토큰 (`[CLS]`, `[SEP]`) 추가, 패딩, 텐서 변환

### 예시
```
"Hello, world! I am learning NLP."
→ 정규화: "hello world i am learning nlp"
→ 토큰화: ['hello', 'world', 'i', 'am', 'learning', 'nlp']
→ ID 매핑: [7592, 2088, 1045, 2572, 4833, 17958]
```

### 서브워드 토큰화 (Subword Tokenization) ⭐

**"붕어빵"**을 BERT 토크나이저로 처리하면?
```
['붕', '##어', '##빵']
```

**왜 이렇게 나눠?**
- OOV(미등록 단어) 문제 해결!
- 모르는 단어도 서브워드 조합으로 이해 가능
- 일반화 능력 향상

### Python 코드로 토큰화 직접 해보기

```python
import re

def normalize(text):
    text = text.lower()                              # 소문자 변환
    text = re.sub(r'[^a-z0-9\s]', '', text)          # 특수문자 제거
    tokens = text.split()                             # 공백 기준 분할
    return tokens

test = "Hello, world! I am learning NLP."
result = normalize(test)
# 결과: ['hello', 'world', 'i', 'am', 'learning', 'nlp']
```

---

## Part 4. 임베딩 (Embedding) ⭐

### 🤔 토큰화만으로 충분해?
아니! 숫자 ID만으로는 **단어 간 관계**를 파악할 수 없어.

### 원-핫 인코딩의 문제점
- 단어 1만 개면 벡터 크기 1만 → 9,999개가 0 (메모리 낭비!)
- "고양이"와 "강아지"가 비슷하다는 걸 알 수 없음
- 💡 **비유**: 모든 단어가 "전혀 무관계"라고 적힌 명단

### 워드 임베딩 (Word Embedding)

단어를 **다차원 벡터**로 변환해서 의미적 유사도를 계산!

```
"king" - "man" + "woman" ≈ "queen"
```

- 💡 **비유**: 단어들에게 **의미 좌표**를 부여하는 마법의 지도
- 비슷한 의미의 단어는 가까운 위치에 존재!

### 임베딩 실습 코드

```python
import torch.nn as nn

embedding = nn.Embedding(
    num_embeddings=10000,   # 어휘 사전 크기
    embedding_dim=32,       # 임베딩 벡터 차원
    padding_idx=0           # 패딩 토큰의 인덱스
)
```

---

## Part 5. Hugging Face & BERT ⭐

### Hugging Face란?
미리 학습된 NLP 모델과 토크나이저를 제공하는 플랫폼
- 💡 **비유**: AI 모델의 **앱스토어** (Git/GitHub과 비슷한 개발 플랫폼)

### BERT (Bidirectional Encoder Representations from Transformer)

- **양방향**으로 문맥을 이해 (앞뒤 단어 모두 참고)
- 사전 학습(pre-trained) 모델 → 다양한 NLP 작업에 활용 가능

### BERT 실습 코드 (Hugging Face)

```python
from transformers import AutoTokenizer, AutoModel

# 1. 토크나이저 & 모델 로드
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

# 2. 토큰화 (텍스트 → 숫자 텐서)
inputs = tokenizer("Hello world!", return_tensors='pt')
# 결과: input_ids, token_type_ids, attention_mask

# 3. 모델 통과 (임베딩 추출)
outputs = model(**inputs)

# 4. 출력 확인
last_hidden_state = outputs.last_hidden_state  
# shape: [1, 8, 768] → (문장 1개, 토큰 8개, 768차원 벡터)

pooler_output = outputs.pooler_output          
# shape: [1, 768] → 문장 전체를 요약하는 [CLS] 토큰 벡터
```

### 출력 구조 이해하기

| 출력 | Shape | 의미 |
|------|-------|------|
| `last_hidden_state` | `[batch, tokens, 768]` | 각 토큰의 문맥 반영 임베딩 |
| `pooler_output` | `[batch, 768]` | `[CLS]` 토큰 기반 문장 요약 벡터 |

### 텍스트 분류 실습

```python
import torch
import torch.nn as nn

# 분류기 레이어 (768 → 2클래스)
classifier = nn.Linear(in_features=768, out_features=2)
softmax = nn.Softmax(dim=0)
labels = ['negative', 'positive']

# 문장 임베딩으로 분류
sentence_embedding = outputs.pooler_output[0]
output = classifier(sentence_embedding)
probabilities = softmax(output)
predicted_class = torch.argmax(probabilities)

print(labels[predicted_class])  # 'negative' 또는 'positive'
```

> ⚠️ 주의: 학습되지 않은 모델이므로 결과는 무작위! 실제로는 fine-tuning 필요

---

## Part 6. Transformer 핵심 개념

### RNN vs Transformer

| 특징 | RNN/LSTM | Transformer |
|------|---------|-------------|
| 처리 방식 | **순차적** (단어 하나씩) | **병렬 처리** (한번에) |
| 문맥 이해 | 단방향/양방향 | Self-Attention (전체 문맥) |
| 장기 의존성 | 어려움 (먼 단어 → 기울기 소실) | 가능 (Attention이 직접 연결) |
| 속도 | 느림 (순차 처리) | 빠름 (병렬) |

### Self-Attention 메커니즘 ⭐

Transformer의 핵심! **문장 내 모든 단어가 서로를 참고**하는 구조

💡 **비유**: 
영화 리뷰에서 "이 영화 정말 재미없는데, 배우 연기는 좋더라"라는 문장이 있을 때,
RNN은 순서대로 읽다가 "재미없는데"를 까먹을 수 있어.
Transformer는 "재미없는데"와 "좋더라"를 **동시에** 읽고 어떤 게 더 중요한지 판단해!

### Attention 공식 (직관적으로 이해하기)

```
Attention(Q, K, V) = softmax(Q × K^T / √d) × V
```

- **Q (Query)**: "나는 뭘 찾고 있지?"
- **K (Key)**: "각 단어가 가진 정보는?"
- **V (Value)**: "실제로 전달할 내용은?"

💡 **비유**: 도서관에서 책 찾기
- Query: 내가 찾고 싶은 주제
- Key: 각 책의 태그/분류
- Value: 책의 실제 내용
- 관련 높은 책에 더 집중 (Attention 점수)

---

## Part 7. CNN 복습 핵심 (9~11시 연계)

6/23 오전에 CNN 심화를 배웠는데, Transformer와 연결해서 정리!

### CNN 전체 파이프라인

```
입력 이미지 → [Conv → BN → ReLU → Pooling] × N → GAP → FC → 출력
```

### 교수님 강조 포인트 ⭐

1. **Batch Normalization은 필수 옵션!** 성능 5~10% 차이남
   - Conv 다음, ReLU 이전에 적용
   - `nn.BatchNorm2d(num_features=출력채널수)`

2. **Dropout은 훈련 시에만!** 테스트 시 절대 적용 ❌
   - 과적합 방지를 위한 기법

3. **nn.Sequential 모듈화**
   - 레고 블록처럼 레이어를 묶어서 관리
   - 특정 블록 교체(가지치기) 가능

4. **Global Average Pooling** = `nn.AdaptiveAvgPool2d(1)`
   - 입력 크기 달라도 출력 고정
   - 파라미터 수 대폭 감소

---

## Part 8. 전체 요약 & 체크포인트

### ✅ 오늘 배운 것 체크리스트

- [ ] 활성화 함수 3개 (ReLU, Sigmoid, Softmax) 위치별 사용법
- [ ] 기울기 소실 문제와 ReLU의 해결 방법
- [ ] 토큰화 4단계 (정규화 → 분할 → 매핑 → 후처리)
- [ ] 서브워드 토큰화의 개념과 이점
- [ ] 워드 임베딩이 원-핫 인코딩보다 나은 이유
- [ ] Hugging Face에서 BERT 모델 로드하고 임베딩 추출하기
- [ ] `last_hidden_state` vs `pooler_output` 차이
- [ ] Transformer가 RNN보다 나은 점 (병렬 처리, Self-Attention)
- [ ] CNN (BatchNorm, Dropout, 모듈화) 핵심 복습

### 🔥 가장 먼저 흡수해야 할 TOP 3

1. **토큰화 + 임베딩** = NLP의 기초 체력. 텍스트를 숫자로 바꾸는 과정!
2. **BERT 임베딩 추출** = Hugging Face로 문장 → 768차원 벡터 변환
3. **Transformer의 Self-Attention** = 문장 내 모든 단어가 서로 참고하는 구조

### ❓ 예상 퀴즈

**Q1. 서브워드 토큰화가 필요한 이유는?**
→ OOV(미등록 단어) 문제를 해결하기 위해. "붕어빵"을 ['붕', '##어', '##빵']으로 나누면 모르는 단어도 이해 가능!

**Q2. BERT의 pooler_output은 뭘 나타내?**
→ [CLS] 토큰의 임베딩으로, 문장 전체의 의미를 요약하는 768차원 벡터!

**Q3. Transformer가 RNN보다 빠른 이유는?**
→ RNN은 단어를 순서대로(순차적) 처리하지만, Transformer는 Self-Attention으로 모든 단어를 **동시에**(병렬) 처리하기 때문!

**Q4. Batch Normalization을 Conv 레이어 다음 어디에 두는 게 맞는가?**
→ Conv 다음, 활성화 함수(ReLU) **이전**에 적용!

---

## Part 9. 데이터 분석가 관점 활용법

| 개념 | 데이터 분석에서의 활용 |
|------|---------------------|
| Transformer/BERT | 고객 리뷰 감성 분석, 문서 분류, 개체명 인식 |
| CNN | 이미지 데이터 분류, 제품 불량 탐지 |
| 토큰화 + 임베딩 | 텍스트 데이터 전처리의 첫 단계 (모든 NLP 프로젝트) |
| Batch Normalization | 딥러닝 모델 성능 향상 필수 옵션 |
| Hugging Face | 사전 학습 모델을 활용한 빠른 NLP 프로토타이핑 |

---

## 💡 다음 수업 예습 포인트

- Transformer 내부 구조 (Multi-Head Attention, Positional Encoding)
- BERT fine-tuning (실제 데이터셋으로 학습시키기)
- GPT vs BERT 차이점

---

*복습 자료 v1.0 | 규연이가 정리했당 🐣*
*질문 있으면 언제든 말해!*
