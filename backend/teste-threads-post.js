/**
 * Script de teste — Publicação no Threads via API
 * InovaShot
 *
 * COMO USAR:
 * 1. Preencha as duas constantes abaixo (ACCESS_TOKEN e THREADS_USER_ID)
 * 2. Rode no terminal do servidor: node teste-threads-post.js
 * 3. Se der certo, vai aparecer o link do post publicado
 *
 * IMPORTANTE: nunca suba esse arquivo pro GitHub com o token preenchido.
 * Depois do teste, o ideal é mover o token pro .env e usar process.env.THREADS_ACCESS_TOKEN
 */

const ACCESS_TOKEN = "COLE_SEU_TOKEN_AQUI";
const THREADS_USER_ID = "27567513142918699"; // já preenchido, é o ID da @inovashot.cortes

const BASE_URL = "https://graph.threads.net/v1.0";

async function publicarNoThreads(texto) {
  try {
    // ETAPA 1 — Criar o container do post
    console.log("1/2 — Criando container...");
    const criarContainer = await fetch(
      `${BASE_URL}/${THREADS_USER_ID}/threads?` +
        new URLSearchParams({
          media_type: "TEXT",
          text: texto,
          access_token: ACCESS_TOKEN,
        })
    );
    const containerData = await criarContainer.json();

    if (containerData.error) {
      console.error("Erro ao criar container:", containerData.error);
      return;
    }

    const containerId = containerData.id;
    console.log("Container criado com ID:", containerId);

    // ETAPA 2 — Publicar o container criado
    console.log("2/2 — Publicando...");
    const publicar = await fetch(
      `${BASE_URL}/${THREADS_USER_ID}/threads_publish?` +
        new URLSearchParams({
          creation_id: containerId,
          access_token: ACCESS_TOKEN,
        }),
      { method: "POST" }
    );
    const publicarData = await publicar.json();

    if (publicarData.error) {
      console.error("Erro ao publicar:", publicarData.error);
      return;
    }

    console.log("✅ Publicado com sucesso!");
    console.log("ID do post:", publicarData.id);
  } catch (err) {
    console.error("Erro inesperado:", err);
  }
}

// Texto de teste — pode trocar por qualquer coisa
publicarNoThreads("Teste de publicação automática via API 🚀 — InovaShot");
