/**
 * claude-news-daily.js
 *
 * Busca novidades recentes da Claude/Anthropic, gera um post em português
 * e publica automaticamente no Threads.
 *
 * VARIÁVEIS DE AMBIENTE NECESSÁRIAS (nunca coloque valores direto no código):
 *   ANTHROPIC_API_KEY     - sua chave da API da Anthropic
 *   THREADS_ACCESS_TOKEN  - token de acesso do Threads (o mesmo que você já usa)
 *   THREADS_USER_ID       - seu ID de usuário no Threads
 *
 * Requer Node 18+ (fetch nativo).
 *
 * Uso manual:   node claude-news-daily.js
 * Uso via cron: 0 9 * * * cd /caminho/do/projeto && node claude-news-daily.js >> logs/claude-news.log 2>&1
 */

const fs = require("fs");
const path = require("path");

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const THREADS_ACCESS_TOKEN = process.env.THREADS_ACCESS_TOKEN;
const THREADS_USER_ID = process.env.THREADS_USER_ID;

const STATE_FILE = path.join(__dirname, "claude-news-state.json");
const MODEL = "claude-haiku-4-5-20251001";

function checkEnv() {
  const missing = [];
  if (!ANTHROPIC_API_KEY) missing.push("ANTHROPIC_API_KEY");
  if (!THREADS_ACCESS_TOKEN) missing.push("THREADS_ACCESS_TOKEN");
  if (!THREADS_USER_ID) missing.push("THREADS_USER_ID");
  if (missing.length) {
    console.error(`Faltando variáveis de ambiente: ${missing.join(", ")}`);
    process.exit(1);
  }
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, "utf8"));
  } catch {
    return { lastHeadline: null, lastRunDate: null };
  }
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

/**
 * Passo 1: pede pro Claude pesquisar novidades recentes da Anthropic/Claude
 * usando a ferramenta de web search.
 */
async function buscarNovidades() {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 1000,
      tools: [{ type: "web_search_20250305", name: "web_search" }],
      messages: [
        {
          role: "user",
          content:
            "Pesquise as notícias/lançamentos mais recentes (últimas 24-48h) sobre a Anthropic ou o Claude " +
            "(novos modelos, features, mudanças de produto, blog posts oficiais). " +
            "Responda em português, em formato de lista curta com: título da novidade, uma frase resumindo, e a fonte (URL). " +
            "Se não houver nada relevante nas últimas 48h, responda exatamente: SEM_NOVIDADES",
        },
      ],
    }),
  });

  if (!res.ok) {
    throw new Error(`Erro na busca de novidades: ${res.status} ${await res.text()}`);
  }

  const data = await res.json();
  const texto = data.content
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("\n")
    .trim();

  return texto;
}

/**
 * Passo 2: transforma o resumo de novidades em um post pronto pro Threads.
 */
async function gerarPost(resumoNovidades) {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 500,
      messages: [
        {
          role: "user",
          content:
            `Com base nestas novidades da Anthropic/Claude:\n\n${resumoNovidades}\n\n` +
            "Escreva um post curto em português para o Threads (máx. 500 caracteres) que conecte essa novidade " +
            "com o InovaShot (plataforma brasileira de geração automática de clips virais com IA, que usa Claude " +
            "no seu pipeline). Regras obrigatórias de marca:\n" +
            "- 'O InovaShot' é sempre o sujeito ativo das frases sobre o produto (nunca dizer 'a IA faz X', dizer 'o InovaShot faz X').\n" +
            "- Tom direto, sem enrolação, com uma leitura/opinião de fundadora técnica sobre o que a novidade muda na prática " +
            "(ex: pra criadores de conteúdo, pra quem edita vídeo, etc.) — não é só notícia repassada.\n" +
            "- Sem hashtags excessivas (no máx. 2-3 relevantes no final), sem emojis em excesso.\n" +
            "- Terminar o post com uma chamada curta e natural convidando a seguir o InovaShot pra acompanhar as novidades " +
            "da Claude/IA todos os dias (varie a frase a cada post, não repita sempre a mesma — evite soar robótico ou spam).\n" +
            "Responda APENAS com o texto final do post, sem aspas, sem explicações.",
        },
      ],
    }),
  });

  if (!res.ok) {
    throw new Error(`Erro ao gerar post: ${res.status} ${await res.text()}`);
  }

  const data = await res.json();
  return data.content
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("\n")
    .trim();
}

/**
 * Passo 3: publica no Threads (fluxo padrão: criar container -> publicar).
 */
async function publicarNoThreads(texto) {
  const criarUrl = `https://graph.threads.net/v1.0/${THREADS_USER_ID}/threads?media_type=TEXT&text=${encodeURIComponent(
    texto
  )}&access_token=${THREADS_ACCESS_TOKEN}`;

  const criarRes = await fetch(criarUrl, { method: "POST" });
  const criarData = await criarRes.json();

  if (!criarRes.ok || !criarData.id) {
    throw new Error(`Erro ao criar container no Threads: ${JSON.stringify(criarData)}`);
  }

  const publicarUrl = `https://graph.threads.net/v1.0/${THREADS_USER_ID}/threads_publish?creation_id=${criarData.id}&access_token=${THREADS_ACCESS_TOKEN}`;
  const publicarRes = await fetch(publicarUrl, { method: "POST" });
  const publicarData = await publicarRes.json();

  if (!publicarRes.ok) {
    throw new Error(`Erro ao publicar no Threads: ${JSON.stringify(publicarData)}`);
  }

  return publicarData;
}

async function main() {
  checkEnv();

  console.log(`[${new Date().toISOString()}] Buscando novidades...`);
  const resumo = await buscarNovidades();

  if (resumo === "SEM_NOVIDADES" || resumo.length < 5) {
    console.log("Nenhuma novidade relevante encontrada hoje. Encerrando sem publicar.");
    return;
  }

  const state = loadState();
  if (state.lastHeadline === resumo) {
    console.log("Mesmo conteúdo do último dia já publicado. Encerrando pra evitar post duplicado.");
    return;
  }

  console.log("Novidades encontradas:\n" + resumo);

  console.log("Gerando post...");
  const post = await gerarPost(resumo);
  console.log("Post gerado:\n" + post);

  console.log("Publicando no Threads...");
  const resultado = await publicarNoThreads(post);
  console.log("Publicado com sucesso:", resultado);

  saveState({ lastHeadline: resumo, lastRunDate: new Date().toISOString() });
}

main().catch((err) => {
  console.error("Erro no script:", err.message);
  process.exit(1);
});
