# InovaShot

**SaaS de cortes de vídeo com IA para criadores de conteúdo brasileiros.**

InovaShot transforma vídeos longos em clipes verticais de alta retenção, prontos para publicação, com inteligência artificial aplicada a cada etapa do processo — da transcrição à decisão de qual trecho tem maior potencial de viralização.

---

## Visão Geral do Produto

O InovaShot recebe vídeos longos — importados via proxy do YouTube, podcasts ou gravações de lives — e os converte automaticamente em múltiplos cortes verticais (9:16), otimizados para distribuição em TikTok, Instagram Reels e YouTube Shorts.

O sistema não realiza apenas o recorte técnico do vídeo. Ele analisa o conteúdo da transcrição para identificar os trechos com maior probabilidade de retenção e engajamento, entregando ao usuário não só o clipe pronto, mas também contexto estratégico sobre por que aquele corte tem potencial — incluindo pontuação de viralidade, variações de hook e sugestão de estratégia de postagem.

O produto é horizontal por natureza — atende qualquer criador de conteúdo, independentemente do nicho — mas mantém um módulo vertical dedicado à comunicação política, funcionando como principal porta de entrada durante o ciclo eleitoral.

---

## Arquitetura e Tech Stack

**Backend**
- Node.js (`server.js`) em produção
- Hospedagem em DigitalOcean, com gerenciamento de processos via PM2
- Nginx como proxy reverso

**Inteligência Artificial**
- Transcrição de áudio via Whisper
- Análise de conteúdo, geração de hooks e pontuação de viralidade via Claude Haiku (Anthropic)

**Infraestrutura de Vídeo**
- Ingestão de vídeos do YouTube via proxy dedicado (Webshare)
- Upload direto de galeria
- Autenticação via login Google

**Pagamentos**
- Integração com Mercado Pago (Pix e cartão)

---

## Recursos Confirmados

- **Nota de Viralidade (0–10):** pontuação gerada por IA para cada clipe, indicando potencial de retenção e engajamento
- **Hook A/B:** geração de variações de abertura para teste de performance do mesmo clipe
- **Legendas animadas em PT-BR:** sincronização automática de legendas, adaptadas ao ritmo da fala
- **Estratégia de postagem por clipe:** cada corte gerado inclui recomendação de abordagem para publicação
- **Módulo Político:** conjunto de ferramentas dedicado a candidatos e assessorias de campanha, incluindo:
  - **Perfil:** cadastro de dados do candidato (nome, número eleitoral, partido, cargo, cidade/UF)
  - **Jurídico:** monitoramento de termos sensíveis na transcrição, com alertas de conformidade
  - **Memória:** organização de clipes por eixo temático (Saúde, Educação, Segurança)
  - **Trends:** identificação de tendências de discurso político relevantes ao contexto do candidato
  - **Propostas:** estrutura para comunicação de propostas de governo, com suporte a material pré-venda
  - **S.O.S.:** fluxo de resposta rápida para emergências de campanha

---

## Diretrizes de Segurança

Todas as credenciais de ambiente (`.env`) e tokens de integração com APIs externas — incluindo Anthropic, OpenAI e Mercado Pago — são armazenados e utilizados exclusivamente no servidor de produção.

Nenhuma chave de API, token de autenticação ou client secret é exposto no front-end em nenhuma circunstância. Toda comunicação com serviços de terceiros que dependa de credenciais sensíveis é intermediada por rotas backend dedicadas, garantindo isolamento completo entre cliente e infraestrutura de segredos.

---

**InovaShot** — inovashot.com.br
