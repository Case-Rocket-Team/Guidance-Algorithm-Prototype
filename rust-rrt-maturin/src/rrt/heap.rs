const MAX_HEAP_SIZE: usize = 127;

pub struct BinaryHeap<T: Ord + Copy> {
    heap: [Option<T>; MAX_HEAP_SIZE],
    size: usize,
}

impl<T: Ord + Copy> BinaryHeap<T> {
    pub fn new() -> BinaryHeap<T> {
        BinaryHeap {
            heap: [None; MAX_HEAP_SIZE],
            size: 0,
        }
    }

    pub fn push(&mut self, item: T) {
        if self.size >= MAX_HEAP_SIZE {
            panic!("Heap overflow");
        }
        let index = self.size;
        self.heap[index] = Some(item);
        self.size += 1;
        if self.size == 1 {
            return;
        }
        let mut current = index;
        let mut parent = (current - 1) / 2;
        // TODO: unwrap_or 
        while self.heap[parent].as_ref().unwrap() > self.heap[current].as_ref().unwrap() {
            self.heap.swap(current, parent);
            if (parent == 0){ //check for if the item bubbles up to the top of the heap
                //parent = null;
                return;
            }
            current = parent;
            parent = (current - 1) / 2;
        }
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.size == 0 {
            return None;
        }
        let index = 0;
        let result = self.heap[index].take().unwrap();
        let last_index = self.size - 1;
        self.heap.swap(index, last_index);
        self.size -= 1;
        let mut current = index;
        loop {
            let left_child = current * 2 + 1;
            let right_child = current * 2 + 2;
            let mut smallest = current;
            if left_child < self.size && self.heap[left_child].as_ref().unwrap() < self.heap[smallest].as_ref().unwrap() {
                smallest = left_child;
            }
            if right_child < self.size && self.heap[right_child].as_ref().unwrap() < self.heap[smallest].as_ref().unwrap() {
                smallest = right_child;
            }
            if smallest != current {
                self.heap.swap(smallest, current);
                current = smallest;
            } else {
                break;
            }
        }
        Some(result)
    }
}
