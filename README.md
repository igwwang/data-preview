# data-preview - 智能电视内容数据预览与测试平台

面向 OS10 智能电视平台的 API 数据预览、对比与自动化测试工具集。

## 项目概述

### 目的

- **核心功能**：提供多环境（DEV/ACC/PROD）的 API 数据可视化预览页面，以及 JDK17 与 JDK8 版本间的数据一致性对比和自动化测试能力
- **业务价值**：加速 OS10 平台迭代验证，支持 JDK 升级过程中的数据回归测试，降低人工验证成本
- **数据流向**：HTML 配置文件 → Python 脚本解析配置 → 调用 SAAS API → 数据对比/完整性检查 → 生成 Markdown/HTML 报告

### 架构模式

- **类型**：工具集（静态页面 + 按需执行脚本）
- **执行模型**：按需触发（手动运行 / CI/CD 集成）
- **扩展性**：单机运行，支持多环境切换

## 项目结构

```
data-preview/
├── index.html                          # 入口页面，环境选择器
├── OS10-dev-*.html                     # DEV 环境数据预览页面
├── OS10-acc-*.html                     # ACC 环境数据预览页面
├── OS10-prod-*.html                    # PROD 环境数据预览页面
├── data-comparator/                    # 数据对比工具
│   ├── html_data_comparator.py         # JDK17 vs JDK8 数据对比脚本
│   ├── html_data_comparator_README.md  # 使用说明
│   └── HTML_Data_Comparison_Report_*.md # 历史对比报告
├── data-test/                          # 自动化测试工具
│   ├── api_data_integrity_checker.py   # API 数据完整性检查脚本
│   ├── cdn_accessibility_tester.py     # CDN 可访问性测试脚本
│   ├── ui_automation_tester.py         # UI 自动化测试脚本（Selenium）
│   ├── requirements.txt                # Python 依赖
│   └── *.html / *.md                   # 历史测试报告
└── docs/                               # 项目文档
    ├── localStorage-design.md          # localStorage 配置设计方案
    └── standards/                      # 开发规范文档
```

## 技术栈

- **HTML / CSS / JavaScript**：数据预览页面，响应式布局，支持本地与 GitHub Pages 访问
- **Python 3**：自动化测试与数据对比脚本
- **requests / urllib3**：HTTP 请求与 API 调用
- **pandas**：数据处理与统计分析
- **Selenium**：UI 自动化测试（需 Chrome + ChromeDriver）
- **HMAC-SHA1**：API 请求签名认证

## 工具说明

### 1. HTML 数据预览页面

各环境的数据预览页面，通过浏览器直接打开即可使用：

| 页面文件 | 环境 | 说明 |
|---------|------|------|
| `OS10-dev-QA.html` | DEV | 开发环境 QA 数据预览 |
| `OS10-acc-QA.html` | ACC | 验收环境 QA 数据预览 |
| `OS10-prod-QA.html` | PROD | 生产环境 QA 数据预览 |
| `OS10-prod-DE.html` | PROD | 德国区生产环境预览 |
| `OS10-*-JDK17.html` | 各环境 | JDK17 版本 API 数据预览 |

### 2. HTML 数据对比工具（data-comparator）

比对 JDK17 与 JDK8 版本 API 的数据差异，生成 Markdown 报告。

```bash
# DEV 环境对比
python data-comparator/html_data_comparator.py dev

# ACC 环境对比（默认）
python data-comparator/html_data_comparator.py acc

# PROD 环境对比
python data-comparator/html_data_comparator.py prod
```

对比内容包括：个性化推荐、Banner AD 推荐、新个性化推荐按钮数据量，以及树形栏目结构所有叶子节点的内容数据量。

详见 [data-comparator/html_data_comparator_README.md](data-comparator/html_data_comparator_README.md)。

### 3. API 数据完整性检查（data-test）

检查单个设备的 API 数据是否符合预期数量。

```bash
# 使用 JDK17 配置（默认）
python data-test/api_data_integrity_checker.py

# 使用 JDK8 配置
python data-test/api_data_integrity_checker.py jdk8
```

详见 [data-test/api_data_integrity_checker_README.md](data-test/api_data_integrity_checker_README.md)。

### 4. CDN 可访问性测试（data-test）

检测 API 返回的 icon 和 App 下载链接是否可正常访问（仅下载前 1MB 验证可达性）。

```bash
python data-test/cdn_accessibility_tester.py prod   # PROD 环境
python data-test/cdn_accessibility_tester.py acc    # ACC 环境
python data-test/cdn_accessibility_tester.py dev    # DEV 环境
```

### 5. UI 自动化测试（data-test）

基于 Selenium 对数据预览页面进行全功能自动化测试，覆盖按钮功能、栏目内容、Play 播放、CDN 下载等。

```bash
# 有界面模式
python data-test/ui_automation_tester.py OS10-prod-DE.html

# 无头模式（更快，适合 CI/CD）
python data-test/ui_automation_tester.py OS10-prod-DE.html --headless
```

详见 [data-test/ui_automation_tester_README.md](data-test/ui_automation_tester_README.md)。

## 快速开始

### 环境要求

- Python 3.8+
- Chrome 浏览器（UI 自动化测试需要）
- ChromeDriver（版本需与 Chrome 匹配，并添加到 PATH）
- 可访问对应环境的 SAAS API 服务器

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/igwwang/data-preview.git
cd data-preview

# 安装 Python 依赖
pip install -r data-test/requirements.txt
```

### 使用数据预览页面

直接用浏览器打开 `index.html`，或访问 GitHub Pages：

```
https://igwwang.github.io/data-preview/
```

选择对应环境后，页面会自动加载 API 数据。

## 配置说明

各 HTML 预览页面内嵌 JavaScript 配置，Python 脚本会自动解析：

| 配置项 | 说明 |
|--------|------|
| `API_BASE_URL` | API 服务器地址 |
| `ACCESS_KEY` | 设备访问密钥 |
| `SECRET_KEY` | 签名密钥 |
| `DEFAULT_PARAMS` | 默认请求参数（productId、brandId、deviceType 等） |

页面配置通过 `localStorage` 持久化，不同页面文件独立存储，详见 [docs/localStorage-design.md](docs/localStorage-design.md)。

## 环境对应关系

| 环境 | JDK8 API 服务器 | JDK17 API 服务器 |
|------|----------------|-----------------|
| DEV | dev-saas.zeasn.tv | dev-saas-17.zeasn.tv |
| ACC | acc-saas.zeasn.tv | acc-saas-17.zeasn.tv |
| PROD | saas.zeasn.tv | saas-17.zeasn.tv |

## 报告说明

各工具生成的报告文件命名规则：

| 工具 | 报告格式 | 示例 |
|------|---------|------|
| 数据对比 | `HTML_Data_Comparison_Report_{env}_{timestamp}.md` | `HTML_Data_Comparison_Report_prod_20260507_145954.md` |
| 完整性检查 | `API_Data_Integrity_Report_{config}_{timestamp}.md` | `API_Data_Integrity_Report_jdk8_20251222_174220.md` |
| CDN 测试 | `CDN_Accessibility_Report_{env}_{timestamp}.md` | `CDN_Accessibility_Report_prod_20260501_154113.md` |
| UI 自动化 | `UI_Automation_Test_Report_{timestamp}.html` | `UI_Automation_Test_Report_20260508_234214.html` |

## 开发规范

参考 [docs/standards/](docs/standards/) 目录下的规范文档：

- [NAMING-CONVENTIONS.md](docs/standards/latest/NAMING-CONVENTIONS.md) - 命名规范
- [API-DOC-STANDARDS.md](docs/standards/latest/API-DOC-STANDARDS.md) - API 文档规范
- [STANDARDS-GUIDE.md](docs/standards/latest/STANDARDS-GUIDE.md) - 规范总览

## 许可证

本项目为内部工具，版权归 Zeasn 所有，保留所有权利。

## 支持

- **文档**：[docs/](docs/) 目录
- **Issues**：[GitHub Issues](https://github.com/igwwang/data-preview/issues)
- **在线预览**：[GitHub Pages](https://igwwang.github.io/data-preview/)
