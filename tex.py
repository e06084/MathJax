#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python版本的MathJax TeX解析器
这是一个简化版本，实现了基本的类和结构
"""

import re
import json
import lxml.html
from lxml.etree import HTMLParser
from typing import Dict, List, Tuple, Callable, Optional, Any, Union, Set


class AbstractInputJax:
    """抽象输入Jax类，作为TeX类的基类"""
    
    OPTIONS = {
        # 基本选项
    }
    
    def __init__(self, options=None):
        """初始化AbstractInputJax"""
        self.options = {}
        self.preFilters = FilterList()
        self.postFilters = FilterList()
        if options:
            self.options.update(options)
    
    def setMmlFactory(self, factory):
        """设置MML工厂"""
        self.mmlFactory = factory
    
    def executeFilters(self, filters, math, document, options):
        """执行过滤器"""
        filters.execute(math, document, options)


class FilterList:
    """过滤器列表类"""
    
    def __init__(self):
        """初始化过滤器列表"""
        self.filters = []
    
    def add(self, filter_func, priority=0):
        """添加过滤器"""
        self.filters.append((filter_func, priority))
        # 按优先级排序
        self.filters.sort(key=lambda x: x[1])
    
    def execute(self, math, document, options):
        """执行所有过滤器"""
        for filter_func, _ in self.filters:
            filter_func(math, document, options)


class FindTeX:
    """查找TeX表达式的类"""
    
    OPTIONS = {
        'inlineMath': [['\\(', '\\)']],
        'displayMath': [['$$', '$$'], ['\\[', '\\]']],
        'processEscapes': True,
        'processEnvironments': True,
        'processRefs': True,
    }
    
    def __init__(self, options=None):
        """初始化FindTeX"""
        self.options = self.OPTIONS.copy()
        if options:
            self.options.update(options)
        self._compile_patterns()
    
    def _compile_patterns(self):
        """编译正则表达式模式"""
        # 这里简化了正则表达式的构建
        inline_patterns = [re.escape(pair[0]) + '(.*?)' + re.escape(pair[1]) 
                          for pair in self.options['inlineMath']]
        display_patterns = [re.escape(pair[0]) + '(.*?)' + re.escape(pair[1]) 
                           for pair in self.options['displayMath']]
        
        self.inline_pattern = re.compile('|'.join(inline_patterns), re.DOTALL)
        self.display_pattern = re.compile('|'.join(display_patterns), re.DOTALL)
    
    def findMath(self, text):
        """查找文本中的数学表达式"""
        results = []
        
        # 查找行内数学表达式
        for match in self.inline_pattern.finditer(text):
            start, end = match.span()
            math = match.group(1)
            results.append({
                'math': math,
                'start': start,
                'end': end,
                'display': False
            })
        
        # 查找显示数学表达式
        for match in self.display_pattern.finditer(text):
            start, end = match.span()
            math = match.group(1)
            results.append({
                'math': math,
                'start': start,
                'end': end,
                'display': True
            })
        
        # 按开始位置排序
        results.sort(key=lambda x: x['start'])
        return results


class NodeFactory:
    """节点工厂类"""
    
    def __init__(self, mml_factory=None):
        """初始化节点工厂"""
        self.mmlFactory = mml_factory
        self.creators = {}
    
    def setMmlFactory(self, factory):
        """设置MML工厂"""
        self.mmlFactory = factory
    
    def setCreators(self, creators):
        """设置创建器"""
        self.creators.update(creators)
    
    def create(self, kind, *args):
        """创建节点"""
        if kind in self.creators:
            return self.creators[kind](*args)
        elif kind == 'node':
            return self.mmlFactory.create(*args)
        elif kind == 'error':
            return self.createError(*args)
        return None
    
    def createError(self, message, id=None, latex=None):
        """创建错误节点"""
        # 简化的错误节点创建
        return {
            'type': 'error',
            'message': message,
            'id': id,
            'latex': latex
        }


class ItemFactory:
    """项目工厂类"""
    
    def __init__(self):
        """初始化项目工厂"""
        self.nodeClasses = {}
    
    def setNodeClass(self, kind, cls):
        """设置节点类"""
        self.nodeClasses[kind] = cls
    
    def create(self, kind, *args):
        """创建项目"""
        if kind in self.nodeClasses:
            return self.nodeClasses[kind](*args)
        return None


class TagsFactory:
    """标签工厂类"""
    
    OPTIONS = {
        'tags': 'none'
    }
    
    _tags = {}
    _default = None
    
    @classmethod
    def addTags(cls, tags):
        """添加标签"""
        cls._tags.update(tags)
    
    @classmethod
    def setDefault(cls, name):
        """设置默认标签"""
        if name in cls._tags:
            cls._default = cls._tags[name]
        else:
            cls._default = cls._tags['none']
    
    @classmethod
    def getDefault(cls):
        """获取默认标签"""
        return cls._default


class ParseOptions:
    """解析选项类"""
    
    def __init__(self, configuration, options=None):
        """初始化解析选项"""
        self.configuration = configuration
        self.options = {}
        self.nodeFactory = NodeFactory()
        self.itemFactory = ItemFactory()
        self.tags = None
        self.error = False
        self.root = None
        
        if options:
            for option in options:
                if option:
                    self.options.update(option)
    
    def clear(self):
        """清除状态"""
        self.error = False
        self.root = None


class ParserError(Exception):
    """解析器错误类"""
    
    def __init__(self, message, id=None):
        """初始化解析器错误"""
        super().__init__(message)
        self.message = message
        self.id = id


class Parser:
    """解析器类"""
    
    def __init__(self, latex, options, parse_options):
        """初始化解析器"""
        self.latex = latex
        self.options = options
        self.parseOptions = parse_options
        self.stack = {'global': {}}
    
    def mml(self):
        """解析LaTeX并返回MML"""
        # 这里是简化的实现
        # 实际实现需要完整的TeX解析逻辑
        return {'type': 'mml', 'content': self.latex}


class Configuration:
    """配置类"""
    
    def __init__(self, name, handler=None, fallback=None, items=None, tags=None, 
                 options=None, nodes=None, preprocessors=None, postprocessors=None,
                 init_method=None, config_method=None, priority=10, parser='tex'):
        """初始化配置"""
        self.name = name
        self.handler = handler or {}
        self.fallback = fallback or {}
        self.items = items or {}
        self.tags = tags or {}
        self.options = options or {}
        self.nodes = nodes or {}
        self.preprocessors = preprocessors or []
        self.postprocessors = postprocessors or []
        self.initMethod = init_method
        self.configMethod = config_method
        self.priority = priority
        self.parser = parser
        
        # 确保handler有基本结构
        default_handlers = {
            'character': [],
            'delimiter': [],
            'macro': [],
            'environment': []
        }
        self.handler = {**default_handlers, **self.handler}
    
    @classmethod
    def create(cls, name, options=None):
        """创建配置"""
        options = options or {}
        config = cls(name, **options)
        ConfigurationHandler.set(name, config)
        return config
    
    @property
    def init(self):
        """获取初始化方法"""
        return self.initMethod[0] if self.initMethod else None
    
    @property
    def config(self):
        """获取配置方法"""
        return self.configMethod[0] if self.configMethod else None


class ConfigurationHandler:
    """配置处理器类"""
    
    _configurations = {}
    
    @classmethod
    def set(cls, name, config):
        """设置配置"""
        cls._configurations[name] = config
    
    @classmethod
    def get(cls, name):
        """获取配置"""
        return cls._configurations.get(name)
    
    @classmethod
    def keys(cls):
        """获取所有配置名"""
        return cls._configurations.keys()


class ParserConfiguration:
    """解析器配置类"""
    
    def __init__(self, packages, parsers=None):
        """初始化解析器配置"""
        self.initMethod = FunctionList()
        self.configMethod = FunctionList()
        self.configurations = PrioritizedList()
        self.parsers = parsers or ['tex']
        self.handlers = {}
        self.items = {}
        self.tags = {}
        self.options = {}
        self.nodes = {}
        
        # 添加包
        for package in reversed(packages):
            self.addPackage(package)
        
        # 应用配置
        for item, priority in self.configurations.items():
            self.append(item, priority)
    
    def init(self):
        """初始化"""
        self.initMethod.execute(self)
    
    def config(self, tex):
        """配置"""
        self.configMethod.execute(self, tex)
        
        # 添加过滤器
        for item, _ in self.configurations.items():
            self.addFilters(tex, item)
    
    def addPackage(self, package):
        """添加包"""
        if isinstance(package, str):
            name = package
            priority = None
        else:
            name = package[0]
            priority = package[1]
        
        config = self.getPackage(name)
        if config:
            priority = priority or config.priority
            self.configurations.add(config, priority)
    
    def getPackage(self, name):
        """获取包"""
        config = ConfigurationHandler.get(name)
        if config and config.parser not in self.parsers:
            raise ValueError(f"Package {name} doesn't target the proper parser")
        return config
    
    def append(self, config, priority=None):
        """添加配置"""
        priority = priority or config.priority
        
        # 添加处理器
        for kind, handlers in config.handler.items():
            if kind not in self.handlers:
                self.handlers[kind] = []
            self.handlers[kind].extend(handlers)
        
        # 添加回退处理器
        for kind, handler in config.fallback.items():
            self.handlers[kind] = handler
        
        # 添加项目
        self.items.update(config.items)
        
        # 添加标签
        self.tags.update(config.tags)
        
        # 添加选项
        self.options.update(config.options)
        
        # 添加节点
        self.nodes.update(config.nodes)
        
        # 添加预处理器
        for processor, proc_priority in config.preprocessors:
            self.initMethod.add(processor, proc_priority)
        
        # 添加后处理器
        for processor, proc_priority in config.postprocessors:
            self.configMethod.add(processor, proc_priority)
        
        # 添加初始化方法
        if config.initMethod:
            processor, proc_priority = config.initMethod
            self.initMethod.add(processor, proc_priority)
        
        # 添加配置方法
        if config.configMethod:
            processor, proc_priority = config.configMethod
            self.configMethod.add(processor, proc_priority)
    
    def addFilters(self, tex, config):
        """添加过滤器"""
        for processor, priority in config.preprocessors:
            tex.preFilters.add(processor, priority)
        
        for processor, priority in config.postprocessors:
            tex.postFilters.add(processor, priority)


class FunctionList:
    """函数列表类"""
    
    def __init__(self):
        """初始化函数列表"""
        self.functions = []
    
    def add(self, func, priority=10):
        """添加函数"""
        self.functions.append((func, priority))
        self.functions.sort(key=lambda x: x[1])
    
    def execute(self, *args):
        """执行所有函数"""
        for func, _ in self.functions:
            func(*args)


class PrioritizedList:
    """优先级列表类"""
    
    DEFAULTPRIORITY = 10
    
    def __init__(self):
        """初始化优先级列表"""
        self.items = []
    
    def add(self, item, priority=None):
        """添加项目"""
        priority = priority or self.DEFAULTPRIORITY
        self.items.append((item, priority))
        self.items.sort(key=lambda x: x[1])
    
    def items(self):
        """获取所有项目"""
        return self.items


class TeX(AbstractInputJax):
    """TeX类，MathJax的TeX解析器"""
    
    NAME = 'TeX'
    OPTIONS = {
        **AbstractInputJax.OPTIONS,
        'FindTeX': None,
        'packages': ['base'],
        'digits': r'^(?:[0-9]+(?:\{,\}[0-9]{3})*(?:\.[0-9]*)?|\.[0-9]+)',
        'maxBuffer': 5120,
    }
    
    def __init__(self, options=None):
        """初始化TeX"""
        options = options or {}
        
        # 分离选项
        tex_options, find_tex_options = self.separateOptions(options)
        
        super().__init__(tex_options)
        
        # 创建FindTeX实例
        self.findTeX = self.options.get('FindTeX') or FindTeX(find_tex_options)
        
        # 配置
        packages = self.options.get('packages', ['base'])
        self.configuration = self.configure(packages)
        
        # 解析选项
        self._parseOptions = ParseOptions(self.configuration, [
            self.options,
            TagsFactory.OPTIONS
        ])
        
        # 配置
        self.configuration.config(self)
        
        # 设置标签
        self.setTags(self._parseOptions, self.configuration)
        
        # 添加后过滤器
        self.postFilters.add(self.cleanSubSup, -6)
        self.postFilters.add(self.setInherited, -5)
        self.postFilters.add(self.moveLimits, -4)
        self.postFilters.add(self.cleanStretchy, -3)
        self.postFilters.add(self.cleanAttributes, -2)
        self.postFilters.add(self.combineRelations, -1)
    
    @staticmethod
    def configure(packages):
        """配置"""
        config = ParserConfiguration(packages, ['tex'])
        config.init()
        return config
    
    @staticmethod
    def setTags(options, config):
        """设置标签"""
        TagsFactory.addTags(config.tags)
        TagsFactory.setDefault(options.options.get('tags'))
        options.tags = TagsFactory.getDefault()
        options.tags.configuration = options
    
    def setMmlFactory(self, factory):
        """设置MML工厂"""
        super().setMmlFactory(factory)
        self._parseOptions.nodeFactory.setMmlFactory(factory)
    
    @property
    def parseOptions(self):
        """获取解析选项"""
        return self._parseOptions
    
    def reset(self, start=0):
        """重置"""
        self.parseOptions.tags.reset(start)
    
    def compile(self, math, document):
        """编译"""
        self.parseOptions.clear()
        self.executeFilters(self.preFilters, math, document, self.parseOptions)
        
        display = math.get('display', False)
        self.latex = math.get('math', '')
        self.parseOptions.tags.startEquation(math)
        
        try:
            parser = Parser(
                self.latex, 
                {'display': display, 'isInner': False}, 
                self.parseOptions
            )
            mml = parser.mml()
            global_data = parser.stack.get('global', {})
        except ParserError as error:
            self.parseOptions.error = True
            mml = self.options.get('formatError', self.formatError)(self, error)
        
        # 创建math节点
        mml = self.parseOptions.nodeFactory.create('node', 'math', [mml])
        
        # 设置属性
        if global_data and global_data.get('indentalign'):
            mml['indentalign'] = global_data['indentalign']
        
        if display:
            mml['display'] = 'block'
        
        self.parseOptions.tags.finishEquation(math)
        self.parseOptions.root = mml
        
        self.executeFilters(
            self.postFilters, 
            math, 
            document, 
            self.parseOptions
        )
        
        self.mathNode = self.parseOptions.root
        return self.mathNode
    
    def findMath(self, text):
        """查找数学表达式"""
        return self.findTeX.findMath(text)
    
    def formatError(self, error):
        """格式化错误"""
        message = error.message.split('\n')[0]
        return self.parseOptions.nodeFactory.create(
            'error', 
            message, 
            error.id, 
            self.latex
        )
    
    @staticmethod
    def separateOptions(options):
        """分离选项"""
        tex_options = {}
        find_tex_options = {}
        
        for key, value in options.items():
            if key in FindTeX.OPTIONS:
                find_tex_options[key] = value
            else:
                tex_options[key] = value
        
        return tex_options, find_tex_options
    
    # 过滤器方法
    def cleanSubSup(self, math, document, options):
        """清理上下标"""
        pass
    
    def setInherited(self, math, document, options):
        """设置继承属性"""
        pass
    
    def moveLimits(self, math, document, options):
        """移动限制"""
        pass
    
    def cleanStretchy(self, math, document, options):
        """清理可伸缩元素"""
        pass
    
    def cleanAttributes(self, math, document, options):
        """清理属性"""
        pass
    
    def combineRelations(self, math, document, options):
        """组合关系"""
        pass


class MathJaxConfigExtractor:
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
        """从HTML内容中提取MathJax配置"""
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
                        # 注意：这是一个简化的实现，可能需要更复杂的解析
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
            if script.get('data-config'):
                # 这里需要加载配置文件，但这超出了当前实现的范围
                pass
        
        return config
    
    def extract_from_file(self, file_path):
        """从HTML文件中提取MathJax配置"""
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return self.extract_from_html(html_content)
    
    def _update_config(self, target, source):
        """递归更新配置"""
        for key, value in source.items():
            if (isinstance(value, dict) and key in target and 
                    isinstance(target[key], dict)):
                self._update_config(target[key], value)
            else:
                target[key] = value
    
    def create_tex_options(self, config):
        """从提取的配置创建TeX选项"""
        options = {}
        
        # 处理tex配置
        if 'tex' in config:
            tex_config = config['tex']
            for key, value in tex_config.items():
                if key in ['inlineMath', 'displayMath', 'processEscapes', 
                           'processEnvironments', 'packages']:
                    options[key] = value
        
        # 处理TeX配置（旧版MathJax可能使用这个键）
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
        
        # 比较TeX配置（旧版MathJax）
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
            self._compare_dicts(opt1, opt2, differences, 'options', ignore_keys)
        elif 'options' in config1 or 'options' in config2:
            differences.append('options')
        
        # 比较其他顶级配置
        all_keys = set(config1.keys()) | set(config2.keys())
        all_keys -= {'tex', 'TeX', 'options'}
        for key in all_keys:
            if key in ignore_keys:
                continue
            
            if key in config1 and key in config2:
                if isinstance(config1[key], dict) and isinstance(config2[key], dict):
                    self._compare_dicts(
                        config1[key], 
                        config2[key], 
                        differences, 
                        key, 
                        ignore_keys
                    )
                elif config1[key] != config2[key]:
                    differences.append(key)
            else:
                differences.append(key)
        
        return len(differences) == 0, differences
    
    def _compare_dicts(self, dict1, dict2, differences, prefix, ignore_keys):
        """比较两个字典，记录差异"""
        all_keys = set(dict1.keys()) | set(dict2.keys())
        
        for key in all_keys:
            full_key = f"{prefix}.{key}"
            if full_key in ignore_keys or key in ignore_keys:
                continue
                
            if key in dict1 and key in dict2:
                if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                    self._compare_dicts(
                        dict1[key], 
                        dict2[key], 
                        differences, 
                        full_key, 
                        ignore_keys
                    )
                elif dict1[key] != dict2[key]:
                    differences.append(full_key)
            else:
                differences.append(full_key)


# 导出模块
__all__ = [
    'AbstractInputJax',
    'FilterList',
    'FindTeX',
    'NodeFactory',
    'ItemFactory',
    'TagsFactory',
    'ParseOptions',
    'ParserError',
    'Parser',
    'Configuration',
    'ConfigurationHandler',
    'ParserConfiguration',
    'FunctionList',
    'PrioritizedList',
    'TeX',
    'MathJaxConfigExtractor'
] 