#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentChatInsight 测试套件
"""

import pytest
import json
import tempfile
from pathlib import Path

from agentchat_insight import (
    ConversationParser,
    ConversationAnalyzer,
    ReportExporter,
    AgentChatInsight
)


class TestConversationParser:
    """测试对话解析器"""
    
    def test_parse_json(self, tmp_path):
        """测试JSON格式解析"""
        # 创建测试JSON文件
        test_data = {
            "conversations": [
                {
                    "id": "test-1",
                    "messages": [
                        {"role": "user", "content": "Hello, how are you?"},
                        {"role": "assistant", "content": "I'm doing great! How can I help you today?"}
                    ]
                }
            ]
        }
        
        json_file = tmp_path / "test.json"
        json_file.write_text(json.dumps(test_data), encoding='utf-8')
        
        parser = ConversationParser()
        result = parser.parse_file(str(json_file))
        
        assert len(result) == 1
        assert result[0]['id'] == 'test-1'
        assert len(result[0]['messages']) == 2
    
    def test_parse_jsonl(self, tmp_path):
        """测试JSONL格式解析"""
        lines = [
            json.dumps({"role": "user", "content": "Question 1"}),
            json.dumps({"role": "assistant", "content": "Answer 1"}),
        ]
        
        jsonl_file = tmp_path / "test.jsonl"
        jsonl_file.write_text('\n'.join(lines), encoding='utf-8')
        
        parser = ConversationParser()
        result = parser.parse_file(str(jsonl_file))
        
        assert len(result) == 2
    
    def test_parse_markdown(self, tmp_path):
        """测试Markdown格式解析"""
        md_content = """**User**: Hello, can you help me with Python?

**Assistant**: Of course! I'd be happy to help with Python. What do you need?

**User**: How do I read a file?

**Assistant**: You can use the `open()` function...
"""
        
        md_file = tmp_path / "test.md"
        md_file.write_text(md_content, encoding='utf-8')
        
        parser = ConversationParser()
        result = parser.parse_file(str(md_file))
        
        assert len(result) == 1
        assert len(result[0]['messages']) == 4
    
    def test_parse_txt(self, tmp_path):
        """测试纯文本格式解析"""
        txt_content = """User: What is machine learning?

Assistant: Machine learning is a subset of artificial intelligence...

User: Can you give me an example?

Assistant: Sure! A common example is email spam filtering...
"""
        
        txt_file = tmp_path / "test.txt"
        txt_file.write_text(txt_content, encoding='utf-8')
        
        parser = ConversationParser()
        result = parser.parse_file(str(txt_file))
        
        assert len(result) == 1
        assert len(result[0]['messages']) == 4
    
    def test_detect_platform(self):
        """测试平台检测"""
        parser = ConversationParser()
        
        assert parser.detect_platform("I'm using Claude to help with coding") == 'claude'
        assert parser.detect_platform("ChatGPT is great for conversations") == 'chatgpt'
        assert parser.detect_platform("Gemini can help with research") == 'gemini'
        assert parser.detect_platform("This is a normal text") == 'unknown'


class TestConversationAnalyzer:
    """测试对话分析器"""
    
    @pytest.fixture
    def sample_conversations(self):
        """创建示例对话数据"""
        return [
            {
                "id": "conv-1",
                "messages": [
                    {"role": "user", "content": "How do I write a Python function?"},
                    {"role": "assistant", "content": "Here's how to write a Python function:\n```python\ndef hello():\n    print('Hello!')\n```"},
                    {"role": "user", "content": "Thanks! That's great!"},
                ]
            },
            {
                "id": "conv-2",
                "messages": [
                    {"role": "user", "content": "Can you explain React hooks?"},
                    {"role": "assistant", "content": "React hooks are functions that let you use state..."},
                ]
            }
        ]
    
    def test_analyze_basic_stats(self, sample_conversations):
        """测试基础统计分析"""
        analyzer = ConversationAnalyzer()
        result = analyzer.analyze(sample_conversations)
        
        stats = result['stats']
        assert stats['total_conversations'] == 2
        assert stats['total_messages'] == 5
        assert stats['user_messages'] == 3
        assert stats['assistant_messages'] == 2
        # 代码块统计：测试数据中有2个```标记
        assert stats['code_blocks'] == 2
        assert stats['questions_asked'] > 0
    
    def test_analyze_topics(self, sample_conversations):
        """测试主题分析"""
        analyzer = ConversationAnalyzer()
        result = analyzer.analyze(sample_conversations)
        
        topics = result['stats']['topics']
        assert 'coding' in topics or 'explanation' in topics
    
    def test_analyze_programming(self, sample_conversations):
        """测试编程语言分析"""
        analyzer = ConversationAnalyzer()
        result = analyzer.analyze(sample_conversations)
        
        langs = result['stats']['programming_languages']
        assert 'python' in langs
        assert 'react' in langs
    
    def test_analyze_sentiment(self, sample_conversations):
        """测试情感分析"""
        analyzer = ConversationAnalyzer()
        result = analyzer.analyze(sample_conversations)
        
        sentiment = result['stats']['sentiment']
        assert 'positive' in sentiment
        assert 'negative' in sentiment
        assert 'neutral' in sentiment
    
    def test_generate_insights(self, sample_conversations):
        """测试洞察生成"""
        analyzer = ConversationAnalyzer()
        result = analyzer.analyze(sample_conversations)
        
        insights = result['insights']
        assert 'summary' in insights
        assert 'patterns' in insights
        assert len(insights['patterns']) > 0


class TestReportExporter:
    """测试报告导出器"""
    
    @pytest.fixture
    def sample_result(self):
        """创建示例分析结果"""
        return {
            'stats': {
                'total_conversations': 10,
                'total_messages': 50,
                'user_messages': 25,
                'assistant_messages': 25,
                'total_chars': 10000,
                'total_words': 2000,
                'avg_message_length': 200.0,
                'code_blocks': 15,
                'questions_asked': 20,
                'topics': {'coding': 30, 'learning': 20},
                'programming_languages': {'python': 25, 'javascript': 15},
                'sentiment': {'positive': 30, 'negative': 5, 'neutral': 15},
                'top_keywords': [('code', 50), ('function', 40)],
                'time_distribution': {10: 5, 14: 10, 20: 8}
            },
            'insights': {
                'summary': 'Test summary',
                'patterns': ['Pattern 1', 'Pattern 2'],
                'recommendations': ['Rec 1'],
                'highlights': ['Highlight 1']
            }
        }
    
    def test_export_json(self, sample_result, tmp_path):
        """测试JSON导出"""
        exporter = ReportExporter(sample_result)
        output = tmp_path / "report.json"
        
        exporter.export_json(str(output))
        
        assert output.exists()
        with open(output, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert 'stats' in data
        assert 'insights' in data
    
    def test_export_markdown(self, sample_result, tmp_path):
        """测试Markdown导出"""
        exporter = ReportExporter(sample_result)
        output = tmp_path / "report.md"
        
        exporter.export_markdown(str(output))
        
        assert output.exists()
        content = output.read_text(encoding='utf-8')
        assert '# AI对话历史分析报告' in content
        assert '基础统计' in content
    
    def test_export_html(self, sample_result, tmp_path):
        """测试HTML导出"""
        exporter = ReportExporter(sample_result)
        output = tmp_path / "report.html"
        
        exporter.export_html(str(output))
        
        assert output.exists()
        content = output.read_text(encoding='utf-8')
        assert '<!DOCTYPE html>' in content
        assert 'AI对话历史分析报告' in content


class TestAgentChatInsight:
    """测试主程序"""
    
    def test_load_and_analyze(self, tmp_path):
        """测试加载和分析流程"""
        # 创建测试文件
        test_data = {
            "conversations": [
                {
                    "id": "test-1",
                    "messages": [
                        {"role": "user", "content": "Hello"},
                        {"role": "assistant", "content": "Hi there!"}
                    ]
                }
            ]
        }
        
        json_file = tmp_path / "test.json"
        json_file.write_text(json.dumps(test_data), encoding='utf-8')
        
        # 执行分析
        insight = AgentChatInsight()
        count = insight.load_from_path(str(json_file))
        
        assert count == 1
        
        result = insight.analyze()
        assert result['stats']['total_conversations'] == 1
        assert result['stats']['total_messages'] == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
