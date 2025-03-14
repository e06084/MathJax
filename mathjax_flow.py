#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用Graphviz绘制MathJax TeX解析器的流程图
"""

import graphviz

# 创建有向图
dot = graphviz.Digraph('MathJax TeX解析器流程图', comment='MathJax TeX解析器流程图')

# 设置图形属性
dot.attr(rankdir='TB', size='12,12', dpi='300', fontname='SimHei', fontsize='14')
dot.attr('node', shape='box', style='filled', fillcolor='lightblue', fontname='SimHei', fontsize='12')
dot.attr('edge', fontname='SimHei', fontsize='10')

# 添加节点
# 主要类
dot.node('TeX', 'TeX\n(主解析器类)')
dot.node('FindTeX', 'FindTeX\n(查找TeX表达式)')
dot.node('Parser', 'Parser\n(解析器)')
dot.node('ParseOptions', 'ParseOptions\n(解析选项)')
dot.node('Configuration', 'Configuration\n(配置)')
dot.node('ParserConfiguration', 'ParserConfiguration\n(解析器配置)')

# 工厂类
dot.node('NodeFactory', 'NodeFactory\n(节点工厂)')
dot.node('ItemFactory', 'ItemFactory\n(项目工厂)')
dot.node('TagsFactory', 'TagsFactory\n(标签工厂)')

# 辅助类
dot.node('FilterList', 'FilterList\n(过滤器列表)')
dot.node('FunctionList', 'FunctionList\n(函数列表)')
dot.node('PrioritizedList', 'PrioritizedList\n(优先级列表)')
dot.node('ConfigHandler', 'ConfigurationHandler\n(配置处理器)')

# 添加边（关系）
# TeX的主要关系
dot.edge('TeX', 'FindTeX', label='使用')
dot.edge('TeX', 'ParserConfiguration', label='配置')
dot.edge('TeX', 'ParseOptions', label='创建')
dot.edge('TeX', 'FilterList', label='使用过滤器')
dot.edge('TeX', 'Parser', label='创建')

# 解析器配置关系
dot.edge('ParserConfiguration', 'Configuration', label='管理')
dot.edge('ParserConfiguration', 'FunctionList', label='使用')
dot.edge('ParserConfiguration', 'PrioritizedList', label='使用')
dot.edge('ParserConfiguration', 'ConfigHandler', label='获取配置')

# 解析选项关系
dot.edge('ParseOptions', 'NodeFactory', label='创建')
dot.edge('ParseOptions', 'ItemFactory', label='创建')
dot.edge('ParseOptions', 'TagsFactory', label='使用')

# 解析流程
dot.edge('FindTeX', 'TeX', label='返回数学表达式')
dot.edge('TeX', 'Parser', label='解析LaTeX')
dot.edge('Parser', 'TeX', label='返回MML')

# 创建子图：处理流程
with dot.subgraph(name='cluster_process') as c:
    c.attr(label='TeX处理流程', style='filled', fillcolor='lightgrey')
    c.node('Input', '输入文本', shape='ellipse', fillcolor='lightgreen')
    c.node('Find', '查找数学表达式', shape='box', fillcolor='white')
    c.node('PreFilter', '应用前置过滤器', shape='box', fillcolor='white')
    c.node('Parse', '解析LaTeX', shape='box', fillcolor='white')
    c.node('PostFilter', '应用后置过滤器', shape='box', fillcolor='white')
    c.node('Output', '输出MML', shape='ellipse', fillcolor='lightgreen')
    
    c.edge('Input', 'Find')
    c.edge('Find', 'PreFilter')
    c.edge('PreFilter', 'Parse')
    c.edge('Parse', 'PostFilter')
    c.edge('PostFilter', 'Output')

# 创建子图：类层次结构
with dot.subgraph(name='cluster_hierarchy') as c:
    c.attr(label='类层次结构', style='filled', fillcolor='lightyellow')
    c.node('AbstractInputJax', 'AbstractInputJax\n(抽象基类)', fillcolor='white')
    c.node('TexClass', 'TeX\n(具体实现)', fillcolor='white')
    
    c.edge('AbstractInputJax', 'TexClass', label='继承')

# 保存图形
dot.render('mathjax_flow', format='png', cleanup=True)
print("流程图已生成：mathjax_flow.png") 