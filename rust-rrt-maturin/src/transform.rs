pub struct GPSRef {
    ref_lat: f64,
    ref_lon: f64,
    ref_alt: f64,
    ecef_ref: [f64;3],
    r_matrix: [[f64; 3]; 3],
    jacobian_matrix: [[f64; 3]; 3],
}

impl GPSRef {
    pub fn new(ref_lat: f64, ref_lon: f64, ref_alt: f64) -> Self {
        let (r_matrix, ecef_ref, jacobian_matrix) = Self::gps_to_enu_matrix_approx(ref_lat, ref_lon, ref_alt);
        GPSRef {
            ref_lat,
            ref_lon,
            ref_alt,
            ecef_ref,
            r_matrix,
            jacobian_matrix,
        }
    }
    
    
    pub fn convert(&self, lat: f64, lon: f64, alt: f64) -> (f64, f64, f64) {
        // difference between current point and reference 
        let diff = [lat - self.ref_lat, lon - self.ref_lon, alt - self.ref_alt];
        println!("{:?}", diff);
        // find the ECEF transform by multipliyng 
        let enu = matmul_3d(matmul_3d(diff, self.jacobian_matrix),self.r_matrix);

        return (enu[0], enu[1], enu[2]);
    }

    
    fn gps_to_enu_matrix_approx(ref_lat: f64, ref_lon: f64, ref_alt: f64) -> ([[f64; 3]; 3], [f64; 3], [[f64; 3]; 3]) {
        // Constants for WGS84 ellipsoid
        let a = 6_378_137.0; // semi-major axis
        let f = 1.0 / 298.257223563; // flattening
        let e_sq = 2.0 * f - f * f; // square of eccentricity

        // Convert reference latitude and longitude to radians
        let ref_lat_rad = ref_lat.to_radians();
        let ref_lon_rad = ref_lon.to_radians();

        // Calculate prime vertical radius of curvature
        let n = a / (1.0 - e_sq * ref_lat_rad.sin().powi(2)).sqrt();

        // Calculate ECEF coordinates of the reference point
        let x0 = (n + ref_alt) * ref_lat_rad.cos() * ref_lon_rad.cos();
        let y0 = (n + ref_alt) * ref_lat_rad.cos() * ref_lon_rad.sin();
        let z0 = (n * (1.0 - e_sq) + ref_alt) * ref_lat_rad.sin();

        // Create ECEF to ENU rotation matrix
        let r = [
            [-ref_lon_rad.sin(), ref_lon_rad.cos(), 0.0],
            [-ref_lat_rad.sin() * ref_lon_rad.cos(), -ref_lat_rad.sin() * ref_lon_rad.sin(), ref_lat_rad.cos()],
            [ref_lat_rad.cos() * ref_lon_rad.cos(), ref_lat_rad.cos() * ref_lon_rad.sin(), ref_lat_rad.sin()]
        ];

        // Create approximate GPS to ECEF matrix
        let cft = a * e_sq * ref_lat_rad.sin() * ref_lat_rad.cos() / (1.0 - e_sq * ref_lat_rad.sin().powi(2)).powf(3.0 / 2.0); //cursed first term
        let jacobian = [
            [
                cft * ref_lat_rad.cos() * ref_lon_rad.cos() - (n + ref_alt) * ref_lat_rad.sin() * ref_lon_rad.cos(),
                -(n + ref_alt) * ref_lat_rad.cos() * ref_lon_rad.sin(),
                ref_lat_rad.cos() * ref_lon_rad.cos()
            ],
            [
                cft * ref_lat_rad.cos() * ref_lon_rad.sin() - (n + ref_alt) * ref_lat_rad.sin() * ref_lon_rad.sin(),
                (n + ref_alt) * ref_lat_rad.sin() * ref_lon_rad.sin(),
                ref_lat_rad.cos() * ref_lon_rad.sin()
            ],
            [
                cft * (1.0 - e_sq) * ref_lat_rad.sin() + (n + ref_alt) * ref_lon_rad.cos(),
                0.0,
                ref_lat_rad.sin()
            ]
        ];

        // Combine ECEF to ENU and GPS to ECEF matrices to get the final GPS to ENU matrix
        return (r, [x0, y0, z0], jacobian);
    }
}



fn matmul_3d(v: [f64; 3], m: [[f64; 3]; 3]) -> [f64; 3] {
    let mut res = [0.0; 3];

    for i in 0..3 {
        for j in 0..3 {
            res[i] += m[i][j] * v[j];
        }
    }

    res
}
