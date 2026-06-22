# OS10-prod-QA-latest 子栏目 #id 复制 URL - 迭代设计

**文档版本**: v1.0
**创建日期**: 2026-06-22
**文档状态**: 已批准
**迭代版本**: v1.3.0
**迭代类型**: 功能增加
**目标读者**: 技术团队、测试团队

## 执行摘要

在树视图叶节点的 `#id` 文本区域增加点击复制交互，一键将完整 column content API URL 写入剪贴板，解决调试人员手动拼接 URL 的效率问题。改动仅涉及 `buildNode()` 函数内约 15 行代码。

---

## 1. 迭代背景与目标

### 1.1 迭代驱动因素

**业务驱动**:
- 调试人员需频繁获取子栏目的 column content 接口 URL，当前需手动拼接（含动态 token），容易出错且耗时

### 1.2 现状分析

**当前系统状态**:
- `#id` 区域：仅展示文本，无交互能力
- 调试获取 URL：手动拼接，每次约 30s+

**存在问题**:
- `#id` 文本无法直接转化为可用的调试 URL，需人工干预

### 1.3 迭代目标

**主要目标**:
1. 点击叶节点 `#id` 区域，完整 URL 自动写入剪贴板
2. 复制成功后有明确视觉反馈（"✓ Copied!" 1.5s）
3. 不影响现有弹窗主流程（stopPropagation 阻止冒泡）

**成功标准**:
- AC1: 剪贴板内容 = `https://saas.zeasn.tv/sp/api/device/v1/column/content?token=<token>&columnIds=<id>`
- AC2: "✓ Copied!" 视觉反馈正常
- AC3: #id 点击不触发 contentModal
- AC4: 节点名称点击弹窗无回归
- AC5: Clipboard API 失败时 alert 降级

---

## 2. 变更设计

### 2.1 变更范围

**涉及组件**:
- `OS10-prod-QA-latest.html` — `buildNode()` 函数内 `#id` `<small>` 元素 [新增 click handler]

**不涉及组件**:
- `renderSubcolPreview()`、`renderModalContent()`、`getColumnContent()` 等所有其他函数均不变更
- CSS 样式不变更
- 无新增依赖

### 2.2 技术方案

#### 2.2.1 功能设计

**新增功能**:
- 叶节点 `#id` `<small>` 元素绑定独立 click handler，核心逻辑：

```javascript
// 在 buildNode() 内，构建 $content 后、绑定 node-content click 之前
if (!isParentNode) {
    const $idBadge = $content.find('small');
    $idBadge.css('cursor', 'pointer').on('click', async function(e) {
        e.stopPropagation();  // 阻止冒泡，不触发 contentModal
        const url = `${API_BASE_URL}/sp/api/device/v1/column/content?token=${globalToken}&columnIds=${item.id}`;
        try {
            await navigator.clipboard.writeText(url);
            const orig = $(this).text();
            $(this).text('✓ Copied!');
            setTimeout(() => $(this).text(orig), 1500);
        } catch (err) {
            alert('Copy failed. URL:\n' + url);
        }
    });
}
```

**样式**:
- `cursor: pointer` 通过 JS 内联设置，无需修改 CSS

---

## 3. 关键流程变更

### 3.1 #id 区域点击行为变更

#### 3.1.1 变更前流程

用户点击 `#id` 文字 → 事件冒泡到 `.node-content` → 触发 contentModal 弹窗（非预期行为，#id 只是静态文本）

#### 3.1.2 变更后流程

用户点击 `#id` 文字 → `$idBadge click handler` 捕获 → `stopPropagation()` 阻止冒泡 → 调用 `clipboard.writeText(url)` → 文本短暂变为 "✓ Copied!" → 1.5s 后恢复

用户点击节点名称文字 → 事件冒泡到 `.node-content` → 触发 contentModal 弹窗（原有行为保持不变）

#### 3.1.3 改进效果
- #id 区域具备明确的复制交互语义
- 不影响节点名称区域的原有弹窗逻辑

---

## 4. 兼容性与风险分析

### 4.1 兼容性评估

| 兼容性类型 | 影响评估 | 保证措施 | 验证方法 |
|------------|----------|----------|----------|
| 现有弹窗流程 | 无影响（stopPropagation 隔离） | 人工回归 | 点击节点名称验证弹窗正常 |
| 父节点 #id | 无影响（仅对 !isParentNode 绑定） | 代码条件判断 | 目测父节点无 cursor:pointer |
| 浏览器兼容 | Chrome 89+ 均支持 Clipboard API | try/catch alert 降级 | 人工测试 |

### 4.2 风险识别与控制

| 风险类型 | 风险描述 | 影响程度 | 预防措施 | 应急预案 |
|----------|----------|----------|----------|----------|
| 事件冒泡误阻 | stopPropagation 影响范围超预期 | 低 | 仅在 `$idBadge` 上绑定，不在父元素绑定 | 移除 handler 回滚 |
| Clipboard 权限 | file:// 协议 Clipboard API 被浏览器策略阻止 | 低 | try/catch + alert 降级 | 已覆盖 |

### 4.3 回滚策略

**回滚触发条件**:
- 原有 contentModal 弹窗功能异常

**回滚步骤**:
1. 删除 `$idBadge` 上的 click 绑定代码（约 15 行）
2. 删除 `cursor: pointer` 样式设置

---

## 附录

### C. 变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
|------|------|----------|--------|
| v1.0 | 2026-06-22 | 初始版本 | AI |
