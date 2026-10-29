# 测试标准 (Test Standards)

> 效率等级分类锚点。来源：5 站抓取 + 行业标准参考。逐型号数值在 5 站文字层普遍未公开，`pending`。

## 效率等级标准

| 标准 | 适用品类 | 等级/值 | 来源依据 | 数据状态 |
|---|---|---|---|---|
| EN 1822 | HEPA/ULPA | H10–H14（EPA/HEPA）、U15–U17（ULPA） | yitong 等级表、cleanroom | `verified` |
| ISO 16890 | HVAC/通风 | ePM1 / ePM2.5 / ePM10 / ePM coarse | yitong 等级表 | `verified` |
| EN 779 | HVAC 初/中效 | G1–G4 / M5–M6 / F7–F9 | yitong、cleanroom | `verified` |
| ISO 5011 | 发动机进气 | 多循环效率 + 容尘量 | 行业标准（5 站未逐型号公开） | `reference` |
| ASHRAE 52.2 | HVAC（美标） | MERV 级 | airyfilter | `reference` |
| UL 900 / DIN 5510 | 阻燃 | 阻燃级 | airyfilter | `reference` |

## 标准适用性说明

- **EN 1822**：洁净室/高效过滤的核心效率分级，H13/H14 为高效 HEPA，U15+ 为超低穿透 ULPA。
- **ISO 16890**：以颗粒物粒径分级（PM1/PM2.5/PM10），取代旧 EN 779 的中效分级口径，适用于一般通风。
- **ISO 5011**：发动机进气空气滤清器的多循环试验标准（效率 + 容尘量）。本仓 5 站未逐型号公开该值，相关字段 `pending`，不编造。
- **ISO 4406**：液压油洁净度分级，用于液压滤选型（见液压滤品类）。

## 诚实声明

测试标准的「等级值」在 yitong/cleanroom 两站为表格原文（`verified`）；其余站仅作描述性引用（`reference`）。逐型号效率/压降/容尘数据 5 站普遍未公开，见 [data-status](../data-status.md)。
