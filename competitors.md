# Concorrentes — InovaShot

Tracker de concorrentes diretos e adjacentes. Cada entrada: posicionamento,
pricing, features, e leitura competitiva (o que isso significa pra estratégia
do InovaShot). Atualizar sempre que houver pesquisa nova (scrape, teste do
produto, etc).

---

## Panda Video (pandavideo.com) — pesquisado em 09/08/2026

**O que é**: plataforma de hospedagem de vídeo brasileira (alternativa a
Vimeo/Bunny Stream), com feature de corte por IA ("Shorts"/"Clipper")
adicionada como bolt-on — não é produto clipping-first como o InovaShot.
30k+ clientes, 2M+ vídeos hospedados.

### Pricing (USD)
| Plano | Preço/mês | Pra quê |
|---|---|---|
| Clipper (standalone) | $3,90 | Só clipping: 12 créditos renováveis/mês, corta vídeos de até 2h, 15 dias de storage gratuito pros clipes |
| Bronze | $17,90 | Hospedagem, inclui Shorts + 30+30 créditos bônus no cadastro |
| Silver | $37,90 | Mais storage/bandwidth, até 2 usuários |
| Gold (mais popular) | $97,90 | Tudo + legendas/dublagem IA grátis, 10 usuários |
| Enterprise | sob consulta | — |

Modelo de créditos: 1 crédito = 10 min de vídeo fonte = US$0,20. Vídeo de
60 min consome 6 créditos.

### Features do Clipper
- Cola link do YouTube (ou usa vídeo já hospedado) → gera clipes automático
- Escolhe aspect ratio (vertical/horizontal) e duração média do clipe
- Personalização de marca: cor/estilo de legenda
- IA de "smart highlight detection" + **virality score** nos clipes gerados
- Legendas dinâmicas automáticas
- Produção em lote: um vídeo longo → vários clipes de uma vez

### Leitura competitiva
- Plano standalone de clipping ($3,90 ≈ R$21) é mais barato que o Starter do
  InovaShot (R$49,90), mas é **limitado por crédito** (12 créditos/mês ≈ 2h
  de vídeo fonte no total) — uso bem mais raso que os tiers fixos do
  InovaShot.
- Usam o termo **"virality score"** como nome oficial da métrica do produto
  — relevante porque há um relato de bug ainda não reproduzido sobre
  "hook_score vs virality_score" (ver `learnings.md`); pode ser confusão de
  nomenclatura vinda da comparação com esse concorrente.
- Depoimentos no site são todos sobre confiabilidade/custo de hospedagem vs
  Vimeo, não sobre qualidade do corte — sinaliza que clipping não é ainda a
  reputação forte deles. Abertura pro InovaShot se posicionar como
  clipping-first de verdade.

---

## Opus Clip (opus.pro) — pesquisado em 09/08/2026

**O que é**: líder de mercado em clipping por IA, posicionado como estúdio
de vídeo completo (não só corte) — B-Roll por IA, dublagem, reframe,
agendador social, editor completo, API/MCP pra agentes de IA. Usado por
Univision, HubSpot, LinkedIn.

### Pricing (USD)
| Plano | Preço/mês | Créditos | Pra quê |
|---|---|---|---|
| Free | $0 | 60/mês | 1080p, com marca d'água, sem edição, clipe expira em 3 dias |
| Starter | $15 | 150/mês | Individual: Virality Score, legendas animadas 20+ idiomas, auto-post YT Shorts/TikTok/IG Reels, editor, 1 template de marca, remoção de silêncio, sem marca d'água |
| Pro (mais popular) | $29 ($14,50/mês no anual) | 3.600/ano | Tudo do Starter + AI B-Roll, 10+ fontes de importação, export p/ Premiere/DaVinci, múltiplos aspect ratios, agendador social, dublagem, API limitada, 2 assentos de equipe |
| Business | sob consulta | customizado | Tudo do Pro + fila prioritária, storage dedicado, API/integrações custom, MSA, suporte com Slack dedicado |

### Features de destaque
- **Virality Score** — nome oficial da métrica de potencial viral (mesmo
  termo usado pelo Panda Video)
- ClipAnything: reprompt pra refinar o corte, seleção de timeframe/duração
- AI B-Roll, dublagem por IA, upscaling — vai muito além de corte simples
- API e **MCP** (Model Context Protocol) — permite que agentes de IA chamem
  o produto como ferramenta, não só usuário final
- Calculadora de ROI na própria página de pricing (clipes gerados, horas
  economizadas, views extras estimadas) — ferramenta de conversão forte

### Leitura competitiva
- É o concorrente mais robusto tecnicamente — feature set de estúdio
  completo (B-roll, dublagem, upscaling, export pra editor profissional)
  bem além do que o InovaShot oferece hoje. Não compete em preço de
  entrada, compete em profundidade.
- Preço do Starter ($15 ≈ R$83) é quase 2x o Starter do InovaShot (R$49,90)
  em termos nominais — mas entrega muito mais escopo. Confirma que o
  InovaShot está posicionado como opção mais acessível/enxuta, não como
  concorrente feature-a-feature.
- Confirma de novo o uso de **"Virality Score"** como termo padrão do
  mercado (2º concorrente a usar essa nomenclatura, depois do Panda Video)
  — reforça a hipótese de que o relato de bug "hook_score vs
  virality_score" citado em `learnings.md` venha de usuário comparando com
  a nomenclatura desses concorrentes, não de um bug real do InovaShot.
- Tem API/MCP pra agentes de IA — sinaliza que "virar ferramenta que outros
  agentes chamam" é uma direção que concorrentes grandes já estão
  perseguindo; não é prioridade agora pro InovaShot, mas vale monitorar.

---

## Klap (klap.app) — pesquisado em 09/08/2026

**O que é**: clipping por IA com modelo simples baseado em nº de clipes
(não crédito/minuto). 8,5M clipes gerados, 3,5M criadores. Produto pequeno
(fundado por 2 pessoas, @theo e @victor, via ZIGG SAS), mas com estratégia
de SEO/conteúdo muito agressiva — página de "alternativas" comparando
contra ~20 concorrentes (Opus Clip, Submagic, Veed.io, Vizard AI, etc).

### Pricing (USD, cobrança anual — mensal disponível mas não capturado)
| Plano | Preço/mês (anual) | Clipes/mês | Pra quê |
|---|---|---|---|
| Basic | $14 | 100 | Individual |
| Pro (mais popular) | $39 | 300 | Profissional |
| Pro+ | $94 | 1.000 | Equipes |

Todos os planos incluem: AI Clipping, contas sociais ilimitadas (TikTok,
Instagram, LinkedIn), Analytics.

### Leitura competitiva
- Modelo de preço por **número de clipes** (não minutos/créditos) é mais
  simples de entender pro usuário final do que o modelo do Opus Clip ou do
  Panda Video — vale considerar se o InovaShot quer testar essa
  simplicidade de comunicação, mesmo mantendo o modelo de tiers atual.
- Entrada mais barata que o Starter do InovaShot em termos nominais ($14 ≈
  R$77 vs R$49,90), mas isso é enganoso: câmbio e paridade de poder de
  compra tornam o InovaShot proporcionalmente muito mais barato pro
  criador brasileiro — vale usar isso na copy ("mesma tecnologia, preço
  pensado pro Brasil").
- **Estratégia de conteúdo a copiar**: Klap tem página dedicada de
  "alternativa a X" pra cada concorrente relevante (`/alternatives/opus-clip`,
  `/alternatives/veed-io`, etc.) — é uma tática de SEO/AEO barata e escalável.
  O InovaShot já tem conteúdo otimizado pra GEO/AEO (guias numerados); vale
  considerar páginas "InovaShot vs Opus Clip", "InovaShot vs Panda Video"
  como próximo passo de conteúdo, já que o próprio Klap valida que esse
  formato funciona.
- Sem feature de B-roll/dublagem/upscaling — mais parecido em escopo com o
  InovaShot do que o Opus Clip é.

---

## Submagic (submagic.co) — pesquisado em 10/08/2026

**O que é**: ferramenta de legendagem/edição por IA (legendas animadas,
B-roll, remoção de silêncio/gagueira) — clipping de vídeo longo pra curto
("Magic Clips") é um **add-on pago separado**, não vem incluído no plano
base. Usado por Shopify, Zapier, Crisp.

### Pricing (cobrança mensal, USD — valores anuais entre parênteses)
| Plano | Base/mês | + Magic Clips/mês | Uso |
|---|---|---|---|
| Starter | $19 ($12 anual) | +$19 (+$12 anual) | 15 vídeos/mês, máx. 2min/vídeo, 3 créditos de IA |
| Pro | $39 ($23 anual) | +$19 (+$12 anual) | 40 vídeos/mês, máx. 5min/vídeo, 6 créditos de IA |
| Business + API | $69 ($41 anual) | +$19 (+$12 anual) | 100 vídeos/mês, máx. 30min/vídeo, 15 créditos de IA, 4K/60fps |
| Custom | sob consulta | — | volume customizado |

**Importante**: eles já publicam preço nativo em **BRL** na própria página
de pricing — Starter R$79, Pro R$159, Business R$279 (+R$79/mês pro
add-on Magic Clips). Ou seja, já localizam preço pro Brasil.

Créditos de API separados: de 500 min/US$75/mês (US$0,15/min) até 10.000
min/US$1000/mês (US$0,10/min).

### Features
- Legendas animadas automáticas, tradução de legenda, remoção de
  silêncio/gagueira/"bad takes", correção de contato visual por IA
- B-roll automático (Storyblocks/Movie Clips nos planos pagos)
- "Magic Clips" (add-on): pega vídeo longo → gera clipes virais — mesma
  função central do InovaShot, mas vendida separadamente
- API de edição de vídeo pra automação

### Leitura competitiva
- Preço nativo em BRL confirma que pelo menos um concorrente internacional
  já enxerga o Brasil como mercado prioritário — reforça a importância do
  InovaShot manter vantagem de custo/localização como diferencial, não
  suposição.
- Comparando clipping equivalente: Starter (R$79) + Magic Clips (R$79) =
  **R$158/mês** só pra ter a função de corte automático — mais de 3x o
  Starter do InovaShot (R$49,90) pela mesma capacidade central. Isso é o
  argumento de preço mais forte que o InovaShot tem contra um concorrente
  internacional de peso.
- Confirma o padrão já visto no Panda Video: em produtos que não nasceram
  clipping-first, o corte automático é tratado como **feature adicional**,
  não como o produto principal. O InovaShot sendo clipping-first desde o
  início é diferencial de posicionamento genuíno, não só discurso de
  marketing.

---

## Vizard AI (vizard.ai) — pesquisado em 10/08/2026

**O que é**: clipping-first como o InovaShot (ao contrário do Submagic/
Panda Video), com modelo de créditos por minuto. Usado por Google, Ubisoft,
Stanford. Nota 4.7-4.9 em G2/Capterra/Software Advice.

### Pricing (USD, mensal — valor anual com 50% off entre parênteses)
| Plano | Preço/mês | Créditos | Uso |
|---|---|---|---|
| Free | $0 | 60/mês | 720p export, storage de 3 dias, 1 conta social |
| Creator (mais popular) | $29 ($14,50 anual) | a partir de 600/mês (7.200/ano) | Sem marca d'água, export 4K, agendamento social, 100GB storage, 6 contas sociais |
| Business | $39 ($19,50 anual) | a partir de 600/mês | Workspace compartilhado, 20 contas sociais, membros de equipe +$5/mês/assento, brand kit, storage ilimitado |

Modelo de crédito: **1 crédito = 1 minuto de vídeo enviado** (consumo no
upload, não no clipe gerado).

### Features
- Clipping por IA com reframe automático, emojis/palavras-chave em
  destaque, B-roll de IA
- Publicação direta em redes sociais (mais contas sociais = planos mais
  caros, ao contrário do InovaShot)
- API própria com rate limit por plano (1/min no Free até 10/min no
  Business)
- Tem página própria de "Vizard vs X" pra Opus, Capcut, Vidyo, Getmunch,
  Captions, Submagic, Veed — mesma tática de SEO comparativo que o Klap usa

### Leitura competitiva
- É o concorrente mais parecido em modelo de negócio com o InovaShot:
  clipping-first, sem hospedagem de vídeo, sem legenda/edição como produto
  principal. Bom benchmark direto de feature-a-feature.
- Preço de entrada ($29 ≈ R$160) é bem mais caro que o Starter do InovaShot
  (R$49,90) em termos nominais, mas modelo de crédito por **minuto
  enviado** (não por clipe gerado) pode punir usuários que sobem vídeos
  longos e cortam pouco — vale considerar se o InovaShot quer comunicar
  isso como vantagem ("sem cobrar pelo tamanho do vídeo que você manda,
  só pelo que você usa").
- Assim como Klap e agora confirmado por outro concorrente (Vizard), a
  tática de página "[Produto] vs [Concorrente]" pra SEO é praticamente
  padrão de mercado entre os players de clipping — mais um voto a favor de
  priorizar esse formato de conteúdo pro InovaShot.

---

## Veed.io (veed.io) — pesquisado em 10/08/2026 — **concorrente adjacente, não direto**

**O que é**: estúdio de vídeo por IA muito amplo — geração de vídeo por
texto, avatares de IA, clonagem de voz, geração de imagem, dublagem —
com o corte de clipe viral sendo **uma ferramenta entre dezenas**, não o
produto principal. Cliente enterprise pesado: Amazon, Netflix, Google,
Meta, BBC, NBCUniversal.

### Pricing (USD, créditos de IA cobrem a plataforma toda, não só clipes)
| Plano | Preço/mês | Créditos/ano | Uso |
|---|---|---|---|
| Creator | $12 ($147/ano) | 6.000 (~1.500 vídeos de IA) | Sem marca d'água, legendas automáticas ilimitadas |
| Pro (recomendado) | $22 ($265/ano) | 30.000 (~7.500 vídeos) | + múltiplos brand kits, tradução 50+ idiomas |
| Studio | $39 ($465/ano) | 180.000 (~45.000 vídeos) | + templates customizados |
| Enterprise | sob consulta | customizado | Gestão centralizada de equipes, controles de privacidade |

### Features do "AI Clip Generator"
- Extrai clipes de vídeos longos (podcast, webinar) com prompt opcional
  guiando quais momentos priorizar
- Sistema de pontuação por clipe em **4 eixos**: Flow, Impact, Clarity,
  Relevance (0-10 cada) — mais granular que o "virality score" único
  usado por Opus Clip/Panda Video
- Editor baseado em transcript pra ajustar/estender clipe depois de gerado
- Compara-se abertamente com o **Opus Clip** na própria landing page do
  Clip Generator (logo do concorrente exibido)

### Leitura competitiva
- Não é concorrente direto no sentido estrito — é uma plataforma de IA
  generativa de vídeo (avatares, texto-pra-vídeo, dublagem) onde clipping
  é só mais uma ferramenta. Escopo mais parecido com Opus Clip do que com
  o InovaShot.
- O sistema de pontuação em 4 eixos (Flow/Impact/Clarity/Relevance) é uma
  terceira nomenclatura diferente pra "potencial de viralização" — reforça
  que não existe padrão único de mercado pro nome dessa métrica, o que
  aumenta a chance de confusão de usuário vindo de qualquer um desses
  concorrentes (mais um dado a favor da hipótese de nomenclatura confusa
  no relato "hook_score vs virality_score").
- Cliente-base é majoritariamente enterprise — não é ameaça direta ao
  público criador brasileiro que o InovaShot atende, mas vale monitorar
  se lançarem plano de entrada mais agressivo.

---

## Captions (captions.ai) — pesquisado em 10/08/2026 — **concorrente adjacente, não direto**

**O que é**: app (mobile-first, iOS) de geração de conteúdo por IA
generativa — avatares/"digital twins", UGC de IA, edição via chat — não é
uma ferramenta de corte de vídeo longo em clipes. Repurposing de vídeo
("AI Shorts", "Reddit to Reel") existe, mas é feature secundária dentro
de "Link to video", não o produto central. Empresa: NOCAP, Inc. d/b/a
Captions.

### Pricing (USD — só planos iOS, créditos cobrem toda a IA generativa)
| Plano | Preço/mês | Créditos |
|---|---|---|
| Max (mais popular) | $24,99 | 500/mês |
| Scale | $69,99 | 1.400/mês |
| Scale 2x | $139,99 | 2.800/mês |
| Scale 4x | $279,99 | 5.600/mês |
| Enterprise | sob consulta | customizado, com desconto de volume |

### Leitura competitiva
- Overlap real com o InovaShot é baixo — o produto central deles é criar
  vídeo novo com avatar/ator de IA, não cortar vídeo longo existente.
  "AI Shorts"/"Reddit to Reel" é a única feature que toca o caso de uso do
  InovaShot, e aparece como item secundário na tabela de comparação.
  Categorizar como referência de mercado adjacente (IA generativa de
  vídeo), não como concorrente de clipping.
- Preço de entrada ($24,99 ≈ R$138) é mais caro que o Pro do InovaShot
  (R$97,90) pra um produto que nem foca em clipping — não é comparação
  direta útil pra posicionamento de preço.
- Vale reavaliar essa entrada só se a Captions expandir a feature de
  repurposing de vídeo longo pra virar core do produto — hoje não é o
  caso.
