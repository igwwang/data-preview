#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资源提取模块
负责从栏目内容中提取图片URL和APK下载链接
"""

import requests
import time
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ResourceExtractor:
    def __init__(self, config: dict, token: str):
        """
        初始化资源提取器
        :param config: 配置字典
        :param token: 认证Token
        """
        self.api_base_url = config.get('API_BASE_URL', '')
        self.token = token
        self.max_retries = 3
        self.retry_delay = 2

        # 需要提取的图片字段
        self.image_fields = ['icon', 'poster', 'cover', 'background', 'backgroud']

    def _make_request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        带重试机制的请求
        """
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

    def get_column_content(self, column_id: str) -> dict:
        """
        获取栏目内容
        :param column_id: 栏目ID
        :return: 栏目内容字典
        """
        url = f"{self.api_base_url}/sp/api/device/v1/column/content?token={self.token}&columnIds={column_id}"
        response = self._make_request_with_retry('get', url)
        result = response.json()

        if result.get('errorCode') != 0:
            raise Exception(f"获取栏目内容失败: {result.get('errorMsg', 'Unknown error')}")

        if not result.get('data') or len(result['data']) == 0:
            return {}

        return result['data'][0]

    def _extract_urls_from_data(self, data, fields, parent_name=""):
        """
        递归从数据中提取指定字段的URL
        :param data: 数据（dict或list）
        :param fields: 需要提取的字段名列表
        :param parent_name: 父字段名
        :return: URL列表，每个元素包含url和field
        """
        urls = []

        if isinstance(data, dict):
            for key, value in data.items():
                field_name = f"{parent_name}.{key}" if parent_name else key
                if key in fields and isinstance(value, str) and value.startswith('http'):
                    urls.append({'url': value, 'field': field_name})
                elif isinstance(value, (dict, list)):
                    urls.extend(self._extract_urls_from_data(value, fields, field_name))
        elif isinstance(data, list):
            for i, element in enumerate(data):
                urls.extend(self._extract_urls_from_data(element, fields, f"{parent_name}[{i}]"))

        return urls

    def extract_image_urls(self, content: dict, node_path: str) -> list:
        """
        提取图片URL列表
        :param content: 栏目内容
        :param node_path: 页面路径
        :return: 图片资源列表
        """
        resources = []

        # 获取数据列表
        content_data = content.get('content', {})
        data_list = content_data.get('dataList', [])

        for item in data_list:
            # 提取图片URL
            image_urls = self._extract_urls_from_data(item, self.image_fields)
            for img_info in image_urls:
                resources.append({
                    'url': img_info['url'],
                    'field': img_info['field'],
                    'page_path': node_path,
                    'item_name': item.get('name', '') or item.get('title', ''),
                    'type': 'image'
                })

        return resources

    def extract_download_links(self, content: dict, node_path: str) -> list:
        """
        提取APK下载链接列表
        :param content: 栏目内容
        :param node_path: 页面路径
        :return: 下载链接列表
        """
        resources = []
        tested_vs_ids = set()

        # 获取数据列表
        content_data = content.get('content', {})
        data_list = content_data.get('dataList', [])

        for item in data_list:
            # 优先从vsId字段获取
            vs_id = item.get('vsId')
            
            # 如果没有vsId，尝试从value字段的JSON中提取appvsId
            if not vs_id:
                value_str = item.get('value', '')
                if value_str:
                    try:
                        value_data = json.loads(value_str)
                        vs_id = value_data.get('appvsId')
                    except json.JSONDecodeError:
                        pass
            
            # 如果还是没有，尝试直接获取appvsId字段
            if not vs_id:
                vs_id = item.get('appvsId')
            
            if vs_id and vs_id not in tested_vs_ids:
                tested_vs_ids.add(vs_id)
                download_url = f"{self.api_base_url}/sp/api/device/v1/app/download?token={self.token}&vsId={vs_id}"
                resources.append({
                    'url': download_url,
                    'field': 'download',
                    'page_path': node_path,
                    'item_name': item.get('name', '') or item.get('title', ''),
                    'vs_id': vs_id,
                    'type': 'download'
                })

        return resources

    def extract_all_resources(self, column_id: str, node_path: str) -> list:
        """
        提取栏目中的所有资源
        :param column_id: 栏目ID
        :param node_path: 页面路径
        :return: 资源列表
        """
        try:
            content = self.get_column_content(column_id)
            if not content:
                return []

            resources = []

            # 提取图片URL
            image_resources = self.extract_image_urls(content, node_path)
            resources.extend(image_resources)

            # 提取下载链接
            download_resources = self.extract_download_links(content, node_path)
            resources.extend(download_resources)

            return resources

        except Exception as e:
            print(f"提取资源失败 [{node_path}]: {e}")
            return []