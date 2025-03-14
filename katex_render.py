class KaTeXRender(BaseMathRender):
    """KaTeX渲染器实现."""

    def __init__(self):
        """初始化KaTeX渲染器."""
        super().__init__()
        self.render_type = MathRenderType.KATEX
        self.options = {
            'auto_render': False,
            'display_mode': False,
            'throw_on_error': True,
            'error_color': '#cc0000',
            'version': '',
            'delimiters': []
        }

    def get_options(self, tree: HtmlElement) -> Dict[str, Any]:
        """从HTML中提取KaTeX选项.

        Args:
            html: 包含KaTeX配置的HTML字符串

        Returns:
            Dict[str, Any]: KaTeX选项字典
        """
        if tree is None:
            return self.options

        # 查找KaTeX样式表，提取版本
        for link in tree.iter('link'):
            href = link.get('href', '')
            if 'katex' in href.lower():
                version_pattern = r'katex@(\d+\.\d+\.\d+)'
                version_match = re.search(version_pattern, href, re.IGNORECASE)
                if version_match:
                    self.options['version'] = version_match.group(1)

        # 查找KaTeX配置脚本
        for script in tree.iter('script'):
            script_text = script.text or ''
            if 'renderMathInElement' in script_text:
                self._parse_katex_config(script_text)

        return self.options

    def _parse_katex_config(self, config_text: str) -> None:
        """解析KaTeX配置脚本.

        Args:
            config_text: KaTeX配置脚本内容
        """
        if not config_text:
            return

        # 检查自动渲染
        if 'renderMathInElement' in config_text:
            self.options['auto_render'] = True

        # 提取显示模式
        display_pattern = r'displayMode\s*:\s*(true|false)'
        display_match = re.search(display_pattern, config_text, re.IGNORECASE)
        if display_match:
            self.options['display_mode'] = display_match.group(1).lower() == 'true'

        # 提取错误处理选项
        throw_pattern = r'throwOnError\s*:\s*(true|false)'
        throw_on_error_match = re.search(throw_pattern, config_text, re.IGNORECASE)
        if throw_on_error_match:
            self.options['throw_on_error'] = (
                throw_on_error_match.group(1).lower() == 'true'
            )

        # 提取错误颜色
        error_pattern = r'errorColor\s*:\s*[\'"](.+?)[\'"]'
        error_color_match = re.search(error_pattern, config_text)
        if error_color_match:
            self.options['error_color'] = error_color_match.group(1)

        # 提取分隔符
        delimiters_pattern = r'delimiters\s*:\s*\[(.*?)\]'
        delimiters_match = re.search(delimiters_pattern, config_text, re.DOTALL)
        if delimiters_match:
            delimiters_str = delimiters_match.group(1)
            self.options['delimiters'] = self._parse_delimiters(delimiters_str)

    def _parse_delimiters(self, delimiters_str: str) -> List[Dict[str, str]]:
        """解析KaTeX分隔符配置.

        Args:
            delimiters_str: 分隔符配置字符串

        Returns:
            List[Dict[str, str]]: 分隔符配置列表
        """
        delimiters = []
        # 匹配 {left: 'x', right: 'y', display: true/false} 形式的配置
        pattern = (
            r'\{\s*left\s*:\s*[\'"](.+?)[\'"]\s*,'
            r'\s*right\s*:\s*[\'"](.+?)[\'"]\s*'
            r'(?:,\s*display\s*:\s*(true|false))?\s*\}'
        )
        for match in re.finditer(pattern, delimiters_str):
            left, right, display = match.groups()
            delimiter = {
                'left': left.replace('\\\\', '\\'),
                'right': right.replace('\\\\', '\\')
            }
            if display:
                delimiter['display'] = display.lower() == 'true'
            delimiters.append(delimiter)
        return delimiters

    def is_customized_options(self) -> bool:
        """是否与默认配置不同."""
        return False

    def find_math(self, root: HtmlElement) -> None:
        """查找KaTeX格式的数学公式，并创建相应的数学公式节点.

        Args:
            root: HTML根节点
        """
        # 获取分隔符配置
        delimiters = self.options.get('delimiters', [])
        if not delimiters:
            # 使用常见的默认分隔符
            delimiters = [
                {'left': '$$', 'right': '$$', 'display': True},
                {'left': '$', 'right': '$', 'display': False},
                {'left': '\\(', 'right': '\\)', 'display': False},
                {'left': '\\[', 'right': '\\]', 'display': True}
            ]

        # 分离行内和行间分隔符
        inline_delimiters = []
        display_delimiters = []

        for delimiter in delimiters:
            start = delimiter.get('left', '')
            end = delimiter.get('right', '')
            is_display = delimiter.get('display', False)

            if start and end:
                if is_display:
                    display_delimiters.append([start, end])
                else:
                    inline_delimiters.append([start, end])

        # 处理所有文本节点
        self._process_text_nodes(
            root, inline_delimiters, display_delimiters
        )

        # 处理特殊的KaTeX元素
        for elem in root.xpath('.//*[@class="katex"]'):
            math_text = elem.get('data-katex-expression')
            if math_text:
                is_display = 'katex-display' in elem.get('class', '')
                tag_name = 'ccmath-interline' if is_display else 'ccmath-inline'

                # 创建新节点，使用build_cc_element
                math_node = build_cc_element(
                    html_tag_name=tag_name,
                    text=math_text,
                    tail=elem.tail or '',
                    type=MathType.LATEX,  # 使用MathType枚举
                    by=self.render_type,
                    html=element_to_html(elem)  # 使用完整的原始HTML
                )
                
                # 替换原节点
                parent = elem.getparent()
                if parent is not None:
                    parent.replace(elem, math_node)


if __name__ == '__main__':
       # KaTeX示例
    katex_html = '''
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css">
        <script src="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/contrib/auto-render.min.js"></script>
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                renderMathInElement(document.body, {
                    delimiters: [
                        {left: "$$", right: "$$", display: true},
                        {left: "$", right: "$", display: false},
                        {left: "\\\\(", right: "\\\\)", display: false},
                        {left: "\\\\[", right: "\\\\]", display: true}
                    ],
                    throwOnError: false,
                    errorColor: "#cc0000"
                });
            });
        </script>
    </head>
    <body>
        <p>Inline math: $E=mc^2$</p>
        <p>Display math: $$F = G\\frac{m_1 m_2}{r^2}$$</p>
    </body>
    </html>
    '''
    print('\nTesting KaTeX detection:')
    katex_tree = html_to_element(katex_html)
    render_type = BaseMathRender.detect_render_type(katex_tree)
    print(f'Detected render type: {render_type}')

    render = BaseMathRender.create_render(katex_tree)
    if render:
        options = render.get_options(katex_tree)
        print(f'KaTeX options: {options}')
    else:
        print('No renderer detected')