# OS10-prod-QA-latest 预览行点击直达 Resource Details - 开发计划

**创建日期**: 2026-06-19
**需求文档**: `docs/requirements/requirements-analysis-v1.2.0.md`
**迭代设计文档**: `docs/releases/iteration-design-v1.2.0.md`

---

## 总览

单函数内 click handler 替换，改动极小，按"逻辑实现 → 测试验收"两阶段推进。全部修改集中在 `OS10-prod-QA-latest.html` 的 `renderSubcolPreview()` 函数。

| 里程碑 | 任务数 | 验收标准 | 状态 |
| ------ | ------ | -------- | ---- |
| M1: click handler 改写 | 1 | 支持类型 item 点击直达 resourceDetailModal，不支持类型弹 "No details available" | ✅ 已完成 |
| M2: 测试与验收 | 3 | 所有验收标准通过，主流程无回归，Console 无 JS error | ✅ 已完成 |

> 状态标记：⏳ 待开始 / 🔄 进行中 / ✅ 已完成

---

## M1: click handler 改写

> 目标：将 `renderSubcolPreview()` 内 item click handler 从 contentModal 流程改为 Resource Details 流程

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M1-1 | 替换 item click handler：增加 contentType=43 前置判断（弹提示）；增加 rsType=2/30/31/32 不支持判断（弹提示）；增加 objectType 解析及支持类型判断；支持类型调用 `showDetailLoading` + `getResourceDetail` + `renderResourceDetail`；其余弹 alert "No details available" | OS10-prod-QA-latest.html（`renderSubcolPreview` 函数体） | 点击 rsType=6/12 item 弹出 resourceDetailModal；点击 rsType=2/30/31/32 item 弹 "No details available"；点击 contentType=43 match schedule item 弹 "No details available" | ✅ |

**M1 完成标志**: 点击各类型预览 item，行为符合类型判断逻辑，resourceDetailModal 正常弹出并展示详情内容

---

## M2: 测试与验收

> 目标：覆盖所有验收标准，确认无回归

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M2-1 | 支持类型验收：分别点击 rsType=6、rsType=12、objectType=REC_CHANNEL、objectType=REC_PROGRAM 的预览 item，确认 resourceDetailModal 弹出并渲染详情 | — | 人工验收，对照 AC1-AC5 | ✅ |
| M2-2 | 不支持类型验收：点击 rsType=2/30/31/32 item 及 contentType=43 match schedule item，确认弹出 "No details available"；点击其他简单类型（非6/12，非REC_CHANNEL/REC_PROGRAM）item，确认同样弹提示 | — | 人工验收 | ✅ |
| M2-3 | 回归验收：节点名称点击弹窗流程正常；父节点展开折叠无异常；Console 无 JS error | — | 完整走一遍主流程，Console 无 error | ✅ |

**M2 完成标志**: 所有验收标准通过，Console 无 JS error，主流程弹窗功能无回归

---

## 开发约定

- **验证方式**: 每个子任务完成后在浏览器中即时验证（DevTools + 真实 API）
- **文件修改**: 所有改动集中在 `OS10-prod-QA-latest.html` 的 `renderSubcolPreview()` 函数，仅替换 click handler 部分
- **行分隔符**: 写入前确保 LF（`\n`），零容忍 CRLF
- **不引入新依赖**: 不添加任何外部 JS/CSS 库
