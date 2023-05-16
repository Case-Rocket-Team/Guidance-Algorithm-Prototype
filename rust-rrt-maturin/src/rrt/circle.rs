use std::f64::consts::PI;

use num_traits::signum;

pub fn circle_from(p1: (isize, isize), p2: (isize, isize), tang: (isize, isize)) -> (isize, isize, (isize, isize), (isize, isize)) {
    let p1_f64 = (p1.0 as f64, p1.1 as f64);
    let p2_f64 = (p2.0 as f64, p2.1 as f64);
    let tang_f64 = (tang.0 as f64, tang.1 as f64);

    let tang_norm = normalize(tang_f64);
    let pvec = (p2_f64.0 - p1_f64.0, p2_f64.1 - p1_f64.1);
    let pnorm = norm(pvec);
    let pvec_normalized = (pvec.0 / pnorm, pvec.1 / pnorm);

    let cos_phi = pvec_normalized.0 * tang_norm.0 + pvec_normalized.1 * tang_norm.1;
    
    let (arclen, radius, center, head_new) = if (cos_phi - 1.0).abs() < f64::EPSILON || (cos_phi + 1.0).abs() < f64::EPSILON {
        let center = (p1_f64.0 - (-tang_norm.1) * f64::INFINITY, p1_f64.1 - (tang_norm.0) * f64::INFINITY);
        (pnorm, f64::INFINITY, center, tang_f64)
    } else {
        let sin_phi = pvec_normalized.1 * tang_norm.0 - pvec_normalized.0 * tang_norm.1;
        let radius = pnorm / (2.0 * sin_phi);
        let center = (p1_f64.0 - (tang_norm.1) * radius, p1_f64.1 + (tang_norm.0) * radius);

        //println!("{},{}", sin_phi.signum(),radius.signum());

        let rel_p2 = (p2_f64.0 - center.0, p2_f64.1 - center.1);
        
        
        
        let dot = tang_f64.0 * rel_p2.0 + tang_f64.1 * rel_p2.1;

        let direct = if signum(dot) > 0.0 { 0.0 } else { -2.0 * PI };
        let arclen = (radius * ((sin_phi.abs()).asin()*2.0 + direct)).abs();
        let pc = (center.0 - p2_f64.0, center.1 - p2_f64.1);
        let pc_sign = radius.signum();
        let head_new = (pc.1 * pc_sign, -pc.0 * pc_sign);
        (arclen, radius,center,head_new)
    };

    
    
   

    (
        radius.round() as isize,
        arclen.round() as isize,
        ((head_new.0*10.0).round() as isize, (head_new.1*10.0).round() as isize),
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


fn calculate_center(x1: f64, x2: f64, y1: f64, y2: f64, m: f64) -> (f64, f64) {
    let numerator1 = m * x1.powi(2) - m * x2.powi(2) - m * y1.powi(2) + 2.0 * m * y1 * y2 - m * y2.powi(2) - 2.0 * x1 * y1 + 2.0 * x1 * y2;
    let denominator1 = 2.0 * m * x1 - 2.0 * m * x2 - 2.0 * y1 + 2.0 * y2;

    let numerator2 = 2.0 * m * x1 * y1 - 2.0 * m * x2 * y1 + x1.powi(2) - 2.0 * x1 * x2 + x2.powi(2) - y1.powi(2) + y2.powi(2);
    let denominator2 = 2.0 * m * x1 - 2.0 * m * x2 - 2.0 * y1 + 2.0 * y2;

    return (numerator1/denominator1, numerator2/denominator2);
}