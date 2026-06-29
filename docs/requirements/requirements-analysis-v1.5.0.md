# 需求分析文档 v1.5.0

**文档版本**: v1.0
**创建日期**: 2026-06-29
**文档状态**: 草案
**目标读者**: 技术团队
**项目类型**: 优化

---

## 立项/预研确认

| 确认项 | 状态 | 说明 |
|----------|------|------|
| 方向判断 | 已确认 | QA 在首页子栏目预览行无法直观看到直播开始时间与发布日期，需手动翻 API 响应核对，效率低 |
| 技术选型初筛 | 已确认 | 纯前端 JS 修改，在现有 renderSubcolPreview 函数末尾追加 DOM 节点，无需新依赖 |
| 备选方案排除 | 已确认 | 排除 tooltip 方案（需额外交互，隐藏信息）；选择内联展示更直观 |
| 资源可行性 | 已确认 | 改动范围仅 1 个函数，< 1 小时可完成 |
| 干系人共识 | 已确认 | 需求来源于用户，已明确字段名和格式 |

---

## 执行摘要

面向 QA 用户，在 OS10-prod-QA-latest.html 首页子栏目预览行卡片下方直接展示 `liveStartTime`（直播开始时间）和 `releaseTime`（发布日期），格式化为 UTC+8 可读时间，省去手动查 API 响应的步骤，提升 QA 核对效率。

---

## 1. 项目概述

### 1.1 业务背景

**现状描述**:
- 首页子栏目预览行（subcol preview strip）仅展示缩略图和内容名称
- QA 核对直播时间或发布日期时，需打开 Network 面板手动查找 column/content 接口响应

**痛点分析**:

| 痛点编号 | 痛点描述 | 影响范围 | 紧迫程度 |
|----------|----------|----------|----------|
| P1 | 无法从预览行直接读取直播开始时间 | 直播类内容 QA | 高 |
| P2 | 无法从预览行直接读取内容发布日期 | 点播/电影类内容 QA | 中 |

### 1.2 项目目标

**技术目标**:

| 目标编号 | 目标描述 | 验收标准 |
|----------|----------|----------|
| TG1 | 在预览卡片下方展示 liveStartTime | 格式 `Start Time: YYYY-MM-DD HH:mm:ss`，UTC+8 |
| TG2 | 在预览卡片下方展示 releaseTime | 格式 `Release Time: YYYY-MM-DD`，UTC+8 日期 |

### 1.3 项目范围

**范围内（In Scope）**:
- 修改 `renderSubcolPreview` 函数，在全部分支的 `$item` 末尾追加时间字段
- 新增 `.subcol-preview-time` CSS class

**范围外（Out of Scope）**:
- 主卡片区（`#contentContainer`）的时间显示逻辑——已有实现，不改动
- localStorage 存储逻辑
- 其他 HTML 文件

### 1.4 成功标准

| 维度 | 成功标准 |
|------|----------|
| 功能正确 | 有 liveStartTime 的 item 展示 Start Time，有 releaseTime > 0 的 item 展示 Release Time |
| 格式正确 | liveStartTime → `YYYY-MM-DD HH:mm:ss`（UTC+8）；releaseTime → `YYYY-MM-DD`（UTC+8） |
| 无副作用 | 字段不存在时不展示任何内容，不影响卡片其他元素 |

### 1.5 技术可行性验证（POC）

| 关键假设 | 验证方法 | 验证结果 | 是否阻塞 |
|----------|----------|----------|----------|
| liveStartTime 为毫秒级 Unix 时间戳 | 查看主卡片区现有代码 `new Date(parseInt(item.liveStartTime))` | 通过，与主区用法一致 | 否 |
| releaseTime 为毫秒级 Unix 时间戳且 > 0 判断 | 查看主卡片区 `item.releaseTime > 0` 分支 | 通过 | 否 |
| UTC+8 可通过 `Date` API 实现无需库 | `new Date(ts).toLocaleString('zh-CN', {timeZone:'Asia/Shanghai'})` 标准 API | 通过 | 否 |

**判定**: 全部通过，继续后续章节。

---

## 2. 目标用户分析

| 维度 | 描述 |
|------|------|
| 角色定义 | QA 工程师，使用此工具核对 TV 平台内容数据 |
| 核心诉求 | 快速读取卡片的直播时间和发布日期，无需额外查 API |
| 技术水平 | 专业用户 |

---

## 3. 核心场景与用户故事

### 3.1 场景总览

| 场景编号 | 场景名称 | 优先级 |
|----------|----------|--------|
| SC-001 | 查看直播类卡片的开始时间 | P0 |
| SC-002 | 查看点播/电影卡片的发布日期 | P0 |

### 3.2 P0 场景详述

#### SC-001: 查看直播类卡片的开始时间

> **用户故事**: 作为 QA，我想要在子栏目预览行直接看到直播开始时间，以便快速核对排期是否正确。

**前置条件**: 接口返回的 item 包含 `liveStartTime` 字段（非空、非 null）

**主流程步骤**:
1. 页面加载，`renderSubcolPreview` 渲染预览条
2. 对每个 item 检查 `item.liveStartTime` 是否存在
3. 若存在，将时间戳格式化为 `YYYY-MM-DD HH:mm:ss`（UTC+8）
4. 在卡片 `$item` 末尾追加 `<div class="subcol-preview-time">Start Time: ...</div>`

**异常流程**:

| 异常编号 | 异常条件 | 系统行为 |
|----------|----------|----------|
| EX-001 | liveStartTime 为 null/undefined/空字符串 | 不追加时间元素，静默跳过 |
| EX-002 | liveStartTime 为无效数字（NaN） | 不追加时间元素，静默跳过 |

**验收标准（AC）**:
- [ ] AC1: item.liveStartTime 存在时，卡片下方显示 `Start Time: YYYY-MM-DD HH:mm:ss`（UTC+8）
- [ ] AC2: item.liveStartTime 不存在时，卡片下方无 Start Time 文字
- [ ] AC3: 格式化结果与用户示例 `2026-06-29 14:54:00` 对齐（UTC+8）

#### SC-002: 查看点播/电影卡片的发布日期

> **用户故事**: 作为 QA，我想要在子栏目预览行直接看到内容发布日期，以便核对上线时间是否正确。

**前置条件**: 接口返回的 item 包含 `releaseTime` 且 `> 0`

**主流程步骤**:
1. 对每个 item 检查 `item.releaseTime > 0`
2. 若满足，将时间戳格式化为 `YYYY-MM-DD`（UTC+8 日期部分）
3. 在卡片 `$item` 末尾追加 `<div class="subcol-preview-time">Release Time: ...</div>`

**验收标准（AC）**:
- [ ] AC4: item.releaseTime > 0 时，卡片下方显示 `Release Time: YYYY-MM-DD`（UTC+8）
- [ ] AC5: item.releaseTime 不存在或 <= 0 时，无 Release Time 文字
- [ ] AC6: 格式化结果与用户示例 `2026-06-29` 对齐

---

## 4. 功能需求

### 4.1 功能需求清单

| 需求编号 | 功能模块 | 需求描述 | 优先级 | 关联场景 |
|----------|----------|----------|--------|----------|
| FR-001 | renderSubcolPreview | 检测 item.liveStartTime，存在则追加 Start Time 展示 | P0 | SC-001 |
| FR-002 | renderSubcolPreview | 检测 item.releaseTime > 0，满足则追加 Release Time 展示 | P0 | SC-002 |
| FR-003 | CSS | 新增 .subcol-preview-time class，小字灰色，宽度 100% | P0 | SC-001/002 |
| FR-004 | JS 工具函数 | formatUTC8DateTime(ts) → `YYYY-MM-DD HH:mm:ss` | P0 | SC-001 |
| FR-005 | JS 工具函数 | formatUTC8Date(ts) → `YYYY-MM-DD` | P0 | SC-002 |

### 4.2 功能模块划分

时间展示逻辑统一在 `renderSubcolPreview` 函数末尾追加，与现有四个内容渲染分支完全解耦——先渲染内容主体，再追加时间字段，适用全部分支。

### 4.3 接口需求

- 无新接口，复用现有 column/content 接口返回的 `dataList[].liveStartTime` 和 `dataList[].releaseTime` 字段

---

## 5. 非功能需求

### 5.1 性能需求

- 时间格式化为纯 JS 运算，O(n) 复杂度，n = dataList.length，无性能影响

### 5.5 兼容性需求

| 兼容维度 | 支持范围 |
|----------|----------|
| 浏览器 | 现代浏览器（支持 `Intl.DateTimeFormat` / `toLocaleString` with timeZone） |

---

## 6. 约束条件

### 6.1 技术约束

| 约束项 | 约束描述 |
|--------|----------|
| 不引入新依赖 | 格式化使用原生 JS Date API |
| 不改主卡片区 | 仅修改 renderSubcolPreview，不触碰主卡片区 dataList.forEach |

### 6.4 假设与依赖

**假设条件**:
- `liveStartTime` 和 `releaseTime` 均为毫秒级 Unix 时间戳（若接口返回秒级，需 ×1000）
- 运行环境支持 `Date` API 的 `timeZone: 'Asia/Shanghai'` 选项

---

## 7. 验收标准与交付定义

### 7.1 交付物清单

| 交付物 | 描述 |
|--------|------|
| OS10-prod-QA-latest.html | 修改 renderSubcolPreview 函数及新增 CSS class |

### 7.2 验收检查清单

**功能验收**:
- [ ] AC1: liveStartTime 存在时展示 `Start Time: YYYY-MM-DD HH:mm:ss`（UTC+8）
- [ ] AC2: liveStartTime 不存在时不展示
- [ ] AC3: releaseTime > 0 时展示 `Release Time: YYYY-MM-DD`（UTC+8）
- [ ] AC4: releaseTime 不存在或 <= 0 时不展示
- [ ] AC5: 同一 item 同时有两个字段时，两行均展示
- [ ] AC6: 主卡片区功能无回归

---

## 9. 附录

### 9.3 变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
|------|------|----------|--------|
| v1.0 | 2026-06-29 | 初始版本 | AI |

---

## 质量检查清单

- [x] 立项/预研确认已全部通过
- [x] 技术可行性验证（POC）已完成，关键假设已验证通过
- [x] 所有占位符已替换为具体内容
- [x] 项目范围边界清晰（In/Out Scope 明确）
- [x] P0 场景有完整的主流程和异常流程
- [x] 功能需求可追溯到用户场景
- [x] 验收标准可测试、可验证
