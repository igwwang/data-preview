# OS10-prod-QA-latest Country→langCode 联动 - 需求分析问卷

> **填写说明**:
>
> - ✅ = 已确认，无需填写
> - ❓ = 待回答，请在 **回答：** 后面填写选项字母或自由描述
> - 填完后告诉我，我会读取并澄清矛盾点

---

## 已确认信息汇总


| 项目         | 确认内容                                                                                                    |
| ------------ | ----------------------------------------------------------------------------------------------------------- |
| 目标文件     | `OS10-prod-QA-latest.html`                                                                                  |
| 功能入口     | Edit Device Configuration 弹窗（`#configModal`）                                                            |
| 触发控件     | `#clientIpSelect` 下拉框（country-IP 列表）                                                                 |
| 联动目标     | `langCode` 文本输入框（`input[name="langCode"]`）                                                           |
| 现有国家列表 | Spain / Portugal / Italy / Brazil / Argentina / Chile / Mexico / Japan / France / Germany / Hong Kong / USA |
| 版本号       | v1.4.0                                                                                                      |

---

## 立项/预研确认

✅ **方向**: 在选择 clientIp 国家时，自动填充对应官方语言码到 langCode 字段，减少手动修改步骤，提高调试效率。

---

## 第1章 langCode 映射规则

### 1.1 语言码格式

❓ **Q1**: langCode 使用哪种格式？

- a) 2字母 ISO 639-1（如 `de`、`fr`、`ja`）
- b) BCP 47 带区域（如 `de-DE`、`fr-FR`、`zh-HK`）
- c) 与现有 `DEFAULT_PARAMS.langCode = 'en'` 保持一致，用现有值中出现的格式

回答：a

### 1.2 多官方语言国家处理

以下国家存在多官方语言，需确认优先选哪一种：

❓ **Q2**: Hong Kong 的 langCode 填什么？

- a) `zh`（中文通用）
- b) `zh-HK`（粤语/繁体香港）
- c) `en`（英文，港英官方语言之一）

回答：b

❓ **Q3**: Brazil 的 langCode 填什么？

- a) `pt`（葡萄牙语通用）
- b) `pt-BR`（巴西葡萄牙语）

回答：b

❓ **Q4**: 西班牙语国家（Spain / Argentina / Chile / Mexico）是否统一用 `es`，还是各自带区域码（`es-ES` / `es-AR` / `es-CL` / `es-MX`）？

- a) 统一用 `es`
- b) 各自带区域码

回答：a

---

## 第2章 触发时机

### 2.1 dropdown 选择触发

✅ **已确认**: 从 `#clientIpSelect` 下拉框选择国家时触发 langCode 自动填充。

### 2.2 手动输入 IP 触发

❓ **Q5**: 当用户在 IP 文本框手动输入一个能匹配 `COUNTRY_IP_LIST` 的 IP 时，是否也联动更新 langCode？

- a) 是，匹配成功即更新 langCode
- b) 否，仅 dropdown 选择触发

回答：b

---

## 第3章 用户覆盖行为

### 3.1 自动填充后用户手动修改

❓ **Q6**: 自动填充 langCode 后，如果用户又手动修改了 langCode 文本框，再次切换 dropdown 时是否覆盖用户的手动输入？

- a) 是，dropdown 选择始终覆盖 langCode
- b) 否，一旦用户手动编辑过，不再覆盖

回答：a

---

## 第4章 Reset 行为

### 4.1 点击 Reset 按钮

✅ **已确认**: Reset 按钮（`#configResetBtn`）当前恢复所有字段为 `DEFAULT_PARAMS`，langCode 也回到默认值 `'en'`，与国家联动无冲突。

---

## 第5章 UI 反馈

❓ **Q7**: 自动填充 langCode 时，是否需要任何视觉提示（如高亮/提示文字"已自动填充"）？

- a) 不需要，静默填充即可
- b) 短暂高亮输入框（如 1s 黄色背景）
- c) 输入框旁显示小提示文字

回答：b

---

## 第6章 约束条件

✅ **不引入新依赖**: 映射表直接硬编码在 HTML 文件 JS 中，无需外部数据源。

✅ **不做什么**: 不修改已保存 localStorage 中的 langCode（仅影响当前弹窗表单填充，保存时和现有逻辑一致）。

---

> 填完后告诉我，我会读取并进行矛盾澄清，最终输出完整的需求分析文档。
