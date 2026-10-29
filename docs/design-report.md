# Filter 产品数据库设计报告 (Design Report)

> 交付：data.filterhub 仓（核心交付）
> 设计日期：2026-10-29
> 输入：5 站官网深度抓取（hbxueyuan / airyfilter / klcintl / yitong-filter / cleanroom-ffu）

## 1. 目标

设计一个**全面、可扩展、可溯源**的 filter 产品数据库结构，覆盖空气/机油/燃油/液压/空调/洁净室 FFU 等全品类滤清器，用 5 站真实字段校准，且**零编造**——缺失字段明确标 `pending`。

## 2. 交付物清单

| 文件 | 内容 |
|---|---|
| `docs/schema-design.md` | 实体关系说明 + ASCII ER 图 + 品类树 + 应用场景枚举 |
| `docs/field-dictionary.md` | 13 张表逐字段：名称/类型/必填/枚举值/来源依据/数据状态 |
| `docs/data-status.md` | verified/catalog-confirmed/reference/pending 四态体系 |
| `data/products.json` | 104 个真实结构化 SKU（5 站，Phase 3 补全）|
| `mkdocs.yml` | MkDocs 文档站骨架 |

## 3. 结构规模

- **实体数**：13（company、category、product、oe_reference、spec、material、filter_media、manufacturing_process、application、factory_capacity、packaging、moq、source）
- **关联表**：1（product_application，M:N）
- **字段数**：约 70+（详见 field-dictionary.md）
- **枚举体系**：品类树 17+ 节点、应用场景 medium 6 类、spec_key 9 类、材质 20+ 枚举值

## 4. 设计要点

### 4.1 OE 交叉参考独立建模
hbxueyuan 提供大量 OE 号（如 23401-1441、42N-62-15470、35330-60070），跨 Komatsu/Volvo/Mercedes-Benz/Mitsubishi 品牌。因此 `oe_reference` 独立成表，一个 `product` 可关联多个 OE 号，支持 OE 号反查。

### 4.2 技术参数 key-value 化
不同品类参数差异大（空气滤：效率/压降/容尘；金属滤芯：过滤精度 μm；FFU：风量/洁净度）。`spec` 用 `spec_key + spec_value + unit` 键值对建模，兼容全品类，新增参数无需改表。

### 4.3 溯源与状态内建
`source` 表记录 `entity + entity_id + site + url + crawl_date + data_status`，每个事实字段可追溯到来源页与抓取日期，字段级标注状态（verified/catalog-confirmed/reference/pending）。

### 4.4 真实字段校准
字段枚举值全部来自站点真实数据：
- 效率等级：G1–G4、M5–M9、F7/F8/F9、H10–H14、U15–U17（yitong/cleanroom 表格原文）
- 材质：SS304/SS316L/Ti、PP/PVDF/PTFE/NL/GF/PET、Silicon/EPDM/Viton/FEP/NBR（yitong 表格原文）
- 规格：610×610×70mm、4000–5000 CMH、80°C、Class 100、1–100μm（cleanroom/yitong 表格原文）

## 5. 数据状态统计（14 个样例产品）

| 状态 | 说明 | 覆盖 |
|---|---|---|
| catalog-confirmed | 产品名/OE 号/分类 | 14/14（100%）|
| verified | 规格/材质/价格/等级 | yitong 3、cleanroom 3、airyfilter（MOQ）|
| reference | 应用场景/技术标准 | 全部 |
| pending | 压降/容尘/克重/包装 | 多数产品（诚实标注，未虚构）|

## 6. 已知局限与后续

- **压降/容尘/克重**：5 站文字层普遍未公开，标记 `pending`，待从供应商目录 PDF / 询价回复补充。
- **klcintl 公司信息**：站点 company 页正文极薄，工厂面积/产能/认证未公开，`pending`。
- **hbxueyuan 产品规格**：产品页仅标题 + 一句话描述，规格参数需从 PDF 目录补全。
- **airyfilter 产品规格**：规格存于图片/JS 渲染，文字层不完整。

## 7. 验证结论

- 两仓文件落盘完整（filterhub：5 站 MD + README + crawl-report；data.filterhub：schema-design + field-dictionary + data-status + products + mkdocs.yml + design-report）
- 5 站 MD 完整性：站点数 5/5，字数 3,183–4,592 字符/篇
- 数据库结构三文档：实体（schema-design）/ 字段（field-dictionary）/ 状态（data-status）齐全
- 结构化 SKU：104 个（Phase 3 从 5 站逐站提取，覆盖 13 主品类；字节一致同步主站 src/data/products.json）
