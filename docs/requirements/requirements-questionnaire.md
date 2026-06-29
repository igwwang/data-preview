# OS10-prod-QA-latest 首页子栏目预览行时间字段展示 - 需求分析问卷

> **填写说明**:
>
> - ✅ = 已确认，无需填写
> - ❓ = 待回答，请在 **回答：** 后面填写选项字母或自由描述
> - 填完后告诉我，我会读取并澄清矛盾点

---

## 已确认信息汇总


| 项目     | 确认内容                                                                |
| -------- | ----------------------------------------------------------------------- |
| 目标文件 | `OS10-prod-QA-latest.html`                                              |
| 目标函数 | `renderSubcolPreview($wrapper, dataList, columnId, contentType)`        |
| 数据来源 | column/content 接口返回的`dataList` 数组中的 item                       |
| 展示位置 | 每个卡片（`.subcol-preview-item`）下方                                  |
| 字段1    | `liveStartTime` → 格式 `2026-06-29 14:54:00`，展示为 `Start Time: ...` |
| 字段2    | `release` 相关字段 → 格式 `2026-06-29`，展示为 `Release Time: ...`     |
| 版本号   | v1.5.0                                                                  |

---

## 立项/预研确认

✅ **方向**: 在首页子栏目预览行（subcol preview strip）的卡片下方，新增 `liveStartTime` 和 release 日期字段的格式化展示，便于 QA 快速核对直播/上线时间。

---

## 第1章 字段名称确认

### 1.1 release 字段

❓ **Q1**: release 日期对应的 item 字段名是哪个？

- a) `item.release`（纯日期字符串，如 `"2026-06-29"` 或时间戳）
- b) `item.releaseTime`（Unix 时间戳，与主卡片区用法一致：`item.releaseTime > 0`）

回答：b

---

## 第2章 liveStartTime 数据格式

### 2.1 时间戳类型

✅ **现有代码参考**: 主卡片区使用 `new Date(parseInt(item.liveStartTime)).toLocaleString()` 处理 `liveStartTime`，推断为毫秒级 Unix 时间戳。

❓ **Q2**: 格式化 `liveStartTime` 时，时区使用哪种？

- a) 本地时区（`new Date(ts)` 直接格式化，与设备时区一致）
- b) UTC 时间（保持与 Release Time(UTC) 标签一致的风格）

回答：UTC+8

---

## 第3章 展示分支范围

### 3.1 适用的内容类型

`renderSubcolPreview` 内部有四个展示分支，需确认哪些分支需要追加时间字段：

❓ **Q3**: 以下哪些分支需要显示时间字段？

- a) 仅默认（`else`）分支——普通内容（缩略图+名称），即 rsType≠2 且 contentType≠43
- b) 默认分支 + contentType=1 && rsType=2 分支
- c) 全部分支（包括 rsType=2 纯文本和 contentType=43 赛程卡）

回答：只要接口有返回liveStartTime或release，就需要追加时间字段

---

## 第4章 视觉样式

### 4.1 展示样式

❓ **Q4**: 时间字段的展示样式？

- a) 小字灰色文本（与现有 `.subcol-preview-name` 保持类似字号，添加新 class `subcol-preview-time`）
- b) 直接复用现有样式，无需新增 class

回答：a

---

## 第5章 约束条件

✅ **不引入新依赖**: 格式化逻辑直接在 JS 中实现，无需外部库。

✅ **不改变主卡片区逻辑**: 仅修改 `renderSubcolPreview` 函数内部，不影响其他展示区域。

---

> 填完后告诉我，我会读取并进行矛盾澄清，最终输出完整的需求分析文档。
