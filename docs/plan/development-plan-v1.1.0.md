# OS10-prod-QA-latest 子栏目内容预览条 - 开发计划

**创建日期**: 2026-06-17
**需求文档**: `docs/requirements/requirements-analysis-v1.1.0.md`
**迭代设计文档**: `docs/releases/iteration-design-v1.1.0.md`

---

## 总览

单文件增量开发，按"样式 → 逻辑 → 测试"三阶段推进。全部修改集中在 `OS10-prod-QA-latest.html`。

| 里程碑 | 任务数 | 验收标准 | 状态 |
| ------ | ------ | -------- | ---- |
| M1: CSS 样式层 | 2 | 静态骨架屏和预览条在页面中正确渲染 | ✅ 已完成 |
| M2: JS 逻辑层 | 3 | 懒加载、内容渲染、点击交互全部可用 | ✅ 已完成 |
| M3: 测试与验收 | 3 | 所有验收标准通过，无 JS 错误 | ✅ 已完成 |

> 状态标记：⏳ 待开始 / 🔄 进行中 / ✅ 已完成

---

## M1: CSS 样式层

> 目标：新增预览条容器样式、骨架屏动画样式，响应式断点正确

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M1-1 | 新增预览条容器样式：`.subcol-preview-strip-wrapper`、`.subcol-preview-strip`、`.subcol-preview-item`、`.subcol-preview-item img`、`.subcol-preview-name`，含响应式媒体查询 | OS10-prod-QA-latest.html（`<style>` 块） | 浏览器 DevTools 确认宽屏 item 宽度约占 1/6.5 容器宽、窄屏约 1/4.5 | ✅ |
| M1-2 | 新增骨架屏样式：`.subcol-skeleton`、`.subcol-skeleton-item`，含 shimmer 动画 `@keyframes skeleton-shimmer` | OS10-prod-QA-latest.html（`<style>` 块） | 页面中手动插入骨架屏 HTML 可见灰色闪烁占位块 | ✅ |

**M1 完成标志**: 在 DevTools Elements 面板手动添加 `.subcol-preview-strip-wrapper` 节点，预览条和骨架屏样式均正确呈现，无 CSS 报错

---

## M2: JS 逻辑层

> 目标：实现懒加载预览条完整交互逻辑，与现有树形渲染无缝集成

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M2-1 | 新增 `renderSubcolPreview(wrapper, dataList, columnId)` 函数：渲染内容项（img + name），处理空数据（"no data"）和图片加载失败（占位图），绑定点击事件复用 contentModal | OS10-prod-QA-latest.html（`<script>` 块） | 直接调用函数传入模拟 dataList，确认内容项正确渲染、点击打开 contentModal | ✅ |
| M2-2 | 新增 `initSubcolPreview(columnId, wrapper)` 函数：创建 IntersectionObserver，进入视口后显示骨架屏、调用 `getColumnContent()`，成功后调用 `renderSubcolPreview`，失败重试一次，仍失败显示 "Failed to load" | OS10-prod-QA-latest.html（`<script>` 块） | Network 面板确认仅视口内节点触发 column/content 请求；滚动页面验证懒加载时机 | ✅ |
| M2-3 | 修改 `buildNode()` 函数：叶子节点（`!isParentNode`）的 `$li` 内追加 `.subcol-preview-strip-wrapper`，并调用 `initSubcolPreview(item.id, wrapper)` | OS10-prod-QA-latest.html（`buildNode` 函数体） | 页面加载后叶子节点下方出现骨架屏，父节点无骨架屏 | ✅ |

**M2 完成标志**: 打开页面后，叶子节点下方自动出现骨架屏，滚动后骨架屏替换为内容缩略图，点击内容项可打开 contentModal

---

## M3: 测试与验收

> 目标：覆盖所有验收标准，确认无回归问题

| 任务 | 描述 | 产出文件 | 验证方式 | 状态 |
| ---- | ---- | -------- | -------- | ---- |
| M3-1 | 响应式布局验证：宽屏（≥992px）可见 6-7 个、窄屏（<768px）可见 4-5 个；移动端模拟器 touch 滑动流畅 | — | DevTools Device 模式切换断点，截图对比；Mobile 模式拖拽滑动 | ✅ |
| M3-2 | 异常场景验证：空 dataList 显示 "no data"；Network 拦截模拟失败，确认重试后显示 "Failed to load"；图片 URL 替换为无效地址，确认显示占位图 | — | DevTools Network 面板手动 Block 请求 URL | ✅ |
| M3-3 | 回归验证：叶子节点原有点击弹窗流程正常；父节点展开折叠无异常；Console 无 JS 报错 | — | 完整走一遍主流程，Console 无 error | ✅ |

**M3 完成标志**: 所有验收标准通过，Console 无 JS error，主流程弹窗功能无回归问题

---

## 开发约定

- **验证方式**: 每个子任务完成后在浏览器中即时验证（DevTools + 真实 API）
- **文件修改**: 所有改动集中在 `OS10-prod-QA-latest.html`，分区域（CSS / JS）修改，每步验证后再进行下一步
- **行分隔符**: 写入前确保 LF（`\n`），零容忍 CRLF
- **不引入新依赖**: 不添加任何外部 JS/CSS 库
