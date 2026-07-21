# Learnings

Memória persistente de erros já cometidos, causas raiz encontradas e o que
funcionou. O agente deve consultar este arquivo ANTES de investigar um
problema — se já foi visto antes, a causa provável já está aqui.

Formato de cada entrada:

```
## [DATA] Título curto do problema
- Sintoma:
- Causa raiz:
- Solução aplicada (ou status, se ainda não resolvido):
- Como evitar de novo:
```

---

## [2026-07] Remoção de silêncio via FFmpeg não confirmada (InovaShot)
- Sintoma: feature documentada como implementada (silencedetect no
  server.js), mas nunca testada contra vídeo real de produção.
- Causa raiz: ainda não investigada — suspeita de que o comando FFmpeg
  roda mas não altera o output, ou que o parsing do resultado do
  silencedetect está incorreto.
- Status: PENDENTE. Não assumir que funciona só porque está no código.
- Como evitar de novo: nenhuma feature de processamento de mídia deve ser
  marcada como "implementada" sem teste com arquivo real (ver
  verification-standard.md, seção 2).

## [2026-07] Botão "Buscar Tendências" quebrado (InovaShot — Módulo Político)
- Sintoma: botão retorna erro ao ser clicado.
- Causa raiz: frontend estava chamando a API da Anthropic diretamente do
  navegador, sem headers de autenticação (deveria passar por um endpoint
  backend que segura a API key).
- Solução aplicada: ainda não corrigido — precisa criar endpoint backend
  proxy que recebe a requisição do frontend e faz a chamada à Anthropic
  API do lado do servidor.
- Como evitar de novo: NUNCA chamar APIs externas com chave secreta
  diretamente do frontend. Toda chamada a Anthropic/OpenAI/etc deve
  passar por um endpoint backend próprio.

## [2026-07] Nginx client_body_timeout causando falha de upload (InovaShot)
- Sintoma: uploads de vídeo falhando em produção (DigitalOcean).
- Causa raiz: timeout do Nginx configurado baixo demais para uploads
  grandes.
- Solução aplicada: ajuste do client_body_timeout no Nginx. Corrigido.
- Como evitar de novo: ao adicionar features que envolvem upload de
  arquivo grande, checar configs de timeout (Nginx, proxy, load
  balancer) como parte do critério de aceitação.

## [2026-07] Meta Graph API (Facebook) retornando me/accounts vazio
- Sintoma: endpoint me/accounts da Graph API voltava vazio, publicação
  na Página não funcionava.
- Causa raiz: faltava o use case "Gerenciar tudo na sua Página" configurado
  no app do Facebook, além de escopo de token incorreto.
- Solução aplicada: configurado o use case correto + token com escopo
  certo. Resolvido em 12/07.
- Como evitar de novo: ao integrar qualquer API da Meta (Facebook/
  Threads/Instagram), checar use cases do app E escopo do token como
  primeiro passo de investigação, antes de assumir bug de código.

<!--
Template para novas entradas — copiar e preencher:

## [DATA] Título curto
- Sintoma:
- Causa raiz:
- Solução aplicada:
- Como evitar de novo:
-->
