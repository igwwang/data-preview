# HTML数据比对测试报告

**测试时间:** 2025-12-19 17:31:32
**JDK17版本API:** https://acc-saas-17.zeasn.tv
**JDK8版本API:** https://acc-saas.zeasn.tv

## 测试概述

- **总测试项:** 47
- **通过测试:** 36
- **差异测试:** 11
- **通过率:** 76.6%

## 详细测试结果

| 测试项目 | JDK17数量 | JDK8数量 | 差异 | 状态 |
|---------|-----------|------------|------|------|
| Personalized recommendations 按钮 | 30 | 30 | +0 | ✅ PASS |
| Banner AD Recommendation 按钮 | 1 | 1 | +0 | ✅ PASS |
| New Personalized recommendations 按钮 | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/Banner | 5 | 5 | +0 | ✅ PASS |
| 树形节点: Home/Menu | 8 | 8 | +0 | ✅ PASS |
| 树形节点: Home/Netflix 二级推荐 | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/Prime Video 二级推荐 | 10 | 10 | +0 | ✅ PASS |
| 树形节点: Home/Whale TV+二级推荐 | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/Disney+二级推荐 | 2 | 2 | +0 | ✅ PASS |
| 树形节点: Home/YouTube | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/Prime Video | 4 | 4 | +0 | ✅ PASS |
| 树形节点: Home/Disney Plus | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/Hot Movies | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/Live | 30 | 0 | +30 | ❌ DIFF |
| 树形节点: Home/Action | 30 | 0 | +30 | ❌ DIFF |
| 树形节点: Home/Action | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/HH | 10 | 10 | +0 | ✅ PASS |
| 树形节点: Home/Game App | 7 | 0 | +7 | ❌ DIFF |
| 树形节点: Apps/Banner | 1 | 0 | +1 | ❌ DIFF |
| 树形节点: Apps/Category | 7 | 0 | +7 | ❌ DIFF |
| 树形节点: Apps/Recommended | 20 | 20 | +0 | ✅ PASS |
| 树形节点: Apps/Video | 7 | 7 | +0 | ✅ PASS |
| 树形节点: Apps/News | 2 | 0 | +2 | ❌ DIFF |
| 树形节点: Apps/Apps | 10 | 0 | +10 | ❌ DIFF |
| 树形节点: Discovery/tab | 5 | 5 | +0 | ✅ PASS |
| 树形节点: Feautured/Latest Movies & TV | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Feautured/Latest News | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Feautured/Latest Trailers | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Movies/Recommended | 15 | 15 | +0 | ✅ PASS |
| 树形节点: Movies/Action | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Movies/test | 30 | 30 | +0 | ✅ PASS |
| 树形节点: TV Shows/Recommended | 30 | 30 | +0 | ✅ PASS |
| 树形节点: TV Shows/Reality | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Live/Recommended | 29 | 30 | -1 | ❌ DIFF |
| 树形节点: Live/Food | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Live/News | 0 | 0 | +0 | ✅ PASS |
| 树形节点: Video/Recommended | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Video/Gaming | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Video/Learning | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Free TV/Hero Banner | 5 | 5 | +0 | ✅ PASS |
| 树形节点: Free TV/Live Now | 15 | 15 | +0 | ✅ PASS |
| 树形节点: Free TV/Program Guide | 1 | 1 | +0 | ✅ PASS |
| 树形节点: Free TV/Recommended Channels | 0 | 11 | -11 | ❌ DIFF |
| 树形节点: Free TV/Trending Free Movies | 73 | 73 | +0 | ✅ PASS |
| 树形节点: Free TV/Free TV Apps | 0 | 0 | +0 | ✅ PASS |
| 树形节点: Free TV/Trending Movie Test | 0 | 12 | -12 | ❌ DIFF |
| 树形节点: Free TV/rlaxxtv channels | 0 | 10 | -10 | ❌ DIFF |

## 差异分析

### 按钮功能差异


### 树形节点差异

- **树形节点: Home/Live:** JDK17版本比JDK8版本多30个数据项
- **树形节点: Home/Action:** JDK17版本比JDK8版本多30个数据项
- **树形节点: Home/Game App:** JDK17版本比JDK8版本多7个数据项
- **树形节点: Apps/Banner:** JDK17版本比JDK8版本多1个数据项
- **树形节点: Apps/Category:** JDK17版本比JDK8版本多7个数据项
- **树形节点: Apps/News:** JDK17版本比JDK8版本多2个数据项
- **树形节点: Apps/Apps:** JDK17版本比JDK8版本多10个数据项
- **树形节点: Live/Recommended:** JDK17版本比JDK8版本少1个数据项
- **树形节点: Free TV/Recommended Channels:** JDK17版本比JDK8版本少11个数据项
- **树形节点: Free TV/Trending Movie Test:** JDK17版本比JDK8版本少12个数据项
- **树形节点: Free TV/rlaxxtv channels:** JDK17版本比JDK8版本少10个数据项

## 统计分析

- **按钮功能测试:** 3 项
- **树形节点测试:** 44 项
- **数据完全一致的项目:** 36 项
- **JDK17数据更多的项目:** 7 项
- **JDK8数据更多的项目:** 4 项
- **JDK17多出数据的平均值:** 12.4
- **JDK8多出数据的平均值:** 8.5

## 结论

⚠️ **发现 11 项差异。** 需要进一步分析差异原因。

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
*报告生成时间: 2025-12-19 17:31:32*
