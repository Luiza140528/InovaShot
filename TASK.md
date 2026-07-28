# TASK.md — Verificação do Silence Removal (InovaShot)

## Objetivo
Confirmar, com evidência real (não suposição), se a remoção de silêncio via
FFmpeg `silencedetect` está de fato funcionando no pipeline de processamento
de vídeo do InovaShot em produção.

## Contexto do problema
- O código de silence removal está documentado como implementado
  (verification-standard.md / learnings.md do repo).
- Existe suspeita de que ele NÃO está funcionando de verdade — nunca foi
  validado com prova concreta (antes/depois do vídeo, log do FFmpeg, etc).
- Repo: Luiza140528/InovaShot, branch main-/-frontend
- Backend: DigitalOcean (Ubuntu, PM2, Nginx)

## Critério de sucesso (o que conta como "resolvido")
O loop só pode marcar a task como concluída se produzir TODAS as evidências abaixo:
1. Log do comando FFmpeg `silencedetect` rodando em um vídeo real de teste
2. Timestamps de silêncio detectados (início/fim) extraídos do log
3. Duração do vídeo de saída comparada com a duração do vídeo de entrada
   (se o silêncio foi cortado, a saída deve ser mais curta)
4. Um clipe de teste processado ponta a ponta, com o arquivo de saída salvo
   em outputs/ para inspeção manual

## Fora de escopo
- Não mexer em outras partes do pipeline (virality score, legendas, publicação)
- Não fazer deploy de correção automaticamente — só diagnosticar e propor

## Escalar para humano (Luiza) quando:
- O código do silence removal não for encontrado no repo
- A correção exigir mudar dependências do servidor (ex: reinstalar FFmpeg)
- Após 5 tentativas de execução, a causa raiz não estiver clara
