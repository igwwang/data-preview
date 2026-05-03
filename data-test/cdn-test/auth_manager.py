#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证管理模块
负责获取设备Token和用户Token
"""

import requests
import time
import hashlib
import hmac
import base64
from urllib.parse import urlencode
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AuthManager:
    def __init__(self, config: dict, proxy: str = None):
        """
        初始化认证管理器
        :param config: 配置字典，包含API_BASE_URL, ACCESS_KEY, SECRET_KEY, DEFAULT_PARAMS
        :param proxy: 代理服务器地址
        """
        self.api_base_url = config.get('API_BASE_URL', '')
        self.access_key = config.get('ACCESS_KEY', '')
        self.secret_key = config.get('SECRET_KEY', '')
        self.default_params = config.get('DEFAULT_PARAMS', {})
        self.device_token = None
        self.user_token = None
        self.max_retries = 3
        self.retry_delay = 2
        
        # 代理配置
        self.proxies = {}
        if proxy:
            self.proxies = {
                'http': proxy,
                'https': proxy
            }

    def generate_auth_header(self, path: str) -> str:
        """
        生成Authorization请求头
        :param path: 请求路径
        :return: Authorization头字符串
        """
        ts = str(int(time.time() * 1000))
        encrypt_str = path + ts
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            encrypt_str.encode('utf-8'),
            hashlib.sha1
        ).digest()
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        return f"{self.access_key}:{signature_b64}:{ts}"

    def _make_request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        带重试机制的请求
        :param method: HTTP方法
        :param url: 请求URL
        :param kwargs: 其他请求参数
        :return: 响应对象
        """
        for attempt in range(self.max_retries):
            try:
                kwargs.setdefault('timeout', 30)
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

    def get_device_token(self) -> str:
        """
        获取设备认证Token
        :return: 设备Token
        """
        print(f"获取设备Token from {self.api_base_url}")

        params = urlencode(self.default_params)

        headers = {
            'Authorization': self.generate_auth_header('/auth-api/api/v1/auth/deviceSign'),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        url = f"{self.api_base_url}/auth-api/api/v1/auth/deviceSign"
        response = self._make_request_with_retry('post', url, headers=headers, data=params)

        result = response.json()
        if result.get('errorCode') != "0":
            raise Exception(f"获取设备Token失败: {result.get('errorMsg', 'Unknown error')}")

        token = result['data']['token']
        self.device_token = token
        print(f"成功获取设备Token: {token[:20]}...")
        return token

    def get_user_token(self) -> str:
        """
        获取用户Token
        :return: 用户Token
        """
        print(f"获取用户Token from {self.api_base_url}")

        params = {
            'productId': self.default_params.get('productId', ''),
            'brandId': self.default_params.get('brandId', ''),
            'deviceSetId': '',
            'mac': self.default_params.get('mac', ''),
            'deviceType': self.default_params.get('deviceType', ''),
            'deviceName': ''
        }

        headers = {
            'Authorization': self.generate_auth_header('/user/device/login'),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        url = f"{self.api_base_url}/user/device/login"
        response = self._make_request_with_retry('post', url, headers=headers, data=urlencode(params))

        result = response.json()
        if result.get('errorCode') != "0":
            raise Exception(f"获取用户Token失败: {result.get('errorMsg', 'Unknown error')}")

        user_token = result['data']['userToken']
        self.user_token = user_token
        print(f"成功获取用户Token: {user_token[:20]}...")
        return user_token

    def get_tokens(self) -> tuple:
        """
        获取所有Token
        :return: (device_token, user_token)
        """
        if not self.device_token:
            self.get_device_token()
        if not self.user_token:
            self.get_user_token()
        return self.device_token, self.user_token