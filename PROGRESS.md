# PROGRESS.md — Estado do loop de verificação do silence removal

## Status atual
CONCLUÍDO — silence removal NÃO está funcionando em produção. Causa raiz
identificada com evidência real (ver Execução 1 abaixo). Correção NÃO
aplicada (fora de escopo deste loop) — proposta registrada para aprovação
da Luiza.

## Histórico de execuções
<!-- Cada execução do loop adiciona uma entrada aqui, mais recente no topo -->

### Execução 1 — 2026-07-28
- Ação (Passo 1): Lido PROGRESS.md — status anterior era NÃO INICIADO, nenhum
  passo confirmado como concluído. Lido também learnings.md e
  verification-standard.md por instrução do Passo 2 (contexto prévio).
  IMPORTANTE: learnings.md já tinha uma entrada de 21/07 sobre este exato
  problema, com status "PARCIALMENTE RESOLVIDO" — confirmava que o código
  chama `removeSilence()` de fato, mas dizia explicitamente que faltava o
  teste funcional real (exatamente o que este loop precisa produzir).
- Ação (Passo 2 — localizar código): busca por "silence"/"ffmpeg"/"trim" em
  backend/src. Código localizado em `backend/src/server.js`:
  - `generateClip()` (linha 587-598) gera o clipe via ffmpeg e, na linha 597,
    chama `return await removeSilence(clipPath);` — confirma que a função É
    chamada no fluxo real (bate com o achado de learnings.md).
  - `removeSilence()` (linha 857-934): roda
    `ffmpeg -i <clip> -af silencedetect=noise=-30dB:d=0.6 -f null -` e
    captura o log via stderr/stdout da exceção (o comando com `-f null`
    sempre "falha" no execAsync, então o log vem de `e.stdout+e.stderr`).
    Extrai `silence_start`/`silence_end` via regex, calcula segmentos a
    manter (`keepSegments`, filtrando >0.15s), monta um
    `filter_complex` com `trim`+`atrim`+`concat` por segmento, e gera
    `<clip>_nosilence.mp4`. Tem fallback: se não detectar silêncio, se
    houver 0 ou >25 segmentos, ou se o arquivo de saída não existir, ou se
    QUALQUER exceção ocorrer no processo inteiro (try/catch envolvendo tudo),
    retorna o `clipPath` ORIGINAL sem remoção — silenciosamente (só loga,
    não propaga erro). Isso bate com o padrão de risco descrito em
    verification-standard.md ("nunca assumir que o FFmpeg fez o que deveria
    fazer" / "checar warnings silenciosos").
- Resultado: código encontrado e mapeado. Ainda NENHUM teste funcional real
  rodado (Passo 3 pendente).
- Próximo passo: Passo 3 — rodar teste real com vídeo curto contendo silêncio
  perceptível, capturar comando ffmpeg exato + log de silencedetect + duração
  entrada vs. saída, salvar em outputs/silencedetect_log_<data>.txt.

- Ação (Passo 3 — teste real): Não havia vídeo de teste no repo nem em
  outputs/, então foi gerado um vídeo sintético com FFmpeg
  (`sine`+`testsrc`, 10s), com silêncio DIGITAL REAL (volume=0, não apenas
  "quieto") em dois blocos: 2s-4s e 6s-8s. Áudio audível (tom 440Hz) nos
  blocos 0-2s, 4-6s, 8-10s. Vídeo salvo em outputs/silencedetect_test_INPUT.mp4.
  A função `removeSilence()` foi extraída VERBATIM de server.js:857-934
  (diff confirmado idêntico, sem alteração de nenhuma linha de lógica) para
  um harness Node isolado, evitando subir o Express/Supabase completo. O
  harness injeta apenas fs/execAsync/logger e chama a função exatamente
  como generateClip() faria, passando uma cópia do clipe de teste.
- Resultado (Passo 3): Harness rodado com sucesso. Log completo salvo em
  outputs/silencedetect_log_20260728_1314.txt e
  outputs/silencedetect_manual_run_full.log.
  - DURAÇÃO_ENTRADA: 10s
  - `starts`/`ends` extraídos pelo REGEX DO CÓDIGO dentro do harness: `[]`
    (vazio!) — apesar do silêncio existir de verdade no vídeo.
  - CAMINHO_RETORNADO: igual ao clipPath original (não gerou `_nosilence.mp4`)
  - DURAÇÃO_SAÍDA: 10s (idêntica à entrada)
  - outputs/silencedetect_test_INPUT.mp4 e
    outputs/silencedetect_test_OUTPUT_returned_by_removeSilence.mp4 são
    BYTE-A-BYTE IDÊNTICOS (`cmp` confirmou) — ou seja, `removeSilence()`
    devolveu o clipe SEM NENHUMA modificação.

- Ação (Passo 4 — verificar / causa raiz): Rodei o MESMO comando ffmpeg que
  o código usa (`ffmpeg -i clip -af silencedetect=noise=-30dB:d=0.6 -f null -
  2>&1`) manualmente contra o mesmo clipe. O log mostra claramente:
  `silence_start: 2.02014` / `silence_end: 4.01714` e `silence_start: 6.01397`
  / `silence_end: 8.01088` — FFmpeg DETECTA o silêncio corretamente.
  Porém o **EXIT_CODE do processo é 0** (sucesso), não erro.
  CAUSA RAIZ CONFIRMADA em server.js:862-870:
  ```js
  let silenceLog = '';
  try {
    await execAsync(`ffmpeg ... -f null - 2>&1`, { timeout: 60000 });
  } catch (e) {
    silenceLog = (e.stdout || '') + (e.stderr || '') + (e.message || '');
  }
  ```
  O código só captura `silenceLog` dentro do bloco `catch`, assumindo que o
  comando `ffmpeg ... -f null -` sempre "falha" (lança exceção) e que o log
  do silencedetect vem do `stderr`/`stdout` da exceção. Isso é falso: o
  filtro `silencedetect` do FFmpeg apenas escreve no stderr, sem afetar o
  exit code — o comando termina com sucesso (exit 0) sempre que o arquivo é
  válido. Como `execAsync` RESOLVE (não rejeita) nesse caso, o `catch` nunca
  roda, `silenceLog` permanece `''` (valor inicial), `starts.length` é
  sempre 0, e a função cai no `if (starts.length === 0) return clipPath;`
  — retornando o clipe original sem qualquer remoção de silêncio, SEMPRE,
  em qualquer vídeo real. É exatamente o padrão "erro silencioso" citado no
  Passo 4 do LOOP_INSTRUCTIONS.md e no verification-standard.md (seção 2).
  Esta é uma REGRESSÃO/BUG DE CÓDIGO, não um problema de ambiente/produção
  — vai reproduzir de forma idêntica em qualquer servidor.

## Evidências (critério de sucesso do TASK.md)
1. ✅ Log do FFmpeg silencedetect rodando em vídeo real de teste →
   outputs/silencedetect_manual_run_full.log
2. ✅ Timestamps de silêncio extraídos do log → silence_start/end em
   2.02s-4.02s e 6.01s-8.01s (batem com o silêncio real inserido no teste)
3. ✅ Duração de entrada vs. saída comparada → 10s vs. 10s (IGUAL, não
   menor → confirma que a remoção NÃO ocorre)
4. ✅ Clipe de teste processado ponta a ponta com output salvo em outputs/
   para inspeção manual → outputs/silencedetect_test_INPUT.mp4 e
   outputs/silencedetect_test_OUTPUT_returned_by_removeSilence.mp4
   (confirmados idênticos byte a byte via `cmp`)

## Conclusão (Passo 6)
Silence removal via FFmpeg **NÃO está funcionando** em produção. Não é uma
questão de "código não confirmado" (isso já tinha sido resolvido em
learnings.md, 21/07) — é um bug real e determinístico: a lógica de captura
do log do `silencedetect` depende de uma exceção que o FFmpeg nunca lança
nesse caso, então o log fica sempre vazio e a função sempre retorna o clipe
original sem cortes.

### Correção proposta (NÃO aplicada — fora de escopo deste loop; requer
aprovação da Luiza antes de mexer em server.js de produção)
Em vez de só capturar o log no `catch`, capturar o `stdout` também no
caminho de sucesso, ex:
```js
let silenceLog = '';
try {
  const { stdout, stderr } = await execAsync(
    `ffmpeg -i "${clipPath}" -af silencedetect=noise=${noiseThreshold}:d=${minSilenceDuration} -f null - 2>&1`,
    { timeout: 60000 }
  );
  silenceLog = (stdout || '') + (stderr || '');
} catch (e) {
  silenceLog = (e.stdout || '') + (e.stderr || '') + (e.message || '');
}
```

## Próximo passo
Nenhum passo adicional do loop é necessário — critério de sucesso do
TASK.md atingido (causa raiz encontrada com evidência real, não
inconclusiva). Próxima ação é humana: Luiza decidir se aprova a correção
proposta acima para ser aplicada e deployada em produção.

## Atualização — 28/07, após aprovação da Luiza
Correção aplicada em `backend/src/server.js` (apenas as 2 linhas descritas
acima — diff conferido, nenhuma outra lógica alterada). Reexecutei o
mesmo harness contra uma cópia nova do vídeo de teste sintético:
- DURAÇÃO_ENTRADA: 10s
- `silence_start`/`silence_end` agora SÃO capturados corretamente pelo
  código: `[2.02014, 6.01397]` / `[4.01714, 8.01088]`
- `keepSegments` calculado: 3 blocos (0-2.02s, 4.02-6.01s, 8.01-10s)
- Gerou de fato `clip_test_copy_nosilence.mp4` (antes nunca gerava)
- DURAÇÃO_SAÍDA: **6.03s** (menor que a entrada, bate com os 3 blocos de
  áudio audível restantes — confirma que o corte está correto, não só
  "algo mudou")
- Log completo: outputs/silencedetect_log_20260728_POSFIX.txt
- Vídeo de saída pós-correção salvo para inspeção manual:
  outputs/silencedetect_test_OUTPUT_APOS_CORRECAO.mp4

**Status final: RESOLVIDO.** Silence removal confirmado funcionando após a
correção, com teste ponta a ponta real (não suposição). Correção ainda
não deployada em produção (DigitalOcean) — isso é uma ação de deploy,
fora do escopo deste loop de diagnóstico/correção de código.
