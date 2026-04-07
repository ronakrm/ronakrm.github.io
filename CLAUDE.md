# Ronak Mehta — Personal Site & Blog

Jekyll site hosted on GitHub Pages.

## Site Structure

- `_posts/` — Published posts (date-prefixed markdown files)
- `_drafts/` — Draft posts and writing workspace (see below)
- `_drafts/style_guide.md` — **Read this before helping write or edit any post.** Writing voice, structure, examples.
- `_drafts/live_refs/` — Copies of published posts for style reference. Do NOT edit.
- `assets/blogfigs/` — Post figures, organized by post slug (e.g., `assets/blogfigs/interp-design/`)
- `_layouts/`, `_includes/`, `_sass/` — Theme (custom minima)
- `_config.yml` — Site config: kramdown markdown, KaTeX for math

## Draft Folder Convention

Each draft is a **folder** inside `_drafts/`:

```
_drafts/
  my-post-slug/
    my-post-slug.md        # The draft itself
    notes.md               # Rough notes, scratchpad
    refs.md                # Links, bibliography, related papers
    outline.md             # Structure planning
    ...                    # Any other supporting files
```

Only the `.md` file matching the folder name is the actual draft. Everything else is supporting material — reference links, bibliography management, rough notes, outlines, whatever is useful. Jekyll ignores non-post files in subdirectories.

## Frontmatter Format

```yaml
---
layout: post
title: "Post Title Here"
excerpt: "One sentence summary."
tags: tag1 tag2 tag3
date: YYYY-MM-DD
katex: True
---
```

- `katex: True` if the post uses any math.
- `tags:` space-separated, lowercase. Common: interpretability, safety, math, viz, fairness, statistics, hypothesis-testing.
- `excerpt:` should work as a standalone sentence. Often reused in the opening.
- Optional: `modified_date: YYYY-MM-DD` for significant post-publication updates.

## Drafting Workflow

### Phase 1: Writing (Obsidian or Claude)
- Focus on **prose and math**. Standard markdown with `$...$` / `$$...$$`.
- Use placeholders for figures: `![FIGURE: description of what goes here](TODO)`
- Standard markdown links for external references.
- Don't worry about Jekyll-specific syntax yet (kramdown classes, liquid tags).
- Supporting material (notes, refs, outlines) goes in the draft's folder alongside the main markdown.

### Phase 2: Production (IDE / Jekyll)
- Add/finalize frontmatter.
- Create figures, place in `assets/blogfigs/<post-slug>/`.
- Replace figure placeholders with paths and kramdown attributes (`{:.centered width="400px"}`).
- Add kramdown formatting: `{:.no_toc}`, `{:toc}`, centered captions.
- Add any liquid tags (`{{ page.excerpt }}`, admonition divs, etc.).
- Preview: `bundle exec jekyll serve --drafts`
- Publish: move from `_drafts/<slug>/<slug>.md` to `_posts/YYYY-MM-DD-<slug>.md`

## Cross-Posting

Posts go on personal site first, then LessWrong (sometimes EA Forum). LessWrong versions may have appendices or supplementary material linked separately.

## When Helping Write

1. Read `_drafts/style_guide.md` first.
2. Match the voice: conversational, technically precise, opinionated, honest about uncertainty.
3. Don't over-polish. The posts have a "working through ideas publicly" quality that is intentional.
4. Suggest structure but don't impose rigid templates. Each post finds its own shape.
5. Math is a first-class citizen, not an appendix. Use it to drive arguments.
6. Flag where figures/animations would strengthen the argument, but leave as placeholders.
7. Don't add generic introductions, mechanical transitions, or restating-conclusions.
