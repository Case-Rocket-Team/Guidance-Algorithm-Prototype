mod rrt;
mod transform;

fn main() {
/*     // Test the function with a reference GPS coordinate (latitude, longitude, altitude)
    let ref_lat = 40.7128;
    let ref_lon = -74.0060;
    let ref_alt = 30.0;

    let gpsref = transform::GPSRef::new(ref_lat,ref_lon,ref_alt);
    
    // create the GPSRef object
    //let refer = transform::GPSRef()

    println!("{:?}", gpsref.convert(40.673247418108275,-73.95520343242187,30.0));
}
*/
    let goal = rrt::Point {
        coords: (10, 40),
        tang: (0, 0),
        gas: 0,
        dist_2_goal: None,
    };
    let mut start = rrt::Point {
        coords: (450, 450),
        tang: (1, 3),
        gas: 1500,
        dist_2_goal: None,
    };
    let (_, arc_len, _, _) = rrt::circle::circle_from(start.coords, goal.coords, start.tang);
    start.dist_2_goal = Some(arc_len);
    let hp = rrt::HyperParams::hp_new(4,13, 100, 5, 10);

    let mut rrt = rrt::RRTWrapper::rrt_new(start, goal, hp);

    loop {
        if let Some(path) = rrt.step() {
            for point in path.iter() {
                if let Some(point) = point {
                    println!("({}, {})", point.coords.0, point.coords.1);
                } else {
                    break;
                }
            }
            break;
        }
    }
}