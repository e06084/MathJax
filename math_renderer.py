#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python版本的MathJax渲染器
实现数学表达式的渲染和替换过程
"""

class MathRenderer:
    """数学表达式渲染器类"""
    
    def __init__(self, document, options=None):
        """初始化渲染器
        
        参数:
            document: MathDocument实例
            options: 渲染选项
        """
        self.document = document
        self.options = options or {}
        self.adaptor = document.adaptor
    
    def render(self):
        """渲染文档中的所有数学表达式
        
        返回:
            self，用于链式调用
        """
        # 确保文档已排版
        self.document.typeset()
        
        # 更新文档
        self.document.update_document()
        
        return self
    
    def render_math_item(self, math_item):
        """渲染单个数学表达式
        
        参数:
            math_item: 要渲染的数学项
            
        返回:
            渲染后的DOM元素
        """
        # 确保数学项已转换
        if math_item.state < 2:
            math_item.convert(self.document)
        
        # 创建容器元素
        container = self.create_container(math_item)
        
        # 添加渲染结果
        self.adaptor.append(container, math_item.typesetRoot)
        
        # 替换原始节点
        self.replace_node(math_item, container)
        
        return container
    
    def create_container(self, math_item):
        """创建数学表达式的容器元素
        
        参数:
            math_item: 数学项
            
        返回:
            容器元素
        """
        # 创建容器
        container_attrs = {
            'class': 'mjx-container',
            'jax': math_item.inputJax.name,
            'display': 'true' if math_item.display else 'false'
        }
        
        # 添加其他属性
        if math_item.display:
            container_attrs['role'] = 'presentation'
            container_attrs['style'] = 'display: block; text-align: center;'
        else:
            container_attrs['role'] = 'presentation'
            container_attrs['style'] = 'display: inline;'
        
        # 创建元素
        container = self.adaptor.create('span', container_attrs)
        
        return container
    
    def replace_node(self, math_item, container):
        """用渲染后的元素替换原始节点
        
        参数:
            math_item: 数学项
            container: 渲染后的容器元素
        """
        node = math_item.start.node
        
        # 如果节点存在且有父节点
        if node and self.adaptor.parent(node):
            # 替换节点
            self.adaptor.replace(container, node)
            
            # 更新节点引用
            math_item.start.node = math_item.end.node = container
            math_item.state = 3  # 更新状态为已渲染
    
    def remove_math(self, math_item):
        """移除已渲染的数学表达式，恢复原始文本
        
        参数:
            math_item: 要移除的数学项
        """
        if math_item.state < 3:
            return
        
        node = math_item.start.node
        
        # 如果节点存在且有父节点
        if node and self.adaptor.parent(node):
            # 创建原始文本
            original_text = self.get_original_text(math_item)
            
            # 创建文本节点
            text_node = self.adaptor.text(original_text)
            
            # 替换渲染节点
            self.adaptor.replace(text_node, node)
            
            # 更新节点引用
            math_item.start.node = math_item.end.node = text_node
            math_item.state = 0  # 重置状态
    
    def get_original_text(self, math_item):
        """获取数学项的原始文本
        
        参数:
            math_item: 数学项
            
        返回:
            原始文本
        """
        # 使用保存的原始文本
        if math_item.text:
            return math_item.text
        
        # 重建原始文本
        original_text = math_item.math
        
        # 添加分隔符
        if hasattr(math_item.inputJax, 'name') and math_item.inputJax.name == 'TeX':
            if hasattr(math_item, 'delim') and math_item.delim:
                start_delim = math_item.delim.get('start', '')
                end_delim = math_item.delim.get('end', '')
                original_text = start_delim + original_text + end_delim
            elif math_item.display:
                # 默认显示模式分隔符
                original_text = '$$' + original_text + '$$'
            else:
                # 默认行内模式分隔符
                original_text = '$' + original_text + '$'
        
        return original_text


class HTMLRenderer(MathRenderer):
    """HTML渲染器类"""
    
    def create_container(self, math_item):
        """创建HTML容器元素
        
        参数:
            math_item: 数学项
            
        返回:
            HTML容器元素
        """
        # 调用父类方法创建基本容器
        container = super().create_container(math_item)
        
        # 添加HTML特定属性
        self.adaptor.setAttribute(container, 'format', 'html')
        
        # 添加可访问性属性
        if math_item.display:
            self.adaptor.setAttribute(container, 'aria-hidden', 'true')
        
        return container
    
    def add_styles(self, container, math_item):
        """添加样式到容器
        
        参数:
            container: 容器元素
            math_item: 数学项
        """
        # 获取样式选项
        styles = self.options.get('styles', {})
        
        # 设置基本样式
        base_style = 'font-family: MathJax_Math, MathJax_Main, MathJax_Size2;'
        
        if math_item.display:
            # 显示模式样式
            display_style = 'margin: 1em 0;'
            self.adaptor.setAttribute(
                container, 
                'style', 
                base_style + display_style + styles.get('display', '')
            )
        else:
            # 行内模式样式
            inline_style = 'vertical-align: -0.25em;'
            self.adaptor.setAttribute(
                container, 
                'style', 
                base_style + inline_style + styles.get('inline', '')
            )
    
    def render_math_item(self, math_item):
        """渲染单个数学表达式为HTML
        
        参数:
            math_item: 要渲染的数学项
            
        返回:
            渲染后的HTML元素
        """
        # 创建容器
        container = self.create_container(math_item)
        
        # 添加样式
        self.add_styles(container, math_item)
        
        # 添加渲染结果
        self.adaptor.append(container, math_item.typesetRoot)
        
        # 替换原始节点
        self.replace_node(math_item, container)
        
        # 添加事件监听器（如果需要）
        if self.options.get('addEventListeners', False):
            self.add_event_listeners(container, math_item)
        
        return container
    
    def add_event_listeners(self, container, math_item):
        """添加事件监听器到容器
        
        参数:
            container: 容器元素
            math_item: 数学项
        """
        # 这里简化实现，实际应该添加点击、悬停等事件
        pass


class SVGRenderer(MathRenderer):
    """SVG渲染器类"""
    
    def create_container(self, math_item):
        """创建SVG容器元素
        
        参数:
            math_item: 数学项
            
        返回:
            SVG容器元素
        """
        # 调用父类方法创建基本容器
        container = super().create_container(math_item)
        
        # 添加SVG特定属性
        self.adaptor.setAttribute(container, 'format', 'svg')
        
        return container


# 示例用法
if __name__ == "__main__":
    # 这里需要导入其他模块才能运行示例
    print("MathJax渲染器模块") 