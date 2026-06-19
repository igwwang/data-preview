# 版本迭代设计文档 - 预览行点击直达 Resource Details

**文档版本**: v1.0
**创建日期**: 2026-06-19
**文档状态**: 已批准
**迭代版本**: v1.2.0
**迭代类型**: 功能修改
**目标读者**: 技术团队

## 执行摘要

将预览条（subcol-preview-strip）item 的点击行为从打开 contentModal 改为直达 Resource Details 弹窗，支持类型直接调用 `getResourceDetail()`，不支持类型统一弹 "No details available"，减少 2-3 步操作。

---

## 1. 迭代背景与目标

### 1.1 迭代驱动因素

**业务驱动**:
- QA/开发人员在预览条中发现异常 item 后，需经过 contentModal 中转才能查看 Resource Details，步骤冗余
- 预览条的设计目标是"快速扫描"，点击应直达详情而非再开一层列表弹窗

### 1.2 现状分析

**当前系统状态**:
- 预览条 item 点击：打开 contentModal（展示该列全部内容列表）
- 从预览条到 Resource Details：需 4-5 步操作

**存在问题**:
- 点击预览 item 打开的是"列"维度的内容，而非"item"维度的详情，与用户预期不符

### 1.3 迭代目标

**主要目标**:
1. 预览条 item 点击直接打开 `#resourceDetailModal`（支持类型）
2. 不支持类型统一弹 alert "No details available"
3. 过渡体验与现有 card click 一致

**成功标准**:
- rsType=6/12 及 objectType=REC_CHANNEL/REC_PROGRAM 的 item 点击直达详情弹窗
- 所有不支持类型弹出统一提示
- 现有 contentModal 及节点点击流程无回归

---

## 2. 变更设计

### 2.1 变更范围

**涉及组件**:
- `OS10-prod-QA-latest.html` — `renderSubcolPreview()` 函数内 item click handler：修改

**不涉及组件**:
- `getResourceDetail()` 函数（复用，不修改）
- `renderResourceDetail()` 函数（复用，不修改）
- `showDetailLoading()` 函数（复用，不修改）
- `#resourceDetailModal` HTML 结构（不变）
- `contentModal` 及相关流程（不变）
- 节点名称点击逻辑（不变）
- 其他 `.html` 文件

### 2.2 技术方案

#### 2.2.1 功能设计

**修改功能**:

- **item click handler**：将原有的 `getColumnContent(columnId)` → `renderModalContent` 流程替换为类型判断 + `getResourceDetail()` → `renderResourceDetail()` 流程

**类型判断逻辑**:

```
支持 Resource Details：
  rsType === 6（APP）
  rsType === 12（MOVIE）
  value 可解析为 JSON 且 objectType === 'REC_CHANNEL'
  value 可解析为 JSON 且 objectType === 'REC_PROGRAM'

不支持（弹 "No details available"）：
  rsType === 2（文本类型）
  rsType === 30（Live Streaming）
  rsType === 31
  rsType === 32（Match Schedule）
  contentType === 43（match schedule item）
  其他简单类型（非上述支持条件）
```

**修改后 click handler 伪代码**:

```js
$item.on('click', async function(e) {
    e.stopPropagation();

    // 跳过 match schedule item（contentType=43 渲染的 item 无 rsType/value）
    if (Number(contentType) === 43) {
        alert('No details available');
        return;
    }

    // 不支持类型直接提示
    if (item.rsType === 30 || item.rsType === 31 || item.rsType === 32 || item.rsType === 2) {
        alert('No details available');
        return;
    }

    // 判断是否为支持 Resource Details 的类型
    let objectType = 'N/A';
    try { objectType = JSON.parse(item.value).objectType || 'N/A'; } catch(e) {}

    const supported = item.rsType === 6 || item.rsType === 12
        || objectType === 'REC_CHANNEL' || objectType === 'REC_PROGRAM';

    if (!supported) {
        alert('No details available');
        return;
    }

    try {
        const detailModal = new bootstrap.Modal('#resourceDetailModal');
        showDetailLoading(detailModal);
        const detailData = await getResourceDetail(item.rsType, item.value);
        renderResourceDetail(detailData, item.rsType);
    } catch (err) {
        alert('Failed to load details: ' + err.message);
    }
});
```

**接口变更**: 无（复用现有 `getResourceDetail()`，签名不变）

### 2.3 架构变更

本次迭代无架构变更，属单函数内 click handler 逻辑替换。

变更前：预览条 item click → `getColumnContent(columnId)` → `renderModalContent`（contentModal）

变更后：预览条 item click → 类型判断 → `getResourceDetail(item.rsType, item.value)` → `renderResourceDetail`（resourceDetailModal）；不支持类型 → alert

---

## 3. 关键流程变更

### 3.1 预览条 item 点击流程

**变更前**:
用户点击预览 item → `getColumnContent(columnId)` → contentModal 展示该列全部内容列表 → 用户需在列表中再次点击目标 card → resourceDetailModal

**变更后**:
用户点击预览 item（支持类型）→ `#resourceDetailModal` 立即弹出（loading spinner）→ `getResourceDetail(item.rsType, item.value)` → 详情内容渲染完成

用户点击预览 item（不支持类型）→ alert "No details available"

**改进效果**:
- 支持类型：从 4-5 步缩减至 1 步
- 不支持类型：即时反馈，无无效等待

---

## 4. 兼容性与风险分析

### 4.1 兼容性评估

| 兼容性类型 | 影响评估 | 保证措施 |
|------------|----------|----------|
| 现有 contentModal 流程 | 不受影响，click handler 仅在预览条 item 上替换 | `e.stopPropagation()` 隔离事件冒泡 |
| 节点名称点击流程 | 不受影响，触发元素不同 | 代码不涉及节点点击逻辑 |
| `#resourceDetailModal` 复用 | 与现有 card click 使用同一弹窗，无冲突 | Bootstrap Modal 实例化方式一致 |

### 4.2 风险识别与控制

| 风险类型 | 风险描述 | 影响程度 | 预防措施 |
|----------|----------|----------|----------|
| value 解析失败 | 部分 item.value 非合法 JSON，objectType 解析异常 | 低 | try/catch 保护，解析失败默认 objectType='N/A'，走不支持分支 |
| contentType=43 item 无 rsType | match schedule item 由 groupInfo 渲染，无标准 rsType/value | 低 | 在类型判断最前置检查 contentType===43，直接弹提示 |
| token 过期 | 详情请求时 globalToken 已失效 | 低 | 复用现有 getResourceDetail 错误处理，catch 后 alert 错误信息 |

### 4.3 回滚策略

**回滚触发条件**:
- 预览条 click 导致 JS 报错影响主流程

**回滚步骤**:
1. 将 item click handler 恢复为原有 `getColumnContent(columnId)` → `renderModalContent` 逻辑
2. 刷新页面验证主流程正常

**回滚验证**:
- 预览条 item 点击可正常打开 contentModal
- Console 无 JS error

---

## 附录

### A. 相关文档

- 需求分析文档: `docs/requirements/requirements-analysis-v1.2.0.md`
- 开发计划文档: `docs/plan/development-plan-v1.2.0.md`
- 上一版迭代设计: `docs/releases/iteration-design-v1.1.0.md`

### C. 变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
|------|------|----------|--------|
| v1.0 | 2026-06-19 | 初始版本 | AI |
