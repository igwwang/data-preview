---
trigger: always_on
---
**记住在后续执行中严格遵循以下规则：**
- 10.邮件通知规范（强制执行）：
    - **触发条件**：每次完成用户请求的主要任务后（包括但不限于：代码修改、文件创建/删除、命令执行、问题分析等）
    - **必须发送**：使用 mcp_email-notification_send_task_completion_notification 工具发送任务完成通知
    - **邮件内容要求**：
        - taskName: 简要描述完成的任务
        - taskResult: 列出关键操作和结果
        - duration: 任务耗时（可选）
    - **执行时机**：在回复用户之前或与其他工具并行调用
- 14.git提交规范（强制执行）：所有git commit必须严格遵循简化格式：
    - 基础格式：<type>: <description>
    - 主要类型：
        - feat: 新功能
        - fix: 修复bug
        - docs: 文档变更
        - refactor: 代码重构
        - perf: 性能优化
        - test: 测试相关
        - chore: 构建/工具变动
        - style: 代码格式变动
        - ci: CI配置变更
        - revert: 回滚
    - 规范要求：50字符以内，祈使语气，首字母小写，无句号，**强制使用英文**
    - 示例：feat: add user registration feature、fix: resolve login page crash、docs: update README file

