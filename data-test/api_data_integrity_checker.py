#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备数据完整性检查脚本
基于html_data_comparator.py裁剪并扩展，用于检查单个设备的数据完整性
检查接口返回数量是否符合预期，生成完整的数据完整性报告
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
import re

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DeviceDataIntegrityChecker:
    def __init__(self, config_type='jdk8'):
        """
        初始化数据完整性检查器
        config_type: 'jdk17' 或 'jdk8'
        """
        # 配置选择
        if config_type == 'jdk17':
            self.config = {
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
        else:  # jdk8
            self.config = {
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
        
        self.config_type = config_type
        self.token = None
        self.user_token = None
        self.integrity_results = []
        self.max_retries = 3
        self.retry_delay = 2
        
        # 定义需要检查的API接口及其预期数量参数
        self.api_endpoints = [
            {
                'name': '个性化推荐',
                'url_template': '/sp/api/device/v1/video/recommend?token={token}&userToken={user_token}&videoType=MOVIE&size={size}&needPoster=true&imgStyle=0&imgWidth=800',
                'expected_size': 30,
                'has_size_param': True,
                'data_path': 'data'
            },
            {
                'name': 'Banner AD推荐',
                'url_template': '/sp/api/device/v1/video/recommend/ad?token={token}&searchType=REC_CHANNEL,VOD&size={size}&scopeId=3&typeWeight=100,100&supportAD=true&moreFields=description,tags,source,background,cover&posterShape&posterWidth&posterHeight&iconShape&iconWidth&iconHeight&position=LAUNCHER&userToken={user_token}',
                'expected_size': 1,
                'has_size_param': True,
                'data_path': 'data'
            },
            {
                'name': '新个性化推荐',
                'url_template': '/sp/api/device/v1/video/recommend/choices?token={token}&objectTypes=REC_CHANNEL,REC_PROGRAM,MOVIE,SEASON&size={size}&moreFields=description,backgroud,releaseTime,categories,scores,contributors,bindSource,views,source,tags,rating,defaultLangCode,updateTime,series,seasonNumber,episodeCount,duration,liveStartTime,liveEndTime,liveState&posterShape&posterWidth&posterHeight&iconShape=HORIZONTAL&iconWidth&iconHeight&userToken={user_token}',
                'expected_size': 30,
                'has_size_param': True,
                'data_path': 'data'
            },
            {
                'name': '栏目列表',
                'url_template': '/sp/api/device/v1/column?token={token}',
                'expected_size': None,  # 不支持size参数，只检查>0
                'has_size_param': False,
                'data_path': 'data'
            }
        ]
    
    def check_network_connectivity(self, url):
        """检查网络连接"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
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
                
                kwargs.setdefault('timeout', 30)
                kwargs.setdefault('verify', False)
                
                if method.lower() == 'get':
                    response = requests.get(url, **kwargs)
                elif method.lower() == 'post':
                    response = requests.post(url, **kwargs)
                else:
                    raise ValueError(f"不支持的HTTP方法: {method}")
                
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
    
    def get_token(self):
        """获取认证token"""
        print(f"获取token from {self.config['API_BASE_URL']}")
        
        if not self.check_network_connectivity(self.config['API_BASE_URL']):
            raise Exception(f"无法连接到服务器: {self.config['API_BASE_URL']}")
        
        params = urlencode(self.config['DEFAULT_PARAMS'])
        
        headers = {
            'Authorization': self.generate_authorization_header(
                '/auth-api/api/v1/auth/deviceSign',
                self.config['SECRET_KEY'],
                self.config['ACCESS_KEY']
            ),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        url = f"{self.config['API_BASE_URL']}/auth-api/api/v1/auth/deviceSign"
        response = self.make_request_with_retry('post', url, headers=headers, data=params)
        
        result = response.json()
        if result.get('errorCode') != "0":
            raise Exception(f"Failed to get token: {result.get('errorMsg', 'Unknown error')}")
        
        token = result['data']['token']
        print(f"成功获取token: {token[:20]}...")
        return token
    
    def get_user_token(self):
        """获取用户token"""
        print(f"获取用户token from {self.config['API_BASE_URL']}")
        
        params = {
            'productId': self.config['DEFAULT_PARAMS']['productId'],
            'brandId': self.config['DEFAULT_PARAMS']['brandId'],
            'deviceSetId': '',
            'mac': self.config['DEFAULT_PARAMS']['mac'],
            'deviceType': self.config['DEFAULT_PARAMS']['deviceType'],
            'deviceName': ''
        }
        
        headers = {
            'Authorization': self.generate_authorization_header(
                '/user/device/login',
                self.config['SECRET_KEY'],
                self.config['ACCESS_KEY']
            ),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        url = f"{self.config['API_BASE_URL']}/user/device/login"
        response = self.make_request_with_retry('post', url, headers=headers, data=urlencode(params))
        
        result = response.json()
        if result.get('errorCode') != "0":
            raise Exception(f"Failed to get user token: {result.get('errorMsg', 'Unknown error')}")
        
        user_token = result['data']['userToken']
        print(f"成功获取用户token: {user_token[:20]}...")
        return user_token
    
    def extract_size_from_url(self, url):
        """从URL中提取size参数值"""
        match = re.search(r'size=(\d+)', url)
        return int(match.group(1)) if match else None
    
    def get_nested_data(self, data, path):
        """根据路径获取嵌套数据"""
        if not path:
            return data
        
        keys = path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current
    
    def check_api_integrity(self, endpoint_config):
        """检查单个API接口的数据完整性"""
        api_name = endpoint_config['name']
        print(f"检查API: {api_name}")
        
        try:
            # 构建URL
            if endpoint_config['has_size_param']:
                url = self.config['API_BASE_URL'] + endpoint_config['url_template'].format(
                    token=self.token,
                    user_token=self.user_token,
                    size=endpoint_config['expected_size']
                )
            else:
                url = self.config['API_BASE_URL'] + endpoint_config['url_template'].format(
                    token=self.token,
                    user_token=self.user_token
                )
            
            # 发送请求
            response = self.make_request_with_retry('get', url)
            result = response.json()
            
            # 检查API响应状态
            if result.get('errorCode') != 0:
                return {
                    'api_name': api_name,
                    'status': 'API_ERROR',
                    'expected_count': endpoint_config['expected_size'],
                    'actual_count': 0,
                    'error_message': result.get('errorMsg', 'Unknown API error'),
                    'url': url
                }
            
            # 提取数据
            data = self.get_nested_data(result, endpoint_config['data_path'])
            actual_count = len(data) if data and isinstance(data, list) else 0
            
            # 检查数据完整性
            if endpoint_config['has_size_param']:
                expected_count = endpoint_config['expected_size']
                if actual_count == expected_count:
                    status = 'PASS'
                    error_message = None
                else:
                    status = 'COUNT_MISMATCH'
                    error_message = f"期望{expected_count}个，实际返回{actual_count}个"
            else:
                # 不支持size参数的接口，只检查是否>0
                expected_count = '>0'
                if actual_count > 0:
                    status = 'PASS'
                    error_message = None
                else:
                    status = 'EMPTY_DATA'
                    error_message = f"期望>0个数据，实际返回{actual_count}个"
            
            return {
                'api_name': api_name,
                'status': status,
                'expected_count': expected_count,
                'actual_count': actual_count,
                'error_message': error_message,
                'url': url,
                'response_time': response.elapsed.total_seconds()
            }
            
        except Exception as e:
            return {
                'api_name': api_name,
                'status': 'REQUEST_ERROR',
                'expected_count': endpoint_config['expected_size'],
                'actual_count': 0,
                'error_message': str(e),
                'url': url if 'url' in locals() else 'URL构建失败'
            }
    
    def check_column_content_integrity(self):
        """检查栏目内容的数据完整性"""
        print("检查栏目内容数据完整性...")
        
        try:
            # 获取栏目列表
            url = f"{self.config['API_BASE_URL']}/sp/api/device/v1/column?token={self.token}"
            response = self.make_request_with_retry('get', url)
            result = response.json()
            
            if result.get('errorCode') != 0:
                return [{
                    'api_name': '栏目内容检查',
                    'status': 'API_ERROR',
                    'expected_count': '>0',
                    'actual_count': 0,
                    'error_message': result.get('errorMsg', 'Unknown error'),
                    'url': url
                }]
            
            columns = result.get('data', [])
            column_results = []
            
            # 提取所有叶子节点
            def extract_leaf_nodes(data, parent_path=""):
                nodes = []
                for item in data:
                    current_path = f"{parent_path}/{item['name']}" if parent_path else item['name']
                    
                    if item.get('children'):
                        nodes.extend(extract_leaf_nodes(item['children'], current_path))
                    else:
                        nodes.append({
                            'id': item['id'],
                            'name': item['name'],
                            'path': current_path
                        })
                return nodes
            
            leaf_nodes = extract_leaf_nodes(columns)
            print(f"发现 {len(leaf_nodes)} 个栏目节点需要检查")
            
            # 提取所有叶子节点
            def extract_leaf_nodes(data, parent_path=""):
                nodes = []
                for item in data:
                    current_path = f"{parent_path}/{item['name']}" if parent_path else item['name']
                    
                    if item.get('children'):
                        nodes.extend(extract_leaf_nodes(item['children'], current_path))
                    else:
                        nodes.append({
                            'id': item['id'],
                            'name': item['name'],
                            'path': current_path
                        })
                return nodes
            
            # 检查每个栏目节点的内容
            for i, node in enumerate(leaf_nodes):  # 检查所有节点
                print(f"  检查栏目 {i+1}/{len(leaf_nodes)}: {node['path']}")
                
                try:
                    content_url = f"{self.config['API_BASE_URL']}/sp/api/device/v1/column/content?token={self.token}&columnIds={node['id']}"
                    content_response = self.make_request_with_retry('get', content_url)
                    content_result = content_response.json()
                    
                    if content_result.get('errorCode') != 0:
                        column_results.append({
                            'api_name': f"栏目内容: {node['path']}",
                            'status': 'API_ERROR',
                            'expected_count': '>0',
                            'actual_count': 0,
                            'error_message': content_result.get('errorMsg', 'Unknown error'),
                            'url': content_url
                        })
                        continue
                    
                    # 检查内容数据
                    content_data = content_result.get('data', [])
                    if content_data and len(content_data) > 0:
                        data_list = content_data[0].get('content', {}).get('dataList', [])
                        actual_count = len(data_list)
                        
                        if actual_count > 0:
                            status = 'PASS'
                            error_message = None
                        else:
                            status = 'EMPTY_DATA'
                            error_message = f"栏目内容为空"
                    else:
                        actual_count = 0
                        status = 'EMPTY_DATA'
                        error_message = f"栏目数据为空"
                    
                    column_results.append({
                        'api_name': f"栏目内容: {node['path']}",
                        'status': status,
                        'expected_count': '>0',
                        'actual_count': actual_count,
                        'error_message': error_message,
                        'url': content_url,
                        'response_time': content_response.elapsed.total_seconds()
                    })
                    
                    time.sleep(0.5)  # 避免请求过快
                    
                except Exception as e:
                    column_results.append({
                        'api_name': f"栏目内容: {node['path']}",
                        'status': 'REQUEST_ERROR',
                        'expected_count': '>0',
                        'actual_count': 0,
                        'error_message': str(e),
                        'url': content_url if 'content_url' in locals() else 'URL构建失败'
                    })
            
            return column_results
            
        except Exception as e:
            return [{
                'api_name': '栏目内容检查',
                'status': 'REQUEST_ERROR',
                'expected_count': '>0',
                'actual_count': 0,
                'error_message': str(e),
                'url': url if 'url' in locals() else 'URL构建失败'
            }]
    
    def run_integrity_check(self):
        """运行完整的数据完整性检查"""
        print(f"开始设备数据完整性检查 ({self.config_type.upper()})...")
        print("=" * 60)
        
        try:
            # 1. 获取认证tokens
            print("1. 获取认证tokens...")
            self.token = self.get_token()
            self.user_token = self.get_user_token()
            
            # 2. 检查主要API接口
            print("\n2. 检查主要API接口...")
            for endpoint in self.api_endpoints:
                result = self.check_api_integrity(endpoint)
                self.integrity_results.append(result)
                
                status_icon = "PASS" if result['status'] == 'PASS' else "FAIL"
                print(f"   [{status_icon}] {result['api_name']}: {result['status']}")
                if result['error_message']:
                    print(f"      错误: {result['error_message']}")
                
                time.sleep(1)  # 避免请求过快
            
            # 3. 检查栏目内容
            print("\n3. 检查栏目内容...")
            column_results = self.check_column_content_integrity()
            self.integrity_results.extend(column_results)
            
            # 显示栏目检查摘要
            column_pass = len([r for r in column_results if r['status'] == 'PASS'])
            column_total = len(column_results)
            print(f"   栏目内容检查: {column_pass}/{column_total} 通过")
            
            # 4. 生成报告
            self.generate_integrity_report()
            
        except Exception as e:
            print(f"数据完整性检查过程中发生错误: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def generate_integrity_report(self):
        """生成数据完整性报告"""
        print("\n" + "=" * 60)
        print("数据完整性检查完成，生成报告...")
        
        if not self.integrity_results:
            print("没有可用的检查结果生成报告")
            return
        
        # 统计结果
        total_checks = len(self.integrity_results)
        passed_checks = len([r for r in self.integrity_results if r['status'] == 'PASS'])
        failed_checks = total_checks - passed_checks
        
        # 生成报告文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"API_Data_Integrity_Report_{self.config_type}_{timestamp}.md"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("# API数据完整性检查报告\n\n")
            f.write(f"**检查时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**API服务器:** {self.config['API_BASE_URL']}\n")
            f.write(f"**配置类型:** {self.config_type.upper()}\n")
            f.write(f"**设备信息:** {self.config['DEFAULT_PARAMS']['deviceType']}\n\n")
            
            f.write("## 检查概述\n\n")
            f.write(f"- **总检查项:** {total_checks}\n")
            f.write(f"- **通过检查:** {passed_checks}\n")
            f.write(f"- **失败检查:** {failed_checks}\n")
            f.write(f"- **通过率:** {(passed_checks/total_checks*100):.1f}%\n\n")
            
            f.write("## 详细检查结果\n\n")
            f.write("| API接口 | 期望数量 | 实际数量 | 状态 | 错误信息 |\n")
            f.write("|---------|----------|----------|------|----------|\n")
            
            for result in self.integrity_results:
                status_icon = "✅" if result['status'] == 'PASS' else "❌"
                error_msg = result.get('error_message', '') or '-'
                f.write(f"| {result['api_name']} | {result['expected_count']} | {result['actual_count']} | {status_icon} {result['status']} | {error_msg} |\n")
            
            f.write("\n## 问题分析\n\n")
            
            # 按状态分类问题
            error_types = {}
            for result in self.integrity_results:
                if result['status'] != 'PASS':
                    status = result['status']
                    if status not in error_types:
                        error_types[status] = []
                    error_types[status].append(result)
            
            if error_types:
                for error_type, results in error_types.items():
                    f.write(f"### {error_type} ({len(results)}项)\n\n")
                    for result in results:
                        f.write(f"- **{result['api_name']}:** {result.get('error_message', '未知错误')}\n")
                    f.write("\n")
            else:
                f.write("✅ **所有检查项都通过了！** API数据完整性良好。\n\n")
            
            f.write("## 性能统计\n\n")
            
            # 响应时间统计
            response_times = [r.get('response_time', 0) for r in self.integrity_results if r.get('response_time')]
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                max_response_time = max(response_times)
                min_response_time = min(response_times)
                
                f.write(f"- **平均响应时间:** {avg_response_time:.2f}秒\n")
                f.write(f"- **最大响应时间:** {max_response_time:.2f}秒\n")
                f.write(f"- **最小响应时间:** {min_response_time:.2f}秒\n\n")
            
            f.write("## 建议\n\n")
            if failed_checks == 0:
                f.write("✅ **API数据完整性检查全部通过！**\n\n")
                f.write("**维护建议:**\n")
                f.write("1. 定期执行数据完整性检查\n")
                f.write("2. 监控API响应时间变化\n")
                f.write("3. 关注数据量的变化趋势\n")
            else:
                f.write("⚠️ **发现API数据完整性问题，需要关注！**\n\n")
                f.write("**修复建议:**\n")
                f.write("1. 检查网络连接和API服务状态\n")
                f.write("2. 验证API配置参数是否正确\n")
                f.write("3. 检查数据源和缓存状态\n")
                f.write("4. 联系技术支持进行深入排查\n")
            
            f.write(f"\n---\n*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        print(f"\n[REPORT] 详细报告已保存到: {report_filename}")
        
        # 控制台输出摘要
        print("\n[SUMMARY] 检查摘要:")
        print(f"   总检查项: {total_checks}")
        print(f"   通过检查: {passed_checks}")
        print(f"   失败检查: {failed_checks}")
        print(f"   通过率: {(passed_checks/total_checks*100):.1f}%")
        
        if failed_checks > 0:
            print("\n[ISSUES] 发现问题的检查项:")
            for result in self.integrity_results:
                if result['status'] != 'PASS':
                    print(f"   - {result['api_name']}: {result['status']}")

def main():
    """主执行函数"""
    import sys
    
    # 支持命令行参数选择配置类型
    config_type = 'jdk8'  # 默认使用jdk8
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['jdk8', 'jdk17']:
            config_type = sys.argv[1].lower()
        else:
            print("使用方法: python device_data_integrity_checker.py [jdk8|jdk17]")
            print("默认使用jdk8配置")
    
    checker = DeviceDataIntegrityChecker(config_type)
    checker.run_integrity_check()

if __name__ == "__main__":
    main()