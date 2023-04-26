use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::types::IntoPyDict;
use pyo3::wrap_pyfunction;
mod rrt;
use rrt::{Point,HyperParams,RRTWrapper};

#[pyclass]
pub struct PyPoint {
    inner: Point<isize>,
}

#[pyclass]
pub struct PyHyperParams {
    inner: HyperParams,
}

#[pyclass]
pub struct PyRRTWrapper {
    inner: RRTWrapper,
}


impl PyPoint {
    fn new(x: isize, y: isize, tx: isize, ty: isize, gas: isize) -> PyResult<Self> {
        Ok(Self {
            inner: Point::point_new(x, y, tx, ty, gas),
        })
    }
}


#[pymethods]
impl PyPoint {
   fn to_dict(&self, py: Python) -> PyResult<Py<PyDict>> {
        let point = &self.inner;
        let dict = PyDict::new(py);
        dict.set_item("coords", (point.coords.0, point.coords.1))?;
        dict.set_item("tang", (point.tang.0, point.tang.1))?;
        dict.set_item("gas", point.gas)?;
        dict.set_item("dist_2_goal", point.dist_2_goal)?;
        Ok(dict.into())
    }
}



impl PyHyperParams {
    fn new(
        num_points: usize,
        min_turn: isize,
        max_curve: isize,
        max_search: isize,
        margin: isize,
    ) -> PyResult<Self> {
        Ok(Self {
            inner: HyperParams::hp_new(num_points, min_turn, max_curve, max_search, margin),
        })
    }
}


impl PyRRTWrapper {
    fn new(start: &PyPoint, goal: &PyPoint, hp: &PyHyperParams) -> Self {
        Self {
            inner: RRTWrapper::rrt_new(start.inner, goal.inner, hp.inner),
        }
    }
}

#[pymethods]
impl PyRRTWrapper {
    fn step(&mut self, py: Python) -> Option<Vec<Py<PyPoint>>> {
        if let Some(path) = self.inner.step() {
            let py_path: Vec<Py<PyPoint>> = path
                .iter()
                .filter_map(|point_option| {
                    point_option.as_ref().map(|point| {
                        let py_point = PyPoint { inner: *point };
                        Py::new(py, py_point).unwrap()
                    })
                })
                .collect();
            Some(py_path)
        } else {
            None
        }
    }
}


#[pyfunction]
fn circle_from(p1: &PyPoint, p2: &PyPoint) -> (isize, isize, (isize, isize), (isize, isize)) {
    rrt::circle::circle_from(p1.inner.coords, p2.inner.coords, p1.inner.tang)
}

#[pyfunction]
fn point_new(x: isize, y: isize, tx: isize, ty: isize, gas: isize) -> PyResult<PyPoint> {
    PyPoint::new(x, y, tx, ty, gas)
}

#[pyfunction]
fn hp_new(
    num_points: usize,
    min_turn: isize,
    max_curve: isize,
    max_search: isize,
    margin: isize,
) -> PyResult<PyHyperParams> {
    PyHyperParams::new(num_points, min_turn, max_curve, max_search, margin)
}

#[pyfunction]
fn rrt_new(start: &PyPoint, goal: &PyPoint, hp: &PyHyperParams) -> PyRRTWrapper {
    PyRRTWrapper::new(start, goal, hp)
}


#[pymodule]
fn rust_rrt_maturin(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyPoint>()?;
    m.add_class::<PyHyperParams>()?;
    m.add_function(wrap_pyfunction!(circle_from, m)?)?;
    m.add_function(wrap_pyfunction!(point_new, m)?)?;
    m.add_function(wrap_pyfunction!(hp_new, m)?)?;
    m.add_function(wrap_pyfunction!(rrt_new, m)?)?;
    Ok(())
}
