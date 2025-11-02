# PyTera

[![PyPI version](https://badge.fury.io/py/pytera.svg)](https://pypi.org/project/pytera/)
[![Python versions](https://img.shields.io/pypi/pyversions/pytera.svg)](https://pypi.org/project/pytera/)
[![License](https://img.shields.io/pypi/l/pytera.svg)](https://github.com/un4gt/pytera/blob/main/LICENSE)
[![CI](https://github.com/un4gt/pytera/actions/workflows/ci.yml/badge.svg)](https://github.com/un4gt/pytera/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/un4gt/pytera/branch/main/graph/badge.svg)](https://codecov.io/gh/un4gt/pytera)

一个快速、原生 Python 模板引擎，由 Rust 的 Tera 库提供支持。PyTera 通过 PyO3 绑定将 Tera 模板的强大功能和性能带到 Python 应用程序中。

## 特性

- 🚀 **高性能**：Rust 驱动的模板引擎，具有零拷贝操作
- 🐍 **Python 原生**：与 Python 数据类型和工作流无缝集成
- 📝 **Tera 兼容**：完全支持 Tera 模板语法和功能
- 🔧 **易于集成**：与 Flask、FastAPI 和其他 Web 框架配合使用的简单 API
- 🛡️ **类型安全**：全面的类型提示和错误处理
- 📚 **丰富功能**：变量、条件语句、循环、过滤器、继承等

## 安装

从 PyPI 安装 PyTera：

```bash
pip install pytera
```

或使用 uv：

```bash
uv add pytera
```

### 系统要求

- Python 3.8+
- Rust 工具链（从源码构建时需要）

## 快速开始

```python
import os
from pytera import PyTera

template_dir = os.path.join(os.path.dirname(__file__), "templates")
tera = PyTera(f"{template_dir}/*.html")

result = tera.render_template("basic_variables.html", name="Alice", age=30)
print(result)  # Hello Alice! You are 30 years old.
```

> ℹ️ **Glob 模式提示**：当前模板文件直接位于 `templates/` 目录下，因此使用 `PyTera(f"{template_dir}/*.html")` 即可。如果未来将模板拆分到多级子目录，请改用 `PyTera(f"{template_dir}/**/*.html")` 以递归加载所有模板。

## 使用示例

### 基本变量

```python
tera = PyTera("templates/*.html")
result = tera.render_template(
    "basic_variables.html",
    name="Alice",
    age=30,
)
print(result)  # Hello Alice! You are 30 years old.
```

```html
<!-- templates/basic_variables.html -->
Hello {{ name }}! You are {{ age }} years old.
```

### 条件语句

```python
user = {"name": "Bob", "is_admin": True}
result = tera.render_template("conditionals.html", user=user)
print(result)  # Welcome, Administrator Bob!
```

```html
<!-- templates/conditionals.html -->
{% if user.is_admin %}
Welcome, Administrator {{ user.name }}!
{% else %}
Hello, {{ user.name }}!
{% endif %}
```

### 循环

```python
items = [
    {"name": "Apple", "price": 1.50},
    {"name": "Banana", "price": 0.75},
    {"name": "Cherry", "price": 2.25},
]
result = tera.render_template("loops.html", items=items)
print(result)
```

```html
<!-- templates/loops.html -->
<ul>
{% for item in items %}
<li>{{ item.name }}: {{ item.price | round(precision=2) }}</li>
{% endfor %}
</ul>
```

### 过滤器

```python
data = {
    "text": "hello world",
    "missing": None,
    "list": ["apple", "banana", "cherry", "date"],
}
result = tera.render_template("filters.html", **data)
print(result)
```

```html
<!-- templates/filters.html -->
<p>Uppercase: {{ text | upper }}</p>
<p>Length: {{ text | length }}</p>
<p>Default: {{ missing | default(value="N/A") }}</p>
<p>Slice: {{ list | slice(start=1, end=3) | join(sep=", ") }}</p>
```

### 模板继承

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <header>
        <h1>My Website</h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2023</p>
    </footer>
</body>
</html>
```

```html
<!-- templates/child.html -->
{% extends "base.html" %}

{% block title %}Home Page{% endblock %}

{% block content %}
<h2>Welcome to {{ site_name }}</h2>
<p>This is the home page content.</p>
{% if user %}
<p>Hello, {{ user.name }}!</p>
{% endif %}
{% endblock %}
```

### Flask 集成

```python
import os
from flask import Flask, render_template
from pytera import PyTera

template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
tera = PyTera(f"{template_dir}/*.html")

app = Flask(__name__, template_folder=os.path.abspath(template_dir))

@app.route("/")
def index():
    return tera.render_template(
        "child.html",
        site_name="example",
        user={"name": "David"},
    )

@app.route("/child")
def child():
    return render_template(
        "child.html",
        site_name="example",
        user={"name": "David"},
    )
```

更多包含 `/basic_variables`、`/conditionals`、`/filters`、`/loops` 路由的完整示例请查看 [examples/app.py](examples/app.py)。


## 模板语法

[examples/app.py](examples/app.py) 中渲染的模板覆盖了 Tera 语法的核心用法：

### 变量
```html
Hello {{ name }}! You are {{ age }} years old.
```

### 条件语句
```html
{% if user.is_admin %}
Welcome, Administrator {{ user.name }}!
{% else %}
Hello, {{ user.name }}!
{% endif %}
```

### 循环
```html
<ul>
{% for item in items %}
<li>{{ item.name }}: {{ item.price | round(precision=2) }}</li>
{% endfor %}
</ul>
```

### 过滤器
```html
<p>Uppercase: {{ text | upper }}</p>
<p>Length: {{ text | length }}</p>
<p>Default: {{ missing | default(value="N/A") }}</p>
<p>Slice: {{ list | slice(start=1, end=3) | join(sep=", ") }}</p>
```

### 模板继承
```html
{% extends "base.html" %}
{% block title %}Home Page{% endblock %}
{% block content %}
<h2>Welcome to {{ site_name }}</h2>
{% if user %}
<p>Hello, {{ user.name }}!</p>
{% endif %}
{% endblock %}
```

更多功能（如宏、测试、自定义过滤器等）请参考 [Tera 文档](https://keats.github.io/tera/docs/#getting-started)。

## 错误处理

PyTera 为常见问题提供详细的错误信息：

- **模板未找到**：请求不存在的模板时
- **无效上下文**：上下文键不是字符串时
- **解析错误**：模板中的语法错误
- **继承问题**：循环依赖或缺少父模板


## 开发

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/un4gt/pytera.git
cd pytera

# 安装开发依赖
uv sync --dev

# 构建包
maturin develop

# 运行测试
pytest
```

### 运行测试

```bash
# 运行所有测试
pytest

# 带覆盖率运行
pytest --cov=pytera --cov-report=html
```

### 代码质量

```bash
# 格式化代码
cargo fmt
black src/

# 检查代码
cargo clippy
flake8 src/
```

## 贡献

我们欢迎贡献！请查看我们的[贡献指南](CONTRIBUTING.md)了解详情。

1. Fork 本仓库
2. 创建功能分支
3. 进行更改
4. 添加测试
5. 提交拉取请求

### 开发环境设置

```bash
# 安装开发依赖
uv sync --dev

# 安装 pre-commit 钩子
pre-commit install

# 构建和测试
maturin develop
pytest
```

## 许可证

PyTera 使用 MIT 许可证。详见 [LICENSE](LICENSE)。

## 致谢

- [Tera](https://keats.github.io/tera/docs/#getting-started/) - Rust 模板引擎
- [PyO3](https://pyo3.rs/) - Rust 的 Python 绑定
- [Maturin](https://www.maturin.rs/) - Python 扩展构建工具

## 更新日志

版本历史请见 [CHANGELOG.md](CHANGELOG.md)。</content>