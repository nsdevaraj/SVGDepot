#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import quote


CSS = """
:root {
  color-scheme: light dark;
  --bg: #0f172a;
  --panel: #111827;
  --panel-soft: #1f2937;
  --text: #e5e7eb;
  --muted: #94a3b8;
  --border: rgba(148, 163, 184, 0.25);
  --accent: #38bdf8;
  --accent-soft: rgba(56, 189, 248, 0.14);
  --success: #22c55e;
  --shadow: 0 18px 60px rgba(15, 23, 42, 0.35);
}

@media (prefers-color-scheme: light) {
  :root {
    --bg: #f8fafc;
    --panel: #ffffff;
    --panel-soft: #f8fafc;
    --text: #0f172a;
    --muted: #475569;
    --border: rgba(15, 23, 42, 0.12);
    --accent-soft: rgba(14, 165, 233, 0.12);
    --shadow: 0 18px 50px rgba(148, 163, 184, 0.22);
  }
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: linear-gradient(180deg, var(--bg) 0%, color-mix(in srgb, var(--bg) 90%, black) 100%);
  color: var(--text);
}

a {
  color: inherit;
}

.shell {
  width: min(1180px, calc(100vw - 32px));
  margin: 0 auto;
  padding: 24px 0 48px;
}

.hero,
.panel,
.item-card,
.icon-card {
  background: color-mix(in srgb, var(--panel) 94%, transparent);
  border: 1px solid var(--border);
  border-radius: 20px;
  box-shadow: var(--shadow);
}

.hero {
  padding: 28px;
  display: grid;
  gap: 18px;
}

.hero h1,
.panel h2,
.item-card h3,
.icon-card h3 {
  margin: 0;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  padding: 8px 12px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent);
  font-size: 0.9rem;
  font-weight: 700;
}

.hero p,
.panel p,
.item-card p,
.icon-card p,
.breadcrumbs,
.small,
.search-note,
code,
pre {
  color: var(--muted);
}

.hero-copy {
  display: grid;
  gap: 12px;
}

.hero-actions,
.stats,
.item-meta,
.icon-actions,
.breadcrumbs {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.button,
button {
  appearance: none;
  border: 1px solid var(--border);
  background: var(--panel-soft);
  color: var(--text);
  border-radius: 12px;
  padding: 10px 14px;
  cursor: pointer;
  font: inherit;
  text-decoration: none;
  transition: 120ms ease;
}

.button:hover,
button:hover {
  border-color: var(--accent);
  transform: translateY(-1px);
}

.button-primary {
  background: var(--accent);
  border-color: var(--accent);
  color: #082f49;
  font-weight: 700;
}

.stats {
  margin: 0;
  padding: 0;
  list-style: none;
}

.stats li {
  min-width: 160px;
  padding: 14px 16px;
  border-radius: 16px;
  background: color-mix(in srgb, var(--panel-soft) 88%, transparent);
  border: 1px solid var(--border);
}

.stats strong {
  display: block;
  font-size: 1.3rem;
  color: var(--text);
}

.panel {
  margin-top: 24px;
  padding: 24px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 18px;
}

.item-card {
  padding: 18px;
  text-decoration: none;
  display: grid;
  gap: 14px;
}

.item-card:hover,
.icon-card:hover {
  border-color: var(--accent);
}

.item-card strong,
.icon-card strong {
  color: var(--text);
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  padding: 6px 10px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--accent-soft) 85%, transparent);
  color: var(--accent);
  font-size: 0.85rem;
  font-weight: 700;
}

.search-wrap {
  display: grid;
  gap: 10px;
  margin: 18px 0 24px;
}

.search-wrap input {
  width: 100%;
  padding: 14px 16px;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: color-mix(in srgb, var(--panel-soft) 92%, transparent);
  color: var(--text);
  font: inherit;
}

.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 18px;
}

.icon-card {
  display: grid;
  grid-template-rows: 160px auto;
  overflow: hidden;
}

.icon-preview {
  display: grid;
  place-items: center;
  padding: 18px;
  background:
    linear-gradient(45deg, rgba(148, 163, 184, 0.08) 25%, transparent 25%) -12px 0 / 24px 24px,
    linear-gradient(-45deg, rgba(148, 163, 184, 0.08) 25%, transparent 25%) -12px 0 / 24px 24px,
    linear-gradient(45deg, transparent 75%, rgba(148, 163, 184, 0.08) 75%) -12px 0 / 24px 24px,
    linear-gradient(-45deg, transparent 75%, rgba(148, 163, 184, 0.08) 75%) -12px 0 / 24px 24px,
    color-mix(in srgb, var(--panel-soft) 88%, transparent);
  border-bottom: 1px solid var(--border);
}

.icon-preview img {
  max-width: 100%;
  max-height: 100%;
}

.icon-body {
  padding: 18px;
  display: grid;
  gap: 12px;
}

.icon-title {
  word-break: break-word;
}

.icon-actions {
  gap: 10px;
}

.icon-actions a,
.icon-actions button {
  font-size: 0.95rem;
}

.utility-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.empty-state {
  padding: 28px;
  text-align: center;
  border: 1px dashed var(--border);
  border-radius: 16px;
  color: var(--muted);
}

pre {
  margin: 0;
  padding: 16px;
  overflow-x: auto;
  border: 1px solid var(--border);
  border-radius: 16px;
  background: color-mix(in srgb, var(--panel-soft) 88%, transparent);
}

.footer {
  margin-top: 24px;
  text-align: center;
  color: var(--muted);
}
"""


PACK_SCRIPT = """
const search = document.querySelector('[data-role="search"]');
const emptyState = document.querySelector('[data-role="empty"]');
const cards = Array.from(document.querySelectorAll('[data-role="icon-card"]'));

if (search) {
  search.addEventListener('input', () => {
    const term = search.value.trim().toLowerCase();
    let visibleCount = 0;

    cards.forEach((card) => {
      const matches = card.dataset.name.includes(term);
      card.hidden = !matches;
      if (matches) {
        visibleCount += 1;
      }
    });

    if (emptyState) {
      emptyState.hidden = visibleCount !== 0;
    }
  });
}

document.querySelectorAll('[data-copy]').forEach((button) => {
  button.addEventListener('click', async () => {
    const url = button.dataset.copy;
    await navigator.clipboard.writeText(url);
    const originalLabel = button.textContent;
    button.textContent = 'Copied';
    setTimeout(() => {
      button.textContent = originalLabel;
    }, 1200);
  });
});
"""


EXCLUDED_TOP_LEVEL_DIRS = {".git", ".github", "_site", "tools"}


@dataclass
class Pack:
  name: str
  slug: str
  relative_dir: str
  svg_files: list[str]

  @property
  def icon_count(self) -> int:
    return len(self.svg_files)


@dataclass
class Category:
  name: str
  slug: str
  packs: list[Pack]

  @property
  def pack_count(self) -> int:
    return len(self.packs)

  @property
  def icon_count(self) -> int:
    return sum(pack.icon_count for pack in self.packs)


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="Generate a GitHub Pages catalog for SVGDepot.")
  parser.add_argument("--repo-root", required=True, type=Path)
  parser.add_argument("--output-dir", required=True, type=Path)
  parser.add_argument("--owner", required=True)
  parser.add_argument("--repo", required=True)
  parser.add_argument("--ref", required=True)
  parser.add_argument("--site-title", default="SVG Catalog")
  return parser.parse_args()


def slugify(value: str) -> str:
  value = value.strip().lower()
  value = re.sub(r"[^a-z0-9]+", "-", value)
  return value.strip("-") or "item"


def unique_slug(name: str, used: set[str]) -> str:
  base_slug = slugify(name)
  slug = base_slug
  counter = 2

  while slug in used:
    slug = f"{base_slug}-{counter}"
    counter += 1

  used.add(slug)
  return slug


def quote_path(path: str) -> str:
  return quote(path, safe="/")


def write_file(path: Path, content: str) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(content, encoding="utf-8")


def relative_css_path(depth: int) -> str:
  prefix = "../" * depth
  return f"{prefix}assets/catalog.css"


def page_template(title: str, css_path: str, body: str, script: str = "") -> str:
  script_block = f"\n<script>\n{script}\n</script>" if script else ""
  return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{css_path}">
</head>
<body>
  <div class="shell">
    {body}
    <p class="footer">Generated from the repository structure. Use jsDelivr links for CDN consumption.</p>
  </div>{script_block}
</body>
</html>
"""


def collect_catalog(repo_root: Path) -> list[Category]:
  categories: list[Category] = []
  category_slugs: set[str] = set()

  top_level_dirs = sorted(
    path for path in repo_root.iterdir() if path.is_dir() and path.name not in EXCLUDED_TOP_LEVEL_DIRS
  )

  for category_dir in top_level_dirs:
    pack_slugs: set[str] = set()
    packs: list[Pack] = []

    for pack_dir in sorted(path for path in category_dir.iterdir() if path.is_dir()):
      svg_files = sorted(path.name for path in pack_dir.iterdir() if path.is_file() and path.suffix.lower() == ".svg")
      if not svg_files:
        continue

      packs.append(
        Pack(
          name=pack_dir.name,
          slug=unique_slug(pack_dir.name, pack_slugs),
          relative_dir=pack_dir.relative_to(repo_root).as_posix(),
          svg_files=svg_files,
        )
      )

    if not packs:
      continue

    categories.append(
      Category(
        name=category_dir.name,
        slug=unique_slug(category_dir.name, category_slugs),
        packs=packs,
      )
    )

  return categories


def sum_icons(categories: Iterable[Category]) -> int:
  return sum(category.icon_count for category in categories)


def home_body(
  categories: list[Category],
  owner: str,
  repo: str,
  ref: str,
  site_title: str,
) -> str:
  category_cards = "\n".join(
    f"""
    <a class="item-card" href="categories/{category.slug}/">
      <span class="pill">Category</span>
      <h3>{html.escape(category.name)}</h3>
      <div class="item-meta">
        <span><strong>{category.pack_count:,}</strong> packs</span>
        <span><strong>{category.icon_count:,}</strong> SVGs</span>
      </div>
    </a>
    """
    for category in categories
  )

  example_path = ""
  if categories and categories[0].packs and categories[0].packs[0].svg_files:
    example_path = (
      f"{categories[0].packs[0].relative_dir}/{categories[0].packs[0].svg_files[0]}"
    )

  example_url = f"https://cdn.jsdelivr.net/gh/{owner}/{repo}@{ref}/{quote_path(example_path)}" if example_path else ""
  repo_url = f"https://github.com/{owner}/{repo}"

  return f"""
  <section class="hero">
    <span class="eyebrow">GitHub Pages catalog + jsDelivr CDN</span>
    <div class="hero-copy">
      <h1>{html.escape(site_title)}</h1>
      <p>Browse the repository by category and pack, then copy a CDN URL for any SVG without changing the source folder layout.</p>
    </div>
    <ul class="stats">
      <li><strong>{len(categories):,}</strong> categories</li>
      <li><strong>{sum(category.pack_count for category in categories):,}</strong> packs</li>
      <li><strong>{sum_icons(categories):,}</strong> SVGs</li>
    </ul>
    <div class="hero-actions">
      <a class="button button-primary" href="{repo_url}" target="_blank" rel="noreferrer">Open repository</a>
      <a class="button" href="api/catalog.json">Catalog JSON</a>
      <a class="button" href="https://www.jsdelivr.com/github" target="_blank" rel="noreferrer">jsDelivr docs</a>
    </div>
  </section>

  <section class="panel">
    <div class="utility-row">
      <div>
        <h2>CDN pattern</h2>
        <p>Pin to a tag for stable production URLs, or use the current branch while iterating.</p>
      </div>
    </div>
    <pre>https://cdn.jsdelivr.net/gh/{html.escape(owner)}/{html.escape(repo)}@{html.escape(ref)}/&lt;category&gt;/&lt;pack&gt;/&lt;file&gt;.svg</pre>
    {"<pre>" + html.escape(example_url) + "</pre>" if example_url else ""}
  </section>

  <section class="panel">
    <div class="utility-row">
      <div>
        <h2>Browse categories</h2>
        <p>Drill down from broad themes to individual packs and files.</p>
      </div>
    </div>
    <div class="grid">
      {category_cards}
    </div>
  </section>
  """


def category_body(category: Category) -> str:
  pack_cards = "\n".join(
    f"""
    <a class="item-card" href="../../packs/{category.slug}/{pack.slug}/">
      <span class="pill">Pack</span>
      <h3>{html.escape(pack.name)}</h3>
      <div class="item-meta">
        <span><strong>{pack.icon_count:,}</strong> SVGs</span>
        <span class="small">{html.escape(pack.relative_dir)}</span>
      </div>
    </a>
    """
    for pack in category.packs
  )

  return f"""
  <nav class="breadcrumbs">
    <a href="../../">Home</a>
    <span>/</span>
    <span>{html.escape(category.name)}</span>
  </nav>

  <section class="hero">
    <span class="eyebrow">Category</span>
    <div class="hero-copy">
      <h1>{html.escape(category.name)}</h1>
      <p>Browse icon packs in this category and open a pack page for searchable SVG previews and CDN links.</p>
    </div>
    <ul class="stats">
      <li><strong>{category.pack_count:,}</strong> packs</li>
      <li><strong>{category.icon_count:,}</strong> SVGs</li>
    </ul>
  </section>

  <section class="panel">
    <div class="utility-row">
      <div>
        <h2>Icon packs</h2>
        <p>Each pack page lists every SVG in that folder.</p>
      </div>
    </div>
    <div class="grid">
      {pack_cards}
    </div>
  </section>
  """


def pack_body(pack: Pack, category: Category, owner: str, repo: str, ref: str) -> str:
  icon_cards: list[str] = []

  for file_name in pack.svg_files:
    relative_path = f"{pack.relative_dir}/{file_name}"
    encoded_relative_path = quote_path(relative_path)
    cdn_url = f"https://cdn.jsdelivr.net/gh/{owner}/{repo}@{ref}/{encoded_relative_path}"
    github_url = f"https://github.com/{owner}/{repo}/blob/{ref}/{encoded_relative_path}"
    icon_label = file_name[:-4] if file_name.lower().endswith(".svg") else file_name

    icon_cards.append(
      f"""
      <article class="icon-card" data-role="icon-card" data-name="{html.escape(icon_label.lower())}">
        <a class="icon-preview" href="{cdn_url}" target="_blank" rel="noreferrer">
          <img loading="lazy" src="{cdn_url}" alt="{html.escape(icon_label)}">
        </a>
        <div class="icon-body">
          <div>
            <h3 class="icon-title">{html.escape(icon_label)}</h3>
            <p class="small">{html.escape(relative_path)}</p>
          </div>
          <div class="icon-actions">
            <a class="button button-primary" href="{cdn_url}" target="_blank" rel="noreferrer">Open CDN</a>
            <button type="button" data-copy="{cdn_url}">Copy CDN</button>
            <a class="button" href="{github_url}" target="_blank" rel="noreferrer">View source</a>
          </div>
        </div>
      </article>
      """
    )

  icon_cards_markup = "\n".join(icon_cards)
  pack_prefix = f"https://cdn.jsdelivr.net/gh/{owner}/{repo}@{ref}/{quote_path(pack.relative_dir)}/"

  return f"""
  <nav class="breadcrumbs">
    <a href="../../../">Home</a>
    <span>/</span>
    <a href="../../../categories/{category.slug}/">{html.escape(category.name)}</a>
    <span>/</span>
    <span>{html.escape(pack.name)}</span>
  </nav>

  <section class="hero">
    <span class="eyebrow">Pack</span>
    <div class="hero-copy">
      <h1>{html.escape(pack.name)}</h1>
      <p>Search within this pack, preview SVGs, and copy their jsDelivr URLs.</p>
    </div>
    <ul class="stats">
      <li><strong>{pack.icon_count:,}</strong> SVGs</li>
      <li><strong>{html.escape(category.name)}</strong> category</li>
    </ul>
  </section>

  <section class="panel">
    <div class="utility-row">
      <div>
        <h2>Pack location</h2>
        <p>{html.escape(pack.relative_dir)}</p>
      </div>
    </div>
    <pre>{html.escape(pack_prefix)}&lt;file&gt;.svg</pre>
  </section>

  <section class="panel">
    <div class="utility-row">
      <div>
        <h2>Browse SVGs</h2>
        <p>Filter by file name to narrow large packs quickly.</p>
      </div>
    </div>
    <div class="search-wrap">
      <input type="search" data-role="search" placeholder="Search this pack">
      <p class="search-note">Start typing a file name such as <code>arrow</code>, <code>logo</code>, or <code>house</code>.</p>
    </div>
    <div class="empty-state" data-role="empty" hidden>No SVGs match the current search.</div>
    <div class="icon-grid">
      {icon_cards_markup}
    </div>
  </section>
  """


def manifest(categories: list[Category], owner: str, repo: str, ref: str) -> str:
  payload = {
    "owner": owner,
    "repo": repo,
    "ref": ref,
    "categories": [
      {
        "name": category.name,
        "slug": category.slug,
        "packCount": category.pack_count,
        "iconCount": category.icon_count,
        "packs": [
          {
            "name": pack.name,
            "slug": pack.slug,
            "relativeDir": pack.relative_dir,
            "iconCount": pack.icon_count,
          }
          for pack in category.packs
        ],
      }
      for category in categories
    ],
  }
  return json.dumps(payload, indent=2)


def generate_site(
  repo_root: Path,
  output_dir: Path,
  owner: str,
  repo: str,
  ref: str,
  site_title: str,
) -> None:
  categories = collect_catalog(repo_root)
  if not categories:
    raise RuntimeError("No SVG categories were found. Expected category/pack/file.svg structure.")

  if output_dir.exists():
    shutil.rmtree(output_dir)

  write_file(output_dir / ".nojekyll", "")
  write_file(output_dir / "assets" / "catalog.css", CSS.strip() + "\n")
  write_file(output_dir / "api" / "catalog.json", manifest(categories, owner, repo, ref) + "\n")

  home_html = page_template(
    title=site_title,
    css_path=relative_css_path(0),
    body=home_body(categories, owner, repo, ref, site_title),
  )
  write_file(output_dir / "index.html", home_html)

  for category in categories:
    category_html = page_template(
      title=f"{category.name} - {site_title}",
      css_path=relative_css_path(2),
      body=category_body(category),
    )
    write_file(output_dir / "categories" / category.slug / "index.html", category_html)

    for pack in category.packs:
      pack_html = page_template(
        title=f"{pack.name} - {site_title}",
        css_path=relative_css_path(3),
        body=pack_body(pack, category, owner, repo, ref),
        script=PACK_SCRIPT.strip(),
      )
      write_file(output_dir / "packs" / category.slug / pack.slug / "index.html", pack_html)


def main() -> None:
  args = parse_args()
  generate_site(
    repo_root=args.repo_root.resolve(),
    output_dir=args.output_dir.resolve(),
    owner=args.owner,
    repo=args.repo,
    ref=args.ref,
    site_title=args.site_title,
  )


if __name__ == "__main__":
  main()
