import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from mpl_toolkits.mplot3d import Axes3D

import rust_funcs
from parafoil_sim import State

DRAW_STUFF = False
PRINT = False

start_x, start_y = 10, 30
goal_x, goal_y = 450, 450
tang_x, tang_y = 1, 3
gas = 600*6.5
glide_ratio = 6.5
points = []

start_coords = start_x, start_y

goal_coords = goal_x, goal_y

printMe = False

##----##
while True:
    try:
        reet = rust_funcs.rrt(start_x, start_y, tang_x, tang_y, goal_x, goal_y, gas, min_turn=13,max_curve=1000)
        for x in reet:
            points.append(x)
    except:
        print("RRT failed, running again")
    else:
        break
##----##

# separate waypoints by height
waypoints = []
for point in points:
    waypoints.append((point,point.to_dict()["gas"]/glide_ratio))
ax = plt.figure()

payload = State(max_wind=0.2)
payload.pos = np.array((start_x,start_y,gas/glide_ratio),dtype='float64')
payload.vel = np.array((0,0,0),dtype='float64')
payload.setHeadingRad(np.arctan2(tang_y,tang_x))

x = []
y = []
z = []

payload.turningRadius = 0
w_idx = 0 #index of the current waypoint

pos = ax.add_subplot(211, projection='3d')
plt.plot(goal_x, goal_y,0, 'y*',markersize=10)


current_waypoint = waypoints[w_idx][0].to_dict()


start = rust_funcs.new_point(payload.pos[0], payload.pos[1],
                         np.real(payload.heading * 5),np.imag(payload.heading * 5),
                         payload.pos[2])
plt.plot(current_waypoint["coords"][0], current_waypoint["coords"][1],current_waypoint["gas"]/glide_ratio, 'ro',markersize=10)
        #plot tangent vector
plt.plot([current_waypoint["coords"][0],current_waypoint["coords"][0]+np.real(payload.heading)*5],
         [current_waypoint["coords"][1],current_waypoint["coords"][1]+np.imag(payload.heading)*5],
         [current_waypoint["gas"]/glide_ratio,current_waypoint["gas"]/glide_ratio], color='orange',markersize=10)
        
desired_radius, desired_arclen, _, center = rust_funcs.circle_from(start, waypoints[w_idx][0])


while payload.pos[2] > 0:
    #create a new PyPoint out of the current position
    current_pos = rust_funcs.new_point(payload.pos[0], payload.pos[1],
                         np.real(payload.heading),np.imag(payload.heading),
                         payload.pos[2])
    
    threshold = 0.5
    close_enough = abs(payload.pos[0] - current_waypoint["coords"][0]) < threshold and...
    abs(payload.pos[1] - current_waypoint["coords"][1]) < threshold
    
    
    if (payload.pos[2] < waypoints[w_idx][1]) and w_idx < len(waypoints)-1:
        plt.plot(current_waypoint["coords"][0], current_waypoint["coords"][1],current_waypoint["gas"]/glide_ratio, 'ro',markersize=10)
        tang_norm = np.array(current_waypoint["tang"])/np.linalg.norm(current_waypoint["tang"])
        #plot tangent vector
        plt.plot([current_waypoint["coords"][0],current_waypoint["coords"][0]+tang_norm[0]],
                 [current_waypoint["coords"][1],current_waypoint["coords"][1]+tang_norm[1]],
                 [current_waypoint["gas"]/glide_ratio,current_waypoint["gas"]/glide_ratio], color='orange',markersize=10)
        #print("current y diff:",waypoints[w_idx][1],payload.pos[2])
        #plot current location
        plt.plot(payload.pos[0], payload.pos[1],payload.pos[2], 'k*',markersize=10)
        
        w_idx += 1
        prev_waypoint = current_waypoint

        current_waypoint = waypoints[w_idx][0].to_dict()
        
        desired_radius, desired_arclen, _, center = rust_funcs.circle_from(waypoints[w_idx-1][0], waypoints[w_idx][0])
        # Generate the points along the arc
        num_points = 100  # Number of points to generate along the arc
        p1 = np.array(prev_waypoint["coords"])-np.array(center)
        p2 = np.array(current_waypoint["coords"])-np.array(center)
        ang = 0
        try:
            ang = (desired_arclen)/desired_radius
        except:
            raise Exception(w_idx,len(waypoints))
            
        t = np.linspace(0, ang, num_points)
        #print("arclen",desired_arclen)
        #rotation matrix for the arc
        rot = np.array([[np.cos(t), -np.sin(t)],[np.sin(t), np.cos(t)]])
        rots = np.array([rot[:,:,i].dot(p1) for i in range(num_points)])
        
        
        
        
        des_x = center[0] + rots[:,0] # x-coordinates of the arc points
        des_y = center[1] + rots[:,1]  # y-coordinates of the arc points
        des_z = np.linspace(prev_waypoint["gas"]/glide_ratio, current_waypoint["gas"]/glide_ratio, num_points)  # z-coordinates of the arc points

        # Plot the desired path in green
        pos.plot(des_x,des_y,des_z, color='orange')
               
        desired_radius, desired_arclen, _, center = rust_funcs.circle_from(waypoints[w_idx-1][0], waypoints[w_idx][0])

    #plt.show()
    # use circle_from to find new turning radius:
    radius, arclen, newhead, center = rust_funcs.circle_from(current_pos, waypoints[w_idx][0])
    Kp = 0.2
    radius_ratio = 1 if desired_radius == 0 else radius / desired_radius #positive if too large, negative if too small
    arc_ratio = 1 if arclen == 0 else np.exp(-desired_arclen/arclen)
    """"""
    #arclen_ratio = 1 if desired_arclen == 0 else arclen / desired_arclen #positive if too large, negative if too small
    assigned_r = 0
    gas_left = payload.pos[2] - waypoints[w_idx][1]
    if gas_left > arclen: # too much gas, turn tighter
        assigned_r = radius * (1 - Kp) 
    elif gas_left < arclen:
        assigned_r = radius * (1 + Kp)
    else:
        assigned_r = radius
    payload.turningRadius = assigned_r * radius_ratio * arc_ratio + desired_radius * (1 - arc_ratio)
    
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
    payload.turningRadius = radius * (1 + turn) * (arc_ratio) #+ desired_radius * (1 - arc_ratio)
    """
    
    
    x.append(payload.pos[0])
    y.append(payload.pos[1])
    z.append(payload.pos[2])
    
    payload.update()
    
plt.plot(goal_x, goal_y,0, 'y*',markersize=10)
pos.plot(x, y, z, label='parametric curve')

flat = ax.add_subplot(212)
flat.plot(start_x, start_y, 'ko',markersize=10)
flat.plot([start_x,start_x+tang_x*5], [start_y,start_y+tang_y*5], color='blue',linewidth=2)
flat.plot(goal_x, goal_y, 'ys',markersize=10)
flat.plot(x,y,color='blue',linewidth=1)
#points.append(rust_funcs.new_point(goal_x, goal_y, 0, 0, 0))
print("num points:", len(points))

for i in range(len(points)-1):
    radius, arclen, newhead, center = rust_funcs.circle_from(points[i], points[i+1])
    current = points[i].to_dict()
    currentX = current["coords"][0]
    currentY = current["coords"][1]
    next = points[i + 1].to_dict()
    nextX = next["coords"][0]
    nextY = next["coords"][1]
    flat.plot((nextX,currentX),(nextY,currentY),color='green',linewidth=1)
    flat.plot(currentX, currentY, 'ro', markersize=3)

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
        
    flat.plot(des_x, des_y, color='orange', linewidth=2)
    #unit_head = np.array(newhead) / np.linalg.norm(np.array(newhead))
    #newHead_end = np.array([currentX, currentY]) + unit_head *3
    #plt.plot((currentX, newHead_end[0]), (currentY, newHead_end[1]), color='blue', linewidth=1)
    
    if printMe:
        print('Path stats:')
        print('Length of final path: ', len(points))
        print('X and Y of closest node: ', current["coords"], current["coords"])
        printMe = False

plt.show()