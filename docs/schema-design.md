# Filter 产品数据库结构设计 (Schema Design)

> 基于 5 站真实字段校准：hbxueyuan（汽车/工程机械滤清器）、airyfilter（工业滤材+成品）、klcintl（空气过滤器+洁净室设备）、yitong-filter（通风/液体/金属滤芯）、cleanroom-ffu（洁净室 HEPA/FFU）。
> 数据来源：5 站官网深度抓取（2026-10-29）。字段全部由站点真实字段推导，缺失字段标 `pending`，不虚构。

## 设计原则

1. **覆盖全品类**：空气 / 机油 / 燃油 / 液压 / 变速箱 / 尿素 / 空调 / HVAC / HEPA / 活性炭 / 液体滤 / 金属滤芯 / 洁净室设备 FFU。
2. **OE 交叉参考独立建模**：一个产品可关联多个 OE 号（跨品牌：Komatsu、Volvo、Mercedes-Benz、Mitsubishi 等）。
3. **技术参数可扩展**：尺寸、效率等级、压降、容尘量、耐温、风量等作为 key-value 参数表，兼容不同品类。
4. **来源与数据状态内建**：每个事实字段可追溯到来源站 + 数据状态（verified/catalog-confirmed/reference/pending）。

## 实体关系说明

### 核心实体

| 实体 | 说明 | 关键属性 |
|---|---|---|
| `company` | 制造商/供应商 | name, brand, location, established_year, website |
| `category` | 滤清器品类（自引用树）| code, name, parent_id |
| `product` | 产品（SKU 级）| name, sku, category_id, company_id, description |
| `oe_reference` | OE 交叉参考号 | oe_number, brand, equipment_type |
| `spec` | 技术参数（key-value）| product_id, spec_key, spec_value, unit |
| `material` | 材质/原料 | product_id, part, material_type, material_value |
| `filter_media` | 滤材 | type, fiber, efficiency_class, grammage |
| `manufacturing_process` | 生产工艺 | product_id, process_name, equipment, params |
| `application` | 应用场景 | code, name, medium (air/oil/fuel/hydraulic/cabin/cleanroom) |
| `factory_capacity` | 工厂产能 | company_id, area_sqm, staff, monthly_output, lines |
| `packaging` | 包装 | product_id, unit, carton_qty, dimensions, weight |
| `moq` | 起订量 | product_id, moq_value, moq_unit |
| `source` | 来源与数据状态 | entity, entity_id, site, url, crawl_date, data_status |

### 关联关系

- `company` 1—N `product`（一家公司多产品）
- `category` 1—N `category`（品类树）、`category` 1—N `product`
- `product` 1—N `oe_reference`（一个产品多个 OE 号）
- `product` 1—N `spec`、`material`、`filter_media`、`manufacturing_process`
- `product` M—N `application`（经 `product_application` 关联表）
- `product` 1—1 `packaging`、`moq`
- `company` 1—N `factory_capacity`
- 所有实体 1—N `source`（溯源与状态）

## ER 图（ASCII）

```
┌──────────────┐ 1      N ┌──────────────┐
│   company    │──────────│   product    │
│ id           │          │ id           │
│ name         │          │ name         │
│ brand        │          │ sku          │
│ location     │          │ category_id  │──┐
│ established  │          │ company_id   │  │
│ website      │          │ description  │  │
│ source_url   │          └──────┬───────┘  │
└──────┬───────┘                 │          │
       │1                        │          │
       │N                        │1         │
┌──────▼────────┐        ┌───────▼──────┐   │
│factory_capacity│       │   (明细)      │   │
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
│ brand        │        │ spec_value   │  │ material_type│      │ fiber        │
│ equipment    │        │ unit         │  │ material_val │      │ efficiency   │
└──────────────┘        └──────────────┘  └──────────────┘      │ grammage     │
                                                                 └──────────────┘
   ┌──────────────┐  M    N ┌──────────────┐
   │   product    │─────────│ application  │
   └──────────────┘         │ code         │
        (经 product_        │ name         │
         application)       │ medium       │
                            └──────────────┘

   ┌──────────────┐ 1     N ┌──────────────┐
   │   category   │─────────│   category   │ (自引用父节点)
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
   │   (任意实体)  │─────────│    source    │
   │ entity+id    │         │ site         │
   └──────────────┘         │ url          │
                            │ crawl_date   │
                            │ data_status  │
                            └──────────────┘
```

## 品类树（category，自引用）

```
root
├─ air_filter（空气滤清器）
│   ├─ engine_air（发动机进气：割草机/农用/卡车/乘用车/重型机械）
│   ├─ powercore（PowerCore 滤）
│   ├─ air_compressor（空压机滤）
│   └─ gt_intake（燃气轮机进气 1/2/3 级）
├─ cabin_filter（空调/驾驶室滤清器）
├─ oil_filter（机油滤清器）
├─ fuel_filter（燃油滤清器）
├─ hydraulic_filter（液压滤清器）
├─ transmission_filter（变速箱滤清器）
├─ urea_filter（尿素滤清器）
├─ hvac_filter（HVAC 过滤器）
│   ├─ pre_filter（初效 G1-G4）
│   ├─ medium_filter（中效 M5-F9）
│   ├─ hepa_filter（高效 H10-H14）
│   └─ ulpa_filter（超低穿透 U15-U17）
├─ activated_carbon_filter（活性炭过滤器）
├─ pocket_filter（袋式/褶式过滤器）
├─ liquid_filter（液体过滤滤芯）
│   ├─ membrane_cartridge（PP/PVDF/PTFE 膜滤芯）
│   └─ metal_cartridge（金属烧结/编织滤芯）
└─ cleanroom_equipment（洁净室设备）
    ├─ ffu（风扇过滤单元）
    ├─ laminar_flow（层流罩）
    ├─ biosafety_cabinet（生物安全柜）
    ├─ air_shower（风淋）
    └─ pass_box（传递窗）
```

## 应用场景（application.medium 枚举）

| medium | 说明 | 代表站点 |
|---|---|---|
| air | 空气过滤（发动机进气/HVAC/洁净室）| 全 5 站 |
| oil | 机油/液压油过滤 | hbxueyuan |
| fuel | 燃油过滤 | hbxueyuan |
| hydraulic | 液压油过滤 | hbxueyuan |
| cabin | 驾驶室/空调过滤 | hbxueyuan |
| cleanroom_ffu | 洁净室 FFU/HEPA | klcintl, cleanroom-ffu |

## 数据状态体系

详见 [data-status.md](data-status.md)。每个事实字段通过 `source.data_status` 关联：

- `verified` — 站点文字层直接提取，可信
- `catalog-confirmed` — 型号/OE/分类从站点目录与标题确认
- `reference` — 站点描述性文案（应用场景/技术标准）
- `pending` — 站点未公开，待补充（不虚构）
