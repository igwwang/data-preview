# 需求分析文档 - 预览行点击直达 Resource Details

**文档版本**: v1.2.0
**创建日期**: 2026-06-19
**文档状态**: 已批准
**目标读者**: 技术团队
**项目类型**: 优化（现有单文件工具交互增强）

---

## 立项/预研确认

| 确认项 | 状态 | 说明 |
|----------|------|------|
| 方向判断 | 已确认 | QA/开发人员在预览条看到感兴趣的 item 后需额外打开 contentModal 才能查看详情，多一步操作；直接跳转可减少交互层级 |
| 技术选型初筛 | 已确认 | 复用现有 `getResourceDetail()` + `renderResourceDetail()` + `#resourceDetailModal` 流程，修改 click handler，无需引入新依赖 |
| 备选方案排除 | 已确认 | 在预览 item 上内联展示详情（排除：信息密度过高，布局复杂）；新建独立页面（排除：破坏现有单文件工作流） |
| 资源可行性 | 已确认 | 仅修改 `renderSubcolPreview()` 内的 click handler，改动范围极小 |
| 干系人共识 | 已确认 | 内部工具，需求方即使用方 |

---

## 执行摘要

面向内部 QA/开发人员，解决预览条中查看 item 详情需经过 contentModal 中转的多步操作问题；直接在预览条 item 上绑定 Resource Details 跳转，支持类型直达详情弹窗，不支持类型统一提示 "No details available"。

---

## 1. 项目概述

### 1.1 业务背景

**现状描述**:
- 预览条（`.subcol-preview-strip`）中点击任意 item，当前行为是打开 contentModal（展示该列全部内容列表）
- 用户若要查看某个具体 item 的 Resource Details，需：点击预览 item → contentModal 弹出 → 在列表中找到对应 card → 点击 card → Resource Details 弹窗，共 4-5 步

**痛点分析**:

| 痛点编号 | 痛点描述 | 影响范围 | 量化影响 | 紧迫程度 |
|----------|----------|----------|----------|----------|
| P1 | 从预览条到 Resource Details 需经过 contentModal 中转，步骤冗余 | QA/开发日常数据核查 | 每次查看详情多 2-3 步操作 | 中 |

**机会识别**:
- 预览条 item 在 `forEach` 闭包内已持有 `rsType` 和 `value`，技术上可直接调用 `getResourceDetail()`，无需额外接口或数据结构变更

### 1.2 项目目标

**技术目标**:

| 目标编号 | 目标描述 | 衡量指标 | 目标值 |
|----------|----------|----------|--------|
| TG1 | 预览条 item 点击直达 Resource Details | 操作步骤数 | 从 4-5 步缩减至 1 步 |
| TG2 | 不影响现有 contentModal 及节点点击流程 | 回归测试 | 主流程零回归 |

### 1.3 项目范围

**范围内（In Scope）**:
- `renderSubcolPreview()` 内 item click handler 改写
- 支持类型（rsType=6/12，objectType=REC_CHANNEL/REC_PROGRAM）：点击直接打开 `#resourceDetailModal`
- 不支持类型（rsType=2/30/31/32，contentType=43 match schedule，其他简单类型）：点击弹 alert "No details available"
- 过渡体验与现有 card click 一致：弹窗立即出现 + loading spinner

**范围外（Out of Scope）**:
- contentModal 流程（不修改）
- 节点名称点击行为（不修改）
- 父节点交互（不涉及）
- 引入任何新 JS/CSS 库

**未来规划（Future Scope）**:
- 可按需为预览 item 增加右键菜单，同时提供"查看详情"和"查看完整列表"两个入口

### 1.4 成功标准

| 维度 | 成功标准 | 衡量方式 |
|------|----------|----------|
| 功能完整性 | 支持类型 item 点击直达 Resource Details | 人工验收 |
| 降级处理 | 不支持类型弹出 "No details available" | 人工验收 |
| 零回归 | 现有 contentModal 及节点点击流程不受影响 | Console 无 JS error，主流程验收 |

### 1.5 技术可行性验证（POC）

| 关键假设 | 验证方法 | 验证结果 | 是否阻塞 |
|----------|----------|----------|----------|
| `item` 对象在 `renderSubcolPreview` forEach 闭包内含 `rsType` 和 `value` | 代码审阅（第 1872-1946 行） | 通过，`dataList.forEach(function(item){...})` 闭包持有完整 item 对象 | 否 |
| `getResourceDetail(rsType, value)` 可直接复用，签名不变 | 代码审阅（第 2022-2052 行） | 通过，函数签名 `(resourceType, value)` 与 card click 调用一致 | 否 |
| `#resourceDetailModal` 及 `showDetailLoading()` / `renderResourceDetail()` 可复用 | 代码审阅（第 2054-2064 行） | 通过，均为全局函数，无上下文依赖 | 否 |

**判定**: 全部通过，继续后续章节。

---

## 2. 目标用户分析

### 2.1 用户画像

#### 用户角色: QA/开发工程师

| 维度 | 描述 |
|------|------|
| 角色定义 | 使用本工具调试/核查 TV 数据接口返回内容的内部技术人员 |
| 用户规模 | 小团队（< 20人） |
| 核心诉求 | 快速查看预览条中某个 item 的完整 Resource Details（海报、描述、deeplinks 等） |
| 使用频率 | 日常（开发/测试周期内高频） |
| 技术水平 | 专业用户 |
| 典型场景 | 扫描预览条，发现某个 item 异常，直接点击查看详情确认 |

---

## 3. 核心场景与用户故事

### 3.1 场景总览

| 场景编号 | 场景名称 | 优先级 | 涉及角色 | 使用频率 | 业务价值 |
|----------|----------|--------|----------|----------|----------|
| SC-001 | 预览条 item 点击直达 Resource Details | P0 | QA/开发工程师 | 高 | 核心 |
| SC-002 | 不支持详情类型的降级提示 | P1 | QA/开发工程师 | 中 | 重要 |

### 3.2 P0 场景详述

#### SC-001: 预览条 item 点击直达 Resource Details

> **用户故事**: 作为 QA 工程师，我想要点击预览条中的某个 item 直接查看其 Resource Details，以便无需经过 contentModal 中转即可快速核查资源详情。

**前置条件**: 页面已完成 token 获取和栏目树渲染，预览条已懒加载完毕

**主流程步骤**:
1. 用户在预览条中点击支持 Resource Details 的 item（rsType=6/12 或 objectType=REC_CHANNEL/REC_PROGRAM）
2. 系统立即弹出 `#resourceDetailModal` 并显示 loading spinner
3. 调用 `getResourceDetail(item.rsType, item.value)` 获取详情数据
4. 数据返回后调用 `renderResourceDetail(data, item.rsType)` 渲染内容
5. 用户查看 Resource Details（海报、名称、描述、deeplinks 等）

**异常流程**:

| 异常编号 | 异常条件 | 系统行为 | 用户提示 |
|----------|----------|----------|----------|
| EX-001 | 接口返回失败 | 捕获异常，关闭弹窗 | alert "Failed to load details: [错误信息]" |
| EX-002 | token 过期（errorCode=1000） | 抛出 Token expired 错误 | alert "Failed to load details: Token expired" |

**验收标准（AC）**:
- [ ] AC1: 点击 rsType=6 的 item，`#resourceDetailModal` 弹出并展示 APP 详情
- [ ] AC2: 点击 rsType=12 的 item，弹窗展示 MOVIE 详情
- [ ] AC3: 点击 objectType=REC_CHANNEL 的 item，弹窗展示频道详情
- [ ] AC4: 点击 objectType=REC_PROGRAM 的 item，弹窗展示节目详情
- [ ] AC5: 弹窗出现时立即显示 loading spinner，数据就绪后替换为详情内容

### 3.3 P1 场景概述

#### SC-002: 不支持详情类型的降级提示

> **用户故事**: 作为 QA 工程师，当我点击不支持 Resource Details 的 item 时，我想要得到明确提示，以便了解该类型无详情可查。

**主流程**: 点击不支持类型 item（rsType=2/30/31/32，contentType=43，或其他简单类型）→ 弹出 alert "No details available"

**验收标准**:
- [ ] 所有不支持类型 item 点击后弹出 alert "No details available"，不打开任何弹窗

---

## 4. 功能需求

### 4.1 功能需求清单

| 需求编号 | 功能模块 | 需求描述 | 优先级 | 关联场景 |
|----------|----------|----------|--------|----------|
| FR-001 | click handler 改写 | 将预览条 item click 从打开 contentModal 改为调用 `getResourceDetail()` | P0 | SC-001 |
| FR-002 | 类型判断 | 根据 rsType 和 objectType 判断是否支持 Resource Details | P0 | SC-001/SC-002 |
| FR-003 | 降级提示 | 不支持类型统一弹 alert "No details available" | P1 | SC-002 |
| FR-004 | 过渡体验 | 点击后立即弹出 `#resourceDetailModal` + loading spinner | P0 | SC-001 |

### 4.2 功能模块划分

- **类型判断逻辑**：
  - 支持：rsType=6 或 rsType=12，以及 value 能解析为 JSON 且 objectType 为 REC_CHANNEL 或 REC_PROGRAM 的 item
  - 不支持：rsType=2/30/31/32，contentType=43（match schedule），其他简单类型
- **click handler**：替换原有 `getColumnContent` 调用，改为 `getResourceDetail` + `renderResourceDetail` 流程
- **降级 alert**：统一提示语 "No details available"

### 4.3 接口需求

| 接口编号 | 对接系统 | 接口类型 | 数据方向 | 备注 |
|----------|----------|----------|----------|------|
| IF-001 | `/sp/api/device/v1/column/resourceDetail` | REST GET | 入（读取资源详情） | 复用现有 `getResourceDetail()` 函数，签名不变 |

---

## 5. 非功能需求

### 5.1 性能需求

| 指标类别 | 场景描述 | 目标值 |
|----------|----------|--------|
| 弹窗响应 | 点击 item 到弹窗出现 | < 100ms（弹窗本身立即出现，loading 期间不阻塞） |
| 详情加载 | 接口响应到内容渲染 | 依赖接口响应，无额外渲染开销 |

### 5.5 兼容性需求

| 兼容维度 | 支持范围 |
|----------|----------|
| 桌面浏览器 | Chrome 80+, Firefox 75+, Edge 80+ |
| 移动端 | iOS Safari 14+, Android Chrome 80+ |
| 依赖 | Bootstrap 5 Modal（已有），jQuery（已有） |

---

## 6. 约束条件

### 6.1 技术约束

| 约束项 | 约束描述 | 是否可协商 |
|--------|----------|------------|
| 单文件 | 所有代码必须在 OS10-prod-QA-latest.html 内实现 | 否 |
| 无新依赖 | 不引入额外 JS/CSS 库 | 否 |
| 行分隔符 | 写入文件时使用 LF（\n），零容忍 CRLF | 否 |

### 6.4 假设与依赖

**假设条件**:
- `getResourceDetail(resourceType, value)` 函数签名不变
- `#resourceDetailModal`、`showDetailLoading()`、`renderResourceDetail()` 均为全局可用
- `globalToken` 在预览条点击时仍然有效

---

## 7. 验收标准与交付定义

### 7.1 交付物清单

| 交付物 | 描述 |
|--------|------|
| OS10-prod-QA-latest.html | 修改 `renderSubcolPreview()` click handler 的完整 HTML 文件 |
| docs/requirements/requirements-analysis-v1.2.0.md | 本文档 |
| docs/plan/development-plan-v1.2.0.md | 开发计划文档 |

### 7.2 验收检查清单

**功能验收**:
- [ ] SC-001 所有 AC（AC1-AC5）通过
- [ ] SC-002 验收标准通过
- [ ] rsType=30/31/32 item 点击弹 "No details available"
- [ ] contentType=43 match schedule item 点击弹 "No details available"
- [ ] 其他简单类型 item 点击弹 "No details available"

**非功能验收**:
- [ ] 现有 contentModal 主流程无回归
- [ ] 节点名称点击弹窗流程无回归
- [ ] Console 无 JS error

---

## 9. 附录

### 9.1 术语表

| 术语 | 定义 |
|------|------|
| Resource Details | 通过 `/column/resourceDetail` 接口获取的资源详情，含海报、描述、deeplinks 等 |
| 预览条 | 叶子节点名称下方的水平滚动缩略图行（`.subcol-preview-strip`） |
| 支持类型 | rsType=6（APP）、rsType=12（MOVIE）及 objectType=REC_CHANNEL/REC_PROGRAM |
| 不支持类型 | rsType=2/30/31/32，contentType=43，以及其他简单类型 |

### 9.2 参考文档

1. 需求分析文档 v1.1.0 - `docs/requirements/requirements-analysis-v1.1.0.md`
2. 迭代设计文档 v1.1.0 - `docs/releases/iteration-design-v1.1.0.md`

### 9.3 变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
|------|------|----------|--------|
| v1.2.0 | 2026-06-19 | 初始版本 | AI |

---

## 质量检查清单

- [x] 立项/预研确认已全部通过
- [x] 技术可行性验证（POC）已完成，关键假设已验证通过
- [x] 所有占位符已替换为具体内容
- [x] 项目目标清晰（内部工具，以功能完整性和零回归为准）
- [x] 范围边界清晰（仅改 click handler，不涉及其他流程）
- [x] P0 场景有完整的主流程和异常流程
- [x] 功能需求可追溯到用户场景
- [x] 约束条件已确认
- [x] 验收标准可测试、可验证
