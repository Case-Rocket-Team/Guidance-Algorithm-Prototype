import ctypes
from ctypes import c_double, c_size_t, c_bool

full_path = "/home/dryogurt/Documents/Habitats/CaseRocketTeam/Guidance-Algorithm-Prototype/rust-rrt/"

# Load the Rust library
lib = ctypes.cdll.LoadLibrary(full_path+"target/release/librust_rrt.so")

class OrderedFloat(ctypes.Structure):
    _fields_ = [("value", c_double)]

class Point(ctypes.Structure):
    _fields_ = [
        ("coords", OrderedFloat * 2),
        ("tang", OrderedFloat * 2),
        ("gas", OrderedFloat),
        ("dist_2_goal", ctypes.POINTER(OrderedFloat)),
    ]

class HyperParams(ctypes.Structure):
    _fields_ = [
        ("num_points", c_size_t),
        ("min_turn", c_size_t),
        ("max_curve", c_size_t),
        ("max_search", c_size_t),
        ("margin", c_size_t),
    ]

class RRTWrapper(ctypes.Structure):
    pass

MAX_PATH_LENGTH = 127
PathArray = Point * MAX_PATH_LENGTH


# Configure the argument and return types for the Rust functions
lib.new.argtypes = [Point, Point, HyperParams]
lib.new.restype = ctypes.POINTER(RRTWrapper)
lib.step.argtypes = [ctypes.POINTER(RRTWrapper)]
lib.step.restype = ctypes.POINTER(PathArray)

# Example usage
def main():
    dist_2_goal_start = ctypes.pointer(OrderedFloat(0))
    start = Point((OrderedFloat(0), OrderedFloat(0)), (OrderedFloat(0), OrderedFloat(0)), OrderedFloat(100), dist_2_goal_start)

    dist_2_goal_goal = ctypes.pointer(OrderedFloat(0))
    goal = Point((OrderedFloat(10), OrderedFloat(10)), (OrderedFloat(0), OrderedFloat(0)), OrderedFloat(0), dist_2_goal_goal)

    hp = HyperParams(10, 5, 5, 5, 5)

    rrt = lib.new(start, goal, hp)

    while True:
        result = lib.step(rrt)
        if result:
            break

    path = result.contents
    for i in range(MAX_PATH_LENGTH):
        point = path[i]
        if point:
            print(f"({point.coords[0].value}, {point.coords[1].value})")
        else:
            break

if __name__ == "__main__":
    main()
