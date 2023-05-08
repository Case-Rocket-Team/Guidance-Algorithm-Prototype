import rust_rrt_maturin as rrtM

def circle_from(p1,p2):
    return rrtM.circle_from(p1,p2)

def new_point(x,y,tx,ty,gas):
    return rrtM.point_new(int(x),int(y),int(10*tx),int(10*ty),int(gas))

# Create points
def rrt(startx,starty,tangx,tangy,goalx,goaly,gas, num_points = 4, min_turn =5, max_curve = 15, max_search = 5, margin = 10):
    start = rrtM.point_new(startx, starty, tangx, tangy,gas)
    goal = rrtM.point_new(goalx, goaly, 0, 0, 0)
    # Create HyperParams
    hp = rrtM.hp_new(num_points, min_turn, max_curve, max_search, margin)

    # Create PyRRTWrapper
    algo = rrtM.rrt_new(start, goal, hp)

    # Run the RRT algorithm
    path = None
    while path is None:
        path = algo.step()
    path.append(goal)
    return path
