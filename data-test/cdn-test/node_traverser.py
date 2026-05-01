#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节点遍历模块
负责递归遍历栏目树形结构，获取所有叶子节点及其路径
"""

import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NodeTraverser:
    def __init__(self, config: dict, token: str):
        """
        初始化节点遍历器
        :param config: 配置字典
        :param token: 认证Token
        """
        self.api_base_url = config.get('API_BASE_URL', '')
        self.token = token
        self.max_retries = 3
        self.retry_delay = 2

    def _make_request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        带重试机制的请求
        """
        for attempt in range(self.max_retries):
            try:
                kwargs.setdefault('timeout', 30)
                kwargs.setdefault('verify', False)

                if method.lower() == 'get':
                    response = requests.get(url, **kwargs)
                elif method.lower() == 'post':
                    response = requests.post(url, **kwargs)
                else:
                    raise ValueError(f"不支持的HTTP方法: {method}")

                if response.status_code == 200:
                    return response
                else:
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        return response

            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise
            except Exception:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise

        raise Exception(f"重试{self.max_retries}次后仍然失败")

    def get_columns(self) -> list:
        """
        获取栏目列表
        :return: 栏目树形结构列表
        """
        print("获取栏目列表...")
        url = f"{self.api_base_url}/sp/api/device/v1/column?token={self.token}"
        response = self._make_request_with_retry('get', url)
        result = response.json()

        if result.get('errorCode') != 0:
            raise Exception(f"获取栏目列表失败: {result.get('errorMsg', 'Unknown error')}")

        columns = result.get('data', [])
        print(f"发现 {len(columns)} 个顶级栏目")
        return columns

    def traverse_nodes(self, nodes: list, parent_path: str = "") -> list:
        """
        递归遍历节点，返回叶子节点列表
        :param nodes: 节点列表
        :param parent_path: 父节点路径
        :return: 叶子节点列表，每个节点包含id, name, path
        """
        leaf_nodes = []

        for node in nodes:
            node_id = node.get('id', '')
            node_name = node.get('name', '')

            # 构建当前节点的完整路径
            if parent_path:
                current_path = f"{parent_path}/{node_name}"
            else:
                current_path = node_name

            # 检查是否有子节点
            children = node.get('children', [])
            if isinstance(children, list) and len(children) > 0:
                # 有子节点，递归遍历
                leaf_nodes.extend(self.traverse_nodes(children, current_path))
            else:
                # 叶子节点，添加到结果
                leaf_nodes.append({
                    'id': node_id,
                    'name': node_name,
                    'path': current_path,
                    'raw_node': node
                })

        return leaf_nodes

    def get_leaf_nodes(self) -> list:
        """
        获取所有叶子节点及其路径
        :return: 叶子节点列表
        """
        columns = self.get_columns()
        leaf_nodes = self.traverse_nodes(columns)
        print(f"共发现 {len(leaf_nodes)} 个叶子节点")
        return leaf_nodes

    def print_tree_structure(self, nodes: list = None, indent: int = 0):
        """
        打印树形结构（用于调试）
        :param nodes: 节点列表
        :param indent: 缩进级别
        """
        if nodes is None:
            nodes = self.get_columns()

        prefix = "  " * indent
        for node in nodes:
            node_name = node.get('name', 'Unknown')
            node_id = node.get('id', '')
            children = node.get('children', [])
            is_leaf = not (isinstance(children, list) and len(children) > 0)

            marker = "└──" if is_leaf else "├──"
            print(f"{prefix}{marker} {node_name} (#{node_id}){' [叶子]' if is_leaf else ''}")

            if not is_leaf:
                self.print_tree_structure(children, indent + 1)