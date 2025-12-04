# HTML数据比对测试报告

**测试时间:** 2025-12-04 13:56:51
**JDK17版本API:** https://dev-saas-17.zeasn.tv
**JDK8版本API:** https://dev-saas.zeasn.tv

## 测试概述

- **总测试项:** 36
- **通过测试:** 34
- **差异测试:** 2
- **通过率:** 94.4%

## 详细测试结果

| 测试项目 | JDK17数量 | JDK8数量 | 差异 | 状态 |
|---------|-----------|------------|------|------|
| Personalized recommendations 按钮 | 23 | 25 | -2 | ❌ DIFF |
| Banner AD Recommendation 按钮 | 1 | 1 | +0 | ✅ PASS |
| New Personalized recommendations 按钮 | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/Menu | 5 | 5 | +0 | ✅ PASS |
| 树形节点: Home/Netflix二级菜单 | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/Prime Video二级菜单 | 0 | 0 | +0 | ✅ PASS |
| 树形节点: Home/Whale TV+二级菜单 | 0 | 0 | +0 | ✅ PASS |
| 树形节点: Home/Disney+二级菜单 | 5 | 5 | +0 | ✅ PASS |
| 树形节点: Home/Prime Video | 0 | 0 | +0 | ✅ PASS |
| 树形节点: Home/Disney+_topic | 5 | 5 | +0 | ✅ PASS |
| 树形节点: Home/Hot Movies | 29 | 29 | +0 | ✅ PASS |
| 树形节点: Home/Live | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/Action | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/Yango Play | 0 | 0 | +0 | ✅ PASS |
| 树形节点: Apps/Banner | 3 | 3 | +0 | ✅ PASS |
| 树形节点: Apps/Category | 4 | 4 | +0 | ✅ PASS |
| 树形节点: Apps/Recommended | 10 | 10 | +0 | ✅ PASS |
| 树形节点: Apps/Video | 10 | 10 | +0 | ✅ PASS |
| 树形节点: Apps/News | 8 | 8 | +0 | ✅ PASS |
| 树形节点: Discovery/Discovery-Banner | 1 | 1 | +0 | ✅ PASS |
| 树形节点: Discovery/tab | 5 | 5 | +0 | ✅ PASS |
| 树形节点: Feautured/Latest Movies & TV | 40 | 40 | +0 | ✅ PASS |
| 树形节点: Feautured/Latest News | 0 | 10 | -10 | ❌ DIFF |
| 树形节点: Feautured/Latest Trailers | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Movies/Recommended | 17 | 17 | +0 | ✅ PASS |
| 树形节点: Movies/Action | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Movies/WTV+Recommed-test | 30 | 30 | +0 | ✅ PASS |
| 树形节点: TV Shows/Recommended | 30 | 30 | +0 | ✅ PASS |
| 树形节点: TV Shows/Reality | 30 | 30 | +0 | ✅ PASS |
| 树形节点: TV Shows/Family | 50 | 50 | +0 | ✅ PASS |
| 树形节点: Live/Recommended | 15 | 15 | +0 | ✅ PASS |
| 树形节点: Live/Home | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Live/Food | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Video/Recommended | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Video/Gaming | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Video/Learning | 30 | 30 | +0 | ✅ PASS |

## 差异分析

### 按钮功能差异

- **Personalized recommendations 按钮:** JDK17版本比JDK8版本少2个数据项

### 树形节点差异

- **树形节点: Feautured/Latest News:** JDK17版本比JDK8版本少10个数据项

## 统计分析

- **按钮功能测试:** 3 项
- **树形节点测试:** 33 项
- **数据完全一致的项目:** 34 项
- **JDK17数据更多的项目:** 0 项
- **JDK8数据更多的项目:** 2 项
- **JDK8多出数据的平均值:** 6.0

## 结论

⚠️ **发现 2 项差异。** 需要进一步分析差异原因。

**可能的差异原因：**
1. **API版本差异** - JDK17版本可能使用了不同的API逻辑
2. **配置参数差异** - 两个版本的默认配置可能不同
3. **数据源差异** - 可能连接到不同的数据库或缓存
4. **缓存机制差异** - 缓存策略或过期时间不同
5. **算法优化** - 推荐算法或数据筛选逻辑的改进

**建议的后续行动：**
1. 检查两个版本的配置文件差异
2. 对比API响应的详细内容，不仅仅是数量
3. 验证数据源的一致性
4. 检查是否存在时间相关的数据变化
5. 进行多次测试以确认差异的稳定性

---
*报告生成时间: 2025-12-04 13:56:51*
