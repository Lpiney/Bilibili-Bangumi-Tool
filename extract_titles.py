#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取动漫名称列表
生成只包含动漫名称的结果，保持原始标题格式
"""

import json


def extract_titles(input_file, output_file):
    """提取动漫名称并保存"""
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"读取到 {len(data)} 部动漫")
    
    # 提取标题
    titles = []
    for item in data:
        title = item.get('title', '')
        if title:
            titles.append(title)
    
    # 保存为文本文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, title in enumerate(titles, 1):
            f.write(f" {i}. {title}\n")
    
    print(f"提取完成，共 {len(titles)} 个标题")
    print(f"结果已保存到：{output_file}")
    
    # 显示前20个结果
    print("\n前20个结果：")
    for i, title in enumerate(titles[:20], 1):
        print(f" {i}. {title}")


if __name__ == '__main__':
    input_file = 'bangumi_list.json'
    output_file = 'bangumi_titles.txt'
    
    extract_titles(input_file, output_file)