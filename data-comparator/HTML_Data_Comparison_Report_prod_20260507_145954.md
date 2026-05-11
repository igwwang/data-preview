# PROD环境HTML数据比对测试报告

**测试环境:** PROD
**测试时间:** 2026-05-07 14:59:54
**JDK17版本API:** https://saas-17.zeasn.tv
**JDK8版本API:** https://saas.zeasn.tv

## 测试概述

- **总测试项:** 44
- **通过测试:** 15
- **差异测试:** 29
- **通过率:** 34.1%

## 详细测试结果

| 测试项目 | JDK17数量 | JDK8数量 | 差异 | 状态 |
|---------|-----------|------------|------|------|
| Personalized recommendations 按钮 | 0 | 8 | -8 | ❌ DIFF |
| Banner AD Recommendation 按钮 | 1 | 1 | +0 | ✅ PASS |
| New Personalized recommendations 按钮 | 30 | 30 | +0 | ✅ PASS |
| 树形节点: Home/Banner | 5 | 5 | +0 | ✅ PASS |
| 树形节点: Home/Menu | 13 | 13 | +0 | ✅ PASS |
| 树形节点: Home/Prime Video 二级推荐 | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Home/Whale TV+二级推荐 | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Home/Prime Video | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Home/Hot Movies | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Home/Lives | 0 | 0 | +0 | ✅ PASS |
| 树形节点: Home/Dazn二级推荐 | 0 | 20 | -20 | ❌ DIFF |
| 树形节点: Discovery/tab | 4 | 4 | +0 | ✅ PASS |
| 树形节点: Apps/Banner | 3 | 3 | +0 | ✅ PASS |
| 树形节点: Apps/Category | 8 | 8 | +0 | ✅ PASS |
| 树形节点: Apps/Top Apps | 6 | 6 | +0 | ✅ PASS |
| 树形节点: Apps/Recommended Apps | 6 | 6 | +0 | ✅ PASS |
| 树形节点: Featured/Latest Movies & TV | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Featured/Latest News | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Featured/Latest Trailers | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Movies/Recommended | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Movies/Comedy | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Movies/Action | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Movies/Drama | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Movies/Crime | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Movies/Fantasy | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Movies/Family | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Movies/Western | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Movies/Documentary | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: TV Shows/Recommended | 0 | 29 | -29 | ❌ DIFF |
| 树形节点: TV Shows/Comedy | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: TV Shows/Action | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: TV Shows/Kids | 0 | 0 | +0 | ✅ PASS |
| 树形节点: TV Shows/Drama | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: TV Shows/Family | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: TV Shows/Western | 0 | 8 | -8 | ❌ DIFF |
| 树形节点: TV Shows/Reality TV | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Live/Recommended | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Live/Movie & Series | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Free TV/Hero Banner | 4 | 4 | +0 | ✅ PASS |
| 树形节点: Free TV/Program Guide | 1 | 1 | +0 | ✅ PASS |
| 树形节点: Free TV/Live Now | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Free TV/Recommended Channels | 11 | 11 | +0 | ✅ PASS |
| 树形节点: Free TV/Trending Free Movies | 0 | 30 | -30 | ❌ DIFF |
| 树形节点: Free TV/Free Apps | 8 | 8 | +0 | ✅ PASS |

## 差异分析

### 按钮功能差异

- **Personalized recommendations 按钮:** JDK17版本比JDK8版本少8个数据项

### 树形节点差异

- **树形节点: Home/Prime Video 二级推荐:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Home/Whale TV+二级推荐:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Home/Prime Video:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Home/Hot Movies:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Home/Dazn二级推荐:** JDK17版本比JDK8版本少20个数据项
- **树形节点: Featured/Latest Movies & TV:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Featured/Latest News:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Featured/Latest Trailers:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Movies/Recommended:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Movies/Comedy:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Movies/Action:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Movies/Drama:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Movies/Crime:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Movies/Fantasy:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Movies/Family:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Movies/Western:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Movies/Documentary:** JDK17版本比JDK8版本少30个数据项
- **树形节点: TV Shows/Recommended:** JDK17版本比JDK8版本少29个数据项
- **树形节点: TV Shows/Comedy:** JDK17版本比JDK8版本少30个数据项
- **树形节点: TV Shows/Action:** JDK17版本比JDK8版本少30个数据项
- **树形节点: TV Shows/Drama:** JDK17版本比JDK8版本少30个数据项
- **树形节点: TV Shows/Family:** JDK17版本比JDK8版本少30个数据项
- **树形节点: TV Shows/Western:** JDK17版本比JDK8版本少8个数据项
- **树形节点: TV Shows/Reality TV:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Live/Recommended:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Live/Movie & Series:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Free TV/Live Now:** JDK17版本比JDK8版本少30个数据项
- **树形节点: Free TV/Trending Free Movies:** JDK17版本比JDK8版本少30个数据项

## 统计分析

- **按钮功能测试:** 3 项
- **树形节点测试:** 41 项
- **数据完全一致的项目:** 15 项
- **JDK17数据更多的项目:** 0 项
- **JDK8数据更多的项目:** 29 项
- **JDK8多出数据的平均值:** 28.1

## 结论

⚠️ **发现 29 项差异。** 需要进一步分析差异原因。

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
*报告生成时间: 2026-05-07 14:59:54*
