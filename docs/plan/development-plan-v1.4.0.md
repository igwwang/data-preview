# OS10-prod-QA-latest Country→langCode 联动 - 开发计划

**创建日期**: 2026-06-22
**需求文档**: `docs/requirements/requirements-analysis-v1.4.0.md`
**迭代设计文档**: `docs/releases/iteration-design-v1.4.0.md`

---

## 总览

单文件两处改动，按"逻辑实现 → 测试验收"两阶段推进。全部修改集中在 `OS10-prod-QA-latest.html`。

| 里程碑 | 任务数 | 验收标准 | 状态 |
| ------ | ------ | -------- | ---- |
| M1: 联动逻辑实现 | 2 | COUNTRY_LANG_MAP 新增完毕，clientIpSelect change handler 联动+高亮逻辑就绪 | ✅ 已完成 |
| M2: 测试与验收 | 3 | AC1-AC6 全部通过，Console 无 JS error | ✅ 已完成 |

> 状态标记：⏳ 待开始 / 🔄 进行中 / ✅ 已完成

---

## M1: 联动逻辑实现

> 目标：在 COUNTRY_IP_LIST 定义之后新增 COUNTRY_LANG_MAP 常量，并在 clientIpSelect change handler 中追加联动填充 langCode + 1s 黄色高亮逻辑

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M1-1 | 在 COUNTRY_IP_LIST 定义之后（约第957行）新增 `COUNTRY_LANG_MAP` 常量对象，包含12条 IP→langCode 映射（Spain→es / Portugal→pt / Italy→it / Brazil→pt-BR / Argentina→es / Chile→es / Mexico→es / Japan→ja / France→fr / Germany→de / Hong Kong→zh-HK / USA→en） | OS10-prod-QA-latest.html | 打开 HTML，DevTools Console 中执行 `COUNTRY_LANG_MAP['45.86.202.30']` 返回 `'de'` | ✅ |
| M1-2 | 在 `$('#clientIpSelect').on('change')` handler 中（约第3069行），在 `$('input[name="clientIp"]').val(selectedIp)` 之后追加：查询 COUNTRY_LANG_MAP，若有匹配则 `$('input[name="langCode"]').val(lang)`，并对 langCode 输入框施加 `background-color: #fff3cd`，1000ms 后清除 | OS10-prod-QA-latest.html（clientIpSelect change handler） | 打开 Edit Device Configuration 弹窗，选择 Germany，确认 langCode 输入框变为 `de` 且出现黄色高亮约 1s | ✅ |

**M1 完成标志**: 打开弹窗，选择任意国家，langCode 自动更新且黄色高亮出现后消失，无 Console 报错

---

## M2: 测试与验收

> 目标：覆盖 AC1-AC6，确认无回归

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M2-1 | 功能验收：逐一选择12个国家，核查 langCode 值是否与映射表一致（AC1）；确认黄色高亮约 1s 后恢复（AC2）；选回空选项 "-- Select Country --"，确认 langCode 不变（AC3） | — | 人工验收，对照 AC1-AC3 | ✅ |
| M2-2 | 保存验收：选择 Japan（ja），点击 Save & Reload，确认页面重载后 langCode 参数为 `ja`（AC4）；手动在 IP 文本框输入 `45.86.202.30`，确认 langCode 不联动（AC5） | — | 人工验收，对照 AC4-AC5 | ✅ |
| M2-3 | 回归验收：选择国家后点击 Save & Reload，确认 countryCode、mac、deviceType 等字段值无变化（AC6）；Console 无 JS error | — | DevTools Console + 人工验收 | ✅ |

**M2 完成标志**: AC1-AC6 全部通过，Console 无 JS error，保存/重置主流程无回归

---

## 开发约定

- **验证方式**: 每个子任务完成后在浏览器中即时验证（DevTools + 弹窗交互）
- **文件修改**: 所有改动集中在 `OS10-prod-QA-latest.html`，两处独立修改点
- **行分隔符**: 写入前确保 LF（`\n`），零容忍 CRLF
- **不引入新依赖**: 不添加任何外部 JS/CSS 库
