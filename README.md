# SVGDepot

SVGDepot is a folder-organized SVG library that can be consumed directly from a CDN and browsed through a generated GitHub Pages catalog.

## What this setup gives you

- Direct asset delivery through jsDelivr from this GitHub repository
- A generated GitHub Pages website for category -> pack -> SVG navigation
- Zero changes to the existing SVG folder structure
- Automatic catalog publishing on pushes to the default branch

## CDN usage

Use jsDelivr for production-friendly asset delivery:

```text
https://cdn.jsdelivr.net/gh/<owner>/<repo>@<ref>/<category>/<pack>/<file>.svg
```

Example:

```text
https://cdn.jsdelivr.net/gh/<owner>/<repo>@main/Art%2C%20Design%20%26%20Patterns/abstract-icons/335745-graphic-stitching.svg
```

For stable URLs, prefer tags or releases instead of a moving branch:

```text
https://cdn.jsdelivr.net/gh/<owner>/<repo>@v1.0.0/<category>/<pack>/<file>.svg
```

## GitHub Pages catalog

The workflow at [.github/workflows/publish-catalog.yml](/home/devtest/Documents/Repo/SVGDepot/.github/workflows/publish-catalog.yml) generates a static catalog with:

- category counts
- pack counts
- per-pack SVG previews
- copyable CDN URLs
- links back to the source file on GitHub
- a machine-readable catalog manifest at `api/catalog.json`

After enabling GitHub Pages for Actions, the catalog will be available at:

```text
https://<owner>.github.io/<repo>/
```

## Publishing steps

1. Push this repository to GitHub.
2. In repository settings, open **Pages** and set the source to **GitHub Actions**.
3. Push to the default branch or run the **Publish SVG catalog** workflow manually.
4. Share the GitHub Pages URL for browsing and the jsDelivr URL pattern for direct consumption.

## Local generation

You can generate the catalog locally before pushing:

```bash
python tools/generate_catalog.py --repo-root . --output-dir _site --owner <owner> --repo <repo> --ref main
```

Then open [_site/index.html](/home/devtest/Documents/Repo/SVGDepot/_site/index.html) in a browser to preview the navigation experience.
