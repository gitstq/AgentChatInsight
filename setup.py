#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentChatInsight - AI对话历史智能分析引擎
Lightweight AI Chat History Intelligent Analysis Engine
"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='agentchat-insight',
    version='1.0.0',
    author='AgentChatInsight Team',
    author_email='team@agentchat-insight.dev',
    description='AI对话历史智能分析引擎 - Lightweight AI Chat History Intelligent Analysis Engine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gitstq/AgentChatInsight',
    py_modules=['agentchat_insight'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.8',
    install_requires=[
        # 核心功能零依赖，以下为可选依赖
    ],
    extras_require={
        'rich': ['rich>=13.0.0'],
        'tui': ['textual>=0.40.0'],
        'all': ['rich>=13.0.0', 'textual>=0.40.0'],
    },
    entry_points={
        'console_scripts': [
            'agentchat-insight=agentchat_insight:main',
        ],
    },
    keywords='ai chat analysis conversation insights claude chatgpt gemini copilot cursor',
)
