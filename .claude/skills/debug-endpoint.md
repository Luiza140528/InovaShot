# Skill: Investigar Erro em Produção (InovaShot)

## Quando usar
Sempre que um endpoint da API do InovaShot (`/api/score-social`, `/api/tendencias`, ou qualquer outro) começar a
retornar erro, comportamento inesperado, ou lentidão em produção.

## Contexto fixo do ambiente
- Processo PM2: `inovashot` (modo fork)
- Gerenciador de processo: PM2 + Nginx
- Repo principal: `/app/inovashot`
- Stack: Node.js, hospedado em droplet DigitalOcean
- Pipeline de IA: Whisper → Claude Haiku → FFmpeg

## Passo a passo que o Claude Code deve seguir

1. **Puxar os logs recentes do processo:**
   ```
   pm2 logs inovashot --lines 200 --nostream
   ```
   Se o erro foi há mais tempo, usar também:
   ```
   pm2 logs inovashot --lines 1000 --nostream | grep -i error
   ```

2. **Checar status geral do processo:**
   ```
   pm2 describe inovashot
   pm2 list
   ```
   Ver se houve restart inesperado, uso de memória anormal, ou uptime baixo (indica crash loop).

3. **Ver se algo mudou recentemente no código:**
   ```
   cd /app/inovashot
   git log --oneline -10
   git diff HEAD~3 HEAD
   ```
   Cruzar o horário dos commits com o horário em que o erro começou.

4. **Checar configs relevantes se o erro parecer de infraestrutura:**
   - Nginx: `nginx -t` e `cat /etc/nginx/sites-enabled/inovashot` (ou nome do site)
   - Variáveis de ambiente: `pm2 env 0` (ou o id do processo)
   - Certificados/DNS se for erro 502/504

5. **Se for erro no pipeline de IA (score-social específico):**
   - Verificar se a chamada à API do Claude Haiku está retornando erro (rate limit, timeout, chave inválida)
   - Verificar se o FFmpeg está falhando por causa de arquivo de vídeo corrompido ou espaço em disco:
     ```
     df -h
     ```

6. **Reportar o diagnóstico**, sempre no formato:
   - **O que quebrou:** (endpoint, sintoma)
   - **Desde quando:** (horário aproximado, baseado nos logs)
   - **Causa mais provável:** (com trecho de log ou commit que sustenta a hipótese)
   - **Correção sugerida:** (não aplicar automaticamente — sugerir e esperar confirmação, seguindo a regra de nunca marcar como implementado sem verificação)

## Prompt de exemplo pra usar no Claude Code

> "O endpoint /api/score-social começou a dar erro 500 há cerca de uma hora. Segue a skill debug-endpoint.md:
> investiga os logs do PM2 do processo inovashot, os últimos commits do repo, e me diz a causa mais provável antes
> de sugerir qualquer correção."

## Regras de governança (herdadas do CLAUDE.md)
- Nunca aplicar fix automaticamente sem confirmação explícita da Luiza.
- Nunca marcar o problema como "resolvido" sem verificação real (rodar o endpoint de novo e confirmar 200).
- Se a causa envolver arquivos de tema/design (`.impeccable/`), NÃO alterar sem aprovação — só reportar.
