# Security Policy

## Reportando vulnerabilidades

Se voce encontrar uma vulnerabilidade, nao abra uma issue publica com detalhes sensiveis.

Entre em contato pelo e-mail publico de suporte informado no perfil do mantenedor ou na pagina do projeto.

## Boas praticas do projeto

- Nunca salve `GITHUB_TOKEN`, senhas ou chaves de API no repositorio.
- Use variaveis de ambiente para credenciais.
- Revise alteracoes em workflows antes de aceitar Pull Requests.
- Evite publicar dados privados de repositorios analisados.

## Escopo

Este projeto consulta dados da API do GitHub e gera um dashboard estatico. O principal risco esperado e vazamento acidental de tokens ou dados privados durante configuracao local.
