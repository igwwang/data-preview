# OS10-prod-QA-latest v1.4.0 迭代设计

**文档版本**: v1.0
**创建日期**: 2026-06-22
**文档状态**: 已批准
**迭代版本**: v1.4.0
**迭代类型**: 功能增加
**目标读者**: 技术团队

## 执行摘要

在 Edit Device Configuration 弹窗中，选择 clientIp 国家时自动联动填充 langCode，消除每次切换国家后的手动修改步骤，提升调试效率。

---

## 1. 迭代背景与目标

### 1.1 迭代驱动因素

**业务驱动**:
- 调试时切换国家 IP 后，langCode 不会自动更新，需额外手动修改

### 1.2 现状分析

**当前系统状态**:
- clientIp dropdown 选择：触发 IP 文本框更新（现有）
- langCode 联动：无，需手动编辑

**存在问题**:
- P1：切换国家每次需两步操作，重复劳动，低效

### 1.3 迭代目标

**主要目标**:
1. clientIp dropdown 变更时自动填充 langCode（12国全覆盖）
2. 填充后提供 1s 黄色高亮视觉反馈

**成功标准**:
- 12个国家映射全部正确（AC1）
- 黄色高亮约 1s 后恢复（AC2）
- 空选项不触发填充（AC3）
- Save & Reload 后 langCode 值与填充值一致（AC4）
- 手动 IP 输入不联动（AC5）
- 其他字段无回归（AC6）

---

## 2. 变更设计

### 2.1 变更范围

**涉及组件**:
- `OS10-prod-QA-latest.html` — JS 新增 `COUNTRY_LANG_MAP` 常量（新增）
- `OS10-prod-QA-latest.html` — `$('#clientIpSelect').on('change')` handler 追加联动逻辑（修改）

**不涉及组件**:
- `#configSaveBtn` 保存逻辑（不变）
- `#configResetBtn` 重置逻辑（不变）
- 手动 IP 输入同步逻辑（不变）
- 所有其他 HTML/CSS/API 调用（不变）

### 2.2 技术方案

#### 2.2.1 功能设计

**新增功能**:

1. `COUNTRY_LANG_MAP` 常量对象（紧跟 `COUNTRY_IP_LIST` 定义之后）：

```js
const COUNTRY_LANG_MAP = {
    '94.127.167.255':  'es',
    '79.168.0.0':      'pt',
    '151.95.219.6':    'it',
    '187.16.202.172':  'pt-BR',
    '1.178.48.0':      'es',
    '38.7.221.172':    'es',
    '148.233.239.0':   'es',
    '221.86.134.130':  'ja',
    '45.154.138.26':   'fr',
    '45.86.202.30':    'de',
    '122.10.101.131':  'zh-HK',
    '8.34.210.0':      'en'
};
```

**修改功能**:

2. 在 `$('#clientIpSelect').on('change')` handler 中，在现有 IP 同步逻辑之后追加联动逻辑：

```js
$('#clientIpSelect').on('change', function() {
    const selectedIp = $(this).val();
    if (selectedIp) {
        $('input[name="clientIp"]').val(selectedIp);
        // --- 新增：联动更新 langCode ---
        const lang = COUNTRY_LANG_MAP[selectedIp];
        if (lang) {
            const $langInput = $('input[name="langCode"]');
            $langInput.val(lang);
            $langInput.css('background-color', '#fff3cd');
            setTimeout(() => $langInput.css('background-color', ''), 1000);
        }
        // --- 新增结束 ---
    }
});
```

**接口变更**: 无

---

## 3. 关键流程变更

### 3.1 切换国家时的配置更新流程

#### 3.1.1 变更前流程

```
用户选择 dropdown → clientIp 文本框更新
                 → langCode 文本框不变（需手动修改）
                 → 点击 Save & Reload
```

#### 3.1.2 变更后流程

```
用户选择 dropdown → clientIp 文本框更新
                 → 查询 COUNTRY_LANG_MAP
                 → langCode 文本框自动更新 + 1s 黄色高亮
                 → 点击 Save & Reload
```

#### 3.1.3 改进效果

- 操作步骤：切换国家从 2 步缩减为 1 步
- 视觉确认：黄色高亮明确告知 langCode 已被自动更新

---

## 4. 兼容性与风险分析

### 4.1 兼容性评估

| 兼容性类型 | 影响评估 | 保证措施 |
| ---------- | -------- | -------- |
| 现有保存流程 | 无影响 | `.val()` 写入后 serializeArray 可正确读取 |
| 现有重置逻辑 | 无影响 | Reset 恢复 DEFAULT_PARAMS，覆盖联动填充值 |
| 手动 IP 输入 | 无影响 | `input` 事件 handler 未修改 |
| localStorage | 无影响 | 联动只改 DOM，保存路径不变 |

### 4.2 风险识别与控制

| 风险类型 | 风险描述 | 影响程度 | 预防措施 |
| -------- | -------- | -------- | -------- |
| 映射缺失 | COUNTRY_LANG_MAP 中找不到选中 IP | 低 | `if (lang)` 守卫，未映射时不修改 langCode |
| 高亮残留 | setTimeout 在弹窗关闭前未执行 | 低 | setTimeout 为 1000ms，弹窗关闭时 DOM 销毁，无影响 |

### 4.3 回滚策略

**回滚触发条件**:
- Console 出现 JS error
- Save & Reload 后 langCode 值异常

**回滚步骤**:
1. 删除 `COUNTRY_LANG_MAP` 常量定义
2. 删除 `$('#clientIpSelect').on('change')` 中"新增"标注的代码块
3. 验证 AC5/AC6 通过

---

## 附录

### A. 相关文档

- 需求分析：`docs/requirements/requirements-analysis-v1.4.0.md`
- 开发计划：`docs/plan/development-plan-v1.4.0.md`

### C. 变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
| ---- | ---- | -------- | ------ |
| v1.0 | 2026-06-22 | 初始版本 | AI |
