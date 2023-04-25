use std::cmp::Ord;
use std::ops::Sub;

use rand::Rng;

use self::{circle::circle_from, path_array::Node};

pub mod circle;
mod heap;
mod path_array;

const MAX_PATH_LENGTH: usize = 127;
const DO_DEBUG: bool = true;

#[derive(Eq, PartialEq, PartialOrd, Copy, Clone)]
#[repr(C)]
pub struct Point<T>
where
    T: Sub + Ord + Copy,
    <T as Sub>::Output: Ord,
{
    pub coords: (T, T),
    pub tang: (T, T),
    pub gas: T,
    pub dist_2_goal: Option<T>,
}

fn print_point(point: Point<isize>) {
    let dist_str = match point.dist_2_goal {
        Some(dist) => format!("{}", dist),
        None => String::from("None"),
    };
    println!(
        "({}, {}) gas: {}, dist_2_goal: {}",
        point.coords.0, point.coords.1, point.gas, dist_str
    );
}

impl<T> Ord for Point<T>
where
    T: Sub + Ord + Copy,
    <T as Sub>::Output: Ord,
{
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        let self_dist = &(self.gas - self.dist_2_goal.unwrap());
        let other_dist = &(other.gas - other.dist_2_goal.unwrap());
        self_dist.cmp(other_dist)
    }
}

impl Point<isize> {
    #[no_mangle]
    pub extern "C" fn point_new(x: isize, y: isize, tx: isize, ty: isize, gas: isize) -> Point<isize> {
        Point {
            coords: (x, y),
            tang: (tx, ty),
            gas,
            dist_2_goal: None,
        }
    }
    fn gen_rand_point(&self, goal: Point<isize>, min_rad: isize, search_rad: isize) -> Point<isize> {
        let mut rng = rand::thread_rng();
        loop {
            let (dx, dy)  = if search_rad <= 1 {
                (0,0)
            }else {
                (rng.gen_range(-search_rad..search_rad),rng.gen_range(-search_rad..search_rad))
            };

            let (radius, arclen, head_new, center) = circle_from(self.coords, (self.coords.0 + dx, self.coords.1 + dy), self.tang);
            if radius >= min_rad {
                let (_, dist_goal, _, _) = circle_from((self.coords.0 + dx, self.coords.1 + dy), goal.coords, head_new);
                return Point {
                    coords: (self.coords.0 + dx, self.coords.1 + dy),
                    tang: head_new,
                    gas: self.gas - arclen,
                    dist_2_goal: Some(dist_goal),
                };
            }
        }
    }
}

fn valid_point(pnt: Point<isize>, goal: Point<isize>) -> bool {
    let (_, arc_len, _, _) = circle_from(pnt.coords, goal.coords, pnt.tang);
    arc_len <= pnt.gas && pnt.gas > 0 && pnt.dist_2_goal.unwrap_or(1) > 0
}
#[repr(C)]
pub struct HyperParams {
    pub num_points: usize,
    pub min_turn: isize,
    pub max_curve: isize,
    pub max_search: isize,
    pub margin: isize,
}


impl HyperParams {
    #[no_mangle]
    pub extern "C" fn hp_new(num_points: usize, min_turn: isize, max_curve: isize, max_search: isize, margin: isize) -> HyperParams {
        HyperParams {
            num_points,
            min_turn,
            max_curve,
            max_search,
            margin,
        }
    }
}


#[repr(C)]
pub struct RRTWrapper {
    start: Point<isize>,
    goal: Point<isize>,
    hp: HyperParams,
    heap: heap::BinaryHeap<Node<Point<isize>>>,
    tree: path_array::FlatArray<Point<isize>>,
}

impl RRTWrapper {
    #[no_mangle]
    pub extern "C" fn rrt_new(start: Point<isize>, goal: Point<isize>, hp: HyperParams) -> Self {
        let mut r = RRTWrapper {
            start,
            goal,
            hp,
            heap: heap::BinaryHeap::new(),
            tree: path_array::FlatArray::new(),
        };
        r.initialize();
        return r;
    }

    #[no_mangle]
    pub extern "C" fn step(&mut self) -> Option<[Option<Point<isize>>; MAX_PATH_LENGTH]> {
        if let Some(idx) = self.rrt() {
            Some(self.get_path_fixed_size(idx))
        } else {
            None
        }
    }

    fn initialize(&mut self) {
        self.heap.push(Node {
            data: self.start.clone(),
            parent_index: None,
        });
    }

    fn get_path_fixed_size(&self, goal_index: usize) -> [Option<Point<isize>>; MAX_PATH_LENGTH] {
        let mut path = [None; MAX_PATH_LENGTH];
        let mut current_index = Some(goal_index);
        let mut index = 0;
        while let Some(idx) = current_index {
            let node = self.tree.get_node(idx).unwrap();
            path[index] = Some(node.data.clone());
            current_index = node.parent_index;
            index += 1;
        }

        // Reverse the path in-place
        path[..index].reverse();
        path
    }

    fn rrt(&mut self) -> Option<usize> {
        if let Some(pnt_node) = self.heap.pop() {
            let pnt = pnt_node.data;
            let idx = self.tree.add_node(pnt, pnt_node.parent_index).unwrap();
            if DO_DEBUG {
                print_point(pnt);
            }
            let dist_remain = pnt.gas - pnt.dist_2_goal.unwrap();
            let (_, arc_len, _, _) = circle_from(pnt.coords, self.goal.coords, pnt.tang);
            if dist_remain <= self.hp.margin { //TODO and the gas is close to 0
                return Some(idx);
            }

            let mut num_points = 0;
            while num_points < self.hp.num_points {
                let new_pnt = pnt.gen_rand_point(self.goal, self.hp.min_turn,dist_remain);

                let new_dist_remain = new_pnt.gas - new_pnt.dist_2_goal.unwrap();
                if valid_point(new_pnt, self.goal) && new_dist_remain >= 0 {
                    self.heap.push(Node {
                        data: new_pnt,
                        parent_index: Some(idx),
                    });
                    num_points += 1;
                }
            }
        } else {
            //TODO search ig
        }
        return None;
    }
}
