# OS10-prod-QA-latest 预览行点击直达 Resource Details - 需求分析问卷

> **填写说明**:
>
> - ✅ = 已确认，无需填写
> - ❓ = 待回答，请在 **回答：** 后面填写选项字母或自由描述
> - 填完后告诉我，我会读取并澄清矛盾点

---

## 已确认信息汇总


| 项目             | 确认内容                                                                             |
| ---------------- | ------------------------------------------------------------------------------------ |
| 目标文件         | OS10-prod-QA-latest.html                                                             |
| 触发位置         | 预览条（`.subcol-preview-strip`）中的每个 item                                       |
| 目标行为         | 点击 item 直接打开 Resource Details 弹窗（`#resourceDetailModal`）                   |
| 现有逻辑         | 点击 item 当前打开 contentModal（展示该列全部内容）                                  |
| 技术可行性       | `item` 在 `forEach` 闭包内已含 `rsType` 和 `value`，可直接传给 `getResourceDetail()` |
| 不支持详情的类型 | `rsType` 31/32/30/2，以及 contentType=43（match schedule）                           |
| 版本号           | v1.2.0                                                                               |

---

## 立项/预研确认

✅ **方向确认**: 修改现有预览条 item 的 click handler，复用已有的 `getResourceDetail()` + `renderResourceDetail()` + `#resourceDetailModal` 流程，无需引入新依赖。

---

## 第1章 项目概述

### 1.1 适用范围

✅ **目标**: 预览条（subcol-preview-strip）中每个可渲染的 item，点击后直接进入 Resource Details，跳过现有的 contentModal 中转步骤。

---

## 第3章 核心场景

✅ **核心场景**: QA 人员在预览条中看到某个感兴趣的内容项，直接点击即可查看该资源的详细信息（海报、描述、deeplinks 等），无需先打开 contentModal 再找到该 item 再点卡片。

---

## 第4章 功能需求

### 4.1 不支持 Resource Details 的 item 的降级行为

❓ **Q1**: 对于不支持 Resource Details 的 item（rsType=2/30/31/32 及 match schedule），点击后的行为？

- a) 什么都不做（静默，无反馈）
- b) 回退打开 contentModal（保持原有行为）
- c) 弹出提示 "No details available for this item"

回答：c

### 4.2 rsType=6 / rsType=12 以外的普通类型

当前 card click 逻辑对非 6/12 且 objectType 非 REC_CHANNEL/REC_PROGRAM 的 item 会弹 alert "For simple types, no further information is needed."

❓ **Q2**: 预览条 item 点击遇到此类"简单类型"时的行为，与 Q1 保持一致，还是单独处理？

- a) 与 Q1 保持一致（统一降级策略）
- b) 同现有 card click 逻辑，弹 alert 提示

回答：a

### 4.3 contentType=1 + rsType=2（文本类型）

此类 item 的 value 是内容本身（非 JSON），无法调用 getResourceDetail。

❓ **Q3**: 此类 item 是否需要可点击？

- a) 不可点击，cursor 保持默认，无任何反馈
- b) 点击后回退打开 contentModal

回答：弹 alert "For simple types, no further information is needed."

### 4.4 加载过渡体验

❓ **Q4**: 点击 item 到 Resource Details 弹窗出现前，是否需要视觉反馈？

- a) 与现有 card click 一致：弹窗立即出现并显示 loading spinner
- b) item 本身显示 loading 状态（如半透明 + spinner），弹窗数据就绪后再出现

回答：a

---

## 第7章 验收标准

✅ **基础验收**:

- 支持 Resource Details 的 item（rsType=6/12，objectType=REC_CHANNEL/REC_PROGRAM）点击后直接打开 `#resourceDetailModal`
- 不支持的 item 按 Q1/Q2/Q3 答案处理
- 不影响现有父节点展开/折叠及 contentModal 主流程

---

> 填完后告诉我，我会读取并进行矛盾澄清，最终输出完整的需求分析文档。
