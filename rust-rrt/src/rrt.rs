use std::alloc::GlobalAlloc;
use std::cmp::Ord;
use std::ops::Sub;
use std::ops::Mul;
use std::ops::Div;
use std::ops::Add;
use std::ops::Neg;

use self::circle::circle_from;

mod circle;

#[derive(Eq, PartialEq, PartialOrd)]
struct Point<T>
where
    T: Sub + Ord + Copy,
    <T as Sub>::Output: Ord,
{
    coords: (T,T),
    tang: (T, T),
    gas: T,
    dist_2_goal: Option<T>,
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

fn valid_point<T>(pnt: Point<T>, goal: Point<T>)
where
    T: Sub<Output = T>
        + Add<Output = T>
        + Mul<Output = T>
        + Div<Output = T>
        + Neg<Output = T>
        + Copy
        + Ord,
    f64: From<T>
{
    let arc_len = circle_from(pnt.coords, goal.coords, pnt.tang);


}
