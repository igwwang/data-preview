# Standards Guide — 文档规范使用说明

> 本指南说明 `standards/` 目录下各规范文档的用途、适用场景及使用方法。

---

## 文档清单总览

| 文件名 | 类型 | 用途 |
|--------|------|------|
| `NAMING-CONVENTIONS.md` | 规范 | 文件、目录、标题、URL、参数的命名规则 |
| `PROJECT-STRUCTURE-TEMPLATE.md` | 模板 | Java Spring Boot 项目完整目录结构参考 |
| `PROJECT-README-TEMPLATE.md` | 模板 | 项目 README.md 的统一撰写模板 |
| `API-DOC-STANDARDS.md` | 规范+模板 | API 接口文档的结构标准与质量检查清单 |
| `TASK-DOC-STANDARDS.md` | 规范+模板 | 定时任务/批处理模块的文档结构标准 |
| `ITERATION-DESIGN-TEMPLATE-CHINESE.md` | 模板 | 版本迭代设计文档（中文版） |
| `ITERATION-DESIGN-TEMPLATE-ENGLISH.md` | 模板 | 版本迭代设计文档（英文版） |

---

## 各文档详细说明

### 1. NAMING-CONVENTIONS.md — 命名规范

**作用**：统一团队内所有文件、目录、文档标题、URL 路径和参数的命名风格，避免混乱。

**核心规则**：
- 文档文件：使用 `kebab-case`（小写 + 连字符），如 `device-group-data.md`
- 规范文件：使用全大写 + 连字符，如 `API-DOC-STANDARDS.md`
- 命名以**业务功能**为导向，不暴露实现细节（如类名、方法名）
- API 文档放 `docs/api/`，任务文档放 `docs/tasks/`

**何时使用**：
- 新建任何文档或目录前
- 代码评审时检查文件命名
- 重命名已有文件时参考迁移步骤

---

### 2. PROJECT-STRUCTURE-TEMPLATE.md — 项目目录结构模板

**作用**：提供标准 Java Spring Boot 项目的完整目录树，包含源码、测试、文档、配置、脚本等所有层级。

**核心内容**：
- 完整目录树（含注释说明每个目录用途）
- 三种项目类型的文档结构差异：
  - **API 项目**：保留 `docs/api/`，移除 `docs/tasks/`
  - **任务型项目**：保留 `docs/tasks/`、`docs/operations/`、`docs/data/`
  - **混合项目**：两者都保留
- 占位符替换说明（`[project-name]`、`[company]`、`[Entity]` 等）

**何时使用**：
- 创建新项目时，以此为蓝图搭建目录结构
- 评审项目结构是否符合规范时参考

---

### 3. PROJECT-README-TEMPLATE.md — README 模板

**作用**：统一项目根目录 `README.md` 的内容结构，确保每个项目都有完整的导航和说明。

**模板包含章节**：
- Project Overview（目的、架构模式）
- Project Structure（目录说明）
- Technology Stack
- API Endpoints / Tasks（按项目类型选择）
- Integration Guide
- Getting Started（安装、配置、快速启动）
- Configuration 表格
- Performance & Monitoring 指标表
- Changelog / Support

**何时使用**：
- 新项目初始化时，复制此模板创建 README
- 替换所有 `[占位符]` 为实际内容，删除不适用章节

---

### 4. API-DOC-STANDARDS.md — API 文档规范

**作用**：规定 API 接口文档的结构、内容深度要求和质量检查清单，确保文档真实反映代码实现。

**文档结构**（每份 API 文档必须包含）：
1. **API Overview** — 完整 URL（含 context-path）、HTTP 方法、功能描述
2. **Core Logic** — 逐层追踪 Controller → Service → DAO 的实际实现
3. **Sequence Diagram** — 使用真实类名和方法名的 Mermaid 时序图
4. **Data Flow** — 实际数据对象的流转路径
5. **Business Logic Characteristics** — 从代码中提取的业务规则
6. **Exception Handling** — 实际 try-catch 的异常处理

**关键强制要求**：
- URL 必须包含完整路径（含 context-path），如 `https://domain:port/tou/device/update`
- 所有内容必须来自实际代码分析，**禁止占位符内容**
- 多方法端点：不同实现 → 分开建文档；同一实现 → 单文档

**多方法端点决策**：

| 场景 | 策略 |
|------|------|
| 不同 `@RequestMapping` 方法 | 分开建文档（如 `user-tcmap-get.md` / `user-tcmap-set.md`） |
| 单方法支持多 HTTP 方法 | 单文档 |

**何时使用**：
- 编写任何 API 接口文档前，以此为结构模板
- 文档发布前，逐项核对文末的 Quality Assurance Checklist

---

### 5. TASK-DOC-STANDARDS.md — 任务文档规范

**作用**：规定定时任务、批处理任务等模块的文档结构标准。

**文档结构**（每份任务文档必须包含）：
1. **Task Usage Scenarios** — 业务场景、触发条件、执行频率
2. **Data Sources** — 数据来源表格（类型、访问方式、格式、更新频率）
3. **Core Processing Logic** — 数据获取 → 校验 → 转换 → 存储的步骤
4. **Sequence Diagram** — Scheduler → TaskJob → Service → DataSource → DB 的时序图
5. **Data Flow** — 数据流转的文字图示
6. **Data Storage** — 存储方式表格 + 数据结构 JSON 示例

**文件命名**：
- 存放位置：`docs/tasks/[task-name].md`
- 命名以业务功能为准：`data-error-notification.md` ✓，`DataErrorTask.md` ✗

**何时使用**：
- 为任何定时任务或批处理模块编写文档时

---

### 6. ITERATION-DESIGN-TEMPLATE-CHINESE.md / ENGLISH.md — 迭代设计文档模板

**作用**：提供版本迭代技术评审文档的完整模板，适用于功能新增、性能优化、重构等各类迭代。

**模板结构**：

| 章节 | 必选/可选 | 说明 |
|------|-----------|------|
| 执行摘要 | 必选 | 80字内概括核心变更 |
| 1. 迭代背景与目标 | 必选 | 驱动因素、现状分析、目标与成功标准 |
| 2. 变更设计 | 必选 | 变更范围、技术方案、架构变更、数据变更 |
| 3. 关键流程变更 | 必选 | 变更前后流程对比（Mermaid 时序图） |
| 4. 兼容性与风险分析 | 必选 | 兼容性评估、风险控制、回滚策略 |
| 5. 实施计划 | 可选 | 复杂迭代使用，含开发/测试/发布计划 |
| 6. 监控与验证 | 可选 | 性能优化或重要功能变更时使用 |
| 7. 总结与后续规划 | 可选 | 需要总结收益时使用 |

**技术方案章节按迭代类型选择**：
- 功能新增/修改 → 保留 `2.2.1 功能设计`
- 性能优化 → 保留 `2.2.2 性能优化设计`
- 重构 → 保留 `2.2.3 重构设计`

**使用步骤**：
1. 根据文档语言选择中文或英文模板
2. 填写文档头部元数据（版本、日期、迭代类型等）
3. 根据迭代类型删除不适用的章节
4. 替换所有 `[占位符]` 为实际内容
5. 删除所有 `<!-- 注释 -->` 行

---

## 快速选择指南

```
新建项目
  ├─ 搭建目录结构    → PROJECT-STRUCTURE-TEMPLATE.md
  └─ 写 README       → PROJECT-README-TEMPLATE.md

日常开发
  ├─ 新建文件/目录   → NAMING-CONVENTIONS.md（先查命名规则）
  ├─ 写 API 文档     → API-DOC-STANDARDS.md
  └─ 写任务文档      → TASK-DOC-STANDARDS.md

版本迭代评审
  ├─ 中文团队        → ITERATION-DESIGN-TEMPLATE-CHINESE.md
  └─ 英文团队        → ITERATION-DESIGN-TEMPLATE-ENGLISH.md
```

---

## 文档间依赖关系

```
NAMING-CONVENTIONS.md
    ↑ 被引用
    ├── API-DOC-STANDARDS.md      (文件命名规则)
    ├── TASK-DOC-STANDARDS.md     (文件命名规则)
    └── PROJECT-STRUCTURE-TEMPLATE.md (目录命名规则)

PROJECT-STRUCTURE-TEMPLATE.md
    ↑ 被引用
    └── PROJECT-README-TEMPLATE.md (目录结构说明)
```

---

**Guide Version**: v1.0
**Applies To**: All standards documents in this directory
