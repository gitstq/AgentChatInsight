<div align="center">

# 🤖 AgentChatInsight

### AI对话历史智能分析引擎

**Lightweight AI Chat History Intelligent Analysis Engine**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-green.svg)](https://github.com/gitstq/AgentChatInsight)

**[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)**

</div>

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

**AgentChatInsight** 是一款轻量级的AI对话历史智能分析引擎，专为开发者、研究人员和AI爱好者设计。它能够深度分析您与AI助手（如Claude、ChatGPT、Gemini、Copilot等）的对话历史，提取有价值的洞察，追踪讨论主题，生成专业的分析报告。

**💡 核心价值**：
- 🔍 **深度洞察**：自动识别对话主题、编程语言偏好、情感倾向
- 📊 **多维分析**：统计消息数量、代码块、提问频率等关键指标
- 📈 **趋势追踪**：分析活跃时段、话题演变、关键词热度
- 📝 **报告生成**：支持JSON、Markdown、HTML多种格式导出

**✨ 自研差异化亮点**：
- 🚀 **零核心依赖**：纯Python实现，无需安装复杂依赖
- 🎯 **多格式支持**：支持JSON、JSONL、Markdown、TXT、CSV等多种格式
- 🤖 **多平台识别**：自动识别Claude、ChatGPT、Gemini、Copilot、Cursor等平台
- 💻 **编程语言分析**：智能识别Python、JavaScript、React等技术栈

---

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📂 **多格式解析** | 支持JSON、JSONL、Markdown、TXT、CSV等格式 |
| 📊 **智能统计** | 消息数量、字符数、词数、代码块统计 |
| 🎯 **主题识别** | 自动识别编程、写作、学习、分析等主题 |
| 💻 **技术栈分析** | 识别Python、JavaScript、React、Django等技术 |
| 😊 **情感分析** | 分析对话情感倾向（正面/负面/中性） |
| ⏰ **时间分布** | 分析活跃时段分布 |
| 🔑 **关键词提取** | 自动提取高频关键词 |
| 📝 **报告导出** | 支持JSON、Markdown、HTML格式 |
| 🎨 **美观输出** | 支持Rich库美化终端输出 |

---

### 🚀 快速开始

#### 环境要求

- Python 3.8+
- 无需额外依赖（核心功能）

#### 安装

```bash
# 方式一：从源码安装
git clone https://github.com/gitstq/AgentChatInsight.git
cd AgentChatInsight
pip install -e .

# 方式二：直接使用
pip install rich  # 可选，用于美化输出
python agentchat_insight.py <输入路径>
```

#### 基本使用

```bash
# 分析单个文件
agentchat-insight chat.json

# 分析目录下所有对话
agentchat-insight ./conversations/

# 导出Markdown报告
agentchat-insight chat.json -o report.md -f markdown

# 导出HTML报告
agentchat-insight chat.json -o report.html -f html

# 导出JSON报告
agentchat-insight chat.json -o report.json -f json
```

---

### 📖 详细使用指南

#### 支持的输入格式

**1. JSON格式**
```json
{
  "conversations": [
    {
      "id": "conv-1",
      "messages": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
      ]
    }
  ]
}
```

**2. JSONL格式**
```jsonl
{"role": "user", "content": "Question 1"}
{"role": "assistant", "content": "Answer 1"}
```

**3. Markdown格式**
```markdown
**User**: Hello, can you help me?

**Assistant**: Of course! How can I assist you?
```

**4. 纯文本格式**
```
User: What is Python?

Assistant: Python is a programming language...
```

#### 输出示例

```
📊 基础统计
┌─────────────┬────────┐
│ 指标        │ 数值   │
├─────────────┼────────┤
│ 对话总数    │ 100    │
│ 消息总数    │ 1,500  │
│ 用户消息    │ 750    │
│ AI消息      │ 750    │
│ 总字符数    │ 500,000│
│ 代码块数量  │ 150    │
└─────────────┴────────┘

🎯 智能洞察
• 主要讨论主题: coding (出现 500 次)
• 最常涉及的编程技术: python (提及 200 次)
• 活跃时段: 14:00 (共 80 条消息)
• 对话情感倾向: 75.2% 正面
```

---

### 💡 设计思路与迭代规划

#### 设计理念

AgentChatInsight 的设计理念是**简单、轻量、实用**：

1. **零核心依赖**：核心分析功能不依赖任何第三方库，确保兼容性和稳定性
2. **多格式兼容**：支持多种对话格式，适配不同AI平台的导出格式
3. **智能洞察**：不仅提供统计数据，还生成有价值的洞察和建议

#### 技术选型

- **纯Python实现**：无需编译，跨平台兼容
- **正则表达式解析**：灵活处理多种文本格式
- **Counter统计**：高效的关键词和主题统计
- **可选Rich库**：美观的终端输出（可选）

#### 后续迭代计划

- [ ] 支持更多AI平台格式（Cursor、Windsurf等）
- [ ] 添加TUI交互界面
- [ ] 支持对话搜索和过滤
- [ ] 添加对话质量评分
- [ ] 支持多语言界面

---

### 📦 打包与部署指南

#### 本地开发

```bash
# 安装开发依赖
pip install -e ".[all]"

# 运行测试
python -m pytest test_agentchat_insight.py -v

# 代码格式化
black agentchat_insight.py
```

#### 构建发布

```bash
# 构建包
python setup.py sdist bdist_wheel

# 上传到PyPI
twine upload dist/*
```

---

### 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 添加某个特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

---

### 📄 开源协议说明

本项目采用 **MIT License** 开源协议，您可以自由使用、修改和分发。

---

<a name="繁體中文"></a>
## 🇹🇼 繁體中文

### 🎉 專案介紹

**AgentChatInsight** 是一款輕量級的AI對話歷史智能分析引擎，專為開發者、研究人員和AI愛好者設計。它能夠深度分析您與AI助手（如Claude、ChatGPT、Gemini、Copilot等）的對話歷史，提取有價值的洞察，追蹤討論主題，生成專業的分析報告。

**💡 核心價值**：
- 🔍 **深度洞察**：自動識別對話主題、程式語言偏好、情感傾向
- 📊 **多維分析**：統計訊息數量、程式碼區塊、提問頻率等關鍵指標
- 📈 **趨勢追蹤**：分析活躍時段、話題演變、關鍵字熱度
- 📝 **報告生成**：支援JSON、Markdown、HTML多種格式匯出

**✨ 自研差異化亮點**：
- 🚀 **零核心依賴**：純Python實現，無需安裝複雜依賴
- 🎯 **多格式支援**：支援JSON、JSONL、Markdown、TXT、CSV等多種格式
- 🤖 **多平台識別**：自動識別Claude、ChatGPT、Gemini、Copilot、Cursor等平台
- 💻 **程式語言分析**：智能識別Python、JavaScript、React等技術棧

---

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📂 **多格式解析** | 支援JSON、JSONL、Markdown、TXT、CSV等格式 |
| 📊 **智能統計** | 訊息數量、字元數、詞數、程式碼區塊統計 |
| 🎯 **主題識別** | 自動識別程式設計、寫作、學習、分析等主題 |
| 💻 **技術棧分析** | 識別Python、JavaScript、React、Django等技術 |
| 😊 **情感分析** | 分析對話情感傾向（正面/負面/中性） |
| ⏰ **時間分布** | 分析活躍時段分布 |
| 🔑 **關鍵字提取** | 自動提取高頻關鍵字 |
| 📝 **報告匯出** | 支援JSON、Markdown、HTML格式 |
| 🎨 **美觀輸出** | 支援Rich庫美化終端輸出 |

---

### 🚀 快速開始

#### 環境要求

- Python 3.8+
- 無需額外依賴（核心功能）

#### 安裝

```bash
# 方式一：從原始碼安裝
git clone https://github.com/gitstq/AgentChatInsight.git
cd AgentChatInsight
pip install -e .

# 方式二：直接使用
pip install rich  # 可選，用於美化輸出
python agentchat_insight.py <輸入路徑>
```

#### 基本使用

```bash
# 分析單個檔案
agentchat-insight chat.json

# 分析目錄下所有對話
agentchat-insight ./conversations/

# 匯出Markdown報告
agentchat-insight chat.json -o report.md -f markdown

# 匯出HTML報告
agentchat-insight chat.json -o report.html -f html

# 匯出JSON報告
agentchat-insight chat.json -o report.json -f json
```

---

### 🤝 貢獻指南

歡迎提交Issue和Pull Request！

1. Fork本倉庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'feat: 新增某個特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 建立Pull Request

---

### 📄 開源協議說明

本專案採用 **MIT License** 開源協議，您可以自由使用、修改和分發。

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Introduction

**AgentChatInsight** is a lightweight AI chat history intelligent analysis engine designed for developers, researchers, and AI enthusiasts. It deeply analyzes your conversation history with AI assistants (such as Claude, ChatGPT, Gemini, Copilot, etc.), extracts valuable insights, tracks discussion topics, and generates professional analysis reports.

**💡 Core Values**:
- 🔍 **Deep Insights**: Automatically identify conversation topics, programming language preferences, and sentiment tendencies
- 📊 **Multi-dimensional Analysis**: Statistics on message count, code blocks, question frequency, and other key metrics
- 📈 **Trend Tracking**: Analyze active time periods, topic evolution, and keyword popularity
- 📝 **Report Generation**: Export in JSON, Markdown, and HTML formats

**✨ Unique Highlights**:
- 🚀 **Zero Core Dependencies**: Pure Python implementation, no complex dependencies required
- 🎯 **Multi-format Support**: Supports JSON, JSONL, Markdown, TXT, CSV, and more
- 🤖 **Multi-platform Recognition**: Automatically identifies Claude, ChatGPT, Gemini, Copilot, Cursor, and other platforms
- 💻 **Programming Language Analysis**: Intelligently identifies Python, JavaScript, React, and other tech stacks

---

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📂 **Multi-format Parsing** | Supports JSON, JSONL, Markdown, TXT, CSV formats |
| 📊 **Intelligent Statistics** | Message count, character count, word count, code block statistics |
| 🎯 **Topic Recognition** | Automatically identifies coding, writing, learning, analysis topics |
| 💻 **Tech Stack Analysis** | Identifies Python, JavaScript, React, Django, and more |
| 😊 **Sentiment Analysis** | Analyzes conversation sentiment (positive/negative/neutral) |
| ⏰ **Time Distribution** | Analyzes active time period distribution |
| 🔑 **Keyword Extraction** | Automatically extracts high-frequency keywords |
| 📝 **Report Export** | Supports JSON, Markdown, HTML formats |
| 🎨 **Beautiful Output** | Supports Rich library for enhanced terminal output |

---

### 🚀 Quick Start

#### Requirements

- Python 3.8+
- No additional dependencies required (core functionality)

#### Installation

```bash
# Method 1: Install from source
git clone https://github.com/gitstq/AgentChatInsight.git
cd AgentChatInsight
pip install -e .

# Method 2: Direct usage
pip install rich  # Optional, for enhanced output
python agentchat_insight.py <input_path>
```

#### Basic Usage

```bash
# Analyze a single file
agentchat-insight chat.json

# Analyze all conversations in a directory
agentchat-insight ./conversations/

# Export Markdown report
agentchat-insight chat.json -o report.md -f markdown

# Export HTML report
agentchat-insight chat.json -o report.html -f html

# Export JSON report
agentchat-insight chat.json -o report.json -f json
```

---

### 💡 Design Philosophy & Roadmap

#### Design Philosophy

AgentChatInsight is designed with **simplicity, lightweight, and practicality** in mind:

1. **Zero Core Dependencies**: Core analysis functions don't rely on any third-party libraries
2. **Multi-format Compatibility**: Supports various conversation formats from different AI platforms
3. **Intelligent Insights**: Not just statistics, but valuable insights and recommendations

#### Roadmap

- [ ] Support more AI platform formats (Cursor, Windsurf, etc.)
- [ ] Add TUI interactive interface
- [ ] Support conversation search and filtering
- [ ] Add conversation quality scoring
- [ ] Support multi-language interface

---

### 📦 Packaging & Deployment

#### Local Development

```bash
# Install development dependencies
pip install -e ".[all]"

# Run tests
python -m pytest test_agentchat_insight.py -v

# Code formatting
black agentchat_insight.py
```

#### Build & Publish

```bash
# Build package
python setup.py sdist bdist_wheel

# Upload to PyPI
twine upload dist/*
```

---

### 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

---

### 📄 License

This project is licensed under the **MIT License** - you are free to use, modify, and distribute it.

---

<div align="center">

**Made with ❤️ by AgentChatInsight Team**

[⬆ Back to Top](#agentchatinsight)

</div>
