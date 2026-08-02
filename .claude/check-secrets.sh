#!/bin/bash
# check-secrets.sh
# Bloqueia commit se detectar padrões de token/API key/segredo no que está staged.
# Usado como hook do Claude Code antes de comandos "git commit".

PADROES_SUSPEITOS=(
  "AIza[0-9A-Za-z_-]{35}"          # Google API key
  "sk-ant-[a-zA-Z0-9_-]{20,}"      # Anthropic API key
  "sk-[a-zA-Z0-9]{20,}"            # OpenAI-style key
  "ghp_[a-zA-Z0-9]{30,}"           # GitHub personal access token
  "eyJ[a-zA-Z0-9_-]{10,}\.eyJ"     # JWT (ex: Supabase, Threads)
  "THREADS_ACCESS_TOKEN"
  "SUPABASE_SERVICE_ROLE"
  "-----BEGIN.*PRIVATE KEY-----"
)

ENCONTROU=0
DIFF=$(git diff --cached)

for PADRAO in "${PADROES_SUSPEITOS[@]}"; do
  if echo "$DIFF" | grep -qE "$PADRAO"; then
    echo "⚠️  BLOQUEADO: padrão suspeito de segredo encontrado ($PADRAO)"
    ENCONTROU=1
  fi
done

if [ "$ENCONTROU" -eq 1 ]; then
  echo ""
  echo "Commit bloqueado. Revise o diff com: git diff --cached"
  echo "Remova o segredo do código e use variável de ambiente (.env) em vez disso."
  exit 1
fi

exit 0
