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
transcribed from the JSON; empty/unpublished fields render as `pending`, never guessed.
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

CATEGORY_NAMES_ZH = {
    "air_filter": "空气滤清器",
    "cabin_filter": "空调滤清器",
    "oil_filter": "机油滤清器",
    "fuel_filter": "燃油滤清器",
    "hydraulic_filter": "液压滤清器",
    "transmission_filter": "变速箱滤清器",
    "hvac_filter": "HVAC 过滤器",
    "hepa_filter": "HEPA/ULPA 过滤器",
    "activated_carbon_filter": "活性炭过滤器",
    "pocket_filter": "袋式过滤器",
    "filter_media": "滤材介质",
    "liquid_filter": "液体过滤滤芯",
    "cleanroom_equipment": "洁净室设备",
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
        "# SKU 索引 (Product Index)\n",
        AUTO_NOTE,
        f"共 {len(products)} 个结构化 SKU，数据来源：5 站深度抓取（2026-10-29）。"
        "无据字段标记 `pending`，不虚构。\n",
        "| SKU | 品类 | 效率等级 | 来源站 | 数据状态 |",
        "|---|---|---|---|---|",
    ]
    for p in products:
        eff = cell(p.get("efficiency_class"))
        idx_lines.append(
            f"| [`{p['sku']}`]({slugify(p['sku'])}.md) | "
            f"[{CATEGORY_NAMES.get(p['category'], p['category'])}]({slugify(p['category'])}.md) | "
            f"{eff} | {p['company']} | {p.get('data_status', 'catalog-confirmed')} |"
        )
    with open(os.path.join(OUT, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx_lines) + "\n")

    # --- Category pages ---
    for cat, items in sorted(groups.items()):
        cat_name = CATEGORY_NAMES.get(cat, cat)
        lines = [
            f"# {cat_name}\n",
            AUTO_NOTE,
            f"品类 code：`{cat}` · SKU 数：{len(items)} · 状态：`catalog-confirmed`\n",
            "| SKU | 描述 | 效率等级 | 数据状态 |",
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
            f"- **SKU**：`{sku}`",
            f"- **品类**：[{CATEGORY_NAMES.get(p['category'], p['category'])}]({slugify(p['category'])}.md)",
            f"- **来源站**：{p['company']}",
            f"- **来源 URL**：{p.get('source_url', '`pending`')}",
            f"- **数据状态**：{p.get('data_status', 'catalog-confirmed')}\n",
        ]
        if p.get("subcategory"):
            lines.append(f"- **子类**：`{p['subcategory']}`")
        if p.get("efficiency_class"):
            lines.append(f"- **效率等级**：`{p['efficiency_class']}`")

        lines.append("\n## 描述\n")
        lines.append(p.get("description") or "`pending`")

        lines.append("\n## OE 交叉参考\n")
        oes = p.get("oe_reference") or []
        if oes:
            lines.append("| OE 号 | 品牌 | 设备类型 | 状态 |")
            lines.append("|---|---|---|---|")
            for o in oes:
                lines.append(
                    f"| `{o.get('oe_number', 'pending')}` | {cell(o.get('brand'))} | "
                    f"{cell(o.get('equipment_type'))} | {o.get('data_status', 'reference')} |"
                )
        else:
            lines.append("`pending`")

        lines.append("\n## 技术参数 (spec)\n")
        if p.get("spec"):
            lines.append("| 参数 | 值 | 单位 | 状态 |")
            lines.append("|---|---|---|---|")
            for s in p["spec"]:
                lines.append(
                    f"| `{s.get('spec_key', '?')}` | `{s.get('spec_value', '?')}` | "
                    f"{cell(s.get('unit'))} | {s.get('data_status', 'pending')} |"
                )
        else:
            lines.append("`pending`")

        lines.append("\n## 材质 (material)\n")
        if p.get("material"):
            lines.append("| 部件 | 材质 | 状态 |")
            lines.append("|---|---|---|")
            for m in p["material"]:
                lines.append(
                    f"| `{m.get('part', '?')}` | `{m.get('material_value', '?')}` | "
                    f"{m.get('data_status', 'pending')} |"
                )
        else:
            lines.append("`pending`")

        lines.append("\n## 滤材 (filter media)\n")
        fm = p.get("filter_media") or []
        if fm:
            m0 = fm[0]
            lines.append(
                f"- 类型：`{m0.get('type', 'pending')}`\n"
                f"- 效率等级：{cell(m0.get('efficiency_class'))}\n"
                f"- 克重：{cell(m0.get('grammage'))}"
            )
        else:
            lines.append("`pending`")

        lines.append("\n## 应用场景 (application)\n")
        apps = p.get("application") or []
        if apps:
            lines.append("| 场景 | 介质 | 状态 |")
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
            lines.append(f"`{moq['moq_value']} {moq.get('moq_unit', '')}` ({moq.get('data_status', 'verified')})".strip())
        else:
            lines.append("`pending`")

        with open(os.path.join(OUT, f"{slugify(sku)}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    # --- Dataset landing page (docs/data/products.md) ---
    by_company = {}
    for p in products:
        by_company.setdefault(p["company"], []).append(p)
    landing = [
        "# 产品数据\n",
        AUTO_NOTE,
        "机器可读数据见 [products.json](products.json)。\n",
        f"共 {len(products)} 个结构化 SKU，覆盖 {len(groups)} 个主品类，来源 5 站：\n",
        "| 来源站 | SKU 数 |",
        "|---|---|",
    ]
    for comp, items in sorted(by_company.items(), key=lambda x: -len(x[1])):
        landing.append(f"| {comp} | {len(items)} |")
    landing.append("")
    landing.append("所有字段来源真实，缺失字段标记 `pending`（不虚构）。")
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
    """Regenerate mkdocs.yml nav from the dataset."""
    category_pages = sorted(groups.keys())
    sku_pages = [slugify(p["sku"]) for p in products]

    nav = [
        "nav:",
        "  - 首页: index.md",
        "  - 产品数据库:",
        "      - SKU 索引: products/index.md",
    ]
    for cat in category_pages:
        zh = CATEGORY_NAMES_ZH.get(cat, CATEGORY_NAMES.get(cat, cat))
        nav.append(f"      - {zh}: products/{slugify(cat)}.md")
    nav.append("      - SKU 单页:")
    for sp in sku_pages:
        nav.append(f"          - {sp}: products/{sp}.md")
    nav += [
        "  - 参考资料:",
        "      - 滤材对比: reference/filter-media.md",
        "      - 测试标准: reference/test-standards.md",
        "  - 数据库设计:",
        "      - 实体关系与 ER 图: schema-design.md",
        "      - 字段字典: field-dictionary.md",
        "      - 数据状态体系: data-status.md",
        "      - 设计报告: design-report.md",
        "  - 数据:",
        "      - 产品数据: data/products.md",
    ]

    mk = [
        "site_name: China Filter Hub Data",
        "site_description: Qinghe Air Filter 产品数据库 —— SKU/OE/参数/滤材对比/测试标准（基于 5 站深度抓取）",
        "site_url: https://data.chinafilterhub.com/",
        "repo_url: https://github.com/martinxionbiotech-max/data.filterhub",
        "theme:",
        "  name: material",
        "  language: zh",
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
        "# 说明：data/products.json 为机器可读数据（源），",
        "# docs/data/products.json 为站点服务副本（由生成脚本同步），",
        "# docs/products/ 下的产品页与 mkdocs.yml 由 scripts/build-product-pages.py 生成。",
        "# 域名 data.chinafilterhub.com 为占位（provisional）。",
    ]
    with open(MKFILE, "w", encoding="utf-8") as f:
        f.write("\n".join(mk) + "\n")


if __name__ == "__main__":
    main()
