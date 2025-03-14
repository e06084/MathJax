#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python版本的MathJax MathDocument类
实现数学表达式的查找、编译、转换、渲染和替换
"""

from typing import List, Dict, Any, Optional, Union
from find_tex import FindTeX, MathItem


class MathList:
    """数学表达式列表类"""
    
    def __init__(self):
        """初始化数学列表"""
        self.items = []
    
    def append(self, item):
        """添加数学项"""
        self.items.append(item)
    
    def clear(self):
        """清空列表"""
        self.items = []
    
    def render_input(self, document):
        """渲染所有数学项的输入"""
        for item in self.items:
            item.render_input(document)
        return self
    
    def convert(self, document):
        """转换所有数学项"""
        for item in self.items:
            item.convert(document)
        return self
    
    def render_output(self, document):
        """渲染所有数学项的输出"""
        for item in self.items:
            item.render_output(document)
        return self
    
    def update_document(self, document):
        """更新文档，替换所有数学项"""
        for item in self.items:
            item.update_document(document)
        return self
    
    def __len__(self):
        """获取列表长度"""
        return len(self.items)
    
    def __getitem__(self, index):
        """获取指定索引的数学项"""
        return self.items[index]


class MathDocument:
    """数学文档类"""
    
    def __init__(self, document, adaptor, options=None):
        """初始化数学文档
        
        参数:
            document: 文档对象
            adaptor: DOM适配器
            options: 选项字典
        """
        self.document = document
        self.adaptor = adaptor
        self.options = options or {}
        self.math = MathList()  # 找到的数学表达式
        self.processed = MathList()  # 已处理的数学表达式
        self.state = 0  # 文档状态：0=初始，1=已查找，2=已编译，3=已排版
        
        # 获取输入和输出Jax
        self.inputJax = self.options.get('InputJax', {})
        self.outputJax = self.options.get('OutputJax', {})
        
        # 默认选项
        self.find_options = {
            'elements': ['body'],
            'inlineMath': [['$', '$'], ['\\(', '\\)']],
            'displayMath': [['$$', '$$'], ['\\[', '\\]']]
        }
        # 更新选项
        if 'findOptions' in self.options:
            self.find_options.update(self.options['findOptions'])
    
    def find_math(self, options=None):
        """查找文档中的数学表达式
        
        参数:
            options: 查找选项
            
        返回:
            self，用于链式调用
        """
        if self.state >= 1:
            return self
        
        # 合并选项
        find_options = self.find_options.copy()
        if options:
            find_options.update(options)
        
        # 添加适配器
        find_options['adaptor'] = self.adaptor
        
        # 查找每个输入Jax的数学表达式
        for jax_name, jax in self.inputJax.items():
            found_items = jax.find_math(find_options)
            for item in found_items:
                # 创建MathItem对象
                math_item = MathItem(
                    item['math'],
                    jax,
                    item.get('display', False),
                    item.get('start', {}).get('n', 0),
                    item.get('end', {}).get('n', 0),
                    item.get('text', '')
                )
                # 设置节点引用
                math_item.start['node'] = item.get('start', {}).get('node')
                math_item.end['node'] = item.get('end', {}).get('node')
                # 添加到列表
                self.math.append(math_item)
        
        self.state = 1
        return self
    
    def compile(self):
        """编译所有数学表达式
        
        返回:
            self，用于链式调用
        """
        if self.state >= 2:
            return self
        
        # 确保已查找数学表达式
        self.find_math()
        
        # 编译所有数学表达式
        self.math.render_input(self)
        
        self.state = 2
        return self
    
    def typeset(self):
        """排版所有数学表达式
        
        返回:
            self，用于链式调用
        """
        if self.state >= 3:
            return self
        
        # 确保已编译
        self.compile()
        
        # 转换和渲染
        self.math.convert(self)
        self.math.render_output(self)
        
        self.state = 3
        return self
    
    def update_document(self):
        """更新文档，替换所有数学表达式
        
        返回:
            self，用于链式调用
        """
        if self.state < 3:
            self.typeset()
        
        # 替换所有数学表达式
        self.math.update_document(self)
        
        # 移动到已处理列表
        self.processed = self.math
        self.math = MathList()
        
        return self
    
    def clear(self):
        """清除所有数学表达式
        
        返回:
            self，用于链式调用
        """
        self.math.clear()
        self.state = 0
        return self
    
    def reset(self):
        """重置文档
        
        返回:
            self，用于链式调用
        """
        # 移除所有已渲染的数学表达式
        for item in self.processed.items:
            self._remove_math_item(item)
        
        # 清除列表
        self.processed.clear()
        self.math.clear()
        
        # 重置状态
        self.state = 0
        
        return self
    
    def _remove_math_item(self, item):
        """从文档中移除数学项
        
        参数:
            item: 要移除的数学项
        """
        if item.state < 3:
            return
        
        adaptor = self.adaptor
        node = item.start.node
        
        # 如果节点存在且有父节点
        if node and adaptor.parent(node):
            # 创建原始文本节点
            original_text = item.text or item.math
            if item.inputJax and hasattr(item.inputJax, 'name') and item.inputJax.name == 'TeX':
                # 对于TeX，添加分隔符
                if hasattr(item, 'delim') and item.delim:
                    original_text = item.delim.get('start', '') + original_text + item.delim.get('end', '')
                elif item.display:
                    # 默认分隔符
                    original_text = '$$' + original_text + '$$'
                else:
                    original_text = '$' + original_text + '$'
            
            # 创建文本节点
            text_node = adaptor.text(original_text)
            
            # 替换渲染节点
            adaptor.replace(text_node, node)
            
            # 更新节点引用
            item.start.node = item.end.node = text_node
            item.state = 0  # 重置状态


class HTMLOutputJax:
    """HTML输出Jax类"""
    
    def __init__(self, options=None):
        """初始化HTML输出Jax"""
        self.options = options or {}
        self.name = 'HTML'
    
    def convert(self, math_item, document):
        """将数学项转换为HTML
        
        参数:
            math_item: 数学项
            document: 文档
            
        返回:
            HTML元素
        """
        # 这里简化实现，实际应该根据内部表示生成HTML
        adaptor = document.adaptor
        
        # 创建容器
        container = adaptor.create('span', {'class': 'mjx-math'})
        
        # 创建行
        row = adaptor.create('span', {'class': 'mjx-mrow'})
        adaptor.append(container, row)
        
        # 简单处理：将数学表达式分割为单个字符，每个字符创建一个元素
        math_text = math_item.math
        for char in math_text:
            if char.isalpha():
                # 字母
                elem = adaptor.create('span', {'class': 'mjx-mi'})
                char_span = adaptor.create('span', {'class': 'mjx-char'})
                adaptor.append(elem, char_span)
                adaptor.append(char_span, adaptor.text(char))
            elif char.isdigit():
                # 数字
                elem = adaptor.create('span', {'class': 'mjx-mn'})
                char_span = adaptor.create('span', {'class': 'mjx-char'})
                adaptor.append(elem, char_span)
                adaptor.append(char_span, adaptor.text(char))
            elif char in '+-*/=':
                # 运算符
                elem = adaptor.create('span', {'class': 'mjx-mo'})
                char_span = adaptor.create('span', {'class': 'mjx-char'})
                adaptor.append(elem, char_span)
                adaptor.append(char_span, adaptor.text(char))
            else:
                # 其他字符
                elem = adaptor.create('span', {'class': 'mjx-mtext'})
                char_span = adaptor.create('span', {'class': 'mjx-char'})
                adaptor.append(elem, char_span)
                adaptor.append(char_span, adaptor.text(char))
            
            adaptor.append(row, elem)
        
        return container
    
    def render(self, math_item, document):
        """渲染数学项
        
        参数:
            math_item: 数学项
            document: 文档
        """
        # 这里简化实现，实际应该添加样式、处理布局等
        if math_item.display:
            # 显示模式：添加display属性
            adaptor = document.adaptor
            adaptor.setAttribute(math_item.typesetRoot, 'display', 'block')
        
        return math_item


# 示例用法
if __name__ == "__main__":
    from test_html_input import SimpleDOMAdaptor
    from find_tex import TeXInputJax
    
    # 测试HTML内容
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MathJax测试</title>
    </head>
    <body>
        <h1>MathJax测试</h1>
        <p>这是一个行内公式: $E = mc^2$，还有一个行内公式 \\(a^2 + b^2 = c^2\\)。</p>
        
        <p>这是一个行间公式:</p>
        <div>
            $$
            \\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}
            $$
        </div>
    </body>
    </html>
    """
    
    # 创建DOM适配器
    adaptor = SimpleDOMAdaptor(html_content)
    
    # 创建输入Jax
    tex_input_jax = TeXInputJax()
    
    # 创建输出Jax
    html_output_jax = HTMLOutputJax()
    
    # 创建文档
    document = MathDocument(
        adaptor.document,
        adaptor,
        {
            'InputJax': {'TeX': tex_input_jax},
            'OutputJax': html_output_jax
        }
    )
    
    # 查找、编译、排版和替换
    document.find_math()
    print(f"找到 {len(document.math)} 个数学表达式")
    
    document.compile()
    print("编译完成")
    
    document.typeset()
    print("排版完成")
    
    document.update_document()
    print("文档更新完成")
    
    # 重置文档
    document.reset()
    print("文档已重置") 