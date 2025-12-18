#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML数据比对测试脚本 - 增强版
用于比对OS10-dev-QA-JDK17.html和OS10-dev-QA.html中各按钮和树形链接的数据数量差异
增加了错误处理、重试机制和网络连接检测
"""

import requests
import json
import time
from urllib.parse import urlencode
import hashlib
import hmac
import base64
from datetime import datetime
import pandas as pd
import urllib3
import socket

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HTMLDataComparator:
    def __init__(self):
        # JDK17版本配置
        self.jdk17_config = {
            'API_BASE_URL': 'https://acc-saas-17.zeasn.tv',
            'ACCESS_KEY': '10e756c18743b342a491b03f6040fbd873',
            'SECRET_KEY': '1063fdb17dcbee464fa248e4acaed367a9',
            'DEFAULT_PARAMS': {
                'productId': 'wtv10',
                'brandId': '7',
                'deviceSetId': '10bfa24f235519482a8b9b1c2ad7a3aef6',
                'deviceType': 'WHALEOS_ZEASN_962D4_4K_MTP_P15',
                'countryCode': 'US',
                'langCode': 'en',
                'mac': 'e8:51:9e:28:c7:4c',
                'functionType': 'TvLauncher',
                'ifGetTvDetail': '1',
                'iconResolution': '320*180',
                'terminalType': 'TV',
                'sn': '',
                'appVersion': '20000018',
                'androidVersion': '13',
                'osType': 'WhaleOSA',
                'clientIp': '122.10.101.131'
            }
        }
        
        # JDK8版本配置
        self.jdk8_config = {
            'API_BASE_URL': 'https://acc-saas.zeasn.tv',
            'ACCESS_KEY': '10e756c18743b342a491b03f6040fbd873',
            'SECRET_KEY': '1063fdb17dcbee464fa248e4acaed367a9',
            'DEFAULT_PARAMS': {
                'productId': 'wtv10',
                'brandId': '7',
                'deviceSetId': '10bfa24f235519482a8b9b1c2ad7a3aef6',
                'deviceType': 'WHALEOS_ZEASN_962D4_4K_MTP_P15',
                'countryCode': 'US',
                'langCode': 'en',
                'mac': 'e8:51:9e:28:c7:4c',
                'functionType': 'TvLauncher',
                'ifGetTvDetail': '1',
                'iconResolution': '320*180',
                'terminalType': 'TV',
                'sn': '',
                'appVersion': '20000018',
                'androidVersion': '13',
                'osType': 'WhaleOSA',
                'clientIp': '122.10.101.131'
            }
        }
        
        self.jdk17_token = None
        self.jdk8_token = None
        self.jdk17_user_token = None
        self.jdk8_user_token = None
        self.comparison_results = []
        self.max_retries = 3
        self.retry_delay = 2
        
    def check_network_connectivity(self, url):
        """检查网络连接"""
        try:
            # 提取主机名
            from urllib.parse import urlparse
            parsed = urlparse(url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            # 尝试TCP连接
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((host, port))
            sock.close()
            
            return result == 0
        except Exception as e:
            print(f"网络连接检查失败: {e}")
            return False
    
    def make_request_with_retry(self, method, url, **kwargs):
        """带重试机制的请求"""
        for attempt in range(self.max_retries):
            try:
                print(f"  尝试 {attempt + 1}/{self.max_retries}: {method.upper()} {url}")
                
                # 设置超时
                kwargs.setdefault('timeout', 30)
                kwargs.setdefault('verify', False)
                
                if method.lower() == 'get':
                    response = requests.get(url, **kwargs)
                elif method.lower() == 'post':
                    response = requests.post(url, **kwargs)
                else:
                    raise ValueError(f"不支持的HTTP方法: {method}")
                
                # 检查响应状态
                if response.status_code == 200:
                    return response
                else:
                    print(f"    HTTP错误: {response.status_code}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        response.raise_for_status()
                        
            except requests.exceptions.Timeout:
                print(f"    请求超时")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise
            except requests.exceptions.ConnectionError as e:
                print(f"    连接错误: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise
            except Exception as e:
                print(f"    请求失败: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise
        
        raise Exception(f"重试{self.max_retries}次后仍然失败")
    
    def generate_authorization_header(self, request_path, secret_key, access_key):
        """生成授权头"""
        ts = str(int(time.time() * 1000))
        encrypt_str = request_path + ts
        signature = hmac.new(
            secret_key.encode('utf-8'),
            encrypt_str.encode('utf-8'),
            hashlib.sha1
        ).digest()
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        return f"{access_key}:{signature_b64}:{ts}"
    
    def get_token(self, config):
        """获取认证token"""
        print(f"  获取token from {config['API_BASE_URL']}")
        
        # 检查网络连接
        if not self.check_network_connectivity(config['API_BASE_URL']):
            raise Exception(f"无法连接到服务器: {config['API_BASE_URL']}")
        
        params = urlencode(config['DEFAULT_PARAMS'])
        
        headers = {
            'Authorization': self.generate_authorization_header(
                '/auth-api/api/v1/auth/deviceSign',
                config['SECRET_KEY'],
                config['ACCESS_KEY']
            ),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        url = f"{config['API_BASE_URL']}/auth-api/api/v1/auth/deviceSign"
        response = self.make_request_with_retry('post', url, headers=headers, data=params)
        
        result = response.json()
        if result.get('errorCode') != "0":
            raise Exception(f"Failed to get token: {result.get('errorMsg', 'Unknown error')}")
        
        token = result['data']['token']
        print(f"  成功获取token: {token[:20]}...")
        return token
    
    def get_user_token(self, config):
        """获取用户token"""
        print(f"  获取用户token from {config['API_BASE_URL']}")
        
        params = {
            'productId': config['DEFAULT_PARAMS']['productId'],
            'brandId': config['DEFAULT_PARAMS']['brandId'],
            'deviceSetId': '',
            'mac': config['DEFAULT_PARAMS']['mac'],
            'deviceType': config['DEFAULT_PARAMS']['deviceType'],
            'deviceName': ''
        }
        
        headers = {
            'Authorization': self.generate_authorization_header(
                '/user/device/login',
                config['SECRET_KEY'],
                config['ACCESS_KEY']
            ),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        url = f"{config['API_BASE_URL']}/user/device/login"
        response = self.make_request_with_retry('post', url, headers=headers, data=urlencode(params))
        
        result = response.json()
        if result.get('errorCode') != "0":
            raise Exception(f"Failed to get user token: {result.get('errorMsg', 'Unknown error')}")
        
        user_token = result['data']['userToken']
        print(f"  成功获取用户token: {user_token[:20]}...")
        return user_token
    
    def get_columns(self, config, token):
        """获取栏目数据"""
        url = f"{config['API_BASE_URL']}/sp/api/device/v1/column?token={token}"
        response = self.make_request_with_retry('get', url)
        result = response.json()
        
        if result.get('errorCode') != 0:
            raise Exception(f"Failed to fetch columns: {result.get('errorMsg', 'Unknown error')}")
        
        return result['data']
    
    def get_column_content(self, config, token, column_id):
        """获取栏目内容"""
        url = f"{config['API_BASE_URL']}/sp/api/device/v1/column/content?token={token}&columnIds={column_id}"
        
        try:
            response = self.make_request_with_retry('get', url)
            result = response.json()
            
            if result.get('errorCode') != 0 or not result.get('data'):
                return None
            
            return result['data'][0] if result['data'] else None
        except Exception as e:
            print(f"    获取栏目内容失败 (ID: {column_id}): {e}")
            return None
    
    def get_personalized_recommendations(self, config, token, user_token):
        """获取个性化推荐"""
        url = f"{config['API_BASE_URL']}/sp/api/device/v1/video/recommend?token={token}&userToken={user_token}&videoType=MOVIE&size=30&needPoster=true&imgStyle=0&imgWidth=800"
        
        try:
            response = self.make_request_with_retry('get', url)
            result = response.json()
            
            if result.get('errorCode') != 0:
                return None
            
            return result.get('data', [])
        except Exception as e:
            print(f"    获取个性化推荐失败: {e}")
            return None
    
    def get_banner_ad_recommendation(self, config, token, user_token):
        """获取Banner AD推荐"""
        # JDK17版本使用不同的参数
        if 'acc-saas-17' in config['API_BASE_URL']:
            url = f"{config['API_BASE_URL']}/sp/api/device/v1/video/recommend/ad?token={token}&searchType=REC_CHANNEL,VOD&size=1&scopeId=3&typeWeight=100,100&supportAD=true&moreFields=description,tags,source,background,cover&posterShape&posterWidth&posterHeight&iconShape&iconWidth&iconHeight&position=LAUNCHER&userToken={user_token}"
        else:
            url = f"{config['API_BASE_URL']}/sp/api/device/v1/video/recommend/ad?token={token}&searchType=REC_CHANNEL,VOD&size=1&scopeId=3&typeWeight=100,100&supportAD=true&moreFields=description,tags,source,background,cover&posterShape&posterWidth&posterHeight&iconShape&iconWidth&iconHeight&position=LAUNCHER&userToken={user_token}"
        
        try:
            response = self.make_request_with_retry('get', url)
            result = response.json()
            
            if result.get('errorCode') != 0:
                return None
            
            return result.get('data', [])
        except Exception as e:
            print(f"    获取Banner AD推荐失败: {e}")
            return None
    
    def get_new_personalized_recommendations(self, config, token, user_token):
        """获取新个性化推荐"""
        url = f"{config['API_BASE_URL']}/sp/api/device/v1/video/recommend/choices?token={token}&objectTypes=REC_CHANNEL,REC_PROGRAM,MOVIE,SEASON&size=30&moreFields=description,backgroud,releaseTime,categories,scores,contributors,bindSource,views,source,tags,rating,defaultLangCode,updateTime,series,seasonNumber,episodeCount,duration,liveStartTime,liveEndTime,liveState&posterShape&posterWidth&posterHeight&iconShape=HORIZONTAL&iconWidth&iconHeight&userToken={user_token}"
        
        try:
            response = self.make_request_with_retry('get', url)
            result = response.json()
            
            if result.get('errorCode') != 0:
                return None
            
            return result.get('data', [])
        except Exception as e:
            print(f"    获取新个性化推荐失败: {e}")
            return None
    
    def extract_tree_nodes(self, data, parent_path=""):
        """递归提取树形节点"""
        nodes = []
        for item in data:
            current_path = f"{parent_path}/{item['name']}" if parent_path else item['name']
            
            if item.get('children'):
                # 父节点
                nodes.extend(self.extract_tree_nodes(item['children'], current_path))
            else:
                # 叶子节点
                nodes.append({
                    'id': item['id'],
                    'name': item['name'],
                    'path': current_path
                })
        
        return nodes
    
    def compare_data_counts(self, jdk17_data, jdk8_data, test_name):
        """比较数据数量"""
        jdk17_count = len(jdk17_data) if jdk17_data else 0
        jdk8_count = len(jdk8_data) if jdk8_data else 0
        difference = jdk17_count - jdk8_count
        
        return {
            'test_name': test_name,
            'jdk17_count': jdk17_count,
            'jdk8_count': jdk8_count,
            'difference': difference,
            'status': 'PASS' if difference == 0 else 'DIFF'
        }
    
    def run_comparison(self):
        """运行完整比对测试"""
        print("开始HTML数据比对测试...")
        print("=" * 60)
        
        try:
            # 1. 获取tokens
            print("1. 获取认证tokens...")
            
            try:
                self.jdk17_token = self.get_token(self.jdk17_config)
            except Exception as e:
                print(f"   JDK17 token获取失败: {e}")
                self.jdk17_token = None
            
            try:
                self.jdk8_token = self.get_token(self.jdk8_config)
            except Exception as e:
                print(f"   JDK8 token获取失败: {e}")
                self.jdk8_token = None
            
            # 检查是否至少有一个token成功
            if not self.jdk17_token and not self.jdk8_token:
                raise Exception("所有API服务器都无法连接，测试终止")
            
            # 获取用户tokens
            if self.jdk17_token:
                try:
                    self.jdk17_user_token = self.get_user_token(self.jdk17_config)
                except Exception as e:
                    print(f"   JDK17 用户token获取失败: {e}")
                    self.jdk17_user_token = None
            
            if self.jdk8_token:
                try:
                    self.jdk8_user_token = self.get_user_token(self.jdk8_config)
                except Exception as e:
                    print(f"   JDK8 用户token获取失败: {e}")
                    self.jdk8_user_token = None
            
            # 2. 测试按钮功能
            print("\n2. 测试按钮功能...")
            
            if self.jdk17_token and self.jdk8_token and self.jdk17_user_token and self.jdk8_user_token:
                # 2.1 个性化推荐按钮
                print("   2.1 测试个性化推荐按钮...")
                jdk17_recommendations = self.get_personalized_recommendations(
                    self.jdk17_config, self.jdk17_token, self.jdk17_user_token
                )
                jdk8_recommendations = self.get_personalized_recommendations(
                    self.jdk8_config, self.jdk8_token, self.jdk8_user_token
                )
                
                result = self.compare_data_counts(
                    jdk17_recommendations, jdk8_recommendations, 
                    "Personalized recommendations 按钮"
                )
                self.comparison_results.append(result)
                print(f"       JDK17: {result['jdk17_count']}, JDK8: {result['jdk8_count']}, 差异: {result['difference']}")
                
                # 2.2 Banner AD推荐按钮
                print("   2.2 测试Banner AD推荐按钮...")
                jdk17_banner = self.get_banner_ad_recommendation(
                    self.jdk17_config, self.jdk17_token, self.jdk17_user_token
                )
                jdk8_banner = self.get_banner_ad_recommendation(
                    self.jdk8_config, self.jdk8_token, self.jdk8_user_token
                )
                
                result = self.compare_data_counts(
                    jdk17_banner, jdk8_banner, 
                    "Banner AD Recommendation 按钮"
                )
                self.comparison_results.append(result)
                print(f"       JDK17: {result['jdk17_count']}, JDK8: {result['jdk8_count']}, 差异: {result['difference']}")
                
                # 2.3 新个性化推荐按钮
                print("   2.3 测试新个性化推荐按钮...")
                jdk17_new_recommendations = self.get_new_personalized_recommendations(
                    self.jdk17_config, self.jdk17_token, self.jdk17_user_token
                )
                jdk8_new_recommendations = self.get_new_personalized_recommendations(
                    self.jdk8_config, self.jdk8_token, self.jdk8_user_token
                )
                
                result = self.compare_data_counts(
                    jdk17_new_recommendations, jdk8_new_recommendations, 
                    "New Personalized recommendations 按钮"
                )
                self.comparison_results.append(result)
                print(f"       JDK17: {result['jdk17_count']}, JDK8: {result['jdk8_count']}, 差异: {result['difference']}")
            else:
                print("   跳过按钮测试 - 缺少必要的tokens")
            
            # 3. 测试树形结构链接
            print("\n3. 测试树形结构链接...")
            
            if self.jdk17_token and self.jdk8_token:
                # 3.1 获取栏目结构
                try:
                    jdk17_columns = self.get_columns(self.jdk17_config, self.jdk17_token)
                    jdk8_columns = self.get_columns(self.jdk8_config, self.jdk8_token)
                    
                    # 3.2 提取所有叶子节点
                    jdk17_nodes = self.extract_tree_nodes(jdk17_columns)
                    jdk8_nodes = self.extract_tree_nodes(jdk8_columns)
                    
                    print(f"   发现 {len(jdk17_nodes)} 个JDK17叶子节点, {len(jdk8_nodes)} 个JDK8叶子节点")
                    
                    # 3.3 创建节点映射表，确保完整覆盖
                    all_node_ids = set()
                    jdk17_node_map = {node['id']: node for node in jdk17_nodes}
                    jdk8_node_map = {node['id']: node for node in jdk8_nodes}
                    
                    # 收集所有节点ID
                    all_node_ids.update(jdk17_node_map.keys())
                    all_node_ids.update(jdk8_node_map.keys())
                    
                    print(f"   总共需要测试 {len(all_node_ids)} 个唯一节点")
                    
                    # 3.4 按API返回的原始顺序测试节点
                    def get_nodes_in_api_order(jdk17_nodes, jdk8_nodes):
                        """按API返回的原始顺序获取节点列表"""
                        # 优先使用JDK17的顺序，如果没有则使用JDK8的顺序
                        primary_nodes = jdk17_nodes if jdk17_nodes else jdk8_nodes
                        secondary_nodes = jdk8_nodes if jdk17_nodes else jdk17_nodes
                        
                        ordered_node_ids = []
                        processed_ids = set()
                        
                        # 按主要节点列表的顺序添加
                        for node in primary_nodes:
                            ordered_node_ids.append(node['id'])
                            processed_ids.add(node['id'])
                        
                        # 添加主要列表中没有的节点
                        for node in secondary_nodes:
                            if node['id'] not in processed_ids:
                                ordered_node_ids.append(node['id'])
                                processed_ids.add(node['id'])
                        
                        return ordered_node_ids
                    
                    ordered_node_ids = get_nodes_in_api_order(jdk17_nodes, jdk8_nodes)
                    
                    # 3.5 测试所有节点（完整覆盖）
                    tested_count = 0
                    for node_id in ordered_node_ids:
                        tested_count += 1
                        
                        # 获取节点信息
                        jdk17_node = jdk17_node_map.get(node_id)
                        jdk8_node = jdk8_node_map.get(node_id)
                        
                        # 确定节点名称和路径
                        if jdk17_node:
                            node_name = jdk17_node['path']
                        elif jdk8_node:
                            node_name = jdk8_node['path']
                        else:
                            node_name = f"Unknown Node (ID: {node_id})"
                        
                        print(f"   3.{tested_count} 测试节点: {node_name} (ID: {node_id})")
                        
                        # 获取内容数据
                        jdk17_content = None
                        jdk8_content = None
                        
                        if jdk17_node:
                            jdk17_content = self.get_column_content(
                                self.jdk17_config, self.jdk17_token, node_id
                            )
                        
                        if jdk8_node:
                            jdk8_content = self.get_column_content(
                                self.jdk8_config, self.jdk8_token, node_id
                            )
                        
                        # 提取数据列表
                        jdk17_data_list = []
                        jdk8_data_list = []
                        
                        if jdk17_content and jdk17_content.get('content', {}).get('dataList'):
                            jdk17_data_list = jdk17_content['content']['dataList']
                        
                        if jdk8_content and jdk8_content.get('content', {}).get('dataList'):
                            jdk8_data_list = jdk8_content['content']['dataList']
                        
                        # 比较数据
                        result = self.compare_data_counts(
                            jdk17_data_list, jdk8_data_list, 
                            f"树形节点: {node_name}"
                        )
                        self.comparison_results.append(result)
                        
                        # 显示结果
                        status_msg = "PASS" if result['status'] == 'PASS' else "DIFF"
                        print(f"         JDK17: {result['jdk17_count']}, JDK8: {result['jdk8_count']}, 差异: {result['difference']:+d} [{status_msg}]")
                        
                        # 添加延迟避免请求过快
                        time.sleep(0.5)
                        
                except Exception as e:
                    print(f"   树形结构测试失败: {e}")
            else:
                print("   跳过树形结构测试 - 缺少必要的tokens")
            
            # 4. 生成报告
            self.generate_report()
            
        except Exception as e:
            print(f"测试过程中发生错误: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def generate_report(self):
        """生成对比报告"""
        print("\n" + "=" * 60)
        print("测试完成，生成对比报告...")
        
        if not self.comparison_results:
            print("没有可用的测试结果生成报告")
            return
        
        # 创建DataFrame
        df = pd.DataFrame(self.comparison_results)
        
        # 保存详细报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"HTML_Data_Comparison_Report_{timestamp}.md"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("# HTML数据比对测试报告\n\n")
            f.write(f"**测试时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**JDK17版本API:** {self.jdk17_config['API_BASE_URL']}\n")
            f.write(f"**JDK8版本API:** {self.jdk8_config['API_BASE_URL']}\n\n")
            
            f.write("## 测试概述\n\n")
            total_tests = len(self.comparison_results)
            passed_tests = len([r for r in self.comparison_results if r['status'] == 'PASS'])
            failed_tests = total_tests - passed_tests
            
            f.write(f"- **总测试项:** {total_tests}\n")
            f.write(f"- **通过测试:** {passed_tests}\n")
            f.write(f"- **差异测试:** {failed_tests}\n")
            f.write(f"- **通过率:** {(passed_tests/total_tests*100):.1f}%\n\n")
            
            f.write("## 详细测试结果\n\n")
            f.write("| 测试项目 | JDK17数量 | JDK8数量 | 差异 | 状态 |\n")
            f.write("|---------|-----------|------------|------|------|\n")
            
            # 按测试执行的原始顺序显示结果（保持API返回的顺序）
            sorted_results = self.comparison_results
            
            for result in sorted_results:
                status_icon = "✅" if result['status'] == 'PASS' else "❌"
                f.write(f"| {result['test_name']} | {result['jdk17_count']} | {result['jdk8_count']} | {result['difference']:+d} | {status_icon} {result['status']} |\n")
            
            f.write("\n## 差异分析\n\n")
            
            # 按钮测试差异
            button_results = [r for r in self.comparison_results if '按钮' in r['test_name']]
            if button_results:
                f.write("### 按钮功能差异\n\n")
                for result in button_results:
                    if result['status'] == 'DIFF':
                        f.write(f"- **{result['test_name']}:** JDK17版本比JDK8版本{'多' if result['difference'] > 0 else '少'}{abs(result['difference'])}个数据项\n")
            
            # 树形节点差异
            tree_results = [r for r in self.comparison_results if '树形节点' in r['test_name']]
            if tree_results:
                f.write("\n### 树形节点差异\n\n")
                diff_nodes = [r for r in tree_results if r['status'] == 'DIFF']
                if diff_nodes:
                    for result in diff_nodes:
                        f.write(f"- **{result['test_name']}:** JDK17版本比JDK8版本{'多' if result['difference'] > 0 else '少'}{abs(result['difference'])}个数据项\n")
                else:
                    f.write("所有树形节点数据一致，无差异。\n")
            
            f.write("\n## 统计分析\n\n")
            
            # 按类型统计
            button_results = [r for r in self.comparison_results if '按钮' in r['test_name']]
            tree_results = [r for r in self.comparison_results if '树形节点' in r['test_name']]
            
            f.write(f"- **按钮功能测试:** {len(button_results)} 项\n")
            f.write(f"- **树形节点测试:** {len(tree_results)} 项\n")
            
            # 差异统计
            diff_results = [r for r in self.comparison_results if r['status'] == 'DIFF']
            if diff_results:
                jdk17_more = [r for r in diff_results if r['difference'] > 0]
                jdk8_more = [r for r in diff_results if r['difference'] < 0]
                
                f.write(f"- **数据完全一致的项目:** {passed_tests} 项\n")
                f.write(f"- **JDK17数据更多的项目:** {len(jdk17_more)} 项\n")
                f.write(f"- **JDK8数据更多的项目:** {len(jdk8_more)} 项\n")
                
                if jdk17_more:
                    avg_jdk17_more = sum(r['difference'] for r in jdk17_more) / len(jdk17_more)
                    f.write(f"- **JDK17多出数据的平均值:** {avg_jdk17_more:.1f}\n")
                
                if jdk8_more:
                    avg_jdk8_more = sum(abs(r['difference']) for r in jdk8_more) / len(jdk8_more)
                    f.write(f"- **JDK8多出数据的平均值:** {avg_jdk8_more:.1f}\n")
            
            f.write("\n## 结论\n\n")
            if failed_tests == 0:
                f.write("✅ **所有测试通过！** JDK17版本与JDK8版本的数据完全一致。\n")
            else:
                f.write(f"⚠️ **发现 {failed_tests} 项差异。** 需要进一步分析差异原因。\n\n")
                
                f.write("**可能的差异原因：**\n")
                f.write("1. **API版本差异** - JDK17版本可能使用了不同的API逻辑\n")
                f.write("2. **配置参数差异** - 两个版本的默认配置可能不同\n")
                f.write("3. **数据源差异** - 可能连接到不同的数据库或缓存\n")
                f.write("4. **缓存机制差异** - 缓存策略或过期时间不同\n")
                f.write("5. **算法优化** - 推荐算法或数据筛选逻辑的改进\n\n")
                
                f.write("**建议的后续行动：**\n")
                f.write("1. 检查两个版本的配置文件差异\n")
                f.write("2. 对比API响应的详细内容，不仅仅是数量\n")
                f.write("3. 验证数据源的一致性\n")
                f.write("4. 检查是否存在时间相关的数据变化\n")
                f.write("5. 进行多次测试以确认差异的稳定性\n")
            
            f.write(f"\n---\n*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        print(f"\n[报告] 详细报告已保存到: {report_filename}")
        
        # 控制台输出摘要
        print("\n[摘要] 测试摘要:")
        print(f"   总测试项: {total_tests}")
        print(f"   通过测试: {passed_tests}")
        print(f"   差异测试: {failed_tests}")
        print(f"   通过率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n[差异] 发现差异的测试项:")
            for result in self.comparison_results:
                if result['status'] == 'DIFF':
                    print(f"   - {result['test_name']}: 差异 {result['difference']:+d}")

# 主执行函数
def main():
    """主执行函数"""
    comparator = HTMLDataComparator()
    comparator.run_comparison()

if __name__ == "__main__":
    main()