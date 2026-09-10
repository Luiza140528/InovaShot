# DESIGN.md — Especificação visual oficial do InovaShot

> Fonte única de verdade dos formatos visuais do @inovashot.cortes.
> Qualquer sessão (Claude, humano, outro agente) deve ler este arquivo
> **antes** de gerar qualquer peça. Se um formato pedido não bater com
> uma das specs abaixo, pare e pergunte — não invente variação nova.

Última atualização: 10/09/2026, com base em verificação direta de
posts reais publicados (@inovashot.cortes).

---

## Regra de marca (vale para todo texto gerado, qualquer formato)

- Sujeito é sempre **"o InovaShot"** (masculino). Nunca "a InovaShot",
  nunca "a IA" como sujeito de frase de produto.
- ✅ "o InovaShot identifica...", "o InovaShot entrega..."
- ❌ "a IA identifica...", "a IA confusa sem você perceber..."
- "IA" só pode aparecer como palavra-chave de SEO ou em posts que
  comentam notícia/indústria de IA em geral — nunca como agente do
  InovaShot.
- Grafia correta: **InovaShot** (I maiúsculo, S maiúsculo, resto
  minúsculo). Nunca "Inovashot" nem "INOVASHOT" fora de kickers em
  caixa alta.

---

## Regra do kicker (vale pra Dark padrão, Lista, Reel/carrossel)

O kicker (linha pequena com ponto colorido, acima do título) **não é
fixo por formato** — é uma tag temática escolhida por post, conforme
o assunto/ângulo do conteúdo. Exemplos reais já usados:
`INOVASHOT · CORTES`, `SEM FRESCURA`, `CONTEÚDO · CORTES`.

Escolha o kicker pelo tom do post (confronto de crença → algo como
"SEM FRESCURA"; dica prática → "CONTEÚDO · CORTES"; etc.), sempre em
CAIXA ALTA, Poppins Medium, cor `#c8bedc`, com ponto roxo `#a855f7`
antes do texto.

**Única exceção:** o formato **Bastidores** tem kicker fixo:
`BASTIDORES`. Não varia, porque marca a categoria do formato em si,
não o tema do post.

---

## Formato 1 — Dark padrão
Carrossel 1080×1080. Uso: conteúdo direto, dicas, confronto de crença.

- Fundo sólido `#070412`. Nunca gradiente de fundo, nunca tema claro.
- Topo: ícone quadrado cantos arredondados (~74px), gradiente
  rosa→roxo (`#f472b6`→`#a855f7`), letra "I" branca centralizada +
  wordmark "InovaShot" ao lado (Poppins Bold ~56px). Única aparição
  do nome da marca no slide.
- Kicker dinâmico (ver regra acima) + barra gradiente 90×8px, 3 cores
  (`#f472b6`→`#a855f7`→`#38bdf8`, 90deg).
- Título: Poppins Bold branco ~58–68px.
- Corpo: Poppins Medium ~44px, cor `#dcd7e6`.
- Ghost number: Poppins Bold ~780px, opacidade ~10%, ancorado inferior
  direito. Omitido no slide de CTA.
- Faixa base: ~220px altura, blend ~35% do gradiente 3 cores sobre o
  fundo escuro.
- Rodapé: "Siga @inovashot.cortes" Poppins Bold ~40px `#ebe8f0`
  (esquerda) + paginação "0X/0Y" Poppins Medium (direita).
- Slide de CTA: sem ghost number, pede comentário de palavra-chave
  (varia por post: "CORTE", "CLIPE", "QUERO"...), seta poligonal
  (nunca emoji), "Link na bio".

---

## Formato 2 — Bastidores
Carrossel 1080×1080 e Reel 1080×1920. Uso: citações/opiniões diretas,
tom de bastidor/confissão.

- Fundo preto puro `#000000`.
- Topo-esquerdo: aspas `""` roxo `#a855f7`, Poppins Bold (quadrado
  ~88px, Reel ~110px).
- Topo-direito: wordmark "InovaShot" branco, Poppins Bold, texto
  simples — **sem** ícone quadrado "I" (o ícone existe só no Dark).
- Kicker fixo: `BASTIDORES` (nunca variar, nunca repetir
  "INOVASHOT").
- Barra abaixo do kicker: gradiente 2 cores apenas, rosa→roxo
  (`#f472b6`→`#a855f7`) — sem azul. Essa é a diferença-chave vs. Dark.
- Citação: Poppins Bold branco `#ffffff`. Ghost number branco ~10%
  opacidade.
- Rodapé: texto simples "@inovashot.cortes" Poppins Bold `#ebe8f0` —
  **sem** faixa gradiente (diferença-chave vs. Dark).
- Paginação conta o slide de CTA final no total (ex: 4 conteúdo + 1
  CTA = "0X/05").
- Reel (1080×1920): kicker começa em y=260; paginação empilhada
  abaixo do handle à esquerda, nunca no canto inferior direito.

---

## Formato 3 — Lista
Card único 1080×1080. Uso: conteúdo de valor genérico, diversificação
de pauta (não fala do InovaShot).

- Fundo `#070412`; kicker dinâmico + barra gradiente 3 cores.
- Card de lista: fundo `#120d20`, linhas divisórias `#261e37`,
  círculos numerados com cor interpolada da paleta (rosa→roxo→azul
  conforme a posição do item).
- Rodapé: faixa gradiente (blend 35%) + "@inovashot.cortes" Poppins
  Bold + seta poligonal.
- Regra de conteúdo: **nunca citar InovaShot no copy** — este formato
  existe pra entregar valor genérico e diversificar o feed.

---

## Formato 4 — Reel/carrossel multi-frame
1080×1920. Uso: sequência numerada de itens (ex: "Sinal 1, Sinal 2...",
"1. A reestruturação, 2. Teste da ideia..."). **Este é o formato dos
slides tipo "Sinal 3, o mais comum" e "1. A reestruturação"** — sem
wordmark/aspas de citação no topo, kicker dinâmico começando mais
alto na tela.

- Estrutura de 5 slides: 01 capa, 02–04 itens agrupados (título do
  item em Poppins Bold + descrição em Poppins Medium, ghost number
  incremental), 05 CTA sem ghost number.
- Kicker dinâmico começa em **y=260** (não y=90) pra não colidir com
  a UI nativa do Instagram (fileira "Amigos" quando o áudio é
  compartilhado).
- Rodapé: reservar **zona de segurança de ~300px** de fundo sólido
  limpo (sem faixa, sem texto) abaixo da faixa de rodapé — a faixa de
  220px deve terminar a ~300px do fundo absoluto do frame, nunca
  grudada no limite da tela. Isso evita que o overlay nativo do
  Instagram (usuário, legenda, música, botões "Insights"/"Turbinar")
  cubra "Siga @inovashot.cortes" e a paginação.
- Paginação "0X/0Y" sempre dentro da faixa de rodapé, à direita, nunca
  no canto inferior absoluto (ali o Instagram põe os próprios ícones).

---

## Checklist rápido antes de gerar qualquer peça

1. Qual dos 4 formatos é esse pedido? (Dark padrão / Bastidores /
   Lista / Reel-carrossel multi-frame) — não misturar specs entre
   eles.
2. O kicker é dinâmico (Dark, Lista, Reel) ou fixo "BASTIDORES"
   (só no formato Bastidores)?
3. O copy tem "IA" como sujeito em algum lugar? Se sim, trocar por
   "o InovaShot" antes de fechar.
4. Grafia "InovaShot" está certa (nem "Inovashot" nem "INOVASHOT"
   fora de kicker)?
5. Reel/carrossel: kicker em y=260 e zona de segurança de 300px no
   rodapé confirmadas?
