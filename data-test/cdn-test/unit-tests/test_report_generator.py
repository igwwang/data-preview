#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成模块单元测试
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from report_generator import ReportGenerator


class TestReportGenerator:
    """报告生成器测试类"""

    def test_init(self):
        """测试初始化"""
        generator = ReportGenerator('prod')
        assert generator.environment == 'prod'

    def test_generate_empty_results(self):
        """测试生成空结果报告"""
        generator = ReportGenerator('prod')
        content = generator.generate([])
        assert content is not None
        assert 'CDN可访问性测试报告' in content
        assert '没有可用的测试结果' in content

    def test_generate_with_results(self):
        """测试生成有结果的报告"""
        generator = ReportGenerator('prod')

        results = [
            {
                'url': 'http://cdn.example.com/image.png',
                'test_type': 'image',
                'page_path': 'Category/SubCategory',
                'field': 'icon',
                'item_name': 'Test Item',
                'status': 'PASS',
                'http_status': 200,
                'downloaded_bytes': 1024,
                'response_time': 0.5,
                'cdn_domain': 'cdn.example.com'
            }
        ]

        content = generator.generate(results)
        assert 'CDN可访问性测试报告' in content
        assert 'Category/SubCategory' in content
        assert 'cdn.example.com' in content
        assert '✅' in content

    def test_generate_with_failed_results(self):
        """测试生成包含失败结果的报告"""
        generator = ReportGenerator('prod')

        results = [
            {
                'url': 'http://cdn.example.com/image.png',
                'test_type': 'image',
                'page_path': 'Test/Path',
                'field': 'icon',
                'item_name': 'Test Item',
                'status': 'FAIL',
                'http_status': 404,
                'cdn_domain': 'cdn.example.com',
                'error_message': 'Not Found'
            }
        ]

        content = generator.generate(results)
        assert '❌' in content
        assert '- **失败测试:** 1' in content
        assert 'Not Found' in content

    def test_generate_summary(self):
        """测试生成摘要信息"""
        generator = ReportGenerator('prod')

        results = [
            {'url': 'http://cdn.com/img1.png', 'test_type': 'image', 'status': 'PASS', 'cdn_domain': 'cdn.com'},
            {'url': 'http://cdn.com/img2.png', 'test_type': 'image', 'status': 'FAIL', 'cdn_domain': 'cdn.com'},
            {'url': 'http://cdn.com/download', 'test_type': 'download', 'status': 'PASS', 'cdn_domain': 'cdn.com'}
        ]

        content = generator.generate(results)
        assert '- **总测试项:** 3' in content
        assert '- **通过测试:** 2' in content
        assert '- **失败测试:** 1' in content
        assert '- **图片资源测试:** 2 项 (1 通过)' in content
        assert '- **下载链接测试:** 1 项 (1 通过)' in content

    def test_save_report(self):
        """测试保存报告到文件"""
        generator = ReportGenerator('prod')

        results = [
            {
                'url': 'http://cdn.example.com/image.png',
                'test_type': 'image',
                'page_path': 'Test/Path',
                'field': 'icon',
                'item_name': 'Test Item',
                'status': 'PASS',
                'http_status': 200,
                'cdn_domain': 'cdn.example.com'
            }
        ]

        report_path = generator.save_report(results, filename='test_report.md')
        assert os.path.exists(report_path)
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'CDN可访问性测试报告' in content

        # 清理测试文件
        os.remove(report_path)