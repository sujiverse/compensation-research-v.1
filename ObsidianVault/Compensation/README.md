# 🧠 보상작용 연구 자동화 시스템

> **OpenAlex API 기반 자동 논문 크롤링 & 5WHY 분석**
> 🤖 **10분마다 자동 실행** | 📊 **실시간 연구 데이터** | 🌐 **GitHub Pages 공개**

[![Auto Research](https://github.com/[YOUR_USERNAME]/[YOUR_REPO]/actions/workflows/auto-research.yml/badge.svg)](https://github.com/[YOUR_USERNAME]/[YOUR_REPO]/actions/workflows/auto-research.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-green)](https://[YOUR_USERNAME].github.io/[YOUR_REPO])

## 🎯 **기능**

### 🔄 **자동 크롤링 (10분마다)**
- OpenAlex API에서 보상작용 관련 논문 수집
- 신뢰도 점수 자동 계산 (venue/level/citations/recency)
- 근육간 보상 패턴 자동 학습
- Obsidian 노드 자동 생성

### 🧠 **5WHY 분석**
- 각 논문마다 5단계 원인 분석 템플릿
- 보상작용 → 근본 원인 추적
- 임상 적용 가이드라인

### 🎯 **크로스체크 시스템**
- MMT (Manual Muscle Testing)
- Movement 스크린 (기능적 움직임)
- ROM (Range of Motion) 테스트
- Special Tests (특수 검사)

### 📊 **실시간 웹사이트**
- GitHub Pages로 자동 퍼블리시
- 실시간 연구 현황 확인
- 논문 링크 및 요약 제공

## 🚀 **사용법**

### **1. 웹사이트에서 확인**
```
https://[YOUR_USERNAME].github.io/[YOUR_REPO]
```

### **2. Obsidian에서 열기**
1. 이 저장소를 클론 또는 다운로드
2. Obsidian에서 "Open folder as vault"
3. 다운로드한 폴더 선택
4. `보상작용.md`에서 시작

### **3. 로컬에서 실행**
```bash
# 의존성 설치
pip install requests unidecode

# 단발성 실행
python compensation_crawler_bot.py

# 자동 갱신 모드
export AUTO_LOOP_HOURS=1
python compensation_crawler_bot.py
```

## 📁 **폴더 구조**

```
📦 보상작용 연구 자동화
├── 📄 보상작용.md                    # 허브 노드
├── 📄 5WHY-보상작용-템플릿.md         # 5WHY 분석 템플릿
├── 📄 보상작용-규칙(자동).md          # 자동 학습 규칙
├── 📄 rules.json                     # 원시 규칙 데이터
├── 📄 compensation_crawler_bot.py    # 메인 크롤러 봇
├── 📁 papers/                        # 논문 노드들
│   ├── 📄 gluteus-medius-weakness-...-.md
│   ├── 📄 serratus-anterior-dysfunction-...-.md
│   └── 📄 ...
├── 📁 logs/                          # 실행 로그
├── 📁 .github/workflows/             # GitHub Actions
├── 📁 .obsidian/                     # Obsidian 설정
└── 📄 README.md                      # 이 파일
```

## ⚙️ **자동화 설정**

### **GitHub Actions 워크플로우**
- **실행 주기**: 10분마다 (`*/10 * * * *`)
- **트리거**: Push, 수동 실행, 스케줄
- **기능**: 크롤링 → 분석 → 커밋 → 배포

### **자동 생성되는 콘텐츠**
1. **논문 노드**: 메타데이터 + 초록 + 5WHY + 크로스체크
2. **규칙 학습**: 근육간 보상 패턴 자동 추출
3. **실행 로그**: 매 실행마다 상태 기록
4. **웹사이트**: GitHub Pages 자동 업데이트

## 🔧 **설정**

### **환경 변수**
```yaml
AUTO_LOOP_HOURS: 1        # 자동 갱신 간격 (시간)
QUERY: "compensation biomechanics rehabilitation"  # 검색 쿼리
LIMIT: 80                 # 논문 수 제한
SINCE: 2010              # 시작 연도
```

### **신뢰도 점수 기준**
- **Venue** (18점): journal > conference > repository
- **Level** (24점): meta-analysis > systematic review > RCT
- **Citations** (25점): √(인용수/1000) × 25
- **Recency** (10점): ≤5년(10) > ≤10년(7) > 기타(4)

## 📊 **현재 상태**

- 🔄 **자동 실행**: ✅ 활성화 (10분마다)
- 📄 **논문 수**: [실시간 확인](./papers/)
- 🧠 **학습 규칙**: [규칙 보기](./보상작용-규칙(자동).md)
- 📝 **마지막 실행**: [로그 확인](./logs/latest.md)

## 🛠️ **개발자 정보**

### **기술 스택**
- **언어**: Python 3.11+
- **API**: OpenAlex Research API
- **자동화**: GitHub Actions
- **배포**: GitHub Pages
- **문서**: Obsidian Markdown

### **주요 라이브러리**
- `requests`: HTTP 요청
- `unidecode`: 유니코드 정규화
- `pathlib`: 파일 경로 처리
- `json`: 데이터 직렬화

## 📝 **라이선스**

MIT License - 자유롭게 사용, 수정, 배포 가능

## 🤝 **기여**

1. Fork this repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

**🤖 이 저장소는 GitHub Actions로 10분마다 자동 업데이트됩니다.**

*마지막 업데이트: [자동 생성됨]*