# OS10-prod-QA-latest 子栏目 #id 复制 URL - 开发计划

**创建日期**: 2026-06-22
**需求文档**: `docs/requirements/requirements-analysis-v1.3.0.md`
**迭代设计文档**: `docs/releases/iteration-design-v1.3.0.md`

---

## 总览

单函数内 click handler 新增，改动极小，按"逻辑实现 → 测试验收"两阶段推进。全部修改集中在 `OS10-prod-QA-latest.html` 的 `buildNode()` 函数。

| 里程碑 | 任务数 | 验收标准 | 状态 |
| ------ | ------ | -------- | ---- |
| M1: #id click handler 实现 | 1 | 叶节点 #id 点击后 URL 写入剪贴板，显示 "✓ Copied!" 反馈，不触发弹窗 | ✅ 已完成 |
| M2: 测试与验收 | 3 | 所有 AC1-AC5 通过，主流程无回归，Console 无 JS error | ✅ 已完成 |

> 状态标记：⏳ 待开始 / 🔄 进行中 / ✅ 已完成

---

## M1: #id click handler 实现

> 目标：在 `buildNode()` 叶节点分支内，对 `<small>` 元素绑定独立 async click handler，实现 URL 复制 + 视觉反馈 + 降级处理

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M1-1 | 在 `buildNode()` 的 `!item.children?.length` 叶节点分支内，找到 `$content.find('small')` 对应的 `<small>` 元素，绑定独立 click handler：`stopPropagation()` 阻止冒泡；构造 column content URL（`API_BASE_URL + /sp/api/device/v1/column/content?token=${globalToken}&columnIds=${item.id}`）；调用 `navigator.clipboard.writeText(url)`；成功后文本变为 "✓ Copied!" 并 1.5s 后恢复；catch 块 alert 弹出完整 URL；设置 `cursor:pointer` | OS10-prod-QA-latest.html（`buildNode` 函数体） | 打开 HTML，点击叶节点 #id 区域，确认剪贴板内容正确，文本短暂变为 "✓ Copied!"，不弹出 contentModal | ✅ |

**M1 完成标志**: 点击叶节点 #id 区域，剪贴板内容为完整 column content URL，"✓ Copied!" 反馈正常，不触发 contentModal 弹窗

---

## M2: 测试与验收

> 目标：覆盖所有验收标准，确认无回归

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M2-1 | 功能验收：点击叶节点 #id 区域，粘贴到浏览器地址栏，确认 URL 包含正确 token 和 columnId（AC1）；确认 "✓ Copied!" 反馈正常显示 1.5s 后恢复（AC2）；确认 contentModal 未弹出（AC3） | — | 人工验收，对照 AC1-AC3 | ✅ |
| M2-2 | 回归验收：点击叶节点名称区域（非 #id），确认 contentModal 正常弹出（AC4）；父节点 #id 无 cursor:pointer 无多余交互；Console 无 JS error | — | 人工验收，对照 AC4 | ✅ |
| M2-3 | 降级验收（可选）：模拟 Clipboard API 不可用（DevTools 禁用权限或使用 `navigator.clipboard = undefined`），确认 alert 弹出完整 URL（AC5） | — | DevTools 模拟验收 | ✅ |

**M2 完成标志**: AC1-AC5 全部通过，Console 无 JS error，主流程弹窗功能无回归

---

## 开发约定

- **验证方式**: 每个子任务完成后在浏览器中即时验证（DevTools + 真实 API）
- **文件修改**: 所有改动集中在 `OS10-prod-QA-latest.html` 的 `buildNode()` 函数，仅新增 #id click handler 部分
- **行分隔符**: 写入前确保 LF（`\n`），零容忍 CRLF
- **不引入新依赖**: 不添加任何外部 JS/CSS 库
