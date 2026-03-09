from pathlib import Path
import sys

from domain_config import parse_simple_yaml


def fail(msg: str):
    print(f"ERROR: {msg}")
    sys.exit(1)


def require_keys(obj: dict, keys: list[str], prefix: str):
    for k in keys:
        if k not in obj or obj[k] in (None, "", []):
            fail(f"Missing required key: {prefix}{k}")


def validate_domain_file(path: Path):
    domain = parse_simple_yaml(path)
    require_keys(domain, ["domain", "brand_name", "niche", "country", "language", "audience"], f"{path}:domain.")
    require_keys(domain, ["homepage", "seo", "cta", "analytics", "content"], f"{path}:domain.")
    require_keys(domain.get("analytics", {}), ["event_name", "event_category"], f"{path}:domain.analytics.")
    require_keys(domain.get("content", {}), ["article_tone", "image_style_hints", "article_cta"], f"{path}:domain.content.")


def validate_theme_file(path: Path):
    theme = parse_simple_yaml(path)
    require_keys(theme, ["palette", "background", "effects", "button_style", "card_style"], f"{path}:theme.")


def main():
    domain_path = Path("data/domain.yaml")
    theme_path = Path("data/theme.yaml")

    if not domain_path.exists():
        fail("data/domain.yaml not found")
    if not theme_path.exists():
        fail("data/theme.yaml not found")

    validate_domain_file(domain_path)
    validate_theme_file(theme_path)

    for example in sorted(Path("data/examples").glob("domain*.yaml")):
        validate_domain_file(example)
    for example in sorted(Path("data/examples").glob("theme*.yaml")):
        validate_theme_file(example)

    print("Config validation passed")


if __name__ == "__main__":
    main()
