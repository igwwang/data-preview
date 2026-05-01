#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证管理模块单元测试
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth_manager import AuthManager


class TestAuthManager:
    """认证管理器测试类"""

    def test_init(self):
        """测试初始化"""
        config = {
            'API_BASE_URL': 'https://saas.zeasn.tv',
            'ACCESS_KEY': 'test_access_key',
            'SECRET_KEY': 'test_secret_key',
            'DEFAULT_PARAMS': {
                'productId': 'test',
                'brandId': '1',
                'deviceType': 'test_device',
                'mac': 'test_mac'
            }
        }
        auth = AuthManager(config)
        assert auth.api_base_url == 'https://saas.zeasn.tv'
        assert auth.access_key == 'test_access_key'
        assert auth.secret_key == 'test_secret_key'

    def test_generate_auth_header(self):
        """测试生成认证头"""
        config = {
            'API_BASE_URL': 'https://saas.zeasn.tv',
            'ACCESS_KEY': 'test_access_key',
            'SECRET_KEY': 'test_secret_key',
            'DEFAULT_PARAMS': {}
        }
        auth = AuthManager(config)
        header = auth.generate_auth_header('/test/path')
        assert header is not None
        assert ':' in header  # 应该包含access_key:signature:timestamp格式

    def test_generate_auth_header_format(self):
        """测试认证头格式"""
        config = {
            'API_BASE_URL': 'https://saas.zeasn.tv',
            'ACCESS_KEY': 'AK123',
            'SECRET_KEY': 'SK123',
            'DEFAULT_PARAMS': {}
        }
        auth = AuthManager(config)
        header = auth.generate_auth_header('/test/path')
        parts = header.split(':')
        assert len(parts) == 3
        assert parts[0] == 'AK123'  # access_key
        assert len(parts[1]) > 0    # signature
        assert parts[2].isdigit()   # timestamp

    def test_token_initially_none(self):
        """测试Token初始为None"""
        config = {
            'API_BASE_URL': 'https://saas.zeasn.tv',
            'ACCESS_KEY': 'test',
            'SECRET_KEY': 'test',
            'DEFAULT_PARAMS': {}
        }
        auth = AuthManager(config)
        assert auth.device_token is None
        assert auth.user_token is None