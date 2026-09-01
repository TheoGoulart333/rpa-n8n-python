"""Generate a static health dashboard for a GitHub repository."""

from __future__ import annotations

import argparse
import html
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / "docs" / "index.html"


def github_get(path: str) -> Any:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "repo-health-dashboard", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.getenv("GITHUB_TOKEN", "")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com{path}", headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def demo_data() -> dict[str, Any]:
    return {
        "repository": {"full_name": "TheoGoulart333/rpa-n8n-python", "description": "Demo mode"},
        "stars": 0, "forks": 0, "open_issues": 0, "open_prs": 0,
        "recent_runs": 0, "failed_runs": 0, "languages": {"Python": 72, "JavaScript": 28},
        "last_push": datetime.now(timezone.utc).isoformat(), "health_score": 82,
        "recommendations": ["Adicione uma primeira issue para orientar contribuições.", "Mantenha uma execução automática diária para acompanhar a evolução."],
        "demo": True,
    }


def collect_data(repository: str) -> dict[str, Any]:
    repo = github_get(f"/repos/{repository}")
    issues = github_get(f"/repos/{repository}/issues?state=open&per_page=100")
    runs = github_get(f"/repos/{repository}/actions/runs?per_page=20").get("workflow_runs", [])
    languages = github_get(f"/repos/{repository}/languages")
    open_prs = sum(1 for issue in issues if "pull_request" in issue)
    failed_runs = sum(1 for run in runs if run.get("conclusion") == "failure")
    score, recommendations = 100, []
    if not repo.get("description"):
        score -= 10; recommendations.append("Adicione uma descrição curta e clara ao repositório.")
    if not repo.get("license"):
        score -= 8; recommendations.append("Inclua uma licença para deixar explícito como outras pessoas podem usar o projeto.")
    if not repo.get("has_issues"):
        score -= 5; recommendations.append("Ative Issues para receber dúvidas e contribuições.")
    if failed_runs:
        score -= min(30, failed_runs * 8); recommendations.append(f"Investigue {failed_runs} execução(ões) recente(s) com falha.")
    if not recommendations:
        recommendations.append("O repositório está bem configurado. Continue publicando melhorias pequenas e frequentes.")
    return {"repository": repo, "stars": repo.get("stargazers_count", 0), "forks": repo.get("forks_count", 0), "open_issues": len(issues) - open_prs, "open_prs": open_prs, "recent_runs": len(runs), "failed_runs": failed_runs, "languages": languages, "last_push": repo.get("pushed_at"), "health_score": max(0, score), "recommendations": recommendations, "demo": False}


def format_date(value: str | None) -> str:
    if not value:
        return "Sem registro"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M UTC")
    except ValueError:
        return value


def render(data: dict[str, Any]) -> str:
    repo = data["repository"]
    name = html.escape(repo.get("full_name", "GitHub Repository"))
    description = html.escape(repo.get("description") or "Painel de saúde e evolução do repositório")
    score = data["health_score"]
    score_class = "good" if score >= 80 else "warn" if score >= 60 else "risk"
    languages, total_bytes = data.get("languages", {}), sum(data.get("languages", {}).values()) or 1
    language_rows = "".join(f'<div class="language"><span>{html.escape(language)}</span><strong>{round(value / total_bytes * 100)}%</strong><i><b style="width:{round(value / total_bytes * 100)}%"></b></i></div>' for language, value in sorted(languages.items(), key=lambda item: item[1], reverse=True)[:5]) or '<p class="muted">Nenhuma linguagem encontrada.</p>'
    recommendations = "".join(f"<li>{html.escape(item)}</li>" for item in data["recommendations"])
    demo_note = '<span class="demo">modo demonstração</span>' if data.get("demo") else ""
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{name} | Repo Health Dashboard</title><style>
:root {{ color-scheme:dark; --ink:#eef2f7; --muted:#9aa7b5; --line:#263340; --panel:#111b24; --bg:#091017; --green:#61d7a4; --amber:#f4bf65; --red:#ff7b7b; --blue:#76b9ff; }} * {{ box-sizing:border-box; }} body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.5 Inter,ui-sans-serif,system-ui,sans-serif; }} main {{ max-width:1120px; margin:auto; padding:42px 22px 60px; }} header {{ display:flex; justify-content:space-between; gap:24px; align-items:flex-start; border-bottom:1px solid var(--line); padding-bottom:28px; }} .eyebrow {{ color:var(--green); font-size:12px; letter-spacing:.12em; text-transform:uppercase; font-weight:700; }} h1 {{ font-size:clamp(28px,5vw,48px); line-height:1.05; margin:10px 0; letter-spacing:0; }} p {{ color:var(--muted); margin:0; }} .demo {{ border:1px solid #65512c; color:var(--amber); padding:6px 10px; font-size:12px; white-space:nowrap; }} .score {{ min-width:150px; text-align:right; }} .score strong {{ display:block; font-size:54px; line-height:1; }} .score.good strong {{ color:var(--green); }} .score.warn strong {{ color:var(--amber); }} .score.risk strong {{ color:var(--red); }} .grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:26px 0; }} .metric,.panel {{ border:1px solid var(--line); background:var(--panel); }} .metric {{ padding:18px; min-height:112px; }} .metric span {{ color:var(--muted); font-size:13px; }} .metric strong {{ display:block; font-size:30px; margin-top:14px; }} .columns {{ display:grid; grid-template-columns:1.25fr .75fr; gap:12px; }} .panel {{ padding:22px; }} h2 {{ margin:0 0 20px; font-size:18px; }} .language {{ display:grid; grid-template-columns:1fr auto; gap:10px; margin:14px 0; }} .language strong {{ color:var(--blue); }} .language i {{ grid-column:1 / -1; display:block; height:7px; background:#24313d; }} .language b {{ display:block; height:100%; background:var(--blue); }} ul {{ margin:0; padding-left:20px; color:var(--muted); }} li+li {{ margin-top:12px; }} .meta {{ margin-top:24px; color:var(--muted); font-size:13px; }} .muted {{ color:var(--muted); }} @media (max-width:700px) {{ main {{ padding:28px 16px 40px; }} header {{ display:block; }} .score {{ text-align:left; margin-top:24px; }} .score strong {{ font-size:42px; }} .grid,.columns {{ grid-template-columns:1fr 1fr; }} .panel:first-child {{ grid-column:1 / -1; }} }} @media (max-width:420px) {{ .grid {{ grid-template-columns:1fr; }} }}
</style></head><body><main><header><div><div class="eyebrow">GitHub Repo Health Dashboard</div><h1>{name}</h1><p>{description}</p></div><div class="score {score_class}"><span>saúde geral</span><strong>{score}<small>/100</small></strong>{demo_note}</div></header><section class="grid"><div class="metric"><span>Estrelas</span><strong>{data["stars"]}</strong></div><div class="metric"><span>Forks</span><strong>{data["forks"]}</strong></div><div class="metric"><span>Issues abertas</span><strong>{data["open_issues"]}</strong></div><div class="metric"><span>Pull requests</span><strong>{data["open_prs"]}</strong></div></section><section class="columns"><article class="panel"><h2>Linguagens do projeto</h2>{language_rows}<div class="meta">Último push: {format_date(data.get("last_push"))}</div></article><article class="panel"><h2>Próximas melhorias</h2><ul>{recommendations}</ul><div class="meta">Execuções analisadas: {data["recent_runs"]} · Falhas: {data["failed_runs"]}</div></article></section></main></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="gera um painel local sem consultar a API")
    parser.add_argument("--repository", default=os.getenv("GITHUB_REPOSITORY", "TheoGoulart333/rpa-n8n-python"))
    args = parser.parse_args()
    try:
        data = demo_data() if args.demo else collect_data(args.repository)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"Não foi possível consultar o GitHub: {error}")
        print("Dica: use --demo para gerar uma prévia local.")
        return 1
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(render(data), encoding="utf-8")
    print(f"Dashboard gerado em {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
