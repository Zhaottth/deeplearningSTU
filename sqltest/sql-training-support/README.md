# SQL 训练营

直接用浏览器打开上一级的 `1.html`，无需联网或安装依赖。原版保留为 `1.original.html`。

包含 233 道题、6 阶段学习路线、8 个电商实战，以及收藏、错题、间隔复习、进度导入导出。

## 学习建议

1. 阅读一个阶段的概念与示例，进入对应专题训练。
2. 多选题选择完后提交。命令题只检查参考写法，不执行 SQL；等价答案可能显示待核对。
3. 在独立 MySQL 8.0.16+ 练习环境中执行 `sql-training-data.sql`，然后独立完成实战。
4. 对照实战预期结果，解释空值、并列、无匹配与重复行，最后再阅读参考解法。
5. 从复习报告进入到期题目，定期导出 JSON 记录。页面不发送桌面提醒。

数据脚本首次运行会创建练习库和两张表，不会删已有表。不要重复执行插入部分。页面本身不连接数据库。新版使用独立 localStorage 键，不迁移原版可能存在误判的结果。

## 校验范围

- Edge 无头浏览器：分页、筛选、单选、多选、严格命令匹配、保存恢复、考试隐藏与交卷锁定、重练、收藏、课程跳转、实战草稿、下载、报告、390px 手机宽度及 JavaScript 错误检查。
- 8 个实战查询在 SQLite 的公共 SQL 子集上执行，并逐行对照预期结果；这仅为逻辑交叉验证，不等于 MySQL 方言、DDL、事务或性能验证。当前环境没有 MySQL 客户端/服务。
- 页面不自动验证索引效果、事务并发或实战自评结果。

## 修改和构建

`upgrade-quiz.cjs` 从原版读取题库、修正知识点并追加进阶题，生成 `quiz-bank.json`。
`quiz-shell.html` 是页面模板；`quiz-cases.cjs` 包含实战样例，生成最终单文件 HTML 和 SQL 脚本。

在工作区根目录执行：

```powershell
node sql-training-support/upgrade-quiz.cjs
node sql-training-support/quiz-cases.cjs
# 需要 playwright 包与 Microsoft Edge；必要时配置 NODE_PATH
node sql-training-support/verify-quiz.cjs
```

最终交付的 `1.html` 不依赖此支持目录，单独复制即可使用。
