# 版本迭代设计文档 - 子栏目内容预览条

**文档版本**: v1.0
**创建日期**: 2026-06-17
**文档状态**: 已批准
**迭代版本**: v1.1.0
**迭代类型**: 功能增加
**目标读者**: 技术团队

## 执行摘要

在 OS10-prod-QA-latest.html 首页树形视图的每个叶子节点名称下，新增水平滚动内容预览条，通过 IntersectionObserver 懒加载展示子栏目缩略图与名称，无需弹窗即可扫描数据。

---

## 1. 迭代背景与目标

### 1.1 迭代驱动因素

**业务驱动**:
- QA/开发人员核查数据时需逐一点击子栏目弹窗，效率低
- 首屏信息密度不足，无法快速判断各子栏目数据是否正常

### 1.2 现状分析

**当前系统状态**:
- 叶子节点仅显示名称和 ID，无内容预览
- 查看内容需点击节点 → 等待接口 → 阅读弹窗 → 关闭，共 4 步

**存在问题**:
- 每次核查一个子栏目需 2-3 次额外操作，批量核查成本高

### 1.3 迭代目标

**主要目标**:
1. 叶子节点名称下方展示水平滚动内容预览条
2. 懒加载：仅视口内节点触发接口请求
3. 响应式：宽屏可见 6-7 个，窄屏可见 4-5 个

**成功标准**:
- 所有叶子节点下出现预览条，父节点不出现
- 骨架屏占位，数据到达后渲染
- 空数据显示 "no data"，失败重试一次后显示 "Failed to load"
- 移动端 touch 手势平滑滑动

---

## 2. 变更设计

### 2.1 变更范围

**涉及组件**:
- `OS10-prod-QA-latest.html` — CSS `<style>` 块：新增预览条/骨架屏样式
- `OS10-prod-QA-latest.html` — JS `renderTree()` 函数：叶子节点渲染时注入预览条容器
- `OS10-prod-QA-latest.html` — JS 新增函数：`initSubcolPreview()`、`renderSubcolPreview()`

**不涉及组件**:
- `getColumnContent()` 函数（仅复用，不修改签名）
- `renderModalContent()` 函数（点击预览项时复用，不修改）
- 所有弹窗 HTML 结构（不变）
- 其他 `.html` 文件

### 2.2 技术方案

#### 2.2.1 功能设计

**新增功能**:

1. **预览条容器** — 在 `buildNode()` 中，叶子节点（`!isParentNode`）的 `$li` 内追加 `.subcol-preview-strip-wrapper`，内含骨架屏和滚动容器
2. **IntersectionObserver 懒加载** — `initSubcolPreview(columnId, wrapper)` 创建 Observer，节点进入视口（threshold: 0.1）时调用 `getColumnContent()`，完成后 disconnect
3. **内容渲染** — `renderSubcolPreview(wrapper, dataList, columnId)` 将 dataList 渲染为内容项（img + span），点击项时复用现有 contentModal 流程
4. **骨架屏** — 加载中显示 6 个灰色矩形占位块，加载完成/失败后替换

**CSS 关键设计**:

```
.subcol-preview-strip          // 水平滚动容器
  display: flex
  align-items: flex-start      // 各item顶部对齐，高度各异不互相拉伸
  overflow-x: auto
  -webkit-overflow-scrolling: touch   // iOS 惯性滚动
  scroll-behavior: smooth
  gap: 8px
  padding: 4px 2px 8px 2px

.subcol-preview-item           // 单个内容项
  flex: 0 0 auto
  width: calc((100% - 6*8px) / 6.5)  // 宽屏约 6-7 个
  display: flex
  flex-direction: column
  overflow: hidden

.subcol-preview-item img       // 图片原始比例，不裁切，无灰色留白
  display: block
  width: 100%                  // 填满item全宽，无两侧空白
  height: auto                 // 保持原始宽高比，竖图约为横图2倍高

.subcol-preview-name           // 名称，受item宽度约束，不会撑宽
  width: 100%
  -webkit-line-clamp: 2        // 最多2行，超出省略
  word-break: break-word

@media (max-width: 768px)
  .subcol-preview-item
    width: calc((100% - 4*8px) / 4.5)  // 窄屏约 4-5 个

.subcol-skeleton-item          // 骨架屏占位块
  background: linear-gradient(90deg, #e9ecef 25%, #f8f9fa 50%, #e9ecef 75%)
  background-size: 200% 100%
  animation: skeleton-shimmer 1.4s infinite
```

**接口复用**（无变更）:
- 使用现有 `getColumnContent(columnId)` 函数
- 失败重试逻辑在 `initSubcolPreview` 内实现（try/catch + 一次重试）

### 2.3 架构变更

本次迭代无架构变更，属单文件功能增量。

变更前：叶子节点 = `node-content` div（名称 + ID）

变更后：叶子节点 = `node-content` div + `.subcol-preview-strip-wrapper`（骨架屏 → 预览条）

---

## 3. 关键流程变更

### 3.1 子栏目内容查看流程

**变更前**:
用户 → 点击叶子节点 → 等待接口响应 → contentModal 展示 → 关闭弹窗

**变更后**:
页面滚动 → 节点进入视口 → 自动懒加载预览条（后台静默）
用户 → 扫描预览条（0次点击即可预览）
用户 → 点击预览项（可选）→ contentModal 展示完整内容

**改进效果**:
- 数据核查从"逐一弹窗"变为"首屏扫描"
- 弹窗流程保留，不影响现有操作习惯

---

## 4. 兼容性与风险分析

### 4.1 兼容性评估

| 兼容性类型 | 影响评估 | 保证措施 |
|------------|----------|----------|
| IntersectionObserver | Chrome 58+/Firefox 55+，已覆盖目标范围 | 无需 polyfill |
| CSS overflow-x scroll | 全平台支持 | `-webkit-overflow-scrolling: touch` 覆盖 iOS |
| 现有弹窗流程 | 不受影响，新增 DOM 不干扰现有事件 | 点击事件 stopPropagation 隔离 |

### 4.2 风险识别与控制

| 风险类型 | 风险描述 | 影响程度 | 预防措施 |
|----------|----------|----------|----------|
| 并发请求过多 | 首屏多个节点同时进入视口触发请求 | 低 | IntersectionObserver 默认批量通知，已足够；可加 100ms debounce |
| token 过期 | 懒加载时 globalToken 已失效 | 低 | 复用现有 getColumnContent 错误处理，显示 "Failed to load" |
| 布局撑高 | 预览条增加节点高度，影响树形布局 | 低 | 固定 max-height，overflow hidden |

### 4.3 回滚策略

**回滚触发条件**:
- 预览条导致页面 JS 报错影响主流程

**回滚步骤**:
1. 注释掉 `$li.append($previewWrapper)` 一行
2. 刷新页面验证主流程正常

**回滚验证**:
- 叶子节点点击弹窗功能正常

---

## 附录

### A. 相关文档

- 需求分析文档: `docs/requirements/requirements-analysis-v1.1.0.md`
- 开发计划文档: `docs/plan/development-plan-v1.1.0.md`

### C. 变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
|------|------|----------|--------|
| v1.0 | 2026-06-17 | 初始版本 | AI |
| v1.1 | 2026-06-17 | 更新 CSS 关键设计：img 改为 width:100%/height:auto（无裁切无灰色），strip 加 align-items:flex-start，名称加 line-clamp:2 | AI |
