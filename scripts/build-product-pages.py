#!/usr/bin/env python3
"""Generate FilterHub data-subsite product pages from the canonical products.json.

Phase 3: reads data/products.json (byte-identical to filterhub/src/data/products.json)
and emits:
- products/index.md          SKU full index
- products/{category}.md     category pages (SKU spec table)
- products/{sku}.md          SKU detail pages
- data/products.md           dataset landing page
- mkdocs.yml                 nav regenerated from the dataset

Idempotent: cleans docs/products/*.md before regenerating. All values are
transcribed from the JSON; the evidence source is rendered as a neutral
"manufacturer catalog record" (source-site identity is kept in the archive only).
"""
import json
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "products.json")
OUT = os.path.join(ROOT, "docs", "products")
SERVED_JSON = os.path.join(ROOT, "docs", "data", "products.json")
DATA_LANDING = os.path.join(ROOT, "docs", "data", "products.md")
MKFILE = os.path.join(ROOT, "mkdocs.yml")

EVIDENCE_SOURCE = "manufacturer catalog record"

CATEGORY_NAMES = {
    "air_filter": "Air Filters (Engine Intake)",
    "cabin_filter": "Cabin Air Filters",
    "oil_filter": "Oil Filters",
    "fuel_filter": "Fuel Filters",
    "hydraulic_filter": "Hydraulic Filters",
    "transmission_filter": "Transmission Filters",
    "hvac_filter": "HVAC Filters",
    "hepa_filter": "HEPA / ULPA Filters",
    "activated_carbon_filter": "Activated Carbon Filters",
    "pocket_filter": "Pocket / Bag Filters",
    "filter_media": "Filter Media",
    "liquid_filter": "Liquid Filter Cartridges",
    "cleanroom_equipment": "Cleanroom Equipment",
}

AUTO_NOTE = "<!-- AUTO-GENERATED: edit the dataset (data/products.json), then rerun scripts/build-product-pages.py. Do not hand-edit values. -->\n"


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def cell(v):
    """Render a list/value as a single-line comma-separated cell (tables don't allow newlines)."""
    if v is None or v == "" or v == []:
        return "`pending`"
    if isinstance(v, list):
        return ", ".join(f"`{x}`" for x in v)
    return f"`{v}`"


def main():
    with open(DATA, encoding="utf-8") as f:
        payload = json.load(f)
    products = payload["products"]

    # Clean previously generated pages.
    if os.path.isdir(OUT):
        for p in glob.glob(os.path.join(OUT, "*.md")):
            os.remove(p)
    os.makedirs(OUT, exist_ok=True)

    # Group by category.
    groups = {}
    for p in products:
        groups.setdefault(p["category"], []).append(p)

    # --- SKU full index ---
    idx_lines = [
        "# SKU Index (Product Index)\n",
        AUTO_NOTE,
        f"{len(products)} structured SKUs across {len(groups)} main categories.\n",
        "| SKU | Category | Efficiency | Data status |",
        "|---|---|---|---|",
    ]
    for p in products:
        eff = cell(p.get("efficiency_class"))
        idx_lines.append(
            f"| [`{p['sku']}`]({slugify(p['sku'])}.md) | "
            f"[{CATEGORY_NAMES.get(p['category'], p['category'])}]({slugify(p['category'])}.md) | "
            f"{eff} | {p.get('data_status', 'catalog-confirmed')} |"
        )
    with open(os.path.join(OUT, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx_lines) + "\n")

    # --- Category pages ---
    for cat, items in sorted(groups.items()):
        cat_name = CATEGORY_NAMES.get(cat, cat)
        lines = [
            f"# {cat_name}\n",
            AUTO_NOTE,
            f"Category code: `{cat}` · SKUs: {len(items)} · Status: `catalog-confirmed`\n",
            "| SKU | Description | Efficiency | Data status |",
            "|---|---|---|---|",
        ]
        for p in items:
            eff = cell(p.get("efficiency_class"))
            desc = (p.get("description") or "").replace("|", "\\|")
            lines.append(
                f"| [`{p['sku']}`]({slugify(p['sku'])}.md) | {desc} | {eff} | "
                f"{p.get('data_status', 'catalog-confirmed')} |"
            )
        with open(os.path.join(OUT, f"{slugify(cat)}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    # --- SKU detail pages ---
    for p in products:
        sku = p["sku"]
        lines = [
            f"# {p['name']}\n",
            AUTO_NOTE,
            f"- **SKU**: `{sku}`",
            f"- **Category**: [{CATEGORY_NAMES.get(p['category'], p['category'])}]({slugify(p['category'])}.md)",
            f"- **Evidence source**: {EVIDENCE_SOURCE}",
            f"- **Data status**: {p.get('data_status', 'catalog-confirmed')}\n",
        ]
        if p.get("subcategory"):
            lines.append(f"- **Subcategory**: `{p['subcategory']}`")
        if p.get("efficiency_class"):
            lines.append(f"- **Efficiency class**: `{p['efficiency_class']}`")

        lines.append("\n## Description\n")
        lines.append(p.get("description") or "`pending`")

        lines.append("\n## OE cross-reference\n")
        oes = p.get("oe_reference") or []
        if oes:
            lines.append("| OE number | Brand | Equipment type | Status |")
            lines.append("|---|---|---|---|")
            for o in oes:
                lines.append(
                    f"| `{o.get('oe_number', 'pending')}` | {cell(o.get('brand'))} | "
                    f"{cell(o.get('equipment_type'))} | {o.get('data_status', 'reference')} |"
                )
        else:
            lines.append("`pending`")

        lines.append("\n## Technical parameters (spec)\n")
        if p.get("spec"):
            lines.append("| Parameter | Value | Unit | Status |")
            lines.append("|---|---|---|---|")
            for s in p["spec"]:
                lines.append(
                    f"| `{s.get('spec_key', '?')}` | `{s.get('spec_value', '?')}` | "
                    f"{cell(s.get('unit'))} | {s.get('data_status', 'pending')} |"
                )
        else:
            lines.append("`pending`")

        lines.append("\n## Material\n")
        if p.get("material"):
            lines.append("| Part | Material | Status |")
            lines.append("|---|---|---|")
            for m in p["material"]:
                lines.append(
                    f"| `{m.get('part', '?')}` | `{m.get('material_value', '?')}` | "
                    f"{m.get('data_status', 'pending')} |"
                )
        else:
            lines.append("`pending`")

        lines.append("\n## Filter media\n")
        fm = p.get("filter_media") or []
        if fm:
            m0 = fm[0]
            lines.append(
                f"- Type: `{m0.get('type', 'pending')}`\n"
                f"- Efficiency class: {cell(m0.get('efficiency_class'))}\n"
                f"- Grammage: {cell(m0.get('grammage'))}"
            )
        else:
            lines.append("`pending`")

        lines.append("\n## Application\n")
        apps = p.get("application") or []
        if apps:
            lines.append("| Application | Medium | Status |")
            lines.append("|---|---|---|")
            for a in apps:
                lines.append(
                    f"| `{a.get('code', '?')}` | `{a.get('medium', '?')}` | "
                    f"{a.get('data_status', 'reference')} |"
                )
        else:
            lines.append("`pending`")

        moq = p.get("moq") or {}
        lines.append("\n## MOQ\n")
        if moq.get("moq_value") is not None:
            lines.append(f"`{moq['moq_value']} {moq.get('moq_unit', '')}` ({moq.get('data_status', 'reference')})".strip())
        else:
            lines.append("`pending`")

        with open(os.path.join(OUT, f"{slugify(sku)}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    # --- Dataset landing page (docs/data/products.md) ---
    landing = [
        "# Product Data\n",
        AUTO_NOTE,
        "Machine-readable data: [products.json](products.json).\n",
        f"{len(products)} structured SKUs across {len(groups)} main categories.\n",
    ]
    with open(DATA_LANDING, "w", encoding="utf-8") as f:
        f.write("\n".join(landing) + "\n")

    # --- Sync the machine-readable JSON to the served location (kept byte-identical). ---
    os.makedirs(os.path.dirname(SERVED_JSON), exist_ok=True)
    with open(SERVED_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    write_mkdocs(payload, products, groups)

    print(f"generated: index + {len(groups)} category pages + {len(products)} SKU pages + data landing + served JSON + mkdocs.yml")


def write_mkdocs(payload, products, groups):
    """Regenerate mkdocs.yml nav from the dataset (English)."""
    category_pages = sorted(groups.keys())
    sku_pages = [slugify(p["sku"]) for p in products]

    nav = [
        "nav:",
        "  - Home: index.md",
        "  - Product Database:",
        "      - SKU Index: products/index.md",
    ]
    for cat in category_pages:
        name = CATEGORY_NAMES.get(cat, cat)
        nav.append(f"      - {name}: products/{slugify(cat)}.md")
    nav.append("      - SKU Pages:")
    for sp in sku_pages:
        nav.append(f"          - {sp}: products/{sp}.md")
    nav += [
        "  - Reference:",
        "      - Filter Media: reference/filter-media.md",
        "      - Test Standards: reference/test-standards.md",
        "  - Database Design:",
        "      - Schema & ER: schema-design.md",
        "      - Field Dictionary: field-dictionary.md",
        "      - Data Status: data-status.md",
        "      - Design Report: design-report.md",
        "  - Data:",
        "      - Product Data: data/products.md",
    ]

    mk = [
        "site_name: China Filter Hub Data",
        "site_description: Qinghe Air Filter product database — SKU / OE / parameters / filter-media comparison / test standards",
        "site_url: https://data.chinafilterhub.com/",
        "repo_url: https://github.com/martinxionbiotech-max/data.filterhub",
        "theme:",
        "  name: material",
        "  language: en",
        "  features:",
        "    - navigation.sections",
        "    - navigation.indexes",
        "    - content.code.copy",
        *nav,
        "markdown_extensions:",
        "  - tables",
        "  - admonition",
        "  - codehilite",
        "  - toc:",
        "      permalink: true",
        "",
        "# data/products.json is the machine-readable source;",
        "# docs/data/products.json is the served copy (synced by the build script);",
        "# docs/products/ pages and mkdocs.yml are generated by scripts/build-product-pages.py.",
        "# Domain data.chinafilterhub.com is a placeholder (provisional).",
        "hooks:",
        "  - hooks/build_hook.py",
    ]
    with open(MKFILE, "w", encoding="utf-8") as f:
        f.write("\n".join(mk) + "\n")


if __name__ == "__main__":
    main()
