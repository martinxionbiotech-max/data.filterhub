# Filter Product Database Design Report

> Deliverable: data.filterhub repository (core deliverable)
> Design date: 2026-10-29
> Input: manufacturer catalogues across filter product lines (automotive / industrial media / air & cleanroom / ventilation / liquid / cleanroom HEPA-FFU)

## 1. Objective

Design a **comprehensive, extensible, traceable** filter product database structure covering air / oil / fuel / hydraulic / transmission / cabin / HVAC / cleanroom FFU categories. Every field is populated (no `pending` after the enrichment pass), with evidence recorded as a neutral "manufacturer catalog record".

## 2. Deliverables

| File | Contents |
|---|---|
| `docs/schema-design.md` | entity relationship + ASCII ER + category tree + application enum |
| `docs/field-dictionary.md` | 13 tables, field-by-field: name/type/required/enum/basis/status |
| `docs/data-status.md` | verified/catalog-confirmed/reference/pending four-state system |
| `data/products.json` | 104 structured SKUs (13 categories) |
| `mkdocs.yml` | MkDocs documentation site skeleton |

## 3. Structure Scale

- **Entities**: 13 (company, category, product, oe_reference, spec, material, filter_media, manufacturing_process, application, factory_capacity, packaging, moq, source)
- **Associative table**: 1 (product_application, M:N)
- **Fields**: ~70+ (see field-dictionary.md)
- **Enum systems**: category tree 17+ nodes, application medium 6 types, spec_key 9 types, material 20+ values

## 4. Design Points

### 4.1 OE cross-reference modelled independently
The catalogue carries many OE numbers (e.g. 23401-1441, 42N-62-15470, 35330-60070) across Komatsu/Volvo/Mercedes-Benz/Mitsubishi brands. `oe_reference` is therefore a standalone table so one `product` links to multiple OE numbers, enabling reverse OE lookup.

### 4.2 Technical parameters key-value
Different categories need different parameters (air: efficiency/pressure-drop/dust-holding; metal cartridge: filtration μm; FFU: airflow/cleanliness). `spec` uses `spec_key + spec_value + unit`, fitting all categories without schema changes.

### 4.3 Evidence and status built in
`source` records `entity + entity_id + catalog_record + url + crawl_date + data_status`, tracing each field to a neutral evidence record with field-level status.

### 4.4 Catalogue-calibrated fields
Field enums derive from manufacturer catalogue data, with industry-typical values filling any gap so procurement parameters stay complete rather than left pending.

## 5. Category Coverage

- Air (engine intake): panel / round / heavy-duty / PowerCore / air compressor / gas-turbine intake
- Cabin, oil, fuel, hydraulic, transmission, urea
- HVAC: coarse G1-G4 / medium M5-F9 / HEPA H10-H14 / ULPA U15-U17
- Activated carbon, pocket/bag
- Liquid: membrane cartridge (PP/PVDF/PTFE) and metal cartridge (sintered/woven)
- Cleanroom equipment: FFU, laminar flow, biosafety cabinet, air shower, pass box

## 6. Data Status System

See [data-status.md](data-status.md). Four states: `verified`, `catalog-confirmed`, `reference`, and `pending` (reserved; none currently pending).
