# Shelf CLI

Manages the shelf database at `_data/shelf.yml`. The Pydantic schema in `cli.py` is the source of truth.

## Setup

Requires [uv](https://docs.astral.sh/uv/). No install step — uv handles dependencies inline.

## Commands

All commands run from the repo root:

```bash
# List all items (compact table)
uv run scripts/shelf/cli.py list
uv run scripts/shelf/cli.py list --type book --starred
uv run scripts/shelf/cli.py list --status in-progress --json

# Show one item (fuzzy title match)
uv run scripts/shelf/cli.py get "severance"

# Add an item
uv run scripts/shelf/cli.py add \
  --title "Book Title" \
  --type book \
  --author "Author Name" \
  --rating 4 \
  --status finished \
  --tags "tag1,tag2" \
  --link "https://..." \
  --comments "Short note."

# Edit fields on an existing item (only pass what you want to change)
uv run scripts/shelf/cli.py edit "severance" --rating 4 --comments "New note"
uv run scripts/shelf/cli.py edit "severance" --starred true
uv run scripts/shelf/cli.py edit "severance" --tags "sci-fi,drama"  # replaces all tags

# Remove an item
uv run scripts/shelf/cli.py remove "severance"
uv run scripts/shelf/cli.py remove "severance" -y  # skip confirmation

# Search across title, author, tags, comments
uv run scripts/shelf/cli.py search "ai"

# Validate all entries against the Pydantic schema
uv run scripts/shelf/cli.py validate
```

## Schema

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| title | str | yes | | |
| author | str | no | "" | |
| type | enum | yes | | book, post, paper, podcast |
| link | str | no | null | URL to the work |
| rating | int | no | null | 1-5 |
| starred | bool | no | false | Shows in Recommended section |
| visible | bool | no | true | false = hidden from public site, stays in YAML |
| status | enum | no | finished | finished, in-progress, up-next, dropped |
| tags | list[str] | no | [] | CLI accepts comma-separated |
| comments | str | no | "" | Short personal note |
| date_added | date | no | today | Auto-set on add |

Enrichment fields (populated by future scripts): `imdb_score`, `rt_score`, `goodreads_score`, `enriched_at`.

## For LLMs

To make a minor update (e.g. "mark Severance as 4 stars"):
```bash
uv run scripts/shelf/cli.py edit "severance" --rating 4
```

To bulk-add items, call `add` multiple times. To see what's there before editing:
```bash
uv run scripts/shelf/cli.py get "title" --json
```

The `--json` flag on `list`, `get`, and `search` outputs structured JSON for programmatic use.
