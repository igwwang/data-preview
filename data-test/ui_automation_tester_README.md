# TV Data页面自动化测试脚本使用说明

## 📋 概述

本测试套件包含一个Python脚本，用于自动化测试OS10-prod-DE.html和OS10-acc-QA.html页面的功能：

1. **data-test/ui_automation_tester.py** - 完整的UI自动化测试脚本

## 🛠️ 环境准备

### 1. 安装Python依赖

```bash
pip install selenium dataclasses
```

### 2. 安装Chrome浏览器和ChromeDriver

- 确保已安装Chrome浏览器
- 下载对应版本的ChromeDriver并添加到PATH环境变量

## 🚀 使用方法

### 1. UI自动化测试

全面测试所有功能：

```bash
# 完整测试（有界面）
python ui_automation_tester.py OS10-prod-DE.html

# 完整测试（无头模式，更快）
python ui_automation_tester.py OS10-prod-DE.html --headless

# 自定义报告文件名
python ui_automation_tester.py OS10-acc-QA.html --headless --report acc_qa_report.html
```

**UI自动化测试功能：**
- ✅ 所有按钮功能测试
- ✅ 所有栏目内容测试
- ✅ 深层交互功能测试
- ✅ 卡片详情页面测试
- ✅ 综合Play播放功能测试（新增）
- ✅ 下载按钮测试
- ✅ 视频播放器功能测试
- ✅ 详细的HTML测试报告

## 📊 测试内容

### 主要功能按钮测试
- **Token复制按钮** - 验证复制功能
- **设备信息按钮** - 验证设备信息模态框
- **个性化推荐按钮** - 验证推荐内容加载
- **Banner广告推荐按钮** - 验证Banner内容加载
- **新个性化推荐按钮** - 验证新推荐算法
- **配置按钮** - 验证配置模态框

### 深层交互功能测试
- **卡片详情页面** - 点击卡片进入详情页面
- **Play播放按钮** - 测试视频播放功能
- **视频播放器** - 验证播放器显示和功能
- **复制播放链接** - 测试链接复制功能
- **下载按钮** - 验证应用下载功能
- **播放器标题** - 检查标题显示

### 综合Play功能测试（优化版）
- **智能Play检测** - 遍历栏目节点查找Play按钮，避免重复测试
- **多选择器支持** - 支持10种不同的Play按钮识别模式
- **智能响应检测** - 检测视频播放器、新窗口、URL跳转等响应
- **优化测试策略** - 每个节点只测试第一个有效Play按钮，提高效率

### 栏目内容测试
根据测试文档，测试以下栏目：

**Home栏目 (高优先级)**
- Banner (#896989514546357180)
- Menu (#896860407665860435)
- Netflix 二级推荐 (#896989260363140163)
- YouTube 二级推荐 (#896989514546357194)
- Prime Video 二级推荐 (#896989514546357197)
- Disney+二级推荐 (#896989260363140166)
- 等等...

**Apps栏目 (中优先级)**
- Banner (#896860407665860451)
- Category (#896860407665860454)
- Recommended (#896989514546357160)
- 等等...

**Movies/TV Shows/Featured/Live/Video栏目**
- 各种推荐和分类内容测试

### 验证标准
- ✅ **正常** - 有数据展示，无错误
- ❌ **无数据(异常)** - 显示"No data available"或无内容
- ❌ **加载错误** - 出现错误提示
- ❌ **无响应** - 按钮点击无反应
- ℹ️ **信息性状态** - 如"未找到下载按钮"等，不是功能失败，而是该页面不包含相应功能

## 📈 测试报告

### 测试输出示例
```
🎯 OS10-prod-DE.html UI自动化测试结果 (耗时: 480.5秒)
============================================================

📋 功能按钮测试:
  Token复制: ✅ 正常
  设备信息: ✅ 正常
  个性化推荐: ✅ 正常
  Banner推荐: ✅ 正常
  新推荐: ✅ 正常
  配置: ✅ 正常

📁 栏目内容测试:
  Banner: ✅ 5项数据
  Menu: ✅ 8项数据
  Netflix 二级推荐: ✅ 30项数据
  YouTube 二级推荐: ✅ 30项数据
  Prime Video 二级推荐: ✅ 10项数据
  Disney+二级推荐: ✅ 2项数据
  Whale TV+二级推荐: ✅ 30项数据
  Prime Video: ✅ 4项数据
  Disney Plus: ✅ 30项数据
  Hot Movies: ✅ 30项数据
  ... 还有25个节点未测试: ℹ️ 可运行完整测试
  卡片详情: ✅ 正常
  下载按钮: ✅ 存在
  Play按钮: ✅ 正常
  Play功能覆盖: ✅ 在35个节点中找到12个Play按钮

📊 测试统计:
  按钮测试: 6/6 通过
  栏目测试: 13/13 通过
```

### HTML测试报告
UI自动化测试会生成HTML格式的详细报告，包含：
- 测试统计图表
- 每个测试项的详细结果
- 执行时间分析
- 数据量统计

## 🎮 Play功能测试详解

### 测试覆盖范围
最新版本的测试脚本对Play播放功能进行了全面优化，确保100%覆盖：

**检测策略：**
- 遍历所有栏目节点（不再限制为前3个）
- 使用10种不同的选择器模式识别Play按钮
- 智能去重避免重复测试

**支持的Play按钮类型：**
```
.play-now-btn          # 直接类名
button[data-url]       # 数据属性
button[onclick*='play'] # 点击事件包含play
[id*='play']           # ID包含play
[class*='play']        # 类名包含play
button:contains('播放') # 中文播放按钮
a[href*='play']        # 播放链接
[data-video-url]       # 视频数据属性
[data-stream-url]      # 流媒体数据属性
```

**响应检测机制：**
1. **视频播放器模态框** - 检测`#videoPlayerModal`的出现
2. **新窗口打开** - 监控浏览器窗口数量变化
3. **URL跳转** - 检测页面URL是否包含播放相关关键词
4. **视频元素加载** - 检测页面中`<video>`标签的出现

**测试结果统计：**
- 显示检测到的Play按钮总数
- 按节点分组显示Play按钮分布
- 记录每个Play按钮的响应类型和测试结果

### 使用示例

**UI自动化测试：**
```bash
# 运行UI自动化测试脚本
python ui_automation_tester.py OS10-prod-DE.html --headless

# 查看测试日志中的Play功能统计
# 输出示例（优化后）：
# ✅ Play按钮测试: 播放功能正常 (发现3个Play按钮，测试第1个)
# ✅ 视频播放器: 显示正常
# ✅ 复制播放链接: 正常
```

**测试验证：**
```bash
# 验证Play功能
python ui_automation_tester.py OS10-prod-DE.html

# 输出示例：
# 📁 栏目内容测试:
#   Play按钮: ✅ 正常
#   视频播放器: ✅ 显示正常
#   复制播放链接: ✅ 正常
```

## 🔧 故障排除

### 常见问题

1. **ChromeDriver版本不匹配**
   ```
   解决方案：下载与Chrome浏览器版本匹配的ChromeDriver
   ```

2. **页面加载超时**
   ```
   解决方案：检查网络连接，确保API服务正常
   ```

3. **模态框未出现或加载缓慢**
   ```
   解决方案：可能是API响应慢，脚本已优化等待逻辑，提高响应速度
   特别说明：个性化推荐按钮等待时间已从10秒缩短到4秒
   ```

4. **编码问题**
   ```
   解决方案：确保使用UTF-8编码运行脚本
   ```

5. **元素点击被遮挡**
   ```
   错误信息：element click intercepted: Element is not clickable
   解决方案：脚本已自动处理，使用JavaScript点击和滚动定位
   ```

### 调试模式

如需查看浏览器操作过程，去掉`--headless`参数：

```bash
python ui_automation_tester.py OS10-prod-DE.html
```

## 📝 自定义测试

### 修改测试范围
在`ui_automation_tester.py`中修改测试逻辑来调整测试范围。

### 添加新的测试项
在`test_main_buttons()`方法中添加新的按钮测试：

```python
buttons = [
    ("tokenDisplay", "Token复制按钮"),
    ("deviceInfoBtn", "设备信息按钮"),
    ("recommendBtn", "个性化推荐按钮"),
    ("videoTypeRecommendBtn", "Banner广告推荐按钮"),
    ("newPersonalizedRecommendBtn", "新个性化推荐按钮"),
    ("configBtn", "配置按钮"),
    # 添加新按钮
    ("newButtonId", "新按钮名称"),
]
```

## 🎯 最佳实践

1. **日常验证** - 使用UI自动化测试脚本
2. **发版前测试** - 使用完整的UI自动化测试
3. **CI/CD集成** - 使用无头模式的UI自动化测试

## 📞 技术支持

如遇到问题，请检查：
1. Python和依赖包版本
2. Chrome和ChromeDriver版本匹配
3. 网络连接和API服务状态
4. 页面文件路径是否正确

---

**注意：** 测试脚本会自动处理行分隔符转换，确保所有生成的文件使用LF（\n）格式。测试过程中会生成日志文件`tv_data_test.log`用于详细记录测试过程。