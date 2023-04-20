use std::cmp::Ordering;

const MAX_ARR_SIZE: usize = 127;

#[derive(Eq, PartialEq, Copy, Clone)]
pub struct Node<T> {
    pub data: T,
    pub parent_index: Option<usize>,
}

impl<T: Copy + PartialEq + PartialOrd> PartialOrd for Node<T> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        match self.data.partial_cmp(&other.data) {
            Some(Ordering::Equal) => self.parent_index.partial_cmp(&other.parent_index),
            cmp => cmp,
        }
    }
}

impl<T: Copy + Eq + Ord> Ord for Node<T> {
    fn cmp(&self, other: &Self) -> Ordering {
        match self.data.cmp(&other.data) {
            Ordering::Equal => self.parent_index.cmp(&other.parent_index),
            cmp => cmp,
        }
    }
}



pub struct FlatArray<T:Copy> {
    nodes: [Option<Node<T>>; MAX_ARR_SIZE],
    size: usize,
}

impl<T: Copy> FlatArray<T> {
    pub fn new() -> Self {
        Self {
            nodes: [None; MAX_ARR_SIZE],
            size: 0,
        }
    }

    pub fn add_node(&mut self, data: T, parent_index: Option<usize>) -> Result<usize, &'static str> {
        if self.size >= MAX_ARR_SIZE {
            return Err("FlatArray is full");
        }

        let new_node = Node { data, parent_index };
        self.nodes[self.size] = Some(new_node);
        self.size += 1;

        Ok(self.size - 1)
    }

    pub fn get_node(&self, index: usize) -> Option<&Node<T>> {
        self.nodes[index].as_ref()
    }

    pub fn get_path(&self, index: usize) -> Vec<&T> {
        let mut path = Vec::new();
        let mut current_index = Some(index);
        while let Some(i) = current_index {
            if let Some(ref node) = self.nodes[i] {
                path.push(&node.data);
                current_index = node.parent_index;
            } else {
                break;
            }
        }
        path.reverse();
        path
    }
}
