const fs = require('fs');
const path = require('path');
const { google } = require('C:/Users/sxeyc/node_modules/googleapis');

// Load Google authorization info
const credentials = JSON.parse(fs.readFileSync(path.join(__dirname, 'credentials.json'), 'utf-8'));
const token = JSON.parse(fs.readFileSync(path.join(__dirname, 'token.json'), 'utf-8'));

const clientConfig = credentials.installed || credentials.web;
const { client_secret, client_id, redirect_uris } = clientConfig;
const oAuth2Client = new google.auth.OAuth2(
  client_id,
  client_secret,
  redirect_uris ? redirect_uris[0] : 'urn:ietf:wg:oauth:2.0:oob'
);
oAuth2Client.setCredentials(token);

const drive = google.drive({ version: 'v3', auth: oAuth2Client });
const desktopPath = 'C:/Users/sxeyc/Desktop';
const reportFile = path.join(desktopPath, 'Study_Progress_Report.md');

// Core topics configuration
const TOPICS = {
  'PyTorch Basics (파이토치 기초)': {
    keywords: ['torch.tensor', 'torch.from_numpy', '.ndim', '.shape', 'np.arange', '.reshape'],
    why: '인공신경망을 다차원 행렬 연산으로 빠르게 연산하기 위한 딥러닝 핵심 라이브러리입니다. GPU 가속 연산을 지원하고 미분 계산을 자동화하여 현대 딥러닝 모델 구현의 필수 기초가 됩니다.',
    meaning: '* **Tensor**: 파이토치에서 다차원 배열을 다루기 위한 데이터 구조입니다.\n* **.shape / .size()**: 텐서의 차원 형태(행과 열의 개수)를 나타냅니다.\n* **.reshape() / .view()**: 텐서의 모양(Dimension Shape)을 다르게 바꾸어 줍니다.\n* **from_numpy()**: NumPy 배열의 메모리를 공유하며 파이토치 텐서로 즉시 변환합니다.',
    review: 'NumPy와 PyTorch Tensor 간의 메모리 공유 메커니즘의 차이를 복습하세요.',
    preview: '자동 미분 기능인 Autograd(torch.autograd)의 원리를 예습하세요.'
  },
  'Data Preprocessing (데이터 전처리)': {
    keywords: ['StandardScaler', 'MinMaxScaler', 'MultiLabelBinarizer', 'SimpleImputer', 'dropna', 'log1p'],
    why: '결측치, 이상치가 많고 데이터 간 단위가 다른 현실 데이터를 정돈해 줍니다. 데이터의 품질이 낮으면 모델의 결과 또한 왜곡되기 때문에 머신러닝의 성공을 좌우하는 중요한 단계입니다.',
    meaning: '* **StandardScaler**: 데이터의 평균을 0, 표준편차를 1로 변환(표준화)합니다.\n* **MinMaxScaler**: 데이터를 최솟값 0, 최댓값 1 사이로 압축합니다.\n* **MultiLabelBinarizer**: 한 데이터에 속한 여러 범주형 값을 각각 독립된 이진(0/1) 형태의 열로 나누어 줍니다.\n* **log1p (로그 변환)**: 한쪽으로 치우친 데이터의 분포를 정규분포 형태로 변환하여 모델의 예측 정확도를 높입니다.',
    review: '정형 데이터를 다룰 때 로그 변환(log1p)을 쓰는 시점과 StandardScaler를 거쳐야 하는 알고리즘을 복습하세요.',
    preview: '데이터 누수(Data Leakage)를 방지하기 위한 `sklearn.pipeline.Pipeline` 사용법을 예습하세요.'
  },
  'Classification & Regression Models (머신러닝 모델링)': {
    keywords: ['LogisticRegression', 'DecisionTreeClassifier', 'RandomForestClassifier', 'GradientBoostingClassifier'],
    why: '입력 피처들 사이의 복잡한 패턴을 규칙이나 공식으로 학습하여 분류나 예측 성능을 내는 머신러닝의 핵심부입니다.',
    meaning: '* **LogisticRegression**: 특정 데이터가 특정 클래스에 속할 확률을 계산해 주는 이진 분류 기초 알고리즘입니다.\n* **DecisionTreeClassifier**: 조건 기반 질문 형태로 분할하며 직관적으로 패턴을 탐색하는 의사결정 모델입니다.\n* **RandomForestClassifier**: 수많은 의사결정 나무를 결합해 투표를 통해 일반화 성능을 올리는 배깅(Bagging) 기반 모델입니다.\n* **GradientBoostingClassifier**: 이전 트리 오차를 보강해 나가며 강한 학습 성능을 지니는 부스팅(Boosting) 기반 모델입니다.',
    review: '데이터 불균형 상태에서 머신러닝 평가 지표(Precision, Recall, F1-score)의 의미를 복습하세요.',
    preview: '현업 최다 활용 모델인 LightGBM, XGBoost, CatBoost의 성능적 우위 요인을 예습하세요.'
  },
  'Hyperparameter Tuning (하이퍼파라미터 튜닝)': {
    keywords: ['GridSearchCV', 'RandomizedSearchCV', 'cv='],
    why: '학습 모델에 수동으로 입력해 주는 설정값들을 컴퓨터 연산을 통해 정교하고 자동화된 알고리즘으로 조합을 찾아내기 위해 학습합니다.',
    meaning: '* **GridSearchCV**: 지정해 놓은 파라미터 후보군 조합 전체를 일일이 대입하여 검증하는 방식입니다.\n* **cv (Cross Validation)**: 과적합 방지를 위해 학습 데이터를 교차로 쪼개어 가며 일반화 성능을 입증하는 교차 검증입니다.',
    review: '하이퍼파라미터 튜닝 시 교차 검증 횟수를 늘릴 때 연산 코스트와의 트레이드오프를 확인하세요.',
    preview: '효율적 파라미터 조합 추정을 위해 가우시안 확률 추론 기반의 Optuna 라이브러리를 예습하세요.'
  }
};

// Substring helper to parse target codes
const CODE_EXPLANATIONS = [
  {
    key: 'torch.tensor',
    title: 'PyTorch 텐서 생성 코드',
    why: '딥러닝 모델이 대규모 행렬 계산을 빠르게 수행하려면 모든 데이터를 PyTorch 전용 자료형인 텐서(Tensor)로 가공해야 합니다. 파이썬 기본 리스트나 NumPy 배열은 GPU 가속 및 자동 미분을 지원하지 않기 때문에 모든 딥러닝 구현의 첫 단추로써 이 코드를 배웁니다.',
    what: '`torch.tensor(list_01)`은 파이썬 리스트인 `list_01`을 입력받아 GPU 가속 연산과 자동 미분이 가능한 다차원 행렬(Tensor) 데이터 구조로 새로 생성합니다.'
  },
  {
    key: 'MultiLabelBinarizer',
    title: '다중 범주형 데이터 원-핫 인코딩',
    why: '하나의 데이터가 여러 장르(예: Fiction, Romance)를 동시 가질 때 기존 라벨 인코딩으로는 학습이 불가능합니다. 이를 컴퓨터가 인지 가능한 이진화 데이터(0 또는 1의 여러 열)로 변환해 다중 속성 패턴을 온전히 가르치기 위해 배웁니다.',
    what: '`MultiLabelBinarizer()` 객체를 생성해 학습용 다중 분류 리스트 데이터에 적용하여, 각각의 고유값을 개별 컬럼으로 펼치고 해당 여부에 따라 1과 0으로 마스킹합니다.'
  },
  {
    key: 'GridSearchCV',
    title: '하이퍼파라미터 조합 탐색 & 교차 검증',
    why: '머신러닝 성능을 극대화하기 위해 조정해야 하는 설정값(하이퍼파라미터) 조합이 너무 많습니다. 수동으로 하나씩 대입해 볼 필요 없이 가능한 최적의 매개변수를 컴퓨터가 루프를 돌며 과학적으로 검증하고 찾도록 하기 위해 배웁니다.',
    what: '`GridSearchCV(model, param_grid, cv=3)`은 정의된 하이퍼파라미터 그리드의 모든 경우의 수 조합을 대입하고, 데이터를 3분할(cv=3)하여 교차 검증한 뒤 최적의 모델 설정을 자동으로 찾아줍니다.'
  },
  {
    key: 'StandardScaler',
    title: 'StandardScaler 수치 데이터 표준화',
    why: '페이지 수(단위 1000)와 평점(단위 0.1)처럼 피처들 간의 수치 스케일 차이가 클 경우, 거리 계산이나 경사하강법 학습 시 단위가 큰 피처에만 모델이 휘둘릴 수 있습니다. 모든 수치 데이터의 단위를 공평하게 맞춰주기 위해 배웁니다.',
    what: '`StandardScaler()` 객체를 생성하여 `fit_transform()`을 통해 컬럼의 데이터 평균을 0, 분산을 1로 맞춘 정규 분포 형태로 평탄화시킵니다.'
  },
  {
    key: 'RandomForestClassifier',
    title: 'Random Forest 앙상블 분류기 생성',
    why: '하나의 결정 트리(Decision Tree)는 훈련 데이터에 너무 민감해서 쉽게 과적합(Overfitting)됩니다. 수십~수백 개의 서로 다른 트리를 만들어 집단 지성(투표)으로 최종 판정을 내려 신뢰성과 예측력을 극대화하는 방법을 학습합니다.',
    what: '`RandomForestClassifier()` 객체는 백그라운드에서 임의로 학습 셋을 조율해 다수의 결정 나무들을 자동으로 설계하고 학습하여 상호 협력 판정이 가능하게 준비합니다.'
  },
  {
    key: 'log1p',
    title: '로그 스케일링 변환 (np.log1p)',
    why: '현실 데이터는 평점 수나 조회수처럼 소수의 데이터에만 엄청나게 큰 값이 몰려 있는 비대칭 분포가 흔합니다. 데이터의 극단적 간격을 로그 스케일로 압축하여 정규 분포에 가깝게 펴주어야 머신러닝의 예측 능력이 극대화되기 때문에 배웁니다.',
    what: '`np.log1p(x)` 함수는 입력 데이터에 자연로그 `log(x+1)` 연산을 가해 왜도를 낮춥니다. 이때 0이 대입되어 로그 연산 에러가 나는 것을 방지하기 위해 자동으로 1을 더해 안정적으로 변환합니다.'
  },
  {
    key: 'LogisticRegression',
    title: '로지스틱 회귀 모델 생성',
    why: '선형 방정식의 단순 출력은 0보다 작거나 1보다 큰 등 무한대 범위입니다. 이를 이진 분류 확률(0%~100%)로 매끄럽게 사상해 주는 시그모이드 함수의 매커니즘과 기초 선형 분류 모델의 수학적 뼈대를 학습하기 위해 배웁니다.',
    what: '`LogisticRegression()`은 입력 데이터를 선형 결합한 뒤 시그모이드 함수를 취해 결과가 클래스 1(참)에 해당할 사후 확률을 얻어 이진 분류를 학습합니다.'
  },
  {
    key: 'DecisionTreeClassifier',
    title: '의사결정 트리 모델 생성',
    why: '인공지능이 데이터를 어떠한 논리 규칙(스무고개 형태)으로 분류하는지에 대한 화이트박스(설명 가능한 AI) 모델의 뼈대를 이해하고 불순도(지니 계수 등)의 개념을 학습하기 위해 배웁니다.',
    what: '`DecisionTreeClassifier()`는 데이터 피처들을 순차 검사하여 엔트로피나 불순도를 가장 많이 낮추는(정보 획득량이 큰) 축을 기준 삼아 이진 트리 형태로 모델을 훈련시킵니다.'
  },
  {
    key: 'GradientBoostingClassifier',
    title: '그라디언트 부스팅 머신 생성',
    why: '정형 데이터 예측에서 가장 성능이 우수한 알고리즘의 원조 모델입니다. 단순히 개별 결과를 취합하는 랜덤 포레스트와 다르게, 이전 모델의 실수(오차 잔차)를 다음 모델이 보완해 나가는 부스팅 앙상블의 흐름을 다루기 위해 배웁니다.',
    what: '`GradientBoostingClassifier(n_estimators=10)`은 지정된 트리들이 이전 단계 오차(경사하강 잔차)를 가중 학습하는 순차 앙상블 구조로 설계되어 판별을 진행합니다.'
  },
  {
    key: 'get_update_weights_value',
    title: '경사하강법 가중치 업데이트 함수 (get_update_weights_value)',
    why: '딥러닝 프레임워크가 내부적으로 수행하는 오차 역전파(Backpropagation)와 경사하강법(Gradient Descent)의 수학적 원리를 직접 코드로 구현하여 이해하기 위해 배웁니다. 가중치(w)와 편향(b)의 미분계수를 공식에 대입해 수동으로 값을 갱신하는 방식을 체득하게 됩니다.',
    what: '선형 방정식 예측 가격과 실제 가격의 잔차 오차(`diff = target - predicted`)를 구하고, 이를 이용해 가중치 업데이트 속도(`w1_update`, `w2_update`, `bias_update`)와 평균제곱오차(`mse_loss = torch.mean(diff**2)`)를 계산하여 반환합니다.'
  },
  {
    key: 'gradient_descent',
    title: '경사하강법 루프 및 가중치 업데이트 구현 (gradient_descent)',
    why: '가중치가 최적의 오차 최소점에 도달할 때까지 여러 에포크(Epoch)에 걸쳐 가중치와 편향을 반복 수정하는 학습 루프(Training Loop)의 흐름을 파악하기 위해 학습합니다.',
    what: '가중치 w1, w2를 0으로, 편향 bias를 1로 텐서 초기화한 후, 2000 에포크 동안 `get_update_weights_value` 함수가 계산한 오차 기울기만큼 기존 가중치를 오차가 줄어드는 기울기 반대 방향(`w1 = w1 - w1_update`)으로 이동시킵니다.'
  },
  {
    key: 'scaled_features_ts',
    title: 'MinMaxScaler 피처 스케일링 & PyTorch 변환',
    why: '주택 데이터 피처인 방 개수(RM)와 하위계층 비율(LSTAT)의 데이터 척도가 다르므로 경사하강법 학습 시 편향 학습이 되는 것을 방지하기 위해 사용합니다. 모든 피처를 0과 1 사이로 압축한 뒤 파이토치 행렬 연산이 가능한 Tensor 형식으로 넘파이 배열을 호환 연계하기 위해 학습합니다.',
    what: 'Scikit-learn의 `MinMaxScaler`를 통해 피처 데이터를 정규화한 후, `torch.from_numpy(scaled_features_np)`를 사용해 메모리 복사 없이 즉시 파이토치 Tensor 형식으로 연계하여 경사하강법 함수로 대입합니다.'
  }
];

/**
 * Parses date from string file name (e.g. "6월 17일") or falls back to system dates
 */
function getStudyDate(file) {
  const match = file.name.match(/(\d+)월\s*(\d+)일/);
  if (match) {
    return `${parseInt(match[1])}월 ${parseInt(match[2])}일`;
  }
  
  // Fallback to modified time
  const dateObj = new Date(file.modifiedTime || file.createdTime);
  const m = dateObj.getMonth() + 1;
  const d = dateObj.getDate();
  return `${m}월 ${d}일`;
}

/**
 * Sorts date strings like "6월 17일", "6월 8일" correctly (descending)
 */
function sortDates(a, b) {
  const parse = str => {
    const m = str.match(/(\d+)월\s*(\d+)일/);
    if (!m) return 0;
    return parseInt(m[1]) * 100 + parseInt(m[2]);
  };
  return parse(b) - parse(a);
}

/**
 * Parses and summarizes Google Docs content
 */
function summarizeDocContent(fileName, text) {
  const lines = text.split('\n').map(l => l.trim()).filter(l => l !== '');
  const isPlanner = fileName.match(/\d+월\s*\d+일/) || text.includes('DAILY AFFIRMATION') || text.includes('PRIORITIES') || text.includes('TO DO LIST');
  
  if (isPlanner) {
    let affirmation = '';
    let priorities = [];
    let todosDone = [];
    let todosPending = [];
    let schedule = [];
    let currentSection = '';

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const upperLine = line.toUpperCase();

      if (upperLine.includes('DAILY AFFIRMATION')) {
        currentSection = 'AFFIRMATION';
        continue;
      } else if (upperLine.includes('TOP THREE PRIORITIES')) {
        currentSection = 'PRIORITIES';
        continue;
      } else if (upperLine.includes('TO DO LIST') || upperLine.includes('TO_DO_LIST')) {
        currentSection = 'TODO';
        continue;
      } else if (upperLine.includes('SCHEDULE')) {
        currentSection = 'SCHEDULE';
        continue;
      }

      if (currentSection === 'AFFIRMATION') {
        if (line.match(/^\d+:(00|30)/) || line.includes('PRIORITIES') || line.includes('TODO')) {
          currentSection = '';
        } else {
          affirmation = line;
          currentSection = '';
        }
      } else if (currentSection === 'PRIORITIES') {
        if (line.match(/^[123]\.\s*(.*)/)) {
          priorities.push(line);
        } else if (priorities.length < 3 && !line.includes('TO DO LIST') && !line.includes('SCHEDULE') && !line.includes('tasks')) {
          priorities.push(line);
        }
      } else if (currentSection === 'TODO') {
        if (line.startsWith('*') || line.startsWith('-') || line.match(/^[a-zA-Z가-힣]/)) {
          if (line.toLowerCase().includes('true')) {
            const task = line.replace(/true/i, '').replace(/^[*-\s]+/, '').trim();
            if (task && task !== 'tasks' && task !== 'soon' && task !== 'later') todosDone.push(task);
          } else if (line.toLowerCase().includes('false')) {
            const task = line.replace(/false/i, '').replace(/^[*-\s]+/, '').trim();
            if (task && task !== 'tasks' && task !== 'soon' && task !== 'later') todosPending.push(task);
          }
        }
      } else if (currentSection === 'SCHEDULE' || line.match(/^\d+:(00|30)\s*(am|pm)/i) || line.match(/^\d+시/)) {
        if (line.match(/^\d+:(00|30)\s*(am|pm)/i)) {
          const time = line;
          if (i + 1 < lines.length && !lines[i+1].includes('am') && !lines[i+1].includes('pm') && !lines[i+1].includes('PRIORITIES')) {
            const scheduleText = lines[i+1].trim();
            if (scheduleText && scheduleText !== 'Schedule' && scheduleText.length > 1) {
              schedule.push(`  * **${time}**: ${scheduleText}`);
            }
            i++;
          }
        } else if (line.match(/^\d+시/) || line.match(/^\d+\s*(am|pm)/i)) {
          schedule.push(`  * ${line}`);
        }
      }
    }

    let summary = `> 📅 **일일 계획서 요약 (Daily Planner Summary)**\n`;
    if (affirmation) summary += `* **오늘의 다짐**: *"${affirmation}"*\n`;
    if (priorities.length > 0) {
      summary += `* **오늘의 최우선 과제 (Top 3)**:\n`;
      priorities.forEach(p => {
        summary += `  * ${p}\n`;
      });
    }
    if (todosDone.length > 0) {
      summary += `* **완료한 항목 (Completed)**: \` ${todosDone.join(' \`  \` ')} \`\n`;
    }
    if (todosPending.length > 0) {
      summary += `* **남은 할 일 (Pending)**: ${todosPending.map(t => `**${t}**`).join(', ')}\n`;
    }
    if (schedule.length > 0) {
      summary += `* **오늘의 주요 타임라인**:\n${schedule.join('\n')}\n`;
    }
    return summary;
  } else {
    const bulletLines = lines.filter(l => l.startsWith('*') || l.startsWith('-') || l.match(/^\d+\./) || l.includes('공부') || l.includes('학습') || l.includes('중요') || l.includes('시험') || l.includes('설치') || l.includes('설명'));
    
    let summary = `> 📖 **학습 요약 문서 분석 (Lecture Notes Summary)**\n`;
    if (bulletLines.length > 0) {
      summary += `* **핵심 배울 점 및 요약 (Key Takeaways)**:\n`;
      bulletLines.slice(0, 8).forEach(bl => {
        summary += `  * ${bl}\n`;
      });
      if (bulletLines.length > 8) {
        summary += `  * *(이하 중요 핵심 내용 생략 - 드라이브 문서 링크 참고)*\n`;
      }
    } else {
      summary += `* **주요 내용 요약**:\n`;
      lines.slice(0, 6).forEach(l => {
        summary += `  * ${l}\n`;
      });
      if (lines.length > 6) {
        summary += `  * *(이하 본문 내용 생략 - 드라이브 문서 링크 참고)*\n`;
      }
    }
    return summary;
  }
}

/**
 * Generates a dynamic 2-line summary for a study day based on docs and notebooks
 */
function getDailyTwoLineSummary(group) {
  let line1 = '';
  let line2 = '';

  const noteSummaries = [];
  group.docs.forEach(doc => {
    const lines = doc.content.split('\n').map(l => l.trim()).filter(Boolean);
    const bulletLines = lines.filter(l => l.startsWith('*') || l.startsWith('-') || l.match(/^\d+\./) || l.includes('공부') || l.includes('학습') || l.includes('중요'));
    if (bulletLines.length > 0) {
      noteSummaries.push(bulletLines[0].replace(/^[*-\d.]\s*/, '').trim());
    } else if (lines.length > 0) {
      noteSummaries.push(lines[0]);
    }
  });

  if (noteSummaries.length > 0) {
    line1 = `오늘 학습 요약: **${noteSummaries[0]}** 주제를 심층 정리했습니다.`;
  } else {
    line1 = '오늘 배운 핵심 개념과 요약 메모를 문서로 정리했습니다.';
  }

  const techTopics = [];
  group.notebooks.forEach(nb => {
    if (nb.topics.length > 0) {
      nb.topics.forEach(t => {
        if (!techTopics.includes(t)) techTopics.push(t);
      });
    }
  });

  if (techTopics.length > 0) {
    line2 = `실습 코드로 **${techTopics.join(', ')}**의 핵심 모듈을 구현하고 훈련했습니다.`;
  } else if (group.notebooks.length > 0) {
    line2 = '실습 코드로 기초 파이썬 및 탐색적 데이터 분석(EDA) 실습을 성공적으로 수행했습니다.';
  } else {
    line2 = '진행된 라이브러리 연계 실습 및 PyTorch 딥러닝 코드 실습 내역이 없습니다.';
  }

  return `1. ${line1}\n2. ${line2}`;
}

async function run() {
  const cutoffDate = new Date();
  cutoffDate.setHours(18, 0, 0, 0);
  const isoTodayStart = new Date(cutoffDate.getTime() - 48 * 60 * 60 * 1000).toISOString();
  console.log(`최근 이틀(기준 18시, 48시간 전) 동안 생성/수정된 구글 드라이브 파일만 수집합니다 (기준 시각: ${isoTodayStart})`);
  console.log('구글 드라이브 소스코드(.ipynb) 및 요약문서(Google Docs) 수집 중...');
  
  let files = [];
  try {
    const [notebooksRes, docsRes] = await Promise.all([
      drive.files.list({
        q: `name contains '.ipynb' and modifiedTime >= '${isoTodayStart}' and trashed = false`,
        fields: 'files(id, name, mimeType, webViewLink, createdTime, modifiedTime)',
        pageSize: 40
      }),
      drive.files.list({
        q: `mimeType = 'application/vnd.google-apps.document' and modifiedTime >= '${isoTodayStart}' and trashed = false`,
        fields: 'files(id, name, mimeType, webViewLink, createdTime, modifiedTime)',
        pageSize: 40
      })
    ]);
    files = (notebooksRes.data.files || []).concat(docsRes.data.files || []);
  } catch (err) {
    console.error('✗ 구글 드라이브 검색 실패:', err.message);
    return;
  }

  console.log(`구글 드라이브에서 총 ${files.length}개의 파일(노트북 + 구글문서)을 발견했습니다.`);
  
  // We will group analysis results by study date
  const dateGroups = {};

  const promises = files.map(async (file) => {
    const dateKey = getStudyDate(file);
    if (!dateGroups[dateKey]) {
      dateGroups[dateKey] = {
        date: dateKey,
        notebooks: [],
        docs: []
      };
    }

    console.log(`분석 중: "${file.name}" (${dateKey})`);

    // Handle Google Docs
    if (file.mimeType === 'application/vnd.google-apps.document') {
      try {
        const exportRes = await drive.files.export({
          fileId: file.id,
          mimeType: 'text/plain'
        });
        
        let textContent = exportRes.data || '';
        // Clean up excessive newlines
        textContent = textContent.replace(/\r\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();

        // Skip daily planners (Docs with date names or containing planner headers)
        const isPlanner = file.name.match(/\d+월\s*\d+일/) || 
                          textContent.includes('DAILY AFFIRMATION') || 
                          textContent.includes('PRIORITIES') || 
                          textContent.includes('TO DO LIST');
        
        if (isPlanner) {
          console.log(`  스킵 (일일 계획서): "${file.name}"`);
          return;
        }

        dateGroups[dateKey].docs.push({
          name: file.name,
          link: file.webViewLink,
          content: textContent
        });
      } catch (e) {
        console.log(`  ⚠ Google Doc "${file.name}" 내보내기 실패:`, e.message);
      }
    }
    // Handle Jupyter/Colab Notebooks
    else {
      try {
        const getRes = await drive.files.get({
          fileId: file.id,
          alt: 'media'
        }, {
          responseType: 'json'
        });

        const notebookJson = getRes.data;
        const codeCells = [];
        const markdownCells = [];
        const cellsWithOutput = [];
        let sectionStructure = []; // [{heading, codeSummary, outputs}]
        let currentHeading = '(서두)';
        let currentCodes = [];
        let currentOutputs = [];

        if (notebookJson.cells) {
          notebookJson.cells.forEach(cell => {
            const rawSource = Array.isArray(cell.source) ? cell.source.join('') : (cell.source || '');

            if (cell.cell_type === 'markdown') {
              // Check if this markdown cell is a heading → new section
              const headingMatch = rawSource.match(/^#{1,3}\s+(.+)/m);
              if (headingMatch) {
                // Save previous section
                if (currentCodes.length > 0 || currentOutputs.length > 0) {
                  sectionStructure.push({
                    heading: currentHeading,
                    codes: [...currentCodes],
                    outputs: [...currentOutputs]
                  });
                }
                currentHeading = headingMatch[1].trim();
                currentCodes = [];
                currentOutputs = [];
              }
              markdownCells.push(rawSource);

            } else if (cell.cell_type === 'code' && rawSource.trim()) {
              codeCells.push(rawSource);
              currentCodes.push(rawSource);

              // Parse outputs
              const outputs = cell.outputs || [];
              const outputTexts = [];
              outputs.forEach(out => {
                if (out.output_type === 'stream') {
                  const txt = Array.isArray(out.text) ? out.text.join('') : (out.text || '');
                  if (txt.trim()) outputTexts.push(txt.trim().split('\n').slice(0, 5).join('\n'));
                } else if (out.output_type === 'execute_result' || out.output_type === 'display_data') {
                  const data = out.data || {};
                  const txt = Array.isArray(data['text/plain']) ? data['text/plain'].join('') : (data['text/plain'] || '');
                  if (txt.trim()) outputTexts.push(txt.trim().split('\n').slice(0, 5).join('\n'));
                } else if (out.output_type === 'error') {
                  outputTexts.push(`[오류] ${out.ename}: ${out.evalue}`);
                }
              });
              if (outputTexts.length > 0) {
                currentOutputs.push({ code: rawSource, output: outputTexts.join('\n---\n') });
                cellsWithOutput.push({ code: rawSource, output: outputTexts.join('\n---\n') });
              }
            }
          });

          // Save last section
          if (currentCodes.length > 0 || currentOutputs.length > 0) {
            sectionStructure.push({
              heading: currentHeading,
              codes: [...currentCodes],
              outputs: [...currentOutputs]
            });
          }
        }

        const totalCells = (notebookJson.cells || []).length;
        const fileTopics = [];
        const codeTextCombined = codeCells.join('\n');

        // Detect topics
        Object.keys(TOPICS).forEach(topic => {
          const match = TOPICS[topic].keywords.some(kw => codeTextCombined.includes(kw));
          if (match) fileTopics.push(topic);
        });

        // Extract known key code snippets
        const codeSnippets = [];
        const usedKeys = new Set();
        CODE_EXPLANATIONS.forEach(expl => {
          const matchingCell = codeCells.find(cell => cell.includes(expl.key));
          if (matchingCell) {
            usedKeys.add(expl.key);
            const lines = matchingCell.split('\n').filter(line => line.trim() !== '');
            const formattedCode = lines.map(line => {
              if (line.includes(expl.key)) return `**${line}**  # <-- 중요 코드`;
              return line;
            }).slice(0, 8).join('\n');
            codeSnippets.push({ title: expl.title, code: formattedCode, why: expl.why, what: expl.what, isKnown: true });
          }
        });

        // Also extract up to 3 additional notable code cells not covered by CODE_EXPLANATIONS
        const unknownCells = codeCells.filter(cell =>
          cell.trim().length > 30 &&
          !CODE_EXPLANATIONS.some(e => cell.includes(e.key))
        );
        unknownCells.slice(0, 3).forEach((cell, idx) => {
          const lines = cell.split('\n').filter(l => l.trim());
          const firstMeaningfulLine = lines.find(l => !l.startsWith('#') && l.trim()) || lines[0] || '';
          codeSnippets.push({
            title: `기타 실습 코드 ${idx + 1}: \`${firstMeaningfulLine.slice(0, 60)}\``,
            code: lines.slice(0, 10).join('\n'),
            why: null,
            what: null,
            isKnown: false
          });
        });

        dateGroups[dateKey].notebooks.push({
          name: file.name,
          link: file.webViewLink,
          topics: fileTopics,
          codeSnippets: codeSnippets,
          markdownCells: markdownCells,
          cellsWithOutput: cellsWithOutput,
          sectionStructure: sectionStructure,
          stats: {
            total: totalCells,
            code: codeCells.length,
            markdown: markdownCells.length,
            withOutput: cellsWithOutput.length
          }
        });
      } catch (e) {
        console.log(`  ⚠ 노트북 "${file.name}" 분석 실패:`, e.message);
      }
    }
  });

  await Promise.all(promises);
  // Generate date-grouped flat markdown report with collapsible topics
  let mdReport = `# 📚 김지우님의 일자별 인공지능 학습 현황 포트폴리오 보고서\n`;
  mdReport += `*최종 동기화 시간: ${new Date().toLocaleString()}*\n\n`;
  mdReport += `> 구글 드라이브에 저장된 실습용 코랩 노트북(.ipynb)과 학습 요약 문서(Google Docs)를 날짜별로 매핑하여 접기(Toggle) 형태로 정리했습니다.\n\n`;

  // Sort dates descending
  const sortedDates = Object.keys(dateGroups).sort(sortDates);
  const globalTopics = new Set();

  sortedDates.forEach(dateStr => {
    const group = dateGroups[dateStr];
    
    // Skip empty dates (though they shouldn't exist)
    if (group.notebooks.length === 0 && group.docs.length === 0) return;

    mdReport += `## 📅 ${dateStr} 학습 및 복습 내역\n\n`;
    
    // Write 2-line important summary first
    mdReport += `### 🌟 일일 핵심 요약 (중요 내용 2줄 정리)\n`;
    mdReport += `${getDailyTwoLineSummary(group)}\n\n`;
    mdReport += `---\n\n`;

    // Write Google Docs section (Daily planners, reviews, notes)
    if (group.docs.length > 0) {
      group.docs.forEach(doc => {
        mdReport += `<details>\n`;
        mdReport += `<summary>📝 학습 요약 문서: ${doc.name}</summary>\n\n`;
        mdReport += `#### 📎 [문서 링크](${doc.link})\n`;
        mdReport += `${summarizeDocContent(doc.name, doc.content)}\n\n`;
        mdReport += `</details>\n\n`;
      });
    }

    // Write Notebooks section
    if (group.notebooks.length > 0) {
      group.notebooks.forEach(nb => {
        mdReport += `<details>\n`;
        mdReport += `<summary>💻 실습 소스코드: ${nb.name}</summary>\n\n`;
        mdReport += `#### 📎 [노트북 링크](${nb.link})\n`;

        // Cell stats
        if (nb.stats) {
          mdReport += `> 📊 **노트북 구성**: 전체 ${nb.stats.total}셀 (코드 ${nb.stats.code}셀 · 설명 ${nb.stats.markdown}셀 · 실행 출력 있음 ${nb.stats.withOutput}셀)\n\n`;
        }

        if (nb.topics.length > 0) {
          mdReport += `* **감지된 학습 영역**: ${nb.topics.join(', ')}\n`;
          nb.topics.forEach(t => globalTopics.add(t));
        } else {
          mdReport += `* **감지된 학습 영역**: 기초 파이썬 및 탐색적 데이터 분석(EDA)\n`;
        }

        // Section structure from markdown headings
        if (nb.sectionStructure && nb.sectionStructure.length > 0) {
          mdReport += `\n##### 📑 노트북 섹션별 구성 요약:\n`;
          nb.sectionStructure.forEach(sec => {
            mdReport += `\n<details>\n<summary>📌 섹션: ${sec.heading}</summary>\n\n`;

            // Show first code in section
            if (sec.codes.length > 0) {
              const firstCode = sec.codes[0].split('\n').filter(l => l.trim()).slice(0, 10).join('\n');
              mdReport += `**대표 코드 (${sec.codes.length}개 코드셀 중 첫 번째)**:\n`;
              mdReport += `\`\`\`python\n${firstCode}\n\`\`\`\n`;
            }

            // Show outputs for this section
            if (sec.outputs.length > 0) {
              mdReport += `**실행 결과 (출력 있는 ${sec.outputs.length}개 셀)**:\n`;
              sec.outputs.slice(0, 2).forEach((o, i) => {
                const outLines = o.output.split('\n').slice(0, 6);
                mdReport += `\`\`\`\n${outLines.join('\n')}\n\`\`\`\n`;
              });
            }

            mdReport += `</details>\n`;
          });
          mdReport += `\n`;
        }

        // Write known code snippets with explanations
        const knownSnippets = nb.codeSnippets.filter(s => s.isKnown);
        const unknownSnippets = nb.codeSnippets.filter(s => !s.isKnown);

        if (knownSnippets.length > 0) {
          mdReport += `\n##### 💡 핵심 개념 코드 발췌 & 심층 설명:\n`;
          knownSnippets.forEach(snippet => {
            mdReport += `\n**🔑 ${snippet.title}**\n`;
            mdReport += `* **왜 이 코드를 배울까요?**\n  > ${snippet.why}\n`;
            mdReport += `* **이 코드는 무엇을 할까요?**\n  > ${snippet.what}\n`;
            mdReport += `\`\`\`python\n${snippet.code}\n\`\`\`\n`;
          });
        }

        if (unknownSnippets.length > 0) {
          mdReport += `\n##### 🔍 기타 실습 코드 발췌 (추가 분석):\n`;
          unknownSnippets.forEach(snippet => {
            mdReport += `\n**${snippet.title}**\n`;
            mdReport += `\`\`\`python\n${snippet.code}\n\`\`\`\n`;
          });
        }

        // Show markdown notes from the notebook
        const meaningfulMarkdowns = (nb.markdownCells || []).filter(md =>
          md.trim().length > 20 && !md.match(/^#{1,3}\s/) // exclude pure headings already shown in sections
        );
        if (meaningfulMarkdowns.length > 0) {
          mdReport += `\n##### 📝 노트북 내 설명 메모 (Markdown 셀):\n`;
          meaningfulMarkdowns.slice(0, 4).forEach(md => {
            const cleanMd = md.trim().split('\n').slice(0, 5).join('\n');
            mdReport += `> ${cleanMd.replace(/\n/g, '\n> ')}\n\n`;
          });
        }

        mdReport += `</details>\n\n`;
      });
    }
    
    mdReport += `\n---\n\n`;
  });

  // Write global learning guide at the end
  mdReport += `## 🧠 종합 핵심 개념 정리 (Scanned Concepts Deep Dive)\n`;
  if (globalTopics.size === 0) {
    mdReport += `* 감지된 머신러닝/파이토치 모듈이 없습니다.\n`;
  } else {
    globalTopics.forEach(topic => {
      mdReport += `### 🎯 ${topic}\n`;
      mdReport += `#### 💡 이 기술을 왜 학습해야 할까요?\n`;
      mdReport += `${TOPICS[topic].why}\n\n`;
      mdReport += `#### 🔍 각 부분의 핵심 개념과 뜻\n`;
      mdReport += `${TOPICS[topic].meaning}\n\n`;
      mdReport += `#### 🔄 추천 복습 (Review)\n`;
      mdReport += `* ${TOPICS[topic].review}\n\n`;
      mdReport += `#### 🚀 추천 예습 (Preview)\n`;
      mdReport += `* ${TOPICS[topic].preview}\n\n`;
      mdReport += `---\n\n`;
    });
  }

  try {
    fs.writeFileSync(reportFile, mdReport, 'utf-8');
    console.log(`성공! 바탕화면에 일자별 보고서가 생성되었습니다.`);
    console.log(`경로: ${reportFile}`);
  } catch (err) {
    console.error('바탕화면 보고서 생성 실패:', err.message);
  }
}

run();
