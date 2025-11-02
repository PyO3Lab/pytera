use pyo3::{exceptions::{PyException, PyIOError, PyRuntimeError, PyUnicodeDecodeError, PyValueError}, PyErr};
use tera::ErrorKind as TeraErrorKind;

// 为 Python 侧暴露自定义异常类型（更明确，不再显示为通用的 Exception）
pyo3::create_exception!(pytera, PyTeraException, PyException);
pyo3::create_exception!(pytera, PyTeraRenderException, PyTeraException);

fn format_source_chain(err: &tera::Error) -> String {
    use std::error::Error as StdError;
    // 提取嵌套 source 链为简洁的一行，不包含 Some(...) 等结构体调试输出
    let mut parts: Vec<String> = Vec::new();
    let mut cur = err.source();
    while let Some(e) = cur {
        parts.push(e.to_string());
        cur = e.source();
    }

    if parts.is_empty() {
        String::new()
    } else {
        format!(" | caused by: {}", parts.join(" -> "))
    }
}

fn fmt_with_chain(msg: impl AsRef<str>, chain: &str) -> String {
    let mut msg = msg.as_ref().to_string();
    if !chain.is_empty() {
        msg.push_str(chain);
    }
    msg
}


#[derive(Debug)]
pub struct  PyTeraError(pub tera::Error);

impl From<tera::Error> for PyTeraError {
    fn from(err: tera::Error) -> Self {
        PyTeraError(err)
    }
}

fn map_kind_to_pyerr(kind: &TeraErrorKind, display_err: &str, source_chain: &str) -> PyErr {
    match kind {
        // Msg 包含自由的字符串，需要根据内容进一步判断
        TeraErrorKind::Msg(msg) => {
            // 按关键词映射（保留原有行为）
            if msg.contains("glob") {
                PyValueError::new_err(fmt_with_chain(msg, source_chain))
            } else if msg.contains("parse") {
                PyRuntimeError::new_err(fmt_with_chain(msg, source_chain))
            } else {
                PyTeraRenderException::new_err(fmt_with_chain(msg, source_chain))
            }
        }

        TeraErrorKind::CircularExtend { tpl, inheritance_chain } => {
            PyRuntimeError::new_err(fmt_with_chain(
                format!("Circular inheritance in template '{}': Chain -> {:?}", tpl, inheritance_chain),
                source_chain,
            ))
        }

        TeraErrorKind::MissingParent { current, parent } => {
            PyRuntimeError::new_err(fmt_with_chain(
                format!("Template '{}' requires missing parent '{}'", current, parent),
                source_chain,
            ))
        }

        TeraErrorKind::Utf8Conversion { context } => {
            PyUnicodeDecodeError::new_err(fmt_with_chain(format!("UTF-8 conversion error in {}", context), source_chain))
        }

        TeraErrorKind::Json(e) => {
            PyValueError::new_err(fmt_with_chain(format!("JSON error: {}", e), source_chain))
        }

        TeraErrorKind::InvalidMacroDefinition(msg) => {
            PyValueError::new_err(fmt_with_chain(format!("Invalid macro: {}", msg), source_chain))
        }

        TeraErrorKind::Io(e) => {
            PyIOError::new_err(fmt_with_chain(format!("IO error: {}", e), source_chain))
        }

        TeraErrorKind::CallFilter(msg) =>
            PyTeraRenderException::new_err(fmt_with_chain(format!("Filter error: {}", msg), source_chain)),

        TeraErrorKind::CallFunction(msg) =>
            PyTeraRenderException::new_err(fmt_with_chain(format!("Function error: {}", msg), source_chain)),

        TeraErrorKind::CallTest(msg) =>
            PyTeraRenderException::new_err(fmt_with_chain(format!("Test error: {}", msg), source_chain)),

        TeraErrorKind::FilterNotFound(msg) =>
            PyTeraRenderException::new_err(fmt_with_chain(format!("Filter '{}' not found", msg), source_chain)),

        TeraErrorKind::TemplateNotFound(msg) =>
            PyTeraRenderException::new_err(fmt_with_chain(format!("Template '{}' not found", msg), source_chain)),

        TeraErrorKind::TestNotFound(msg) =>
            PyTeraRenderException::new_err(fmt_with_chain(format!("Test '{}' not found", msg), source_chain)),

        TeraErrorKind::FunctionNotFound(msg) =>
            PyTeraRenderException::new_err(fmt_with_chain(format!("Function '{}' not found", msg), source_chain)),

        // 兜底（未知种类）
        _ => PyTeraException::new_err(fmt_with_chain(format!("Unknown Tera error: {}", display_err), source_chain)),
    }
}

impl From<PyTeraError> for PyErr {

    fn from(value: PyTeraError) -> Self {
        
        let err = value.0;
        let source_chain = format_source_chain(&err);
        let display_err = err.to_string();
        
        #[cfg(debug_assertions)]
        {
            eprintln!("Debug: Converting Tera error to PyErr: kind={:?}, display='{}', source_chain='{}'", err.kind, display_err, source_chain);
        }

        map_kind_to_pyerr(&err.kind, &display_err, &source_chain)
    }
}