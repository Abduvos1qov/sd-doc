---
sidebar_position: 9
title: Search & RAG
audience: Anyone making docs discoverable / building an "Ask docs" feature
summary: How the in-page search works today, what tuning options exist, and the path to a real RAG layer with vector embeddings + an LLM endpoint.
topics: [search, rag, vector, embeddings, lunr, performance]
---

# Search & RAG

Two distinct layers for finding things in sd-docs.

## Layer 1 — `docusaurus-search-local` (already wired)

Out of the box, every page has a search box in the top bar. It runs entirely in the browser using a [lunr.js](https://lunrjs.com/) index built at compile time.

### Config in `docusaurus.config.js`

```javascript
themes: [
  '@docusaurus/theme-mermaid',
  [
    require.resolve('@easyops-cn/docusaurus-search-local'),
    {
      hashed: true,                                   // content-addressed cache
      language: ['en', 'ru'],                         // stemmer per language
      docsRouteBasePath: ['/docs', '/guide'],         // both collections
      indexBlog: false,
      highlightSearchTermsOnTargetPage: true,
      explicitSearchResultPath: true,
      searchResultLimits: 8,                          // results per query
      searchResultContextMaxLength: 50,               // snippet length
    },
  ],
],
```

### What got tuned in Phase 31

| Change | Why |
|--------|-----|
| Added `/guide` to `docsRouteBasePath` | Client guide pages weren't searchable before. Now they are. |
| `searchResultLimits: 8` | Default was higher; smaller index payload, faster paint |
| `searchResultContextMaxLength: 50` | Trims snippet length per result, smaller index |
| Kept `hashed: true` | Content-addressed cache survives across deploys |

### Uzbek caveat

The `language` option supports lunr's official language stemmers — Uzbek isn't on that list, so UZ content is indexed using the English stemmer. Practically that means:

- Russian UI labels in Uzbek prose (`Логин`, `Войти`) still match because Russian stemmer is loaded
- Pure-Uzbek words match exactly (no stemming, but exact-match works)
- Stemming-dependent searches (singular/plural, verb forms) only work for English/Russian

If Uzbek stemming becomes critical, you'd need to fork the plugin or write a custom indexer.

### Performance tuning if response time is still long

1. **Check the index size** after build: `ls -lh build/search-index*.json`. If it's >5 MB, the browser download is the bottleneck.
2. **Filter what gets indexed.** The plugin walks every page; you can exclude paths with `ignoreFiles: [...]`.
3. **Disable highlight** if the highlight-on-target-page is heavy: `highlightSearchTermsOnTargetPage: false`.
4. **Switch to Algolia DocSearch** if you want server-side search. Free for OSS-style projects.

## Layer 2 — RAG (vector embeddings + LLM)

For "Ask the docs in natural language" — what `docusaurus-search-local` can't do — you need a Retrieval-Augmented Generation layer. This isn't shipped yet; the scaffolding is.

### Step 1 — Build the index (already scaffolded)

`scripts/build-rag-index.py` walks every markdown file across all three locales and emits one JSONL row per page:

```bash
python3 scripts/build-rag-index.py
# → build/rag-index.jsonl  (about 1,500 records, ~17 MB)
```

Each record has:

```json
{
  "doc_id":    "docs/modules/orders.md",
  "locale":    "en",
  "collection": "docs",
  "url":       "/docs/modules/orders",
  "title":     "orders",
  "summary":   "Order capture, status machine, ...",
  "topics":    ["orders", "modules", "sales"],
  "audience":  "Backend engineers, QA, PM",
  "headings":  ["Key features", "Folder", "Controllers", ...],
  "content":   "<full markdown body>",
  "chunks":    [
    { "heading": "Key features", "text": "..." },
    { "heading": "Folder",       "text": "..." }
  ]
}
```

Filter by locale or collection if you only want a slice:

```bash
python3 scripts/build-rag-index.py --locale ru
python3 scripts/build-rag-index.py --collection guide
```

### Step 2 — Embed (your choice of provider)

The JSONL is provider-agnostic. Three sensible options:

#### Option A — Anthropic (via Voyage AI)

```python
import json
from voyageai import Client

vo = Client()
with open("build/rag-index.jsonl") as f:
    for line in f:
        rec = json.loads(line)
        # Embed each chunk separately for finer retrieval
        for chunk in rec["chunks"]:
            text = f"{rec['title']}\n{chunk['heading']}\n{chunk['text']}"
            emb = vo.embed([text], model="voyage-multilingual-2").embeddings[0]
            # Store {emb, rec['url'], chunk['heading'], text} in your vector DB
```

`voyage-multilingual-2` is recommended for RU + UZ content. ~$0.10 per million tokens.

#### Option B — OpenAI

```python
from openai import OpenAI

oa = OpenAI()
# text-embedding-3-small (1536 dims, $0.02/1M tokens)
# or text-embedding-3-large (3072 dims, $0.13/1M)
emb = oa.embeddings.create(
    input=text,
    model="text-embedding-3-small",
).data[0].embedding
```

#### Option C — Local model (free, slower)

```python
from sentence_transformers import SentenceTransformer

m = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")  # 768 dims, ~1.1 GB
emb = m.encode(text).tolist()
```

Multilingual mpnet handles EN/RU/UZ well in our testing.

### Step 3 — Store

Pick one based on operational appetite:

| Vector store | Hosted | Cost | When to pick |
|--------------|--------|------|--------------|
| **Pinecone** | yes | from $70/mo | You want zero ops, paid SaaS |
| **Weaviate Cloud** | yes | from $25/mo | You want zero ops, cheaper than Pinecone |
| **pgvector** (Postgres extension) | self-hosted | free | You already run Postgres |
| **Chroma** (local) | self-hosted | free | Dev-only, simple file backing |

Each chunk gets one row: `(embedding_vector, url, locale, heading, text)`.

### Step 4 — Query path

Add a `/ask` API endpoint and a chat widget. Pseudocode:

```python
@app.post("/ask")
def ask(question: str, locale: str):
    q_emb = embed(question)
    hits = vector_db.query(q_emb, top_k=8, filter={"locale": locale})

    context = "\n\n".join(
        f"[{h.url}] {h.heading}\n{h.text}" for h in hits
    )

    answer = claude.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=(
            "You answer questions about SalesDoctor using only the provided context. "
            f"Reply in the user's locale ({locale}). If the context doesn't answer the "
            "question, say so plainly and cite the URLs of the most relevant pages."
        ),
        messages=[
            {"role": "user", "content": f"Question: {question}\n\nContext:\n{context}"}
        ],
    )
    return {"answer": answer.content[0].text, "sources": [h.url for h in hits]}
```

### Step 5 — Widget

Either:

1. **Reuse your existing RAG layer.** The `team/rag-indexing.md` page already mentions a team-wide RAG; just point it at this JSONL.
2. **Embed a chat widget** on the docs site. Docusaurus supports React components in MDX — drop `<AskDocs />` at the top of `intro.md` and route it at `/ask`.

### Estimated cost at current corpus size

- ~1,500 records × avg 800 tokens each = ~1.2 M input tokens for one-time embedding.
- Voyage AI multilingual-2: ~$0.12 one-time.
- OpenAI text-embedding-3-small: ~$0.024 one-time.
- Local mpnet: free, ~10 minutes on a Mac M-series.

Per query:
- Voyage AI: ~$0.0001 per question (embed once)
- Claude Haiku 4.5: ~$0.001–0.005 per answered question depending on context length

So ~$1 per 1,000 questions answered. Cheaper than the lunr download for a busy site.

## Implementation phases

| Phase | What | Effort | Status |
|-------|------|--------|--------|
| 1 — Search-local tuning | Better config in `docusaurus.config.js` | 1 session | ✅ done |
| 2 — RAG index builder | `scripts/build-rag-index.py` | 1 session | ✅ done |
| 3 — Embedding pipeline | Pick provider + run once | 1 session | ⏳ next |
| 4 — Vector DB choice | Pinecone / Weaviate / pgvector | 1 session | ⏳ |
| 5 — Ask-docs endpoint | FastAPI / Cloudflare Worker | 1 session | ⏳ |
| 6 — Chat widget | React component in MDX | 1 session | ⏳ |
| 7 — Track unanswered | Log queries that produce no good hits | ongoing | — |

## See also

- [Contributing →](./contributing) — local setup, build commands
- [Style guide →](./style-guide) — what goes in frontmatter (drives RAG metadata)
- [RAG indexing concept](./rag-indexing) — the existing team-wide RAG approach
- Scripts:
  - `scripts/build-rag-index.py` — JSONL builder
  - `docusaurus.config.js` — search-local config
