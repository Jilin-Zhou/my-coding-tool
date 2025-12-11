# 刷题辅助工具 (My Coding Tool)

一个基于 Web 的刷题辅助工具，帮助你管理刷过的编程题目、分析解题思路、存储高频函数，提升算法能力。

## 项目简介

这是一个功能完善的刷题管理系统，专为算法学习者设计。它不仅能帮你记录刷过的题目，还能通过智能分析帮你理解算法模式，并提供基于艾宾浩斯遗忘曲线的复习提醒。

## 核心功能

### 1. 题目管理
- ✅ 添加、编辑、删除题目
- ✅ 记录题目来源、题号、难度
- ✅ 支持 Markdown 格式的题目描述和解题思路
- ✅ 代码高亮显示
- ✅ 时间/空间复杂度记录
- ✅ 多标签分类
- ✅ 按难度、来源、标签筛选
- ✅ 全文搜索

### 2. 智能分析模块（混合方案）
- ✅ **基础分析（默认，离线可用）**：
  - 基于关键词匹配识别题目类型
  - 支持 14+ 种算法/数据结构模式
  - 推荐 Python 函数和代码模板
  - 无需网络，完全免费

- ✅ **AI 增强分析（可选）**：
  - 集成 OpenAI API（需配置 API Key）
  - 更精准的算法推荐
  - 深度思路分析
  - 自动降级保护

支持的算法模式：
- 双指针、滑动窗口、二分查找
- 动态规划、BFS、DFS/回溯
- 哈希表、栈、堆/优先队列
- 树、图、贪心、并查集
- 字符串处理

### 3. 函数库管理
- ✅ 预置 23+ 个 Python 高频函数
- ✅ 支持多语言（Python/Java/C++）
- ✅ 按分类浏览（排序、哈希、堆、队列等）
- ✅ 使用频率统计
- ✅ 添加自定义函数
- ✅ 详细的语法说明和示例代码

预置函数分类：
- 排序：sorted()、list.sort()
- 哈希：Counter、defaultdict
- 堆：heappush、heappop、nlargest、nsmallest
- 队列：deque
- 二分：bisect_left、bisect_right、insort
- 缓存：@lru_cache
- 迭代：permutations、combinations、product、accumulate
- 字符串：join、split
- 集合：交并差运算
- 数学：gcd、lcm、inf

### 4. 标签系统
- ✅ 创建、编辑、删除标签
- ✅ 多颜色支持
- ✅ 标签使用统计
- ✅ 按标签筛选题目

### 5. 统计面板（Dashboard）
- ✅ 刷题总数统计
- ✅ 难度分布饼图
- ✅ 刷题趋势折线图
- ✅ 标签分布柱状图
- ✅ 高频函数 Top 10
- ✅ 最近刷题记录
- ✅ 需要复习提醒

### 6. 复习提醒
- ✅ 基于艾宾浩斯遗忘曲线
- ✅ 自动安排复习计划
- ✅ 显示待复习和即将复习的题目
- ✅ 一键标记已复习

复习间隔：
- 第1次：1天后
- 第2次：2天后
- 第3次：4天后
- 第4次：7天后
- 第5次：15天后
- 第6次及以后：每30天

### 7. 界面特性
- ✅ 响应式布局（支持移动端）
- ✅ 深色/浅色主题切换
- ✅ 代码语法高亮
- ✅ Bootstrap 5 现代化设计
- ✅ Chart.js 数据可视化
- ✅ 中文界面

## 技术栈

### 后端
- **框架**：Python + Flask
- **数据库**：SQLite + SQLAlchemy ORM
- **AI分析**：OpenAI API（可选）

### 前端
- **框架**：Bootstrap 5
- **图表**：Chart.js
- **代码高亮**：Highlight.js
- **Markdown渲染**：Marked.js

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/Jilin-Zhou/my-coding-tool.git
cd my-coding-tool
```

### 2. 创建虚拟环境

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 初始化数据库

```bash
python init_db.py
```

这将创建数据库并预置 23+ 个 Python 高频函数。

### 5. 启动应用

```bash
python run.py
```

应用将在 http://localhost:5000 启动。

**开发模式**：设置环境变量 `FLASK_DEBUG=True` 启用调试模式（仅用于开发）：
```bash
# Windows (PowerShell)
$env:FLASK_DEBUG="True"

# macOS/Linux
export FLASK_DEBUG=True
```

**注意**：生产环境请使用 WSGI 服务器（如 gunicorn 或 uwsgi）而非 Flask 内置服务器。

## 使用说明

### 基本使用

1. **添加题目**
   - 点击"题目管理" → "添加题目"
   - 填写题目信息（标题、来源、难度等）
   - 支持 Markdown 格式的描述和思路
   - 添加代码和复杂度分析
   - 选择相关标签

2. **智能分析**
   - 进入"智能分析"页面
   - 输入题目标题和描述
   - 点击"分析题目"获取推荐算法和代码模板
   - 可选：勾选"使用 AI 增强分析"（需配置 API Key）

3. **查看函数库**
   - 进入"函数库"浏览预置函数
   - 按语言、分类筛选
   - 查看详细语法和示例
   - 点击"使用"按钮增加频率

4. **复习题目**
   - 进入"复习提醒"查看待复习题目
   - 点击"已复习"更新复习进度
   - 系统自动安排下次复习时间

5. **统计分析**
   - Dashboard 展示刷题统计
   - 难度分布、标签分布
   - 刷题趋势图
   - 高频函数统计

### 配置 AI 分析（可选）

AI 分析功能是可选的，基础分析已经足够强大。如需使用 AI 增强分析：

1. 获取 OpenAI API Key：
   - 访问 https://platform.openai.com/api-keys
   - 创建 API Key

2. 配置环境变量：

```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"

# macOS/Linux
export OPENAI_API_KEY="your-api-key-here"
```

或修改 `config.py` 文件直接设置。

3. 使用时勾选"使用 AI 增强分析"选项

**注意**：如果 API 调用失败，系统会自动降级到基础分析，不影响使用。

## 项目结构

```
my-coding-tool/
├── app/
│   ├── __init__.py          # Flask 应用初始化
│   ├── models.py            # 数据库模型
│   ├── routes/              # 路由模块
│   │   ├── main.py          # 主页/Dashboard
│   │   ├── problems.py      # 题目管理
│   │   ├── functions.py     # 函数库
│   │   ├── tags.py          # 标签管理
│   │   ├── analysis.py      # 智能分析
│   │   ├── stats.py         # 统计 API
│   │   └── review.py        # 复习提醒
│   ├── services/            # 业务逻辑
│   │   ├── analyzer.py      # 混合分析器
│   │   └── review.py        # 复习服务
│   ├── static/              # 静态文件
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── templates/           # HTML 模板
│       ├── base.html
│       ├── index.html
│       ├── problems/
│       ├── functions/
│       ├── tags/
│       ├── analysis.html
│       └── review.html
├── config.py                # 配置文件
├── requirements.txt         # Python 依赖
├── init_db.py              # 数据库初始化脚本
├── run.py                  # 应用启动入口
└── README.md               # 项目文档
```

## 数据库模型

### Problem（题目）
- 标题、来源、题号、难度
- 题目描述、解题思路、代码
- 时间/空间复杂度
- 关联标签和复习记录

### Function（函数）
- 函数名、编程语言、分类
- 语法、描述、示例
- 使用频率统计

### Tag（标签）
- 标签名、颜色
- 关联的题目列表

### Review（复习）
- 关联题目
- 复习次数、下次复习日期
- 上次复习时间

## 截图

（预留位置 - 待添加实际截图）

## 开发计划

- [ ] 导入/导出功能（JSON/CSV）
- [ ] 多用户支持和认证
- [ ] 题目评论和笔记
- [ ] Java/C++ 预置函数库
- [ ] 移动端 App
- [ ] 社区分享功能
- [ ] VS Code 插件集成

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 联系方式

- 作者：Jilin Zhou
- 项目链接：https://github.com/Jilin-Zhou/my-coding-tool

## 致谢

- Flask 社区
- Bootstrap 团队
- OpenAI
- 所有贡献者

---

**开始你的刷题之旅吧！** 🚀
