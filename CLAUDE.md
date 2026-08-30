# InovaShot — Contexto do Projeto

## O que é
InovaShot (inovashot.com.br) é uma ferramenta de IA para cortar vídeos, voltada
para criadores de conteúdo brasileiros. Posicionamento: "InovaShot corta o vídeo,
você decide o que vale a pena publicar."

## Regra de marca (OBRIGATÓRIA)
- **Nunca usar "IA" como sujeito da frase** em nenhum conteúdo, copy, UI ou
  comunicação (ex: evitar "a IA corta seu vídeo" → preferir "o InovaShot corta
  seu vídeo" ou construções que tirem IA do papel de agente).
- Essa regra vale para todo texto voltado ao usuário final: site, app, posts,
  e-mails transacionais, mensagens de erro.

## Stack técnico
- Backend: Node/Express, PM2, Nginx (DigitalOcean)
- Banco: Supabase
- Transcrição: Whisper
- IA de conteúdo: Claude Haiku
- Pagamentos: Mercado Pago
- Fila de jobs: BullMQ + Redis (em modo shadow/observação)
- Auth: Google OAuth configurado
- Download de vídeo: YouTube via proxy residencial Webshare (resolve bloqueio
  de IP datacenter)
- Frontend: GitHub Pages, branch `main-/-frontend`, repo `Luiza140528/InovaShot`
- SMTP: noreply@inovashot.com.br

## Configurações importantes já ajustadas
- Nginx `client_body_timeout` em 300s (resolveu falha de upload em galeria)
- Remoção de silêncio via FFmpeg implementada
- `.gitignore` configurado — NUNCA commitar `.env`. Se um `.env` for staged
  por engano, rotacionar credenciais imediatamente.

## Pricing atual
- Free
- Starter: R$49,90
- Pro: R$97,90
- Elite: R$197,90

## Bugs conhecidos / pendências
- ~~Módulo Político → aba Trends: erro ao clicar em "Buscar Tendências"~~ —
  **RESOLVIDO** (confirmado em teste em 11/07/2026). Se voltar a falhar,
  reabrir como pendência com detalhes do erro.
- Relatos de bug "hook_score vs virality_score" de outro agente NÃO foram
  reproduzidos em teste ao vivo — tratar relatos assim com cautela, sempre
  reproduzir antes de assumir como verdade
- ~~Script gerador do carrossel claro (template "Radar Claude") vivia só num
  scratchpad de sessão temporário, fora do repo~~ — **RESOLVIDO** (30/08/2026).
  Movido pra `scripts/gen-carousel-light.py` + `scripts/fonts/`, com paths
  relativos ao próprio arquivo (antes apontavam pra diretório de sessão).
  Reexecução verificada byte-a-byte idêntica ao output anterior.
- ~~Linha do rodapé do carrossel claro saía 100% opaca em vez de
  translúcida~~ — **RESOLVIDO** (30/08/2026). `img.convert("RGB")` no save
  descartava o canal alfa sem compor contra o fundo; corrigido compondo a
  linha numa camada RGBA separada antes de salvar. Confirmado por leitura
  de pixel (antes `(26,26,24)` puro, depois blend correto ~27% opacidade).
- ~~Frase-gradiente do headline podia vazar pra fora da margem em textos
  longos~~ — **RESOLVIDO** (30/08/2026). `fit_headline()` só checava altura
  e número de linhas, nunca a largura do token individual; agora também
  exige que o token mais largo caiba em `max_width`, encolhendo a fonte
  além do mínimo normal só nesse cenário de emergência. Testado com frase
  artificial de ~70 caracteres que antes vazava.
- ~~Conteúdo dos slides do carrossel claro hardcoded dentro do motor de
  renderização~~ — **RESOLVIDO** (30/08/2026). Copy movida pra
  `scripts/carousel-content/radar-claude.json`; script aceita
  `[content.json] [out_dir]` opcionais e mantém os defaults atuais. Sem
  regressão nos 6 slides já publicados.

**Regra de manutenção desta seção:** sempre que um bug for corrigido e
confirmado por teste, mover para "resolvido" com a data. Sempre que um bug
novo for identificado, adicionar aqui imediatamente. Este arquivo é a fonte
única de verdade sobre o estado do projeto — deve ser atualizado a cada
sessão relevante, não só revisado esporadicamente.
- Anthropic API key pode desaparecer das variáveis do Railway após redeploy
  em outros projetos da Luiza — se acontecer aqui, checar se dotenv está
  sendo usado em produção (não deveria)

## Marketing / distribuição
- Agente de marketing "Eco" (configurado como Claude Project separado) cuida
  de conteúdo e distribuição
- Canais: Instagram @inovashot.cortes, TikTok @inovashot.corte, Facebook page
- Formato de conteúdo: pillar → slice (peça principal vira vários cortes pra
  carrossel/reels)
- Conteúdo otimizado pra GEO/AEO (guias numerados)
- Blog publicado via GitHub Pages + perfil no Medium (canonical do Medium
  ainda pendente de configurar)

## Como a Luiza trabalha
- Constrói e gerencia tudo pelo celular Android
- É cuidadora familiar (Dona Niza), o que limita o tempo disponível — prefira
  respostas diretas, objetivas e acionáveis, sem enrolação
- Prefere que eu já resolva/implemente em vez de só explicar o que fazer
- ## Protocolo de auto-otimização

Antes de qualquer tarefa não-trivial, siga este protocolo:

1. **Investigar**: consulte `learnings.md` primeiro — o problema pode já
   ter sido visto antes.
2. **Planejar**: descreva em poucas linhas o que vai fazer.
3. **Implementar**: mudança mínima, arquivo completo (nunca trecho
   solto).
4. **Verificar**: rode os critérios de `verification-standard.md`
   correspondentes ao tipo de mudança antes de reportar como concluído.

Sempre que encontrar um erro, resolver um bug ou descobrir uma causa raiz
não óbvia, registre em `learnings.md` no formato definido no próprio
arquivo — isso vale tanto para sucessos quanto para tentativas que não
funcionaram.

Nunca marque uma feature como "implementada" ou "funcionando" sem
verificação real (ver verification-standard.md). "O código parece
correto" não é critério de aceitação.

Referências:
- @verification-standard.md
- @learnings.md

## Gestão de tokens (economia de contexto)

- /clear ao trocar de assunto — zera contexto, evita releitura cara do histórico velho.
- /compact quando a sessão fica longa — resume sem apagar, corta ~28k pra ~4k tokens.
- Escolher modelo pela tarefa, não usar o mais caro por padrão:
  - Haiku -> tarefa simples/rapida (parsing, checagem de status)
  - Sonnet -> dia a dia, melhor custo-beneficio (grosso da manutencao do InovaShot)
  - Opus -> raciocinio complexo/decisao dificil (arquitetura, debug pesado)
  - Fable 5 -> trabalho pesado, mais caro
- Juntar pedidos numa mensagem so em vez de mandar em pedacos — evita releitura multipla do mesmo historico.

## Simplicidade e Impacto Mínimo
- Preferir sempre a solução mais simples que resolve o problema — evitar over-engineering.
- Mexer apenas no que é necessário para a tarefa pedida; não refatorar código não solicitado.
- Nunca aplicar fix temporário/gambiarra sem avisar explicitamente que é temporário e qual é a solução definitiva pendente.
- Antes de entregar mudança não-trivial, perguntar: "essa é a forma mais elegante e simples de resolver isso?"

## Início de sessão
- No início de cada sessão nova, revisar `learnings.md` antes de começar qualquer tarefa — o problema pode já ter sido resolvido ou documentado antes.

## Início de tarefa: ler contexto antes de executar

Antes de implementar qualquer tarefa nova (código, copy, design, conteúdo
de marketing), sempre:

1. Ler completamente os arquivos de contexto relevantes antes de escrever
   qualquer linha — não apenas escanear:
   - CLAUDE.md (este arquivo)
   - DESIGN.md (paleta, tipografia, tom visual)
   - learnings.md (erros já resolvidos, não repetir)
   - verification-standard.md (critério de "pronto")
   - Se for conteúdo/copy: regras de copy do projeto (nunca usar "IA",
     sempre "InovaShot")

2. NÃO começar a implementar ainda. Se algo estiver ambíguo — estilo,
   escopo, prioridade, decisão de design — perguntar antes de executar.
   Preferir uma pergunta objetiva a uma suposição errada.

3. Só depois de alinhado (ou se não houver ambiguidade), implementar.

Isso evita retrabalho por assumir cor/tom/estilo errado e só descobrir
depois de pronto.
