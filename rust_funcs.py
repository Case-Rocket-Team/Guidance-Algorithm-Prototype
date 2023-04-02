import ctypes
full_path = "/home/dryogurt/Documents/Habitats/CaseRocketTeam/Guidance-Algorithm-Prototype/rust-rrt/"
rust_rrt = ctypes.cdll.LoadLibrary(full_path+"target/release/librust_rrt.so")

circ = rust_rrt.circle_from
circ.argtypes = [ctypes.c_int, ctypes.c_int]
circ.restype = ctypes.c_int
circle_from = circ