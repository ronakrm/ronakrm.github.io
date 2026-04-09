# /// script
# requires-python = ">=3.10"
# dependencies = ["pydantic>=2.0", "pyyaml>=6.0"]
# ///
"""
Shelf CLI — manage _data/shelf.yml

Usage:
    uv run scripts/shelf/cli.py list [--type TYPE] [--status STATUS] [--starred] [--json]
    uv run scripts/shelf/cli.py get TITLE [--json]
    uv run scripts/shelf/cli.py add --title TITLE --type TYPE [OPTIONS]
    uv run scripts/shelf/cli.py edit TITLE --field VALUE [--field VALUE ...]
    uv run scripts/shelf/cli.py remove TITLE
    uv run scripts/shelf/cli.py validate
    uv run scripts/shelf/cli.py search QUERY [--json]

Run with --help on any subcommand for details.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

SHELF_PATH = Path(__file__).resolve().parents[2] / "_data" / "shelf.yml"

ItemType = Literal["book", "post", "paper", "podcast"]
ItemStatus = Literal["finished", "in-progress", "up-next", "dropped"]


class ShelfItem(BaseModel):
    """A single entry on the shelf."""

    title: str
    author: str = ""
    type: ItemType
    link: Optional[str] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    starred: bool = False
    visible: bool = True
    status: ItemStatus = "finished"
    tags: list[str] = Field(default_factory=list)
    comments: str = ""
    date_added: date = Field(default_factory=date.today)

    # Third-party enrichment (populated by future scripts)
    imdb_score: Optional[float] = None
    rt_score: Optional[int] = None
    goodreads_score: Optional[float] = None
    enriched_at: Optional[date] = None

    @field_validator("tags", mode="before")
    @classmethod
    def coerce_tags(cls, v):
        if isinstance(v, str):
            return [t.strip() for t in v.split(",") if t.strip()]
        return v

    @field_validator("rating", mode="before")
    @classmethod
    def coerce_rating(cls, v):
        if v == "" or v is None:
            return None
        return int(v)

    @field_validator("link", mode="before")
    @classmethod
    def coerce_link(cls, v):
        if v == "" or v is None:
            return None
        return v


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------


def load_shelf() -> list[ShelfItem]:
    """Load and validate the shelf YAML."""
    if not SHELF_PATH.exists():
        return []
    raw = yaml.safe_load(SHELF_PATH.read_text()) or []
    items = []
    for i, entry in enumerate(raw):
        try:
            items.append(ShelfItem(**entry))
        except Exception as e:
            print(f"Warning: entry {i} ({entry.get('title', '?')}): {e}", file=sys.stderr)
    return items


def save_shelf(items: list[ShelfItem]) -> None:
    """Write items back to YAML, preserving the header comment."""
    header = (
        "# Shelf Database\n"
        "# Schema: see ShelfItem in scripts/shelf/cli.py\n"
        "# Manage with: uv run scripts/shelf/cli.py --help\n\n"
    )

    def represent_none(dumper, _):
        return dumper.represent_scalar("tag:yaml.org,2002:null", "")

    yaml.add_representer(type(None), represent_none)

    records = []
    for item in items:
        d = item.model_dump(mode="json")
        # Drop enrichment fields if empty
        for k in ("imdb_score", "rt_score", "goodreads_score", "enriched_at"):
            if d.get(k) is None:
                del d[k]
        records.append(d)

    body = yaml.dump(records, default_flow_style=False, sort_keys=False, allow_unicode=True)
    SHELF_PATH.write_text(header + body)


def find_item(items: list[ShelfItem], title: str) -> tuple[int, ShelfItem] | None:
    """Find item by title (case-insensitive substring match)."""
    title_lower = title.lower()
    matches = [(i, item) for i, item in enumerate(items) if title_lower in item.title.lower()]
    if len(matches) == 0:
        return None
    if len(matches) == 1:
        return matches[0]
    # Prefer exact match
    for i, item in matches:
        if item.title.lower() == title_lower:
            return (i, item)
    # Ambiguous
    print(f"Ambiguous title '{title}'. Matches:", file=sys.stderr)
    for _, item in matches:
        print(f"  - {item.title}", file=sys.stderr)
    sys.exit(1)


def format_item(item: ShelfItem, verbose: bool = True) -> str:
    """Human-readable single-item display."""
    lines = [f"  {item.title}"]
    if item.author:
        lines.append(f"  Author:  {item.author}")
    lines.append(f"  Type:    {item.type}")
    lines.append(f"  Status:  {item.status}")
    if item.rating:
        lines.append(f"  Rating:  {'*' * item.rating}{'.' * (5 - item.rating)}")
    if item.starred:
        lines.append(f"  Starred: yes")
    if not item.visible:
        lines.append(f"  Visible: no (hidden from site)")
    if item.link:
        lines.append(f"  Link:    {item.link}")
    if item.tags:
        lines.append(f"  Tags:    {', '.join(item.tags)}")
    if item.comments and verbose:
        lines.append(f"  Notes:   {item.comments}")
    lines.append(f"  Added:   {item.date_added}")
    # Enrichment
    scores = []
    if item.imdb_score is not None:
        scores.append(f"IMDB {item.imdb_score}")
    if item.rt_score is not None:
        scores.append(f"RT {item.rt_score}%")
    if item.goodreads_score is not None:
        scores.append(f"GR {item.goodreads_score}")
    if scores:
        lines.append(f"  Scores:  {', '.join(scores)}")
    return "\n".join(lines)


def format_row(item: ShelfItem) -> str:
    """Compact one-line display."""
    star = "*" if item.starred else " "
    rating = f"{'*' * item.rating}{'.' * (5 - item.rating)}" if item.rating else "     "
    vis = " " if item.visible else "H"
    return f" {star}{vis} {rating}  {item.type:<8} {item.status:<12} {item.title}"


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_list(args):
    items = load_shelf()
    if args.type:
        items = [i for i in items if i.type == args.type]
    if args.status:
        items = [i for i in items if i.status == args.status]
    if args.starred:
        items = [i for i in items if i.starred]

    if args.json:
        print(json.dumps([i.model_dump(mode="json") for i in items], indent=2))
        return

    if not items:
        print("No items found.")
        return

    print(f" {'':2} {'Rating':<7} {'Type':<8} {'Status':<12} Title")
    print(f" {'':2} {'------':<7} {'----':<8} {'------':<12} -----")
    for item in items:
        print(format_row(item))
    print(f"\n{len(items)} items")


def cmd_get(args):
    items = load_shelf()
    result = find_item(items, args.title)
    if result is None:
        print(f"Not found: '{args.title}'", file=sys.stderr)
        sys.exit(1)
    _, item = result
    if args.json:
        print(json.dumps(item.model_dump(mode="json"), indent=2))
    else:
        print(format_item(item))


def cmd_add(args):
    items = load_shelf()

    # Check for duplicate
    for existing in items:
        if existing.title.lower() == args.title.lower():
            print(f"Already exists: '{existing.title}'", file=sys.stderr)
            sys.exit(1)

    data = {
        "title": args.title,
        "type": args.type,
        "author": args.author or "",
        "link": args.link,
        "rating": args.rating,
        "starred": args.starred,
        "visible": not args.hidden,
        "status": args.status,
        "tags": [t.strip() for t in args.tags.split(",")] if args.tags else [],
        "comments": args.comments or "",
        "date_added": date.today(),
    }

    item = ShelfItem(**data)
    items.append(item)
    save_shelf(items)
    print(f"Added:")
    print(format_item(item))


def cmd_edit(args):
    items = load_shelf()
    result = find_item(items, args.title)
    if result is None:
        print(f"Not found: '{args.title}'", file=sys.stderr)
        sys.exit(1)
    idx, item = result

    updates = {}
    for field_name in ShelfItem.model_fields:
        val = getattr(args, field_name, None)
        if val is not None:
            updates[field_name] = val

    if not updates:
        print("No fields to update. Use --field VALUE flags.", file=sys.stderr)
        print(f"Editable fields: {', '.join(ShelfItem.model_fields.keys())}", file=sys.stderr)
        sys.exit(1)

    updated = item.model_copy(update=updates)
    items[idx] = updated
    save_shelf(items)
    print(f"Updated:")
    print(format_item(updated))


def cmd_remove(args):
    items = load_shelf()
    result = find_item(items, args.title)
    if result is None:
        print(f"Not found: '{args.title}'", file=sys.stderr)
        sys.exit(1)
    idx, item = result

    if not args.yes:
        print(f"Remove '{item.title}'? [y/N] ", end="")
        if input().strip().lower() != "y":
            print("Cancelled.")
            return

    items.pop(idx)
    save_shelf(items)
    print(f"Removed: {item.title}")


def cmd_validate(args):
    items = load_shelf()
    errors = 0
    for item in items:
        issues = []
        if not item.title:
            issues.append("missing title")
        if item.rating is not None and not (1 <= item.rating <= 5):
            issues.append(f"rating {item.rating} out of range 1-5")
        if item.link and not item.link.startswith("http"):
            issues.append(f"link doesn't look like a URL: {item.link}")
        if issues:
            print(f"  {item.title}: {', '.join(issues)}")
            errors += 1

    if errors:
        print(f"\n{errors} item(s) with issues.")
        sys.exit(1)
    else:
        print(f"All {len(items)} items valid.")


def cmd_search(args):
    items = load_shelf()
    query = args.query.lower()
    matches = [
        i
        for i in items
        if query in i.title.lower()
        or query in i.author.lower()
        or query in i.comments.lower()
        or any(query in t.lower() for t in i.tags)
    ]

    if args.json:
        print(json.dumps([i.model_dump(mode="json") for i in matches], indent=2))
        return

    if not matches:
        print("No matches.")
        return

    for item in matches:
        print(format_item(item, verbose=False))
        print()


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(description="Manage the shelf database (_data/shelf.yml)")
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p = sub.add_parser("list", aliases=["ls"], help="List items")
    p.add_argument("--type", choices=["book", "post", "paper", "podcast"])
    p.add_argument("--status", choices=["finished", "in-progress", "up-next", "dropped"])
    p.add_argument("--starred", action="store_true")
    p.add_argument("--json", action="store_true")

    # get
    p = sub.add_parser("get", help="Show one item by title")
    p.add_argument("title")
    p.add_argument("--json", action="store_true")

    # add
    p = sub.add_parser("add", help="Add a new item")
    p.add_argument("--title", required=True)
    p.add_argument("--type", required=True, choices=["book", "post", "paper", "podcast"])
    p.add_argument("--author", default="")
    p.add_argument("--link")
    p.add_argument("--rating", type=int, choices=[1, 2, 3, 4, 5])
    p.add_argument("--starred", action="store_true")
    p.add_argument("--hidden", action="store_true", help="Set visible=false")
    p.add_argument("--status", default="finished", choices=["finished", "in-progress", "up-next", "dropped"])
    p.add_argument("--tags", help="Comma-separated tags")
    p.add_argument("--comments", default="")

    # edit
    p = sub.add_parser("edit", help="Edit an existing item")
    p.add_argument("title", help="Title to match (case-insensitive substring)")
    p.add_argument("--title", dest="new_title")  # rename
    p.add_argument("--author")
    p.add_argument("--type", choices=["book", "post", "paper", "podcast"])
    p.add_argument("--link")
    p.add_argument("--rating", type=int, choices=[1, 2, 3, 4, 5])
    p.add_argument("--starred", choices=["true", "false"])
    p.add_argument("--visible", choices=["true", "false"])
    p.add_argument("--status", choices=["finished", "in-progress", "up-next", "dropped"])
    p.add_argument("--tags", help="Comma-separated (replaces existing)")
    p.add_argument("--comments")

    # remove
    p = sub.add_parser("remove", aliases=["rm"], help="Remove an item")
    p.add_argument("title")
    p.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")

    # validate
    sub.add_parser("validate", help="Validate all entries against the schema")

    # search
    p = sub.add_parser("search", help="Search by title, author, tags, comments")
    p.add_argument("query")
    p.add_argument("--json", action="store_true")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Coerce edit boolean fields
    if args.command == "edit":
        updates = {}
        if args.new_title is not None:
            updates["title"] = args.new_title
        if args.author is not None:
            updates["author"] = args.author
        if args.type is not None:
            updates["type"] = args.type
        if args.link is not None:
            updates["link"] = args.link
        if args.rating is not None:
            updates["rating"] = args.rating
        if args.starred is not None:
            updates["starred"] = args.starred == "true"
        if args.visible is not None:
            updates["visible"] = args.visible == "true"
        if args.status is not None:
            updates["status"] = args.status
        if args.tags is not None:
            updates["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
        if args.comments is not None:
            updates["comments"] = args.comments

        # Replace args fields with processed updates
        for k, v in updates.items():
            setattr(args, k, v)

    dispatch = {
        "list": cmd_list,
        "ls": cmd_list,
        "get": cmd_get,
        "add": cmd_add,
        "edit": cmd_edit,
        "remove": cmd_remove,
        "rm": cmd_remove,
        "validate": cmd_validate,
        "search": cmd_search,
    }

    dispatch[args.command](args)


if __name__ == "__main__":
    main()
