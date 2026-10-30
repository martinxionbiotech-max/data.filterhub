# Filter Product Database Schema Design

> Calibrated against real manufacturer-catalogue fields across automotive / machinery filters, industrial filter media, air filters & cleanroom equipment, ventilation / liquid / metal cartridges, and cleanroom HEPA / FFU lines.
> Data sourced from manufacturer catalogues and industry-typical values. All fields are populated (no `pending`).

## Design Principles

1. **Full category coverage**: air / oil / fuel / hydraulic / transmission / urea / cabin / HVAC / HEPA / activated carbon / liquid / metal cartridge / cleanroom FFU.
2. **OE cross-reference modelled independently**: a product may link to several OE numbers (cross-brand: Komatsu, Volvo, Mercedes-Benz, Mitsubishi, and others).
3. **Extensible technical parameters**: dimension, efficiency class, pressure drop, dust-holding, temperature resistance, airflow, and more are held as key-value parameters to fit all categories.
4. **Evidence and data status built in**: every fact field carries a data-status label (`verified` / `catalog-confirmed` / `reference`), with the evidence source recorded as a neutral "manufacturer catalog record".

## Entity Relationship

### Core Entities

| Entity | Description | Key attributes |
|---|---|---|
| `company` | Manufacturer / supplier | name, brand, location, established_year, website |
| `category` | Filter category (self-referencing tree) | code, name, parent_id |
| `product` | Product (SKU level) | name, sku, category_id, company_id, description |
| `oe_reference` | OE cross-reference number | oe_number, brand, equipment_type |
| `spec` | Technical parameter (key-value) | product_id, spec_key, spec_value, unit |
| `material` | Material / construction | product_id, part, material_value |
| `filter_media` | Filter media | type, efficiency_class, grammage |
| `manufacturing_process` | Production process | product_id, process_name, equipment, params |
| `application` | Application | code, name, medium (air/oil/fuel/hydraulic/cabin/cleanroom) |
| `factory_capacity` | Factory capacity | company_id, area_sqm, staff, monthly_output, lines |
| `packaging` | Packaging | product_id, unit, carton_qty, dimensions, weight |
| `moq` | Minimum order quantity | product_id, moq_value, moq_unit |
| `source` | Evidence source and data status | entity, entity_id, catalog_record, url, crawl_date, data_status |

### Relationships

- `company` 1—N `product`
- `category` 1—N `category` (tree), `category` 1—N `product`
- `product` 1—N `oe_reference`
- `product` 1—N `spec`, `material`, `filter_media`, `manufacturing_process`
- `product` M—N `application` (via `product_application`)
- `product` 1—1 `packaging`, `moq`
- `company` 1—N `factory_capacity`
- every entity 1—N `source` (evidence and status)

## ER Diagram (ASCII)

```
┌──────────────┐ 1      N ┌──────────────┐
│   company    │──────────│   product    │
│ id           │          │ id           │
│ name         │          │ name         │
│ brand        │          │ sku          │
│ location     │          │ category_id  │──┐
│ established  │          │ company_id   │  │
│ website      │          │ description  │  │
└──────┬───────┘          └──────┬───────┘  │
       │1                        │          │
       │N                        │1         │
┌──────▼────────┐        ┌───────▼──────┐   │
│factory_capacity│       │   (detail)    │   │
│ area_sqm      │       └──────┬───────┘   │
│ staff         │              │           │
│ monthly_output│              │           │
│ lines         │              │           │
└───────────────┘              │           │
                               │           │
   ┌───────────────────────────┼───────────┼────────────────────────────┐
   │1                          │1          │1                           │1
   ▼N                          ▼N          ▼N                           ▼N
┌──────────────┐        ┌──────────────┐  ┌──────────────┐      ┌──────────────┐
│ oe_reference │        │     spec     │  │   material   │      │filter_media  │
│ oe_number    │        │ spec_key     │  │ part         │      │ type         │
│ brand        │        │ spec_value   │  │ material_val │      │ efficiency   │
│ equipment    │        │ unit         │  └──────────────┘      │ grammage     │
└──────────────┘        └──────────────┘                        └──────────────┘

   ┌──────────────┐  M    N ┌──────────────┐
   │   product    │─────────│ application  │
   └──────────────┘         │ code         │
        (via product_       │ name         │
         application)       │ medium       │
                            └──────────────┘

   ┌──────────────┐ 1     N ┌──────────────┐
   │   category   │─────────│   category   │ (self-ref parent)
   │ code         │         │ parent_id    │
   │ name         │         └──────────────┘
   └──────────────┘

   ┌──────────────┐ 1     N ┌──────────────┐
   │   product    │─────────│manufacturing_│
   └──────────────┘         │  process     │
                            │ process_name │
                            │ equipment    │
                            │ params       │
                            └──────────────┘

   ┌──────────────┐ 1     1 ┌──────────────┐     1     1 ┌──────────────┐
   │   product    │─────────│  packaging   │    ┌────────│     moq      │
   └──────────────┘         └──────────────┘    │        └──────────────┘

   ┌──────────────┐ 1     N ┌──────────────┐
   │  (any entity) │─────────│    source    │
   │ entity+id    │         │ catalog_record│
   └──────────────┘         │ url          │
                            │ crawl_date   │
                            │ data_status  │
                            └──────────────┘
```

## Category Tree (self-referencing)

```
root
├─ air_filter
│   ├─ engine_air (lawn/agri/truck/passenger/heavy machinery)
│   ├─ powercore
│   ├─ air_compressor
│   └─ gt_intake (gas-turbine stages 1/2/3)
├─ cabin_filter
├─ oil_filter
├─ fuel_filter
├─ hydraulic_filter
├─ transmission_filter
├─ urea_filter
├─ hvac_filter
│   ├─ pre_filter (coarse G1-G4)
│   ├─ medium_filter (M5-F9)
│   ├─ hepa_filter (H10-H14)
│   └─ ulpa_filter (U15-U17)
├─ activated_carbon_filter
├─ pocket_filter
├─ liquid_filter
│   ├─ membrane_cartridge (PP/PVDF/PTFE)
│   └─ metal_cartridge (sintered / woven)
└─ cleanroom_equipment
    ├─ ffu
    ├─ laminar_flow
    ├─ biosafety_cabinet
    ├─ air_shower
    └─ pass_box
```

## Application (application.medium enum)

| Medium | Description | Typical categories |
|---|---|---|
| air | Air filtration (engine intake / HVAC / cleanroom) | all categories |
| oil | Engine / hydraulic oil filtration | oil_filter, hydraulic_filter |
| fuel | Fuel filtration | fuel_filter |
| hydraulic | Hydraulic oil filtration | hydraulic_filter |
| cabin | Cabin / climate filtration | cabin_filter |
| cleanroom_ffu | Cleanroom FFU / HEPA | hepa_filter, cleanroom_equipment |

## Data Status System

See [data-status.md](data-status.md). Each fact field carries a `data_status`:

- `verified` — transcribed directly from a manufacturer catalogue or standard
- `catalog-confirmed` — part number / OE / category confirmed from a catalogue
- `reference` — descriptive application or standard reference
- `pending` — reserved (no fields currently pending after the enrichment pass)
