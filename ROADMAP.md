# Roadmap

Este roadmap lista melhorias pequenas e boas para novos contribuidores. Cada item pode virar uma issue no GitHub.

## Good first issues

### Docs: adicionar exemplo de uso com repositorio real

Adicionar ao README um exemplo mostrando como executar o dashboard contra um repositorio real do GitHub.

Sugestao:

- incluir comandos com `GITHUB_REPOSITORY=owner/repo`;
- explicar quando usar `GITHUB_TOKEN`;
- reforcar que tokens nunca devem ser salvos no repositorio.

### Feature: mostrar top linguagens no dashboard

Melhorar o dashboard exibindo as principais linguagens do repositorio de forma mais visual.

Sugestao:

- usar os dados de linguagens ja coletados pela API do GitHub;
- renderizar uma lista ou barra percentual no HTML;
- manter o layout funcionando em telas pequenas.

### Test: cobrir calculo de pontuacao de saude

Adicionar testes para o calculo da pontuacao de saude do repositorio.

Sugestao:

- cobrir repositorio saudavel;
- cobrir repositorio sem atividade;
- cobrir repositorio com muitas issues abertas.

## Ideias maiores

- Comparar dois repositorios lado a lado.
- Exportar dados em JSON para outras automacoes.
- Adicionar modo de analise para organizacoes inteiras.
- Criar badges para README com a pontuacao de saude.
