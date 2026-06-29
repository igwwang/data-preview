# OS10-prod-QA-latest 首页子栏目预览行时间字段展示 - 开发计划 v1.5.0

**创建日期**: 2026-06-29
**需求文档**: `docs/requirements/requirements-analysis-v1.5.0.md`
**迭代设计文档**: `docs/releases/iteration-design-v1.5.0.md`

---

## 总览

本次迭代改动仅涉及 OS10-prod-QA-latest.html 单文件，按"基础设施→核心逻辑→验证"三段划分里程碑。

| 里程碑 | 任务数 | 验收标准 | 状态 |
| ------ | ------ | -------- | ---- |
| M1: CSS + 工具函数 | 2 | .subcol-preview-time 样式生效，两个格式化函数返回值正确 | ✅ 已完成 |
| M2: renderSubcolPreview 逻辑 | 1 | 有 liveStartTime/releaseTime 的卡片下方正确展示时间 | ✅ 已完成 |
| M3: 测试与验证 | 2 | 全部 AC1~AC6 通过，无回归问题 | ✅ 已完成 |

> 状态标记：⏳ 待开始 / 🔄 进行中 / ✅ 已完成

---

## M1: CSS + 工具函数

> 目标：新增 .subcol-preview-time CSS class 和两个 UTC+8 格式化工具函数，为核心逻辑提供基础设施

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M1-1 | 在 CSS 块中 .subcol-preview-name 规则之后追加 .subcol-preview-time class | OS10-prod-QA-latest.html | 读取文件确认 CSS 内容正确无截断 | ✅ |
| M1-2 | 在 formatUTCDate 函数之后追加 formatUTC8DateTime / formatUTC8Date 两个工具函数 | OS10-prod-QA-latest.html | 读取文件确认两函数完整，验证逻辑正确 | ✅ |

**M1 完成标志**: 文件中存在 .subcol-preview-time class 定义及 formatUTC8DateTime / formatUTC8Date 函数，可通过代码读取核实

---

## M2: renderSubcolPreview 逻辑

> 目标：在 renderSubcolPreview 函数中，四个渲染分支之后、$item.on('click') 之前追加时间字段展示逻辑

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M2-1 | 在 $item.on('click', ...) 之前插入 liveStartTime / releaseTime 条件判断及 DOM 追加代码 | OS10-prod-QA-latest.html | 读取 renderSubcolPreview 函数确认代码位置和内容正确 | ✅ |

**M2 完成标志**: renderSubcolPreview 函数内存在时间字段追加逻辑，位置在 click 绑定之前

---

## M3: 测试与验证

> 目标：在浏览器中实际验证 AC1~AC6，确认无回归

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M3-1 | 文档同步门禁（步骤 6.5）：确认迭代设计、开发计划文档与代码改动一致 | docs/ 各文档 | 逐一读取核对 | ✅ |
| M3-2 | 全链路验证（步骤 8）：在浏览器打开 HTML，检查有/无时间字段的卡片展示是否符合 AC1~AC6 | — | 浏览器截图核对 | ✅ |

**M3 完成标志**: AC1~AC6 全部通过，主卡片区无回归

---

## 开发约定

- **验证方式**: 每个任务完成后读取文件核对改动内容，确认无截断
- **行分隔符**: 写入前确保使用 LF（\n），不引入 CRLF
- **Git**: 不自动 commit/push，由用户决定
- **分批操作**: HTML 文件超 100 行触发分批规则，每次改动独立区域后读取验证
