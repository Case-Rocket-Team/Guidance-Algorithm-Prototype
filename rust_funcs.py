import rust_rrt_maturin as rrt

# Create points
start = rrt.point_new(0, 0, 1, 0, 10)
goal = rrt.point_new(5, 5, 1, 0, 0)

# Create HyperParams
hp = rrt.hp_new(10, 1, 10, 10, 1)

# Create PyRRTWrapper
algo = rrt.rrt_new(start, goal, hp)

# Run the RRT algorithm
path = algo.step()