# 版本迭代设计文档 v1.5.0

**文档版本**: v1.0
**创建日期**: 2026-06-29
**文档状态**: 草案
**迭代版本**: v1.5.0
**迭代类型**: 功能增加
**目标读者**: 技术团队

## 执行摘要

在 OS10-prod-QA-latest.html 首页子栏目预览行卡片下方新增时间字段展示：`liveStartTime` 显示为 `Start Time: YYYY-MM-DD HH:mm:ss`，`releaseTime` 显示为 `Release Time: YYYY-MM-DD`，均采用 UTC+8，帮助 QA 无需翻 Network 面板即可快速核对时间。

---

## 1. 迭代背景与目标

### 1.1 迭代驱动因素

**业务驱动**:
- QA 核对直播排期和内容上线日期时，目前只能手动查看 column/content 接口响应，效率低
- 子栏目预览行只展示缩略图和标题，缺少关键时间维度信息

### 1.2 现状分析

**存在问题**:
- `renderSubcolPreview` 函数渲染卡片时仅追加图片和名称，不输出任何时间字段
- 主卡片区（`#contentContainer`）已有 `liveStartTime` / `releaseTime` 展示逻辑，但子栏目预览行未跟进

### 1.3 迭代目标

**主要目标**:
1. `item.liveStartTime` 存在时，卡片下方展示 `Start Time: YYYY-MM-DD HH:mm:ss`（UTC+8）
2. `item.releaseTime > 0` 时，卡片下方展示 `Release Time: YYYY-MM-DD`（UTC+8）
3. 字段缺失时静默不展示，不影响现有布局

**成功标准**:
- 见需求分析文档 AC1~AC6

---

## 2. 变更设计

### 2.1 变更范围

**涉及组件**:
- `OS10-prod-QA-latest.html` — CSS 区域（新增 class）：修改
- `OS10-prod-QA-latest.html` — JS 工具函数区域（新增两个格式化函数）：新增
- `OS10-prod-QA-latest.html` — `renderSubcolPreview` 函数（追加时间字段逻辑）：修改

**不涉及组件**:
- 主卡片区 `renderModalContent` 逻辑
- `formatUTCDate` / `formatEPGTime` 等现有工具函数
- localStorage、配置弹窗、Token 相关逻辑
- 其他 HTML 文件

### 2.2 技术方案

#### 2.2.1 功能设计

**新增 CSS class** — 追加于现有 `.subcol-preview-name` 规则附近：

```css
.subcol-preview-time {
    width: 100%;
    font-size: 0.75em;
    color: #6c757d;
    margin-top: 2px;
    word-break: break-all;
}
```

**新增工具函数** — 追加于 `formatUTCDate` 函数之后：

```js
// Format timestamp to UTC+8 datetime string: YYYY-MM-DD HH:mm:ss
function formatUTC8DateTime(ts) {
    if (!ts) return null;
    var n = Number(ts);
    if (isNaN(n) || n <= 0) return null;
    // Shift to UTC+8 by adding 8h offset
    var d = new Date(n + 8 * 3600 * 1000);
    var Y = d.getUTCFullYear();
    var M = String(d.getUTCMonth() + 1).padStart(2, '0');
    var D = String(d.getUTCDate()).padStart(2, '0');
    var h = String(d.getUTCHours()).padStart(2, '0');
    var m = String(d.getUTCMinutes()).padStart(2, '0');
    var s = String(d.getUTCSeconds()).padStart(2, '0');
    return Y + '-' + M + '-' + D + ' ' + h + ':' + m + ':' + s;
}

// Format timestamp to UTC+8 date string: YYYY-MM-DD
function formatUTC8Date(ts) {
    if (!ts || Number(ts) <= 0) return null;
    var n = Number(ts);
    if (isNaN(n)) return null;
    var d = new Date(n + 8 * 3600 * 1000);
    return d.getUTCFullYear() + '-' +
        String(d.getUTCMonth() + 1).padStart(2, '0') + '-' +
        String(d.getUTCDate()).padStart(2, '0');
}
```

**修改 `renderSubcolPreview`** — 在各分支渲染完 `$item` 主体后（`$item.on('click', ...)` 之前），统一追加时间字段：

```js
// Append time fields if available (applies to all content branches)
var liveStartFormatted = item.liveStartTime ? formatUTC8DateTime(item.liveStartTime) : null;
if (liveStartFormatted) {
    $item.append(
        $('<div>').addClass('subcol-preview-time').text('Start Time: ' + liveStartFormatted)
    );
}
var releaseFormatted = (item.releaseTime > 0) ? formatUTC8Date(item.releaseTime) : null;
if (releaseFormatted) {
    $item.append(
        $('<div>').addClass('subcol-preview-time').text('Release Time: ' + releaseFormatted)
    );
}
```

**设计说明**:
- 时间逻辑置于四个渲染分支（contentType=1+rsType=2 / rsType=2 / contentType=43 / else）之后、`$item.on('click')` 之前，与内容渲染完全解耦
- UTC+8 采用 offset 方式（`ts + 8*3600*1000` → `getUTC*`），不依赖宿主环境时区设置，确保跨机器一致性
- 不复用现有 `formatUTCDate`（该函数输出 UTC 日期，非 UTC+8）

### 2.3 架构变更

无架构变更，纯前端 UI 扩展，不涉及接口、存储或模块边界调整。

### 2.4 数据变更

无数据模型变更，复用现有 column/content 接口响应字段。

---

## 3. 关键流程变更

### 3.1 子栏目预览行渲染流程

#### 3.1.1 变更前流程

```
renderSubcolPreview(dataList)
  └─ forEach item
       ├─ [branch A] contentType=1 + rsType=2: 追加 icon + name
       ├─ [branch B] rsType=2: 追加 text value
       ├─ [branch C] contentType=43: 追加 match card
       └─ [branch D] else: 追加 img + name
       └─ 绑定 click 事件
       └─ $strip.append($item)
```

#### 3.1.2 变更后流程

```
renderSubcolPreview(dataList)
  └─ forEach item
       ├─ [branch A/B/C/D] 内容渲染（不变）
       ├─ [NEW] if liveStartTime → 追加 .subcol-preview-time "Start Time: ..."
       ├─ [NEW] if releaseTime > 0 → 追加 .subcol-preview-time "Release Time: ..."
       └─ 绑定 click 事件（不变）
       └─ $strip.append($item)
```

---

## 4. 兼容性与风险分析

### 4.1 兼容性评估

| 兼容性类型 | 影响评估 | 保证措施 |
|------------|----------|----------|
| 字段缺失兼容 | 无影响 | null/undefined 判断保护 |
| 现有卡片布局 | 无影响 | 追加在末尾，不改动现有 DOM 结构 |
| 浏览器兼容 | 无影响 | 使用 Date.getUTC* 系列，无 Intl 依赖 |

### 4.2 风险识别与控制

| 风险类型 | 风险描述 | 影响程度 | 预防措施 |
|----------|----------|----------|----------|
| 时间戳单位 | 若接口返回秒级时间戳，显示时间将偏差 | 低 | 验证时对比接口实际值，必要时乘以 1000 |
| 卡片过窄 | 长时间字符串在窄卡片中换行 | 低 | CSS 设置 `word-break: break-all` |

### 4.3 回滚策略

**回滚触发条件**:
- 时间字段显示为 NaN 或 Invalid Date

**回滚步骤**:
1. 在 `renderSubcolPreview` 函数中注释掉时间字段追加块（4行）
2. 删除 `formatUTC8DateTime` / `formatUTC8Date` 两个函数
3. 删除 `.subcol-preview-time` CSS class

---

## 附录

### C. 变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
|------|------|----------|--------|
| v1.0 | 2026-06-29 | 初始版本 | AI |
