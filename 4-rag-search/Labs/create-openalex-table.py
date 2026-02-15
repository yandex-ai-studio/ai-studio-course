# OpenAlex -> curated Markdown table snapshot for a RAG manual chunking lab
# Produces a single large Markdown table where the header must be preserved during chunking.
#
# Requirements: pip install requests
#
# Notes:
# - OpenAlex does not provide plaintext abstracts; it provides abstract_inverted_index
#   which we reconstruct into a readable abstract here. :contentReference[oaicite:0]{index=0}
# - The API is free, but an API key is recommended for higher daily limits. :contentReference[oaicite:1]{index=1}
#
# Output: openalex_rag_snapshot.md

import os
import time
import requests
from typing import Dict, List, Any, Optional

BASE = "https://api.openalex.org"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "University-RAG-Lab/1.0 (contact: instructor@example.edu)"})

API_KEY = os.getenv("OPENALEX_API_KEY", "").strip()  # optional
EMAIL = os.getenv("OPENALEX_EMAIL", "").strip()      # optional, polite parameter
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

def _get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    max_retries: int = 5,
    base_backoff_sec: float = 1.0,
) -> Dict[str, Any]:
    params = dict(params or {})
    if API_KEY:
        params["api_key"] = API_KEY
    if EMAIL:
        params["mailto"] = EMAIL
    last_error: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        try:
            r = SESSION.get(url, params=params, timeout=60)
        except requests.exceptions.RequestException as e:
            last_error = e
            if attempt == max_retries:
                break
            time.sleep(base_backoff_sec * (2 ** (attempt - 1)))
            continue

        if r.status_code in RETRYABLE_STATUS_CODES and attempt < max_retries:
            retry_after = r.headers.get("Retry-After", "").strip()
            if retry_after.isdigit():
                sleep_for = float(retry_after)
            else:
                sleep_for = base_backoff_sec * (2 ** (attempt - 1))
            time.sleep(sleep_for)
            continue

        if r.status_code >= 400:
            error_preview = " ".join((r.text or "").split())[:300]
            raise RuntimeError(
                f"OpenAlex request failed ({r.status_code}) for {url} with params={params}. "
                f"Response: {error_preview}"
            )

        try:
            return r.json()
        except ValueError as e:
            raise RuntimeError(
                f"OpenAlex returned non-JSON response for {url} with params={params}."
            ) from e

    raise RuntimeError(
        f"OpenAlex request failed after {max_retries} attempts for {url} with params={params}."
    ) from last_error

def search_concept_id(query: str) -> str:
    """
    Returns the first concept ID for a concept search term.
    Uses Concepts search endpoint. :contentReference[oaicite:2]{index=2}
    """
    data = _get(f"{BASE}/concepts", params={"search": query, "per-page": 5})
    results = data.get("results", [])
    if not results:
        raise RuntimeError(f"No concepts found for query: {query}")
    return results[0]["id"]  # e.g., https://openalex.org/C154945302

def undo_abstract_inverted_index(inv: Optional[Dict[str, List[int]]]) -> str:
    """
    Reconstructs text from OpenAlex abstract_inverted_index.
    If inv is None, returns empty string.
    """
    if not inv:
        return ""
    # Determine the total number of tokens (max position + 1)
    max_pos = -1
    for positions in inv.values():
        if positions:
            max_pos = max(max_pos, max(positions))
    if max_pos < 0:
        return ""

    tokens = [""] * (max_pos + 1)
    for word, positions in inv.items():
        for p in positions:
            if 0 <= p < len(tokens):
                tokens[p] = word

    # Join with spaces, then lightly clean.
    text = " ".join(t for t in tokens if t)
    # Some abstracts contain spacing artifacts around punctuation; keep it simple.
    text = text.replace(" .", ".").replace(" ,", ",").replace(" ;", ";").replace(" :", ":")
    text = text.replace(" )", ")").replace("( ", "(")
    return text.strip()

def pick_best_location(work: Dict[str, Any]) -> Dict[str, Any]:
    """
    Chooses best available location for landing page / pdf info.
    OpenAlex includes primary_location and best_oa_location in some cases.
    """
    for key in ("best_oa_location", "primary_location"):
        loc = work.get(key)
        if isinstance(loc, dict):
            return loc
    return {}

def extract_source_display_name(work: Dict[str, Any]) -> str:
    """
    OpenAlex source details are nested in location objects.
    """
    for key in ("primary_location", "best_oa_location"):
        loc = work.get(key) or {}
        source = loc.get("source") or {}
        name = source.get("display_name")
        if name:
            return str(name)
    return ""

def normalize_cell(s: str, max_len: int = 600) -> str:
    """
    Make table cells safe for Markdown tables:
    - Replace newlines with spaces
    - Escape pipes
    - Truncate overly long text to keep the table usable
    """
    if s is None:
        s = ""
    s = str(s).replace("\n", " ").replace("\r", " ")
    s = s.replace("|", "\\|")
    s = " ".join(s.split())
    if len(s) > max_len:
        s = s[: max_len - 1].rstrip() + "…"
    return s

def format_authors(work: Dict[str, Any], max_authors: int = 8) -> str:
    authorships = work.get("authorships") or []
    names = []
    for a in authorships[:max_authors]:
        author = (a.get("author") or {}).get("display_name")
        if author:
            names.append(author)
    if len(authorships) > max_authors:
        names.append(f"+{len(authorships) - max_authors} more")
    return ", ".join(names)

def format_concepts(work: Dict[str, Any], max_concepts: int = 6) -> str:
    concepts = work.get("concepts") or []
    # Keep the most relevant concepts (OpenAlex often orders by score)
    names = []
    for c in concepts[:max_concepts]:
        dn = c.get("display_name")
        if dn:
            names.append(dn)
    if len(concepts) > max_concepts:
        names.append(f"+{len(concepts) - max_concepts} more")
    return ", ".join(names)

def fetch_works_snapshot(
    n_rows: int = 800,
    from_year: int = 2018,
    per_page: int = 200,
) -> List[Dict[str, Any]]:
    """
    Fetch a snapshot of AI-related works using:
    - concept filters (AI, Neural network, Language model) plus a search term
    - recent years to bias toward LLM-era literature
    Uses Works search and filter parameters. :contentReference[oaicite:3]{index=3}
    """
    # Find concept IDs (two-step lookup recommended by OpenAlex docs for ambiguous entities). :contentReference[oaicite:4]{index=4}
    concept_ai = search_concept_id("artificial intelligence")
    concept_nn = search_concept_id("neural network")
    concept_lm = search_concept_id("language model")

    # OpenAlex concept IDs look like https://openalex.org/Cxxxx
    # Filters use the short ID portion after the last slash.
    def short_id(uri: str) -> str:
        return uri.rsplit("/", 1)[-1]

    ai_id = short_id(concept_ai)
    nn_id = short_id(concept_nn)
    lm_id = short_id(concept_lm)

    # OR filter: concepts.id:{C1|C2|C3}
    concepts_or = f"{ai_id}|{nn_id}|{lm_id}"

    # Cursor pagination
    url = f"{BASE}/works"
    cursor = "*"
    collected: List[Dict[str, Any]] = []

    # We add a search term to bias toward LLM-ish content, while concepts pull in broader AI/NN.
    search_term = "large language model transformer neural network"

    while len(collected) < n_rows:
        params = {
            "search": search_term,
            "filter": f"concepts.id:{concepts_or},from_publication_date:{from_year}-01-01",
            "per-page": min(per_page, 200),
            "cursor": cursor,
            "select": ",".join([
                "id",
                "doi",
                "display_name",
                "publication_year",
                "publication_date",
                "type",
                "cited_by_count",
                "open_access",
                "primary_location",
                "best_oa_location",
                "authorships",
                "concepts",
                "abstract_inverted_index",
            ]),
        }
        data = _get(url, params=params)
        results = data.get("results") or []
        if not results:
            break

        collected.extend(results)

        meta = data.get("meta") or {}
        cursor = meta.get("next_cursor")
        if not cursor:
            break

        # gentle rate limiting
        time.sleep(0.25)

    return collected[:n_rows]

def works_to_markdown_table(works: List[Dict[str, Any]]) -> str:
    """
    Convert works to a Markdown table with one long column: Abstract.
    """
    headers = [
        "OpenAlex ID",
        "Title",
        "Year",
        "Venue",
        "Type",
        "Cited by",
        "Open Access",
        "Authors",
        "Top concepts",
        "Landing page",
        "Abstract (reconstructed)",
    ]

    rows = []
    for w in works:
        wid = w.get("id", "")
        title = w.get("display_name", "")
        year = w.get("publication_year", "")
        wtype = w.get("type", "")

        venue = extract_source_display_name(w)

        cited_by = w.get("cited_by_count", 0)

        oa = (w.get("open_access") or {}).get("is_oa", None)
        oa_str = "yes" if oa is True else ("no" if oa is False else "")

        authors = format_authors(w)
        concepts = format_concepts(w)

        loc = pick_best_location(w)
        landing = loc.get("landing_page_url") or loc.get("pdf_url") or ""
        if not landing and w.get("doi"):
            landing = w["doi"]

        abstract = undo_abstract_inverted_index(w.get("abstract_inverted_index"))

        row = [
            normalize_cell(wid, 200),
            normalize_cell(title, 220),
            normalize_cell(year, 10),
            normalize_cell(venue, 80),
            normalize_cell(wtype, 30),
            normalize_cell(str(cited_by), 20),
            normalize_cell(oa_str, 10),
            normalize_cell(authors, 220),
            normalize_cell(concepts, 220),
            normalize_cell(landing, 200),
            normalize_cell(abstract, 900),  # long column on purpose
        ]
        rows.append(row)

    # Build Markdown
    md = []
    md.append("| " + " | ".join(headers) + " |")
    md.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        md.append("| " + " | ".join(r) + " |")
    md.append("")  # trailing newline

    return "\n".join(md)

def main(
    out_path: str = "openalex_rag_snapshot.md",
    n_rows: int = 800,
    from_year: int = 2018,
):
    works = fetch_works_snapshot(n_rows=n_rows, from_year=from_year)
    md = works_to_markdown_table(works)

    intro = f"""# OpenAlex RAG snapshot (AI, neural networks, LLM-related)

This file is an automatically generated snapshot from the OpenAlex API.
It is designed as lab data for manual chunking of a large Markdown table.

Rows: {len(works)}
Filters: concepts include AI, neural network, language model, plus search bias toward LLM terms.
Abstracts are reconstructed from OpenAlex abstract_inverted_index.

---

"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(intro)
        f.write(md)

    print(f"Wrote: {out_path}  (rows={len(works)})")

if __name__ == "__main__":
    # Adjust size here. 500 to 2000 rows works well for chunking labs.
    main(out_path="openalex_rag_snapshot.md", n_rows=900, from_year=2019)
