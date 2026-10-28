# System Design: Sliding-Window Page Classification

Technical write-up for the assessment scenario: classifying every page of large PDFs into **Invoice**, **Purchase Order**, **Contract**, **Appendix**, or **Other**, using neighboring pages and the **previous page’s predicted label** as context.

---

## Problem and approach

**Today’s failure mode:** single-page calls miss structure. A continuation page (line items, clauses, totals) often lacks the original title, so the model guesses wrong.

**Proposed fix:** when classifying target page *N*, send:

1. Page *N−1* text and its **predicted** label (if *N > 1*)
2. Page *N* text (the only page to classify)
3. Page *N+1* text (if *N* is not the last page)

The system prompt requires classifying **only** the target page; neighbors are supporting evidence. The previous label is a **hint**, not ground truth, so a new document can start on page *N* even if *N−1* was an invoice.

This repository implements that contract in Python (`classifier.py`): sequential orchestration, payload construction, HTTP calls, validation, retries, and logging.

---



## 1. Orchestration



### Single document

```
For page_index = 0 .. N-1:
  Build payload(prev text + prev label, target text, next text)
  Call LLM → validate JSON label
  If success: prev_label = label
  Else: record failure; prev_label = UNKNOWN for the next iteration
  Persist result immediately (production: DB row per page)
```

**State carried forward:** only the **validated label** from page *N−1*. Text for *N−1* is re-read from the input list each time (immutable source of truth).

**Failure representation:** `{ "page": k, "label": null, "status": "failed", "error": "…", "attempts": … }`. Processing **does not** abort the document. Page *k+1* still gets *k*’s text in the window; `predicted_label` is `UNKNOWN`, not `Other`, so a transient API error is not mistaken for a business category.

**Validation gate:** HTTP success → parse JSON → exactly one key `label` → value in allow-list. Anything else is retryable until `MAX_RETRIES` is exhausted.

**Boundaries:** page 1 has `previous_page: null`; last page has `next_page: null` (see `BuildUserPayload` in `classifier.py`).

### Many documents in parallel

Within one document, calls **must** stay sequential because page *N* depends on the prediction for *N−1*.

Across documents, run **independent workers**:

- Queue: `(document_id, page_texts_ref, model, prompt_version)`
- Each worker: sequential loop above for one document
- Global **concurrency limit** to respect provider rate limits (429 → exponential backoff with jitter)
- **Idempotent writes** keyed by `(document_id, page_number, model, prompt_version)`
- Checkpoint **last completed page** so a crash resumes at the next pending page

For a multi-host deployment, replace a single SQLite file with PostgreSQL + a durable queue; **Temporal** (or similar) helps when you need long-running workflows, timers, and retry policies across services—still with per-page results stored in your own DB.

**Cloudflare-oriented deployment (not fully built here):** a Worker consumes queue messages, calls **Workers AI** (OpenAI-compatible REST) per page in order, writes results to **D1** or **KV**, and exposes job status. Credits from a personal Cloudflare account fit the assignment’s provider note; this repo uses the same HTTP shape against OpenRouter for local runs.

---



## 2. Latency and sequential dependency



### The constraint

A 100-page document implies **~100 serial LLM round trips** if you keep the strict sliding-window + previous-label design. Parallelizing pages *within* the same document without changing the algorithm breaks the specified context chain.

### Back-of-envelope

If mean end-to-end latency is **L** seconds per page (network + provider + validation), wall time for one document is approximately:

**T ≈ N × L** (plus retry overhead)


| N (pages) | L = 1.2 s | L = 1.8 s | L = 2.3 s |
| --------- | --------- | --------- | --------- |
| 16        | ~19 s     | ~29 s     | ~37 s     |
| 100       | ~120 s    | ~180 s    | ~230 s    |




### Observed demo (this repo)

Synthetic 16-page bundle, `openai/gpt-4o-mini` via OpenRouter, `MAX_RETRIES=1`:

- Total wall time **~30 s** for 16 pages (~**1.9 s** average per call).
- Per-call latency from logs: **~1.2–2.3 s**; all `finish_reason=stop`.
- **16/16** API successes; labels matched `expected_labels` in `demo_data.py`.

That aligns with extrapolating **~3 minutes** for 100 pages at ~1.8 s/page before queueing or extraction.

### Safe ways to reduce end-to-end latency


| Approach                                                                                                          | Preserves design? | Trade-off                                                    |
| ----------------------------------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------ |
| **Parallelize across documents**                                                                                  | Yes               | Needs queue + concurrency cap; no change to per-doc accuracy |
| **Faster/smaller model** after eval                                                                               | Yes               | May hurt continuation accuracy; must measure on labeled set  |
| **HTTP keep-alive, regional endpoint, tight timeouts**                                                            | Yes               | Engineering only                                             |
| **Truncate context pages more aggressively than target**                                                          | Mostly            | Risk missing headers on neighbors; A/B on F1                 |
| **Speculative pass** (classify all pages in parallel without prev label, then sequential repair on disagreements) | Partially         | Extra tokens/calls; not equivalent to strict baseline        |
| **Parallel within doc without prev label**                                                                        | No                | Faster but drops the assignment’s state requirement          |


**Recommendation:** keep sequential in-document processing as the **source of truth**; scale throughput with **document-level** workers first.

---



## 3. Token cost

Let **T** = average tokens of one page body in the payload, **S** = system prompt + JSON wrapper overhead.


| Strategy                     | Input tokens per page (mid-document) | Output               |
| ---------------------------- | ------------------------------------ | -------------------- |
| Single-page                  | ~T + S                               | one short JSON label |
| Sliding window (this design) | ~**3T** + S                          | one short JSON label |


For **N = 100** and similar page lengths, input volume is roughly **~3×** single-page classification (boundaries slightly lower). Output stays tiny (~5–10 tokens).

### Observed demo (prompt/completion tokens from logs)

Typical per page with three neighbors in the bundle:

- **Prompt (input):** ~700–1,090 tokens  
- **Completion (output):** ~5–6 tokens

Rough totals for 16 pages: **~16k input + ~90 output** (order-of-magnitude; sum varies by page length). Scaling to 100 pages: **~100k–110k input tokens** for this payload size before caching.

### Cost controls

- `MAX_PAGE_CHARS` with head/tail truncation (implemented in `LimitPageText`).
- Shorter previews for **prev/next** only, full text for **target** (evaluate on labeled data before shipping).
- Stable system prompt for provider **prompt caching** where available.
- `temperature=0`, low `max_tokens` on completion (watch models that truncate JSON—prefer 64+ or JSON mode if needed).
- Log `usage` from each response (implemented) for billing reconciliation.

Any reduction that strips headers or continuation cues can hurt exactly the cases this design targets—measure on continuation pages and document boundaries.

---



## 4. Reliability, testing, and evaluation

- **Retries:** transient HTTP errors and invalid outputs; exponential backoff between attempts (`ClassifyOnePage`).
- **Tests:** `python -m unittest -v` mocks the API—label parsing, boundaries, failed-page → `UNKNOWN`, document continues.
- **Demo ground truth:** `demo_data.expected_labels` (synthetic procurement bundle: multi-page invoice, PO, contract, appendices, routing, email, second invoice, scan notes). `main.py` reports matched / unmatched / failed page numbers on stderr.

---



## 5. Honest scoping / next steps

Delivered: design above, working orchestrator, prompt/payload spec (`prompt.md`), runnable demo, tests, logging, evaluation hook.

Not delivered: Cloudflare Worker deployment, PDF extraction, durable job store, or a production-grade labeled benchmark. Highest-value follow-ups: Workers AI deployment with D1 checkpoints, env-driven `max_tokens` + JSON response mode, and a larger evaluation set with macro-F1 on continuation pages.