# Prompts Adaptados — InovaShot (Claude Code)

Baseado no carrossel @coding_dev_ (8 Vibe Coding Prompts). Adaptado pro contexto do servidor DigitalOcean + PM2/Nginx + stack InovaShot (Whisper, Claude Haiku, FFmpeg).

---

## Prompt de Debug Rápido

Usar sempre que um bug aparecer (upload, geração de clipe, posts automáticos, etc.) — evita o loop "tenta isso... não espera, tenta aquilo" que gasta tokens à toa.

```
Tenho um bug no InovaShot. NÃO escreva nenhum fix ainda.

Erro / comportamento inesperado: [COLAR O ERRO OU LOG]
O que eu esperava: [DESCREVER]
O que realmente acontece: [DESCREVER]
Código relevante: [COLAR OU APONTAR ARQUIVOS — ex: server.js, nginx.conf, removeSilence()]
Componente afetado: [Whisper / Claude Haiku / FFmpeg / Nginx / PM2 / Threads API / outro]
O que eu já tentei: [LISTAR]

Passo 1: Reafirme o problema com suas próprias palavras, pra eu confirmar que entendeu certo.
Passo 2: Liste de 3 a 5 causas mais prováveis, ranqueadas por probabilidade, cada uma com sua justificativa.
Passo 3: Para cada causa, me dê a forma mais rápida de confirmar ou eliminar — uma linha de log, um comando, um teste rápido.
Passo 4: Pare e espere meus resultados.
Passo 5: Só depois de confirmarmos a causa, escreva o fix mínimo, explique por que funciona, e diga exatamente o que testar pra verificar.

Não faça mudanças "de tiro no escuro". Não refatore código sem relação com o bug.
Não corrija coisas que eu não pedi.
```

---

## Prompt para Transformar Tarefa em Skill

Usar depois de resolver algo junto com o Claude Code que provavelmente vai se repetir (ex: publicar carrossel, investigar timeout de upload, corrigir bug de silêncio, etc.) — assim vira uma skill documentada em vez de reexplicar toda vez.

```
Acabamos de terminar uma tarefa juntos no InovaShot.
Transforme isso em uma Skill reutilizável, pra eu nunca mais precisar reexplicar.

A tarefa: [DESCREVER, OU DIZER "o que acabamos de fazer"]

Produza:
1. Nome — curto, orientado à ação
2. Descrição — gatilho preciso: exatamente quando essa Skill deve e não deve ser usada,
   incluindo frases que eu realmente diria. Específico o bastante pra disparar sempre que
   for o caso e nunca disparar em tarefas sem relação.
3. Instruções — numeradas, passo a passo, escritas para um modelo sem contexto prévio.
   Incluir o que checar primeiro (ex: client_body_timeout E proxy_*_timeout juntos),
   o que me perguntar, e em que ordem fazer as coisas.
4. Regras e restrições — exigências obrigatórias e o que nunca deve acontecer
   (ex: nunca reproduzir credenciais em texto claro, sempre testar com netlify dev antes
   de push, sempre entregar arquivo completo corrigido).
5. Formato de saída — exatamente como o resultado deve ficar, com um modelo.
6. Exemplo completo — um caso de entrada até saída.
7. Modos de falha — as 3-5 formas mais comuns disso dar errado e como evitar cada uma.

Escreva de forma standalone. Assuma que quem for ler não sabe nada sobre o projeto InovaShot.
```

---

## O padrão por trás dos dois

- **Atribui um papel** implícito (engenheiro depurando, redator de skill)
- **Força uma pausa** — diagnosticar antes de corrigir, confirmar antes de escrever a skill
- **Define a saída exata** — sem adivinhação, formato claro do começo ao fim
