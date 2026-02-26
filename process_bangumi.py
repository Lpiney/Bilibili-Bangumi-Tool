#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理bangumi_list.json文件
1. 去除重复的动漫（如同时有一、二、三季的）
2. 只保留番剧名称
"""

import json
import re


def process_bangumi_list(input_file, output_file):
    """处理bangumi列表"""
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"原始数据：{len(data)} 部动漫")
    
    # 提取和处理动漫名称
    processed_titles = set()
    
    for item in data:
        title = item.get('title', '')
        if not title:
            continue
        
        # 去除季数信息
        # 匹配模式：如 "第二季"、"第2季"、"Season 2" 等
        cleaned_title = re.sub(r'\s*第[一二三四五六七八九十0-9]+季\s*', '', title)
        cleaned_title = re.sub(r'\s*Season\s*[0-9]+\s*', '', cleaned_title)
        cleaned_title = re.sub(r'\s*S[0-9]+\s*', '', cleaned_title)
        
        # 去除多余空格
        cleaned_title = cleaned_title.strip()
        
        if cleaned_title:
            processed_titles.add(cleaned_title)
    
    # 转换为列表并排序
    final_titles = sorted(list(processed_titles))
    
    print(f"处理后：{len(final_titles)} 部动漫")
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_titles, f, ensure_ascii=False, indent=2)
    
    print(f"处理完成，结果已保存到：{output_file}")
    
    # 显示前20个结果
    print("\n前20个处理结果：")
    for i, title in enumerate(final_titles[:20], 1):
        print(f"{i}. {title}")


if __name__ == '__main__':
    input_file = 'bangumi_list.json'
    output_file = 'bangumi_list_cleaned.json'
    
    process_bangumi_list(input_file, output_file)