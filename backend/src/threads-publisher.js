/**
 * threads-publisher.js
 * Publicação automática de clipes no Threads (@inovashot.cortes) para o InovaShot.
 *
 * COMO INTEGRAR (3 passos):
 *
 * 1) Salve este arquivo em /app/inovashot/backend/threads-publisher.js
 *
 * 2) No server.js, adicione esta linha no topo, junto com os outros requires:
 *      const { publicarClipeNoThreads } = require('./threads-publisher');
 *
 * 3) Dentro da função processVideoAsync, no loop "for (const moment of finalMoments)",
 *    logo APÓS o bloco que já salva o clip no Supabase (depois de
 *    "logger(`✅ Clip saved: ${clipId}`); clipIds.push(clipId);"), adicione:
 *
 *      publicarClipeNoThreads({
 *        id: clipId,
 *        video_url: `${process.env.SUPABASE_URL}/storage/v1/object/public/clips/${storagePath}`,
 *        nota_viralidade: moment.score,
 *        tema: moment.reason,
 *        hook: moment.hook_a,
 *      }, supabase).catch(e => logger(`Threads publish falhou (não bloqueante): ${e.message}`));
 *
 *    Não usar "await" nessa chamada — assim a publicação roda em segundo plano
 *    e não atrasa a resposta do job para o usuário. O segundo argumento (supabase)
 *    é o client que já existe no topo do server.js — passe ele para habilitar o log.
 *
 * Requisitos já atendidos no seu ambiente:
 * - THREADS_ACCESS_TOKEN já está no .env de produção (configurado 21/07/2026)
 * - ANTHROPIC_API_KEY já está no .env (usado por analyzeWithClaude)
 * - Bucket "clips" do Supabase Storage precisa ser público para a URL funcionar
 *   (mesma URL que a rota /api/clips já usa para montar share_url)
 *
 * Opcional: para o log funcionar, crie no Supabase uma tabela "social_posts" com
 * colunas: clip_id (text), rede (text), status (text), post_id (text), legenda (text),
 * erro (text), created_at (timestamp, default now()). Sem essa tabela, tudo continua
 * funcionando normalmente — só o log fica desativado silenciosamente.
 */

const Anthropic = require('@anthropic-ai/sdk');

const NOTA_MINIMA = 7; // só publica clipes com nota de viralidade >= 7

/**
 * Gera a legenda do post usando Claude Haiku (mesmo modelo já usado em analyzeWithClaude).
 */
async function gerarLegenda(clipe) {
  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

  const prompt = `Escreva uma legenda curta (máximo 2 frases, até 200 caracteres) para um post no Threads divulgando um clipe de vídeo.

Regras obrigatórias:
- "A InovaShot" deve ser o sujeito ativo quando mencionar a marca (ex: "A InovaShot identificou...", nunca "a IA fez...")
- NUNCA use a palavra "IA" ou "Inteligência Artificial" como sujeito da frase
- Tom natural e humanizado, sem soar robótico ou genérico
- No máximo 2 hashtags, só se fizer sentido

Tema do clipe: ${clipe.tema || "conteúdo geral"}
Hook: ${clipe.hook || ""}

Retorne APENAS o texto da legenda, sem aspas, sem explicação.`;

  const message = await client.messages.create({
    model: 'claude-haiku-4-5',
    max_tokens: 150,
    messages: [{ role: 'user', content: prompt }],
  });

  return message.content[0].text.trim();
}

/**
 * Publica um clipe no Threads.
 * @param {Object} clipe - { id, video_url, nota_viralidade, tema, hook }
 * @param {Object} supabaseClient - opcional, instância já criada no server.js, para log
 */
async function publicarClipeNoThreads(clipe, supabaseClient = null) {
  if (!clipe.nota_viralidade || clipe.nota_viralidade < NOTA_MINIMA) {
    console.log(`[Threads] Clipe ${clipe.id} não publicado (nota ${clipe.nota_viralidade} < ${NOTA_MINIMA})`);
    return { publicado: false, motivo: 'nota_abaixo_do_minimo' };
  }

  const token = process.env.THREADS_ACCESS_TOKEN;
  if (!token) {
    console.error('[Threads] THREADS_ACCESS_TOKEN não configurado no .env');
    return { publicado: false, motivo: 'token_ausente' };
  }

  try {
    const legenda = await gerarLegenda(clipe);

    // 1. Cria o container de mídia
    const createUrl = new URL('https://graph.threads.net/v1.0/me/threads');
    createUrl.searchParams.set('media_type', 'VIDEO');
    createUrl.searchParams.set('video_url', clipe.video_url);
    createUrl.searchParams.set('text', legenda);
    createUrl.searchParams.set('access_token', token);

    const createRes = await fetch(createUrl.toString(), { method: 'POST' });
    const createData = await createRes.json();
    if (createData.error) throw new Error(`Criar container: ${createData.error.message}`);

    const creationId = createData.id;

    // 2. Vídeo precisa de um tempo de processamento no Threads antes de publicar
    await new Promise((resolve) => setTimeout(resolve, 15000));

    // 3. Publica
    const publishUrl = new URL('https://graph.threads.net/v1.0/me/threads_publish');
    publishUrl.searchParams.set('creation_id', creationId);
    publishUrl.searchParams.set('access_token', token);

    const publishRes = await fetch(publishUrl.toString(), { method: 'POST' });
    const publishData = await publishRes.json();
    if (publishData.error) throw new Error(`Publicar: ${publishData.error.message}`);

    console.log(`[Threads] Clipe ${clipe.id} publicado. Post ID: ${publishData.id}`);

    if (supabaseClient) {
      supabaseClient.from('social_posts').insert({
        clip_id: clipe.id,
        rede: 'threads',
        status: 'sucesso',
        post_id: publishData.id,
        legenda,
      }).then(() => {}, () => {}); // não bloqueia se a tabela não existir ainda
    }

    return { publicado: true, post_id: publishData.id };
  } catch (erro) {
    console.error(`[Threads] Falha ao publicar clipe ${clipe.id}:`, erro.message);

    if (supabaseClient) {
      supabaseClient.from('social_posts').insert({
        clip_id: clipe.id,
        rede: 'threads',
        status: 'erro',
        erro: erro.message,
      }).then(() => {}, () => {});
    }

    return { publicado: false, motivo: 'erro_api', erro: erro.message };
  }
}

module.exports = { publicarClipeNoThreads };
