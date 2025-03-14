#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python版本的MathJax TeX查找器
基于core.js中的DOM遍历和查找数学表达式的逻辑
"""

import re
from typing import List, Dict, Any, Optional, Union, Tuple


class FindTeX:
    """查找TeX表达式的类"""
    
    OPTIONS = {
        'inlineMath': [['\\(', '\\)']],
        'displayMath': [['$$', '$$'], ['\\[', '\\]']],
        'processEscapes': True,
        'processEnvironments': True,
        'processRefs': True,
        'skipTags': ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
        'ignoreClass': 'tex2jax_ignore',
        'processClass': 'tex2jax_process',
        'elements': ['body']
    }
    
    def __init__(self, options=None):
        """初始化FindTeX"""
        self.options = self.OPTIONS.copy()
        if options:
            self.options.update(options)
        self._compile_patterns()
    
    def _compile_patterns(self):
        """编译正则表达式模式"""
        # 内联数学表达式模式
        inline_patterns = []
        for start, end in self.options['inlineMath']:
            # 转义特殊字符
            start_escaped = re.escape(start)
            end_escaped = re.escape(end)
            # 创建模式
            pattern = f"{start_escaped}(.*?){end_escaped}"
            inline_patterns.append(pattern)
        
        # 显示数学表达式模式
        display_patterns = []
        for start, end in self.options['displayMath']:
            # 转义特殊字符
            start_escaped = re.escape(start)
            end_escaped = re.escape(end)
            # 创建模式
            pattern = f"{start_escaped}(.*?){end_escaped}"
            display_patterns.append(pattern)
        
        # 编译正则表达式
        self.inline_pattern = re.compile('|'.join(inline_patterns), re.DOTALL)
        self.display_pattern = re.compile('|'.join(display_patterns), re.DOTALL)
        
        # 环境模式 (如果启用)
        if self.options['processEnvironments']:
            self.environment_pattern = re.compile(
                r'\\begin\{([^}]*)\}(.*?)\\end\{\1\}', 
                re.DOTALL
            )
        else:
            self.environment_pattern = None
        
        # 转义模式 (如果启用)
        if self.options['processEscapes']:
            self.escape_pattern = re.compile(r'\\([\\$])')
        else:
            self.escape_pattern = None
        
        # 引用模式 (如果启用)
        if self.options['processRefs']:
            self.ref_pattern = re.compile(r'\\(eq)?ref\{([^}]*)\}')
        else:
            self.ref_pattern = None
    
    def find_math(self, options=None):
        """查找文档中的数学表达式
        
        参数:
            options: 查找选项
            
        返回:
            数学表达式列表
        """
        options = options or {}
        # 合并选项
        search_options = self.options.copy()
        search_options.update(options)
        
        # 获取要处理的元素
        adaptor = search_options.get('adaptor')
        if not adaptor:
            raise ValueError("No adaptor specified")
        
        document = adaptor.document
        elements = adaptor.getElements(
            search_options.get('elements', ['body']), 
            document
        )
        
        # 查找数学表达式
        items = []
        for element in elements:
            self._find_math_in_element(element, items, search_options, adaptor)
        
        return items
    
    def _find_math_in_element(self, element, items, options, adaptor):
        """在元素中查找数学表达式
        
        参数:
            element: DOM元素
            items: 数学表达式列表
            options: 查找选项
            adaptor: DOM适配器
        """
        # 检查是否应该忽略此元素
        if self._should_ignore(element, options, adaptor):
            return
        
        # 处理元素的子节点
        for child in adaptor.childNodes(element):
            kind = adaptor.kind(child)
            
            # 文本节点
            if kind == '#text':
                self._find_math_in_text(child, items, options, adaptor)
            
            # 元素节点
            elif kind not in options.get('skipTags', []):
                self._find_math_in_element(child, items, options, adaptor)
    
    def _should_ignore(self, element, options, adaptor):
        """检查是否应该忽略此元素
        
        参数:
            element: DOM元素
            options: 查找选项
            adaptor: DOM适配器
            
        返回:
            是否应该忽略
        """
        # 检查标签名
        if adaptor.kind(element) in options.get('skipTags', []):
            return True
        
        # 检查类名
        ignore_class = options.get('ignoreClass')
        process_class = options.get('processClass')
        
        if ignore_class and adaptor.hasClass(element, ignore_class):
            return True
        
        if process_class and not adaptor.hasClass(element, process_class):
            parent = adaptor.parent(element)
            while parent and adaptor.kind(parent) != 'body':
                if adaptor.hasClass(parent, process_class):
                    return False
                if adaptor.hasClass(parent, ignore_class):
                    return True
                parent = adaptor.parent(parent)
            
            # 如果没有找到processClass，则忽略
            if process_class:
                return True
        
        return False
    
    def _find_math_in_text(self, node, items, options, adaptor):
        """在文本节点中查找数学表达式
        
        参数:
            node: 文本节点
            items: 数学表达式列表
            options: 查找选项
            adaptor: DOM适配器
        """
        text = adaptor.value(node)
        
        # 查找内联数学表达式
        for match in self.inline_pattern.finditer(text):
            start, end = match.span()
            math = match.group(1)
            
            # 创建数学项
            item = {
                'math': math,
                'display': False,
                'start': {'node': node, 'n': start},
                'end': {'node': node, 'n': end},
                'delim': {'start': text[start:start+len(match.group(0))-len(math)], 
                          'end': text[end-len(match.group(0))+len(math):end]}
            }
            items.append(item)
        
        # 查找显示数学表达式
        for match in self.display_pattern.finditer(text):
            start, end = match.span()
            math = match.group(1)
            
            # 创建数学项
            item = {
                'math': math,
                'display': True,
                'start': {'node': node, 'n': start},
                'end': {'node': node, 'n': end},
                'delim': {'start': text[start:start+len(match.group(0))-len(math)], 
                          'end': text[end-len(match.group(0))+len(math):end]}
            }
            items.append(item)
        
        # 查找环境 (如果启用)
        if self.environment_pattern:
            for match in self.environment_pattern.finditer(text):
                start, end = match.span()
                env = match.group(1)
                math = match.group(2)
                
                # 创建数学项
                item = {
                    'math': f"\\begin{{{env}}}{math}\\end{{{env}}}",
                    'display': True,
                    'start': {'node': node, 'n': start},
                    'end': {'node': node, 'n': end},
                    'delim': {'start': '', 'end': ''}
                }
                items.append(item)
        
        # 处理转义字符 (如果启用)
        if self.escape_pattern and options.get('processEscapes'):
            for match in self.escape_pattern.finditer(text):
                start, end = match.span()
                escaped = match.group(1)
                
                # 替换转义字符
                if escaped in ['\\', '$']:
                    # 这里简化处理，实际应该修改DOM
                    pass
        
        # 处理引用 (如果启用)
        if self.ref_pattern and options.get('processRefs'):
            for match in self.ref_pattern.finditer(text):
                start, end = match.span()
                ref_type = match.group(1) or ''
                ref_id = match.group(2)
                
                # 处理引用
                # 这里简化处理，实际应该查找引用的公式
                pass
    
    def find_math_in_string(self, text):
        """在字符串中查找数学表达式
        
        参数:
            text: 文本字符串
            
        返回:
            数学表达式列表
        """
        results = []
        
        # 查找内联数学表达式
        for match in self.inline_pattern.finditer(text):
            start, end = match.span()
            # 获取匹配的数学表达式，处理可能为None的情况
            math = match.group(1) if match.group(1) is not None else ""
            # 计算分隔符
            full_match = match.group(0) or ""
            start_delim = text[start:start+len(full_match)-len(math)] if math else text[start:start]
            end_delim = text[end-len(full_match)+len(math):end] if math else text[end:end]
            
            results.append({
                'math': math,
                'start': start,
                'end': end,
                'display': False,
                'delim': {'start': start_delim, 'end': end_delim}
            })
        
        # 查找显示数学表达式
        for match in self.display_pattern.finditer(text):
            start, end = match.span()
            # 获取匹配的数学表达式，处理可能为None的情况
            math = match.group(1) if match.group(1) is not None else ""
            # 计算分隔符
            full_match = match.group(0) or ""
            start_delim = text[start:start+len(full_match)-len(math)] if math else text[start:start]
            end_delim = text[end-len(full_match)+len(math):end] if math else text[end:end]
            
            results.append({
                'math': math,
                'start': start,
                'end': end,
                'display': True,
                'delim': {'start': start_delim, 'end': end_delim}
            })
        
        # 查找环境 (如果启用)
        if self.environment_pattern:
            for match in self.environment_pattern.finditer(text):
                start, end = match.span()
                env = match.group(1) or ""
                math = match.group(2) or ""
                
                results.append({
                    'math': f"\\begin{{{env}}}{math}\\end{{{env}}}",
                    'start': start,
                    'end': end,
                    'display': True,
                    'delim': {'start': '', 'end': ''}
                })
        
        # 按开始位置排序
        results.sort(key=lambda x: x['start'])
        return results


class TeXInputJax:
    """TeX输入Jax类"""
    
    def __init__(self, options=None):
        """初始化TeX输入Jax"""
        self.options = {}
        if options:
            self.options.update(options)
        
        # 创建FindTeX实例
        find_tex_options = {}
        for key, value in self.options.items():
            if key in FindTeX.OPTIONS:
                find_tex_options[key] = value
        
        self.find_tex = FindTeX(find_tex_options)
        self.name = 'TeX'
    
    def find_math(self, options=None):
        """查找数学表达式
        
        参数:
            options: 查找选项
            
        返回:
            数学表达式列表
        """
        return self.find_tex.find_math(options)
    
    def compile(self, math, document):
        """编译数学表达式
        
        参数:
            math: 数学表达式
            document: 文档
            
        返回:
            编译后的表达式
        """
        # 这里简化实现，实际应该解析TeX并生成内部表示
        return {'type': 'math', 'math': math, 'mode': 'display' if math.get('display') else 'inline'}


class MathItem:
    """表示单个数学表达式的类"""
    
    def __init__(self, math, jax, display=False, start=0, end=0, text=''):
        """初始化数学项"""
        self.math = math  # 原始数学表达式
        self.inputJax = jax  # 输入Jax
        self.display = display  # 是否为显示模式
        self.start = {'node': None, 'n': start}  # 开始位置
        self.end = {'node': None, 'n': end}  # 结束位置
        self.text = text  # 原始文本
        self.state = 0  # 状态：0=初始，1=已编译，2=已转换，3=已渲染
        self.root = None  # 内部表示
        self.typesetRoot = None  # 渲染结果
    
    def render_input(self, document):
        """渲染输入（编译阶段）"""
        if self.state >= 1:
            return
        
        self.root = self.inputJax.compile(self, document)
        self.state = 1
        return self
    
    def convert(self, document, end_state=3):
        """转换（转换阶段）"""
        if self.state >= 2:
            return
        
        self.render_input(document)
        # 转换为输出格式
        self.typesetRoot = document.outputJax.convert(self, document)
        self.state = 2
        return self
    
    def render_output(self, document):
        """渲染输出（渲染阶段）"""
        if self.state >= 3:
            return
        
        self.convert(document)
        # 最终渲染
        document.outputJax.render(self, document)
        self.state = 3
        return self
    
    def update_document(self, document):
        """更新文档（替换阶段）"""
        if self.state < 3:
            self.render_output(document)
        
        adaptor = document.adaptor
        node = self.start.node
        parent = adaptor.parent(node)
        
        # 创建包含渲染结果的元素
        container = adaptor.create('span', {'class': 'mjx-container'})
        adaptor.append(container, self.typesetRoot)
        
        # 替换原始节点
        adaptor.replace(container, node)
        
        # 更新节点引用
        self.start.node = self.end.node = container
        
        return self


# 示例用法
if __name__ == "__main__":
    # 创建FindTeX实例
    find_tex = FindTeX()
    
    # 在字符串中查找数学表达式
    text = """
    这是一个行内公式: $E = mc^2$，还有一个行内公式 \\(a^2 + b^2 = c^2\\)。
    
    这是一个行间公式:
    $$
    \\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}
    $$  
    
    还有一个行间公式:
    \\[
    \\frac{d}{dx}\\left( \\int_{a}^{x} f(t) dt \\right) = f(x)
    \\]
    
    这是一个环境:
    \\begin{align}
    a &= b + c \\\\
    &= d + e
    \\end{align}
    """
    
    results = find_tex.find_math_in_string(text)
    
    # 打印结果
    for i, result in enumerate(results):
        print(f"公式 {i+1}:")
        print(f"  类型: {'显示' if result['display'] else '行内'}")
        print(f"  位置: {result['start']} - {result['end']}")
        print(f"  公式: {result['math']}")
        print() 