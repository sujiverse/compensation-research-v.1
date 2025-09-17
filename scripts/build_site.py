# -*- coding: utf-8 -*-
import os, re, json, datetime, requests
from pathlib import Path

DOCS = Path("docs")
VAULT = Path("ObsidianVault/Compensation")   # 옵시디언 볼트 경로(있으면 그래프 만듦)
DOCS.mkdir(parents=True, exist_ok=True)
(DOCS/"papers").mkdir(parents=True, exist_ok=True)

API = "https://api.openalex.org/works"
QUERY = {
    "search": "compensation muscle weakness biomechanics rehabilitation",
    "per_page": 10,
    "sort": "cited_by_count:desc",
}

def fetch_papers():
    r = requests.get(API, params=QUERY, headers={"User-Agent":"simple-bot/0.1"})
    r.raise_for_status()
    return r.json().get("results", [])

def line_of(w):
    title = (w.get("display_name") or "Untitled").strip()
    year  = w.get("publication_year") or ""
    doi   = (w.get("doi") or "").replace("https://doi.org/","")
    url   = f"https://doi.org/{doi}" if doi else (w.get("primary_location",{}) or {}).get("landing_page_url","")
    return f"- **{title}** ({year}) → [{('DOI' if doi else 'link')}]({url})"

LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

def scan_vault_graph():
    nodes, edges = {}, []
    if not VAULT.exists():
        return {"nodes": [], "links": []}
    for p in VAULT.rglob("*.md"):
        nid = str(p.relative_to(VAULT)).replace("\\","/")
        nodes.setdefault(nid, {"id": nid})
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except:
            continue
        for tgt in LINK_RE.findall(txt):
            cand = tgt if tgt.endswith(".md") else tgt + ".md"
            local = p.parent / cand
            target = None
            if local.exists():
                target = str(local.relative_to(VAULT)).replace("\\","/")
            else:
                hits = list(VAULT.rglob(cand))
                if hits:
                    target = str(hits[0].relative_to(VAULT)).replace("\\","/")
            if target:
                nodes.setdefault(target, {"id": target})
                edges.append({"source": nid, "target": target})
    return {"nodes": list(nodes.values()), "links": edges}

def write_index(papers):
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    md = [
        "# 보상작용 위키 (심플)",
        f"- 마지막 업데이트: **{now}**",
        "",
        "## 최신 논문",
    ] + [line_of(w) for w in papers] + [
        "",
        "## 노드 그래프",
        "- 그래프 보기: [graph.html](graph.html)",
        "",
        "## 논문 목록 (파일)",
        "- 목록: [papers/](papers/)",
    ]
    (DOCS/"index.md").write_text("\n".join(md), encoding="utf-8")

def write_graph_assets(graph):
    (DOCS/"graph.json").write_text(json.dumps(graph, ensure_ascii=False), encoding="utf-8")
    (DOCS/"graph.html").write_text("""
<!doctype html><meta charset="utf-8"><title>Graph</title>
<style>body{font:14px/1.4 system-ui,sans-serif;margin:0}#g{width:100vw;height:100vh}.n{stroke:#999;stroke-width:.5}.c{fill:#444}
a{position:fixed;left:12px;top:10px;text-decoration:none}</style>
<a href="index.html">← back</a><svg id="g"></svg>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script>
fetch("graph.json").then(r=>r.json()).then(({nodes,links})=>{
  const svg=d3.select("#g"), W=innerWidth, H=innerHeight; svg.attr("width",W).attr("height",H);
  const sim=d3.forceSimulation(nodes).force("link", d3.forceLink(links).id(d=>d.id).distance(60))
    .force("charge", d3.forceManyBody().strength(-120)).force("center", d3.forceCenter(W/2,H/2));
  const link=svg.append("g").selectAll("line").data(links).enter().append("line").attr("class","n");
  const node=svg.append("g").selectAll("g").data(nodes).enter().append("g").call(d3.drag()
    .on("start",(e,d)=>{if(!e.active)sim.alphaTarget(.3).restart();d.fx=d.x;d.fy=d.y;})
    .on("drag",(e,d)=>{d.fx=e.x;d.fy=e.y;})
    .on("end",(e,d)=>{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null;}));
  node.append("circle").attr("r",4).attr("class","c");
  node.append("title").text(d=>d.id);
  sim.on("tick",()=>{ link.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y)
    .attr("x2",d=>d.target.x).attr("y2",d=>d.target.y); node.attr("transform",d=>`translate(${d.x},${d.y})`); });
});
</script>
""", encoding="utf-8")

def main():
    try:
        papers = fetch_papers()
    except Exception:
        papers = []
    write_index(papers)                # ← /docs/index.md 생성 (404 해결 핵심)
    write_graph_assets(scan_vault_graph())

if __name__ == "__main__":
    main()