#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成模块
负责生成Markdown格式的测试报告
"""

from datetime import datetime
import os


class ReportGenerator:
    def __init__(self, environment: str):
        """
        初始化报告生成器
        :param environment: 测试环境
        """
        self.environment = environment
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate(self, results: list, config: dict = None) -> str:
        """
        生成Markdown报告内容
        :param results: 测试结果列表
        :param config: 配置信息（可选）
        :return: Markdown内容字符串
        """
        if not results:
            return "# CDN可访问性测试报告\n\n没有可用的测试结果"

        # 统计结果
        total_tests = len(results)
        passed_tests = len([r for r in results if r['status'] == 'PASS'])
        failed_tests = total_tests - passed_tests

        # 按类型统计
        image_tests = [r for r in results if r.get('test_type') == 'image']
        download_tests = [r for r in results if r.get('test_type') == 'download']

        image_passed = len([r for r in image_tests if r['status'] == 'PASS'])
        download_passed = len([r for r in download_tests if r['status'] == 'PASS'])

        # 按页面路径分组
        path_groups = {}
        for result in results:
            path = result.get('page_path', 'Unknown')
            if path not in path_groups:
                path_groups[path] = []
            path_groups[path].append(result)

        # 生成报告内容
        content = []

        # 标题
        content.append("# CDN可访问性测试报告")
        content.append("")
        content.append(f"**测试时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"**测试环境:** {self.environment.upper()}")
        if config:
            content.append(f"**API服务器:** {config.get('API_BASE_URL', '')}")
        content.append("")

        # 测试概述
        content.append("## 测试概述")
        content.append("")
        content.append(f"- **总测试项:** {total_tests}")
        content.append(f"- **通过测试:** {passed_tests}")
        content.append(f"- **失败测试:** {failed_tests}")
        content.append(f"- **通过率:** {(passed_tests/total_tests*100):.1f}%")
        content.append("")

        content.append("### 按类型统计")
        content.append("")
        content.append(f"- **图片资源测试:** {len(image_tests)} 项 ({image_passed} 通过)")
        content.append(f"- **下载链接测试:** {len(download_tests)} 项 ({download_passed} 通过)")
        content.append("")

        # 详细测试结果（按页面路径分组）
        content.append("## 详细测试结果")
        content.append("")

        for path, path_results in sorted(path_groups.items()):
            content.append(f"### {path}")
            content.append("")

            # 判断是否包含下载链接
            has_download = any(r.get('test_type') == 'download' for r in path_results)

            if has_download:
                # 下载链接表格
                download_items = [r for r in path_results if r.get('test_type') == 'download']
                content.append("#### 下载链接")
                content.append("")
                content.append("| 应用名称 | vsId | CDN域名 | HTTP状态 | 响应时间 | 状态 | 错误信息 |")
                content.append("|----------|------|---------|----------|----------|------|----------|")
                for result in download_items:
                    status_icon = "✅" if result['status'] == 'PASS' else "❌"
                    error_msg = result.get('error_message', '') or '-'
                    content.append(f"| {result.get('item_name', '-')} | {result.get('vs_id', '-')} | {result.get('cdn_domain', '-')} | {result.get('http_status', '-')} | {result.get('response_time', 0):.2f}s | {status_icon} | {error_msg} |")
                content.append("")

            # 图片资源表格
            image_items = [r for r in path_results if r.get('test_type') == 'image']
            content.append("#### 图片资源")
            content.append("")
            content.append("| 内容名称 | 字段 | CDN域名 | HTTP状态 | 下载字节数 | 响应时间 | 状态 | 错误信息 |")
            content.append("|----------|------|---------|----------|------------|----------|------|----------|")
            for result in image_items:
                status_icon = "✅" if result['status'] == 'PASS' else "❌"
                error_msg = result.get('error_message', '') or '-'
                content.append(f"| {result.get('item_name', '-')} | {result.get('field', '-')} | {result.get('cdn_domain', '-')} | {result.get('http_status', '-')} | {result.get('downloaded_bytes', 0)} | {result.get('response_time', 0):.2f}s | {status_icon} | {error_msg} |")
            content.append("")

        # 问题分析
        content.append("## 问题分析")
        content.append("")

        failed_results = [r for r in results if r['status'] != 'PASS']

        if failed_results:
            content.append("### 失败的测试项")
            content.append("")
            for result in failed_results:
                content.append(f"- **页面路径:** {result.get('page_path', 'Unknown')}")
                content.append(f"  - **资源名称:** {result.get('item_name', '-')}")
                content.append(f"  - **字段:** {result.get('field', '-')}")
                content.append(f"  - **URL:** {result.get('url', '')[:100]}...")
                content.append(f"  - **状态:** {result['status']}")
                content.append(f"  - **错误:** {result.get('error_message', 'Unknown')}")
                content.append("")
        else:
            content.append("✅ **所有测试项都通过了！** CDN可访问性良好。")
            content.append("")

        # CDN域名统计
        content.append("## CDN域名统计")
        content.append("")
        domains = {}
        for result in results:
            domain = result.get('cdn_domain')
            if domain:
                if domain not in domains:
                    domains[domain] = {'pass': 0, 'fail': 0}
                if result['status'] == 'PASS':
                    domains[domain]['pass'] += 1
                else:
                    domains[domain]['fail'] += 1

        if domains:
            content.append("| CDN域名 | 测试次数 | 通过次数 | 失败次数 | 通过率 |")
            content.append("|---------|----------|----------|----------|--------|")
            for domain, stats in sorted(domains.items()):
                total = stats['pass'] + stats['fail']
                rate = (stats['pass'] / total * 100) if total > 0 else 0
                content.append(f"| {domain} | {total} | {stats['pass']} | {stats['fail']} | {rate:.1f}% |")
        else:
            content.append("未检测到CDN域名")

        content.append("")
        content.append(f"---")
        content.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return '\n'.join(content)

    def save_report(self, results: list, config: dict = None, filename: str = None) -> str:
        """
        保存报告到文件
        :param results: 测试结果列表
        :param config: 配置信息（可选）
        :param filename: 文件名（可选）
        :return: 保存的文件路径
        """
        if not filename:
            filename = f"CDN_Accessibility_Report_{self.environment}_{self.timestamp}.md"

        # 确保在cdn-test目录下
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

        content = self.generate(results, config)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return save_path