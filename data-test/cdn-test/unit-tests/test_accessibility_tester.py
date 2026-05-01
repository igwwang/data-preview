#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可访问性验证模块单元测试
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from accessibility_tester import AccessibilityTester


class TestAccessibilityTester:
    """可访问性测试器测试类"""

    def test_init(self):
        """测试初始化"""
        tester = AccessibilityTester()
        assert tester.max_retries == 3
        assert tester.retry_delay == 2

    def test_test_url_result_structure(self):
        """测试测试结果结构"""
        tester = AccessibilityTester()

        resource = {
            'url': 'http://example.com/test.png',
            'type': 'image',
            'page_path': 'Test/Path',
            'field': 'icon',
            'item_name': 'Test Item'
        }

        result = tester.test_url(resource)
        assert 'url' in result
        assert 'test_type' in result
        assert 'page_path' in result
        assert 'field' in result
        assert 'item_name' in result
        assert 'status' in result
        assert 'http_status' in result
        assert 'cdn_domain' in result

    def test_test_url_image_type(self):
        """测试图片类型资源"""
        tester = AccessibilityTester()

        resource = {
            'url': 'http://example.com/test.png',
            'type': 'image',
            'page_path': 'Test/Path',
            'field': 'icon',
            'item_name': 'Test Item'
        }

        result = tester.test_url(resource)
        assert result['test_type'] == 'image'
        assert result['cdn_domain'] == 'example.com'

    def test_test_url_download_type(self):
        """测试下载类型资源"""
        tester = AccessibilityTester()

        resource = {
            'url': 'http://example.com/download?vsId=123',
            'type': 'download',
            'page_path': 'Test/Path',
            'field': 'download',
            'item_name': 'Test App',
            'vs_id': '123'
        }

        result = tester.test_url(resource)
        assert result['test_type'] == 'download'
        assert result['vs_id'] == '123'

    def test_test_url_empty_url(self):
        """测试空URL"""
        tester = AccessibilityTester()

        resource = {
            'url': '',
            'type': 'image',
            'page_path': 'Test/Path',
            'field': 'icon'
        }

        result = tester.test_url(resource)
        # 空URL应该返回失败
        assert result['status'] == 'FAIL'

    def test_batch_test(self):
        """测试批量测试"""
        tester = AccessibilityTester()

        resources = [
            {
                'url': 'http://example.com/test1.png',
                'type': 'image',
                'page_path': 'Test/Path1',
                'field': 'icon'
            },
            {
                'url': 'http://example.com/test2.png',
                'type': 'image',
                'page_path': 'Test/Path2',
                'field': 'icon'
            }
        ]

        results = tester.batch_test(resources)
        assert len(results) == 2