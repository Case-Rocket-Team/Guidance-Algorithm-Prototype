import rust_rrt_maturin as rrtM

def circle_from(p1,p2):
    return rrtM.circle_from(p1,p2)

# Create points
def rrt(startx,starty,tangx,tangy,goalx,goaly,gas):
    start = rrtM.point_new(startx, starty, tangx, tangy,gas)
    goal = rrtM.point_new(goalx, goaly, 0, 0, 0)

    # Create HyperParams
    hp = rrtM.hp_new(4,5,15,5,10)

    # Create PyRRTWrapper
    algo = rrtM.rrt_new(start, goal, hp)

    # Run the RRT algorithm
    path = None
    while path is None:
        path = algo.step()
    path.append(goal)
    return path