#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资源提取模块单元测试
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resource_extractor import ResourceExtractor


class TestResourceExtractor:
    """资源提取器测试类"""

    def test_init(self):
        """测试初始化"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        extractor = ResourceExtractor(config, 'test_token')
        assert extractor.api_base_url == 'https://saas.zeasn.tv'
        assert extractor.token == 'test_token'

    def test_extract_urls_from_data_dict(self):
        """测试从字典中提取URL"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        extractor = ResourceExtractor(config, 'test_token')

        data = {
            'icon': 'http://example.com/icon.png',
            'name': 'Test',
            'poster': 'http://example.com/poster.jpg'
        }

        urls = extractor._extract_urls_from_data(data, ['icon', 'poster'])
        assert len(urls) == 2
        assert urls[0]['url'] == 'http://example.com/icon.png'
        assert urls[0]['field'] == 'icon'
        assert urls[1]['url'] == 'http://example.com/poster.jpg'
        assert urls[1]['field'] == 'poster'

    def test_extract_urls_from_data_nested(self):
        """测试从嵌套结构提取URL"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        extractor = ResourceExtractor(config, 'test_token')

        data = {
            'items': [
                {'icon': 'http://example.com/icon1.png'},
                {'icon': 'http://example.com/icon2.png'}
            ]
        }

        urls = extractor._extract_urls_from_data(data, ['icon'])
        assert len(urls) == 2
        assert urls[0]['field'] == 'items[0].icon'
        assert urls[1]['field'] == 'items[1].icon'

    def test_extract_urls_from_data_no_match(self):
        """测试无匹配字段时返回空列表"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        extractor = ResourceExtractor(config, 'test_token')

        data = {
            'name': 'Test',
            'description': 'No URLs here'
        }

        urls = extractor._extract_urls_from_data(data, ['icon', 'poster'])
        assert len(urls) == 0

    def test_extract_image_urls(self):
        """测试提取图片URL"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        extractor = ResourceExtractor(config, 'test_token')

        content = {
            'content': {
                'dataList': [
                    {
                        'name': 'Item1',
                        'icon': 'http://example.com/icon1.png',
                        'poster': 'http://example.com/poster1.jpg'
                    }
                ]
            }
        }

        resources = extractor.extract_image_urls(content, 'Test/Path')
        assert len(resources) == 2
        assert resources[0]['page_path'] == 'Test/Path'
        assert resources[0]['item_name'] == 'Item1'
        assert resources[0]['type'] == 'image'

    def test_extract_download_links(self):
        """测试提取下载链接"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        extractor = ResourceExtractor(config, 'test_token')

        content = {
            'content': {
                'dataList': [
                    {'name': 'App1', 'vsId': 'vs123'},
                    {'name': 'App2', 'vsId': 'vs456'}
                ]
            }
        }

        resources = extractor.extract_download_links(content, 'Test/Path')
        assert len(resources) == 2
        assert resources[0]['page_path'] == 'Test/Path'
        assert resources[0]['vs_id'] == 'vs123'
        assert resources[0]['type'] == 'download'
        assert 'vsId=vs123' in resources[0]['url']

    def test_extract_download_links_duplicate_vsid(self):
        """测试去重下载链接"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        extractor = ResourceExtractor(config, 'test_token')

        content = {
            'content': {
                'dataList': [
                    {'name': 'App1', 'vsId': 'vs123'},
                    {'name': 'App2', 'vsId': 'vs123'}  # 重复vsId
                ]
            }
        }

        resources = extractor.extract_download_links(content, 'Test/Path')
        assert len(resources) == 1  # 应该去重

    def test_extract_download_links_from_value_json(self):
        """测试从value字段的JSON中提取appvsId"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        extractor = ResourceExtractor(config, 'test_token')

        content = {
            'content': {
                'dataList': [
                    {
                        'name': 'Netflix',
                        'value': '{"appId":"680570911942319187","appvsId":"706515241039103377"}'
                    }
                ]
            }
        }

        resources = extractor.extract_download_links(content, 'Test/Path')
        assert len(resources) == 1
        assert resources[0]['vs_id'] == '706515241039103377'
        assert 'vsId=706515241039103377' in resources[0]['url']

    def test_extract_download_links_appvsid_field(self):
        """测试直接从appvsId字段提取"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        extractor = ResourceExtractor(config, 'test_token')

        content = {
            'content': {
                'dataList': [
                    {'name': 'App1', 'appvsId': 'vs789'}
                ]
            }
        }

        resources = extractor.extract_download_links(content, 'Test/Path')
        assert len(resources) == 1
        assert resources[0]['vs_id'] == 'vs789'