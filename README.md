# Domain Factory Template (Hugo)

This repository is the **master template** for launching new SEO-focused domain sites quickly.

It keeps the current Hugo architecture and reusable workflow intact while making domain setup config-driven via:
- `data/domain.yaml`
- `data/theme.yaml`

It preserves:
- Google Analytics integration
- Sedo click tracking
- Homepage latest-post and article archive behavior
- Config-driven style/token system
- Article generation pipeline (`scripts/generate_article.py`)

## Core template architecture

- Hugo layouts/partials: `layouts/`
- Domain config source of truth: `data/domain.yaml`
- Theme token source of truth: `data/theme.yaml`
- Bootstrap/automation scripts: `scripts/`
- Example presets: `data/examples/`

## Quick start: launch a new domain repo in under a minute

1. Clone and enter the template repo.

```bash
git clone <your-new-repo-url>
cd <your-new-repo-folder>
```

2. Bootstrap domain + theme config interactively.

```bash
python scripts/bootstrap_domain.py
```

Prompts include:
- domain name
- brand name
- language
- country
- niche
- audience
- theme preset (`legal`, `industrial`, `organic`, `fintech`)
- Sedo URL
- optional GA measurement ID

3. Validate active + example configs.

```bash
python scripts/validate_config.py
```

4. Dry-run article generation (no external writes/APIs required for content output).

```bash
python scripts/generate_article.py --dry-run
```

5. Run local Hugo server.

```bash
hugo server -D
```

6. Deploy the new domain repo.
- Set secrets (`OPENROUTER_KEY`, `UNSPLASH_KEY`, optional mail credentials for workflow notifications)
- Push to default branch
- Run the publish workflow manually for first content generation

## Domain configuration pattern

Keep domain-specific values in config files:

### `data/domain.yaml`
Contains brand/domain metadata, homepage copy, SEO keywords, CTA/Sedo links, analytics, and content generation settings.

### `data/theme.yaml`
Contains design tokens used by `layouts/partials/theme-vars.css` and downstream style partials.

## Bootstrap system

`scripts/bootstrap_domain.py` creates/updates:
- `data/domain.yaml`
- `data/theme.yaml`

How it works:
- asks for core domain launch fields
- writes a full `data/domain.yaml` with required sections (`homepage`, `seo`, `cta`, `analytics`, `content`)
- copies selected theme preset from `data/examples/theme.<preset>.yaml` into `data/theme.yaml`
- keeps architecture untouched (templates and pipeline continue to read the same paths)

## Example presets

Domain/template examples:
- `data/examples/domain.template.yaml`
- `data/examples/domain.produktionsausfall.de.yaml`

Theme presets:
- `data/examples/theme.legal.yaml`
- `data/examples/theme.industrial.yaml`
- `data/examples/theme.organic.yaml`
- `data/examples/theme.fintech.yaml`

The industrial preset is tuned for German B2B downtime/monitoring positioning (`produktionsausfall`, `maschinenstillstand`, `industrie störung`, `ausfallzeiten`, `produktionsüberwachung`).

## Article generation strategy diversity

`scripts/generate_article.py` includes strategy guards for less repetitive content:
- topic buckets
- duplicate-intent protection
- title similarity guard
- angle diversification
- recent-post awareness in prompts and selection

Existing cleanup, dry-run behavior, image logic, CTA insertion, and workflow compatibility remain intact.
