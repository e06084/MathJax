#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用Graphviz绘制MathJax核心功能流程图
"""

import graphviz

# 创建有向图
dot = graphviz.Digraph('MathJax核心功能流程图', comment='MathJax核心功能流程图')

# 设置图形属性
dot.attr(rankdir='TB', size='12,12', dpi='300', fontname='SimHei', 
         fontsize='14')
dot.attr('node', shape='box', style='filled', fillcolor='lightblue', 
         fontname='SimHei', fontsize='12')
dot.attr('edge', fontname='SimHei', fontsize='10')

# 添加主要类节点
dot.node('MathJax', 'MathJax\n(主类)')
dot.node('MathDocument', 'MathDocument\n(数学文档)')
dot.node('MathList', 'MathList\n(数学列表)')
dot.node('MathItem', 'MathItem\n(数学项)')
dot.node('DOMAdaptor', 'DOMAdaptor\n(DOM适配器)')
dot.node('HTMLAdaptor', 'HTMLAdaptor\n(HTML适配器)')
dot.node('Options', 'Options\n(选项管理)')

# 添加关系边
dot.edge('MathJax', 'MathDocument', label='创建')
dot.edge('MathDocument', 'MathList', label='包含')
dot.edge('MathList', 'MathItem', label='包含多个')
dot.edge('MathDocument', 'DOMAdaptor', label='使用')
dot.edge('HTMLAdaptor', 'DOMAdaptor', label='继承')
dot.edge('MathJax', 'Options', label='使用')

# 创建子图：MathJax初始化流程
with dot.subgraph(name='cluster_init') as c:
    c.attr(label='MathJax初始化流程', style='filled', fillcolor='lightgrey')
    c.node('Init1', '创建MathJax实例', shape='box', fillcolor='white')
    c.node('Init2', '注册输入Jax', shape='box', fillcolor='white')
    c.node('Init3', '注册输出Jax', shape='box', fillcolor='white')
    c.node('Init4', '注册文档类', shape='box', fillcolor='white')
    c.node('Init5', '启动MathJax', shape='box', fillcolor='white')
    
    c.edge('Init1', 'Init2')
    c.edge('Init2', 'Init3')
    c.edge('Init3', 'Init4')
    c.edge('Init4', 'Init5')

# 创建子图：数学处理流程
with dot.subgraph(name='cluster_process') as c:
    c.attr(label='数学处理流程', style='filled', fillcolor='lightgrey')
    c.node('Process1', '创建MathDocument', shape='box', fillcolor='white')
    c.node('Process2', '查找数学表达式', shape='box', fillcolor='white')
    c.node('Process3', '编译数学表达式', shape='box', fillcolor='white')
    c.node('Process4', '转换数学表达式', shape='box', fillcolor='white')
    c.node('Process5', '排版数学表达式', shape='box', fillcolor='white')
    c.node('Process6', '更新文档', shape='box', fillcolor='white')
    
    c.edge('Process1', 'Process2')
    c.edge('Process2', 'Process3')
    c.edge('Process3', 'Process4')
    c.edge('Process4', 'Process5')
    c.edge('Process5', 'Process6')

# 创建子图：MathItem状态流程
with dot.subgraph(name='cluster_mathitem') as c:
    c.attr(label='MathItem状态流程', style='filled', fillcolor='lightyellow')
    c.node('State0', '初始状态\n(state=0)', shape='ellipse', fillcolor='white')
    c.node('State1', '输入已渲染\n(state=1)', shape='ellipse', fillcolor='white')
    c.node('State2', '已转换\n(state=2)', shape='ellipse', fillcolor='white')
    c.node('State3', '输出已渲染\n(state=3)', shape='ellipse', fillcolor='white')
    
    c.edge('State0', 'State1', label='render_input()')
    c.edge('State1', 'State2', label='convert()')
    c.edge('State2', 'State3', label='render_output()')
    c.edge('State3', 'State0', label='reset()')

# 创建子图：Options选项处理流程
with dot.subgraph(name='cluster_options') as c:
    c.attr(label='Options选项处理流程', style='filled', fillcolor='lightpink')
    c.node('Opt1', '默认选项\n(MathJax.options)', shape='box', fillcolor='white')
    c.node('Opt2', '用户选项\n(user_options)', shape='box', fillcolor='white')
    c.node('Opt3', '合并选项\n(Options.user_options())', shape='box', fillcolor='white')
    c.node('Opt4', '文档选项\n(doc_options)', shape='box', fillcolor='white')
    c.node('Opt5', '组件选项\n(InputJax/OutputJax)', shape='box', fillcolor='white')
    c.node('Opt6', '分离选项\n(separate_options())', shape='box', fillcolor='white')
    
    c.edge('Opt1', 'Opt3')
    c.edge('Opt2', 'Opt3')
    c.edge('Opt3', 'Opt4', label='创建文档时')
    c.edge('Opt4', 'Opt5', label='传递给组件')
    c.edge('Opt5', 'Opt6', label='组件内部处理')
    c.edge('Options', 'Opt1', style='dashed')
    c.edge('Options', 'Opt3', style='dashed', label='静态方法')

# 创建子图：DOM操作
with dot.subgraph(name='cluster_dom') as c:
    c.attr(label='DOM操作', style='filled', fillcolor='lightcyan')
    c.node('DOM1', '解析HTML/XML', shape='box', fillcolor='white')
    c.node('DOM2', '创建/修改元素', shape='box', fillcolor='white')
    c.node('DOM3', '查询元素', shape='box', fillcolor='white')
    c.node('DOM4', '操作属性/样式', shape='box', fillcolor='white')
    
    c.edge('DOMAdaptor', 'DOM1', style='dashed')
    c.edge('DOMAdaptor', 'DOM2', style='dashed')
    c.edge('DOMAdaptor', 'DOM3', style='dashed')
    c.edge('DOMAdaptor', 'DOM4', style='dashed')

# 创建子图：类层次结构
with dot.subgraph(name='cluster_hierarchy') as c:
    c.attr(label='核心类关系', style='filled', fillcolor='lavender')
    c.node('Core', 'MathJax核心', shape='ellipse', fillcolor='white')
    c.node('Input', '输入Jax', shape='ellipse', fillcolor='white')
    c.node('Output', '输出Jax', shape='ellipse', fillcolor='white')
    c.node('Adaptor', '适配器', shape='ellipse', fillcolor='white')
    
    c.edge('Core', 'Input', label='使用')
    c.edge('Core', 'Output', label='使用')
    c.edge('Core', 'Adaptor', label='使用')
    c.edge('Input', 'MathItem', label='处理', style='dashed')
    c.edge('Output', 'MathItem', label='处理', style='dashed')

# 保存图形
dot.render('mathjax_core_flow', format='png', cleanup=True)
print("流程图已生成：mathjax_core_flow.png") 