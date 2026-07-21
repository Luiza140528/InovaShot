# Verification Standard

Este arquivo define o que significa "está pronto" antes de qualquer tarefa
ser considerada concluída. O agente (Claude Code) deve consultar este
arquivo antes de reportar sucesso.

## Regra geral

Nenhuma tarefa é considerada "feita" só porque o código foi escrito ou o
deploy rodou sem erro aparente. "Feito" = testado de forma que prova que o
comportamento esperado realmente acontece.

## Critérios de aceitação por tipo de mudança

### 1. Integração com API externa (ex: Facebook, Threads, Mercado Pago, RapidAPI)
- [ ] Chamada real feita contra o ambiente de produção ou sandbox (não só
      leitura do código)
- [ ] Resposta da API inspecionada (status code + corpo), não assumida
- [ ] Testado o caminho de erro (o que acontece se a API cair, token
      expirar, rate limit bater)
- [ ] Se envolve variável de ambiente nova, confirmar que ela existe no
      .env do servidor de produção (ex: DigitalOcean), não só localmente

### 2. Processamento de mídia (ex: FFmpeg, remoção de silêncio, cortes)
- [ ] Rodado contra um arquivo de vídeo real, não só "o código parece
      certo"
- [ ] Output final verificado (duração, presença/ausência do que deveria
      ser removido) — nunca assumir que o FFmpeg fez o que o comando diz
      que deveria fazer
- [ ] Logs do processo checados por warnings silenciosos

### 3. Frontend / botão / fluxo de usuário
- [ ] Clicado de verdade (ou simulado via teste) do início ao fim
- [ ] Erros de rede/console verificados, não só a UI "parece" carregar
- [ ] Se a função depende de chamada direta a uma API (ex: Anthropic) a
      partir do navegador, confirmar que há autenticação/proxy backend —
      chamada direta do frontend sem headers de auth é erro recorrente
      aqui (ver learnings.md)

### 4. Deploy / infraestrutura
- [ ] `netlify dev` (ou equivalente local) rodado antes de qualquer
      deploy — nunca subir direto
- [ ] Após deploy, endpoint/página real acessada e resultado conferido
- [ ] Nenhuma credencial em texto plano commitada (checar diff antes do
      commit)

## Protocolo: Investigar → Planejar → Implementar → Verificar

1. **Investigar**: ler o código/log relevante antes de propor solução.
   Nunca supor causa raiz sem checar.
2. **Planejar**: escrever em 2-3 linhas o que vai ser feito e por quê,
   antes de editar arquivos.
3. **Implementar**: fazer a mudança mínima necessária. Entregar arquivo
   completo, nunca trecho solto.
4. **Verificar**: rodar o critério de aceitação correspondente acima.
   Só reportar "concluído" depois disso passar.

## Quando o agente encontra um erro

- Nível 1 (mínimo): logar o erro e alertar (ex: WhatsApp) — nunca falhar
  silenciosamente.
- Nível 2: tentar autocorreção dentro de limites definidos (ex: retry,
  fallback de API).
- Nível 3: registrar o padrão em `learnings.md` para não repetir, e só
  então considerar ajuste de arquitetura — nunca mudar arquitetura sem
  registrar o aprendizado primeiro.

## Antes de reportar "concluído" para a Luiza

- [ ] O critério de aceitação relevante foi executado (não só assumido)
- [ ] Se havia incerteza, ela foi sinalizada explicitamente
- [ ] Nenhuma credencial aparece em texto plano na resposta
