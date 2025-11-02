use crate::error::PyTeraError;
use crate::utils::pyany_to_serde_json_value;
use pyo3::{prelude::*, pyclass, types::PyDict, PyResult};
use tera::{Context, Tera};

#[pyclass]
pub struct PyTera {
    tera: Tera,
}

#[pymethods]
impl PyTera {
    #[new]
    fn new(glob: &str) -> PyResult<Self> {
        let tera = Tera::new(glob).map_err(|e| PyTeraError::from(e))?; // PyTeraError -> PyErr via From
        Ok(PyTera { tera })
    }

    #[pyo3(signature = (template, **kwargs))]
    fn render_template(
        &self,
        py: Python<'_>,
        template: &str,
        kwargs: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<String> {
        // 一次性把整个 kwargs 转换为 serde_json::Value，并批量构建 Context，减少克隆与哈希扩容
        let ctx = if let Some(kwargs) = kwargs {
            let value = pyany_to_serde_json_value(&kwargs.as_any())?;
            Context::from_serialize(&value).map_err(PyTeraError::from)?
        } else {
            Context::new()
        };

        // 渲染阶段释放 GIL，降低与 Python 线程的竞争
        let rendered_result = py
            .allow_threads(|| self.tera.render(template, &ctx))
            .map_err(PyTeraError::from)?;

        Ok(rendered_result)
    }

    fn templates(&self) -> PyResult<Vec<&String>> {
        let tpls = self.tera.templates.keys().collect();
        Ok(
            tpls
        )
    }
}
