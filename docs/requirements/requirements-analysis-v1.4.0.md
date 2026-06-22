# OS10-prod-QA-latest Country→langCode 联动 - 需求分析

**文档版本**: v1.0
**创建日期**: 2026-06-22
**文档状态**: 已批准
**目标读者**: 技术团队
**项目类型**: 优化

---

## 立项/预研确认

| 确认项 | 状态 | 说明 |
| -------- | ------ | ---- |
| 方向判断 | 已确认 | 调试时频繁手动修改 langCode 以匹配国家，联动可消除重复操作 |
| 技术选型初筛 | 已确认 | 纯前端 JS：在现有 `$('#clientIpSelect').on('change')` handler 内追加联动逻辑，无需后端 |
| 备选方案排除 | 已确认 | 无需动态获取语言码，硬编码映射表足够（国家列表固定为12条） |
| 资源可行性 | 已确认 | 单文件单函数改动，改动量极小 |
| 干系人共识 | 已确认 | 内部工具，无外部干系人 |

---

## 执行摘要

面向开发/QA调试人员，解决在 Edit Device Configuration 弹窗中切换国家 IP 后仍需手动修改 langCode 的重复操作问题。在 clientIp dropdown 的 change 事件中自动填充对应官方语言码，并通过短暂高亮给用户视觉反馈，节省调试时每次切换国家的操作步骤。

---

## 1. 项目概述

### 1.1 业务背景

**现状描述**:
- `OS10-prod-QA-latest.html` 提供 Edit Device Configuration 弹窗，用于覆盖 API 请求参数（clientIp / langCode / countryCode 等）
- 当前选择 clientIp（国家）后，langCode 不会自动变化，需要用户手动修改

**痛点分析**:

| 痛点编号 | 痛点描述 | 影响范围 | 紧迫程度 |
| -------- | -------- | -------- | -------- |
| P1 | 切换国家后需手动改 langCode，每次2步操作变1步 | 所有使用该页面的调试人员 | 中 |

### 1.2 项目目标

**技术目标**:

| 目标编号 | 目标描述 | 衡量指标 |
| -------- | -------- | -------- |
| TG1 | clientIp dropdown 变更时自动填充 langCode | 选择12个国家均能正确填充对应语言码 |
| TG2 | 填充后有视觉反馈 | langCode 输入框出现 1s 黄色高亮 |

### 1.3 项目范围

**范围内（In Scope）**:
- `#clientIpSelect` dropdown 选择时联动更新 `input[name="langCode"]`
- 12个国家→语言码硬编码映射表
- langCode 输入框 1s 黄色高亮反馈

**范围外（Out of Scope）**:
- 手动输入 IP 时不触发联动（保持现有行为）
- 不修改 countryCode 字段
- 不引入新依赖

### 1.4 成功标准

| 维度 | 成功标准 |
| ---- | -------- |
| 功能正确性 | 12个国家全部映射正确，无遗漏 |
| 用户体验 | 选国家后 langCode 立即更新，高亮 1s 消失 |
| 无回归 | Save & Reload 后 langCode 值正确写入 localStorage |

### 1.5 技术可行性验证（POC）

| 关键假设 | 验证方法 | 验证结果 | 是否阻塞 |
| -------- | -------- | -------- | -------- |
| `input[name="langCode"]` 在 dropdown change 时已存在于 DOM | 检查 configBtn click handler 渲染顺序 | 通过：langCode 字段在 CONFIG_KEYS.forEach 中与其他字段同批渲染，change handler 绑定时 DOM 已就绪 | 否 |
| jQuery `.val()` 可正确触发值变更 | 代码审查 | 通过：serializeArray 直接读取 input value，不依赖 change 事件，`.val()` 写入足够 | 否 |

---

## 2. 目标用户分析

### 2.1 用户画像

| 维度 | 描述 |
| ---- | ---- |
| 角色定义 | 使用该 HTML 调试页的开发/QA工程师 |
| 核心诉求 | 快速切换国家配置，减少手动操作 |
| 技术水平 | 专业用户 |
| 典型场景 | 切换国家验证不同区域内容推荐结果 |

---

## 3. 核心场景与用户故事

### 3.1 场景总览

| 场景编号 | 场景名称 | 优先级 | 使用频率 |
| -------- | -------- | ------ | -------- |
| SC-001 | 切换国家自动填充 langCode | P0 | 高 |

### 3.2 P0 场景详述

#### SC-001: 切换国家自动填充 langCode

> **用户故事**: 作为调试工程师，我想要选择国家 IP 时自动更新 langCode，以便减少手动修改步骤。

**前置条件**: Edit Device Configuration 弹窗已打开

**主流程步骤**:
1. 用户点击 `#clientIpSelect` 选择某个国家（如 Germany）
2. 系统从映射表查找对应语言码（`de`）
3. 将 `input[name="langCode"]` 的值更新为 `de`
4. langCode 输入框出现 1s 黄色高亮后恢复
5. 用户点击 Save & Reload，langCode `de` 随其他字段一起存入 localStorage

**异常流程**:

| 异常编号 | 异常条件 | 系统行为 |
| -------- | -------- | -------- |
| EX-001 | dropdown 选回 "-- Select Country --"（空值）| 不更新 langCode，保持当前值 |

**验收标准（AC）**:
- [ ] AC1: 选择任意12个国家，langCode 均填充为正确语言码（见映射表）
- [ ] AC2: 切换后 langCode 输入框出现黄色高亮，约 1s 后恢复原样
- [ ] AC3: 选择空选项时 langCode 不变
- [ ] AC4: 点击 Save & Reload 后，langCode 值与切换后的值一致
- [ ] AC5: 手动在 IP 文本框输入 IP，langCode 不联动
- [ ] AC6: 其他字段（countryCode、mac 等）不受影响

---

## 4. 功能需求

### 4.1 功能需求清单

| 需求编号 | 功能模块 | 需求描述 | 优先级 | 关联场景 |
| -------- | -------- | -------- | ------ | -------- |
| FR-001 | configModal JS | 在 `$('#clientIpSelect').on('change')` handler 中，根据选中国家查映射表并更新 `input[name="langCode"]` | P0 | SC-001 |
| FR-002 | configModal JS | 新增 `COUNTRY_LANG_MAP` 硬编码映射对象（12条） | P0 | SC-001 |
| FR-003 | configModal CSS/JS | 更新 langCode 输入框后施加 1s 黄色高亮动画 | P1 | SC-001 |

### 4.2 Country→langCode 映射表

| 国家 | IP | langCode |
| ---- | -- | -------- |
| Spain | 94.127.167.255 | es |
| Portugal | 79.168.0.0 | pt |
| Italy | 151.95.219.6 | it |
| Brazil | 187.16.202.172 | pt-BR |
| Argentina | 1.178.48.0 | es |
| Chile | 38.7.221.172 | es |
| Mexico | 148.233.239.0 | es |
| Japan | 221.86.134.130 | ja |
| France | 45.154.138.26 | fr |
| Germany | 45.86.202.30 | de |
| Hong Kong | 122.10.101.131 | zh-HK |
| USA | 8.34.210.0 | en |

---

## 5. 非功能需求

### 5.1 性能需求

映射表查找为 O(1) 对象属性访问，无性能影响。

### 5.5 兼容性需求

| 兼容维度 | 支持范围 |
| -------- | -------- |
| 浏览器 | 与现有页面一致（Chrome/Firefox/Edge 现代版本） |
| 依赖 | jQuery（已有）、Bootstrap（已有），不新增 |

---

## 6. 约束条件

### 6.1 技术约束

| 约束项 | 约束描述 |
| ------ | -------- |
| 单文件修改 | 所有改动集中在 `OS10-prod-QA-latest.html` |
| 无新依赖 | 不引入任何外部 JS/CSS 库 |
| 行分隔符 | 写入前确保 LF，零容忍 CRLF |

### 6.4 假设与依赖

**假设条件**:
- COUNTRY_IP_LIST 中国家顺序与 IP 不会频繁变动；若新增国家需同步更新 COUNTRY_LANG_MAP

---

## 7. 验收标准与交付定义

### 7.1 交付物清单

| 交付物 | 描述 |
| ------ | ---- |
| OS10-prod-QA-latest.html | 新增 COUNTRY_LANG_MAP 和联动逻辑 |

### 7.2 验收检查清单

**功能验收**:
- [ ] AC1-AC6 全部通过
- [ ] 空选项异常流程符合预期

**非功能验收**:
- [ ] Console 无 JS error
- [ ] 其他配置字段无回归

---

## 9. 附录

### 9.1 术语表

| 术语 | 定义 |
| ---- | ---- |
| langCode | API 请求参数，标识内容语言，格式以 ISO 639-1 为主（zh-HK / pt-BR 为区域化例外） |
| clientIp | 模拟的客户端 IP，用于测试不同地区的内容推荐结果 |
| COUNTRY_LANG_MAP | 新增 JS 对象，key 为国家 IP，value 为对应语言码 |

### 9.3 变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
| ---- | ---- | -------- | ------ |
| v1.0 | 2026-06-22 | 初始版本 | AI |
