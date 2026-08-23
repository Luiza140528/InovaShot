# Git Cheatsheet — InovaShot

Cola rápida pra usar direto no servidor via Termius. Copia e cola o comando quando precisar.

---

## 🆘 Emergência — desfazer coisa errada

### Recuperar commit "perdido" (depois de reset errado, checkout errado, etc.)
```
git reflog
```
Mostra o histórico de TUDO que você fez, mesmo o que parece ter sumido.
Acha a linha do commit que quer (ex: `HEAD@{2}`) e volta com:
```
git reset --hard HEAD@{2}
```

### Desfazer o último commit mas manter as alterações nos arquivos
```
git reset --soft HEAD~1
```

### Descartar TODAS as alterações não commitadas (cuidado, apaga mesmo)
```
git checkout -- .
```

---

## 📦 Guardar trabalho sem commitar

### Guardar mudanças temporariamente
```
git stash
```

### Trocar de branch, fazer outra coisa, e depois voltar com as mudanças guardadas
```
git stash pop
```

### Ver lista de tudo que tá guardado no stash
```
git stash list
```

---

## 🍒 Pegar um commit específico de outra branch

Útil quando você corrigiu um bug numa branch de teste e quer levar só aquele commit pra `main`, sem trazer o resto.

```
git log --oneline          # acha o hash do commit que quer
git checkout main
git cherry-pick <hash-do-commit>
```

---

## 🧹 Limpar histórico antes de subir (juntar commits tipo "fix", "fix2")

```
git rebase -i HEAD~5
```
Abre uma lista dos últimos 5 commits. Troca `pick` por `squash` (ou `s`) nos que quer juntar no de cima, salva, e o Git pede pra escrever uma mensagem final única.

⚠️ Só faz isso em commits que **ainda não subiu** pro GitHub (senão bagunça quem já puxou).

---

## 🔍 Achar qual commit quebrou o sistema

```
git bisect start
git bisect bad                # a versão atual tá com bug
git bisect good <hash-antigo> # essa versão antiga funcionava
```
O Git vai te levando por commits no meio pra você testar, até achar o exato commit que quebrou.
Quando terminar:
```
git bisect reset
```

---

## 📋 Comandos do dia a dia (referência)

| Comando | O que faz |
|---|---|
| `git status` | Ver o que mudou |
| `git diff` | Ver as diferenças linha a linha |
| `git log --oneline` | Histórico resumido |
| `git branch` | Listar branches |
| `git checkout -b nome-branch` | Criar e trocar pra branch nova |
| `git add .` | Adicionar tudo pra commit |
| `git commit -m "mensagem"` | Commitar |
| `git push` | Subir pro GitHub |
| `git pull` | Baixar atualizações |

---

*Dica: se travar em qualquer coisa, roda `git status` primeiro — quase sempre ele já te diz o próximo passo.*
