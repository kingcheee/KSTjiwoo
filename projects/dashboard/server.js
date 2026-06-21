const http = require('http');
const fs = require('fs');
const path = require('path');
const { google } = require('C:/Users/sxeyc/node_modules/googleapis');

const PORT = 3000;
const runDir = __dirname;
const CREDENTIALS_PATH = path.join(runDir, 'credentials.json');
const TOKEN_PATH = path.join(runDir, 'token.json');

// Initialize Google OAuth2 client
let oAuth2Client;
try {
  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf-8'));
  const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf-8'));
  const clientConfig = credentials.installed || credentials.web;
  oAuth2Client = new google.auth.OAuth2(
    clientConfig.client_id,
    clientConfig.client_secret,
    clientConfig.redirect_uris ? clientConfig.redirect_uris[0] : 'urn:ietf:wg:oauth:2.0:oob'
  );
  oAuth2Client.setCredentials(token);
} catch (err) {
  console.error('[ERROR] Failed to load Google credentials. Please run setup first.', err.message);
}

// Help format dates
const formatKoreanDate = (date) => {
  const month = date.getMonth() + 1;
  const day = date.getDate();
  return `${month}월 ${day}일`;
};

/**
 * Core business logic helper to fetch and compile all dashboard status data.
 */
async function getDashboardData(onProgress) {
  const sheets = google.sheets({ version: 'v4', auth: oAuth2Client });
  const calendar = google.calendar({ version: 'v3', auth: oAuth2Client });
  const tasks = google.tasks({ version: 'v1', auth: oAuth2Client });
  const drive = google.drive({ version: 'v3', auth: oAuth2Client });

  if (onProgress) onProgress({ percent: 10, message: '구글 API 연동 초기화 중...' });
  const todayStr = formatKoreanDate(new Date());

  const data = {
    today: todayStr,
    affirmation: '영양제 챙겨먹고 청결하게 생활하기!',
    priorities: [],
    tasks: [],
    habits: [],
    schedule: [],
    budget: {
      incomePlanned: 0,
      spendingLimit: 0,
      spendingActual: 0,
      spendingExceeded: 0,
      savingsPlanned: 0,
      warnings: []
    },
    recommendation: ''
  };

  // 1. Fetch Today's Planner Doc (for Affirmation, Priorities, Tasks, and Schedule)
  if (onProgress) onProgress({ percent: 25, message: '오늘의 플래너 문서(구글 Docs) 조회 및 파싱 중...' });
  try {
    const docList = await drive.files.list({
      q: `name = '${todayStr}' and mimeType = 'application/vnd.google-apps.document' and trashed = false`,
      fields: 'files(id, name)'
    });
    
    if (docList.data.files && docList.data.files.length > 0) {
      const docRes = await drive.files.export({
        fileId: docList.data.files[0].id,
        mimeType: 'text/plain'
      });
      const lines = docRes.data.split('\n').map(l => l.trim()).filter(l => l !== '');
      
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
            data.affirmation = line;
            currentSection = '';
          }
        } else if (currentSection === 'PRIORITIES') {
          if (line.match(/^[123]\.\s*(.*)/)) {
            data.priorities.push(line);
          } else if (data.priorities.length < 3 && !line.includes('TO DO LIST') && !line.includes('SCHEDULE')) {
            data.priorities.push(line);
          }
        } else if (currentSection === 'TODO') {
          if (line.startsWith('*') || line.startsWith('-') || line.match(/^[a-zA-Z가-힣]/)) {
            const completed = line.toLowerCase().includes('true');
            const taskTitle = line.replace(/true/i, '').replace(/false/i, '').replace(/^[*-\s]+/, '').trim();
            if (taskTitle && taskTitle !== 'tasks' && taskTitle !== 'soon' && taskTitle !== 'later') {
              const hasKorean = /[가-힣]/.test(taskTitle);
              if (hasKorean) {
                data.tasks.push({
                  id: taskTitle,
                  title: taskTitle,
                  completed: completed
                });
              }
            }
          }
        } else if (currentSection === 'SCHEDULE' || line.match(/^\d+:(00|30)\s*(am|pm)/i) || line.match(/^\d+시/)) {
          if (line.match(/^\d+:(00|30)\s*(am|pm)/i)) {
            const time = line;
            if (i + 1 < lines.length && !lines[i+1].includes('am') && !lines[i+1].includes('pm') && !lines[i+1].includes('PRIORITIES') && !lines[i+1].includes('TODO')) {
              data.schedule.push({
                id: time,
                summary: lines[i+1].trim(),
                time: time,
                description: ''
              });
              i++;
            }
          } else if (line.match(/^\d+시/) || line.match(/^\d+\s*(am|pm)/i)) {
            data.schedule.push({
              id: line,
              summary: line,
              time: '',
              description: ''
            });
          }
        }
      }
    }
  } catch (err) {
    console.error('Drive Doc Fetch Error:', err.message);
  }

  // Fallback priorities if empty
  if (data.priorities.length === 0) {
    data.priorities = ['바닥 청소하기', '다이소 정리하기', '파이토치 복습'];
  }

  if (onProgress) onProgress({ percent: 55, message: '가계부 예산 시트(구글 Sheets) 분석 중...' });
  // 2. Fetch Spreadsheet (Habits & Budget)
  try {
    // We search Drive for a Sheet titled '김지우 돈생'
    const sheetsList = await drive.files.list({
      q: "name = '김지우 돈생' and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false",
      fields: 'files(id)'
    });
    
    if (sheetsList.data.files && sheetsList.data.files.length > 0) {
      const spreadsheetId = sheetsList.data.files[0].id;
      data.spreadsheetId = spreadsheetId;


      // Get Monthly Budget Data from the 'Budget' sheet
      try {
        const budgetRes = await sheets.spreadsheets.values.get({
          spreadsheetId,
          range: 'Budget!A28:L50'
        });

        const bRows = budgetRes.data.values || [];
        let totalPlannedExpenses = 0;
        let totalActualExpenses = 0;
        
        bRows.forEach((row) => {
          // Parse Income
          const incItem = row[1] ? row[1].trim() : '';
          const incEst = row[2] ? parseFloat(row[2].replace(/[^0-9.-]/g, '')) || 0 : 0;
          const incAct = row[3] ? parseFloat(row[3].replace(/[^0-9.-]/g, '')) || 0 : 0;
          if (incItem && incItem !== 'DESCRIPTION' && incItem !== 'TOTAL') {
            data.budget.incomePlanned += incEst;
          }

          // Parse Fixed Expenses
          const fixedItem = row[5] ? row[5].trim() : '';
          const fixedEst = row[6] ? parseFloat(row[6].replace(/[^0-9.-]/g, '')) || 0 : 0;
          const fixedAct = row[7] ? parseFloat(row[7].replace(/[^0-9.-]/g, '')) || 0 : 0;
          if (fixedItem && fixedItem !== 'DESCRIPTION' && fixedItem !== 'TOTAL') {
            totalPlannedExpenses += fixedEst;
            totalActualExpenses += fixedAct;
            if (fixedAct > fixedEst) {
              data.budget.warnings.push(`[경고] 고정지출 "${fixedItem}" 예산(₩${fixedEst.toLocaleString()})을 ₩${(fixedAct - fixedEst).toLocaleString()} 초과하여 ₩${fixedAct.toLocaleString()}을 지출했습니다!`);
            }
          }

          // Parse Variable Expenses
          const varItem = row[9] ? row[9].trim() : '';
          const varEst = row[10] ? parseFloat(row[10].replace(/[^0-9.-]/g, '')) || 0 : 0;
          const varAct = row[11] ? parseFloat(row[11].replace(/[^0-9.-]/g, '')) || 0 : 0;
          if (varItem && varItem !== 'DESCRIPTION' && varItem !== 'TOTAL') {
            totalPlannedExpenses += varEst;
            totalActualExpenses += varAct;
            if (varAct > varEst) {
              data.budget.warnings.push(`[경고] 변동지출 "${varItem}" 예산(₩${varEst.toLocaleString()})을 ₩${(varAct - varEst).toLocaleString()} 초과하여 ₩${varAct.toLocaleString()}을 지출했습니다!`);
            }
          }
        });

        data.budget.spendingLimit = totalPlannedExpenses;
        data.budget.spendingActual = totalActualExpenses;
        data.budget.spendingExceeded = Math.max(0, totalActualExpenses - totalPlannedExpenses);
        data.budget.savingsPlanned = 1300000;
      } catch (err) {
        console.error('Budget Fetch Error:', err.message);
      }
    }
  } catch (err) {
    console.error('Sheets Global Error:', err.message);
  }


  if (onProgress) onProgress({ percent: 75, message: '저장된 AI 시간표 불러오는 중...' });
  // 4. Load Generated Schedule if exists
  const schedulePath = path.join(runDir, 'current_schedule.json');
  if (fs.existsSync(schedulePath)) {
    try {
      data.schedule = JSON.parse(fs.readFileSync(schedulePath, 'utf-8'));
    } catch (e) {
      data.schedule = [];
    }
  } else {
    data.schedule = [];
  }

  // 5. Build AI Recommendation (Module B & D)
  let rec = `반갑습니다 지우님! 오늘 학습 스케줄을 분석해 드립니다.\n`;
  const hasTensorStudy = data.tasks.some(t => t.title.toLowerCase().includes('tensor') || t.title.toLowerCase().includes('pytorch'));
  const hasCleanTask = data.priorities.some(p => p.includes('청소') || p.includes('정리'));
  
  if (hasCleanTask) {
    rec += `* 오늘 핵심 목표인 **'${data.priorities.find(p => p.includes('청소') || p.includes('정리'))}'** 일정이 감지되었습니다. 쾌적한 학습 환경을 위해 20분 내외로 우선 진행하세요.\n`;
  }
  
  if (data.schedule.length > 0) {
    const nextEvent = data.schedule[0];
    rec += `* 오늘 예정된 일정이 있습니다: **"${nextEvent.summary}"** (시작: ${nextEvent.time}). 일정 전에 예습 범위를 미리 체크하세요.\n`;
  } else {
    rec += `* 오늘 등록된 캘린더 일정이 없습니다. 여유 시간을 확보하여 드라이브의 **파이토치 딥러닝 실습(410_boston.ipynb)** 예습을 30분 동안 진행해 보세요!\n`;
  }

  if (data.budget.spendingExceeded > 0) {
    rec += `* ⚠️ **소비 통제 비상경보**: 장바구니 예산 초과 상태입니다. 목표 적금(₩1,300,000) 달성을 위해 당분간 외식 지출을 차단해 주세요!\n`;
  }

  data.recommendation = rec;
  if (onProgress) onProgress({ percent: 90, message: '광주 동구 서석동 실시간 날씨 데이터 조회 중...' });
  // 5. Fetch Gwangju weather on the server side (avoids CORS)
  let weather = '날씨 정보 없음';
  try {
    const https = require('https');
    weather = await new Promise((resolve, reject) => {
      const options = {
        headers: {
          'User-Agent': 'curl/7.64.1'
        }
      };
      https.get('https://wttr.in/Seoseok-dong,Gwangju?format=3', options, (res) => {
        let dataStr = '';
        res.on('data', chunk => { dataStr += chunk; });
        res.on('end', () => {
          const text = dataStr.trim();
          const info = text.includes(':') ? text.split(':')[1].trim() : text;
          resolve(info);
        });
      }).on('error', () => resolve('날씨 정보 없음'));
    });
  } catch (e) {
    // Ignore
  }
  data.weather = weather;
  if (onProgress) onProgress({ percent: 100, message: '로딩 완료!' });
  return data;
}

// HTTP Server setup
const server = http.createServer(async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  const parsedUrl = new URL(req.url, `http://${req.headers.host}`);

  // Route: Serve Web Page
  if (req.method === 'GET' && parsedUrl.pathname === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    const htmlPath = path.join(runDir, 'index.html');
    res.end(fs.readFileSync(htmlPath));
    return;
  }

  // Route: API Status Stream (SSE)
  if (req.method === 'GET' && parsedUrl.pathname === '/api/status-stream') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream; charset=utf-8',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*'
    });

    const sendEvent = (event, dataObj) => {
      res.write(`event: ${event}\ndata: ${JSON.stringify(dataObj)}\n\n`);
    };

    try {
      const data = await getDashboardData((progress) => {
        sendEvent('progress', progress);
      });
      sendEvent('complete', data);
      res.end();
    } catch (err) {
      sendEvent('error', { message: err.message });
      res.end();
    }
    return;
  }

  // Route: API Status Get
  if (req.method === 'GET' && parsedUrl.pathname === '/api/status') {
    try {
      const data = await getDashboardData();
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify(data));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // Route: Toggle Google Doc task status (True/False)
  if (req.method === 'POST' && parsedUrl.pathname === '/api/toggle-task') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const { taskId, completed } = JSON.parse(body); // taskId is the task title string
        
        const drive = google.drive({ version: 'v3', auth: oAuth2Client });
        const docs = google.docs({ version: 'v1', auth: oAuth2Client });
        const todayStr = formatKoreanDate(new Date());
        
        // Find today's document
        const docList = await drive.files.list({
          q: `name = '${todayStr}' and mimeType = 'application/vnd.google-apps.document' and trashed = false`,
          fields: 'files(id)'
        });
        
        if (docList.data.files && docList.data.files.length > 0) {
          const docId = docList.data.files[0].id;
          
          const oldText = `${taskId} ${completed ? 'False' : 'True'}`;
          const newText = `${taskId} ${completed ? 'True' : 'False'}`;
          
          await docs.documents.batchUpdate({
            documentId: docId,
            requestBody: {
              requests: [
                {
                  replaceAllText: {
                    containsText: {
                      text: oldText,
                      matchCase: false
                    },
                    replaceText: newText
                  }
                }
              ]
            }
          });
          console.log(`✓ Updated Google Doc: replaced "${oldText}" with "${newText}"`);
        }
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true }));
      } catch (err) {
        console.error('Failed to toggle task in Google Doc:', err.message);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }


  // Route: Delete Google Doc task line
  if (req.method === 'POST' && parsedUrl.pathname === '/api/delete-task') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const { taskId } = JSON.parse(body); // taskId is the task title string
        
        const drive = google.drive({ version: 'v3', auth: oAuth2Client });
        const docs = google.docs({ version: 'v1', auth: oAuth2Client });
        const todayStr = formatKoreanDate(new Date());
        
        // Find today's document
        const docList = await drive.files.list({
          q: `name = '${todayStr}' and mimeType = 'application/vnd.google-apps.document' and trashed = false`,
          fields: 'files(id)'
        });
        
        if (docList.data.files && docList.data.files.length > 0) {
          const docId = docList.data.files[0].id;
          
          const targets = [
            `* ${taskId} True`,
            `* ${taskId} False`,
            `- ${taskId} True`,
            `- ${taskId} False`,
            `${taskId} True`,
            `${taskId} False`
          ];
          
          const requests = targets.map(targetText => {
            return {
              replaceAllText: {
                containsText: {
                  text: targetText,
                  matchCase: false
                },
                replaceText: ''
              }
            };
          });
          
          await docs.documents.batchUpdate({
            documentId: docId,
            requestBody: {
              requests: requests
            }
          });
          console.log(`✓ Deleted task from Google Doc: "${taskId}"`);
        }
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true }));
      } catch (err) {
        console.error('Failed to delete task in Google Doc:', err.message);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }

  // Route: Generate custom schedule based on tasks
  if (req.method === 'POST' && parsedUrl.pathname === '/api/generate-schedule') {
    try {
      const data = await getDashboardData(); // Fetches fresh tasks and priorities
      
      const dayOfWeek = new Date().getDay();
      const isWeekday = dayOfWeek >= 1 && dayOfWeek <= 5;
      
      const aiSchedule = [];
      if (isWeekday) {
        aiSchedule.push({
          time: '09:00 - 18:00',
          summary: '🏫 인공지능사관학교 수업',
          description: '사관학교 정규 수업 진행 (집중 학습 시간)'
        });
      }

      // Filter active (unchecked) tasks containing Korean characters
      const activeTasks = data.tasks.filter(t => !t.completed);
      
      // Classify tasks
      const houseworkTasks = activeTasks.filter(t => 
        t.title.includes('청소') || t.title.includes('정리') || t.title.includes('빨래') || 
        t.title.includes('다이소') || t.title.includes('설거지') || t.title.includes('식단') || 
        t.title.includes('소분') || t.title.includes('욕실') || t.title.includes('주방')
      );
      
      const studyTasks = activeTasks.filter(t => 
        t.title.includes('수업') || t.title.includes('복습') || t.title.includes('공부') || 
        t.title.includes('학습') || t.title.includes('프로젝트') || t.title.includes('시스템') || 
        t.title.includes('파이토치') || t.title.includes('텐서') || t.title.includes('예습') ||
        t.title.includes('데이터')
      );

      const otherTasks = activeTasks.filter(t => 
        !houseworkTasks.includes(t) && !studyTasks.includes(t)
      );

      // 1. Post-class learning / Daewon's class
      const daewonClass = studyTasks.find(t => t.title.includes('대원'));
      if (daewonClass) {
        aiSchedule.push({
          time: '18:00 - 19:00',
          summary: `📚 ${daewonClass.title}`,
          description: '수업 참석 및 강의 복습 진행'
        });
      } else {
        aiSchedule.push({
          time: '18:00 - 19:00',
          summary: '📚 일일 예습 및 복습 시간',
          description: '사관학교 당일 핵심 내용 복습'
        });
      }

      // 2. Dinner & Rest
      aiSchedule.push({
        time: '19:00 - 20:00',
        summary: '🍽️ 저녁 식사 및 자유 시간',
        description: '식사 및 리그 오브 레전드 게임 휴식 추천'
      });

      // 3. Housework slot
      const hwNames = houseworkTasks.map(t => t.title).join(', ');
      aiSchedule.push({
        time: '20:00 - 21:00',
        summary: '🧹 오늘의 집안일 해결',
        description: hwNames ? `진행 업무: ${hwNames}` : '방 정리정돈 및 간단한 청소 완료하기'
      });

      // 4. Study/Projects slot
      const studyNames = studyTasks.filter(t => !t.title.includes('대원')).map(t => t.title).concat(otherTasks.map(t => t.title)).join(', ');
      aiSchedule.push({
        time: '21:00 - 22:30',
        summary: '💻 개인 AI 개발 프로젝트 및 학습',
        description: studyNames ? `진행 업무: ${studyNames}` : '개인 딥러닝 실습(410_boston.ipynb) 예습 및 코딩 공부'
      });

      // 5. Wrap-up
      aiSchedule.push({
        time: '22:30 - 23:00',
        summary: '📝 하루 회고 및 취침 전 정리',
        description: '오늘의 다짐 준수 여부 체크 및 내일 플래너 작성하기'
      });

      aiSchedule.push({
        time: '23:00 ~',
        summary: '💤 취침 준비',
        description: '수면 패턴 유지 (밤 11시/11시 반 취침 취소)'
      });

      // Save generated schedule locally
      fs.writeFileSync(path.join(runDir, 'current_schedule.json'), JSON.stringify(aiSchedule, null, 2), 'utf-8');

      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true }));
    } catch (err) {
      console.error('Failed to generate schedule:', err.message);
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }
  res.writeHead(404);
  res.end();
});

server.listen(PORT, () => {
  console.log(`================================================================`);
  console.log(`Jiwoo's Personal AI Assistant Server running at http://localhost:${PORT}`);
  console.log(`================================================================`);
});
