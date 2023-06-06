from matplotlib.collections import LineCollection
import numpy as np
import rust_funcs
import matplotlib.pyplot as plt
from parafoil_sim import State


ax = plt.figure()
flat = ax.add_subplot(221)
threed = ax.add_subplot(222, projection='3d')
error_chart = ax.add_subplot(223)

glide_ratio = 6.5

MIN_TURN = 13

r_pnts = [rust_funcs.new_point(0,0,-1,1,111 * 2),
          rust_funcs.new_point(50,50,1,-1,111),
          rust_funcs.new_point(100,100,1,-1,0)]


payload = State(max_wind=0.1)
payload.pos = np.array((0,0,111 * 2 /glide_ratio),dtype='float64')
payload.vel = np.array((0,0,0),dtype='float64')
payload.setHeadingRad(np.arctan2(1,-1))

x = []
y = []
z = []
c = []
d = []
g = []

payload.turningRadius = 0
w_idx = 0 #index of the current waypoint
waypoints = []
for point in r_pnts:
    waypoints.append((point,point.to_dict()["gas"]/glide_ratio))

current_waypoint = waypoints[w_idx][0].to_dict()


start = rust_funcs.new_point(payload.pos[0], payload.pos[1],
                         np.real(payload.heading * 5),np.imag(payload.heading * 5),
                         payload.pos[2])

desired_radius, desired_arclen, _, desired_center = rust_funcs.circle_from(start, waypoints[w_idx][0])


cheat_in_error_previous = 0
integral = 0

while payload.pos[2] > 0:
    #create a new PyPoint out of the current position
    current_pos = rust_funcs.new_point(payload.pos[0], payload.pos[1],
                         np.real(payload.heading),np.imag(payload.heading),
                         payload.pos[2])
    

    if (payload.pos[2] < waypoints[w_idx][1]) and w_idx < len(waypoints)-1:
        w_idx += 1
        flat.plot(payload.pos[0], payload.pos[1], 'k*', markersize=10)
        threed.plot(payload.pos[0], payload.pos[1], payload.pos[2], 'k*')
        error_chart.vlines([len(c)-1],[-10],[10],colors=['#80ff20'])
        prev_waypoint = current_waypoint

        current_waypoint = waypoints[w_idx][0].to_dict()
        integral = 0
        cheat_in_error_previous = 0
        
        desired_radius, desired_arclen, _, center = rust_funcs.circle_from(waypoints[w_idx-1][0], waypoints[w_idx][0])

    #plt.show()
    # use circle_from to find new turning radius:
    radius, arclen, newhead, center = rust_funcs.circle_from(current_pos, waypoints[w_idx][0])

    #center_dist = np.linalg.norm(np.array(center) - np.array(current_pos.to_dict()["coords"]))
    #desired_center_dist = np.linalg.norm(np.array(center) - np.array(prev_waypoint["coords"]))
    """"""
    K1 = 1
    
    Kp = 1e-5
    Ki = 0
    Kd = 0
    error_limit = 100
    integral_limit = 10 * Ki

    """
    error_gas = (payload.pos[2] - waypoints[w_idx][1]) - arclen

    d_error = desired_radius**2 - center_dist - radius**2 #positive inside, negative outside


    error_radius = d_error
    integral += error_radius * payload.dt
    derivative = (error_radius - previous_error) / payload.dt
    control = Kp * error_radius + Ki * integral + Kd * derivative
    
    payload.turningRadius = 
    """
    center_dist = np.linalg.norm(np.array(desired_center) - np.array(payload.pos[0],payload.pos[1])) # absolute distance from the center of the desired
    d_error = (abs(desired_radius) - center_dist) # difference in distance from the desired radius
    error_gas = (payload.pos[2] - waypoints[w_idx][1])*glide_ratio - arclen # Whether too much (if positive) or too little (if negative) gas will be left at the end of the turn
    desired_cheat_in = -K1 * error_gas #scaling error gas
    cheat_in_error = (desired_cheat_in - d_error)
    
    proportional = Kp * cheat_in_error
    derivative = Kd * (cheat_in_error - cheat_in_error_previous)
    integral = np.clip(integral + Ki * (cheat_in_error) * payload.dt, -integral_limit, integral_limit)
    correction = proportional + derivative + integral
    
    desired_curvature = correction if desired_radius == 0 else correction + abs(1 / desired_radius)
    desired_curvature = desired_curvature.clip(-1/MIN_TURN,1/MIN_TURN)
    if desired_curvature == 0:
        payload.turningRadius = 0
    else:
        payload.turningRadius = 1 / desired_curvature * np.sign(desired_radius)
    cheat_in_error_previous = cheat_in_error



    """
    
    MAX_TURN = 1e5
    arc_ratio = 1 if arclen == 0 else np.exp(-desired_arclen/arclen)
    dist_left = abs(payload.pos[2] - waypoints[w_idx][1])*glide_ratio - arclen
    turn = 0 if desired_radius == 0 else radius/desired_radius
    if abs(radius) >= MAX_TURN:
        print(f"radius {radius} too large, intended radius {desired_radius}")
    if np.sign(desired_radius) != np.sign(radius):
        print("signs don't match")
        #payload.turningRadius = -payload.turningRadius
    turn = 0 if desired_arclen == 0 else dist_left/desired_arclen
    payload.turningRadius = radius * (1 + turn) * (arc_ratio) + desired_radius * (1-arc_ratio)
    """
    
    
    x.append(payload.pos[0])
    y.append(payload.pos[1])
    z.append(payload.pos[2])
    c.append(cheat_in_error)
    d.append(d_error)
    g.append(desired_cheat_in)
    
    payload.update()






# -- plotting -- #

y__lim = 5e2

#flat.plot(x,y,color='blue',linewidth=1)

threed.plot(x,y,z,color='blue',linewidth=1)
error_chart.plot(c,color='blue',linewidth=1, label="cheat_in_error")
error_chart.plot(d,color='red',linewidth=1 ,label="d_error")
error_chart.plot(g,color='green',linewidth=1, label="error_gas")
error_chart.legend()
#error_chart.set_ylim(bottom=-y__lim, top=y__lim)

for i in range(len(r_pnts)-1):
    radius, arclen, newhead, center = rust_funcs.circle_from(r_pnts[i], r_pnts[i+1])
    current = r_pnts[i].to_dict()
    currentX = current["coords"][0]
    currentY = current["coords"][1]
    next = r_pnts[i + 1].to_dict()
    nextX = next["coords"][0]
    nextY = next["coords"][1]
    flat.plot((nextX,currentX),(nextY,currentY),color='green',linewidth=1)
    flat.plot(currentX, currentY, 'ro', markersize=3)
    threed.plot(currentX, currentY, current["gas"]/glide_ratio, 'ro', markersize=3)

    #plt.show()
    #print("({},{}) -> ({},{})".format(currentX, currentY, parentX, parentY))
    #print(center)
    #plt.plot(center[0], center[1], 'bo', markersize=3)
    num_points = 100  # Number of points to generate along the arc
    p1 = np.array([currentX, currentY])-np.array(center)
    p2 = np.array([nextX, nextY])-np.array(center)
    ang = float(arclen)/float(radius)
    t = np.linspace(0, ang, num_points)
    rot = np.array([[np.cos(t), -np.sin(t)],[np.sin(t), np.cos(t)]])
    rots = np.array([rot[:,:,i].dot(p1) for i in range(num_points)])

    des_x = center[0] + rots[:,0] # x-coordinates of the arc points
    des_y = center[1] + rots[:,1]  # y-coordinates of the arc points
    des_z = np.linspace(current["gas"]/glide_ratio, next["gas"]/glide_ratio, num_points)
        
    flat.plot(des_x, des_y, color='orange', linewidth=2)
    threed.plot(des_x, des_y, des_z, color='orange', linewidth=2)
    #unit_head = np.array(newhead) / np.linalg.norm(np.array(newhead))
    #newHead_end = np.array([currentX, currentY]) + unit_head *3
    #plt.plot((currentX, newHead_end[0]), (currentY, newHead_end[1]), color='blue', linewidth=1)

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
lc = LineCollection(segments, cmap='viridis')
lc.set_array(c)
lc.set_linewidth(2)
flat.add_collection(lc)
#plt.colorbar(lc)
plt.show()