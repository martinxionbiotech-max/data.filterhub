# Data Status System

Data status labels the confidence and basis of every fact field. Each field carries a `data_status`, separating catalogue-confirmed facts from descriptive references.

## Status Definitions

| Status | Definition | Criterion | Example |
|---|---|---|---|
| `verified` | transcribed directly from a manufacturer catalogue or standard | value appears verbatim in the source table | HEPA price table, production-equipment parameters |
| `catalog-confirmed` | model / OE number / category confirmed from catalogue and titles | appears in a product title, URL, navigation or filename | OE numbers, product categories |
| `reference` | descriptive copy (application, standard, industry-typical value) | appears in profile / application copy, or a typical industry value | ISO 16890 / EN 779 / ASHRAE 52.2 descriptions, typical dimensions and MOQ |
| `pending` | reserved | not currently used — all fields are populated after the enrichment pass | (none remaining) |

## Usage Conventions

1. **No fabrication**: descriptive `reference` fields state the basis; catalogue facts are `verified` or `catalog-confirmed`.
2. **Traceable**: every field can be traced to an evidence record (neutral "manufacturer catalog record" + archived URL + crawl date + data status).
3. **Status can upgrade**: when a field is later confirmed from a spec sheet or quotation, its status moves from `reference` to `verified` / `catalog-confirmed`.
4. **Field-level labelling**: a product may mix `verified`, `catalog-confirmed` and `reference` fields.

## Status-to-Field Mapping (example)

| Field | Common status | Note |
|---|---|---|
| product.name / sku | catalog-confirmed | name / OE number from title |
| spec.dimension | verified / reference | catalogue size table or typical form factor |
| spec.efficiency | verified / reference | catalogue grade or typical grade |
| spec.pressure_drop | reference | catalogue or industry-typical value |
| spec.dust_holding | reference | catalogue or industry-typical value |
| material.frame | catalog-confirmed | frame material from product name / description |
| filter_media.type | catalog-confirmed | glass fibre / synthetic / carbon etc. |
| moq | verified / reference | catalogue MOQ or industry-typical MOQ |
| factory_capacity | verified / reference | catalogue figure or industry-typical |
| price | verified / reference | catalogue price table where published |
