# PyTera

[![PyPI version](https://badge.fury.io/py/pytera.svg)](https://pypi.org/project/pytera/)
[![Python versions](https://img.shields.io/pypi/pyversions/pytera.svg)](https://pypi.org/project/pytera/)
[![License](https://img.shields.io/pypi/l/pytera.svg)](https://github.com/un4gt/pytera/blob/main/LICENSE)
[![CI](https://github.com/un4gt/pytera/actions/workflows/ci.yml/badge.svg)](https://github.com/un4gt/pytera/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/un4gt/pytera/branch/main/graph/badge.svg)](https://codecov.io/gh/un4gt/pytera)

A fast, Python-native templating engine powered by Rust's Tera library. PyTera brings the power and performance of Tera templates to Python applications through PyO3 bindings.

## Features

- 🚀 **High Performance**: Rust-powered templating with zero-copy operations
- 🐍 **Python Native**: Seamless integration with Python data types and workflows
- 📝 **Tera Compatible**: Full support for Tera template syntax and features
- 🔧 **Easy Integration**: Simple API that works with Flask, FastAPI, and other web frameworks
- 🛡️ **Type Safe**: Comprehensive type hints and error handling
- 📚 **Rich Features**: Variables, conditionals, loops, filters, inheritance, and more

## Installation

Install PyTera from PyPI:

```bash
pip install pytera
```

Or using uv:

```bash
uv add pytera
```

### Requirements

- Python 3.8+
- Rust toolchain (for building from source)

## Quick Start

```python
import os
from pytera import PyTera

template_dir = os.path.join(os.path.dirname(__file__), "templates")
tera = PyTera(f"{template_dir}/*.html")

result = tera.render_template("basic_variables.html", name="Alice", age=30)
print(result)  # Hello Alice! You are 30 years old.
```

> ℹ️ **Glob pattern tips**: The current templates live directly under `templates/`, so `PyTera(f"{template_dir}/*.html")` works. If you reorganize templates into nested subdirectories, switch to `PyTera(f"{template_dir}/**/*.html")` to load them recursively.

## Usage Examples

### Basic Variables

```python
tera = PyTera("templates/*.html")
result = tera.render_template(
    "basic_variables.html",
    name="Alice",
    age=30,
)
print(result)  # Hello Alice! You are 30 years old.
```

> ℹ️ **Glob pattern tips**: Current templates live directly under `templates/`, so `PyTera(f"{template_dir}/*.html")` works. If you organize templates into nested subdirectories later, switch to `PyTera(f"{template_dir}/**/*.html")` to load them recursively.

```html
<!-- templates/basic_variables.html -->
Hello {{ name }}! You are {{ age }} years old.
```

### Conditionals

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

### Loops

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

### Filters

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

### Template Inheritance

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

### Flask Integration

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

For a complete working example with additional routes (`/basic_variables`, `/conditionals`, `/filters`, `/loops`), see [examples/app.py](examples/app.py).


## Template Syntax

The templates rendered in [examples/app.py](examples/app.py) cover the core pieces of Tera syntax:

### Variables
```html
Hello {{ name }}! You are {{ age }} years old.
```

### Conditionals
```html
{% if user.is_admin %}
Welcome, Administrator {{ user.name }}!
{% else %}
Hello, {{ user.name }}!
{% endif %}
```

### Loops
```html
<ul>
{% for item in items %}
<li>{{ item.name }}: {{ item.price | round(precision=2) }}</li>
{% endfor %}
</ul>
```

### Filters
```html
<p>Uppercase: {{ text | upper }}</p>
<p>Length: {{ text | length }}</p>
<p>Default: {{ missing | default(value="N/A") }}</p>
<p>Slice: {{ list | slice(start=1, end=3) | join(sep=", ") }}</p>
```

### Template Inheritance
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

For more template features—such as macros, tests, and custom filters—consult the [Tera documentation](https://keats.github.io/tera/docs/#getting-started).

## Error Handling

PyTera provides detailed error messages for common issues:

- **Template Not Found**: When requesting a non-existent template
- **Invalid Context**: When context keys aren't strings
- **Parsing Errors**: Syntax errors in templates
- **Inheritance Issues**: Circular dependencies or missing parents


## Development

### Building from Source

```bash
# Clone the repository
git clone https://github.com/un4gt/pytera.git
cd pytera

# Install development dependencies
uv sync --dev

# Build the package
maturin develop

# Run tests
pytest
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pytera --cov-report=html
```

### Code Quality

```bash
# Format code
cargo fmt
black src/

# Lint code
cargo clippy
flake8 src/
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
uv sync --dev

# Install pre-commit hooks
pre-commit install

# Build and test
maturin develop
pytest
```

## License

PyTera is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- [Tera](https://keats.github.io/tera/docs/#getting-started) - The Rust templating engine
- [PyO3](https://pyo3.rs/) - Python bindings for Rust
- [Maturin](https://www.maturin.rs/) - Build tool for Python extensions

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.