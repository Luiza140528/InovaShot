---
name: InovaShot
description: Corte de vídeo automático pra criadores brasileiros — não é sorte, é o corte certo.
colors:
  bg: "#0e0820"
  bg2: "#16103a"
  card: "#1e1650"
  card2: "#2d2458"
  border: "#3b2f6e"
  rosa-sinal: "#f472b6"
  roxo-sinal: "#a855f7"
  azul-sinal: "#38bdf8"
  text: "#ffffff"
  muted: "#a0a0c0"
  footer-bg: "#070412"
  lilas-link: "#c4a5ff"
typography:
  display:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "56px"
    fontWeight: 900
    lineHeight: 1.1
    letterSpacing: "-1px"
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "38px"
    fontWeight: 800
    lineHeight: 1.2
  headline:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "18px"
    fontWeight: 700
    lineHeight: 1.4
  stat:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "36px"
    fontWeight: 900
    lineHeight: 1.1
  price:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "42px"
    fontWeight: 900
    lineHeight: 1.1
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
  nav:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  cta:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "15px"
    fontWeight: 700
    lineHeight: 1.4
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "13px"
    fontWeight: 700
    letterSpacing: "1px"
  label-sm:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "12px"
    fontWeight: 700
    letterSpacing: "0.5px"
  logo:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "26px"
    fontWeight: 900
    letterSpacing: "-0.5px"
  logo-footer:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "20px"
    fontWeight: 800
  display-mobile:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "34px"
    fontWeight: 900
    lineHeight: 1.1
  title-mobile:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "28px"
    fontWeight: 800
  stat-mobile:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "28px"
    fontWeight: 900
rounded:
  sm: "8px"
  md: "10px"
  lg: "12px"
  xl: "16px"
  pill: "20px"
spacing:
  xs: "8px"
  sm: "16px"
  md: "24px"
  lg: "40px"
  xl: "80px"
components:
  button-primary:
    backgroundColor: "linear-gradient(135deg, {colors.rosa-sinal}, {colors.roxo-sinal}, {colors.azul-sinal})"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "14px 36px"
  button-primary-hover:
    backgroundColor: "linear-gradient(135deg, {colors.rosa-sinal}, {colors.roxo-sinal}, {colors.azul-sinal})"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.roxo-sinal}"
    rounded: "{rounded.md}"
    padding: "14px 36px"
  button-outline-hover:
    backgroundColor: "{colors.roxo-sinal}"
    textColor: "{colors.rosa-sinal}"
  card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.text}"
    rounded: "{rounded.xl}"
    padding: "30px"
  input:
    backgroundColor: "{colors.bg}"
    textColor: "#e0e0ff"
    rounded: "{rounded.md}"
    padding: "12px 14px"
---

# Design System: InovaShot

## Overview

**Creative North Star: "Sinal Viral"**

InovaShot vive na metáfora de um sinal de transmissão elétrico cortando o
escuro — a energia de um clipe que está prestes a viralizar, capturada no
instante do corte. O fundo é sempre roxo quase-preto (#0e0820), como um
estúdio às 2h da manhã; contra esse breu, um gradiente neon de rosa a azul
carrega toda a informação que importa (título, CTA, número, ícone) como se
fosse o próprio sinal passando pela tela. Nada aqui aspira a "SaaS
profissional" — a estética é deliberadamente elétrica, cyberpunk-pop, feita
pra quem corta vídeo de madrugada no celular e quer que o produto pareça tão
rápido e vivo quanto o conteúdo que ele gera.

A interface não tenta se acalmar pra parecer "séria". Ela é confiante o
bastante pra brilhar. Cards e inputs ficam quietos e escuros em repouso;
cada interação (hover, foco, CTA) acende o gradiente neon como resposta —
tátil e elétrico, nunca decorativo por decoração.

**Key Characteristics:**
- Fundo roxo quase-preto único em toda a superfície (marketing e app usam o
  mesmo `:root`).
- Um único gradiente de marca (rosa → roxo → azul) carrega toda ênfase;
  cores sólidas (branco, cinza-lilás) fazem o resto do trabalho.
- Cards e superfícies ficam neutros em repouso; o neon aparece como reação
  a estado (hover, foco, destaque de plano).
- Cantos generosamente arredondados (8–20px) em tudo — nenhuma superfície
  reta ou cortante.
- Tipografia do sistema (system-ui stack), pesos pesados (700–900) pra
  títulos e números, deixando o peso visual pro gradiente, não pra fonte
  display.

## Colors

Paleta de duas camadas: neutros roxo-escuro pra estrutura, gradiente neon
de três cores pra tudo que precisa de atenção.

### Primary
- **Roxo Sinal** (#a855f7): cor de ação central — bordas de hover, foco de
  input, ícones de destaque, meio do gradiente de marca.
- **Rosa Sinal** (#f472b6): abre o gradiente de marca; usado sozinho em
  acentos pontuais (hover de link, badge de destaque).
- **Azul Sinal** (#38bdf8): fecha o gradiente de marca; raramente usado
  isolado, principalmente como a extremidade fria do gradiente em textos e
  CTAs.

### Neutral
- **Roxo Profundo** (#0e0820): fundo base de toda a aplicação — o "breu"
  contra o qual o neon acende.
- **Roxo Meia-Noite** (#16103a): variação de fundo em seções alternadas.
- **Roxo Cartão** (#1e1650): fundo padrão de cards, inputs (borda), painéis.
- **Roxo Cartão Elevado** (#2d2458): segunda camada de superfície, usada em
  gradientes internos de cards em destaque.
- **Borda Violeta** (#3b2f6e): toda borda de 1px em cards, inputs, divisores
  de header/footer.
- **Lilás Apagado** (#a0a0c0): texto secundário/muted em toda a interface.
- **Branco** (#ffffff): texto primário.
- **Roxo Rodapé** (#070412): fundo do footer, mais escuro que o body.
- **Lilás Link** (#c4a5ff): cor exclusiva de link no footer — mais clara
  que o roxo-sinal pra manter contraste alto sobre o fundo mais escuro do
  rodapé, migra pra rosa-sinal no hover.

### Named Rules
**The One Gradient Rule.** Existe um único gradiente de marca (rosa → roxo →
azul, 135deg pra botões/CTAs, 90deg pra texto/divisores). Ele nunca se
fragmenta em gradientes alternativos por seção — é a assinatura visual, não
um efeito reaproveitável à vontade.

**The Never-Corporate Rule.** Confirmado pela usuária: o visual nunca deve
suavizar em direção a um SaaS B2B genérico (fundo branco, sombras suaves,
paleta neutra "profissional"). O roxo-escuro com neon é proposital e
permanece mesmo sob pressão de parecer "mais sério".

## Typography

**Display Font:** system-ui stack (-apple-system, BlinkMacSystemFont,
'Segoe UI', Roboto, sans-serif) — sem fonte customizada carregada.

**Character:** Uma pilha de sistema só, mas usada com pesos extremos (700 a
900) e letter-spacing negativo em display/headline — o peso visual vem do
gradiente e do contraste de cor, não da personalidade da fonte em si.

### Hierarchy
- **Display** (900, 56px desktop / 34px mobile, line-height 1.1): H1 de
  hero, sempre com o trecho de maior impacto em `.gradient-text`.
- **Title** (800, 38px desktop / 28px mobile): títulos de seção
  (`.section-title`), sempre centralizados.
- **Headline** (700, 18px): nome de card de feature, título de card.
- **Stat** (900, 36px desktop / 28px mobile): números grandes do painel de
  stats (`.stat-number`).
- **Price** (900, 42px): valor do plano (`.plan-price`) — o único passo
  maior que Stat, reservado pro preço.
- **Body** (400, 16–18px, line-height 1.6–1.8): parágrafos e subtítulos de
  hero (`.hero-sub` usa 18px como variante grande do body).
- **Nav** (400, 14px): links de navegação do header.
- **CTA** (700, 15px): texto de botão (`.plan-cta`) e frases de apoio
  curtas (citação do hero, texto de rodapé de seção).
- **Label** (700, 13px, letter-spacing 1px): nome de plano
  (`.plan-name`), uppercase.
- **Label Small** (700, 12px, letter-spacing 0.5px): badges compactos
  (`.featured-badge`), texto legal de rodapé.
- **Logo** (900, 26px header / 20px footer, letter-spacing -0.5px): sempre
  em `.gradient-text`, nunca em cor sólida.

### Named Rules
**The Continuous Scale Note.** A escala não é um sistema fechado de 4
passos — o hand-coded CSS usa incrementos finos (12/13/14/15/16/18px pro
corpo de texto, 20/26/28/34/36/38/42/56px pra ênfase) conforme o contexto
pede. Isso é uma característica real do sistema, não drift: qualquer novo
tamanho deve continuar próximo de um desses passos observados em vez de
inventar um valor arbitrário fora da escala.

**The Gradient-Carries-Weight Rule.** Nunca introduzir uma segunda família
tipográfica pra criar hierarquia — hierarquia vem de tamanho, peso (700–900)
e aplicação seletiva de `.gradient-text`, mantendo a pilha de fontes única
em toda a superfície.

## Layout

Container central de 1200px (`max-width: 1200px; margin: 0 auto`) com
padding lateral de 40px (20px em mobile). Seções empilham verticalmente com
respiro generoso (`margin-bottom: 80px` entre blocos principais). Grids de
cartão usam `repeat(auto-fit, minmax(240–260px, 1fr))` — colunas fluidas,
sem breakpoints numerados além do único ponto de quebra mobile em 768px, que
reduz paddings, empilha a navegação e derruba os tamanhos de display/título.

Header é sticky com blur de fundo (`backdrop-filter: blur(10px)` sobre
`rgba(14,8,32,0.95)`), sempre no topo.

## Elevation & Depth

Sistema híbrido: superfícies ficam planas em repouso (sem sombra), e a
profundidade aparece só como resposta a estado — hover eleva o elemento
(`translateY(-3px)` a `-4px`) e acende um glow colorido em vez de uma sombra
neutra. Não existe uma escala de elevação estática tipo Material; existe uma
única transição de "apagado" pra "aceso".

### Shadow Vocabulary
- **Glow de botão primário** (`box-shadow: 0 0 20px rgba(168,85,247,0.5)`
  em repouso, `0 0 40px rgba(168,85,247,0.8), 0 0 80px rgba(244,114,182,0.4)`
  no hover): único vocabulário de sombra do sistema — nunca cinza, sempre
  colorido com a cor de marca.
- **Glow de card em hover** (`box-shadow: 0 10px 40px rgba(168,85,247,0.2)`):
  aplicado a feature-card e pricing-card ao passar o mouse.

### Named Rules
**The Glow-Not-Shadow Rule.** Toda sombra do sistema é colorida (rosa/roxo),
nunca cinza/preta. Se algo precisa de profundidade, ela vem como glow de
marca, não como sombra neutra de UI genérica.

## Shapes

Cantos generosamente arredondados em toda parte — nunca retos. Escala: 8px
(botões pequenos/inputs), 10–12px (botões, inputs, FAQ items), 16px (cards,
painel de stats), 20px (badges/pills, ex.: `featured-badge`, `hero-badge`).
Bordas são sempre 1px sólidas em `--border` (#3b2f6e) em repouso, migrando
pra roxo-sinal (#a855f7) em estados de hover/foco/destaque — nunca duas
larguras de borda diferentes coexistindo.

## Components

Tátil e elétrico: toda superfície interativa responde com movimento (subida
de poucos pixels) e luz (glow) — nada muda de estado só trocando de cor
plana.

### Buttons
- **Shape:** 10px de raio padrão (8px em variantes compactas de nav).
- **Primary (`.btn-neon`):** gradiente de marca 135deg de fundo, texto
  branco 700, padding 14px 36px, glow roxo em repouso que se intensifica e
  ganha um segundo halo rosa no hover, com leve elevação (`translateY(-3px)`).
- **Outline (`.btn-outline`):** fundo transparente, borda 2px roxo-sinal,
  texto roxo-sinal; no hover preenche com roxo translúcido e a borda/texto
  migram pra rosa-sinal.
- **Plan CTA (`.plan-cta`):** mesma lógica do outline em repouso; no hover
  (ou sempre, no plano `featured`) vira o gradiente de marca sólido.

### Cards / Containers
- **Corner Style:** 16px.
- **Background:** roxo-cartão (#1e1650), com o card `featured` recebendo um
  gradiente vertical sutil de roxo translúcido pra roxo-cartão.
- **Shadow Strategy:** ver Elevation — plano em repouso, glow roxo no hover
  (`translateY(-4px)`).
- **Border:** 1px `--border`, migra pra roxo-sinal em hover/destaque.
- **Internal Padding:** 30–32px.

### Inputs / Fields
- **Style:** fundo roxo-profundo (#0e0820), borda 1px `--border`, raio 10px,
  padding 12px 14px, texto #e0e0ff, placeholder em lilás apagado (#8a8aaa).
- **Focus:** só a borda muda de cor, pra roxo-sinal (#a855f7) — sem glow
  extra no campo, o glow fica reservado pros CTAs.

### Navigation
- Header sticky com fundo `rgba(14,8,32,0.95)` e blur; links em lilás
  apagado (14px) que viram rosa-sinal no hover; menu colapsa totalmente em
  mobile (768px) — sem hambúrguer, os links somem e o CTA de entrar
  permanece.

### FAQ Accordion (signature component)
Cada item é um card de 12px de raio que expande via `max-height` transition;
o ícone de toggle (⚡/seta) gira 180° e muda pra roxo-sinal quando ativo. A
resposta usa texto muted (14px) com padding assimétrico (0 20px 20px) só
quando aberta.

## Social Media Carousel (Instagram @inovashot.cortes)

Especificação separada do site: os slides de carrossel são gerados como
imagem (Python/Pillow), não HTML, então usam uma pilha tipográfica própria
(Poppins) em vez do system-ui stack do site — mas herdam as mesmas cores de
marca acima. **Aprovado pela usuária como padrão definitivo** após revisão
de slide em 31/08/2026; qualquer novo carrossel deve seguir esta estrutura.

### Format
- Canvas: 1080×1080px (quadrado) — nunca 1080×1350 (retrato corta no feed e
  no grid do perfil).
- Fundo: `colors.footer-bg` (#070412), o roxo mais escuro da paleta.
- Fonte: Poppins Bold (títulos), Poppins Medium (corpo). Nenhum emoji
  Unicode — ícones/setas são sempre polígonos desenhados (`ImageDraw.polygon`),
  por conflito visual de emoji com Poppins Bold.

### Slide Anatomy
- **Kicker** (topo): "INOVASHOT · CORTES" em Poppins Medium, com um ponto
  colorido (`roxo-sinal`) antes do texto.
- **Barra de gradiente**: linha curta (90×8px) logo abaixo do kicker, usando
  `The One Gradient Rule` (rosa → roxo → azul).
- **Número de fundo**: número do slide em branco puro a ~10% de opacidade,
  tamanho ~780px, ancorado no canto inferior direito — decorativo, nunca
  cobre o texto principal. Omitido no slide final de CTA.
- **Título**: Poppins Bold, maior corpo de texto do slide.
- **Corpo** (opcional): Poppins Medium, cor lilás-apagado (`colors.muted`),
  usado pra 1 frase de apoio por slide — nunca mais de uma ideia por card.
- **Faixa de gradiente na base**: banda horizontal (~220px de altura) na
  parte inferior do slide, gradiente de marca misturado a ~35% sobre o
  fundo escuro — sutil, não um bloco sólido de cor.
- **Rodapé**: `@inovashot.cortes` em Poppins **Bold** branco quase puro
  (#ebe8f0) — nunca cinza/muted aqui, pois testado e rejeitado por baixo
  contraste. Paginação "0X/05" alinhada à direita, Poppins Medium.

### Slide final (CTA)
- Sem número de fundo.
- Título = pedido de comentário de palavra-chave (ex: "Comenta 'CORTE' que
  eu te mando o link"), nunca link direto no corpo do slide.
- Corpo = reforço do posicionamento de marca ("O InovaShot corta o vídeo,
  você decide o que vale publicar").
- Seta poligonal + "Link na bio" como fechamento visual.

### Named Rule
**The Comment-Gate CTA Rule.** O carrossel nunca expõe o link diretamente
no slide de fechamento — o CTA sempre pede um comentário de palavra-chave
específica, alinhado à mecânica de alcance por comentário (igual ao restante
da estratégia de Reels/social do InovaShot).

## Do's and Don'ts

### Do:
- **Do** manter um único gradiente de marca (rosa → roxo → azul) como toda
  a linguagem de ênfase — não introduzir gradientes alternativos por seção
  ou feature.
- **Do** manter o fundo roxo quase-preto (#0e0820) como base em toda
  superfície nova, marketing ou app.
- **Do** usar glow colorido (nunca sombra cinza) como único vocabulário de
  profundidade.
- **Do** arredondar generosamente (mínimo 8px) — nenhum elemento com cantos
  retos.

### Don't:
- **Don't** suavizar pra estética de SaaS corporativo genérico (fundo
  claro, sombras neutras, paleta "profissional") — confirmado como
  anti-referência permanente pela usuária.
- **Don't** introduzir uma segunda família tipográfica; hierarquia vem de
  peso e cor, não de fonte.
- **Don't** aplicar o glow neon a superfícies em repouso — ele é
  reservado pra resposta de interação (hover/foco/destaque), não decoração
  estática.
