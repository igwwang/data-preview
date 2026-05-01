#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节点遍历模块单元测试
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from node_traverser import NodeTraverser


class TestNodeTraverser:
    """节点遍历器测试类"""

    def test_init(self):
        """测试初始化"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        traverser = NodeTraverser(config, 'test_token')
        assert traverser.api_base_url == 'https://saas.zeasn.tv'
        assert traverser.token == 'test_token'

    def test_traverse_nodes_leaf_only(self):
        """测试遍历只有叶子节点的树"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        traverser = NodeTraverser(config, 'test_token')

        nodes = [
            {'id': '1', 'name': 'Node1', 'children': []},
            {'id': '2', 'name': 'Node2', 'children': []}
        ]

        leaf_nodes = traverser.traverse_nodes(nodes)
        assert len(leaf_nodes) == 2
        assert leaf_nodes[0]['id'] == '1'
        assert leaf_nodes[0]['name'] == 'Node1'
        assert leaf_nodes[0]['path'] == 'Node1'

    def test_traverse_nodes_with_children(self):
        """测试遍历带有子节点的树"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        traverser = NodeTraverser(config, 'test_token')

        nodes = [
            {
                'id': '1',
                'name': 'Parent1',
                'children': [
                    {'id': '1-1', 'name': 'Child1', 'children': []},
                    {'id': '1-2', 'name': 'Child2', 'children': []}
                ]
            }
        ]

        leaf_nodes = traverser.traverse_nodes(nodes)
        assert len(leaf_nodes) == 2
        assert leaf_nodes[0]['path'] == 'Parent1/Child1'
        assert leaf_nodes[1]['path'] == 'Parent1/Child2'

    def test_traverse_nodes_nested(self):
        """测试遍历多层嵌套节点"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        traverser = NodeTraverser(config, 'test_token')

        nodes = [
            {
                'id': '1',
                'name': 'Level1',
                'children': [
                    {
                        'id': '1-1',
                        'name': 'Level2',
                        'children': [
                            {'id': '1-1-1', 'name': 'Level3', 'children': []}
                        ]
                    }
                ]
            }
        ]

        leaf_nodes = traverser.traverse_nodes(nodes)
        assert len(leaf_nodes) == 1
        assert leaf_nodes[0]['path'] == 'Level1/Level2/Level3'

    def test_traverse_nodes_empty(self):
        """测试遍历空节点列表"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        traverser = NodeTraverser(config, 'test_token')

        leaf_nodes = traverser.traverse_nodes([])
        assert len(leaf_nodes) == 0

    def test_traverse_nodes_mixed(self):
        """测试遍历混合结构（既有叶子又有分支）"""
        config = {'API_BASE_URL': 'https://saas.zeasn.tv'}
        traverser = NodeTraverser(config, 'test_token')

        nodes = [
            {'id': '1', 'name': 'Leaf1', 'children': []},
            {
                'id': '2',
                'name': 'Branch1',
                'children': [
                    {'id': '2-1', 'name': 'Leaf2', 'children': []}
                ]
            }
        ]

        leaf_nodes = traverser.traverse_nodes(nodes)
        assert len(leaf_nodes) == 2
        paths = [n['path'] for n in leaf_nodes]
        assert 'Leaf1' in paths
        assert 'Branch1/Leaf2' in paths