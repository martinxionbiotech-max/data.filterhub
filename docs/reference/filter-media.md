# 滤材介质对比 (Filter Media Comparison)

> 来源：5 站深度抓取（2026-10-29）。字段级数据状态标注，缺失字段 `pending`，不虚构。

## 滤材类型对比

| 滤材类型 | 典型用途 | 效率等级锚点 | 来源站 | 数据状态 |
|---|---|---|---|---|
| 针刺棉 (needle-punched) | HVAC 预过滤、天花板滤卷 | F5 / MERV 5（示例） | airyfilter | `catalog-confirmed` |
| 合成纤维 (synthetic fiber) | HVAC 面板/袋式、耐高温初效 | M5–F9 | airyfilter, klcintl | `catalog-confirmed` |
| 微玻纤 (micro glass fiber) | HEPA/ULPA 高效过滤 | H13/H14/U15 | yitong, cleanroom | `catalog-confirmed` |
| 活性炭 (activated carbon) | 除味/化学蒸汽 | — | airyfilter, klcintl, cleanroom | `catalog-confirmed` |
| PP/PVDF/PTFE 膜 | 液体过滤 | 过滤精度 μm | yitong | `verified` |
| 烧结金属网 (sintered mesh) | 液体/高温过滤 | 1–100 μm | yitong | `verified` |

## 关键差异

- **针刺棉 vs 合成纤维**：针刺棉为非织造毡状结构，容尘高、用于粗滤；合成纤维强度与寿命更高，用于中效袋式与面板。
- **微玻纤 vs 合成纤维**：微玻纤效率高（可到 HEPA/ULPA），但需分隔结构（隔板/mini-pleat）；合成纤维强度高但效率上限低于微玻纤。
- **活性炭**：吸附气相污染物，不替代颗粒过滤，通常与颗粒滤级组合使用。
- **膜滤芯 vs 金属滤芯**：膜（PP/PVDF/PTFE）用于化学兼容性要求高的液体；金属（SS304/SS316L/Ti）用于高温/高压/可清洗再生场景。

## 未公开字段（诚实标注）

- 克重 (grammage)：5 站文字层普遍未公开，`pending`。
- 效率曲线 (efficiency curve)：未公开，`pending`。
- 具体滤材厚度：未公开，`pending`。

数据状态体系见 [data-status](../data-status.md)。
