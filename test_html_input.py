#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试FindTeX处理HTML输入的脚本
"""

from lxml import html, etree
from find_tex import FindTeX


class SimpleDOMAdaptor:
    """简单的DOM适配器，用于测试"""
    
    def __init__(self, html_content):
        """初始化适配器"""
        self.document = html.fromstring(html_content)
    
    def getElements(self, selectors, document):
        """根据选择器获取元素"""
        result = []
        for selector in selectors:
            if selector == 'body':
                # 获取body元素
                body = document.xpath('//body')
                if body:
                    result.extend(body)
            else:
                # 使用CSS选择器
                try:
                    elements = document.cssselect(selector)
                    if elements:
                        result.extend(elements)
                except Exception:
                    # 如果cssselect不可用，尝试使用xpath
                    try:
                        elements = document.xpath(f'//{selector}')
                        if elements:
                            result.extend(elements)
                    except Exception:
                        pass
        return result
    
    def childNodes(self, element):
        """获取所有子节点"""
        if isinstance(element, etree._Element):
            # 获取元素子节点和文本节点
            children = []
            for child in element.getchildren():
                children.append(child)
            
            # 获取文本节点
            if element.text:
                children.append(element.text)
            
            # 获取元素之间的文本
            for child in element.getchildren():
                if child.tail:
                    children.append(child.tail)
            
            return children
        return []
    
    def kind(self, node):
        """获取节点类型"""
        if isinstance(node, etree._Element):
            return node.tag.lower()  # 返回小写标签名
        elif isinstance(node, str):
            return '#text'
        return ''
    
    def value(self, node):
        """获取节点值"""
        if isinstance(node, str):
            return node
        elif isinstance(node, etree._Element):
            if node.text:
                return node.text
        return ''
    
    def hasClass(self, element, class_name):
        """检查元素是否有指定的类"""
        if isinstance(element, etree._Element):
            classes = element.get('class', '').split()
            return class_name in classes
        return False
    
    def parent(self, node):
        """获取父节点"""
        if isinstance(node, etree._Element):
            return node.getparent()
        # 对于文本节点，我们无法直接获取父节点
        # 这里简化处理，实际应该保存文本节点与其父节点的关系
        return None


def find_math_in_html(html_content):
    """在HTML内容中查找数学表达式
    
    参数:
        html_content: HTML内容
        
    返回:
        数学表达式列表
    """
    # 创建FindTeX实例，直接使用字符串查找
    find_tex = FindTeX()
    
    # 提取所有文本节点的内容
    text_content = extract_text_from_html(html_content)
    
    # 直接在文本中查找数学表达式
    return find_tex.find_math_in_string(text_content)


def extract_text_from_html(html_content):
    """从HTML中提取所有文本内容
    
    参数:
        html_content: HTML内容
        
    返回:
        文本内容
    """
    # 解析HTML
    tree = html.fromstring(html_content)
    
    # 提取所有文本
    text_parts = []
    
    # 递归提取文本
    def extract_text(element):
        # 添加元素开始的文本
        if element.text and element.text.strip():
            text_parts.append(element.text)
        
        # 处理子元素
        for child in element.getchildren():
            extract_text(child)
            # 添加子元素后的文本
            if child.tail and child.tail.strip():
                text_parts.append(child.tail)
    
    # 从body开始提取
    body = tree.xpath('//body')
    if body:
        extract_text(body[0])
    
    # 合并所有文本，确保数学表达式不被分割
    return ' '.join(text_parts)


def main():
    """主函数"""
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
        
        <p>还有一个行间公式:</p>
        <div>
            \\[
            \\frac{d}{dx}\\left( \\int_{a}^{x} f(t) dt \\right) = f(x)
            \\]
        </div>
        
        <p>这是一个环境:</p>
        <div>
            \\begin{align}
            a &= b + c \\\\
            &= d + e
            \\end{align}
        </div>
        
        <div class="tex2jax_ignore">
            <p>这个区域会被忽略: $E = mc^2$</p>
        </div>
        
        <div class="tex2jax_process">
            <p>这个区域会被处理: $F = ma$</p>
        </div>
    </body>
    </html>
    """
    
    # 查找数学表达式
    math_items = find_math_in_html(html_content)
    
    # 打印结果
    print(f"找到 {len(math_items)} 个数学表达式:")
    for i, item in enumerate(math_items):
        print(f"公式 {i+1}:")
        print(f"  类型: {'显示' if item.get('display') else '行内'}")
        print(f"  公式: {item.get('math')}")
        print()
    
    # 打印提取的文本内容，用于调试
    print("提取的文本内容:")
    text_content = extract_text_from_html(html_content)
    print(text_content)


if __name__ == "__main__":
    main() 