# OS10-prod-QA 页面转 APK 原生可行性分析

## 1. 当前页面核心功能

1. 调用远程 REST API（认证、获取栏目/内容/设备信息/推荐等）
2. 树形结构渲染 + 弹窗展示卡片列表
3. Video.js 播放 m3u8 流
4. HMAC-SHA1 签名生成
5. 配置管理（localStorage 持久化）
6. APK 下载（XHR + Blob）

## 2. 结论

**技术上可行，但投入产出比很低，不建议完全 Native 化。**

## 3. 技术对应关系

| 当前 HTML 功能 | Android 原生替代方案 |
|---|---|
| REST API 调用（Fetch） | Retrofit / OkHttp |
| 树形结构（DOM） | RecyclerView + ExpandableListView |
| 卡片列表（Bootstrap Card） | RecyclerView + CardView |
| 视频播放（Video.js / m3u8） | ExoPlayer（原生支持 HLS，更强） |
| HMAC-SHA1 签名（CryptoJS） | javax.crypto.Mac |
| 配置存储（localStorage） | SharedPreferences |
| 文件下载（XHR + Blob） | DownloadManager 或 OkHttp |

## 4. 不建议完全 Native 的原因

| 维度 | HTML 当前方案 | APK 原生方案 |
|---|---|---|
| 开发周期 | 已完成 | 预估 2-3 周（含 UI + 网络 + 播放器） |
| 部署更新 | 改文件即生效 | 需重新打包、签名、分发安装 |
| 跨设备使用 | 任何浏览器直接打开 | 仅限 Android 设备 |
| 维护成本 | 改 HTML/JS | 需 Android 开发环境 + Gradle 构建链 |
| 当前用途 | QA 测试/数据预览工具 | 过度工程化 |

## 5. AI 辅助开发评估

即使用 AI 辅助，完全 Native 方案仍需较长时间。

**AI 能加速的部分：**

- 生成 Retrofit 接口定义、数据模型类 → 几分钟
- 生成 RecyclerView Adapter 模板代码 → 几分钟
- ExoPlayer 播放器集成代码 → 几分钟
- HMAC-SHA1 签名工具类 → 几分钟

**AI 帮不了太多的部分：**

- Android 项目工程搭建、Gradle 依赖调试 → 环境问题多
- UI 还原度调试（间距、字体、响应式适配 TV 遥控器焦点） → 反复调
- 多个 Modal 弹窗的交互逻辑迁移（树形展开、卡片点击、详情、播放器层叠） → 状态管理复杂
- 真机调试、TV 设备适配 → AI 无法代劳
- API 联调中的 CORS 策略差异、Token 刷新时序 → 需要实际运行验证

**时间对比：**

| 阶段 | 纯手写 | AI 辅助 |
|---|---|---|
| 代码编写 | 2-3 周 | 3-5 天 |
| UI 调试适配 | 3-5 天 | 3-5 天（省不了） |
| 联调测试 | 2-3 天 | 2-3 天（省不了） |
| **合计** | **约 3-4 周** | **约 1.5-2 周** |

快了一倍左右，但仍然是"天"级别的工作量，不是"小时"级别。

## 6. 最终推荐方案：Hybrid App（WebView 壳 + DeepLink 桥接）

### 6.1 方案说明

APK 套壳 WebView，播放影音资源时解析 DeepLink 跳转到对应的应用进行播放。这是当前场景下的最优解。

### 6.2 为什么比完全 Native 更好

1. **开发成本极低**：WebView 加载现有 HTML，核心逻辑零改动，只需加一层 DeepLink 跳转的桥接代码
2. **维护简单**：业务逻辑改动只改 HTML/JS，不用重新打包 APK（HTML 可以放远程服务器）
3. **DeepLink 跳转是原生强项**：WebView 里拦截特定 URL scheme，用 Android Intent 跳转到目标 App

### 6.3 架构设计

```
WebView 壳 APK
├── MainActivity + WebView → 加载现有 HTML 页面
├── WebViewClient.shouldOverrideUrlLoading()
│   └── 拦截 deeplink URL scheme（如 netflix://、youtube:// 等）
│       → 构造 Intent 跳转到对应 App
│       → 目标 App 未安装时 fallback 提示
└── 可选：JS Bridge
    └── 让 HTML 端调用 window.Android.openDeeplink(url)
```

核心代码量：一个 Activity + 一个 WebViewClient，大概 100 行左右。

### 6.4 Hybrid 方案定位

这属于 Hybrid App（混合应用）的最轻量形态。

| 方案 | 说明 | 典型代表 |
|---|---|---|
| WebView 壳 + 原生桥接 | 本方案，最轻量 | 企业内部工具 |
| Cordova / Capacitor | 框架化的 WebView 壳，提供统一插件体系 | Ionic 系列 App |
| React Native / Flutter | JS/Dart 编写，编译为原生组件，不是 WebView | 大量商业 App |

Hybrid 的核心思想：**能用 Web 的用 Web，必须原生的才用原生**。本场景唯一需要原生能力的就是 Intent 跳转播放器 App，其余全部 Web 搞定。
