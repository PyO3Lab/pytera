use pyo3::prelude::*;

use pytera::PyTera;
use crate::error::{PyTeraException, PyTeraRenderException};

mod pytera;
mod error;
mod utils;




#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyTera>()?;

    // 导出自定义异常，避免 Python 侧显示为笼统的 Exception
    m.add("PyTeraException", m.py().get_type::<PyTeraException>())?;
    m.add("PyTeraRenderException", m.py().get_type::<PyTeraRenderException>())?;

    Ok(())
}
