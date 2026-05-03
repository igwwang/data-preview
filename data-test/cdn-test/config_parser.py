#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置解析模块
直接使用内置的默认配置，支持prod/acc/dev三种环境
"""


class ConfigParser:
    def __init__(self, environment: str = 'prod', proxy: str = None):
        """
        初始化配置解析器
        :param environment: 环境类型 'prod', 'acc', 或 'dev'
        :param proxy: 代理服务器地址，格式: http://host:port 或 https://host:port
        """
        self.environment = environment
        self.proxy = proxy
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

    def get_config(self) -> dict:
        """
        获取当前环境的配置
        :return: 配置字典
        """
        if not self.config:
            # 使用默认配置
            env = self.environment if self.environment in self.default_configs else 'prod'
            self.config = self.default_configs.get(env, {})
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

    def get_proxy(self) -> str:
        """获取代理服务器地址"""
        return self.proxy

    def get_proxy_dict(self) -> dict:
        """获取代理字典配置，用于requests库"""
        if self.proxy:
            return {
                'http': self.proxy,
                'https': self.proxy
            }
        return {}

    def has_proxy(self) -> bool:
        """是否配置了代理"""
        return self.proxy is not None and self.proxy.strip() != ''