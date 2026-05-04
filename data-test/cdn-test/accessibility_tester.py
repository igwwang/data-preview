#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可访问性验证模块
负责验证URL的可访问性
"""

import requests
import time
from urllib.parse import urlparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AccessibilityTester:
    def __init__(self, proxy: str = None):
        """
        初始化可访问性测试器
        :param proxy: 代理服务器地址，格式: http://host:port 或 https://host:port
        """
        self.max_retries = 3
        self.retry_delay = 2
        self.max_download_size = 8 * 1024  # 8KB
        self.timeout = 60  # 超时时间（秒）
        self.request_interval = 1.0  # 请求间隔时间（秒），限制每秒最多发起一次请求
        self.last_request_time = 0  # 上次请求时间
        
        # 代理配置
        self.proxies = {}
        if proxy:
            self.proxies = {
                'http': proxy,
                'https': proxy
            }
    
    def _rate_limit(self):
        """
        请求频率限制：确保每秒最多发起一次请求
        """
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.request_interval:
            time.sleep(self.request_interval - elapsed)
        self.last_request_time = time.time()

    def _make_request_with_retry(self, method: str, url: str, success_codes: list = None, **kwargs):
        """
        带重试机制的请求
        :param method: HTTP方法
        :param url: 请求URL
        :param success_codes: 成功状态码列表，默认为[200]
        :param kwargs: 请求参数
        """
        if success_codes is None:
            success_codes = [200]

        for attempt in range(self.max_retries):
            # 请求频率限制
            self._rate_limit()
            
            try:
                kwargs.setdefault('timeout', self.timeout)
                kwargs.setdefault('verify', False)
                if self.proxies:
                    kwargs.setdefault('proxies', self.proxies)
                else:
                    kwargs.setdefault('proxies', {'http': None, 'https': None})

                if method.lower() == 'get':
                    response = requests.get(url, **kwargs)
                elif method.lower() == 'post':
                    response = requests.post(url, **kwargs)
                else:
                    raise ValueError(f"不支持的HTTP方法: {method}")

                if response.status_code in success_codes:
                    return response
                else:
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        return response

            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise
            except Exception:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise

        raise Exception(f"重试{self.max_retries}次后仍然失败")

    def test_url(self, resource: dict) -> dict:
        """
        测试单个资源的可访问性
        :param resource: 资源字典，包含url, type, page_path, field, item_name, vs_id
        :return: 测试结果字典
        """
        url = resource.get('url', '')
        test_type = resource.get('type', 'image')
        page_path = resource.get('page_path', '')
        field = resource.get('field', '')
        item_name = resource.get('item_name', '')
        vs_id = resource.get('vs_id', None)

        result = {
            'url': url,
            'test_type': test_type,
            'page_path': page_path,
            'field': field,
            'item_name': item_name,
            'vs_id': vs_id,
            'status': 'PASS',
            'http_status': None,
            'downloaded_bytes': 0,
            'response_time': 0,
            'cdn_domain': None,
            'error_message': None
        }

        try:
            # 解析CDN域名
            parsed = urlparse(url)
            result['cdn_domain'] = parsed.netloc

            start_time = time.time()

            if test_type == 'download':
                # 下载链接需要先获取重定向，接受301/302状态码
                response = self._make_request_with_retry('get', url, success_codes=[301, 302], allow_redirects=False)
                result['http_status'] = response.status_code

                if response.status_code in [301, 302]:
                    location = response.headers.get('Location')
                    if location:
                        result['url'] = location
                        result['cdn_domain'] = urlparse(location).netloc
                        # 测试实际下载链接（只下载1MB）
                        download_response = requests.get(
                            location,
                            headers={'Range': f'bytes=0-{self.max_download_size - 1}'},
                            verify=False,
                            timeout=self.timeout,
                            stream=True,
                            proxies=self.proxies if self.proxies else {'http': None, 'https': None}
                        )
                        result['http_status'] = download_response.status_code

                        if download_response.status_code in [200, 206]:
                            downloaded = 0
                            for chunk in download_response.iter_content(chunk_size=65536):
                                if chunk:
                                    downloaded += len(chunk)
                                    if downloaded >= self.max_download_size:
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
                # 测试图片等静态资源（只下载1MB），使用重试机制
                response = self._make_request_with_retry(
                    'get',
                    url,
                    success_codes=[200, 206],
                    headers={'Range': f'bytes=0-{self.max_download_size - 1}'},
                    stream=True
                )
                result['http_status'] = response.status_code

                if response.status_code in [200, 206]:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=65536):
                        if chunk:
                            downloaded += len(chunk)
                            if downloaded >= self.max_download_size:
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

    def batch_test(self, resources: list) -> list:
        """
        批量测试资源列表
        :param resources: 资源列表
        :return: 测试结果列表
        """
        results = []
        for resource in resources:
            result = self.test_url(resource)
            results.append(result)
            # 添加间隔避免请求过快
            time.sleep(0.2)
        return results