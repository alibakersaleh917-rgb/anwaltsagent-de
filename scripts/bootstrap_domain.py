#!/usr/bin/env python3
"""Fast-start initializer for domain-factory-template configs."""

from __future__ import annotations

from pathlib import Path

from domain_config import parse_simple_yaml

DOMAIN_TEMPLATE_PATH = Path("data/examples/domain.template.yaml")
THEME_PRESETS = {
    "legal": Path("data/examples/theme.legal.yaml"),
    "industrial": Path("data/examples/theme.industrial.yaml"),
    "organic": Path("data/examples/theme.organic.yaml"),
    "fintech": Path("data/examples/theme.fintech.yaml"),
}


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def dump_yaml(data, indent: int = 0) -> str:
    lines: list[str] = []
    pad = " " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(dump_yaml(value, indent + 2))
            else:
                if isinstance(value, str):
                    lines.append(f"{pad}{key}: {yaml_quote(value)}")
                else:
                    lines.append(f"{pad}{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(dump_yaml(item, indent + 2))
            elif isinstance(item, str):
                lines.append(f"{pad}- {yaml_quote(item)}")
            else:
                lines.append(f"{pad}- {item}")

    return "\n".join(lines)


def load_domain_template() -> dict:
    if not DOMAIN_TEMPLATE_PATH.exists():
        raise SystemExit(f"Missing template: {DOMAIN_TEMPLATE_PATH}")
    return parse_simple_yaml(DOMAIN_TEMPLATE_PATH)


def apply_inputs_to_domain(template: dict, values: dict[str, str]) -> dict:
    domain = dict(template)
    homepage = dict(domain.get("homepage") or {})
    seo = dict(domain.get("seo") or {})
    cta = dict(domain.get("cta") or {})
    analytics = dict(domain.get("analytics") or {})
    content = dict(domain.get("content") or {})

    domain_name = values["domain"]
    brand_name = values["brand_name"]
    language = values["language"]
    country = values["country"]
    niche = values["niche"]
    audience = values["audience"]
    sedo_url = values["sedo_url"]
    ga_id = values["ga_measurement_id"]

    domain["domain"] = domain_name
    domain["brand_name"] = brand_name
    domain["language"] = language
    domain["country"] = country
    domain["niche"] = niche
    domain["audience"] = audience
    domain["brand_positioning"] = (
        f"{brand_name} positioniert sich als klare, moderne Marke für {niche} in {country}."
    )

    homepage["title"] = f"{brand_name} — Domain Factory Launch"
    homepage["description"] = f"{brand_name}: Template-Launch für {niche} in {country}."
    homepage["headline"] = f"Die <strong>passende Domain</strong> für {niche}"
    homepage["subheadline"] = (
        f"{brand_name} unterstützt den schnellen Start einer klaren Marken- und Content-Strategie für {audience}."
    )

    seo["archive_description"] = f"Alle Beiträge rund um {niche} in {country}."
    seo["article_default_description"] = f"Artikel auf {brand_name}"
    seo["keywords"] = [
        f"{niche} {country}",
        f"{niche} Anbieter",
        f"{niche} Vergleich",
        f"{niche} Kosten",
        f"{niche} Tipps",
    ]

    cta["sedo_url"] = sedo_url
    cta["contact_heading"] = f"Interesse an {domain_name}?"
    cta["contact_body"] = (
        f"Wenn Sie in dieser Nische eine starke Marke aufbauen möchten, ist {domain_name} ein klarer Startpunkt."
    )
    cta["single_article_text"] = (
        f"Wenn Sie eine Nischenmarke aufbauen möchten, kann <strong>{domain_name}</strong> ein prägnanter Domain-Startpunkt sein."
    )

    analytics["ga_measurement_id"] = ga_id

    content["seo_keyword_hints"] = f"{niche}, vergleich, kosten, auswahl, tipps"
    content["image_style_hints"] = f"{niche}; professional; modern; {country}"
    content["article_cta"] = (
        f"Wenn Sie eine starke Nischenmarke in {country} aufbauen möchten, kann **{domain_name}** eine interessante Domain-Basis sein."
    )

    domain["homepage"] = homepage
    domain["seo"] = seo
    domain["cta"] = cta
    domain["analytics"] = analytics
    domain["content"] = content

    return domain


def main() -> None:
    print("Domain Factory Bootstrap")
    print("------------------------")

    domain_name = ask("Domain name", "example.com")
    brand_name = ask("Brand name", "Example")
    language = ask("Language", "de")
    country = ask("Country", "Deutschland")
    niche = ask("Niche", "Digitale Dienstleistungen")
    audience = ask("Audience", "Unternehmen und Privatpersonen")
    theme_preset = ask("Theme preset (legal/industrial/organic/fintech)", "legal").lower()
    sedo_url = ask("Sedo URL", f"https://sedo.com/search/details/?domain={domain_name}")
    ga_measurement_id = ask("GA measurement ID (optional)", "")

    if theme_preset not in THEME_PRESETS:
        raise SystemExit(f"Unknown theme preset '{theme_preset}'. Expected one of: {', '.join(THEME_PRESETS)}")

    theme_source = THEME_PRESETS[theme_preset]
    if not theme_source.exists():
        raise SystemExit(f"Missing theme preset: {theme_source}")

    domain_data = apply_inputs_to_domain(
        load_domain_template(),
        {
            "domain": domain_name,
            "brand_name": brand_name,
            "language": language,
            "country": country,
            "niche": niche,
            "audience": audience,
            "sedo_url": sedo_url,
            "ga_measurement_id": ga_measurement_id,
        },
    )

    domain_path = Path("data/domain.yaml")
    theme_path = Path("data/theme.yaml")

    domain_path.write_text(dump_yaml(domain_data) + "\n", encoding="utf-8")
    theme_path.write_text(theme_source.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"✅ Updated {domain_path} from {DOMAIN_TEMPLATE_PATH}")
    print(f"✅ Updated {theme_path} from {theme_source}")
    print("\nNext steps:")
    print("1) python scripts/validate_config.py")
    print(f'2) python scripts/generate_article.py --dry-run --keyword "{niche}"')
    print("3) hugo server --disableFastRender")


if __name__ == "__main__":
    main()
