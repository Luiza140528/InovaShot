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

## Opus Clip — pendente de pesquisa
Mencionado como concorrente de referência (fase 2, expansão EN) em
`.claude/skills/inovashot/SKILL.md`. Sem dados de pricing/features
levantados ainda.

## Klap — pendente de pesquisa
Mencionado como concorrente de referência (fase 2, expansão EN) em
`.claude/skills/inovashot/SKILL.md`. Sem dados de pricing/features
levantados ainda.
