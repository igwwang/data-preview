# localStorage 配置存储设计方案

## 需求背景

页面配置参数 `GLOBAL_PARAMS` 需要持久化存储，且要求：
- 不同页面文件拥有独立配置（如 `OS10-prod-QA.html` 和 `OS10-prod-DE.html`）
- 同一文件在不同环境（本地/线上）共享配置

## 页面地址示例

```
本地环境：
- file:///D:/projects/data-preview/OS10-prod-QA.html
- file:///D:/projects/data-preview/OS10-prod-DE.html

线上环境：
- https://igwwang.github.io/data-preview/OS10-prod-QA.html
- https://igwwang.github.io/data-preview/OS10-prod-DE.html
```

## 方案对比

### 方案1：全局共享（原始方案）❌

```javascript
localStorage.setItem('GLOBAL_PARAMS', JSON.stringify(GLOBAL_PARAMS));
```

**问题**：同一域名下所有页面共享同一份配置，无法区分不同页面。

---

### 方案2：路径+文件名 ❌

```javascript
const PAGE_STORAGE_KEY = `GLOBAL_PARAMS_${location.pathname}`;
```

**存储键示例**：
- 本地：`GLOBAL_PARAMS_/D:/projects/data-preview/OS10-prod-QA.html`
- 线上：`GLOBAL_PARAMS_/data-preview/OS10-prod-QA.html`

**问题**：同一文件在本地和线上会产生不同的存储键，配置无法共享。

---

### 方案3：仅文件名 ✅（最终方案）

```javascript
const PAGE_STORAGE_KEY = `GLOBAL_PARAMS_${location.pathname.split('/').pop()}`;
```

**存储键示例**：
- `OS10-prod-QA.html` → `GLOBAL_PARAMS_OS10-prod-QA.html`
- `OS10-prod-DE.html` → `GLOBAL_PARAMS_OS10-prod-DE.html`

**优势**：
- ✅ 不同文件独立配置
- ✅ 同一文件跨环境共享配置
- ✅ 简洁明了

---

### 方案4：域名+文件名（可选扩展）

```javascript
const PAGE_STORAGE_KEY = `GLOBAL_PARAMS_${location.host}_${location.pathname.split('/').pop()}`;
```

**存储键示例**：
- 本地：`GLOBAL_PARAMS__OS10-prod-QA.html`（host 为空）
- 线上：`GLOBAL_PARAMS_igwwang.github.io_OS10-prod-QA.html`

**适用场景**：需要本地和线上配置也隔离时使用。

## 最终实现代码

```javascript
// Configuration Modal Logic
const CONFIG_KEYS = Object.keys(DEFAULT_PARAMS);
// 获取当前页面文件名作为存储键
const PAGE_STORAGE_KEY = `GLOBAL_PARAMS_${location.pathname.split('/').pop()}`;

// 保存配置
$('#configSaveBtn').click(function() {
    const formArr = $('#configForm').serializeArray();
    formArr.forEach(({name, value}) => {
        GLOBAL_PARAMS[name] = value;
    });
    // 按文件名存储到localStorage
    localStorage.setItem(PAGE_STORAGE_KEY, JSON.stringify(GLOBAL_PARAMS));
    location.reload();
});

// 重置配置
$('#configResetBtn').click(function() {
    Object.assign(GLOBAL_PARAMS, DEFAULT_PARAMS);
    $('#configForm input').each(function() {
        const key = $(this).attr('name');
        if (key in DEFAULT_PARAMS) $(this).val(DEFAULT_PARAMS[key]);
    });
    // 清除当前页面的localStorage
    localStorage.removeItem(PAGE_STORAGE_KEY);
});

// 页面加载时恢复配置
(function restoreConfig() {
    const saved = localStorage.getItem(PAGE_STORAGE_KEY);
    if (saved) {
        try {
            const obj = JSON.parse(saved);
            Object.assign(GLOBAL_PARAMS, obj);
        } catch(e) {}
    }
})();
```

## 使用效果

| 页面文件 | 存储键 | 配置隔离 |
|---------|--------|---------|
| OS10-prod-QA.html | `GLOBAL_PARAMS_OS10-prod-QA.html` | ✅ 独立 |
| OS10-prod-DE.html | `GLOBAL_PARAMS_OS10-prod-DE.html` | ✅ 独立 |
| 本地 vs 线上 | 相同存储键 | ✅ 共享 |

## 总结

采用**方案3（仅文件名）**作为最终方案，实现了：
1. 不同页面配置独立管理
2. 同一页面跨环境配置共享
3. 代码简洁易维护

---

**文档版本**：v1.0  
**更新日期**：2025-01-XX  
**作者**：igwwang
