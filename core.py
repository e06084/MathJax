#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python版本的MathJax核心功能
基于es5/core.js转换而来
"""

import re
import json
import lxml.html
from lxml.etree import HTMLParser
from abc import ABC, abstractmethod
from typing import Optional


class DOMAdaptor(ABC):
    """DOM适配器的抽象基类"""
    
    def __init__(self, document):
        """初始化DOM适配器"""
        self.document = document
    
    @abstractmethod
    def parse(self, text: str, format: str = "text/html"):
        """解析HTML或XML文本"""
        pass
    
    @abstractmethod
    def create(self, tag: str, ns: Optional[str] = None):
        """创建DOM元素"""
        pass
    
    @abstractmethod
    def text(self, text: str):
        """创建文本节点"""
        pass
    
    @abstractmethod
    def head(self, doc):
        """获取文档的head元素"""
        pass
    
    @abstractmethod
    def body(self, doc):
        """获取文档的body元素"""
        pass
    
    @abstractmethod
    def root(self, doc):
        """获取文档的根元素"""
        pass
    
    @abstractmethod
    def doctype(self, doc):
        """获取文档的DOCTYPE"""
        pass
    
    @abstractmethod
    def tags(self, node, name: str, ns: Optional[str] = None):
        """获取指定标签名的元素"""
        pass
    
    @abstractmethod
    def getElements(self, selectors, document):
        """根据选择器获取元素"""
        pass
    
    @abstractmethod
    def contains(self, node1, node2):
        """检查node1是否包含node2"""
        pass
    
    @abstractmethod
    def parent(self, node):
        """获取节点的父节点"""
        pass
    
    @abstractmethod
    def append(self, node, child):
        """将child添加到node的子节点末尾"""
        pass
    
    @abstractmethod
    def insert(self, node, child):
        """将node插入到child之前"""
        pass
    
    @abstractmethod
    def remove(self, node):
        """移除节点"""
        pass
    
    @abstractmethod
    def replace(self, new_node, old_node):
        """用new_node替换old_node"""
        pass
    
    @abstractmethod
    def clone(self, node):
        """克隆节点"""
        pass
    
    @abstractmethod
    def split(self, node, position):
        """分割文本节点"""
        pass
    
    @abstractmethod
    def next(self, node):
        """获取下一个兄弟节点"""
        pass
    
    @abstractmethod
    def previous(self, node):
        """获取上一个兄弟节点"""
        pass
    
    @abstractmethod
    def firstChild(self, node):
        """获取第一个子节点"""
        pass
    
    @abstractmethod
    def lastChild(self, node):
        """获取最后一个子节点"""
        pass
    
    @abstractmethod
    def childNodes(self, node):
        """获取所有子节点"""
        pass
    
    @abstractmethod
    def childNode(self, node, i):
        """获取第i个子节点"""
        pass
    
    @abstractmethod
    def kind(self, node):
        """获取节点类型"""
        pass
    
    @abstractmethod
    def value(self, node):
        """获取节点值"""
        pass
    
    @abstractmethod
    def textContent(self, node):
        """获取节点的文本内容"""
        pass
    
    @abstractmethod
    def innerHTML(self, node):
        """获取节点的HTML内容"""
        pass
    
    @abstractmethod
    def outerHTML(self, node):
        """获取节点的外部HTML"""
        pass
    
    @abstractmethod
    def serializeXML(self, node):
        """将节点序列化为XML"""
        pass
    
    @abstractmethod
    def setAttribute(self, node, name, value, ns=None):
        """设置属性"""
        pass
    
    @abstractmethod
    def getAttribute(self, node, name):
        """获取属性"""
        pass
    
    @abstractmethod
    def removeAttribute(self, node, name):
        """移除属性"""
        pass
    
    @abstractmethod
    def hasAttribute(self, node, name):
        """检查是否有属性"""
        pass
    
    @abstractmethod
    def allAttributes(self, node):
        """获取所有属性"""
        pass
    
    @abstractmethod
    def addClass(self, node, name):
        """添加类"""
        pass
    
    @abstractmethod
    def removeClass(self, node, name):
        """移除类"""
        pass
    
    @abstractmethod
    def hasClass(self, node, name):
        """检查是否有类"""
        pass
    
    @abstractmethod
    def setStyle(self, node, name, value):
        """设置样式"""
        pass
    
    @abstractmethod
    def getStyle(self, node, name):
        """获取样式"""
        pass
    
    @abstractmethod
    def allStyles(self, node):
        """获取所有样式"""
        pass
    
    @abstractmethod
    def fontSize(self, node):
        """获取字体大小"""
        pass
    
    @abstractmethod
    def fontFamily(self, node):
        """获取字体族"""
        pass
    
    @abstractmethod
    def nodeSize(self, node):
        """获取节点尺寸"""
        pass
    
    @abstractmethod
    def nodeBBox(self, node):
        """获取节点边界框"""
        pass


class HTMLAdaptor(DOMAdaptor):
    """HTML适配器，用于浏览器环境"""
    
    def __init__(self, window):
        """初始化HTML适配器"""
        super().__init__(window.document)
        self.window = window
        self.parser = window.DOMParser()
    
    def parse(self, text, format="text/html"):
        """解析HTML或XML文本"""
        return self.parser.parseFromString(text, format)
    
    def create(self, tag, ns=None):
        """创建DOM元素"""
        if ns:
            return self.document.createElementNS(ns, tag)
        return self.document.createElement(tag)
    
    def text(self, text):
        """创建文本节点"""
        return self.document.createTextNode(text)
    
    def head(self, doc):
        """获取文档的head元素"""
        return doc.head or doc
    
    def body(self, doc):
        """获取文档的body元素"""
        return doc.body or doc
    
    def root(self, doc):
        """获取文档的根元素"""
        return doc.documentElement or doc
    
    def doctype(self, doc):
        """获取文档的DOCTYPE"""
        if doc.doctype:
            return f"<!DOCTYPE {doc.doctype.name}>"
        return ""
    
    def tags(self, node, name, ns=None):
        """获取指定标签名的元素"""
        if ns:
            elements = node.getElementsByTagNameNS(ns, name)
        else:
            elements = node.getElementsByTagName(name)
        return list(elements)
    
    def getElements(self, selectors, document):
        """根据选择器获取元素"""
        result = []
        for selector in selectors:
            if isinstance(selector, str):
                elements = document.querySelectorAll(selector)
                result.extend(list(elements))
            elif isinstance(selector, (list, tuple)) or hasattr(selector, '__iter__'):
                result.extend(list(selector))
            else:
                result.append(selector)
        return result
    
    def contains(self, node1, node2):
        """检查node1是否包含node2"""
        return node1.contains(node2)
    
    def parent(self, node):
        """获取节点的父节点"""
        return node.parentNode
    
    def append(self, node, child):
        """将child添加到node的子节点末尾"""
        return node.appendChild(child)
    
    def insert(self, node, child):
        """将node插入到child之前"""
        return self.parent(child).insertBefore(node, child)
    
    def remove(self, node):
        """移除节点"""
        return self.parent(node).removeChild(node)
    
    def replace(self, new_node, old_node):
        """用new_node替换old_node"""
        return self.parent(old_node).replaceChild(new_node, old_node)
    
    def clone(self, node):
        """克隆节点"""
        return node.cloneNode(True)
    
    def split(self, node, position):
        """分割文本节点"""
        return node.splitText(position)
    
    def next(self, node):
        """获取下一个兄弟节点"""
        return node.nextSibling
    
    def previous(self, node):
        """获取上一个兄弟节点"""
        return node.previousSibling
    
    def firstChild(self, node):
        """获取第一个子节点"""
        return node.firstChild
    
    def lastChild(self, node):
        """获取最后一个子节点"""
        return node.lastChild
    
    def childNodes(self, node):
        """获取所有子节点"""
        return list(node.childNodes)
    
    def childNode(self, node, i):
        """获取第i个子节点"""
        return node.childNodes[i]
    
    def kind(self, node):
        """获取节点类型"""
        node_type = node.nodeType
        if node_type in (1, 3, 8):  # 元素、文本或注释节点
            return node.nodeName.lower()
        return ""
    
    def value(self, node):
        """获取节点值"""
        return node.nodeValue or ""
    
    def textContent(self, node):
        """获取节点的文本内容"""
        return node.textContent
    
    def innerHTML(self, node):
        """获取节点的HTML内容"""
        return node.innerHTML
    
    def outerHTML(self, node):
        """获取节点的外部HTML"""
        return node.outerHTML
    
    def serializeXML(self, node):
        """将节点序列化为XML"""
        return self.window.XMLSerializer().serializeToString(node)
    
    def setAttribute(self, node, name, value, ns=None):
        """设置属性"""
        if ns:
            name = f"{ns.split('/')[-1]}:{name.split(':')[-1]}"
            return node.setAttributeNS(ns, name, value)
        return node.setAttribute(name, value)
    
    def getAttribute(self, node, name):
        """获取属性"""
        return node.getAttribute(name)
    
    def removeAttribute(self, node, name):
        """移除属性"""
        return node.removeAttribute(name)
    
    def hasAttribute(self, node, name):
        """检查是否有属性"""
        return node.hasAttribute(name)
    
    def allAttributes(self, node):
        """获取所有属性"""
        return [{"name": attr.name, "value": attr.value} for attr in node.attributes]
    
    def addClass(self, node, name):
        """添加类"""
        if hasattr(node, 'classList'):
            node.classList.add(name)
        else:
            node.className = (node.className + " " + name).strip()
    
    def removeClass(self, node, name):
        """移除类"""
        if hasattr(node, 'classList'):
            node.classList.remove(name)
        else:
            classes = node.className.split()
            node.className = " ".join(c for c in classes if c != name)
    
    def hasClass(self, node, name):
        """检查是否有类"""
        if hasattr(node, 'classList'):
            return node.classList.contains(name)
        else:
            classes = node.className.split()
            return name in classes
    
    def setStyle(self, node, name, value):
        """设置样式"""
        node.style[name] = value
    
    def getStyle(self, node, name):
        """获取样式"""
        return self.window.getComputedStyle(node)[name]
    
    def allStyles(self, node):
        """获取所有样式"""
        styles = {}
        computed_style = self.window.getComputedStyle(node)
        for i in range(computed_style.length):
            name = computed_style[i]
            styles[name] = computed_style.getPropertyValue(name)
        return styles
    
    def fontSize(self, node):
        """获取字体大小"""
        return parseFloat(self.getStyle(node, 'fontSize'))
    
    def fontFamily(self, node):
        """获取字体族"""
        return self.getStyle(node, 'fontFamily')
    
    def nodeSize(self, node):
        """获取节点尺寸"""
        return {
            'width': node.offsetWidth,
            'height': node.offsetHeight
        }
    
    def nodeBBox(self, node):
        """获取节点边界框"""
        rect = node.getBoundingClientRect()
        return {
            'left': rect.left,
            'right': rect.right,
            'top': rect.top,
            'bottom': rect.bottom,
            'width': rect.width,
            'height': rect.height
        }


class Options:
    """选项管理类"""
    
    @staticmethod
    def defaults(options, defaults):
        """设置默认选项"""
        for key, value in defaults.items():
            if key not in options:
                options[key] = value
            elif isinstance(value, dict) and isinstance(options[key], dict):
                Options.defaults(options[key], value)
        return options
    
    @staticmethod
    def user_options(options, user_options):
        """应用用户选项"""
        for key, value in user_options.items():
            if isinstance(value, dict) and key in options and isinstance(options[key], dict):
                Options.user_options(options[key], value)
            else:
                options[key] = value
        return options
    
    @staticmethod
    def separate_options(options, allowed_options, *other_allowed):
        """分离选项"""
        result = [{}, {}, {}]
        
        # 处理第一个选项集
        for key, value in options.items():
            if key in allowed_options:
                result[0][key] = value
            else:
                found = False
                for i, allowed in enumerate(other_allowed):
                    if key in allowed:
                        result[i + 1][key] = value
                        found = True
                        break
                if not found:
                    result[0][key] = value
        
        return result


class MathItem:
    """数学项类"""
    
    def __init__(self, math, jax, display=False, start=0, end=0, text=""):
        """初始化数学项"""
        self.math = math
        self.jax = jax
        self.display = display
        self.start = start
        self.end = end
        self.text = text
        self.state = 0
        self.styles = {}
        self.metrics = {}
        self.data = {}
        self.root = None
        self.typesetRoot = None
        self.outputData = None
    
    def render_input(self, document):
        """渲染输入"""
        if self.state >= 1:
            return
        self.root = self.jax.input.compile(self, document)
        self.state = 1
        return self
    
    def convert(self, document):
        """转换"""
        if self.state >= 2:
            return
        this.render_input(document)
        this.root = this.jax.convert(this, document)
        this.state = 2
        return this
    
    def render_output(self, document):
        """渲染输出"""
        if self.state >= 3:
            return
        this.convert(document)
        this.typesetRoot = this.jax.output.typeset(this, document)
        this.state = 3
        return this
    
    def reset(self):
        """重置状态"""
        this.state = 0
        this.root = this.typesetRoot = this.outputData = None
        return this


class MathList:
    """数学列表类"""
    
    def __init__(self, items=None):
        """初始化数学列表"""
        self.items = items or []
    
    def render_input(self, document):
        """渲染所有项的输入"""
        for item in self.items:
            item.render_input(document)
        return self
    
    def convert(self, document):
        """转换所有项"""
        for item in self.items:
            item.convert(document)
        return self
    
    def render_output(self, document):
        """渲染所有项的输出"""
        for item in self.items:
            item.render_output(document)
        return self
    
    def reset(self):
        """重置所有项"""
        for item in self.items:
            item.reset()
        return self
    
    def clear(self):
        """清空列表"""
        self.items = []
        return self
    
    def add(self, *items):
        """添加项"""
        self.items.extend(items)
        return self
    
    def append(self, item):
        """追加项"""
        self.items.append(item)
        return self


class MathDocument:
    """数学文档类"""
    
    def __init__(self, document, adaptor, options=None):
        """初始化数学文档"""
        self.document = document
        self.adaptor = adaptor
        self.options = options or {}
        self.math = MathList()
        self.processed = MathList()
        self.state = 0
    
    def find_math(self, options=None):
        """查找数学表达式"""
        if self.state >= 1:
            return
        
        options = options or {}
        for jax_name, jax in self.options.get('InputJax', {}).items():
            found = jax.find_math(options)
            for math_item in found:
                self.math.append(MathItem(
                    math_item['math'],
                    jax,
                    math_item.get('display', False),
                    math_item.get('start', 0),
                    math_item.get('end', 0),
                    math_item.get('text', '')
                ))
        
        self.state = 1
        return self
    
    def compile(self):
        """编译所有数学表达式"""
        if self.state >= 2:
            return
        
        self.find_math()
        self.math.render_input(self.document)
        self.state = 2
        return self
    
    def get_metrics(self):
        """获取度量"""
        if self.state < 2:
            self.compile()
        
        # 获取度量信息
        # 这里简化了实现
        
        return self
    
    def typeset(self):
        """排版所有数学表达式"""
        if self.state >= 3:
            return
        
        self.compile()
        self.math.convert(self.document)
        self.math.render_output(self.document)
        self.state = 3
        return self
    
    def update(self):
        """更新文档"""
        if self.state < 3:
            self.typeset()
        
        # 更新文档
        # 这里简化了实现
        
        return self
    
    def reset(self):
        """重置文档"""
        this.state = 0
        this.math.reset()
        this.processed.reset()
        return this
    
    def clear(self):
        """清空文档"""
        this.reset()
        this.math.clear()
        this.processed.clear()
        return this


class MathJax:
    """MathJax主类"""
    
    def __init__(self):
        """初始化MathJax"""
        self.options = {
            'InputJax': {},
            'OutputJax': {},
            'document': None,
            'adaptor': None
        }
        self.document_class = MathDocument
        self.handlers = {}
        self.input_jax = {}
        self.output_jax = {}
        self.config_extractor = ConfigExtractor()
    
    def register_input_jax(self, jax, priority=10):
        """注册输入Jax"""
        name = jax.name
        self.input_jax[name] = jax
        self.options['InputJax'][name] = jax
        return self
    
    def register_output_jax(self, jax, priority=10):
        """注册输出Jax"""
        name = jax.name
        self.output_jax[name] = jax
        self.options['OutputJax'][name] = jax
        return self
    
    def register_document(self, document_class, priority=10):
        """注册文档类"""
        self.document_class = document_class
        return self
    
    def register_handler(self, type, handler, priority=10):
        """注册处理器"""
        if type not in self.handlers:
            self.handlers[type] = []
        self.handlers[type].append(handler)
        return self
    
    def document(self, document, options=None):
        """创建文档"""
        options = options or {}
        doc_options = {}
        doc_options.update(self.options)
        Options.user_options(doc_options, options)
        
        adaptor = doc_options.get('adaptor')
        if not adaptor:
            raise ValueError("No adaptor specified")
        
        return self.document_class(document, adaptor, doc_options)
    
    def extract_config_from_html(self, html_content):
        """从HTML内容中提取MathJax配置
        
        参数:
            html_content: HTML内容字符串
            
        返回:
            提取的配置字典
        """
        return self.config_extractor.extract_from_html(html_content)
    
    def apply_config(self, config):
        """应用从HTML中提取的配置
        
        参数:
            config: 配置字典
            
        返回:
            self，用于链式调用
        """
        # 处理输入Jax配置
        if 'tex' in config:
            tex_options = self.config_extractor.create_tex_options(config)
            if tex_options and 'TeX' in self.input_jax:
                self.input_jax['TeX'].options.update(tex_options)
        
        # 处理全局选项
        if 'options' in config:
            Options.user_options(self.options, config['options'])
        
        return self
    
    def start_up(self):
        """启动MathJax"""
        # 启动逻辑
        return self


class ConfigExtractor:
    """从HTML中提取MathJax配置的类"""
    
    def __init__(self):
        """初始化配置提取器"""
        self.default_config = {
            'tex': {
                'inlineMath': [['\\(', '\\)']],
                'displayMath': [['$$', '$$'], ['\\[', '\\]']],
                'processEscapes': True,
                'processEnvironments': True,
                'packages': ['base', 'ams', 'noerrors', 'noundefined']
            },
            'options': {
                'ignoreHtmlClass': 'tex2jax_ignore',
                'processHtmlClass': 'tex2jax_process'
            }
        }
    
    def extract_from_html(self, html_content):
        """从HTML内容中提取MathJax配置
        
        参数:
            html_content: HTML内容字符串
            
        返回:
            提取的配置字典
        """
        # 使用lxml.html解析HTML
        parser = HTMLParser()
        root = lxml.html.fromstring(html_content, parser=parser)
        
        # 查找配置脚本
        config = self.default_config.copy()
        
        # 方法1：查找MathJax.Hub.Config调用
        script_tags = root.xpath('//script')
        for script in script_tags:
            if script.text and 'MathJax.Hub.Config' in script.text:
                try:
                    # 提取配置对象
                    config_text = re.search(
                        r'MathJax\.Hub\.Config\s*\(\s*(\{.*?\})\s*\)', 
                        script.text, 
                        re.DOTALL
                    )
                    if config_text:
                        # 将JavaScript对象转换为Python字典
                        js_config = config_text.group(1)
                        # 将JS对象转换为有效的JSON
                        js_config = re.sub(r'(\w+):', r'"\1":', js_config)
                        js_config = re.sub(r'\'', r'"', js_config)
                        try:
                            extracted_config = json.loads(js_config)
                            self._update_config(config, extracted_config)
                        except json.JSONDecodeError:
                            pass
                except Exception:
                    pass
        
        # 方法2：查找window.MathJax = {...}
        for script in script_tags:
            if script.text and 'window.MathJax' in script.text:
                try:
                    config_text = re.search(
                        r'window\.MathJax\s*=\s*(\{.*?\})', 
                        script.text, 
                        re.DOTALL
                    )
                    if config_text:
                        js_config = config_text.group(1)
                        js_config = re.sub(r'(\w+):', r'"\1":', js_config)
                        js_config = re.sub(r'\'', r'"', js_config)
                        try:
                            extracted_config = json.loads(js_config)
                            self._update_config(config, extracted_config)
                        except json.JSONDecodeError:
                            pass
                except Exception:
                    pass
        
        # 方法3：查找data-config属性
        mathjax_scripts = root.xpath(
            '//script[contains(@src, "mathjax")]'
        )
        for script in mathjax_scripts:
            config_url = script.get('data-config')
            if config_url:
                # 这里应该加载配置文件，但简化实现
                pass
            
            # 从URL参数中提取配置
            src = script.get('src', '')
            if 'config=' in src:
                config_param = re.search(r'config=([^&]+)', src)
                if config_param:
                    config_names = config_param.group(1).split(',')
                    for name in config_names:
                        if name == 'TeX-AMS-MML_HTMLorMML':
                            # 预设配置
                            tex_config = {
                                'tex2jax': {
                                    'inlineMath': [['$', '$'], ['\\(', '\\)']],
                                    'displayMath': [['$$', '$$'], ['\\[', '\\]']],
                                    'processEscapes': True
                                },
                                'TeX': {
                                    'extensions': ['AMSmath.js', 'AMSsymbols.js']
                                }
                            }
                            self._update_config(config, tex_config)
        
        return config
    
    def extract_from_file(self, file_path):
        """从HTML文件中提取MathJax配置
        
        参数:
            file_path: HTML文件路径
            
        返回:
            提取的配置字典
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return self.extract_from_html(html_content)
    
    def _update_config(self, target, source):
        """递归更新配置
        
        参数:
            target: 目标配置字典
            source: 源配置字典
        """
        for key, value in source.items():
            if (isinstance(value, dict) and key in target and 
                    isinstance(target[key], dict)):
                self._update_config(target[key], value)
            else:
                target[key] = value
    
    def create_tex_options(self, config):
        """从提取的配置创建TeX选项
        
        参数:
            config: 配置字典
            
        返回:
            TeX选项字典
        """
        options = {}
        
        # 处理tex配置（MathJax v3）
        if 'tex' in config:
            tex_config = config['tex']
            for key, value in tex_config.items():
                if key in ['inlineMath', 'displayMath', 'processEscapes', 
                          'processEnvironments', 'packages']:
                    options[key] = value
        
        # 处理tex2jax配置（MathJax v2）
        if 'tex2jax' in config:
            tex2jax_config = config['tex2jax']
            for key, value in tex2jax_config.items():
                if key in ['inlineMath', 'displayMath', 'processEscapes']:
                    options[key] = value
        
        # 处理TeX配置（MathJax v2）
        if 'TeX' in config:
            tex_config = config['TeX']
            for key, value in tex_config.items():
                if key in ['equationNumbers', 'Macros', 'extensions']:
                    options[key] = value
        
        return options
    
    def compare_configs(self, config1, config2, ignore_keys=None):
        """比较两个MathJax配置是否一致
        
        参数:
            config1: 第一个配置
            config2: 第二个配置
            ignore_keys: 忽略比较的键列表
            
        返回:
            (bool, list): 是否一致的布尔值和不一致的键列表
        """
        ignore_keys = ignore_keys or []
        differences = []
        
        # 比较tex配置
        if 'tex' in config1 and 'tex' in config2:
            tex1 = config1['tex']
            tex2 = config2['tex']
            self._compare_dicts(tex1, tex2, differences, 'tex', ignore_keys)
        elif 'tex' in config1 or 'tex' in config2:
            differences.append('tex')
        
        # 比较tex2jax配置
        if 'tex2jax' in config1 and 'tex2jax' in config2:
            tex1 = config1['tex2jax']
            tex2 = config2['tex2jax']
            self._compare_dicts(tex1, tex2, differences, 'tex2jax', ignore_keys)
        elif 'tex2jax' in config1 or 'tex2jax' in config2:
            differences.append('tex2jax')
        
        # 比较TeX配置
        if 'TeX' in config1 and 'TeX' in config2:
            tex1 = config1['TeX']
            tex2 = config2['TeX']
            self._compare_dicts(tex1, tex2, differences, 'TeX', ignore_keys)
        elif 'TeX' in config1 or 'TeX' in config2:
            differences.append('TeX')
        
        # 比较options配置
        if 'options' in config1 and 'options' in config2:
            opt1 = config1['options']
            opt2 = config2['options']
            self._compare_dicts(opt1, opt2, differences, 'options', 
                               ignore_keys)
        elif 'options' in config1 or 'options' in config2:
            differences.append('options')
        
        return len(differences) == 0, differences
    
    def _compare_dicts(self, dict1, dict2, differences, prefix, ignore_keys):
        """比较两个字典，记录差异
        
        参数:
            dict1: 第一个字典
            dict2: 第二个字典
            differences: 差异列表
            prefix: 键前缀
            ignore_keys: 忽略的键列表
        """
        for key in set(list(dict1.keys()) + list(dict2.keys())):
            full_key = f"{prefix}.{key}"
            if full_key in ignore_keys:
                continue
                
            if key not in dict1:
                differences.append(full_key)
            elif key not in dict2:
                differences.append(full_key)
            elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                self._compare_dicts(dict1[key], dict2[key], differences, 
                                   full_key, ignore_keys)
            elif dict1[key] != dict2[key]:
                differences.append(full_key)


# 创建全局MathJax实例
mathjax = MathJax()


# 导出模块
__all__ = [
    'DOMAdaptor',
    'HTMLAdaptor',
    'Options',
    'MathItem',
    'MathList',
    'MathDocument',
    'MathJax',
    'ConfigExtractor',
    'mathjax'
] 