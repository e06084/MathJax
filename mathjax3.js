window.MathJax = {
    // TeX输入处理器配置
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],  // 行内数学表达式的定界符
      displayMath: [['$$', '$$'], ['\\[', '\\]']],  // 行间数学表达式的定界符
      processEscapes: true,  // 是否处理转义字符
      processEnvironments: true,  // 是否处理环境
      packages: ['base', 'ams', 'noerrors', 'noundefined', 'autoload', 'require']  // 加载的TeX包
    },
    
    // MathML输入处理器配置
    mml: {
      // MathML相关选项
    },
    
    // AsciiMath输入处理器配置
    asciimath: {
      // AsciiMath相关选项
    },
    
    // 输出处理器配置
    chtml: {
      // CommonHTML输出选项
      scale: 1,  // 缩放比例
      minScale: .5,  // 最小缩放
      mtextFont: '',  // mtext元素的字体
      fontURL: ''  // 字体URL
    },
    
    svg: {
      // SVG输出选项
      scale: 1,
      minScale: .5,
      fontCache: 'local',  // 字体缓存策略
      fontURL: ''
    },
    
    // 全局选项
    options: {
      ignoreHtmlClass: 'tex2jax_ignore',  // 忽略处理的HTML类
      processHtmlClass: 'tex2jax_process',  // 需要处理的HTML类
      renderActions: {
        // 渲染动作
      },
      enableMenu: true  // 是否启用右键菜单
    },
    
    // 加载器配置
    loader: {
      load: ['input/tex', 'output/chtml'],  // 要加载的组件
      paths: {
        // 组件路径
      },
      require: {
        // require.js配置
      }
    },
    
    // 启动配置
    startup: {
      elements: null,  // 要处理的元素
      typeset: true,  // 是否自动排版
      ready: function() {
        // MathJax准备好后的回调
      },
      pageReady: function() {
        // 页面准备好后的回调
      }
    }
  };