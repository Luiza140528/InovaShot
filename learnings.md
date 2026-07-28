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
- Atualização (21/07): confirmado por leitura do server.js REAL de
  produção (obtido via SFTP, não do GitHub) que `generateClip()` chama
  `return await removeSilence(clipPath)` de fato — antes o código do
  GitHub estava desatualizado e só retornava `clipPath` sem remoção.
  Isso resolve a dúvida de "será que está no código", mas NÃO é ainda
  um teste real com vídeo — falta rodar um processamento completo e
  comparar duração/conteúdo do output antes/depois.
- Atualização (28/07): teste funcional real executado (vídeo sintético de
  10s com silêncio digital real em 2-4s e 6-8s, processado pela função
  `removeSilence()` extraída verbatim de server.js e rodada isolada em
  harness Node — ver PROGRESS.md/outputs/ para logs e arquivos completos).
  CAUSA RAIZ ENCONTRADA: em `removeSilence()` (server.js:857-934), o log do
  `ffmpeg -af silencedetect=... -f null -` só é capturado dentro do bloco
  `catch` do `execAsync`, assumindo que esse comando sempre lança exceção.
  Na prática, `silencedetect` escreve os timestamps no stderr mas o
  processo termina com exit code 0 (sucesso) — então `execAsync` RESOLVE em
  vez de rejeitar, o `catch` nunca roda, `silenceLog` fica sempre `''`, e a
  função sempre cai em `if (starts.length === 0) return clipPath;`,
  devolvendo o clipe ORIGINAL sem nenhum corte. Confirmado com `cmp`
  byte-a-byte entre input e output.
- Status: RESOLVIDO (28/07). Correção aplicada em `backend/src/server.js`
  (capturar `stdout`/`stderr` também no caminho de SUCESSO do `execAsync`,
  não só no `catch`) e reconfirmada com o mesmo harness: saída passou de
  10s (idêntica à entrada, bug) para 6.03s (corte correto, bate com os
  blocos de áudio audível esperados). Deployada em produção em 28/07 via
  `pm2 restart inovashot` (este ambiente É o servidor de produção —
  confirmado por `pm2 describe inovashot`), com `/health` respondendo 200
  após o restart.
- Como evitar de novo: nenhuma feature de processamento de mídia deve ser
  marcada como "implementada" sem teste com arquivo real (ver
  verification-standard.md, seção 2). Além disso: ao usar `execAsync`/
  `exec` do Node para capturar log de uma ferramenta CLI (ffmpeg, etc),
  NUNCA assumir que "informação relevante só vem via exceção" — exit code
  0 é sucesso mesmo quando a ferramenta escreve warnings/dados no stderr;
  sempre capturar `stdout`/`stderr` da resolução bem-sucedida também.

## [2026-07] GitHub desatualizado em relação à produção (InovaShot)
- Sintoma: código no GitHub divergia significativamente do que rodava
  em produção (`/app/inovashot/backend/src/server.js`) — descoberto ao
  investigar o bug do Trends.
- Causa raiz: mudanças feitas direto no servidor (via SSH) nunca foram
  commitadas de volta ao GitHub. Diferenças incluíam: rota
  `/api/tendencias` (implementação própria via fetch, não o SDK),
  chamada real a `removeSilence()`, observação do orquestrador de
  transcrição, cálculo de confidence do Whisper, mensagens de erro em
  português.
- Solução aplicada: `server.js` real de produção (obtido via SFTP)
  commitado no GitHub em 21/07. Confirmado por `git clone` + `diff` que
  os dois ambientes estão idênticos agora.
- Como evitar de novo: qualquer edição feita direto no servidor via SSH
  deve ser commitada de volta ao GitHub no mesmo dia. Antes de investigar
  qualquer bug "resolvido no GitHub mas ainda ocorrendo", checar primeiro
  se produção e GitHub estão sincronizados (`git status` no diretório
  real de produção, localizado via `pm2 describe <app>`).

## [2026-07] Botão "Buscar Tendências" quebrado (InovaShot — Módulo Político)
- Sintoma: botão retorna erro ao ser clicado.
- Causa raiz original: frontend estava chamando a API da Anthropic
  diretamente do navegador, sem headers de autenticação.
- Causa raiz secundária (descoberta em 21/07): o diretório real de
  produção no PM2 NÃO é `~/InovaShot/backend` (não existe) — é
  `/app/inovashot/backend`, confirmado via `pm2 describe inovashot`
  (campos `script path` e `exec cwd`). O repositório GitHub e a
  produção estavam dessincronizados: a correção commitada no GitHub
  (rota via SDK Anthropic, commit 89dea17) nunca foi deployada nesse
  diretório. A produção já tinha uma implementação PRÓPRIA e diferente
  da rota `/api/tendencias` (usando `fetch` direto com header
  `x-api-key`, não o SDK), criada localmente no servidor e nunca
  commitada de volta ao GitHub.
- Solução aplicada: confirmado por teste real (log do PM2 + clique no
  botão pelo celular, 21/07 17:18) que a rota já em produção estava
  funcionando corretamente. RESOLVIDO.
- Verificação real feita (não assumida):
  - `pm2 describe inovashot` → confirmou script path e exec cwd reais
  - `git status` no diretório de produção → confirmou mudanças não
    commitadas (`src/server.js`, `package.json`) divergentes do GitHub
  - `grep`/`awk` no `.env` → confirmou `ANTHROPIC_API_KEY` presente e
    bem formada (sem expor o valor)
  - `pm2 logs inovashot --lines 0` + clique real no botão pelo app →
    confirmou resposta com conteúdo válido renderizado na tela
- Pendência aberta: `server.js` de produção está desalinhado do
  GitHub (mudanças não commitadas). Precisa subir a versão real de
  produção para o repositório, ou um próximo `git pull` no servidor
  pode sobrescrever a versão que está funcionando.
- Como evitar de novo:
  1. NUNCA chamar APIs externas com chave secreta diretamente do
     frontend — toda chamada deve passar por endpoint backend próprio.
  2. NUNCA assumir que o caminho de deploy é o mesmo do `git clone`
     local/GitHub — confirmar sempre via `pm2 describe <app>` (campos
     `script path` e `exec cwd`) antes de investigar arquivo errado.
  3. Rodar `git status` no diretório real de produção como parte da
     investigação — divergência entre produção e GitHub é uma causa
     raiz tão comum quanto bug de código.
  4. "Está no GitHub" não significa "está em produção". Só reportar
     como corrigido depois de teste real no ambiente que o usuário usa.

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
