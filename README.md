# Sliding-Window Document Classifier

Sequential page classifier for long PDFs: each target page is labeled using a **three-page sliding window** (previous text + previous predicted label, target text, next text). Built for the document-processing scenario where isolated per-page calls miss continuations (e.g. invoice line items on page 5 without the header on page 4).

**Labels:** `Invoice`, `Purchase Order`, `Contract`, `Appendix`, `Other`.

## Repository map (assessment deliverables)

| Deliverable | Location |
|-------------|----------|
| System design, latency, token cost | [`design.md`](design.md) |
| Prompt, JSON payload, response schema | [`prompt.md`](prompt.md) |
| Orchestration implementation | [`classifier.py`](classifier.py) |
| Demo runner + evaluation vs ground truth | [`main.py`](main.py), [`demo_data.py`](demo_data.py) |
| Tests (no API key) | [`test_classifier.py`](test_classifier.py) |

## What the code demonstrates

- Sequential traversal with **state**: page *N* receives the validated label from page *N−1* (or `UNKNOWN` if *N−1* failed after retries).
- **Boundaries**: first page has no previous neighbor; last page has no next neighbor (`null` in the payload).
- **Failure isolation**: a failed page yields `label: null`, `status: failed`; the document run continues.
- **Output validation**: malformed JSON, wrong shape, or labels outside the allow-list trigger retry, then failure.
- **Structured logging** per API call and per page (stderr); JSON results on stdout.
- **Demo evaluation** against `expected_labels` in `demo_data.py` (stderr summary + `evaluation` JSON).

PDF extraction and OCR are **out of scope**; input is an ordered `list[str]` of page text.

## Quick start

Requires **Python 3.12+** (see `.python-version`).

### Option A — `uv` (recommended)

```bash
cd sliding_window_document_classifier
uv sync
cp .env.example .env
# Edit .env: set OPENROUTER_API_KEY and OPENROUTER_MODEL
uv run main.py
uv run python -m unittest -v
```

`uv sync` creates `.venv` and installs dependencies from `pyproject.toml` / `uv.lock`.

### Option B — `pip` and venv

```bash
cd sliding_window_document_classifier
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set OPENROUTER_API_KEY and OPENROUTER_MODEL
python main.py
python -m unittest -v
```

### Environment variables

| Variable | Purpose |
|----------|---------|
| `OPENROUTER_API_KEY` | Bearer token for the chat-completions API |
| `OPENROUTER_MODEL` | Model slug (e.g. `openai/gpt-4o-mini` on OpenRouter) |
| `OPENROUTER_BASE_URL` | API root, default OpenRouter; swap for Cloudflare Workers AI (see `.env.example`) |
| `REQUEST_TIMEOUT_SECONDS` | Per-request timeout (default `45`) |
| `MAX_RETRIES` | Extra attempts after the first try (default `2`) |
| `MAX_PAGE_CHARS` | Truncation limit per page in the payload (default `12000`) |
| `LOG_LEVEL` | `INFO` or `DEBUG` (default `INFO`) |

### Programmatic use

```python
from classifier import ClassifyDocument

results = ClassifyDocument(
    page_texts=["page one …", "page two …"],
    document_id="doc-001",
)
```

## Running the demo

`main.py` classifies the 16-page synthetic procurement bundle in `demo_data.py`, logs progress to **stderr**, prints the results array to **stdout**, and prints an **evaluation** object to stderr:

```bash
uv run main.py 2>run.log
# stdout: per-page JSON results
# stderr: logs + {"evaluation": { "matched_count", "failed_pages", "unmatched", ... }}
```

### Sample run (observed)

End-to-end demo with **`openai/gpt-4o-mini`** via OpenRouter (`MAX_RETRIES=1`, 16 pages):

- **Wall time:** ~30 s (16 sequential calls, ~1.2–2.3 s latency each).
- **API success:** 16/16 pages (`status: success`, 1 attempt each).
- **Vs `expected_labels`:** 16/16 matched on the synthetic bundle (continuation pages, PO/contract/appendix boundaries, separate invoice, email, routing sheet).
- **Typical usage per page:** ~700–1,090 prompt tokens (three-page window + system prompt), ~5–6 completion tokens for `{"label":"…"}`.

See [`design.md`](design.md) for latency/token extrapolation to 100-page documents and trade-offs.

## Input and output

Each result object:

| Field | Meaning |
|-------|---------|
| `page` | One-based page number |
| `label` | Allowed label, or `null` if classification failed |
| `status` | `success` or `failed` |
| `attempts` | API attempts used for that page |
| `error` | Short error string on failure, else `null` |

On failure, the **next** page still receives the previous page **text**, but `predicted_label` is **`UNKNOWN`**, not `Other`.

## LLM provider assumptions

- The client uses the **OpenAI-compatible** `POST …/chat/completions` shape (`classifier.CallOpenRouter`).
- **OpenRouter** is the default in `.env.example` (easy model switching).
- **Cloudflare Workers AI** supports the same compatibility layer; point `OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY` at your account token and use a Workers AI model id (comments in `.env.example`). No code changes required for a basic swap.

## If I had more time

- Deploy the orchestrator as a **Cloudflare Worker** (queue + D1/KV for per-page checkpoints) using Workers AI natively.
- Raise `max_tokens` via env for models that truncate JSON at low caps; add optional `response_format: json_object` where supported.
- PDF ingestion pipeline (extractor upstream), persistent job store, and resume-from-last-page for worker crashes.
- Larger labeled evaluation set, macro-F1, and confusion matrix on boundary/continuation pages.
- Document-level parallelism with a global concurrency limit and rate-limit-aware backoff.
