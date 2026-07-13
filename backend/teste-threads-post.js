const ACCESS_TOKEN = "27567513142918699";
const THREADS_USER_ID = "27567513142918699";
const BASE_URL = "https://graph.threads.net/v1.0";

async function publicarNoThreads(texto) {
  try {
    console.log("1/2 - Criando container...");
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

    console.log("2/2 - Publicando...");
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

    console.log("Publicado com sucesso!");
    console.log("ID do post:", publicarData.id);
  } catch (err) {
    console.error("Erro inesperado:", err);
  }
}

publicarNoThreads("Teste de publicacao automatica via API - InovaShot");
