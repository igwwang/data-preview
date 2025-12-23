# HTML数据比对测试脚本使用说明

## 📋 概述

本测试套件包含一个Python脚本，用于比对JDK17版本和JDK8版本API接口的数据差异：

1. **data-comparator/html_data_comparator.py** - 完整的HTML数据比对测试脚本

## 🛠️ 环境准备

### 1. 安装Python依赖

```bash
pip install requests pandas urllib3
```

### 2. 网络环境要求

根据不同环境自动连接对应的API服务器：

**DEV环境：**
- JDK17版本API: https://dev-saas-17.zeasn.tv
- JDK8版本API: https://dev-saas.zeasn.tv

**ACC环境：**
- JDK17版本API: https://acc-saas-17.zeasn.tv
- JDK8版本API: https://acc-saas.zeasn.tv

**PROD环境：**
- JDK17版本API: https://prod-saas-17.zeasn.tv
- JDK8版本API: https://prod-saas.zeasn.tv

## 🚀 使用方法

### 1. HTML数据比对测试

支持多环境数据比对，自动解析HTML文件配置：

```bash
# DEV环境比对测试
python html_data_comparator.py dev

# ACC环境比对测试（默认）
python html_data_comparator.py acc

# PROD环境比对测试
python html_data_comparator.py prod

# 不指定参数时使用默认ACC环境
python html_data_comparator.py

# 查看生成的报告
# 报告文件名格式: HTML_Data_Comparison_Report_{环境}_{时间戳}.md
```

**支持的环境：**
- **dev** - 开发环境，比对 OS10-dev-QA-JDK17.html 和 OS10-dev-QA.html
- **acc** - 验收环境，比对 OS10-acc-QA-JDK17.html 和 OS10-acc-QA.html  
- **prod** - 生产环境，比对 OS10-prod-QA-JDK17.html 和 OS10-prod-QA.html

**HTML数据比对测试功能：**
- ✅ 多环境支持（dev/acc/prod）
- ✅ 自动解析HTML文件配置
- ✅ 认证token获取和验证
- ✅ 个性化推荐按钮数据比对
- ✅ Banner AD推荐按钮数据比对
- ✅ 新个性化推荐按钮数据比对
- ✅ 树形结构节点完整遍历
- ✅ 栏目内容数据量比对
- ✅ 网络连接检测和重试机制
- ✅ 详细的Markdown测试报告

## 📊 测试内容

### API认证测试
- **设备认证Token** - 获取设备访问令牌
- **用户认证Token** - 获取用户访问令牌
- **网络连接检测** - 验证API服务器可达性

### 按钮功能数据比对
- **个性化推荐按钮** - 比对推荐内容数据量
- **Banner AD推荐按钮** - 比对广告推荐数据量
- **新个性化推荐按钮** - 比对新算法推荐数据量

### 树形结构数据比对
- **栏目结构获取** - 获取完整的栏目树形结构
- **叶子节点提取** - 提取所有可测试的叶子节点
- **内容数据比对** - 逐个比对每个节点的数据量
- **完整覆盖测试** - 确保所有节点都被测试

### 验证标准
- ✅ **PASS** - 两个版本数据量完全一致
- ❌ **DIFF** - 两个版本数据量存在差异
- ℹ️ **网络错误** - API请求失败或超时
- ⚠️ **部分失败** - 部分API可用，部分不可用

## 📈 测试报告

### 测试输出示例
```
开始DEV环境HTML数据比对测试...
============================================================
成功加载DEV环境配置:
  JDK17: https://dev-saas-17.zeasn.tv
  JDK8: https://dev-saas.zeasn.tv

1. 获取认证tokens...
  成功获取token: 10e756c18743b342a491...
  成功获取用户token: 1063fdb17dcbee464fa2...

2. 测试按钮功能...
   2.1 测试个性化推荐按钮...
       JDK17: 30, JDK8: 30, 差异: 0
   2.2 测试Banner AD推荐按钮...
       JDK17: 1, JDK8: 1, 差异: 0
   2.3 测试新个性化推荐按钮...
       JDK17: 30, JDK8: 28, 差异: +2

3. 测试树形结构链接...
   发现 45 个JDK17叶子节点, 43 个JDK8叶子节点
   总共需要测试 47 个唯一节点
   3.1 测试节点: Home/Banner (ID: 896989514546357180)
         JDK17: 5, JDK8: 5, 差异: 0 [PASS]
   3.2 测试节点: Home/Menu (ID: 896860407665860435)
         JDK17: 8, JDK8: 8, 差异: 0 [PASS]
   ...

============================================================
测试完成，生成对比报告...

[报告] 详细报告已保存到: HTML_Data_Comparison_Report_dev_20241219_173132.md

[摘要] 测试摘要:
   总测试项: 50
   通过测试: 47
   差异测试: 3
   通过率: 94.0%
```

### Markdown测试报告
HTML数据比对测试会生成Markdown格式的详细报告，包含：
- 测试概述和统计信息
- 详细的测试结果表格
- 差异分析和原因推测
- 统计分析和数据分布
- 结论和后续建议

## 🔧 核心功能详解

### 多环境配置解析
测试脚本支持自动解析HTML文件中的配置：

**配置解析策略：**
- 自动定位对应环境的HTML文件
- 提取API_BASE_URL、ACCESS_KEY、SECRET_KEY
- 解析DEFAULT_PARAMS参数对象
- 支持JavaScript对象格式解析

**环境文件映射：**
```python
env_mapping = {
    'dev': {'jdk17_file': 'OS10-dev-QA-JDK17.html', 'jdk8_file': 'OS10-dev-QA.html'},
    'acc': {'jdk17_file': 'OS10-acc-QA-JDK17.html', 'jdk8_file': 'OS10-acc-QA.html'},
    'prod': {'jdk17_file': 'OS10-prod-QA-JDK17.html', 'jdk8_file': 'OS10-prod-QA.html'}
}
```

### 网络连接检测
测试脚本包含智能的网络连接检测机制：

**检测策略：**
- TCP连接测试验证服务器可达性
- 支持HTTPS和HTTP协议
- 10秒连接超时设置

**重试机制：**
```python
# 最多重试3次，每次间隔2秒
max_retries = 3
retry_delay = 2
```

### 认证机制
支持完整的API认证流程：

**认证类型：**
1. **设备认证** - 获取设备访问token
2. **用户认证** - 获取用户访问token
3. **HMAC签名** - 使用SHA1算法生成请求签名

**认证参数：**
```python
DEFAULT_PARAMS = {
    'productId': 'wtv10',
    'brandId': '7',
    'deviceType': 'WHALEOS_ZEASN_962D4_4K_MTP_P15',
    'countryCode': 'US',
    'langCode': 'en',
    # ... 更多参数
}
```

### 数据比对算法
采用智能的数据比对策略：

**比对维度：**
- 数据数量比对
- 差异值计算
- 状态判断（PASS/DIFF）

**树形遍历：**
- 递归提取所有叶子节点
- 按API返回顺序测试
- 确保100%节点覆盖

### 使用示例

**基础数据比对：**
```bash
# 运行DEV环境数据比对测试
python html_data_comparator.py dev

# 查看测试过程输出
# 输出示例：
# ✅ 个性化推荐按钮: 数据一致 (JDK17: 30, JDK8: 30)
# ❌ 新推荐按钮: 发现差异 (JDK17: 30, JDK8: 28, 差异: +2)
```

**多环境比对：**
```bash
# 比对不同环境
python html_data_comparator.py dev    # 开发环境
python html_data_comparator.py acc    # 验收环境  
python html_data_comparator.py prod   # 生产环境
```

**报告分析：**
```bash
# 查看生成的报告文件
cat HTML_Data_Comparison_Report_dev_20241219_173132.md

# 报告包含：
# - 环境信息和测试概述
# - 详细的差异分析
# - 可能的差异原因
# - 后续行动建议
```

## 🔧 故障排除

### 常见问题

1. **HTML文件不存在**
   ```
   错误信息：HTML文件不存在: OS10-dev-QA-JDK17.html
   解决方案：确保对应环境的HTML文件存在于项目根目录
   ```

2. **配置解析失败**
   ```
   错误信息：无法在文件中找到API_BASE_URL
   解决方案：检查HTML文件中的JavaScript配置格式是否正确
   ```

3. **环境参数错误**
   ```
   错误信息：不支持的环境参数
   解决方案：使用支持的环境参数：dev、acc、prod
   ```

4. **API服务器连接失败**
   ```
   错误信息：无法连接到服务器
   解决方案：检查网络连接，确认API服务器状态
   ```

5. **认证token获取失败**
   ```
   错误信息：Failed to get token
   解决方案：检查ACCESS_KEY和SECRET_KEY配置
   ```

6. **请求超时**
   ```
   错误信息：请求超时
   解决方案：脚本已内置重试机制，会自动重试3次
   ```

7. **数据解析错误**
   ```
   错误信息：JSON解析失败
   解决方案：检查API响应格式，可能是服务器返回了错误页面
   ```

8. **部分节点测试失败**
   ```
   错误信息：获取栏目内容失败
   解决方案：这是正常现象，某些节点可能暂时无数据
   ```

### 调试模式

如需查看详细的请求过程，可以修改脚本中的调试输出：

```python
# 在脚本中启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 自定义测试

### 修改测试参数
脚本会自动从HTML文件中解析配置，如需手动修改：

```python
# 修改环境映射
env_mapping = {
    'dev': {'jdk17_file': 'your-dev-jdk17.html', 'jdk8_file': 'your-dev-jdk8.html'},
    # ... 其他环境
}
```

### 添加新环境
在`_load_environment_configs()`方法中添加新环境：

```python
elif self.environment == 'test':
    jdk17_file = 'OS10-test-QA-JDK17.html'
    jdk8_file = 'OS10-test-QA.html'
```

### 添加新的API测试
在`run_comparison()`方法中添加新的API测试：

```python
# 添加新的API测试
def test_new_api(self, config, token):
    url = f"{config['API_BASE_URL']}/your/new/api?token={token}"
    response = self.make_request_with_retry('get', url)
    return response.json().get('data', [])
```

### 自定义报告格式
修改`generate_report()`方法来自定义报告格式：

```python
# 添加自定义报告内容
f.write("## 自定义分析\n\n")
f.write("您的自定义分析内容...\n")
```

## 🎯 最佳实践

1. **多环境验证** - 在不同环境间进行数据一致性验证
2. **定期比对** - 建议每日运行数据比对测试
3. **版本发布前** - 在版本发布前进行完整比对
4. **CI/CD集成** - 可集成到持续集成流程中
5. **报告归档** - 保存历史报告用于趋势分析

## 📞 技术支持

如遇到问题，请检查：
1. HTML文件是否存在于正确位置
2. HTML文件中的JavaScript配置格式是否正确
3. Python和依赖包版本
4. 网络连接和API服务器状态
5. 认证密钥配置是否正确
6. API接口是否有变更

**命令行帮助：**
```bash
python html_data_comparator.py --help
# 或运行时会显示用法说明
```

## 🔍 报告解读

### 差异类型分析
- **数据增加** - JDK17版本数据比JDK8多，可能是新功能或优化
- **数据减少** - JDK17版本数据比JDK8少，可能是数据筛选或缓存差异
- **完全一致** - 两个版本数据完全相同，表示该功能稳定

### 可能的差异原因
1. **API版本差异** - 不同版本的API逻辑变化
2. **配置参数差异** - 默认配置或环境变量不同
3. **数据源差异** - 连接到不同的数据库或缓存
4. **缓存机制差异** - 缓存策略或过期时间不同
5. **算法优化** - 推荐算法或数据筛选逻辑的改进

---

**注意：** 测试脚本会自动处理网络异常和API错误，确保测试的稳定性和可靠性。所有生成的报告文件使用UTF-8编码和LF行分隔符。