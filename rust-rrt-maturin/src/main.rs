mod rrt;

fn main() {
    let goal = rrt::Point {
        coords: (20, 30),
        tang: (0, 0),
        gas: 0,
        dist_2_goal: None,
    };
    let mut start = rrt::Point {
        coords: (10, 20),
        tang: (1, 3),
        gas: 1500,
        dist_2_goal: None,
    };
    let (_, arc_len, _, _) = rrt::circle::circle_from(start.coords, goal.coords, start.tang);
    start.dist_2_goal = Some(arc_len);
    let hp = rrt::HyperParams::hp_new(4, 5, 50, 5, 5);

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
