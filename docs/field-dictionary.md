# 字段字典 (Field Dictionary)

逐字段定义：名称 / 类型 / 必填 / 枚举值 / 来源依据 / 数据状态。所有枚举值来自 5 站真实字段（2026-10-29 抓取）。

## 1. company（公司）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string(uuid) | ✅ | — | 系统生成 | verified |
| name | string | ✅ | — | 站点 about 页 | verified |
| brand | string | ✅ | — | 站点品牌名 | verified |
| location | string | ✅ | — | 站点地址 | verified |
| established_year | integer | ❌ | — | 站点沿革 | verified/pending |
| website | string(url) | ✅ | — | 站点 URL | verified |
| factory_area_sqm | integer | ❌ | — | 站点工厂介绍 | verified/pending |
| staff_count | integer | ❌ | — | 站点介绍 | verified/pending |
| monthly_output | integer | ❌ | — | 站点产能 | verified/pending |
| certifications | string[] | ❌ | ISO 9001, ISO 16890, EN 779, EN 1822, ASHRAE 52.2, UL 900, DIN 5510 | 站点认证页 | catalog-confirmed |
| source_url | string(url) | ✅ | — | 站点 URL | verified |

## 2. category（品类）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| code | string | ✅ | air_filter/cabin_filter/oil_filter/fuel_filter/hydraulic_filter/transmission_filter/urea_filter/hvac_filter/hepa_filter/ulpa_filter/activated_carbon_filter/pocket_filter/liquid_filter/metal_cartridge/cleanroom_equipment/ffu/... | 品类树 | verified |
| name | string | ✅ | — | 站点产品导航 | catalog-confirmed |
| parent_id | string | ❌ | 品类树父节点 | 层级关系 | verified |

## 3. product（产品）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| name | string | ✅ | — | 产品页标题 | catalog-confirmed |
| sku | string | ✅ | 型号/OE 号 | 产品页 | catalog-confirmed |
| category_id | string | ✅ | FK→category | 产品归类 | verified |
| company_id | string | ✅ | FK→company | 来源公司 | verified |
| description | string | ❌ | — | 产品页正文 | verified/reference |
| source_url | string(url) | ✅ | — | 产品页 URL | verified |

## 4. oe_reference（OE 交叉参考）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| product_id | string | ✅ | FK→product | 关联 | verified |
| oe_number | string | ✅ | 如 23401-1441、42N-62-15470、35330-60070 | 产品页标题 | catalog-confirmed |
| brand | string | ❌ | Komatsu/Volvo/Mercedes-Benz/Mitsubishi/... | 产品页标题 | catalog-confirmed |
| equipment_type | string | ❌ | 卡车/装载机/拖拉机/联合收割机/乘用车/ATV | 产品页描述 | reference |
| data_status | enum | ✅ | verified/catalog-confirmed/reference/pending | 状态体系 | catalog-confirmed |

## 5. spec（技术参数 key-value）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| product_id | string | ✅ | FK→product | 关联 | verified |
| spec_key | string | ✅ | dimension/efficiency_class/pressure_drop/dust_holding/temperature_resistance/airflow/cleanliness_class/removal_rating | 规格表 | verified/pending |
| spec_value | string | ✅ | 如 "610×610×70mm"、"H14"、"1μm"、"80°C" | 规格表 | verified/pending |
| unit | string | ❌ | mm/inch/Pa/°C/μm/CMH/CFM/m/s/%/USD | 规格表 | verified/pending |
| data_status | enum | ✅ | 状态体系 | — | verified/pending |

### spec_key 枚举与来源依据

| spec_key | 说明 | 来源依据 | 状态 |
|---|---|---|---|
| dimension | 外形尺寸 | cleanroom HEPA 尺寸表、FFU 尺寸 | verified |
| efficiency_class | 效率等级 | G1-G4/M5-M9/H10-H14/U15-U17/F8/F9 | verified |
| pressure_drop | 压降 | 站点普遍未公开 | pending |
| dust_holding | 容尘量 | 站点普遍未公开 | pending |
| temperature_resistance | 耐温 | klcintl 260/350°C、cleanroom 80°C | catalog-confirmed |
| airflow | 风量 | cleanroom FFU 4000-5000 CMH | verified |
| cleanliness_class | 洁净度 | cleanroom FFU Class 100 | verified |
| removal_rating | 过滤精度 | yitong 金属滤芯 1/3/5/10/20/30/50/100μm | verified |
| efficiency_percentage | 过滤效率% | cleanroom 95% DOP | catalog-confirmed |

## 6. material（材质/原料）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| product_id | string | ✅ | FK→product | 关联 | verified |
| part | string | ✅ | frame/end_cap/seal/o_ring/support_layer/housing/core | 站点表格 | catalog-confirmed |
| material_value | string | ✅ | 见下方枚举 | 站点表格 | catalog-confirmed |
| data_status | enum | ✅ | 状态体系 | — | catalog-confirmed |

### material_value 枚举（来自站点表格）

- 帧/壳体 frame/housing：镀锌钢（galvanized steel）、不锈钢（stainless steel/SS304/SS316L）、铝（aluminum）、纸/纸板（cardboard/paper）、钛（Ti）
- 端盖 end_cap：PU（聚氨酯）、215/222/226、DOE、Flat 222、High 222/226、螺纹
- 密封/O 型圈 seal/o_ring：Silicon、EPDM、Viton、FEP、NBR、PEFE、无端垫片（endless gasket）、凝胶（gel）
- 支撑层/内芯 support_layer/core：PP、PET、PTFE、PP mesh
- 滤膜 membrane：PP、PVDF、PTFE、NL、GF、PET

## 7. filter_media（滤材）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| product_id | string | ✅ | FK→product | 关联 | verified |
| type | string | ✅ | needle_punched/synthetic_fiber/micro_glass_fiber/activated_carbon/paper/membrane/sintered_mesh/tio2 | 站点描述 | catalog-confirmed |
| efficiency_class | string | ❌ | G1-G4/M5-M9/H10-H14/U15-U17 | 站点等级表 | verified/pending |
| grammage | string | ❌ | g/m² | 未公开 | pending |
| data_status | enum | ✅ | 状态体系 | — | catalog-confirmed |

## 8. manufacturing_process（生产工艺）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| product_id | string | ✅ | FK→product | 关联 | verified |
| process_name | string | ✅ | pu_potting/pleating/separator_pleating/mini_pleat/sintering/welding/lamination/needle_punching | 站点设备/工艺 | catalog-confirmed |
| equipment | string | ❌ | 折纸机/成型机/覆膜机/针刺机 | 站点设备页 | verified/pending |
| params | json | ❌ | 褶深/速度/纸宽等 | 站点设备参数 | verified/pending |
| data_status | enum | ✅ | 状态体系 | — | catalog-confirmed |

## 9. application（应用场景）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| code | string | ✅ | automotive/heavy_machinery/agricultural/air_compressor/lawn_garden/swimming_pool/paint_booth/hvac/food_beverage/healthcare/pharma/public_transport/commercial_building/industrial/oil_gas/chemical/power/electronics/livestock/water/cleanroom/mushroom/3d_printer/air_purifier/fresh_air | 站点应用页 | catalog-confirmed |
| name | string | ✅ | — | 站点应用页 | catalog-confirmed |
| medium | enum | ✅ | air/oil/fuel/hydraulic/cabin/cleanroom_ffu | 过滤介质 | verified |

## 10. factory_capacity（工厂产能）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| company_id | string | ✅ | FK→company | 关联 | verified |
| area_sqm | integer | ❌ | 24000/10000/22496 | 站点工厂介绍 | verified/pending |
| staff_count | integer | ❌ | 180/90 | 站点介绍 | verified/pending |
| monthly_output | integer | ❌ | 200000 | airyfilter | verified |
| production_lines | string[] | ❌ | PU线/大型空气滤线/HEPA线/滤纸线/FFU线 | 站点设备 | catalog-confirmed |
| data_status | enum | ✅ | 状态体系 | — | verified/pending |

## 11. packaging（包装）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| product_id | string | ✅ | FK→product | 关联 | verified |
| unit | string | ❌ | pcs/roll/set | 站点 MOQ 描述 | reference |
| carton_qty | integer | ❌ | — | 未公开 | pending |
| dimensions | string | ❌ | — | 未公开 | pending |
| weight | string | ❌ | — | 未公开 | pending |

## 12. moq（起订量）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| product_id | string | ✅ | FK→product | 关联 | verified |
| moq_value | integer | ❌ | 20（卷）/200（套）| airyfilter | verified |
| moq_unit | string | ❌ | roll/set/pcs | airyfilter | verified |
| data_status | enum | ✅ | 状态体系 | — | verified/pending |

## 13. source（来源与数据状态）

| 字段 | 类型 | 必填 | 枚举/格式 | 来源依据 | 数据状态 |
|---|---|---|---|---|---|
| id | string | ✅ | — | 系统 | verified |
| entity | string | ✅ | company/product/oe_reference/spec/... | 溯源对象 | verified |
| entity_id | string | ✅ | — | 关联实体 id | verified |
| site | string | ✅ | hbxueyuan.com/airyfilter.com/klcintl.com/yitong-filter.com/cleanroom-ffu.com | 来源站 | verified |
| url | string(url) | ✅ | — | 具体页面 URL | verified |
| crawl_date | date | ✅ | 2026-10-29 | 抓取日期 | verified |
| data_status | enum | ✅ | verified/catalog-confirmed/reference/pending | 状态体系 | verified |
