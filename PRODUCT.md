# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: criadores de conteúdo brasileiros que produzem vídeo longo (YouTube,
lives, podcasts) e precisam de cortes verticais (Shorts/Reels/TikTok) rápido,
sem tempo ou equipe de edição — operando muitas vezes sozinhos, do celular.

Secundário (confirmado): assessores de campanha e candidatos políticos, que
usam o Módulo Político do app para cortar discursos e conteúdo de campanha —
job diferente do criador de conteúdo geral (recorte de fala política/discurso,
não conteúdo de entretenimento), servido por uma aba dedicada (Trends/busca de
tendências).

## Product Purpose

Transformar vídeo longo (link do YouTube ou upload da galeria) em clipes
verticais prontos — cortados, legendados e entregues — em até 5 minutos, sem
exigir habilidade de edição do usuário. Sucesso = clipe pronto pra publicar
rápido o bastante pra manter o ritmo de postagem de um criador solo.

## Positioning

"InovaShot corta o vídeo, você decide o que vale a pena publicar." O produto
automatiza o corte/legendagem, mas a curadoria final (o que publicar) fica
explicitamente com o usuário — não é apresentado como decisão autônoma da
ferramenta. Ver regra de marca em Brand Commitments.

## Operating Context

- Fluxo principal: colar link do YouTube (via proxy residencial, contorna
  bloqueio de IP datacenter) ou enviar vídeo da galeria → processamento →
  clipes 9:16 com legenda em até 5 minutos.
- Usuária/fundadora opera o produto inteiro pelo celular Android.
- Distribuição de conteúdo próprio (marketing) segue padrão pillar→slice:
  peça principal do blog vira vários cortes pra carrossel/reels, publicados
  via agente de marketing "Eco".
- Módulo Político roda como fluxo separado dentro do mesmo app (aba Trends).

## Capabilities and Constraints

- Transcrição via Whisper; geração de conteúdo/curadoria via Claude Haiku.
- Remoção de silêncio via FFmpeg (confirmada por teste real, ver
  learnings.md).
- Pagamento via Mercado Pago; auth via Google OAuth.
- Fila de jobs BullMQ + Redis em modo shadow/observação (não é ainda o
  caminho principal de processamento).
- Backend Node/Express em DigitalOcean (PM2 + Nginx); frontend estático
  publicado via GitHub Pages.
- Terminologia de marca: nunca usar "IA" como sujeito da frase em texto
  voltado ao usuário final (site, app, e-mails, mensagens de erro) — ver
  Brand Commitments.

## Brand Commitments

- Nome: InovaShot (inovashot.com.br).
- Regra obrigatória de marca: nunca "a IA corta seu vídeo" — sempre "o
  InovaShot corta seu vídeo" ou construção que tire "IA" do papel de agente
  da frase. Vale para todo texto voltado ao usuário final.
- Canais de marketing: Instagram @inovashot.cortes, TikTok
  @inovashot.corte, Facebook page. Conteúdo otimizado pra GEO/AEO (guias
  numerados).

## Evidence on Hand

Nenhuma prova social pública ainda (sem depoimentos, números de usuários ou
cobertura de imprensa publicáveis confirmados). Não inventar testemunhos,
cases ou métricas de uso em trabalho futuro até que a Luiza forneça algo
real.

## Product Principles

1. Curadoria final é sempre do usuário — a ferramenta corta, o humano decide
   o que publicar. Isso é regra de marca e de produto, não só copy.
2. Velocidade e simplicidade pra operação solo: o fluxo (link/upload → clipe
   pronto) precisa caber no tempo e atenção de alguém sem equipe de edição
   nem, muitas vezes, mais que o celular na mão.
3. Dois públicos com jobs diferentes sob o mesmo produto: criador de
   conteúdo geral e campanha política — não assumir que UX/linguagem pensada
   pra um serve automaticamente pro outro.
4. Sem prova social ainda: não fabricar depoimentos, números ou cases em
   nenhuma peça (site, marketing, produto) até que existam de verdade.

## Accessibility & Inclusion

Nenhum requisito de acessibilidade específico do produto foi estabelecido
ainda.
