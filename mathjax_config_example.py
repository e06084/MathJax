#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
示例脚本：展示如何使用MathJaxConfigExtractor从HTML中提取MathJax配置
并比较不同配置之间的差异
"""

from tex import MathJaxConfigExtractor, TeX

# 示例HTML内容
HTML_EXAMPLE = """
<!DOCTYPE html>
<html>
<head>
    <title>MathJax示例</title>
    <script type="text/javascript">
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true,
                packages: ['base', 'ams', 'noerrors', 'noundefined', 
                           'autoload', 'require']
            },
            options: {
                ignoreHtmlClass: 'no-mathjax',
                processHtmlClass: 'mathjax'
            }
        };
    </script>
    <script type="text/javascript" 
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>
</head>
<body>
    <h1>MathJax示例</h1>
    <p>行内公式: $E = mc^2$</p>
    <p>行间公式: $$E = mc^2$$</p>
</body>
</html>
"""

# 另一个示例HTML内容（使用MathJax.Hub.Config）
HTML_EXAMPLE2 = """
<!DOCTYPE html>
<html>
<head>
    <title>MathJax示例2</title>
    <script type="text/javascript" 
            src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
    </script>
    <script type="text/javascript">
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true
            },
            TeX: {
                equationNumbers: { autoNumber: "AMS" },
                Macros: {
                    RR: "{\\\\mathbb{R}}",
                    NN: "{\\\\mathbb{N}}"
                },
                extensions: ["AMSmath.js", "AMSsymbols.js"]
            }
        });
    </script>
</head>
<body>
    <h1>MathJax示例2</h1>
    <p>行内公式: $E = mc^2$</p>
    <p>行间公式: $$E = mc^2$$</p>
    <p>带编号的公式: \\begin{equation} E = mc^2 \\end{equation}</p>
</body>
</html>
"""

# 第三个示例，与第一个几乎相同，但有细微差别
HTML_EXAMPLE3 = """
<!DOCTYPE html>
<html>
<head>
    <title>MathJax示例3</title>
    <script type="text/javascript">
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true,
                packages: ['base', 'ams', 'noerrors', 'noundefined', 
                           'autoload']  // 少了'require'包
            },
            options: {
                ignoreHtmlClass: 'no-mathjax',
                processHtmlClass: 'mathjax'
            }
        };
    </script>
    <script type="text/javascript" 
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>
</head>
<body>
    <h1>MathJax示例3</h1>
    <p>行内公式: $E = mc^2$</p>
    <p>行间公式: $$E = mc^2$$</p>
</body>
</html>
"""

def main():
    """主函数"""
    # 创建配置提取器
    extractor = MathJaxConfigExtractor()
    
    # 从HTML内容中提取配置
    print("从第一个HTML示例中提取配置:")
    config1 = extractor.extract_from_html(HTML_EXAMPLE)
    print(f"提取的配置: {config1}")
    
    # 创建TeX选项
    tex_options1 = extractor.create_tex_options(config1)
    print(f"TeX选项: {tex_options1}")
    
    # 使用提取的配置创建TeX实例
    tex1 = TeX(tex_options1)
    print(f"TeX实例已创建，包含包: {tex1.options.get('packages', [])}")
    
    # 从第二个HTML示例中提取配置
    print("\n从第二个HTML示例中提取配置:")
    config2 = extractor.extract_from_html(HTML_EXAMPLE2)
    print(f"提取的配置: {config2}")
    
    # 创建TeX选项
    tex_options2 = extractor.create_tex_options(config2)
    print(f"TeX选项: {tex_options2}")
    
    # 使用提取的配置创建TeX实例
    tex2 = TeX(tex_options2)
    print(f"TeX实例已创建，包含包: {tex2.options.get('packages', [])}")
    
    # 从第三个HTML示例中提取配置
    print("\n从第三个HTML示例中提取配置:")
    config3 = extractor.extract_from_html(HTML_EXAMPLE3)
    print(f"提取的配置: {config3}")
    
    # 比较配置1和配置3
    print("\n比较配置1和配置3:")
    is_same, differences = extractor.compare_configs(config1, config3)
    if is_same:
        print("两个配置完全相同")
    else:
        print(f"两个配置有差异，差异项: {differences}")
    
    # 比较配置1和配置3，忽略packages差异
    print("\n比较配置1和配置3（忽略packages差异）:")
    is_same, differences = extractor.compare_configs(
        config1, config3, ignore_keys=['tex.packages']
    )
    if is_same:
        print("忽略packages后，两个配置相同")
    else:
        print(f"忽略packages后，两个配置仍有差异: {differences}")
    
    # 比较配置1和配置2
    print("\n比较配置1和配置2:")
    is_same, differences = extractor.compare_configs(config1, config2)
    if is_same:
        print("两个配置完全相同")
    else:
        print(f"两个配置有差异，差异项: {differences}")
    
    # 示例：查找数学表达式
    print("\n查找第一个HTML中的数学表达式:")
    math_expressions = tex1.findMath("""
    <p>行内公式: $E = mc^2$</p>
    <p>行间公式: $$E = mc^2$$</p>
    """)
    
    for expr in math_expressions:
        print(f"类型: {'显示' if expr['display'] else '行内'}, 公式: {expr['math']}")

if __name__ == "__main__":
    main() 