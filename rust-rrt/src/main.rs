mod rrt;

fn main() {
    let goal = rrt::Point {
        coords: (100, 100),
        tang: (0, 0),
        gas: 1000,
        dist_2_goal: None,
    };
    let mut start = rrt::Point {
        coords: (0, 0),
        tang: (1, 1),
        gas: 1000,
        dist_2_goal: None,
    };
    let (_, arc_len, _, _) = rrt::circle::circle_from(start.coords, goal.coords, start.tang);
    start.dist_2_goal = Some(arc_len);
    let hp = rrt::HyperParams {
        num_points: 4,
        min_turn: 5,
        max_curve: 5,
        max_search: 5,
        margin: 5,
    };

    let mut rrt = rrt::RRTWrapper::new(start, goal, hp);

    loop {
        if let Some(path) = errt.step() {
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
