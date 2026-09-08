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

## [2026-09] FONT_DIR hardcoded quebra gen_bastidores_sample.py fora do servidor original
- Sintoma: ao tentar reconfirmar visualmente o fundo #070412 do
  `gen_bastidores_sample.py`, o script quebrou com `OSError: cannot open
  resource` antes de gerar qualquer imagem.
- Causa raiz: `FONT_DIR` estava hardcoded em
  `/usr/share/fonts/truetype/google-fonts`, caminho que não existe neste
  ambiente (as fontes Poppins reais do projeto ficam em
  `scripts/fonts/`). `gen-carousel-dark.py` já tinha sido corrigido pra
  usar caminho relativo ao próprio arquivo; `gen_bastidores_sample.py`
  (e `gen_listicle.py`, ainda não corrigido) ficaram pra trás com o
  caminho absoluto antigo.
- Solução aplicada: `FONT_DIR` de `gen_bastidores_sample.py` trocado pra
  `os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")`,
  igual ao padrão de `gen-carousel-dark.py`. Reconfirmado rodando o
  script de ponta a ponta: pixel de fundo gerado = `(7, 4, 18)` =
  `#070412`. Commit `f55b219` (07/09/2026).
- Atualização (07/09/2026): `gen_listicle.py` corrigido com o mesmo
  padrão (commit a seguir), reconfirmado rodando de ponta a ponta —
  pixel de fundo também `(7, 4, 18)`. Pendência fechada.
- Atualização (08/09/2026): `grep -rn "/usr/share/fonts"` no repo
  inteiro achou mais um caso — `gen_reel_carousel.py` (na raiz do
  projeto, não em `scripts/`). Corrigido apontando `FONT_DIR` pra
  `scripts/fonts` relativo ao próprio arquivo (não `SCRIPT_DIR/fonts`
  puro, já que este script não mora em `scripts/`). Testado em
  produção de ponta a ponta (fundo `(7, 4, 18)`). Confirmado por
  `grep` que não sobra nenhum outro `/usr/share/fonts` hardcoded no
  repo.
- Status: RESOLVIDO (08/09/2026). Os 3 scripts afetados
  (`gen_bastidores_sample.py`, `gen_listicle.py`,
  `gen_reel_carousel.py`) corrigidos e testados de ponta a ponta em
  produção; `gen-carousel-dark.py` já estava correto. Nenhum caso
  restante no repo.
- Como evitar de novo: qualquer script gerador de asset visual novo
  deve usar caminho de fonte relativo ao próprio arquivo
  (`os.path.dirname(os.path.abspath(__file__))`), nunca caminho
  absoluto de sistema — ambientes diferentes (servidor de produção vs.
  sessão local vs. container de verificação) não têm garantia da mesma
  árvore de fontes do sistema.

## [2026-09] gen_listicle.py sobrepõe linhas com muitos itens
- Sintoma: ao testar `lista_slide()` com edge cases (1 item vs. 7 itens
  + headline longo) depois do fix do `FONT_DIR`, o slide de 7 itens saiu
  com texto e círculos numerados sobrepostos de forma severa — item 1
  atropelado pelo texto do item 2, item 2 pelo item 3, etc. Slide de 1
  item saiu correto (sobra espaço vazio no card).
- Causa raiz: em `lista_slide()` (scripts/gen_listicle.py:210-212),
  `scale = card_height / natural_total` encolhe a altura de CADA LINHA
  proporcionalmente pra caber no card, mas o conteúdo desenhado dentro
  da linha — círculo de raio fixo (`circle_r = 34`) e bloco de texto
  (`line_h_total`, dependente do wrap real) — não escala junto. Quando
  `natural_total` (soma das alturas naturais) é bem maior que
  `card_height` disponível (muitos itens, ou headline longo reduzindo
  o espaço do card), `scale` fica bem menor que 1 e a linha escalada
  fica menor que o conteúdo real, causando sobreposição visual.
- Solução aplicada (08/09/2026): `scale` agora usa
  `max(card_height / natural_total, 1.0)` — nunca comprime abaixo do
  tamanho natural de cada linha, só estica pra preencher espaço sobrando.
  Reconfirmado rodando os dois edge cases: 1 item (idêntico a antes,
  sem regressão) e 7 itens + headline longo (sobreposição eliminada,
  cada linha legível).
- Mitigação intermediária (08/09/2026, substituída no mesmo dia): teto
  fixo `MAX_ITEMS = 5` resolvia o caso comum mas não o geral (headline
  longo ainda estourava mesmo com só 5 itens truncados).
- Solução definitiva aplicada (08/09/2026): teto fixo removido.
  `lista_slide()` agora calcula a altura natural de TODOS os itens
  recebidos (`all_rows`), depois monta `rows_data` adicionando item por
  item só enquanto a soma das alturas naturais couber em `card_height`
  (que já reflete o espaço real sobrando depois do headline) — sempre
  mantém pelo menos 1 item mesmo que ele sozinho não caiba, pra nunca
  renderizar um card vazio. Como `rows_data` final sempre cabe por
  construção, o `scale` (clamp em `max(..., 1.0)`) só estica pra
  preencher, nunca comprime.
- Reconfirmado rodando os 4 casos de teste que expuseram os bugs
  anteriores: 1 item (sem regressão), headline curto + 6 itens (trunca
  dinamicamente pra 5, idêntico ao teto fixo — mas agora por cálculo,
  não coincidência), headline longo + 5 itens (trunca pra 3, cabe sem
  overflow), headline longo + 7 itens (trunca pra 3, cabe sem overflow
  nem sobreposição). Nenhum dos 4 casos estoura ou sobrepõe mais.
- Como evitar de novo: ao implementar layout que escala altura de linha
  proporcionalmente pra caber num espaço fixo, sempre testar com o caso
  de "muito conteúdo" (mais itens do que o "feliz" caminho testado
  originalmente) — escalar o espaçamento sem escalar o conteúdo
  desenhado dentro dele é uma classe de bug fácil de não notar testando
  só com poucos itens.

## [2026-09] gen_reel_carousel.py: body_slide() sem limite de conteúdo, invade rodapé
- Sintoma: ao testar edge cases do `gen_reel_carousel.py` (mesmo
  exercício que achou o bug de overflow do `gen_listicle.py`), rodei
  `body_slide()` com 5 itens (título + texto cada, 1 com texto longo)
  e o conteúdo acumulado invadiu visualmente a faixa de rodapé.
- Causa raiz: em `body_slide()` (gen_reel_carousel.py:189-220), `y`
  cresce sequencialmente a cada item/linha sem NENHUM check contra
  `H - FOOTER_HEIGHT` (1600) ou contra `SAFE_ZONE` (480px reservados
  pra UI do Reels, documentados no próprio docstring do arquivo,
  linha 11: "Safe zone 480px at bottom - no custom footer content
  there"). Diferente do `gen_listicle.py`, aqui nem existe uma "área
  fixa" (tipo o card) pra comparar contra — é desenho sequencial puro.
- Verificação numérica (script de debug isolado, reimportando as
  funções reais do arquivo): com o sample de 5 itens, `y` final = 1626.
  Rodapé começa em 1600 → invade a faixa em 26px. Safe zone começa em
  1440 → o conteúdo já estava dentro da área reservada da UI do Reels
  bem antes do rodapé.
- `cover_slide()` tem a mesma estrutura de risco (headline + body sem
  limite), mas não foi reproduzido no teste feito (headline de 4 linhas
  + body de 3 linhas coube com espaço sobrando).
- Status: NÃO CORRIGIDO. Identificado em 08/09/2026. Correção provável
  seria replicar a mesma estratégia usada em `gen_listicle.py`: truncar
  itens dinamicamente com base no espaço real disponível antes do
  rodapé/safe zone, em vez de desenhar sem limite.
- Como evitar de novo: qualquer gerador de slide que desenha conteúdo
  sequencialmente (sem card/área fixa) ainda precisa de uma checagem
  de limite contra o rodapé e qualquer safe zone documentada — a
  ausência de um "container" visual não significa ausência do bug de
  overflow, só significa que ele é mais fácil de esquecer de checar.

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
