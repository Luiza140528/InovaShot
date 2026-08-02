---
name: deploy-inovashot
description: "Use esta skill sempre que for fazer deploy de mudanças no backend do InovaShot (DigitalOcean, PM2, Nginx). Cobre o fluxo padrão de commit → push → restart → verificação de logs. Acionar quando o usuário disser 'faz o deploy', 'sobe pra produção', 'reinicia o servidor do InovaShot' ou similar."
---

# Deploy do InovaShot (backend)

## Contexto do ambiente
- Repo: `Luiza140528/InovaShot`, branch `main-/-frontend`
- Servidor: DigitalOcean Droplet (Ubuntu), processo gerenciado via PM2, proxy Nginx
- Nome do processo PM2: `inovashot`

## Fluxo padrão (seguir nesta ordem, um passo por vez)

1. **Checar estado local antes de subir**
   ```
   git status
   git diff
   ```
   Confirmar que não sobrou nada sensível (tokens, .env) no diff antes de commitar.

2. **Commit e push**
   ```
   git add <arquivos específicos, nunca add -A sem revisar>
   git commit -m "mensagem clara do que mudou"
   git push origin main-/-frontend
   ```

3. **No servidor: puxar a mudança**
   ```
   cd /caminho/do/repo
   git pull origin main-/-frontend
   ```

4. **Reiniciar o processo**
   ```
   pm2 restart inovashot
   ```

5. **Verificar saúde imediatamente após o restart**
   ```
   pm2 status
   curl -s localhost:PORTA/health
   ```

6. **Checar logs por erros nos primeiros minutos**
   ```
   pm2 logs inovashot --lines 50 --nostream
   ```
   Se a mudança for relacionada a algo específico (ex: Threads, silence removal), filtrar:
   ```
   pm2 logs inovashot --lines 50 --nostream | grep -i "termo relevante"
   ```

## Regras importantes
- Nunca reiniciar em produção sem antes rodar `pm2 logs` para confirmar que o processo estava saudável antes da mudança (baseline).
- Se `pm2 status` mostrar o processo em loop de restart (`↺` alto), parar e investigar antes de qualquer outra ação — não reiniciar de novo às cegas.
- Sempre que a mudança envolver `.env` ou segredos, confirmar que o arquivo `.env` de produção foi atualizado manualmente no servidor (não vai via git).
- Depois de deploy relacionado a bug corrigido, documentar a causa raiz e o fix em `learnings.md` do repo (padrão que já é seguido no InovaShot).
