pub fn circle_from(p1: (isize, isize), p2: (isize, isize), tang: (isize, isize)) -> (isize, isize, (isize, isize), (isize, isize)) {
    let p1_f64 = (p1.0 as f64, p1.1 as f64);
    let p2_f64 = (p2.0 as f64, p2.1 as f64);
    let tang_f64 = (tang.0 as f64, tang.1 as f64);

    let tang_norm = normalize(tang_f64);
    let pvec = (p2_f64.0 - p1_f64.0, p2_f64.1 - p1_f64.1);
    let pnorm = norm(pvec);
    let pvec_normalized = (pvec.0 / pnorm, pvec.1 / pnorm);

    let cos_angle = pvec_normalized.0 * tang_norm.0 + pvec_normalized.1 * tang_norm.1;

    let (arclen, radius) = if (cos_angle - 1.0).abs() < f64::EPSILON {
        (pnorm, f64::INFINITY)
    } else if (cos_angle + 1.0).abs() < f64::EPSILON { // Added condition
        (pnorm, f64::INFINITY)
    } else {
        let sin_phi = pvec_normalized.0 * tang_norm.1 - pvec_normalized.1 * tang_norm.0;
        let radius = pnorm / (2.0 * sin_phi);
        //println!("{},{}", sin_phi.signum(),radius.signum());
        let arclen = radius.abs() * sin_phi.abs().asin() * 2.0;
        (arclen, radius)
    };

    let center = (p1_f64.0 - (-tang_norm.1) * radius, p1_f64.1 - (tang_norm.0) * radius);
    let pc = (center.0 - p2_f64.0, center.1 - p2_f64.1);
    let pc_sign = radius.signum();
    let head_new = (-pc.1 * pc_sign, pc.0 * pc_sign);

    (
        radius.round() as isize,
        arclen.round() as isize,
        (head_new.0.round() as isize, head_new.1.round() as isize),
        (center.0.round() as isize, center.1.round() as isize),
    )
}

fn norm(vector: (f64, f64)) -> f64 {
    (vector.0.powi(2) + vector.1.powi(2)).sqrt()
}

fn normalize(vector: (f64, f64)) -> (f64, f64) {
    let length = norm(vector);
    (vector.0 / length, vector.1 / length)
}