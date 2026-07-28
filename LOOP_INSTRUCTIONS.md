# LOOP_INSTRUCTIONS.md — Como o Claude deve operar este loop

## Passo 1 — Ler estado
Antes de qualquer ação, ler PROGRESS.md para saber em que ponto a
investigação parou na última execução. Nunca repetir um passo já
confirmado como concluído lá.

## Passo 2 — Localizar o código
Buscar no repo (Luiza140528/InovaShot, branch main-/-frontend) pelos
arquivos responsáveis pelo silence removal (provavelmente algo com
"silence", "ffmpeg" ou "trim" no nome). Registrar o caminho exato em
PROGRESS.md.

## Passo 3 — Rodar um teste real
Pegar um vídeo de teste curto (ou baixar um de exemplo com silêncio
perceptível), rodar o pipeline de processamento local ou no servidor,
e capturar:
- O comando FFmpeg exato que foi executado
- O log completo do `silencedetect`
- Duração de entrada vs. duração de saída

Salvar esse log em outputs/silencedetect_log_<data>.txt

## Passo 4 — Verificar
Comparar duração de entrada e saída.
- Se a saída for igual ou maior → silence removal NÃO está funcionando.
  Investigar se a função está sendo chamada, se o filtro está sendo
  aplicado no comando final de export, ou se há erro silencioso (try/except
  engolindo falha).
- Se a saída for menor e os timestamps batem com os cortes esperados →
  está funcionando. Documentar isso como confirmado.

## Passo 5 — Registrar progresso
Atualizar PROGRESS.md com:
- Data/hora da execução
- O que foi verificado
- Resultado (funciona / não funciona / inconclusivo)
- Próximo passo, se houver

## Passo 6 — Decidir o próximo ciclo
- Se resolvido → marcar TASK.md como concluído e parar o loop.
- Se não resolvido e ainda dentro do limite de tentativas → repetir a partir
  do Passo 3 com um ajuste (ex: outro vídeo de teste, outro ponto do código).
- Se travado → escalar para Luiza conforme critério em TASK.md.

## Regras de segurança
- Nunca alterar código em produção sem confirmação explícita da Luiza.
- Nunca commitar direto na branch principal — sempre propor o diff primeiro.
- Nunca expor tokens/segredos (Threads app secret, etc) em logs ou outputs.
