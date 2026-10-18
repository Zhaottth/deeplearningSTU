# 如何使用这个项目

## 为什么要有这个项目
> 由于大家在每次使用的时候都是新手，甚至不知道如何使用github或者说不知道如何下载，我这边先对git进行平时我会用到的基础的讲解，希望对大家有一定的帮助；不过目前我也并非精通git，只是会使用而已，如果有错误，我会积极改正.。


对于新手来应该都听说过github，或者说听说过git，但是平时大家在外边的教学班中不一定回使用到

首先记住这张图基本上就能会60%了

```bash
你用 VS Code 修改文件
          │
          ▼
    工作区（未暂存）
          │  git add
          ▼
    暂存区（已选择）
          │  git commit
          ▼
    本地仓库历史（Commit）
          │  git push
          ▼
    GitHub 远程仓库
```

## 一、Git 是什么？

- **Git**：记录代码修改历史，可以找回以前的版本。
- **GitHub**：把代码放到网上，方便保存和分享。
- **VS Code**：写代码的软件，也能操作 Git。

记住：**修改文件 → add → commit → push**。

## 二、最常用的 Git 命令

在 VS Code 中打开终端（`Ctrl + ~`），依次使用这些命令。

```bash
# 查看哪些文件被修改了
git status

# 把当前项目的修改加入暂存区
git add .

# 保存一次修改记录，双引号里的文字可以自己改
git commit -m "完成今天的学习笔记"

# 上传到 GitHub（需要先连接远程仓库）
git push

# 拉取 GitHub 上的更新
git pull

# 查看简短的提交记录
git log --oneline
```

> 注意：`add` 不是上传，`commit` 是保存在本地，`push` 才是上传 GitHub。

## 三、新项目怎么连接 GitHub？

先在 GitHub 创建一个空仓库，然后在项目文件夹的终端执行：

```bash
# 初始化仓库，并把初始分支命名为 main
git init -b main

# 添加文件
git add .

# 创建第一次提交
git commit -m "第一次提交"

# 连接 GitHub：把下面的地址换成自己的仓库地址
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 第一次上传，并建立 main 的跟踪关系
git push -u origin main
```

> 这组命令适合**本地新项目、GitHub 上的空仓库**。已经连接过 GitHub 的项目不要重复 `git init` 和 `git remote add`。

## 四、分支是什么？

分支就像项目的另一条开发路线。可以在新分支里试验，完成后再合并回 `main`。

```bash
# 查看本地有哪些分支，星号表示当前分支
git branch

# 新建并切换到 test 分支
git switch -c test

# 回到主分支
git switch main

# 将 test 的提交合并到当前 main 分支
git merge test

# 安全删除已经合并的本地 test 分支
git branch -d test
```

**常见问题：**

- `Already up to date.`：没有新的提交需要合并。
- 合并时出现黑色 Vim 编辑器：Git 要你确认合并说明。按 `Esc`，输入 `:wq`，再按回车即可保存退出。
- 删除分支**不一定删除提交历史**。如果提交已经合并进 `main`，别人仍能在历史里看到。

## 五、怎么查看以前的版本？

```bash
# 查看提交记录及分叉关系
git log --oneline --graph --all

# 查看当前分支状态
git status
```

想找回旧代码时，先记下提交编号，**不要直接使用 `git reset --hard` 或 `git push -f`**；这些命令可能让未保存的修改丢失，或者改写 GitHub 历史。


## 六、Markdown（.md）怎么写？
*我正好想到了markdown文档正好也写一下怎么使用啊，也是平时会用但是没有精通啊，大家见谅*
Markdown 是一种简单的文档格式。这个文件本身就是 Markdown。

| 想写什么 | 怎么写 |
| --- | --- |
| 一级标题 | `# 我的标题` |
| 二级标题 | `## 小标题` |
| 加粗 | `**重要内容**` |
| 斜体 | `*文字*` |
| 无序列表 | `- 第一项` |
| 有序列表 | `1. 第一项` |
| 链接 | `[GitHub](https://github.com)` |
| 图片 | `![图片说明](图片路径.png)` |
| 行内代码 | `` `git status` `` |
| 引用 | `> 这是一段提示` |

**代码块**要用三个反引号围起来，并在第一行写语言名称，例如：

````markdown
```bash
# 查看 Git 状态
git status
```
````

在 VS Code 中按 **`Ctrl + Shift + V`** 可以预览 Markdown；按 **`Ctrl + K`，再按 `V`** 可以在旁边预览。

## 七、我平时怎么记录学习过程？

1. 在 VS Code 中修改学习文件。
2. 输入 `git status` 看修改了什么。
3. 输入 `git add .` 选择本次修改。
4. 输入 `git commit -m "今天学会了分支合并"` 保存历史。
5. 输入 `git push` 上传到 GitHub。

以后每学会一个知识点，就往这个文件里补充一点。**GitHub 上的 Commits 页面就能看到我的学习和创作过程。**