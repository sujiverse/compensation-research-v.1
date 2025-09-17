# 보상작용 자동 크롤러 & 분석 봇

OpenAlex API를 통해 보상작용 관련 논문을 자동 수집하고, 5WHY 분석 + 크로스체크 가이드가 포함된 Obsidian 볼트를 생성합니다.

## 🚀 빠른 시작

```bash
# 패키지 설치
pip install requests unidecode

# 단발성 실행
python compensation_crawler.py

# 자동 갱신 모드 (6시간마다)
export AUTO_LOOP_HOURS=6
python compensation_crawler.py
```

## 📁 출력 구조

```
ObsidianVault/Compensation/
├── papers/                     # 논문별 노드 (80개)
├── 보상작용.md                # 허브 노드
├── 5WHY-보상작용-템플릿.md    # 5WHY 템플릿
├── 보상작용-규칙(자동).md     # 자동 학습된 규칙 요약
├── rules.json                  # 원시 규칙 데이터
├── changelog.md                # 규칙 변경 히스토리
├── logs/                       # 실행 로그
└── rules_history/              # 규칙 백업
```

## 🔧 주요 기능

### 1. 자동 데이터 수집
- OpenAlex API를 통한 논문 크롤링
- 신뢰도 기반 품질 필터링 (preprint 제외)
- 에러 처리 및 재시도 로직

### 2. 5WHY 분석 템플릿
각 논문마다 자동 생성:
1. 왜 이런 통증/제한이 발생했는가?
2. 왜 특정 근육이 약화되었는가?
3. 왜 근육 불균형이 생기는가?
4. 왜 보상작용이 일어나는가?
5. 왜 패턴이 고착화되는가?

### 3. 자동 규칙 학습
- 논문에서 근육간 보상 패턴 자동 추출
- 약화근 → 보상근 관계 학습
- 빈도와 균형성 기반 점수화

### 4. 크로스체크 가이드
추정된 약화근별 맞춤형 검사:
- **MMT**: 수동근력검사
- **Movement**: 기능적 움직임 스크린
- **ROM**: 관절가동범위
- **Special Tests**: 특수검사

### 5. 변경 추적 시스템
- 규칙 변화 자동 감지
- 백업 및 히스토리 관리
- 상세한 변경 로그

### 6. 자가 갱신 루프
환경변수 `AUTO_LOOP_HOURS` 설정으로 주기적 자동 업데이트

## 📊 데이터 품질 관리

### 필터링 기준
- 최소 신뢰도 점수: 20점
- 제목 길이: 10자 이상
- 출판 유형: preprint 제외

### 신뢰도 점수 산정
- **Venue** (18점): journal > conference > repository
- **Level** (24점): meta-analysis > systematic review > RCT > general
- **Citations** (25점): √(인용수/1000) × 25
- **Recency** (10점): 5년 이내 > 10년 이내 > 그 외

## 🔄 워크플로우

1. **논문 수집** → OpenAlex API 쿼리
2. **품질 필터링** → 고품질 논문만 선별
3. **규칙 학습** → 근육간 보상 패턴 추출
4. **노드 생성** → Obsidian 마크다운 파일 생성
5. **변경 추적** → 이전 버전과 비교 분석
6. **백업** → 규칙 히스토리 저장

## 🛠️ 커스터마이징

코드 상단 설정 섹션에서 조정 가능:

```python
QUERY = "compensation biomechanics rehabilitation"  # 검색 쿼리
LIMIT = 80                                         # 논문 수
SINCE = 2010                                       # 시작 연도
AUTO_LOOP_HOURS = 0                               # 자동 갱신 간격
```

## 📝 사용 예시

### 기본 실행
```bash
python compensation_crawler.py
```

### 자동 갱신 모드
```bash
export AUTO_LOOP_HOURS=12
nohup python compensation_crawler.py &
```

### 로그 확인
```bash
tail -f ObsidianVault/Compensation/logs/crawler.log
```

## 🔍 출력 예시

### 논문 노드 구조
```markdown
---
title: "Gluteus medius weakness and compensation strategies"
year: 2020
trust_score: 45
...
---

## 초록
[논문 초록]

## 핵심
- [ ] 주요 주장
- [ ] 연구 방법
- [ ] 보상작용 관련 의미

## 5WHY 추적
1. 왜 이런 통증/제한이 발생했는가?
- 특정 근육 약화 → 다른 근육 과활성 (보상작용)
...

## 근육간 보상작용 (규칙기반 추정)
- 규칙 1: 약화(↓): gluteus medius → 보상(↑): tensor fasciae latae
  - 메모: G. med 약화 시 측부 골반 안정성 상실 → TFL 과활성

## 크로스체크
### 약화(↓) 추정: gluteus medius
- **MMT**: 옆으로 누워 고관절 외전 MMT(중둔근 분리)
- **Movement**: Trendelenburg 한발서기; Single-leg squat에서 동적 knee valgus 관찰
- **ROM**: 고관절 외전/내회전 가동성
- **Special Tests**: Trendelenburg sign
```

## 📈 고급 기능

### 변경 로그 추적
매 실행마다 규칙 변화를 자동 감지하고 `changelog.md`에 기록:
- 신규 규칙
- 점수 변경된 규칙
- 제거된 규칙

### 백업 시스템
`rules_history/` 폴더에 타임스탬프별 규칙 백업 자동 저장

### 진행률 표시
대량 논문 처리 시 10개 단위로 진행률 표시

이제 완전히 자동화된 보상작용 연구 지식베이스를 구축할 수 있습니다! 🎯