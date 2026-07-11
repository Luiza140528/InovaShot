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
- SMTP: noreply.inovashot@gmail.com

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
- Módulo Político → aba Trends: erro ao clicar em "Buscar Tendências" (fix
  pendente)
- Relatos de bug "hook_score vs virality_score" de outro agente NÃO foram
  reproduzidos em teste ao vivo — tratar relatos assim com cautela, sempre
  reproduzir antes de assumir como verdade
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
