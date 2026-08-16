#!/usr/bin/env node

/**
 * analisar-site.js
 *
 * Analisa uma URL com o Google PageSpeed Insights e pede pro Claude
 * explicar, em português simples, os principais problemas e como corrigir.
 *
 * USO:
 *   node analisar-site.js https://seusite.com.br
 *   node analisar-site.js https://seusite.com.br mobile   (padrão)
 *   node analisar-site.js https://seusite.com.br desktop
 *
 * VARIÁVEIS DE AMBIENTE NECESSÁRIAS (ex: no .env ou export no terminal):
 *   ANTHROPIC_API_KEY   -> sua chave da API da Anthropic
 *   PAGESPEED_API_KEY   -> chave da API do Google PageSpeed Insights
 *                          (gratuita, gerada no Google Cloud Console:
 *                          ative "PageSpeed Insights API" e crie uma API key)
 *
 * Sem PAGESPEED_API_KEY o script ainda funciona, mas com limite de
 * requisições bem baixo (a API aceita chamadas sem chave, só que restritas).
 */

const https = require("https");

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const PAGESPEED_API_KEY = process.env.PAGESPEED_API_KEY || "";

function fail(msg) {
  console.error(`\n❌ ${msg}\n`);
  process.exit(1);
}

const targetUrl = process.argv[2];
const strategy = (process.argv[3] || "mobile").toLowerCase();

if (!targetUrl) {
  fail("Uso: node analisar-site.js https://seusite.com.br [mobile|desktop]");
}
if (!ANTHROPIC_API_KEY) {
  fail("Variável ANTHROPIC_API_KEY não encontrada. Defina antes de rodar o script.");
}
if (!["mobile", "desktop"].includes(strategy)) {
  fail("O segundo argumento deve ser 'mobile' ou 'desktop'.");
}

// ---------- 1. Chamar o PageSpeed Insights ----------

function fetchPageSpeed(url, strategy) {
  return new Promise((resolve, reject) => {
    const params = new URLSearchParams({
      url,
      strategy,
      category: "performance",
    });
    params.append("category", "seo");
    params.append("category", "accessibility");
    params.append("category", "best-practices");
    if (PAGESPEED_API_KEY) params.append("key", PAGESPEED_API_KEY);

    const endpoint = `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?${params.toString()}`;

    https
      .get(endpoint, (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          if (res.statusCode !== 200) {
            reject(new Error(`PageSpeed API retornou status ${res.statusCode}: ${data.slice(0, 500)}`));
            return;
          }
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(new Error("Falha ao ler resposta do PageSpeed Insights: " + e.message));
          }
        });
      })
      .on("error", reject);
  });
}

// ---------- 2. Resumir os dados brutos (o JSON completo é enorme) ----------

function resumirResultado(json) {
  const lighthouse = json.lighthouseResult;
  if (!lighthouse) {
    throw new Error("Resposta do PageSpeed não trouxe lighthouseResult. Confira se a URL está correta e acessível publicamente.");
  }

  const categorias = lighthouse.categories;
  const scores = {};
  for (const key of Object.keys(categorias)) {
    scores[key] = Math.round(categorias[key].score * 100);
  }

  // Pega as auditorias que falharam ou têm oportunidade de melhoria
  const audits = lighthouse.audits;
  const problemas = Object.values(audits)
    .filter((a) => a.score !== null && a.score < 0.9 && a.title)
    .sort((a, b) => (a.score ?? 1) - (b.score ?? 1))
    .slice(0, 15)
    .map((a) => ({
      titulo: a.title,
      descricao: a.description ? a.description.replace(/\[.*?\]\(.*?\)/g, "").slice(0, 200) : "",
      score: a.score,
      valor_exibido: a.displayValue || "",
    }));

  return { scores, problemas };
}

// ---------- 3. Mandar pro Claude explicar ----------

function chamarClaude(resumo, url) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model: "claude-sonnet-4-6",
      max_tokens: 1500,
      messages: [
        {
          role: "user",
          content: `Você é um especialista em SEO técnico explicando para uma pessoa empreendedora, sem conhecimento técnico profundo, mas que sabe operar site e servidor.

Analisei a URL ${url} no Google PageSpeed Insights e aqui está o resumo dos resultados:

Notas por categoria (0-100): ${JSON.stringify(resumo.scores)}

Principais problemas encontrados:
${JSON.stringify(resumo.problemas, null, 2)}

Escreva em português do Brasil, tom direto e objetivo, sem enrolação:
1. Um resumo de 2-3 frases sobre a saúde geral do site
2. Os 3 a 5 problemas MAIS IMPORTANTES (priorize por impacto em tráfego orgânico e experiência mobile), cada um com: o que é, por que importa pro Google, e como corrigir na prática
3. Não invente estatísticas nem afirme causas que não estão nos dados fornecidos

Formate em texto simples, sem markdown pesado.`,
        },
      ],
    });

    const req = https.request(
      {
        hostname: "api.anthropic.com",
        path: "/v1/messages",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": ANTHROPIC_API_KEY,
          "anthropic-version": "2023-06-01",
          "Content-Length": Buffer.byteLength(body),
        },
      },
      (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          if (res.statusCode !== 200) {
            reject(new Error(`Claude API retornou status ${res.statusCode}: ${data.slice(0, 500)}`));
            return;
          }
          try {
            const parsed = JSON.parse(data);
            const texto = parsed.content
              .filter((c) => c.type === "text")
              .map((c) => c.text)
              .join("\n");
            resolve(texto);
          } catch (e) {
            reject(new Error("Falha ao ler resposta do Claude: " + e.message));
          }
        });
      }
    );

    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

// ---------- Execução ----------

(async () => {
  try {
    console.log(`\n🔍 Analisando ${targetUrl} (${strategy}) no PageSpeed Insights...`);
    const resultadoBruto = await fetchPageSpeed(targetUrl, strategy);

    const resumo = resumirResultado(resultadoBruto);
    console.log(`\n📊 Notas: Performance ${resumo.scores.performance} | SEO ${resumo.scores.seo} | Acessibilidade ${resumo.scores.accessibility} | Boas práticas ${resumo["best-practices"]}`);

    console.log(`\n🤖 Pedindo pro Claude explicar os problemas...\n`);
    const explicacao = await chamarClaude(resumo, targetUrl);

    console.log("=".repeat(60));
    console.log(explicacao);
    console.log("=".repeat(60));
  } catch (err) {
    fail(err.message);
  }
})();
