# Field Dictionary

Per-field definitions: name / type / required / enum / basis / data status. Enum values are drawn from manufacturer-catalogue fields and industry-typical values.

## 1. company

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string(uuid) | yes | — | system-generated | verified |
| name | string | yes | — | company page | verified |
| brand | string | yes | — | company brand name | verified |
| location | string | yes | — | company address | verified |
| established_year | integer | no | — | company history | verified/reference |
| website | string(url) | yes | — | company URL | verified |
| factory_area_sqm | integer | no | — | factory profile | verified/reference |
| staff_count | integer | no | — | company profile | verified/reference |
| monthly_output | integer | no | — | company capacity | verified/reference |
| certifications | string[] | no | ISO 9001, ISO 16890, EN 779, EN 1822, ASHRAE 52.2, UL 900, DIN 5510 | certifications page | catalog-confirmed |
| source_url | string(url) | yes | — | company URL | verified |

## 2. category

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| code | string | yes | air_filter/cabin_filter/oil_filter/fuel_filter/hydraulic_filter/transmission_filter/urea_filter/hvac_filter/hepa_filter/ulpa_filter/activated_carbon_filter/pocket_filter/liquid_filter/metal_cartridge/cleanroom_equipment/ffu/... | category tree | verified |
| name | string | yes | — | product navigation | catalog-confirmed |
| parent_id | string | no | category-tree parent | hierarchy | verified |

## 3. product

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| name | string | yes | — | product page title | catalog-confirmed |
| sku | string | yes | model / OE number | product page | catalog-confirmed |
| category_id | string | yes | FK → category | product grouping | verified |
| company_id | string | yes | FK → company | manufacturer | verified |
| description | string | no | — | product page body | verified/reference |
| source_url | string(url) | yes | — | product page URL | verified |

## 4. oe_reference (OE cross-reference)

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| product_id | string | yes | FK → product | relation | verified |
| oe_number | string | yes | e.g. 23401-1441, 42N-62-15470, 35330-60070 | product title | catalog-confirmed |
| brand | string | no | Komatsu/Volvo/Mercedes-Benz/Mitsubishi/... | product title | catalog-confirmed |
| equipment_type | string | no | truck/loader/tractor/combine/passenger/ATV | product description | reference |
| data_status | enum | yes | verified/catalog-confirmed/reference/pending | status system | catalog-confirmed |

## 5. spec (technical parameter key-value)

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| product_id | string | yes | FK → product | relation | verified |
| spec_key | string | yes | dimension/efficiency_class/pressure_drop/dust_holding/temperature_resistance/airflow/cleanliness_class/removal_rating | spec table | verified/reference |
| spec_value | string | yes | e.g. "610×610×70mm", "H14", "1μm", "80°C" | spec table | verified/reference |
| unit | string | no | mm/inch/Pa/°C/μm/CMH/CFM/m/s/%/USD | spec table | verified/reference |
| data_status | enum | yes | status system | — | verified/reference |

### spec_key enum and basis

| spec_key | Description | Basis | Status |
|---|---|---|---|
| dimension | Outer dimensions | HEPA size table, FFU size | verified |
| efficiency_class | Efficiency class | G1-G4/M5-M9/H10-H14/U15-U17/F8/F9 | verified |
| pressure_drop | Pressure drop | catalogue / industry-typical | reference |
| dust_holding | Dust-holding capacity | catalogue / industry-typical | reference |
| temperature_resistance | Temperature resistance | 260/350°C, 80°C, 300°C etc. | catalog-confirmed |
| airflow | Airflow | FFU 4000-5000 CMH | verified |
| cleanliness_class | Cleanliness class | FFU Class 100 | verified |
| removal_rating | Filtration rating | metal cartridge 1/3/5/10/20/30/50/100 μm | verified |
| efficiency_percentage | Efficiency % | 95% DOP | catalog-confirmed |

## 6. material

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| product_id | string | yes | FK → product | relation | verified |
| part | string | yes | frame/end_cap/seal/o_ring/support_layer/housing/core/media/thread | catalogue table | catalog-confirmed |
| material_value | string | yes | see enum below | catalogue table | catalog-confirmed |
| data_status | enum | yes | status system | — | catalog-confirmed |

### material_value enum

- frame/housing: galvanized steel, stainless steel (SS304/SS316L), aluminium, cardboard/paper, titanium (Ti)
- end_cap: PU (polyurethane), 215/222/226, DOE, Flat 222, High 222/226, threaded
- seal/o_ring: Silicone, EPDM, Viton, FEP, NBR, PEFE, endless gasket, gel
- support_layer/core: PP, PET, PTFE, PP mesh
- membrane: PP, PVDF, PTFE, NL, GF, PET

## 7. filter_media

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| product_id | string | yes | FK → product | relation | verified |
| type | string | yes | needle_punched/synthetic_fiber/micro_glass_fiber/activated_carbon/paper/membrane/sintered_mesh/tio2 | description | catalog-confirmed |
| efficiency_class | string | no | G1-G4/M5-M9/H10-H14/U15-U17 | grade table | verified/reference |
| grammage | string | no | g/m² | industry-typical | reference |
| data_status | enum | yes | status system | — | catalog-confirmed |

## 8. manufacturing_process

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| product_id | string | yes | FK → product | relation | verified |
| process_name | string | yes | pu_potting/pleating/separator_pleating/mini_pleat/sintering/welding/lamination/needle_punching | equipment/process | catalog-confirmed |
| equipment | string | no | pleating/forming/laminating/needle-punch machines | equipment page | verified/reference |
| params | json | no | pleat depth/speed/paper width etc. | equipment parameters | verified/reference |
| data_status | enum | yes | status system | — | catalog-confirmed |

## 9. application

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| code | string | yes | automotive/heavy_machinery/agricultural/air_compressor/lawn_garden/swimming_pool/paint_booth/hvac/food_beverage/healthcare/pharma/public_transport/commercial_building/industrial/oil_gas/chemical/power/electronics/livestock/water/cleanroom/mushroom/3d_printer/air_purifier/fresh_air | application page | catalog-confirmed |
| name | string | yes | — | application page | catalog-confirmed |
| medium | enum | yes | air/oil/fuel/hydraulic/cabin/cleanroom_ffu | filtration medium | verified |

## 10. factory_capacity

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| company_id | string | yes | FK → company | relation | verified |
| area_sqm | integer | no | 24000/10000/22496 | factory profile | verified/reference |
| staff_count | integer | no | 180/90 | company profile | verified/reference |
| monthly_output | integer | no | 200000 | company capacity | verified |
| production_lines | string[] | no | PU line/air-filter line/HEPA line/paper line/FFU line | equipment | catalog-confirmed |
| data_status | enum | yes | status system | — | verified/reference |

## 11. packaging

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| product_id | string | yes | FK → product | relation | verified |
| unit | string | no | pcs/roll/set | MOQ description | reference |
| carton_qty | integer | no | — | industry-typical | reference |
| dimensions | string | no | — | industry-typical | reference |
| weight | string | no | — | industry-typical | reference |

## 12. moq

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| product_id | string | yes | FK → product | relation | verified |
| moq_value | integer | no | 20 (roll) / 200 (set) / 500 (pcs) | catalogue | verified/reference |
| moq_unit | string | no | roll/set/pcs | catalogue | verified/reference |
| data_status | enum | yes | status system | — | verified/reference |

## 13. source (evidence source and data status)

| Field | Type | Required | Enum / format | Basis | Data status |
|---|---|---|---|---|---|
| id | string | yes | — | system | verified |
| entity | string | yes | company/product/oe_reference/spec/... | traceability object | verified |
| entity_id | string | yes | — | related entity id | verified |
| catalog_record | string | yes | neutral "manufacturer catalog record" | evidence source | verified |
| url | string(url) | yes | — | page URL (archived) | verified |
| crawl_date | date | yes | 2026-10-29 | crawl date | verified |
| data_status | enum | yes | verified/catalog-confirmed/reference/pending | status system | verified |
