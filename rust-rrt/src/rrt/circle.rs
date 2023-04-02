use std::ops::Sub;
use std::ops::Mul;
use std::ops::Div;
use std::ops::Add;
use std::ops::Neg;

pub fn circle_from<T>(
    p1: (T, T),
    p2: (T, T),
    tang: (T, T),
) -> (T, T, (T, T), (T, T))
where
    T: Sub<Output = T>
        + Add<Output = T>
        + Mul<Output = T>
        + Div<Output = T>
        + Neg<Output = T>
        + Copy
        + PartialOrd
        + PartialEq,
    f64: From<T>,
{
    let tang_norm = normalize(tang);
    let pvec = (p2.0 - p1.0, p2.1 - p1.1);
    let pnorm = norm(pvec);
    let pvec_3 = (pvec.0 / pnorm, pvec.1 / pnorm, T::from(0.0).unwrap());
    let tang_3 = (tang_norm.0, tang_norm.1, T::from(0.0).unwrap());
    let sin_phi = cross(pvec_3, tang_3).2;
    let radius = pnorm / (T::from(2.0).unwrap() * sin_phi);
    let center = (
        p1.0 - (-tang_norm.1) * radius,
        p1.1 - (tang_norm.0) * radius,
    );

    let arclen = radius * sin_phi.abs().asin();
    let pc = (center.0 - p2.0, center.1 - p2.1);
    let pc_sign = radius.signum();
    let head_new = (-pc.1 * pc_sign, pc.0 * pc_sign);
    (radius, arclen, head_new, center)
}

fn norm<T>(vector: (T, T)) -> T
where
    T: Mul<Output = T> + Add<Output = T> + Copy,
    f64: From<T>,
{
    (vector.0 * vector.0 + vector.1 * vector.1).sqrt()
}

fn normalize<T>(vector: (T, T)) -> (T, T)
where
    T: Mul<Output = T> + Div<Output = T> + Copy,
    f64: From<T>,
{
    let length = norm(vector);
    (vector.0 / length, vector.1 / length)
}

fn cross<T>(a: (T, T, T), b: (T, T, T)) -> (T, T, T)
where
    T: Mul<Output = T> + Sub<Output = T> + Copy,
{
    (
        a.1 * b.2 - a.2 * b.1,
        a.2 * b.0 - a.0 * b.2,
        a.0 * b.1 - a.1 * b.0,
    )
}
