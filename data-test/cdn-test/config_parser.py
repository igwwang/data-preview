#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置解析模块
从HTML文件中提取API配置信息
支持prod/acc/dev三种环境
"""

import re
import json
import os


class ConfigParser:
    def __init__(self, environment: str = 'prod'):
        """
        初始化配置解析器
        :param environment: 环境类型 'prod', 'acc', 或 'dev'
        """
        self.environment = environment
        self.html_file_map = {
            'prod': 'OS10-prod-QA.html',
            'acc': 'OS10-acc-QA.html',
            'dev': 'OS10-dev-QA.html'
        }
        self.default_configs = {
            'prod': {
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
                    'clientIp': '45.86.202.30'
                }
            },
            'acc': {
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
                    'clientIp': '45.86.202.30'
                }
            },
            'dev': {
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
                    'clientIp': '122.10.101.131'
                }
            }
        }
        self.config = {}

    def _find_html_file(self) -> str:
        """
        查找HTML配置文件
        优先查找项目根目录，然后查找当前目录
        """
        file_name = self.html_file_map.get(self.environment)
        if not file_name:
            return None

        # 优先检查项目根目录
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        root_path = os.path.join(project_root, file_name)
        if os.path.exists(root_path):
            return root_path

        # 检查当前目录
        current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        if os.path.exists(current_path):
            return current_path

        # 检查父目录
        parent_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), file_name)
        if os.path.exists(parent_path):
            return parent_path

        return None

    def _extract_js_variable(self, html_content: str, var_name: str) -> str:
        """
        从HTML内容中提取JavaScript变量值
        :param html_content: HTML内容
        :param var_name: 变量名
        :return: 变量值字符串
        """
        # 匹配 var xxx = ...; 或 const xxx = ...; 或 const xxx=...;
        pattern = rf"(?:var|const)\s*{var_name}\s*=\s*([^;]+);"
        match = re.search(pattern, html_content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None

    def parse_html_config(self, html_path: str = None) -> dict:
        """
        从HTML文件解析配置
        :param html_path: HTML文件路径，为空则自动查找
        :return: 配置字典
        """
        if not html_path:
            html_path = self._find_html_file()

        if not html_path or not os.path.exists(html_path):
            print(f"警告: 未找到HTML配置文件 {html_path}，使用默认配置")
            # 如果环境无效，使用prod作为默认环境
            env = self.environment if self.environment in self.default_configs else 'prod'
            self.config = self.default_configs.get(env, {})
            return self.config

        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()

            config = {}

            # 提取API_BASE_URL
            api_base_url = self._extract_js_variable(content, 'API_BASE_URL')
            if api_base_url and api_base_url.startswith("'") and api_base_url.endswith("'"):
                config['API_BASE_URL'] = api_base_url.strip("'")
            else:
                config['API_BASE_URL'] = self.default_configs[self.environment]['API_BASE_URL']

            # 提取ACCESS_KEY
            access_key = self._extract_js_variable(content, 'ACCESS_KEY')
            if access_key and access_key.startswith("'") and access_key.endswith("'"):
                config['ACCESS_KEY'] = access_key.strip("'")
            else:
                config['ACCESS_KEY'] = self.default_configs[self.environment]['ACCESS_KEY']

            # 提取SECRET_KEY
            secret_key = self._extract_js_variable(content, 'SECRET_KEY')
            if secret_key and secret_key.startswith("'") and secret_key.endswith("'"):
                config['SECRET_KEY'] = secret_key.strip("'")
            else:
                config['SECRET_KEY'] = self.default_configs[self.environment]['SECRET_KEY']

            # 提取DEFAULT_PARAMS
            default_params_str = self._extract_js_variable(content, 'DEFAULT_PARAMS')
            if default_params_str:
                try:
                    config['DEFAULT_PARAMS'] = json.loads(default_params_str)
                except json.JSONDecodeError:
                    config['DEFAULT_PARAMS'] = self.default_configs[self.environment]['DEFAULT_PARAMS']
            else:
                config['DEFAULT_PARAMS'] = self.default_configs[self.environment]['DEFAULT_PARAMS']

            self.config = config
            return config

        except Exception as e:
            print(f"解析HTML配置失败: {e}，使用默认配置")
            return self.default_configs.get(self.environment, {})

    def get_config(self) -> dict:
        """
        获取当前环境的配置
        :return: 配置字典
        """
        if not self.config:
            self.parse_html_config()
        return self.config

    def get_api_base_url(self) -> str:
        """获取API基础URL"""
        return self.get_config().get('API_BASE_URL', '')

    def get_access_key(self) -> str:
        """获取访问密钥"""
        return self.get_config().get('ACCESS_KEY', '')

    def get_secret_key(self) -> str:
        """获取签名密钥"""
        return self.get_config().get('SECRET_KEY', '')

    def get_default_params(self) -> dict:
        """获取默认设备参数"""
        return self.get_config().get('DEFAULT_PARAMS', {})