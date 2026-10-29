#!/usr/bin/env python3
"""Generate FilterHub data-subsite product pages from sample-products.json.

Phase 2 skeleton: reads the canonical seed data (14 sample products) and emits
- products/index.md          SKU full index
- products/{category}.md     category pages (SKU spec table)
- products/{sku}.md          SKU detail pages

Idempotent: cleans docs/products/*.md before regenerating. All values are
transcribed from the JSON; empty/unpublished fields render as `pending`, never guessed.
"""
import json
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "sample-products.json")
OUT = os.path.join(ROOT, "docs", "products")
SERVED_JSON = os.path.join(ROOT, "docs", "data", "sample-products.json")

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
    "metal_cartridge": "Metal Filter Cartridges",
    "cleanroom_equipment": "Cleanroom Equipment",
    "ffu": "Fan Filter Units (FFU)",
}

AUTO_NOTE = "<!-- AUTO-GENERATED: edit the dataset (data/sample-products.json), then rerun scripts/build-product-pages.py. Do not hand-edit values. -->\n"


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def cell(v):
    """Render a list/value as a single-line comma-separated cell (tables don't allow newlines)."""
    if v is None or v == "" or v == []:
        return "`pending`"
    if isinstance(v, list):
        return ", ".join(f"`{x}`" for x in v)
    return f"`{v}`"


def data_status_of(obj, default="catalog-confirmed"):
    return obj.get("data_status", default) if isinstance(obj, dict) else default


def spec_lines(specs):
    if not specs:
        return "`pending`"
    return "; ".join(
        f"{s.get('spec_key', '?')}={s.get('spec_value', '?')} {s.get('unit') or ''}".strip()
        + f" ({s.get('data_status', 'pending')})"
        for s in specs
    )


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
        f"共 {len(products)} 个样例产品（阶段 2 打样），数据来源：5 站深度抓取（2026-10-29）。"
        "缺失字段标记 `pending`，不虚构。\n",
        "| SKU | 品类 | 来源站 | 数据状态 |",
        "|---|---|---|---|",
    ]
    for p in products:
        idx_lines.append(
            f"| [`{p['sku']}`]({slugify(p['sku'])}.md) | "
            f"[{CATEGORY_NAMES.get(p['category'], p['category'])}]({slugify(p['category'])}.md) | "
            f"{p['company']} | {p.get('data_status', 'catalog-confirmed')} |"
        )
    with open(os.path.join(OUT, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx_lines) + "\n")

    # --- Category pages ---
    for cat, items in sorted(groups.items()):
        cat_name = CATEGORY_NAMES.get(cat, cat)
        lines = [
            f"# {cat_name}\n",
            AUTO_NOTE,
            f"品类 code：`{cat}` · SKU 数：{len(items)} · 状态：`catalog-confirmed`（样例）\n",
            "| SKU | 描述 | 效率等级 | 数据状态 |",
            "|---|---|---|---|",
        ]
        for p in items:
            eff = "`pending`"
            fm = [m for m in p.get("filter_media", [])]
            if fm and fm[0].get("efficiency_class"):
                eff = f"`{fm[0]['efficiency_class']}`"
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
            "## 描述\n",
            p.get("description") or "`pending`",
            "\n## OE 交叉参考\n",
        ]
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

    # Sync the machine-readable JSON to the served location (kept byte-identical).
    os.makedirs(os.path.dirname(SERVED_JSON), exist_ok=True)
    with open(SERVED_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"generated: index + {len(groups)} category pages + {len(products)} SKU pages + served JSON")


if __name__ == "__main__":
    main()
