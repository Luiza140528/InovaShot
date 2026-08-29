// instagram-webhook.js - Webhook de comentarios/DM do Instagram para InovaShot

const express = require('express');
const router = express.Router();

const VERIFY_TOKEN = process.env.IG_WEBHOOK_VERIFY_TOKEN;
const PAGE_ACCESS_TOKEN = process.env.IG_PAGE_ACCESS_TOKEN;
const KEYWORD = 'QUERO';
const DM_MESSAGE = 'Oi! Aqui esta o prompt que a gente realmente usa no InovaShot pra gerar hook de video curto:\n\n"Analise esta transcricao e sugira 3 hooks de abertura de ate 8 palavras, testados pra prender atencao nos primeiros 3 segundos. Priorize pergunta ou afirmacao polemica sobre a maior curiosidade do video."\n\nSe quiser testar isso automatico direto no seu video: inovashot.com.br';

router.get('/webhook', (req, res) => {
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  if (mode === 'subscribe' && token === VERIFY_TOKEN) {
    console.log('Webhook do Instagram verificado com sucesso.');
    return res.status(200).send(challenge);
  }
  return res.sendStatus(403);
});

router.post('/webhook', async (req, res) => {
  res.sendStatus(200);

  try {
    const entries = req.body.entry || [];
    for (const entry of entries) {
      const changes = entry.changes || [];
      for (const change of changes) {
        if (change.field === 'comments') {
          const comment = change.value;
          const commentText = (comment.text || '').toUpperCase();
          const fromUserId = comment.from?.id;

          if (commentText.includes(KEYWORD) && fromUserId) {
            await sendDirectMessage(fromUserId);
            console.log('DM enviada para: ' + fromUserId);
          }
        }
      }
    }
  } catch (err) {
    console.error('Erro no webhook do Instagram:', err.message);
  }
});

async function sendDirectMessage(recipientId) {
  const url = 'https://graph.instagram.com/v21.0/me/messages?access_token=' + PAGE_ACCESS_TOKEN;
  const payload = {
    recipient: { id: recipientId },
    message: { text: DM_MESSAGE },
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error('Falha ao enviar DM: ' + response.status + ' - ' + errorBody);
  }
}

module.exports = router;
