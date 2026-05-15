#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentChatInsight - AI对话历史智能分析引擎
Lightweight AI Chat History Intelligent Analysis Engine

A powerful CLI tool for analyzing AI assistant conversation history,
extracting insights, tracking topics, and generating intelligent reports.
"""

__version__ = "1.0.0"
__author__ = "AgentChatInsight Team"
__license__ = "MIT"

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter, defaultdict
import re

# Try to import optional dependencies
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from textual.app import App
    from textual.widgets import Header, Footer, Static, Tree
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False


class ConversationParser:
    """解析多种AI对话格式的解析器"""
    
    SUPPORTED_FORMATS = ['json', 'jsonl', 'markdown', 'txt', 'csv']
    
    # AI平台标识
    PLATFORM_PATTERNS = {
        'claude': [r'claude', r'anthropic'],
        'chatgpt': [r'chatgpt', r'gpt-4', r'gpt-3.5', r'openai'],
        'gemini': [r'gemini', r'bard', r'google'],
        'copilot': [r'copilot', r'github copilot'],
        'cursor': [r'cursor'],
        'windsurf': [r'windsurf'],
        'codex': [r'codex'],
    }
    
    def __init__(self):
        self.conversations = []
        self.metadata = {}
    
    def parse_file(self, file_path: str) -> List[Dict]:
        """解析单个对话文件"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        suffix = path.suffix.lower().lstrip('.')
        
        if suffix == 'json':
            return self._parse_json(path)
        elif suffix == 'jsonl':
            return self._parse_jsonl(path)
        elif suffix in ['md', 'markdown']:
            return self._parse_markdown(path)
        elif suffix == 'txt':
            return self._parse_txt(path)
        elif suffix == 'csv':
            return self._parse_csv(path)
        else:
            raise ValueError(f"不支持的文件格式: {suffix}")
    
    def _parse_json(self, path: Path) -> List[Dict]:
        """解析JSON格式对话"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 处理不同的JSON结构
        if isinstance(data, list):
            conversations = data
        elif isinstance(data, dict):
            # Claude Code格式
            if 'conversations' in data:
                conversations = data['conversations']
            elif 'messages' in data:
                conversations = [{'messages': data['messages']}]
            elif 'history' in data:
                conversations = data['history']
            else:
                conversations = [data]
        else:
            conversations = []
        
        return self._normalize_conversations(conversations, path.name)
    
    def _parse_jsonl(self, path: Path) -> List[Dict]:
        """解析JSONL格式对话"""
        conversations = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        conversations.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return self._normalize_conversations(conversations, path.name)
    
    def _parse_markdown(self, path: Path) -> List[Dict]:
        """解析Markdown格式对话"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        messages = []
        # 匹配常见的对话格式
        patterns = [
            (r'\*\*User\*\*[:\s]*(.*?)(?=\*\*Assistant\*\*|\*\*AI\*\*|\Z)', 'user'),
            (r'\*\*Assistant\*\*[:\s]*(.*?)(?=\*\*User\*\*|\Z)', 'assistant'),
            (r'\*\*AI\*\*[:\s]*(.*?)(?=\*\*User\*\*|\Z)', 'assistant'),
            (r'## User[:\s]*(.*?)(?=## Assistant|## AI|\Z)', 'user'),
            (r'## Assistant[:\s]*(.*?)(?=## User|\Z)', 'assistant'),
        ]
        
        for pattern, role in patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                messages.append({
                    'role': role,
                    'content': match.strip()
                })
        
        return [{
            'id': path.stem,
            'source': path.name,
            'messages': messages,
            'timestamp': datetime.fromtimestamp(path.stat().st_mtime).isoformat()
        }]
    
    def _parse_txt(self, path: Path) -> List[Dict]:
        """解析纯文本格式对话"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        messages = []
        lines = content.split('\n')
        current_role = None
        current_content = []
        
        for line in lines:
            # 检测角色标识
            if re.match(r'^(User|Human|Q|Question)[:\s]', line, re.IGNORECASE):
                if current_role and current_content:
                    messages.append({
                        'role': current_role,
                        'content': '\n'.join(current_content).strip()
                    })
                current_role = 'user'
                current_content = [re.sub(r'^(User|Human|Q|Question)[:\s]*', '', line, flags=re.IGNORECASE)]
            elif re.match(r'^(Assistant|AI|A|Answer|Bot)[:\s]', line, re.IGNORECASE):
                if current_role and current_content:
                    messages.append({
                        'role': current_role,
                        'content': '\n'.join(current_content).strip()
                    })
                current_role = 'assistant'
                current_content = [re.sub(r'^(Assistant|AI|A|Answer|Bot)[:\s]*', '', line, flags=re.IGNORECASE)]
            else:
                if current_role:
                    current_content.append(line)
        
        # 添加最后一条消息
        if current_role and current_content:
            messages.append({
                'role': current_role,
                'content': '\n'.join(current_content).strip()
            })
        
        return [{
            'id': path.stem,
            'source': path.name,
            'messages': messages,
            'timestamp': datetime.fromtimestamp(path.stat().st_mtime).isoformat()
        }]
    
    def _parse_csv(self, path: Path) -> List[Dict]:
        """解析CSV格式对话"""
        import csv
        messages = []
        
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                role = row.get('role', row.get('speaker', 'user'))
                content = row.get('content', row.get('message', row.get('text', '')))
                messages.append({
                    'role': role.lower(),
                    'content': content
                })
        
        return [{
            'id': path.stem,
            'source': path.name,
            'messages': messages,
            'timestamp': datetime.fromtimestamp(path.stat().st_mtime).isoformat()
        }]
    
    def _normalize_conversations(self, conversations: List, source: str) -> List[Dict]:
        """标准化对话格式"""
        normalized = []
        
        for i, conv in enumerate(conversations):
            if not isinstance(conv, dict):
                continue
            
            # 提取消息
            messages = []
            if 'messages' in conv:
                messages = conv['messages']
            elif 'history' in conv:
                messages = conv['history']
            elif 'content' in conv:
                # 单条消息格式
                messages = [{
                    'role': conv.get('role', 'user'),
                    'content': conv.get('content', '')
                }]
            
            # 标准化消息格式
            normalized_messages = []
            for msg in messages:
                if isinstance(msg, dict):
                    normalized_messages.append({
                        'role': msg.get('role', 'user'),
                        'content': msg.get('content', msg.get('text', msg.get('message', ''))),
                        'timestamp': msg.get('timestamp')
                    })
            
            if normalized_messages:
                normalized.append({
                    'id': conv.get('id', f"{source}_{i}"),
                    'source': source,
                    'messages': normalized_messages,
                    'timestamp': conv.get('timestamp', conv.get('created_at')),
                    'title': conv.get('title', conv.get('name')),
                    'model': conv.get('model')
                })
        
        return normalized
    
    def detect_platform(self, content: str) -> str:
        """检测AI平台类型"""
        content_lower = content.lower()
        
        for platform, patterns in self.PLATFORM_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    return platform
        
        return 'unknown'


class ConversationAnalyzer:
    """对话智能分析引擎"""
    
    # 编程语言关键词
    PROGRAMMING_KEYWORDS = [
        'python', 'javascript', 'typescript', 'java', 'c++', 'rust', 'go',
        'react', 'vue', 'angular', 'node', 'django', 'flask', 'fastapi',
        'api', 'database', 'sql', 'mongodb', 'redis', 'docker', 'kubernetes',
        'git', 'github', 'function', 'class', 'variable', 'loop', 'array'
    ]
    
    # 主题关键词
    TOPIC_KEYWORDS = {
        'coding': ['code', '编程', '代码', 'function', 'class', 'debug', 'error'],
        'writing': ['write', '写作', '文章', 'document', 'article', 'blog'],
        'analysis': ['analyze', '分析', 'data', 'report', '统计'],
        'learning': ['learn', '学习', 'tutorial', '教程', 'how to', '如何'],
        'translation': ['translate', '翻译', '中文', 'english'],
        'creative': ['create', '创建', 'design', '设计', 'generate', '生成'],
        'review': ['review', '审查', 'check', '检查', 'improve', '改进'],
        'explanation': ['explain', '解释', 'what is', '什么是', 'why', '为什么'],
    }
    
    # 情感关键词
    SENTIMENT_POSITIVE = ['great', 'good', 'excellent', 'perfect', 'awesome', 'thanks', 'thank', 'helpful', '很好', '谢谢', '感谢', '棒', '完美']
    SENTIMENT_NEGATIVE = ['bad', 'wrong', 'error', 'fail', 'problem', 'issue', 'bug', '错误', '问题', '失败', '不好']
    
    def __init__(self):
        self.stats = {}
        self.insights = {}
    
    def analyze(self, conversations: List[Dict]) -> Dict:
        """分析对话数据"""
        if not conversations:
            return {}
        
        self.stats = {
            'total_conversations': len(conversations),
            'total_messages': 0,
            'user_messages': 0,
            'assistant_messages': 0,
            'total_chars': 0,
            'total_words': 0,
            'avg_message_length': 0,
            'topics': Counter(),
            'programming_languages': Counter(),
            'sentiment': {'positive': 0, 'negative': 0, 'neutral': 0},
            'time_distribution': defaultdict(int),
            'message_length_distribution': [],
            'top_keywords': Counter(),
            'code_blocks': 0,
            'questions_asked': 0,
            'platforms': Counter(),
        }
        
        all_text = []
        
        for conv in conversations:
            messages = conv.get('messages', [])
            self.stats['total_messages'] += len(messages)
            
            for msg in messages:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                
                if role == 'user':
                    self.stats['user_messages'] += 1
                else:
                    self.stats['assistant_messages'] += 1
                
                self.stats['total_chars'] += len(content)
                words = len(content.split())
                self.stats['total_words'] += words
                self.stats['message_length_distribution'].append(len(content))
                
                all_text.append(content)
                
                # 分析主题
                self._analyze_topics(content)
                
                # 分析编程语言
                self._analyze_programming(content)
                
                # 分析情感
                self._analyze_sentiment(content)
                
                # 统计代码块
                self.stats['code_blocks'] += content.count('```')
                
                # 统计问题
                self.stats['questions_asked'] += content.count('?') + content.count('？')
                
                # 检测平台
                platform = ConversationParser().detect_platform(content)
                if platform != 'unknown':
                    self.stats['platforms'][platform] += 1
            
            # 时间分布
            timestamp = conv.get('timestamp')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    hour = dt.hour
                    self.stats['time_distribution'][hour] += 1
                except:
                    pass
        
        # 计算平均值
        if self.stats['total_messages'] > 0:
            self.stats['avg_message_length'] = self.stats['total_chars'] / self.stats['total_messages']
        
        # 提取关键词
        self.stats['top_keywords'] = self._extract_keywords(all_text)
        
        # 生成洞察
        self.insights = self._generate_insights()
        
        return {
            'stats': dict(self.stats),
            'insights': self.insights
        }
    
    def _analyze_topics(self, content: str):
        """分析主题"""
        content_lower = content.lower()
        
        for topic, keywords in self.TOPIC_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    self.stats['topics'][topic] += 1
                    break
    
    def _analyze_programming(self, content: str):
        """分析编程语言"""
        content_lower = content.lower()
        
        for keyword in self.PROGRAMMING_KEYWORDS:
            if keyword in content_lower:
                self.stats['programming_languages'][keyword] += 1
    
    def _analyze_sentiment(self, content: str):
        """分析情感"""
        content_lower = content.lower()
        
        positive_count = sum(1 for word in self.SENTIMENT_POSITIVE if word in content_lower)
        negative_count = sum(1 for word in self.SENTIMENT_NEGATIVE if word in content_lower)
        
        if positive_count > negative_count:
            self.stats['sentiment']['positive'] += 1
        elif negative_count > positive_count:
            self.stats['sentiment']['negative'] += 1
        else:
            self.stats['sentiment']['neutral'] += 1
    
    def _extract_keywords(self, texts: List[str]) -> Counter:
        """提取关键词"""
        # 简单的关键词提取（基于词频）
        all_words = []
        
        for text in texts:
            # 提取英文单词
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            all_words.extend(words)
            
            # 提取中文词（简单分词）
            chinese = re.findall(r'[\u4e00-\u9fff]+', text)
            for word in chinese:
                if len(word) >= 2:
                    all_words.append(word)
        
        # 过滤停用词
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                     'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                     'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
                     'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
                     'through', 'during', 'before', 'after', 'above', 'below',
                     'between', 'under', 'again', 'further', 'then', 'once',
                     'here', 'there', 'when', 'where', 'why', 'how', 'all',
                     'each', 'few', 'more', 'most', 'other', 'some', 'such',
                     'only', 'own', 'same', 'than', 'too', 'very', 'just',
                     'and', 'but', 'if', 'or', 'because', 'until', 'while',
                     'this', 'that', 'these', 'those', 'what', 'which', 'who',
                     'whom', 'this', 'that', 'am', 'it', 'its', 'not', 'no',
                     '的', '是', '在', '了', '和', '与', '或', '我', '你', '他',
                     '她', '它', '们', '这', '那', '有', '也', '就', '都', '而',
                     '及', '着', '或', '但', '可', '把', '被', '让', '给', '向'}
        
        filtered_words = [w for w in all_words if w not in stopwords]
        
        return Counter(filtered_words).most_common(50)
    
    def _generate_insights(self) -> Dict:
        """生成智能洞察"""
        insights = {
            'summary': '',
            'patterns': [],
            'recommendations': [],
            'highlights': []
        }
        
        # 生成摘要
        total_conv = self.stats['total_conversations']
        total_msg = self.stats['total_messages']
        avg_len = self.stats['avg_message_length']
        
        insights['summary'] = (
            f"共分析 {total_conv} 个对话，包含 {total_msg} 条消息。"
            f"平均消息长度 {avg_len:.0f} 字符。"
        )
        
        # 识别模式
        if self.stats['topics']:
            top_topic = self.stats['topics'].most_common(1)[0]
            insights['patterns'].append(
                f"主要讨论主题: {top_topic[0]} (出现 {top_topic[1]} 次)"
            )
        
        if self.stats['programming_languages']:
            top_lang = self.stats['programming_languages'].most_common(1)[0]
            insights['patterns'].append(
                f"最常涉及的编程技术: {top_lang[0]} (提及 {top_lang[1]} 次)"
            )
        
        # 时间模式
        if self.stats['time_distribution']:
            peak_hour = max(self.stats['time_distribution'].items(), key=lambda x: x[1])
            insights['patterns'].append(
                f"活跃时段: {peak_hour[0]}:00 (共 {peak_hour[1]} 条消息)"
            )
        
        # 情感分析
        sentiment = self.stats['sentiment']
        total_sentiment = sum(sentiment.values())
        if total_sentiment > 0:
            positive_ratio = sentiment['positive'] / total_sentiment * 100
            insights['patterns'].append(
                f"对话情感倾向: {positive_ratio:.1f}% 正面"
            )
        
        # 生成建议
        if self.stats['code_blocks'] > 10:
            insights['recommendations'].append(
                "代码讨论较多，建议使用代码片段管理工具整理常用代码"
            )
        
        if self.stats['questions_asked'] > 20:
            insights['recommendations'].append(
                "提问频率较高，可考虑建立FAQ知识库"
            )
        
        # 亮点
        if self.stats['total_words'] > 10000:
            insights['highlights'].append(
                f"累计对话内容丰富，共 {self.stats['total_words']} 词"
            )
        
        return insights


class ReportExporter:
    """报告导出器"""
    
    def __init__(self, analysis_result: Dict):
        self.result = analysis_result
    
    def export_json(self, output_path: str):
        """导出JSON格式"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.result, f, ensure_ascii=False, indent=2)
    
    def export_markdown(self, output_path: str):
        """导出Markdown格式"""
        stats = self.result.get('stats', {})
        insights = self.result.get('insights', {})
        
        md_content = f"""# AI对话历史分析报告

## 📊 基础统计

| 指标 | 数值 |
|------|------|
| 对话总数 | {stats.get('total_conversations', 0)} |
| 消息总数 | {stats.get('total_messages', 0)} |
| 用户消息 | {stats.get('user_messages', 0)} |
| AI消息 | {stats.get('assistant_messages', 0)} |
| 总字符数 | {stats.get('total_chars', 0):,} |
| 总词数 | {stats.get('total_words', 0):,} |
| 平均消息长度 | {stats.get('avg_message_length', 0):.1f} |
| 代码块数量 | {stats.get('code_blocks', 0)} |
| 提问数量 | {stats.get('questions_asked', 0)} |

## 🎯 智能洞察

### 摘要
{insights.get('summary', '无')}

### 识别模式
"""
        for pattern in insights.get('patterns', []):
            md_content += f"- {pattern}\n"
        
        md_content += "\n### 建议\n"
        for rec in insights.get('recommendations', []):
            md_content += f"- {rec}\n"
        
        md_content += "\n### 亮点\n"
        for highlight in insights.get('highlights', []):
            md_content += f"- {highlight}\n"
        
        # 主题分布
        topics = stats.get('topics', {})
        if topics:
            md_content += "\n## 📚 主题分布\n\n"
            # 支持Counter和普通dict
            if hasattr(topics, 'most_common'):
                topic_items = topics.most_common(10)
            else:
                topic_items = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:10]
            for topic, count in topic_items:
                md_content += f"- **{topic}**: {count} 次\n"
        
        # 编程语言
        langs = stats.get('programming_languages', {})
        if langs:
            md_content += "\n## 💻 编程技术\n\n"
            # 支持Counter和普通dict
            if hasattr(langs, 'most_common'):
                lang_items = langs.most_common(10)
            else:
                lang_items = sorted(langs.items(), key=lambda x: x[1], reverse=True)[:10]
            for lang, count in lang_items:
                md_content += f"- **{lang}**: {count} 次\n"
        
        # 关键词
        keywords = stats.get('top_keywords', [])
        if keywords:
            md_content += "\n## 🔑 高频关键词\n\n"
            for word, count in keywords[:20]:
                md_content += f"- **{word}**: {count} 次\n"
        
        # 情感分析
        sentiment = stats.get('sentiment', {})
        if sentiment:
            md_content += "\n## 😊 情感分析\n\n"
            md_content += f"- 正面: {sentiment.get('positive', 0)}\n"
            md_content += f"- 负面: {sentiment.get('negative', 0)}\n"
            md_content += f"- 中性: {sentiment.get('neutral', 0)}\n"
        
        # 时间分布
        time_dist = stats.get('time_distribution', {})
        if time_dist:
            md_content += "\n## ⏰ 时间分布\n\n```\n"
            for hour in range(24):
                count = time_dist.get(hour, 0)
                bar = '█' * min(count, 50)
                md_content += f"{hour:02d}:00 | {bar} {count}\n"
            md_content += "```\n"
        
        md_content += f"\n---\n*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    def export_html(self, output_path: str):
        """导出HTML格式"""
        stats = self.result.get('stats', {})
        insights = self.result.get('insights', {})
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI对话历史分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a1a1a; margin-bottom: 30px; border-bottom: 3px solid #4CAF50; padding-bottom: 15px; }}
        h2 {{ color: #333; margin: 25px 0 15px; padding-left: 10px; border-left: 4px solid #4CAF50; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .stat-card .value {{ font-size: 2em; font-weight: bold; }}
        .stat-card .label {{ font-size: 0.9em; opacity: 0.9; margin-top: 5px; }}
        .insight-box {{ background: #f8f9fa; border-radius: 8px; padding: 20px; margin: 15px 0; }}
        .insight-box h3 {{ color: #4CAF50; margin-bottom: 10px; }}
        .insight-box ul {{ list-style: none; padding-left: 0; }}
        .insight-box li {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
        .insight-box li:last-child {{ border-bottom: none; }}
        .tag {{ display: inline-block; background: #e3f2fd; color: #1976d2; padding: 4px 12px; border-radius: 20px; margin: 3px; font-size: 0.85em; }}
        .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 AI对话历史分析报告</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="value">{stats.get('total_conversations', 0)}</div>
                <div class="label">对话总数</div>
            </div>
            <div class="stat-card">
                <div class="value">{stats.get('total_messages', 0)}</div>
                <div class="label">消息总数</div>
            </div>
            <div class="stat-card">
                <div class="value">{stats.get('total_words', 0):,}</div>
                <div class="label">总词数</div>
            </div>
            <div class="stat-card">
                <div class="value">{stats.get('code_blocks', 0)}</div>
                <div class="label">代码块</div>
            </div>
        </div>
        
        <h2>🎯 智能洞察</h2>
        <div class="insight-box">
            <h3>摘要</h3>
            <p>{insights.get('summary', '无')}</p>
        </div>
        
        <div class="insight-box">
            <h3>识别模式</h3>
            <ul>
                {''.join(f'<li>{p}</li>' for p in insights.get('patterns', []))}
            </ul>
        </div>
        
        <div class="insight-box">
            <h3>建议</h3>
            <ul>
                {''.join(f'<li>{r}</li>' for r in insights.get('recommendations', []))}
            </ul>
        </div>
        
        <h2>📚 主题分布</h2>
        <div class="insight-box">
            {''.join(f'<span class="tag">{t}: {c}</span>' for t, c in list(stats.get('topics', {}).items())[:15])}
        </div>
        
        <h2>💻 编程技术</h2>
        <div class="insight-box">
            {''.join(f'<span class="tag">{l}: {c}</span>' for l, c in list(stats.get('programming_languages', {}).items())[:15])}
        </div>
        
        <h2>🔑 高频关键词</h2>
        <div class="insight-box">
            {''.join(f'<span class="tag">{w}</span>' for w, c in stats.get('top_keywords', [])[:20])}
        </div>
        
        <div class="footer">
            报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)


class AgentChatInsight:
    """主程序入口"""
    
    def __init__(self):
        self.parser = ConversationParser()
        self.analyzer = ConversationAnalyzer()
        self.conversations = []
    
    def load_from_path(self, path: str) -> int:
        """从路径加载对话"""
        path_obj = Path(path)
        
        if path_obj.is_file():
            self.conversations.extend(self.parser.parse_file(str(path_obj)))
        elif path_obj.is_dir():
            for ext in ConversationParser.SUPPORTED_FORMATS:
                for file_path in path_obj.glob(f'*.{ext}'):
                    try:
                        self.conversations.extend(self.parser.parse_file(str(file_path)))
                    except Exception as e:
                        print(f"警告: 无法解析 {file_path}: {e}")
        else:
            raise FileNotFoundError(f"路径不存在: {path}")
        
        return len(self.conversations)
    
    def analyze(self) -> Dict:
        """执行分析"""
        return self.analyzer.analyze(self.conversations)
    
    def export_report(self, result: Dict, output_path: str, format: str = 'markdown'):
        """导出报告"""
        exporter = ReportExporter(result)
        
        if format == 'json':
            exporter.export_json(output_path)
        elif format == 'markdown':
            exporter.export_markdown(output_path)
        elif format == 'html':
            exporter.export_html(output_path)
        else:
            raise ValueError(f"不支持的格式: {format}")
    
    def print_summary(self, result: Dict):
        """打印摘要"""
        if RICH_AVAILABLE:
            self._print_rich_summary(result)
        else:
            self._print_plain_summary(result)
    
    def _print_rich_summary(self, result: Dict):
        """使用Rich打印摘要"""
        console = Console()
        stats = result.get('stats', {})
        insights = result.get('insights', {})
        
        # 标题
        console.print(Panel.fit(
            "[bold blue]AgentChatInsight - AI对话历史智能分析报告[/bold blue]",
            subtitle=f"v{__version__}"
        ))
        
        # 基础统计表
        table = Table(title="📊 基础统计", show_header=True, header_style="bold magenta")
        table.add_column("指标", style="cyan")
        table.add_column("数值", style="green")
        
        table.add_row("对话总数", str(stats.get('total_conversations', 0)))
        table.add_row("消息总数", str(stats.get('total_messages', 0)))
        table.add_row("用户消息", str(stats.get('user_messages', 0)))
        table.add_row("AI消息", str(stats.get('assistant_messages', 0)))
        table.add_row("总字符数", f"{stats.get('total_chars', 0):,}")
        table.add_row("总词数", f"{stats.get('total_words', 0):,}")
        table.add_row("平均消息长度", f"{stats.get('avg_message_length', 0):.1f}")
        table.add_row("代码块数量", str(stats.get('code_blocks', 0)))
        table.add_row("提问数量", str(stats.get('questions_asked', 0)))
        
        console.print(table)
        
        # 智能洞察
        console.print("\n[bold]🎯 智能洞察[/bold]")
        console.print(Panel(insights.get('summary', '无'), title="摘要"))
        
        if insights.get('patterns'):
            console.print("\n[bold]识别模式:[/bold]")
            for pattern in insights['patterns']:
                console.print(f"  • {pattern}")
        
        if insights.get('recommendations'):
            console.print("\n[bold]建议:[/bold]")
            for rec in insights['recommendations']:
                console.print(f"  💡 {rec}")
        
        # 主题分布
        topics = stats.get('topics', {})
        if topics:
            console.print("\n[bold]📚 主题分布 (Top 10):[/bold]")
            for topic, count in topics.most_common(10):
                console.print(f"  • {topic}: {count} 次")
        
        # 编程语言
        langs = stats.get('programming_languages', {})
        if langs:
            console.print("\n[bold]💻 编程技术 (Top 10):[/bold]")
            for lang, count in langs.most_common(10):
                console.print(f"  • {lang}: {count} 次")
        
        # 关键词
        keywords = stats.get('top_keywords', [])
        if keywords:
            console.print("\n[bold]🔑 高频关键词 (Top 15):[/bold]")
            keyword_str = " | ".join([f"{w}({c})" for w, c in keywords[:15]])
            console.print(f"  {keyword_str}")
        
        # 情感分析
        sentiment = stats.get('sentiment', {})
        if sentiment:
            console.print("\n[bold]😊 情感分析:[/bold]")
            total = sum(sentiment.values())
            if total > 0:
                pos_pct = sentiment.get('positive', 0) / total * 100
                console.print(f"  正面: {sentiment.get('positive', 0)} ({pos_pct:.1f}%)")
                console.print(f"  负面: {sentiment.get('negative', 0)}")
                console.print(f"  中性: {sentiment.get('neutral', 0)}")
    
    def _print_plain_summary(self, result: Dict):
        """打印纯文本摘要"""
        stats = result.get('stats', {})
        insights = result.get('insights', {})
        
        print("\n" + "=" * 60)
        print("AgentChatInsight - AI对话历史智能分析报告")
        print("=" * 60)
        
        print("\n📊 基础统计:")
        print(f"  对话总数: {stats.get('total_conversations', 0)}")
        print(f"  消息总数: {stats.get('total_messages', 0)}")
        print(f"  用户消息: {stats.get('user_messages', 0)}")
        print(f"  AI消息: {stats.get('assistant_messages', 0)}")
        print(f"  总字符数: {stats.get('total_chars', 0):,}")
        print(f"  总词数: {stats.get('total_words', 0):,}")
        print(f"  平均消息长度: {stats.get('avg_message_length', 0):.1f}")
        print(f"  代码块数量: {stats.get('code_blocks', 0)}")
        print(f"  提问数量: {stats.get('questions_asked', 0)}")
        
        print("\n🎯 智能洞察:")
        print(f"  摘要: {insights.get('summary', '无')}")
        
        if insights.get('patterns'):
            print("\n  识别模式:")
            for pattern in insights['patterns']:
                print(f"    • {pattern}")
        
        if insights.get('recommendations'):
            print("\n  建议:")
            for rec in insights['recommendations']:
                print(f"    💡 {rec}")
        
        print("\n" + "=" * 60)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='AgentChatInsight - AI对话历史智能分析引擎',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
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
        """
    )
    
    parser.add_argument('input', help='输入文件或目录路径')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-f', '--format', choices=['json', 'markdown', 'html'],
                        default='markdown', help='输出格式 (默认: markdown)')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    # 创建分析器
    analyzer = AgentChatInsight()
    
    try:
        # 加载对话
        count = analyzer.load_from_path(args.input)
        print(f"✅ 成功加载 {count} 个对话")
        
        if count == 0:
            print("❌ 没有找到有效的对话数据")
            return 1
        
        # 执行分析
        result = analyzer.analyze()
        
        # 打印摘要
        analyzer.print_summary(result)
        
        # 导出报告
        if args.output:
            analyzer.export_report(result, args.output, args.format)
            print(f"\n✅ 报告已导出: {args.output}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        return 1
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
