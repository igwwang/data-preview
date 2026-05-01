#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CDN可访问性测试脚本
用于检测API返回的icon和app下载链接是否可以正常访问
只下载前1MB数据以验证CDN可访问性
支持三种环境: prod, acc, dev
配置信息从对应的HTML文件中提取
"""

import requests
import json
import time
from urllib.parse import urlencode, urlparse
import hashlib
import hmac
import base64
from datetime import datetime
import urllib3
import socket
import re

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CDNAccessibilityTester:
    def __init__(self, environment='prod'):
        """
        初始化CDN可访问性测试器
        environment: 'prod', 'acc', 或 'dev'
        配置信息分别从 OS10-prod-QA.html, OS10-acc-QA.html, OS10-dev-QA.html 提取
        """
        # 根据环境选择配置
        if environment == 'prod':
            # 配置取自 OS10-prod-QA.html
            self.config = {
                'API_BASE_URL': 'https://saas.zeasn.tv',
                'ACCESS_KEY': '12205c45d719594b2c88c76c0ff4df13c2',
                'SECRET_KEY': '12d9b9ae08be0542e7898d24de30c5d648',
                'DEFAULT_PARAMS': {
                    'productId': 'wtv10',
                    'brandId': '19',
                    'deviceSetId': '10bfa24f235519482a8b9b1c2ad7a3aef6',
                    'deviceType': 'WHALEOS_CTV_KTC_AML950D4_2K_MTP_P31',
                    'countryCode': 'US',
                    'langCode': 'en',
                    'mac': 'A8%3A2C%3A3E%3A72%3AEC%3A4C',
                    'functionType': 'TvLauncher',
                    'ifGetTvDetail': '1',
                    'iconResolution': '320*180',
                    'terminalType': 'TV',
                    'sn': '',
                    'appVersion': '2000800',
                    'androidVersion': '13',
                    'osType': 'AOSP',
                    'clientIp': '45.86.202.30'  # Germany
                }
            }
        elif environment == 'acc':
            # 配置取自 OS10-acc-QA.html
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
                    'clientIp': '45.86.202.30'  # Germany
                }
            }
        else:  # dev
            # 配置取自 OS10-dev-QA.html
            self.config = {
                'API_BASE_URL': 'https://dev-saas.zeasn.tv',
                'ACCESS_KEY': '10353c6d999f4141bbb35dcc70ed08e0e6',
                'SECRET_KEY': '10e643bd7c7df54073ab333c6309926337',
                'DEFAULT_PARAMS': {
                    'productId': 'wtv10',
                    'brandId': '7',
                    'deviceSetId': '10bfa24f235519482a8b9b1c2ad7a3aef6',
                    'deviceType': 'WHALEOS10_Zeasn_Test_AML962D4',
                    'countryCode': 'AU',
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
                    'clientIp': '122.10.101.131'  # Hong Kong
                }
            }
        
        self.environment = environment
        self.token = None
        self.user_token = None
        self.test_results = []
        self.max_retries = 3
        self.retry_delay = 2
        self.MAX_DOWNLOAD_SIZE = 1024 * 1024  # 1MB
        
        # 需要检查的API接口（用于提取icon）
        self.api_endpoints = [
            {
                'name': '个性化推荐',
                'url_template': '/sp/api/device/v1/video/recommend?token={token}&userToken={user_token}&videoType=MOVIE&size={size}&needPoster=true&imgStyle=0&imgWidth=800',
                'size': 30,
                'icon_fields': ['icon', 'poster']
            },
            {
                'name': 'Banner AD推荐',
                'url_template': '/sp/api/device/v1/video/recommend/ad?token={token}&searchType=REC_CHANNEL,VOD&size={size}&scopeId=3&typeWeight=100,100&supportAD=true&moreFields=description,tags,source,background,cover&posterShape&posterWidth&posterHeight&iconShape&iconWidth&iconHeight&position=LAUNCHER&userToken={user_token}',
                'size': 5,
                'icon_fields': ['icon', 'poster', 'cover', 'background']
            },
            {
                'name': '新个性化推荐',
                'url_template': '/sp/api/device/v1/video/recommend/choices?token={token}&objectTypes=REC_CHANNEL,REC_PROGRAM,MOVIE,SEASON&size={size}&moreFields=description,backgroud,releaseTime,categories,scores,contributors,bindSource,views,source,tags,rating,defaultLangCode,updateTime,series,seasonNumber,episodeCount,duration,liveStartTime,liveEndTime,liveState&posterShape&posterWidth&posterHeight&iconShape=HORIZONTAL&iconWidth&iconHeight&userToken={user_token}',
                'size': 30,
                'icon_fields': ['icon', 'poster']
            },
            {
                'name': '栏目列表',
                'url_template': '/sp/api/device/v1/column?token={token}',
                'size': None,
                'icon_fields': ['icon']
            }
        ]
    
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
        response = self._make_request_with_retry('post', url, headers=headers, data=params)
        
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
        response = self._make_request_with_retry('post', url, headers=headers, data=urlencode(params))
        
        result = response.json()
        if result.get('errorCode') != "0":
            raise Exception(f"Failed to get user token: {result.get('errorMsg', 'Unknown error')}")
        
        user_token = result['data']['userToken']
        print(f"成功获取用户token: {user_token[:20]}...")
        return user_token
    
    def _make_request_with_retry(self, method, url, **kwargs):
        """带重试机制的请求"""
        for attempt in range(self.max_retries):
            try:
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
                        return response
                        
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
    
    def _extract_urls_from_data(self, data, fields):
        """从数据中提取指定字段的URL"""
        urls = []
        
        def extract(item, parent_name=""):
            if isinstance(item, dict):
                for key, value in item.items():
                    field_name = f"{parent_name}.{key}" if parent_name else key
                    if key in fields and isinstance(value, str) and value.startswith('http'):
                        urls.append({'url': value, 'field': field_name})
                    elif isinstance(value, (dict, list)):
                        extract(value, field_name)
            elif isinstance(item, list):
                for i, element in enumerate(item):
                    extract(element, f"{parent_name}[{i}]")
        
        extract(data)
        return urls
    
    def _test_url_accessibility(self, url, test_type='icon', vs_id=None):
        """测试URL的可访问性，只下载前1MB"""
        result = {
            'url': url,
            'test_type': test_type,
            'vs_id': vs_id,
            'status': 'PASS',
            'http_status': None,
            'downloaded_bytes': 0,
            'response_time': 0,
            'error_message': None,
            'cdn_domain': None
        }
        
        try:
            # 解析CDN域名
            parsed = urlparse(url)
            result['cdn_domain'] = parsed.netloc
            
            start_time = time.time()
            
            if test_type == 'download':
                # 获取重定向的Location
                response = self._make_request_with_retry('get', url, allow_redirects=False)
                result['http_status'] = response.status_code
                
                if response.status_code in [301, 302]:
                    location = response.headers.get('Location')
                    if location:
                        result['url'] = location
                        result['cdn_domain'] = urlparse(location).netloc
                        # 测试实际下载链接（只下载1MB）
                        download_response = requests.get(
                            location,
                            headers={'Range': f'bytes=0-{self.MAX_DOWNLOAD_SIZE - 1}'},
                            verify=False,
                            timeout=30,
                            stream=True
                        )
                        result['http_status'] = download_response.status_code
                        
                        if download_response.status_code in [200, 206]:
                            downloaded = 0
                            for chunk in download_response.iter_content(chunk_size=65536):
                                if chunk:
                                    downloaded += len(chunk)
                                    if downloaded >= self.MAX_DOWNLOAD_SIZE:
                                        break
                            result['downloaded_bytes'] = downloaded
                        else:
                            result['status'] = 'FAIL'
                            result['error_message'] = f"下载链接HTTP错误: {download_response.status_code}"
                    else:
                        result['status'] = 'FAIL'
                        result['error_message'] = "未找到Location重定向头"
                else:
                    result['status'] = 'FAIL'
                    result['error_message'] = f"预期301/302重定向，实际: {response.status_code}"
            
            else:
                # 测试icon等静态资源（只下载1MB）
                response = requests.get(
                    url,
                    headers={'Range': f'bytes=0-{self.MAX_DOWNLOAD_SIZE - 1}'},
                    verify=False,
                    timeout=30,
                    stream=True
                )
                result['http_status'] = response.status_code
                
                if response.status_code in [200, 206]:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=65536):
                        if chunk:
                            downloaded += len(chunk)
                            if downloaded >= self.MAX_DOWNLOAD_SIZE:
                                break
                    result['downloaded_bytes'] = downloaded
                else:
                    result['status'] = 'FAIL'
                    result['error_message'] = f"HTTP错误: {response.status_code}"
            
            result['response_time'] = time.time() - start_time
            
        except Exception as e:
            result['status'] = 'FAIL'
            result['error_message'] = str(e)
        
        return result
    
    def test_icons_from_api(self):
        """测试所有API返回的icon可访问性"""
        print("\n测试API返回的icon可访问性...")
        icon_test_results = []
        
        for endpoint in self.api_endpoints:
            print(f"  检查API: {endpoint['name']}")
            
            try:
                # 构建URL
                if endpoint['size']:
                    url = self.config['API_BASE_URL'] + endpoint['url_template'].format(
                        token=self.token,
                        user_token=self.user_token,
                        size=endpoint['size']
                    )
                else:
                    url = self.config['API_BASE_URL'] + endpoint['url_template'].format(
                        token=self.token,
                        user_token=self.user_token
                    )
                
                # 获取API数据
                response = self._make_request_with_retry('get', url)
                result = response.json()
                
                if result.get('errorCode') != 0:
                    icon_test_results.append({
                        'api_name': endpoint['name'],
                        'url': url,
                        'status': 'API_ERROR',
                        'error_message': result.get('errorMsg', 'API调用失败')
                    })
                    continue
                
                # 提取所有icon URL
                data = result.get('data', [])
                urls = self._extract_urls_from_data(data, endpoint['icon_fields'])
                
                print(f"    发现 {len(urls)} 个URL需要测试")
                
                # 测试每个URL
                for url_info in urls:
                    test_result = self._test_url_accessibility(url_info['url'], test_type='icon')
                    test_result['api_name'] = endpoint['name']
                    test_result['field'] = url_info['field']
                    icon_test_results.append(test_result)
                    
                    status_icon = "✅" if test_result['status'] == 'PASS' else "❌"
                    print(f"      {status_icon} {test_result['cdn_domain']} - {test_result['url'][:60]}...")
                    
                    time.sleep(0.2)  # 避免请求过快
            
            except Exception as e:
                icon_test_results.append({
                    'api_name': endpoint['name'],
                    'url': url if 'url' in locals() else 'URL构建失败',
                    'status': 'REQUEST_ERROR',
                    'error_message': str(e)
                })
        
        self.test_results.extend(icon_test_results)
        return icon_test_results
    
    def test_app_download_links(self):
        """测试app下载链接的可访问性"""
        print("\n测试app下载链接可访问性...")
        download_test_results = []
        
        # 获取栏目内容中的应用信息
        try:
            # 获取栏目列表
            url = f"{self.config['API_BASE_URL']}/sp/api/device/v1/column?token={self.token}"
            response = self._make_request_with_retry('get', url)
            columns = response.json()
            
            if columns.get('errorCode') != 0:
                download_test_results.append({
                    'api_name': 'App下载测试',
                    'url': url,
                    'status': 'API_ERROR',
                    'error_message': columns.get('errorMsg', '获取栏目列表失败')
                })
                self.test_results.extend(download_test_results)
                return download_test_results
            
            # 提取所有叶子节点
            def extract_leaf_nodes(data):
                nodes = []
                for item in data:
                    if item.get('children'):
                        nodes.extend(extract_leaf_nodes(item['children']))
                    else:
                        nodes.append(item)
                return nodes
            
            leaf_nodes = extract_leaf_nodes(columns.get('data', []))
            print(f"    发现 {len(leaf_nodes)} 个栏目节点")
            
            # 检查每个栏目内容中的应用
            tested_vs_ids = set()
            
            for node in leaf_nodes:
                try:
                    content_url = f"{self.config['API_BASE_URL']}/sp/api/device/v1/column/content?token={self.token}&columnIds={node['id']}"
                    content_response = self._make_request_with_retry('get', content_url)
                    content_result = content_response.json()
                    
                    if content_result.get('errorCode') != 0:
                        continue
                    
                    content_data = content_result.get('data', [])
                    if content_data:
                        data_list = content_data[0].get('content', {}).get('dataList', [])
                        
                        for item in data_list:
                            vs_id = item.get('vsId')
                            if vs_id and vs_id not in tested_vs_ids:
                                tested_vs_ids.add(vs_id)
                                download_url = f"{self.config['API_BASE_URL']}/sp/api/device/v1/app/download?token={self.token}&vsId={vs_id}"
                                
                                print(f"    测试下载链接 vsId={vs_id}")
                                test_result = self._test_url_accessibility(download_url, test_type='download', vs_id=vs_id)
                                test_result['api_name'] = 'App下载'
                                test_result['original_url'] = download_url
                                download_test_results.append(test_result)
                                
                                status_icon = "✅" if test_result['status'] == 'PASS' else "❌"
                                print(f"      {status_icon} {test_result.get('cdn_domain', 'N/A')}")
                                
                                time.sleep(0.5)  # 避免请求过快
                                
                        if len(tested_vs_ids) >= 10:  # 最多测试10个下载链接
                            print("    已测试10个下载链接，停止继续测试")
                            break
                
                except Exception as e:
                    print(f"    检查栏目 {node.get('name', 'Unknown')} 时出错: {e}")
                    continue
            
        except Exception as e:
            download_test_results.append({
                'api_name': 'App下载测试',
                'url': url if 'url' in locals() else 'URL构建失败',
                'status': 'REQUEST_ERROR',
                'error_message': str(e)
            })
        
        self.test_results.extend(download_test_results)
        return download_test_results
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("CDN可访问性测试完成，生成报告...")
        
        if not self.test_results:
            print("没有可用的测试结果")
            return
        
        # 统计结果
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = total_tests - passed_tests
        
        # 按类型统计
        icon_tests = [r for r in self.test_results if r.get('test_type') == 'icon']
        download_tests = [r for r in self.test_results if r.get('test_type') == 'download']
        
        icon_passed = len([r for r in icon_tests if r['status'] == 'PASS'])
        download_passed = len([r for r in download_tests if r['status'] == 'PASS'])
        
        # 生成报告文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"CDN_Accessibility_Report_{self.environment}_{timestamp}.md"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("# CDN可访问性测试报告\n\n")
            f.write(f"**测试时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**测试环境:** {self.environment.upper()}\n")
            f.write(f"**API服务器:** {self.config['API_BASE_URL']}\n\n")
            
            f.write("## 测试概述\n\n")
            f.write(f"- **总测试项:** {total_tests}\n")
            f.write(f"- **通过测试:** {passed_tests}\n")
            f.write(f"- **失败测试:** {failed_tests}\n")
            f.write(f"- **通过率:** {(passed_tests/total_tests*100):.1f}%\n\n")
            
            f.write("### 按类型统计\n\n")
            f.write(f"- **Icon测试:** {len(icon_tests)} 项 ({icon_passed} 通过)\n")
            f.write(f"- **下载链接测试:** {len(download_tests)} 项 ({download_passed} 通过)\n\n")
            
            f.write("## 详细测试结果\n\n")
            
            # Icon测试结果
            if icon_tests:
                f.write("### Icon可访问性测试\n\n")
                f.write("| API接口 | 字段 | CDN域名 | HTTP状态 | 下载字节数 | 响应时间 | 状态 | 错误信息 |\n")
                f.write("|---------|------|---------|----------|------------|----------|------|----------|\n")
                
                for result in icon_tests:
                    status_icon = "✅" if result['status'] == 'PASS' else "❌"
                    error_msg = result.get('error_message', '') or '-'
                    f.write(f"| {result.get('api_name', '-')} | {result.get('field', '-')} | {result.get('cdn_domain', '-')} | {result.get('http_status', '-')} | {result.get('downloaded_bytes', 0)} | {result.get('response_time', 0):.2f}s | {status_icon} | {error_msg} |\n")
            
            # 下载链接测试结果
            if download_tests:
                f.write("\n### App下载链接测试\n\n")
                f.write("| vsId | CDN域名 | HTTP状态 | 下载字节数 | 响应时间 | 状态 | 错误信息 |\n")
                f.write("|------|---------|----------|------------|----------|------|----------|\n")
                
                for result in download_tests:
                    status_icon = "✅" if result['status'] == 'PASS' else "❌"
                    error_msg = result.get('error_message', '') or '-'
                    f.write(f"| {result.get('vs_id', '-')} | {result.get('cdn_domain', '-')} | {result.get('http_status', '-')} | {result.get('downloaded_bytes', 0)} | {result.get('response_time', 0):.2f}s | {status_icon} | {error_msg} |\n")
            
            # 问题分析
            f.write("\n## 问题分析\n\n")
            failed_results = [r for r in self.test_results if r['status'] != 'PASS']
            
            if failed_results:
                f.write("### 失败的测试项\n\n")
                for result in failed_results:
                    f.write(f"- **{result.get('api_name', 'Unknown')}:** {result.get('url', '')[:80]}...\n")
                    f.write(f"  - 状态: {result['status']}\n")
                    f.write(f"  - 错误: {result.get('error_message', 'Unknown')}\n\n")
            else:
                f.write("✅ **所有测试项都通过了！** CDN可访问性良好。\n\n")
            
            f.write("## CDN域名统计\n\n")
            domains = {}
            for result in self.test_results:
                domain = result.get('cdn_domain')
                if domain:
                    if domain not in domains:
                        domains[domain] = {'pass': 0, 'fail': 0}
                    if result['status'] == 'PASS':
                        domains[domain]['pass'] += 1
                    else:
                        domains[domain]['fail'] += 1
            
            if domains:
                f.write("| CDN域名 | 测试次数 | 通过次数 | 失败次数 | 通过率 |\n")
                f.write("|---------|----------|----------|----------|--------|\n")
                
                for domain, stats in domains.items():
                    total = stats['pass'] + stats['fail']
                    rate = (stats['pass'] / total * 100) if total > 0 else 0
                    f.write(f"| {domain} | {total} | {stats['pass']} | {stats['fail']} | {rate:.1f}% |\n")
            else:
                f.write("未检测到CDN域名\n")
            
            f.write(f"\n---\n*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        print(f"\n[REPORT] 详细报告已保存到: {report_filename}")
        
        # 控制台输出摘要
        print("\n[SUMMARY] CDN可访问性测试摘要:")
        print(f"   测试环境: {self.environment.upper()}")
        print(f"   总测试项: {total_tests}")
        print(f"   通过测试: {passed_tests}")
        print(f"   失败测试: {failed_tests}")
        print(f"   通过率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n[ISSUES] 发现问题的测试项:")
            for result in self.test_results:
                if result['status'] != 'PASS':
                    print(f"   - {result.get('api_name', 'Unknown')}: {result.get('url', '')[:60]}...")
                    if result.get('error_message'):
                        print(f"     错误: {result['error_message']}")
    
    def run_test(self):
        """运行完整的CDN可访问性测试"""
        print(f"开始CDN可访问性测试 ({self.environment.upper()}环境)...")
        print("=" * 60)
        
        try:
            # 1. 获取认证tokens
            print("1. 获取认证tokens...")
            self.token = self.get_token()
            self.user_token = self.get_user_token()
            
            # 2. 测试API返回的icon可访问性
            print("\n2. 测试API返回的icon可访问性...")
            self.test_icons_from_api()
            
            # 3. 测试app下载链接可访问性
            print("\n3. 测试app下载链接可访问性...")
            self.test_app_download_links()
            
            # 4. 生成报告
            self.generate_report()
            
        except Exception as e:
            print(f"测试过程中发生错误: {str(e)}")
            import traceback
            traceback.print_exc()

def main():
    """主执行函数"""
    import sys
    
    environment = 'prod'  # 默认使用prod环境
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['prod', 'acc', 'dev']:
            environment = sys.argv[1].lower()
        else:
            print("使用方法: python cdn_accessibility_tester.py [prod|acc|dev]")
            print("默认使用prod环境")
    
    tester = CDNAccessibilityTester(environment)
    tester.run_test()

if __name__ == "__main__":
    main()