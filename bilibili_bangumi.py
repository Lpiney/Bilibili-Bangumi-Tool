#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站追番列表爬虫
"""

import json
import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_bangumi_list(mid):
    """获取B站用户追番列表"""
    
    # 直接使用 API 方法，避免 Chrome 驱动问题
    print("使用 B 站 API 获取追番列表...")
    return get_bangumi_list_api(mid)
    
    try:
        print(f"正在打开页面: {url}")
        driver.get(url)
        
        # 增加等待时间
        time.sleep(5)
        
        # 尝试不同的选择器
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.bangumi-item'))
            )
        except:
            print("无法找到 .bangumi-item，尝试其他选择器")
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.bili-bangumi-card'))
                )
            except:
                print("无法找到番剧元素，返回空列表")
                return []
        
        all_bangumi = []
        page = 1
        
        while True:
            # 尝试不同的选择器
            try:
                items = driver.find_elements(By.CSS_SELECTOR, '.bangumi-item')
                if not items:
                    items = driver.find_elements(By.CSS_SELECTOR, '.bili-bangumi-card')
            except:
                items = []
            
            print(f"第 {page} 页，找到 {len(items)} 部追番")
            
            for item in items:
                try:
                    title_elem = item.find_element(By.CSS_SELECTOR, '.bili-bangumi-card__title')
                    title = title_elem.text.strip()
                except:
                    try:
                        title_elem = item.find_element(By.CSS_SELECTOR, '.title')
                        title = title_elem.text.strip()
                    except:
                        title = ''
                
                try:
                    cover = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                except:
                    cover = ''
                
                try:
                    desc_list = item.find_elements(By.CSS_SELECTOR, '.bili-bangumi-card__desc')
                    ep_text = ''
                    if desc_list:
                        last_desc = desc_list[-1].text.strip()
                        if '全' in last_desc and '话' in last_desc:
                            ep_text = last_desc
                except:
                    ep_text = ''
                
                try:
                    desc_list = item.find_elements(By.CSS_SELECTOR, '.bili-bangumi-card__desc')
                    rating = '0'
                    for desc in desc_list:
                        text = desc.text.strip()
                        if text.replace('.', '').replace('分', '').isdigit():
                            rating = text
                            break
                except:
                    rating = '0'
                
                try:
                    desc_list = item.find_elements(By.CSS_SELECTOR, '.bili-bangumi-card__desc')
                    pub_date = ''
                    if desc_list:
                        first_desc = desc_list[0].text.strip()
                        if '年' in first_desc or '月' in first_desc or '日' in first_desc:
                            pub_date = first_desc
                        elif '番剧' in first_desc:
                            pub_date = first_desc
                except:
                    pub_date = ''
                
                try:
                    url_elem = item.find_element(By.CSS_SELECTOR, '.bili-bangumi-card__title')
                    url = url_elem.get_attribute('href')
                except:
                    try:
                        url_elem = item.find_element(By.TAG_NAME, 'a')
                        url = url_elem.get_attribute('href')
                    except:
                        url = ''
                
                bangumi = {
                    'title': title,
                    'cover': cover,
                    'ep_text': ep_text,
                    'rating': rating,
                    'pub_date': pub_date,
                    'url': url
                }
                
                if title:
                    all_bangumi.append(bangumi)
            
            # 尝试不同的分页按钮选择器
            try:
                next_buttons = driver.find_elements(By.CSS_SELECTOR, '.vui_pagenation--btn-side')
                if not next_buttons:
                    next_buttons = driver.find_elements(By.CSS_SELECTOR, '.pagination-btn')
                
                if len(next_buttons) >= 2:
                    next_button = next_buttons[1]  # 第二个是下一页
                    if 'disabled' in next_button.get_attribute('class'):
                        print("已到最后一页")
                        break
                    next_button.click()
                    page += 1
                    time.sleep(3)  # 增加等待时间
                else:
                    print("无法找到下一页按钮，停止")
                    break
            except Exception as e:
                print(f"分页出错: {e}")
                break
        
        return all_bangumi
        
    finally:
        driver.quit()


def get_bangumi_list_api(mid):
    """使用 B 站 API 获取追番列表"""
    print("使用 B 站 API 获取追番列表...")
    
    all_bangumi = []
    page = 1
    ps = 20  # 每页数量
    
    while True:
        url = f"https://api.bilibili.com/x/space/bangumi/follow/list"
        params = {
            "vmid": mid,
            "pn": page,
            "ps": ps,
            "type": 1,  # 1 表示追番
            "tid": 0,
            "keyword": "",
            "order": "progress"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "Referer": f"https://space.bilibili.com/{mid}/bangumi",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            print(f"API 请求状态码: {response.status_code}")
            print(f"API 响应内容: {response.text[:100]}...")
            
            data = response.json()
            
            if data.get("code") != 0:
                print(f"API 请求失败: {data.get('message')}")
                break
            
            items = data.get("data", {}).get("list", [])
            if not items:
                print("已到最后一页")
                break
            
            print(f"第 {page} 页，找到 {len(items)} 部追番")
            
            for item in items:
                bangumi = {
                    "title": item.get("title", ""),
                    "cover": item.get("cover", ""),
                    "ep_text": f"全{item.get('total_count', 0)}话" if item.get('total_count') else "",
                    "rating": f"{item.get('score', 0)}分" if item.get('score') else "0",
                    "pub_date": item.get("pub_date", ""),
                    "url": f"https://www.bilibili.com/bangumi/play/ss{item.get('season_id')}" if item.get('season_id') else ""
                }
                
                if bangumi["title"]:
                    all_bangumi.append(bangumi)
            
            page += 1
            time.sleep(1)  # 防止请求过快
            
        except Exception as e:
            print(f"API 请求出错: {e}")
            break
    
    return all_bangumi


def save_to_json(data, filename='bangumi_list.json'):
    """保存数据到JSON文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n数据已保存到: {filename}")


def print_bangumi_list(bangumi_list):
    """打印追番列表"""
    print(f"\n{'='*80}")
    print(f"追番列表 (共{len(bangumi_list)}部)")
    print(f"{'='*80}\n")
    
    for i, item in enumerate(bangumi_list, 1):
        print(f"{i}. {item['title']}")
        print(f"   评分: {item['rating']} | 集数: {item['ep_text']}")
        print(f"   发布时间: {item['pub_date']}")
        print(f"   链接: {item['url']}")
        print()


if __name__ == '__main__':
    print("注意：请手动输入用户ID，避免直接复制粘贴导致的乱码问题")
    mid = input("请输入B站用户ID: ")
    # 提取数字部分
    mid = ''.join(filter(str.isdigit, mid))
    if not mid:
        print("用户ID不能为空")
        exit()
    print(f"开始爬取用户 {mid} 的追番列表...")
    
    bangumi_list = get_bangumi_list(mid)
    
    if bangumi_list:
        print_bangumi_list(bangumi_list)
        save_to_json(bangumi_list)
    else:
        print("未获取到任何数据")