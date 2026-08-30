---
name: inovashot
description: Contexto completo do InovaShot (inovashot.com.br), SaaS de clipagem de vídeo com IA para criadores de conteúdo brasileiros, fundado e operado por Luiza a partir do celular em Pedreiras/MA. Use esta skill sempre que a tarefa envolver InovaShot — seja escrever conteúdo de marketing (posts, blog, legendas, roteiros, Threads/Instagram), seja peça visual (carrossel, imagem, landing page — cores oficiais e tipografia), seja trabalho técnico (backend Node.js no DigitalOcean, integrações de API, deploy, debug, arquitetura, Supabase, PM2/Nginx), seja decisão de produto/growth/pricing. Consulte também quando a pergunta mencionar "meu produto", "meu app", "o InovaShot" ou @inovashot.cortes, mesmo sem citar o nome completo.
---

# InovaShot — Skill de Contexto do Produto

Skill de referência único para qualquer tarefa relacionada ao InovaShot — evita reexplicar contexto toda vez.

## O que é

SaaS que usa IA para transformar vídeos longos (lives, podcasts, sessões oficiais) em clipes curtos virais, com hook A/B, nota de viralidade e publicação automática nas redes. Público: criadores de conteúdo brasileiros. Site: inovashot.com.br. Perfil de publicação automática: @inovashot.cortes (Threads).

Luiza é fundadora solo, opera majoritariamente pelo celular Android (não notebook) — isso importa tanto pra código (ver "Convenções de trabalho" abaixo) quanto pra marketing (a história "fundei do interior do Maranhão, pelo celular" é ativo de marca real, não gimmick).

## Stack técnico e arquitetura

- **Backend**: Node.js, roda em Droplet DigitalOcean (Ubuntu), gerenciado com PM2, proxy via Nginx
- **Repo**: GitHub `Luiza140528/InovaShot`, branch `main-/-frontend`
- **Banco**: Supabase (bucket `clips` público — necessário pro fluxo de publicação)
- **Pipeline de vídeo**: download YouTube (via proxy Webshare), transcrição Whisper + Claude, geração de clipes, FFmpeg (corte e remoção de silêncio via `silencedetect`), hook A/B + nota de viralidade
- **Auto-deleção**: clipes são apagados automaticamente após 3 dias (hoje via cron no PM2)
- **Publicação automática**: clipe com nota de viralidade ≥7 gera legenda via Claude Haiku e publica sozinho no Threads (@inovashot.cortes) via graph.threads.net — fluxo POST me/threads → creation_id → POST me/threads_publish
- **Pagamento**: Mercado Pago configurado; débito de créditos por uso
- **Login**: Google OAuth
- **Email transacional**: Gmail InovaShot
- **IDs de referência**: Meta App ID `1347752133848054`, Threads App ID `1868212397919801`, Facebook Page ID `1224411967402653`
- **Custos mensais aproximados**: Anthropic R$110, OpenAI R$26,59, DigitalOcean ~R$66, Railway R$25,79, Labels R$52,30, Netlify grátis

⚠️ **Segurança**: nunca colar chaves/tokens (Threads app secret, tokens de API) diretamente no chat, mesmo em debug. Se precisar referenciar, use placeholder e instrua Luiza a checar/rotacionar direto no painel ou `.env`.

### Antes de assumir que algo "funciona"

Há histórico de features documentadas como implementadas que na prática tinham bugs silenciosos (ex.: remoção de silêncio que rodava mas não cortava nada, por causa de um bug de captura de log no `execAsync`). **Regra prática**: para qualquer pendência técnica, não afirme que está resolvido só porque está no código ou na documentação — sugira teste ao vivo (log real, output real) antes de reportar como concluído.

## Convenções de trabalho técnico

- Luiza trabalha pelo celular: sempre entregar **arquivos completos corrigidos**, nunca só snippets/diffs soltos
- Orientação de terminal: **um passo de cada vez**, comandos prontos pra copiar e colar
- Preferir soluções que ela consiga validar sozinha (ex.: `pm2 logs`, `curl /health`) antes de considerar algo pronto
- Ao propor infraestrutura nova, considerar que o Droplet do DigitalOcean já roda processamento pesado (FFmpeg) e deve continuar sempre ligado; endpoints leves são candidatos a serverless (Supabase Edge Functions / Cloudflare Workers) pra evitar cobrança por inatividade

## Identidade visual

**Paleta oficial** (validada contra inovashot.com.br em 29/07/2026) — gradiente rosa → roxo → azul sobre fundo escuro:

| Cor | Hex | Uso |
|---|---|---|
| Rosa | `#f472b6` | Destaque, início do gradiente |
| Roxo | `#a855f7` | Cor principal da marca |
| Azul | `#38bdf8` | Destaque, fim do gradiente |
| Fundo escuro | `#070412` | Base de todo fundo dark |
| Texto | `#ffffff` | Texto principal sobre fundo escuro |

Gradiente padrão (CSS): `linear-gradient(135deg, #f472b6, #a855f7, #38bdf8)`

❌ Nunca usar: vermelho ou ciano isolados, paletas fora dessas cores, fundo claro/branco como base — **exceto** no template de carrossel claro (ver "Carrossel — template claro" abaixo), que é uma variante intencional, não um desvio de marca.

**Tipografia**: Poppins Bold em todo material visual (carrosséis, posts, landing pages). Emojis (⚡, →) não renderizam bem com Poppins Bold — usar ícone desenhado (polígono) ou alternativa em texto.

**Carrossel (Instagram/Facebook)**: formato quadrado 1080×1080px (nunca 1080×1350 — corta a barra de marca no preview do feed). "INOVASHOT" precisa aparecer com destaque visual em todo slide.

**Tokens de espaçamento** (pra UI do app, landing pages e peças com componentes — não só carrossel):

| Token | Valor | Uso |
|---|---|---|
| `--space-xs` | 8px | gap entre ícone e texto, padding interno pequeno |
| `--space-sm` | 12px | padding de botões, gap entre linhas |
| `--space-md` | 16–20px | padding de cards e componentes |
| `--space-lg` | 24–28px | separação entre seções da página |
| `--radius-card` | 12–14px | cantos de cards, exemplos, tabelas |
| `--radius-pill` | 999px | botões primário e secundário |

**Componentes:**
- **Botão primário**: fundo com o gradiente oficial (`linear-gradient(135deg, #f472b6, #a855f7, #38bdf8)`), texto sempre em `#070412` (escuro) — nunca texto branco em cima do gradiente, o contraste fica ruim. Border-radius `--radius-pill`.
- **Botão secundário**: fundo transparente, contorno sólido `#a855f7` (1.5px), texto branco. Mesmo radius do primário.
- **Card de conteúdo**: fundo `#16103a` (não usar o `#070412` puro pra cards sobre o fundo escuro — precisa de contraste sutil), borda `1px solid rgba(168,85,247,0.25)`, texto branco, `--radius-card`.

❌ Nunca usar gradiente escuro multi-stop como fundo de card ou seção — o fundo oficial é sempre sólido `#070412`. Gradiente é só pra texto de destaque, ícone e botão primário.

## Voz de marca e conteúdo de marketing

**Tom**: direto, sem economês, linguagem de quem constrói de verdade — nada de jargão de startup do Vale do Silício traduzido. Fala com criador de conteúdo brasileiro real, não com investidor.

**Regra de voz — "IA" nunca é sujeito da frase**: o InovaShot é sempre quem age no texto. "IA" só pode aparecer como palavra-chave de SEO (título de página, meta description, meta keywords) — nunca como quem faz a ação no texto voltado ao usuário.

- ❌ "A IA identifica os melhores momentos." / "Usamos inteligência artificial para cortar vídeos."
- ✅ "O InovaShot identifica os melhores momentos." / "O InovaShot corta o vídeo, você decide o que vale a pena."

**Ângulos que funcionam**:
- Bastidor real: "fundei isso do interior do Maranhão, com um celular" — usar como prova de que o produto é feito por quem entende a dor de quem cria sozinho, sem estrutura
- Resultado concreto > promessa vaga (número de clipes, tempo economizado, nota de viralidade real)
- Evitar hype genérico de IA ("revolucionário", "the future is now") — focar no problema específico que resolve (editar vídeo longo dá trabalho, o InovaShot faz o corte que vira)

**Canais ativos**: blog em inovashot.com.br com SEO, cross-post no Medium com link canônico, Threads (@inovashot.cortes, publicação automática de clipes), pesquisa em andamento de crescimento via Discord (comunidades de criadores tipo VDClip, LEOFGEDITZ) e Reddit (r/VideoEditing, r/brdev) como aquisição de custo zero — fase 1 Brasil, fase 2 expansão EN (concorrentes de referência: Opus Clip, Klap).

**Agente de marketing dedicado**: existe um Claude Project chamado "InovaShot Marketing" (codinome Eco) pra geração de conteúdo em lote — esta skill complementa, não substitui, esse projeto.

## Ao usar esta skill

1. Para tarefas técnicas: confirme antes de assumir estado de produção — peça log/teste real quando a dúvida for sobre algo crítico (pagamento, publicação, deleção de dados)
2. Para conteúdo: mantenha o tom direto e a história de fundação como pano de fundo, sem forçar em todo texto
3. Combine os dois quando fizer sentido (ex.: post técnico "como resolvi X" é conteúdo de marca também)

## Carrossel de Instagram/Facebook — template validado (30/07/2026)

Peça de referência: "Checklist Hook 3 Segundos" (7 slides, `inovashot_carrossel_hook3s/`).

**Formato**: 1080×1080px (quadrado), PNG RGB. Nunca 1080×1350 — o Instagram corta a barra de marca no preview do feed.

**Estrutura de cada slide** (de cima pra baixo):
1. Logo: raio desenhado (não emoji) + "InovaShot" em texto com gradiente rosa→roxo→azul, Poppins Bold, canto superior esquerdo
2. Pill de categoria: retângulo arredondado roxo sólido `#a855f7`, texto branco Poppins Bold (ex. "CRITÉRIO 01", "RESULTADO")
3. Título grande Poppins Bold branco, com 1 trecho em gradiente de destaque
4. Corpo de texto Poppins Regular
5. Cards quando aplicável: fundo `#16103a`, borda `rgba(168,85,247,0.25)` (~`#372169` sólido equivalente)
6. Barra inferior sólida full-bleed (encosta nas 4 bordas laterais), cor `#16103a`, com marca + contador de página ("02 / 07")

**Fundo do slide**: sempre sólido `#070412` — nunca gradiente (isso é regra geral da marca, não só de carrossel).

**Seta e outros ícones**: sempre desenhados (linha+triângulo, polígono), nunca glifo de texto (→, ⚡) — Poppins Bold não renderiza bem esses caracteres.

**Regra de segurança vertical**: nenhum conteúdo essencial a menos de ~120px da barra inferior. Validar com script (checar último pixel de conteúdo vs. início da barra), não só visualmente — folga mínima recomendada 100px.

**Erros já cometidos e corrigidos nessa sessão** (não repetir):
- Formato 4:5 (1080×1350) em vez de quadrado → corta no feed
- Fundo em gradiente multi-stop em vez de sólido `#070412`
- Fontes erradas (Bricolage Grotesque / JetBrains Mono / WorkSans) em vez de Poppins
- Seta (→) e raio (⚡) como caractere de texto em vez de ícone desenhado
- Espaço vazio grande no meio do slide por falta de elemento full-bleed no rodapé
- Nome do arquivo: usar `slide-N.png` (convenção padronizada em 30/08/2026 — substitui o `InovaShot_<descrição>_<n>.png` usado antes)
- Legenda com "a IA avalia/identifica" em vez de "o InovaShot avalia/identifica" (regra de voz)

## Carrossel — template claro (validado 30/08/2026)

Segunda variante de carrossel, usada em conteúdo tipo "achados/insights" (ex.: série "Radar Claude"). Convive com o template escuro acima — escolher conforme o tom da peça (escuro = produto/institucional, claro = editorial/dica). Peça de referência: `marketing/carrossel-radar-claude/` (6 slides).

**Formato**: 1080×1080px, PNG RGB — mesma regra do template escuro.

**Fundo**: gradiente diagonal (135deg) creme `#F6F1EA` → lilás `#E6DEF3`. Único lugar da marca onde fundo gradiente/claro é permitido.

**Estrutura de cada slide** (de cima pra baixo, margem lateral 72px):
1. Logo: mark "I" branco sobre quadrado arredondado com o gradiente oficial (rosa→roxo→azul), + wordmark "InovaShot" em Poppins ExtraBold escuro, canto superior esquerdo
2. Eyebrow: Space Mono Bold uppercase, cor roxa `#a855f7`, letter-spacing manual (Pillow não suporta tracking nativo — desenhar char a char)
3. Headline: Poppins ExtraBold (800), cor escura `#1A1A18`, com 1 trecho em gradiente rosa→roxo→azul (a frase-chave nunca pode quebrar entre linhas — tratar como token atômico no wrap)
4. Corpo (quando houver): dentro de chip fundo `#1A1A18`, cantos arredondados 24px, texto branco Poppins Regular
5. Rodapé fixo: linha fina + "SIGA @INOVASHOT.CORTES" em caixa alta (Space Mono Bold, roxo, tracking manual char a char) à esquerda + pill gradiente "O INOVASHOT" à direita (texto sempre escuro `#1A1A18` sobre o gradiente, nunca branco — mesma regra do botão primário)

**Layout**: bloco (logo+eyebrow+headline+chip) medido e centralizado verticalmente entre o topo e a linha do rodapé — evita slide com muito espaço vazio embaixo quando o corpo de texto é curto ou inexistente (capa).

**Fontes**: Poppins (ExtraBold/Bold/SemiBold/Medium/Regular) e Space Mono (Bold/Regular) via Google Fonts — não vêm instaladas no ambiente, baixar de `raw.githubusercontent.com/google/fonts/main/ofl/{poppins,spacemono}/`.

**Nomenclatura de arquivo**: `slide-N.png` — mesma convenção do template escuro (ver acima).

