import ctypes
from ctypes import c_int32, c_void_p

full_path = "/home/dryogurt/Documents/Habitats/CaseRocketTeam/Guidance-Algorithm-Prototype/rust-rrt/"

# Load the Rust library
rrt = ctypes.cdll.LoadLibrary(full_path+"target/release/librust_rrt.so")

# Create the Point struct
class Point(ctypes.Structure):
    _fields_ = [("x", c_int32), ("y", c_int32), ("tx", c_int32), ("ty", c_int32), ("gas", c_int32)]

# Define the argtypes and restype for the Rust functions
rrt.point_new.argtypes = [c_int32, c_int32, c_int32, c_int32, c_int32]
rrt.point_new.restype = Point

class HyperParams(ctypes.Structure):
    _fields_ = [
        ("num_points", ctypes.c_size_t),
        ("min_turn", c_int32),
        ("max_curve", c_int32),
        ("max_search", c_int32),
        ("margin", c_int32),
    ]
    
    
class RRTWrapper:
    def __init__(self, start: Point, goal: Point, hp: HyperParams):
        self.obj = rrt.rrt_new(start, goal, hp)

    def step(self):
        # Call the Rust RRTWrapper::step method
        result = rrt.step(self.obj)

        # Convert the result to a Python list (you can also implement a helper function for this)
        path = []
        i = 0
        while True:
            point = result[i]
            if point:
                path.append(Point(point.contents.x, point.contents.y, point.contents.tx, point.contents.ty, point.contents.gas))
            else:
                break
            i += 1

        return path if path else None


# Define the argtypes and restype for the HyperParams constructor
rrt.hp_new.argtypes = [ctypes.c_size_t, c_int32, c_int32, c_int32, c_int32]
rrt.hp_new.restype = HyperParams

# Update RRTWrapper_new argtypes
rrt.rrt_new.restype = c_void_p
rrt.step.argtypes = [c_void_p]
rrt.step.restype = ctypes.POINTER(ctypes.POINTER(Point))
rrt.rrt_new.argtypes = [Point, Point, HyperParams]

def run_rrt(start_x, start_y, start_tangent, goal_x, goal_y, gas):
    # Create the start and goal points
    start = rrt.point_new(start_x, start_y, start_tangent[0], start_tangent[1], gas)
    goal = rrt.point_new(goal_x, goal_y, 0, 0, 0)

    # Create the HyperParams struct
    hp = rrt.hp_new(4, 5, 5, 5, 5)

    # Create the RRTWrapper object
    rrt_wrapper = RRTWrapper(start, goal, hp)

    # Call the RRTWrapper::step method and process the result
    while True:
        path = rrt_wrapper.step()
        if path:
            for point in path:
                print("({}, {})".format(point.x, point.y))
            break
