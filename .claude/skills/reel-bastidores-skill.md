# Skill: Gerar Reel Bastidores (formato nativo 1080x1920)

## Quando usar
Sempre que for produzir um Reel pra série Bastidores (@inovashot.cortes) misturando
slides de texto gerados com prints reais (Termius, GitHub, etc).

## Fluxo geral
1. Gerar as imagens dos slides de texto em Python + Pillow, **nativas em 1080x1920**
   (nunca gerar em 1080x1080 e depois espremer/centralizar — isso quebra a posição
   do rodapé e cria efeito de "pôster" com barra flutuando no meio do quadro).
2. Recortar os prints reais (screenshots de celular) removendo status bar, barra de
   endereço e teclado, centralizando o conteúdo relevante num canvas 1080x1920 preto.
3. Montar o vídeo com ffmpeg (slideshow com crossfade entre os slides).
4. Áudio entra depois, direto no Instagram na hora de postar — o vídeo sai mudo
   de propósito (evita problema de direito autoral e usa a trilha nativa do app).

## Specs de cor e formato (Bastidores, Reel 1080x1920)

| Elemento | Valor |
|---|---|
| Fundo | Preto puro `#000000` |
| Kicker | "INOVASHOT · BASTIDORES", Poppins Medium 30px, cor `#c8bedc` |
| Ponto do kicker | Roxo `#a855f7` |
| Barra gradiente | 90×8px, rosa→roxo→azul: `#f472b6 → #a855f7 → #38bdf8` |
| Título | Poppins Bold ~72px, branco `#ffffff`, alinhado à esquerda |
| Ghost number | Poppins Bold ~950px, branco a 10% de opacidade, canto inferior direito |
| Footer (banda) | Gradiente rosa→roxo→azul, blend 35% sobre preto, ~320px de altura |
| Handle | "@inovashot.cortes" Poppins Bold 46px, quase-branco `#ebe8f0` |
| Paginação | "0X/0Y" Poppins Medium 38px, **empilhada abaixo do handle** (nunca no canto inferior direito — ali ficam os ícones nativos do Instagram) |
| Kicker (posição) | `y=260`, não `y=90` — evita colidir com a UI nativa do topo do Instagram |

## Detalhe importante: número fantasma com largura variável
Números como "05" ou "08" são mais largos que "01". Se o tamanho da fonte for fixo,
o número pode estourar a borda esquerda do quadro. A função de desenho precisa
**reduzir o tamanho dinamicamente até caber** dentro da largura disponível
(margem direita ~40px, folga mínima na esquerda ~20px), em vez de usar um
tamanho fixo pra todos os números.

## Estrutura do script
- Fontes em `/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf` e
  `Poppins-Medium.ttf`
- Função de gradiente horizontal interpolando os 3 tons (rosa→roxo→azul)
- Função de wrap de texto pra quebrar linha automaticamente no título
- Uma função `make_slide()` que desenha, nessa ordem: ghost number (camada
  separada em escala de cinza, composta por cima do fundo) → footer band →
  kicker → barra gradiente → título → handle + paginação
- Salva cada slide como PNG

## Montagem do vídeo (ffmpeg)
- Slides de gancho/CTA (menos texto) ficam ~3s cada
- Slides com mais conteúdo pra ler ficam ~3.5s
- Transição: crossfade (`xfade=transition=fade`) de ~0.4s entre clipes
- Prints reais (screenshots) entram na mesma duração dos slides de texto, sem
  zoom ou efeito — eles já têm densidade visual suficiente
- Vídeo final sai sem áudio, `-pix_fmt yuv420p`, resolução 1080x1920

## Prints reais: como preparar
1. Cortar removendo status bar, barra de URL (opcional manter pra dar contexto
   de "isso é real") e teclado/toolbar do app
2. Redimensionar mantendo proporção pra 1080px de largura
3. Centralizar verticalmente num canvas 1080x1920 preto (não esticar)

## Erros já cometidos (não repetir)
- Gerar slide em 1080x1080 e colar centralizado num canvas 1080x1920: cria
  espaço preto igual em cima e embaixo, fazendo o rodapé flutuar no meio do
  quadro ("efeito pôster"). Sempre gerar nativo em 1080x1920.
- Usar tamanho de fonte fixo pro número fantasma sem checar a largura do
  texto: números com dígitos largos (5, 8) estouram a borda.
- Rodar ffmpeg em background com `&`: o processo morre quando o comando
  termina (cada chamada de bash é um shell novo). Sempre rodar em foreground.
- Usar `zoompan` em imagens grandes (1080x1920) com muitos frames: é lento e
  pode estourar o tempo limite de execução. Se quiser esse efeito, testar com
  duração menor por slide primeiro.
