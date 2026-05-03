#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CDN可访问性测试工具 - 完整版
能够100%遍历页面所有栏目节点，验证所有图片和APK下载链接的可访问性
输出包含完整页面路径的测试报告
支持prod/acc/dev三种环境
"""

import sys
import time

from config_parser import ConfigParser
from auth_manager import AuthManager
from node_traverser import NodeTraverser
from resource_extractor import ResourceExtractor
from accessibility_tester import AccessibilityTester
from report_generator import ReportGenerator


class CDNAccessibilityFullTester:
    def __init__(self, environment: str = 'prod', proxy: str = None):
        """
        初始化CDN可访问性测试器
        :param environment: 环境类型 'prod', 'acc', 或 'dev'
        :param proxy: 代理服务器地址，格式: http://host:port 或 https://host:port
        """
        self.environment = environment
        self.proxy = proxy
        self.config_parser = ConfigParser(environment, proxy)
        self.config = {}
        self.auth_manager = None
        self.node_traverser = None
        self.resource_extractor = None
        self.accessibility_tester = None
        self.report_generator = ReportGenerator(environment)
        self.test_results = []

    def initialize(self):
        """
        初始化所有模块
        """
        print(f"初始化CDN可访问性测试器 ({self.environment.upper()}环境)...")

        # 1. 解析配置
        print("1. 解析配置...")
        self.config = self.config_parser.get_config()
        print(f"   API_BASE_URL: {self.config.get('API_BASE_URL', '')}")

        # 2. 初始化认证管理器
        print("2. 初始化认证管理器...")
        self.auth_manager = AuthManager(self.config, self.proxy)

        # 3. 获取Token
        print("3. 获取认证Token...")
        token, user_token = self.auth_manager.get_tokens()

        # 4. 初始化节点遍历器
        print("4. 初始化节点遍历器...")
        self.node_traverser = NodeTraverser(self.config, token, self.proxy)

        # 5. 初始化资源提取器
        print("5. 初始化资源提取器...")
        self.resource_extractor = ResourceExtractor(self.config, token, self.proxy)

        # 6. 初始化可访问性测试器
        print("6. 初始化可访问性测试器...")
        self.accessibility_tester = AccessibilityTester(proxy=self.proxy)

        # 显示代理配置
        if self.proxy:
            print(f"   使用代理: {self.proxy}")

        print("初始化完成！")
        print("")

    def run_test(self):
        """
        运行完整的CDN可访问性测试
        """
        print("=" * 70)
        print(f"开始CDN可访问性完整测试 ({self.environment.upper()}环境)")
        print("=" * 70)
        print("")

        start_time = time.time()

        try:
            # 1. 初始化
            self.initialize()

            # 2. 获取所有叶子节点
            print("步骤1: 获取所有栏目叶子节点")
            print("-" * 50)
            leaf_nodes = self.node_traverser.get_leaf_nodes()
            print("")

            # 3. 遍历每个叶子节点，提取资源并测试
            print("步骤2: 遍历节点并测试资源可访问性")
            print("-" * 50)

            total_resources = 0
            tested_resources = 0

            for idx, node in enumerate(leaf_nodes, 1):
                node_id = node['id']
                node_name = node['name']
                node_path = node['path']

                print(f"\n[{idx}/{len(leaf_nodes)}] 处理栏目: {node_path}")

                # 提取资源
                try:
                    resources = self.resource_extractor.extract_all_resources(node_id, node_path)
                    print(f"    发现 {len(resources)} 个资源")
                    total_resources += len(resources)

                    if resources:
                        # 测试每个资源
                        for resource in resources:
                            result = self.accessibility_tester.test_url(resource)
                            self.test_results.append(result)
                            tested_resources += 1

                            status_icon = "✅" if result['status'] == 'PASS' else "❌"
                            item_name = resource.get('item_name', '')
                            if item_name:
                                print(f"    {status_icon} [{resource['field']}] {item_name}")
                                print(f"        URL: {resource['url']}")
                            else:
                                print(f"    {status_icon} [{resource['field']}] {resource['url']}")

                        # 添加间隔
                        time.sleep(0.5)

                except Exception as e:
                    print(f"    处理失败: {e}")
                    continue

            # 4. 生成报告
            print("\n步骤3: 生成测试报告")
            print("-" * 50)
            report_path = self.report_generator.save_report(self.test_results, self.config)
            print(f"报告已保存到: {report_path}")

            # 5. 输出摘要
            print("\n步骤4: 测试摘要")
            print("-" * 50)
            self.print_summary(start_time)

        except Exception as e:
            print(f"\n测试过程中发生错误: {str(e)}")
            import traceback
            traceback.print_exc()

    def print_summary(self, start_time):
        """
        打印测试摘要
        :param start_time: 测试开始时间
        """
        total_time = time.time() - start_time

        # 统计结果
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = total_tests - passed_tests

        # 按类型统计
        image_tests = [r for r in self.test_results if r.get('test_type') == 'image']
        download_tests = [r for r in self.test_results if r.get('test_type') == 'download']

        image_passed = len([r for r in image_tests if r['status'] == 'PASS'])
        download_passed = len([r for r in download_tests if r['status'] == 'PASS'])

        print(f"\n[SUMMARY] CDN可访问性测试摘要 ({self.environment.upper()}):")
        print(f"   测试环境: {self.environment.upper()}")
        print(f"   API服务器: {self.config.get('API_BASE_URL', '')}")
        print(f"   总测试项: {total_tests}")
        print(f"   - 图片资源: {len(image_tests)} 项 ({image_passed} 通过)")
        print(f"   - 下载链接: {len(download_tests)} 项 ({download_passed} 通过)")
        print(f"   通过测试: {passed_tests}")
        print(f"   失败测试: {failed_tests}")
        print(f"   通过率: {(passed_tests/total_tests*100):.1f}%")
        print(f"   总耗时: {total_time:.2f}秒")

        if failed_tests > 0:
            print("\n[ISSUES] 发现问题的测试项:")
            for result in self.test_results:
                if result['status'] != 'PASS':
                    print(f"   - {result.get('page_path', 'Unknown')}")
                    print(f"     {result.get('field', '-')}: {result.get('url', '')}")
                    if result.get('error_message'):
                        print(f"     错误: {result['error_message']}")


def main():
    """
    主执行函数
    """
    environment = 'prod'  # 默认使用prod环境
    proxy = None

    # 解析命令行参数
    i = 1
    while i < len(sys.argv):
        if sys.argv[i].lower() in ['prod', 'acc', 'dev']:
            environment = sys.argv[i].lower()
        elif sys.argv[i].lower() == '--proxy' and i + 1 < len(sys.argv):
            proxy = sys.argv[i + 1]
            i += 1
        else:
            print("使用方法:")
            print("  python cdn_accessibility_full_tester.py [prod|acc|dev] [--proxy http://host:port]")
            print("")
            print("参数说明:")
            print("  prod|acc|dev   : 测试环境 (默认: prod)")
            print("  --proxy URL    : 代理服务器地址 (可选)")
            print("")
            print("示例:")
            print("  python cdn_accessibility_full_tester.py")
            print("  python cdn_accessibility_full_tester.py acc")
            print("  python cdn_accessibility_full_tester.py prod --proxy http://proxy.example.com:8080")
            sys.exit(1)
        i += 1

    tester = CDNAccessibilityFullTester(environment, proxy)
    tester.run_test()


if __name__ == "__main__":
    main()