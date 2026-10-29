# 数据状态体系 (Data Status)

数据状态用于标注每个事实字段的可信度与来源。任何字段必须携带 `data_status`，避免把"推测"当成"事实"。

## 状态定义

| 状态 | 定义 | 判断标准 | 示例 |
|---|---|---|---|
| `verified` | 站点文字层直接提取，字段值可信 | 抓取的正文/表格中明确出现该值 | cleanroom-ffu 的 HEPA 价格表、yitong 的生产设备参数 |
| `catalog-confirmed` | 型号/OE 号/分类从站点目录与标题确认 | 出现在产品标题、URL、导航或文件名中 | hbxueyuan 的 OE 号（23401-1441）、klcintl 的产品分类 |
| `reference` | 站点描述性文案（应用场景、技术标准、认证） | 出现在公司介绍/应用页/博客文案中 | airyfilter 的 ISO 16890/EN779/ASHRAE 52.2 描述 |
| `pending` | 站点未公开该字段，待补充 | 抓取文字中无该字段 | hbxueyuan 产品页的尺寸/效率/压降 |

## 使用约定

1. **不虚构**：`pending` 字段保持空值，绝不填入推断值或行业典型值。
2. **可追溯**：每个字段可追溯到 `source` 表（site + url + crawl_date + data_status）。
3. **状态可升级**：当从其它来源（供应商目录 PDF、询价回复、第三方数据库）补充字段后，状态从 `pending` → `verified` 或 `catalog-confirmed`，并记录新来源。
4. **混合字段**：一个产品可能部分字段 `verified`、部分 `pending`，字段级标注（而非产品级整体标注）。

## 状态与字段映射（示例）

| 字段 | 常见状态 | 说明 |
|---|---|---|
| product.name / sku | catalog-confirmed | 产品名/OE 号来自标题 |
| spec.dimension | verified / pending | 有规格表则 verified，否则 pending |
| spec.efficiency | verified / pending | 同上 |
| spec.pressure_drop | pending（多数）| 5 站文字层普遍未公开压降 |
| spec.dust_holding | pending（多数）| 同上 |
| material.frame | catalog-confirmed | 帧材质常出现在产品名/描述 |
| filter_media.fiber | catalog-confirmed | 玻纤/合成纤维/活性炭等 |
| moq | verified / reference | airyfilter 明确 MOQ 20卷/200套 |
| factory_capacity | verified / pending | yitong/hbxueyuan/airyfilter 有，klcintl pending |
| price | verified / pending | cleanroom 有价格表，其余 pending |

## 字段状态统计（当前 5 站样本）

- `verified` 字段集中在：公司概况、产品线分类、等级表（ISO 16890/EN 1822）、价格表（cleanroom）、设备参数（yitong）、FFU 规格（cleanroom）。
- `pending` 字段集中在：多数产品的压降（pressure drop）、容尘量（dust holding capacity）、克重（grammage）、滤材效率曲线、包装规格、MOQ（除 airyfilter 外）。
