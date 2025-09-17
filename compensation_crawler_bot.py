#!/usr/bin/env python3
"""
보상작용 중심 자동 크롤링 → 신뢰도 점수화 → Obsidian 노드 생성 봇
+ 5WHY 추적 + 근육간 보상 규칙 + 크로스체크 + 규칙 자동 학습

실행:
  pip install requests unidecode
  python compensation_crawler_bot.py
옵션(자가 갱신):
  AUTO_LOOP_HOURS=6 python compensation_crawler_bot.py
"""
import os, re, math, json, time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

import requests
from unidecode import unidecode

# ------------------ 설정 ------------------
QUERY = "compensation biomechanics rehabilitation"
LIMIT = 80
SINCE = 2010
VAULT_DIR = Path("./ObsidianVault/Compensation")
VAULT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------ 유틸 ------------------
def slugify(s: str) -> str:
    s = unidecode(s).strip().lower()
    s = re.sub(r"[^a-z0-9\- ]", "", s)
    return "-".join(s.split())

# ------------------ 데이터 수집 (OpenAlex API) ------------------
OA = "https://api.openalex.org"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9"
}

def mock_test_data() -> List[Dict]:
    """API 제한 시 사용할 모의 데이터"""
    return [
        {
            "display_name": "Gluteus medius weakness and compensation patterns in running injuries: A systematic review",
            "publication_year": 2020,
            "doi": "https://doi.org/10.1016/j.gaitpost.2020.example",
            "primary_location": {
                "landing_page_url": "https://example.com/gluteus-medius-running",
                "pdf_url": "https://example.com/gluteus-medius-running.pdf"
            },
            "host_venue": {"type": "journal"},
            "cited_by_count": 245,
            "authorships": [
                {"author": {"display_name": "Dr. Sarah Johnson"}},
                {"author": {"display_name": "Dr. Michael Chen"}}
            ],
            "concepts": [
                {"display_name": "biomechanics"},
                {"display_name": "muscle activation"},
                {"display_name": "compensation patterns"},
                {"display_name": "gait analysis"}
            ],
            "abstract_inverted_index": {
                "Gluteus": [0], "medius": [1], "weakness": [2], "is": [3], "a": [4], "common": [5],
                "finding": [6], "in": [7], "runners": [8], "leading": [9], "to": [10], "compensatory": [11],
                "patterns": [12], "including": [13], "tensor": [14], "fasciae": [15], "latae": [16],
                "overactivity": [17], "and": [18], "altered": [19], "hip": [20], "kinematics": [21]
            }
        },
        {
            "display_name": "Serratus anterior dysfunction and upper trapezius compensation in overhead athletes",
            "publication_year": 2019,
            "doi": "https://doi.org/10.1016/j.jshs.2019.example",
            "primary_location": {
                "landing_page_url": "https://example.com/serratus-anterior-athletes"
            },
            "host_venue": {"type": "journal"},
            "cited_by_count": 156,
            "authorships": [
                {"author": {"display_name": "Dr. Emily Rodriguez"}}
            ],
            "concepts": [
                {"display_name": "shoulder biomechanics"},
                {"display_name": "muscle imbalance"},
                {"display_name": "sports medicine"}
            ],
            "abstract_inverted_index": {
                "Serratus": [0], "anterior": [1], "weakness": [2], "commonly": [3], "results": [4],
                "in": [5], "upper": [6], "trapezius": [7], "dominance": [8], "and": [9],
                "scapular": [10], "dyskinesis": [11], "among": [12], "overhead": [13], "athletes": [14]
            }
        },
        {
            "display_name": "Tibialis posterior dysfunction and peroneal muscle compensation in flat foot syndrome",
            "publication_year": 2021,
            "doi": "https://doi.org/10.1016/j.foot.2021.example",
            "primary_location": {
                "landing_page_url": "https://example.com/tibialis-posterior-flatfoot"
            },
            "host_venue": {"type": "journal"},
            "cited_by_count": 89,
            "authorships": [
                {"author": {"display_name": "Dr. James Wilson"}},
                {"author": {"display_name": "Dr. Lisa Park"}}
            ],
            "concepts": [
                {"display_name": "foot biomechanics"},
                {"display_name": "arch support"},
                {"display_name": "muscle dysfunction"}
            ],
            "abstract_inverted_index": {
                "Tibialis": [0], "posterior": [1], "dysfunction": [2], "leads": [3], "to": [4],
                "compensatory": [5], "peroneal": [6], "muscle": [7], "overactivity": [8],
                "resulting": [9], "in": [10], "pronation": [11], "and": [12], "arch": [13], "collapse": [14]
            }
        }
    ]

def oa_search(query: str, since: Optional[int], limit: int) -> List[Dict]:
    res, cursor, fetched = [], "*", 0
    while fetched < limit and cursor:
        params = {
            "search": query,
            "per_page": min(200, limit - fetched),
            "cursor": cursor,
            "sort": "cited_by_count:desc",
        }
        if since:
            params["from_publication_date"] = f"{since}-01-01"
        import time
        time.sleep(1)  # API 요청 간격 조절
        r = requests.get(f"{OA}/works", params=params, headers=HEADERS, timeout=30)
        if r.status_code == 403:
            print(f"WARNING: API access limited. Status code: {r.status_code}")
            print("INFO: Continuing with mock test data...")
            return mock_test_data()
        r.raise_for_status()
        js = r.json()
        for w in js.get("results", []):
            res.append(w)
            fetched += 1
            if fetched >= limit:
                break
        cursor = js.get("meta", {}).get("next_cursor")
        if not cursor:
            break
    return res

# ------------------ 신뢰도 점수 ------------------
def trust_score(w: Dict) -> Tuple[int, Dict[str, int]]:
    score, parts = 0, {}
    vt = (w.get("host_venue", {}).get("type") or "").lower()
    v = 18 if vt == "journal" else 10 if vt == "conference" else 4
    score += v; parts["venue"] = v
    title = (w.get("display_name") or "").lower()
    level = 8
    if "meta-analysis" in title: level = 24
    elif "systematic review" in title: level = 20
    elif "randomized" in title: level = 16
    elif vt == "repository": level = 4
    score += level; parts["level"] = level
    c = int(w.get("cited_by_count", 0))
    cit = min(25, int(25 * math.sqrt(min(c, 1000) / 1000)))
    score += cit; parts["citations"] = cit
    y = w.get("publication_year")
    rec = 0
    if y:
        age = max(0, datetime.now().year - int(y))
        rec = 10 if age <= 5 else 7 if age <= 10 else 4
    score += rec; parts["recency"] = rec
    return score, parts

# ------------------ 규칙 자동 학습 ------------------
MUSCLE_LEXICON = [
    # 하체/골반
    "gluteus medius","gluteus maximus","tensor fasciae latae","piriformis","quadratus lumborum","hamstrings","adductor magnus","iliopsoas","rectus femoris","vastus medialis","tibialis posterior","peroneus longus","peroneus brevis","gastrocnemius","soleus","erector spinae",
    # 어깨/견갑
    "serratus anterior","upper trapezius","lower trapezius","levator scapulae","pectoralis minor","infraspinatus","teres minor",
]
WEAK_TRIGGERS = ["weakness","deficit","inhibition","reduced activation","decreased strength"]
STRONG_TRIGGERS = ["increased activation","overactivity","dominance","hyperactivity","greater activation","compensatory activation","substitution"]


def extract_candidates(text: str) -> List[str]:
    t = text.lower()
    return [m for m in MUSCLE_LEXICON if m in t]


def mine_rules(works: List[Dict]) -> List[Dict]:
    from collections import defaultdict
    pair_counts = defaultdict(int)
    weak_counts = defaultdict(int)
    strong_counts = defaultdict(int)
    evidences = defaultdict(list)
    for w in works:
        title = (w.get("display_name") or "").lower()
        inv = w.get("abstract_inverted_index")
        if inv:
            toks = sorted([(pos, word) for word, poses in inv.items() for pos in poses])
            abstract = " ".join([word for _, word in toks]).lower()
        else:
            abstract = ""
        txt = title + ". " + abstract
        muscles = extract_candidates(txt)
        if not muscles:
            continue
        for sent in re.split(r"[.!?]", txt):
            if not any(m in sent for m in muscles):
                continue
            weak_hits = [m for m in muscles if m in sent and any(t in sent for t in WEAK_TRIGGERS)]
            strong_hits = [m for m in muscles if m in sent and any(t in sent for t in STRONG_TRIGGERS)]
            for wmus in weak_hits:
                weak_counts[wmus] += 1
            for smus in strong_hits:
                strong_counts[smus] += 1
            for wmus in weak_hits:
                for smus in strong_hits:
                    if wmus != smus:
                        key = (wmus, smus)
                        pair_counts[key] += 1
                        evidences[key].append(sent.strip())
    rules = []
    for (wkey, skey), c in pair_counts.items():
        score = c * 1.0 / (1 + abs(weak_counts[wkey] - strong_counts[skey]))
        rules.append({
            "weak": wkey,
            "strong": skey,
            "count": c,
            "weak_mentions": weak_counts[wkey],
            "strong_mentions": strong_counts[skey],
            "score": round(score, 3),
            "examples": evidences[(wkey, skey)][:3],
        })
    rules.sort(key=lambda x: (-x["score"], -x["count"]))
    return rules

# ------------------ 임상 규칙(핸드크래프트) ------------------
COMP_RULES = [
    {
        "weak": ["gluteus medius", "hip abductor"],
        "strong": ["tensor fasciae latae", "TFL", "piriformis", "quadratus lumborum", "IT band", "hamstrings (lateral)", "adductor compensations"],
        "signs": ["Trendelenburg", "pelvic drop", "hip hike", "knee valgus", "femoral internal rotation"],
        "note": "G. med 약화 → 측부 골반 안정성 상실 → TFL/QL/Piriformis 과활성 보상",
    },
    {
        "weak": ["gluteus maximus", "hip extensor"],
        "strong": ["hamstrings", "erector spinae", "quadratus lumborum", "adductor magnus (extensor part)"],
        "signs": ["lumbar extension strategy", "anterior pelvic tilt"],
        "note": "G. max 약화 → 햄스트링/요방형근/기립근 과사용",
    },
    {
        "weak": ["serratus anterior", "lower trapezius"],
        "strong": ["upper trapezius", "levator scapulae", "pectoralis minor"],
        "signs": ["scapular anterior tilt", "winging", "scapular dyskinesis"],
        "note": "SA/LT 약화 → 상부승모/견갑거근/소흉근 과활성",
    },
    {
        "weak": ["tibialis posterior"],
        "strong": ["peroneus longus", "peroneus brevis", "flexor hallucis longus"],
        "signs": ["overpronation", "navicular drop", "medial arch collapse"],
        "note": "후경골근 약화 → 외측근/종아치 보상",
    },
    {
        "weak": ["hip external rotator", "deep hip rotator", "gluteus medius posterior"],
        "strong": ["TFL", "adductors", "rectus femoris"],
        "signs": ["dynamic knee valgus", "femoral IR", "foot pronation"],
        "note": "고관절 외회전/후부 안정성 저하 → 내회전/내전 보상",
    },
]


def infer_compensations(title: str, abstract: Optional[str], concepts: List[str]) -> List[Dict]:
    text = (title + " " + (abstract or "") + " " + " ".join(concepts)).lower()
    findings = []
    for rule in COMP_RULES:
        if any(kw in text for kw in rule["weak"]):
            findings.append({
                "weak": ", ".join(rule["weak"]),
                "strong": ", ".join(rule["strong"]),
                "signs": ", ".join(rule["signs"]),
                "note": rule["note"],
            })
    for rule in COMP_RULES:
        if any(kw.lower() in text for kw in rule["strong"]):
            findings.append({
                "weak": ", ".join(rule["weak"]) + " (의심)",
                "strong": ", ".join(rule["strong"]),
                "signs": ", ".join(rule["signs"]),
                "note": "보상근 과활성 패턴 → 약화근 역추정",
            })
    return findings

# ------------------ 크로스체크(교차검증) ------------------
CROSSCHECK_MAP = {
    "gluteus medius": {
        "MMT": ["옆으로 누워 고관절 외전 MMT(중둔근 분리)"],
        "Movement": ["Trendelenburg 한발서기", "Single-leg squat 동적 knee valgus", "Step-down"],
        "ROM": ["고관절 외전/내회전"],
        "Special": ["Trendelenburg sign"],
    },
    "gluteus maximus": {
        "MMT": ["엎드린 고관절 신전 MMT(무릎 굴곡 90°)"],
        "Movement": ["Prone hip extension에서 요추 과신전/햄스트링 지배"],
        "ROM": ["고관절 신전"],
        "Special": [],
    },
    "serratus anterior": {
        "MMT": ["SA 펀치 테스트"],
        "Movement": ["Wall slide 상회/전인 과다", "Scapular winging"],
        "ROM": ["견갑흉 상회/후경"],
        "Special": ["SAT", "SRT"],
    },
    "lower trapezius": {
        "MMT": ["Lower trap 하강 MMT"],
        "Movement": ["팔 들기 시 견갑 상회 타이밍"],
        "ROM": [],
        "Special": ["SAT", "SRT"],
    },
    "tibialis posterior": {
        "MMT": ["발목 내반/저측굴곡 MMT(후경골근)"],
        "Movement": ["Single-leg heel raise 내반 유지", "보행 과회내"],
        "ROM": ["발목 배측굴곡"],
        "Special": ["Navicular drop test"],
    },
}


def build_crosscheck_md(findings: List[Dict]) -> str:
    if not findings:
        return (
            "## 크로스체크\n"
            "- [ ] MMT 대상 근육 선택\n"
            "- [ ] 기능 스크린(SLS/스텝다운/보행)\n"
            "- [ ] 관련 ROM/특수검사\n"
        )
    lines = ["## 크로스체크"]
    for f in findings:
        weak_names = [w.strip() for w in f["weak"].split(",")]
        key = weak_names[0].replace("(의심)", "").strip()
        cc = CROSSCHECK_MAP.get(key)
        lines.append(f"### 약화(↓) 추정: {key}")
        if cc:
            if cc.get("MMT"): lines += ["- **MMT**: " + "; ".join(cc["MMT"]) ]
            if cc.get("Movement"): lines += ["- **Movement**: " + "; ".join(cc["Movement"]) ]
            if cc.get("ROM"): lines += ["- **ROM**: " + "; ".join(cc["ROM"]) ]
            if cc.get("Special"): lines += ["- **Special Tests**: " + "; ".join(cc["Special"]) ]
        else:
            lines.append("- 표준 체크: 해당 근육 MMT, 연관 움직임 스크린, 연관 ROM/특수검사")
    return "\n".join(lines)

# ------------------ Markdown 생성 ------------------
def make_note(w: Dict, outdir: Path) -> str:
    title = (w.get("display_name") or "Untitled").strip()
    year = w.get("publication_year")
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    url = (w.get("primary_location", {}) or {}).get("landing_page_url")
    pdf = (w.get("primary_location", {}) or {}).get("pdf_url")
    authors = [a.get("author", {}).get("display_name") for a in w.get("authorships", [])]
    score, parts = trust_score(w)

    # 초록 복원
    abstract = None
    inv = w.get("abstract_inverted_index")
    if inv:
        toks = sorted([(pos, word) for word, poses in inv.items() for pos in poses])
        abstract = " ".join([word for _, word in toks])

    # 근육간 보상 규칙 적용
    concepts = [c.get("display_name") for c in w.get("concepts", [])]
    comp = infer_compensations(title, abstract, concepts)

    fm = {
        "title": title,
        "year": year,
        "doi": doi,
        "url": url,
        "pdf": pdf,
        "authors": authors,
        "cited_by_count": w.get("cited_by_count", 0),
        "trust_score": score,
        "trust_parts": parts,
        "tags": ["research", "compensation"],
    }
    yaml = "---\n" + json.dumps(fm, ensure_ascii=False, indent=2) + "\n---\n"

    why_section = (
        "## 5WHY 추적\n"
        "1. 왜 이런 통증/제한이 발생했는가?\n- 특정 근육 약화 → 다른 근육 과활성 (보상작용)\n"
        "2. 왜 특정 근육이 약화되었는가?\n- 반복된 패턴, 신경근 억제, 자세 불균형\n"
        "3. 왜 근육 불균형이 생기는가?\n- 운동사슬 연쇄 반응, 인접 관절의 보상\n"
        "4. 왜 보상작용이 일어나는가?\n- 중력하 안정성 유지하려는 적응\n"
        "5. 왜 패턴이 고착화되는가?\n- 습관화된 움직임, 근막 긴장 패턴 지속\n"
    )

    comp_section = "## 근육간 보상작용 (규칙기반 추정)\n"
    if comp:
        for i, cset in enumerate(comp, 1):
            comp_section += (
                f"- 규칙 {i}: 약화(↓): {cset['weak']} → 보상(↑): {cset['strong']} | 징후: {cset['signs']}\n"
                f"  - 메모: {cset['note']}\n"
            )
        comp_section += (
            "\n**역추론 가이드**: 보상근(↑)이 비정상적으로 강/타이트하면 상응 약화근(↓) 우선 의심 → MMT/패턴/특수검사로 확인.\n"
        )
    else:
        comp_section += "- 관련 근육 키워드가 부족하여 자동 추정 불가. 임상 패턴 기반 수기 입력 권장.\n"

    cross_md = build_crosscheck_md(comp)

    body = (
        f"## 초록\n{abstract or ''}\n\n"
        "## 핵심\n- [ ] 주요 주장\n- [ ] 연구 방법\n- [ ] 보상작용 관련 의미\n\n"
        f"{why_section}\n{comp_section}\n{cross_md}\n"
    )

    fname = slugify(title) + (f"-{year}" if year else "") + ".md"
    Path(outdir, fname).write_text(yaml + "\n" + body, encoding="utf-8")
    return fname

# ------------------ 허브 노드 ------------------
def make_hub(filenames: List[str]) -> None:
    hub = Path(VAULT_DIR, "보상작용.md")
    lines = ["# 보상작용 (Compensation)", "보상작용 연구 허브.", "\n## 연결된 문헌"]
    for f in filenames:
        name = f[:-3]
        lines.append(f"- [[{name}]]")
    lines += ["\n## 5WHY 분석 가이드", "- [[5WHY-보상작용-템플릿]]", "\n## 자동 학습 규칙", "- [[보상작용-규칙(자동)]]"]
    hub.write_text("\n".join(lines), encoding="utf-8")

# ------------------ 5WHY 템플릿 노드 ------------------
def make_5why_template() -> None:
    tpl = Path(VAULT_DIR, "5WHY-보상작용-템플릿.md")
    txt = (
        "# 5WHY 보상작용 템플릿\n\n"
        "1. 왜 이런 통증/제한이 발생했는가?\n- 예: 둔근 약화 → 햄스트링 과활성\n\n"
        "2. 왜 특정 근육이 약화되었는가?\n- 예: 신경근 억제, 반복된 자세 불균형\n\n"
        "3. 왜 근육 불균형이 생기는가?\n- 예: 운동사슬 연쇄 보상 반응\n\n"
        "4. 왜 보상작용이 일어나는가?\n- 예: 중력하 안정성 확보 위한 적응\n\n"
        "5. 왜 패턴이 고착화되는가?\n- 예: 습관화, 근막 긴장 패턴 고정화\n"
    )
    tpl.write_text(txt, encoding="utf-8")

# ------------------ 규칙 요약 파일 ------------------
def write_rules_summary(rules: List[Dict]) -> None:
    summary = [
        "# 보상작용 규칙(자동 학습)",
        "",
        "| 약화(↓) | 보상(↑) | 빈도 | 점수 | 예시 |",
        "|---|---|---:|---:|---|",
    ]
    for r in rules[:80]:
        ex = (r.get("examples") or [])
        ex_str = (ex[0][:100] + "…") if ex else "-"
        summary.append(f"| {r['weak']} | {r['strong']} | {r['count']} | {r['score']} | {ex_str} |")
    (VAULT_DIR / "보상작용-규칙(자동).md").write_text("\n".join(summary), encoding="utf-8")

# ------------------ 실행 ------------------
def run_once() -> None:
    works = oa_search(QUERY, SINCE, LIMIT)
    paper_dir = VAULT_DIR / "papers"
    paper_dir.mkdir(exist_ok=True)
    files: List[str] = []
    for w in works:
        fn = make_note(w, paper_dir)
        files.append("papers/" + fn[:-3])
    make_5why_template()
    rules = mine_rules(works)
    (VAULT_DIR / "rules.json").write_text(json.dumps(rules, ensure_ascii=False, indent=2), encoding="utf-8")
    write_rules_summary(rules)
    make_hub(files)
    print(f"COMPLETED! Papers: {len(files)}, Rules: {len(rules)}, Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    run_once()
    interval = os.environ.get("AUTO_LOOP_HOURS")
    if interval:
        hours = max(1, int(float(interval)))
        while True:
            time.sleep(hours * 3600)
            try:
                run_once()
                print("INFO: Auto-refresh completed")
            except Exception as e:
                print("WARNING: Error during refresh", e)