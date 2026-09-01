# Contributing

Obrigado por considerar contribuir com o GitHub Repo Health Dashboard.

Este projeto existe para ajudar pessoas a entenderem a saude de um repositorio usando a API do GitHub e publicar um painel simples com GitHub Pages.

## Como contribuir

1. Procure uma issue aberta com os labels `good first issue`, `documentation`, `bug` ou `enhancement`.
2. Comente na issue dizendo que voce quer trabalhar nela.
3. Crie uma branch com um nome claro, por exemplo `fix/readme-example` ou `feature/language-card`.
4. Faca uma mudanca pequena e focada.
5. Rode os testes antes de abrir o Pull Request.

## Rodando localmente

Para gerar uma demo do dashboard sem token:

```bash
python3 github_dashboard.py --demo
```

Para rodar os testes:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile github_dashboard.py disparar.py
```

## Padrao de commits

Use mensagens curtas e claras:

```text
feat: adiciona card de linguagens
fix: corrige calculo de pull requests abertos
docs: melhora instrucoes de instalacao
test: cobre recomendacoes do dashboard
```

## Pull Requests

Um bom PR deve ter:

- descricao objetiva da mudanca;
- passos para testar;
- prints ou link do GitHub Pages quando a mudanca afetar o dashboard;
- referencia para a issue relacionada, quando existir.

## Codigo de conduta

Seja respeitoso, claro e paciente. Este projeto tambem serve como porta de entrada para pessoas que estao aprendendo open source.
