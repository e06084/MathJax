MathJax.Hub.Config({
    // TeX输入处理器配置
    tex2jax: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']],
      processEscapes: true,
      skipTags: ["script", "noscript", "style", "textarea", "pre", "code"]
    },
    
    // TeX处理器配置
    TeX: {
      equationNumbers: { autoNumber: "AMS" },
      Macros: {
        RR: "{\\mathbb{R}}",
        NN: "{\\mathbb{N}}"
      },
      extensions: ["AMSmath.js", "AMSsymbols.js"]
    },
    
    // MathML输入处理器配置
    mml2jax: {
      // MathML相关选项
    },
    
    // 输出处理器配置
    "HTML-CSS": {
      availableFonts: ["STIX", "TeX"],
      preferredFont: "TeX",
      webFont: "TeX",
      scale: 100,
      imageFont: null
    },
    
    // 其他输出处理器
    SVG: {
      // SVG输出选项
    },
    
    NativeMML: {
      // 原生MathML输出选项
    },
    
    // 消息配置
    messageStyle: "none",
    
    // 显示配置
    showMathMenu: true,
    showProcessingMessages: false
  });