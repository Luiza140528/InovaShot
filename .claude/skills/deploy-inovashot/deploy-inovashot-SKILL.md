---
name: deploy-inovashot
description: "Use esta skill sempre que for fazer deploy de mudanças no backend do InovaShot (DigitalOcean, PM2, Nginx), ou quando a tarefa envolver commit e organização de mudanças no repositório (branch, stash). Cobre o fluxo padrão de commit → push → restart → verificação de logs, convenção de mensagens de commit, e gestão de stash pendente. Acionar quando o usuário disser 'faz o deploy', 'sobe pra produção', 'reinicia o servidor do InovaShot', 'commita isso' ou similar."
---

# Deploy do InovaShot (backend)

## Contexto do ambiente
- Repo: `Luiza140528/InovaShot`, branch `main-/-frontend`
- Servidor: DigitalOcean Droplet (Ubuntu), processo gerenciado via PM2, proxy Nginx
- Nome do processo PM2: `inovashot`

## Antes de iniciar qualquer tarefa nova: checar stash

```
git stash list
```

Se houver stash pendente, **nunca aplicar silenciosamente**. Perguntar à Luiza se deve ser:
- aplicado (`git stash pop` / `git stash apply`)
- descartado (`git stash drop`)
- deixado de lado por enquanto

Confirmar também a branch atual (`git branch --show-current`) antes de commitar, caso a tarefa pareça tocar backend vs frontend.

## Fluxo padrão de deploy (seguir nesta ordem, um passo por vez)

1. **Checar estado local antes de subir**
   ```
   git status
   git diff
   ```
   Confirmar que não sobrou nada sensível (tokens, .env) no diff antes de commitar. Rodar `check-secrets.sh` antes do commit quando presente no repo.

2. **Commit e push**
   ```
   git add <arquivos específicos, nunca add -A sem revisar>
   git commit -m "mensagem clara do que mudou e por quê"
   git push origin main-/-frontend
   ```
   Convenção de mensagem: curta e descritiva (ex: `fix: remoção de silêncio não cortava clipes com áudio baixo`).

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

## Ao concluir um bug que levou vários commits

No resumo final para a Luiza, referenciar o intervalo de commits (ex: `e497625→c9f80ca`), não só o commit final. Documentar causa raiz e fix em `learnings.md` do repo.

## Regras importantes
- Nunca reiniciar em produção sem antes rodar `pm2 logs` para confirmar que o processo estava saudável antes da mudança (baseline).
- Se `pm2 status` mostrar o processo em loop de restart (`↺` alto), parar e investigar antes de qualquer outra ação — não reiniciar de novo às cegas.
- Sempre que a mudança envolver `.env` ou segredos, confirmar que o arquivo `.env` de produção foi atualizado manualmente no servidor (não vai via git).
- Nunca commitar segredos — sempre rodar `check-secrets.sh` antes de commit quando o script estiver presente no repo.
- Se a tarefa for ambígua (ex: "corrige o bug" sem dizer qual), assumir a interpretação mais provável dado o contexto recente, avisar qual suposição foi feita, e seguir — só parar pra perguntar (uma pergunta por vez) se o risco de retrabalho for alto.
