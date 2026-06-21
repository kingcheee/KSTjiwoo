# Template

날짜: 2026/06/02   (GMT+9)

> 📌 **목차**: `#Template` | `#오늘 배운 내용` | `#회고` | `#참고자료` | `#내일 학습`

---

## 1. 📝 오늘 배운 내용 요약

1. **Netflix 데이터 시각화**
    - 파이차트 (`plt.pie`): Movie vs TV Show 비율 시각화
    - `listed_in` 분할: `.str.split(', ', expand=True)` 로 다중 장르 컬럼 분리
    - 장르 빈도 집계: `.stack().value_counts()` 후 `sns.barplot()` 으로 막대그래프
2. **가설검정 (Hypothesis Testing)**
    - 와인 품질 비교: 레드 vs 화이트 t-검정 (`equal_var=False`, Welch)
    - p-value ≈ 8.17e-24 → 귀무가설 기각 → "품질 평균 유의미하게 다름"
    - 가설검정 6단계: 문제정의 → 가설설정 → 표본추출 → 통계량계산 → 유의성검정 → 결론
3. **코딩 테스트 연습**
    - Pandas: 불리언 인덱싱(`loc`), 컬럼명 공백→언더바 교체, `pd.concat()`
    - Scipy: `stats.ttest_ind()` 인자 이해 (`equal_var`의 의미)
    - if-else 기반 p-value 판단 로직 구현

---

## 2. 💭 오늘의 회고

1. **배운 점**
    - `str.split` → `expand` → `stack` 흐름이 한번에 이해됨. 기존처럼 `for`문 돌려서 분할하는 것보다 훨씬 직관적
    - `equal_var=False` 주는 의미가 분산 차이를 고려한다는 거구나. 교과서에서만 보다가 실제 코드로 보니까 와닿음
2. **어려운 점 / 개선할 점**
    - `stack()` 하고 나서 인덱스가 왜 2레벨로 생기는지 아직 직관이 안 잡힘 → 나중에 멀티인덱스 정리까지 extension으로练息练息
    - t-검정에서 `equal_var=True`일 때랑 False일 때 결과값이 어떻게 달라지는지 직접 눈으로 비교해보고 싶음
3. **액션 플랜**
    - 6/3: 멀티인덱스 다루는 법 복습 (`.reset_index()`, `.unstack()`)
    - 6/3: 와인 데이터 정규분포 시각화 추가해보기 (`sns.histplot`)
4. **함께 나누고 싶은 점**
    - Netflix 데이터에서 `rating` 컬럼도 분석하면 재미있을 거 같음 (청소년 이용가 vs 성인물 비율)

---

## 3. 📚 참고자료

- 원본: 반 친구 TIL ExportBlock (`6 2 386716bf...md`)
- Pandas `str.split`: https://pandas.pydata.org/docs/reference/api/pandas.Series.str.split.html
- Scipy t-test: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
- 수업 노트: `G:\내 드라이브\인공지능사관학교\수업 공유함_wine.ipynb`

---

## 4. 🔍 내일 학습 예정

- (수업 들은 후 채우기)

---

> ✍️ 본문은 지우가 직접 채움. 초안 제공: Teto
