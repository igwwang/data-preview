#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置解析模块单元测试
"""

import pytest
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_parser import ConfigParser


class TestConfigParser:
    """配置解析器测试类"""

    def test_init_prod(self):
        """测试初始化prod环境"""
        parser = ConfigParser('prod')
        assert parser.environment == 'prod'

    def test_init_acc(self):
        """测试初始化acc环境"""
        parser = ConfigParser('acc')
        assert parser.environment == 'acc'

    def test_init_dev(self):
        """测试初始化dev环境"""
        parser = ConfigParser('dev')
        assert parser.environment == 'dev'

    def test_get_config_prod(self):
        """测试获取prod环境配置"""
        parser = ConfigParser('prod')
        config = parser.get_config()
        assert 'API_BASE_URL' in config
        assert 'ACCESS_KEY' in config
        assert 'SECRET_KEY' in config
        assert 'DEFAULT_PARAMS' in config
        assert config['API_BASE_URL'] == 'https://saas.zeasn.tv'

    def test_get_config_acc(self):
        """测试获取acc环境配置"""
        parser = ConfigParser('acc')
        config = parser.get_config()
        assert config['API_BASE_URL'] == 'https://acc-saas.zeasn.tv'

    def test_get_config_dev(self):
        """测试获取dev环境配置"""
        parser = ConfigParser('dev')
        config = parser.get_config()
        assert config['API_BASE_URL'] == 'https://dev-saas.zeasn.tv'

    def test_get_api_base_url(self):
        """测试获取API基础URL"""
        parser = ConfigParser('prod')
        url = parser.get_api_base_url()
        assert url == 'https://saas.zeasn.tv'

    def test_get_access_key(self):
        """测试获取访问密钥"""
        parser = ConfigParser('prod')
        key = parser.get_access_key()
        assert len(key) > 0

    def test_get_secret_key(self):
        """测试获取签名密钥"""
        parser = ConfigParser('prod')
        key = parser.get_secret_key()
        assert len(key) > 0

    def test_get_default_params(self):
        """测试获取默认参数"""
        parser = ConfigParser('prod')
        params = parser.get_default_params()
        assert 'productId' in params
        assert 'brandId' in params
        assert 'deviceType' in params

    def test_invalid_environment(self):
        """测试无效环境"""
        parser = ConfigParser('invalid')
        assert parser.environment == 'invalid'
        # 无效环境会使用默认配置（prod）
        config = parser.get_config()
        assert config['API_BASE_URL'] == 'https://saas.zeasn.tv'