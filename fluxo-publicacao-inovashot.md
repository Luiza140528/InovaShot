# Fluxo de Publicação de Conteúdo — InovaShot

Checklist fixo para todo artigo novo (blog + Medium). Seguir na ordem — nenhum passo é opcional.

---

## 1. Blog (inovashot.com.br) — fonte oficial

- [ ] Artigo publicado como página HTML no site (GitHub Pages)
- [ ] Estrutura otimizada para citação por IA/AI Overview: headers claros (H2/H3), respostas diretas logo após perguntas, listas quando fizer sentido
- [ ] Schema FAQPage (JSON-LD) adicionado no `<head>`, com as mesmas perguntas/respostas que aparecem na seção FAQ visível do artigo
- [ ] Regra de marca aplicada: "O InovaShot" como sujeito, nunca "a IA"
- [ ] URL final confirmada (ex: `inovashot.com.br/nome-do-artigo.html`)
- [ ] Link adicionado ao sitemap (se não for automático)

### Como subir o arquivo no GitHub (mobile)

**Artigo novo (arquivo novo):**
1. Abrir o repositório do site no navegador/app do GitHub
2. Ir até a pasta correta (raiz ou pasta do blog, conforme estrutura do site)
3. Tocar em **"Add file" → "Create new file"**
4. Nomear o arquivo (ex: `nome-do-artigo.html`)
5. Colar o HTML completo do artigo
6. Escrever mensagem de commit curta (ex: "Novo post: [título]")
7. Confirmar em **"Commit directly to the main branch"** — checar sempre qual é a branch certa do repositório antes de commitar

**Atualizar arquivo existente (ex: sitemap, índice do blog):**
1. Abrir o arquivo no GitHub
2. Ícone de lápis (editar)
3. Fazer a alteração
4. Commit direto na branch certa

⚠️ Sempre confirmar a branch certa antes de commitar — checar isso é parte do passo, não assumir "main" por padrão.

## 2. Indexação no Google — não esperar o rastreio automático

- [ ] Abrir Google Search Console
- [ ] Inspeção de URL → colar a URL do artigo novo
- [ ] Clicar em **"Solicitar indexação"**
- [ ] Confirmar depois de alguns dias com `site:inovashot.com.br "trecho do título"` no Google

⚠️ Sem esse passo, o artigo pode levar semanas para ser rastreado sozinho — ou nunca aparecer.

## 3. Medium — distribuição, não fonte principal

- [ ] Publicar o artigo na conta **Equipe InovaShot**
- [ ] Definir **canonical link** apontando pro artigo do blog (evita conteúdo duplicado penalizado)
- [ ] Verificar que o status do post é **"Published"**, não "Draft" — checar na aba Stories do perfil
- [ ] Lembrar: contas novas do Medium ficam com `noindex,nofollow` até ganhar histórico/engajamento — isso destrava sozinho com tempo, não precisa (nem dá) para forçar

## 4. Otimização pós-publicação

- [ ] Meta description do artigo do blog preenchida (se aplicável)
- [ ] Compartilhar o link em pelo menos 1 canal social (Instagram, TikTok, Facebook) pra gerar sinal de engajamento externo
- [ ] Anotar a data de publicação (referência pra saber quando cobrar indexação, geralmente 1-2 semanas)

---

## Ordem resumida
**Blog publicado → Search Console (solicitar indexação) → Medium publicado (canonical pro blog) → compartilhar em 1 rede social**
