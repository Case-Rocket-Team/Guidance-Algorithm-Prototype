import time
import numpy as np
import matplotlib.pyplot as plt


import rust_funcs
from parafoil_sim import State

DRAW_STUFF = False
PRINT = False

start_x, start_y = 10, 30
goal_x, goal_y = 450, 450
tang_x, tang_y = 1, 3
gas = 2000
glide_ratio = 6.5
points = []

threshold = 10

start_coords = start_x, start_y

goal_coords = goal_x, goal_y

if DRAW_STUFF:
    plt.figure(figsize=(20, 14))

    plt.plot(start_x, start_y, 'ko',markersize=10)
    plt.plot(goal_x, goal_y, 'ys',markersize=10)

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


payload = State(max_wind=0.01)
payload.pos = np.array((start_x,start_y,gas/glide_ratio),dtype='float64')
payload.vel = np.array((0,0,0),dtype='float64')
payload.setHeadingRad(-np.arctan2(tang_y,tang_x))

x = []
y = []
z = []

payload.turningRadius = 0
w_idx = 0 #index of the current waypoint
pos = plt.figure().add_subplot(projection='3d')
plt.plot(goal_x, goal_y,0, 'y*',markersize=10)
current_waypoint = waypoints[w_idx][0].to_dict()



while payload.pos[2] > 0:
    #create a new PyPoint out of the current position
    current_pos = rust_funcs.new_point(payload.pos[0], payload.pos[1],
                         np.real(payload.heading),np.imag(payload.heading),
                         payload.pos[2])
    
    
    close_enough = abs(payload.pos[0] - current_waypoint["coords"][0]) < threshold and...
    abs(payload.pos[1] - current_waypoint["coords"][1]) < threshold and ...
    payload.pos[2] - waypoints[w_idx][1] < threshold
    
    
    if payload.pos[2] < waypoints[w_idx][1]:
        plt.plot(current_waypoint["coords"][0], current_waypoint["coords"][1],current_waypoint["gas"]/glide_ratio, 'ro',markersize=10)
        #plot tangent vector
        plt.plot([current_waypoint["coords"][0],current_waypoint["coords"][0]+current_waypoint["tang"][0] *50],
                 [current_waypoint["coords"][1],current_waypoint["coords"][1]+current_waypoint["tang"][1]*50],
                 [current_waypoint["gas"]/glide_ratio,current_waypoint["gas"]/glide_ratio], color='orange',markersize=10)
        print("current y diff:",waypoints[w_idx][1],payload.pos[2])
        
        
        w_idx += 1
        current_waypoint = waypoints[w_idx][0].to_dict()

        
    # use circle_from to find new turning radius:
    radius, arclen, newhead, center = rust_funcs.circle_from(current_pos, waypoints[w_idx][0])
    payload.turningRadius = radius
    
    x.append(payload.pos[0])
    y.append(payload.pos[1])
    z.append(payload.pos[2])
    
    payload.update()
    
pos.plot(x, y, z, label='parametric curve')
plt.show()



"""
plt.ion()
for i in range(len(points)-1, 0, -1):
    print(i)
    #plt.clf()
    radius, arclen, newhead, center = rust_funcs.circle_from(points[i-1], points[i])
    current = points[i].to_dict()
    currentX = current["coords"][0]
    currentY = current["coords"][1]
    parent = points[i - 1].to_dict()
    parentX = parent["coords"][0]
    parentY = parent["coords"][1]
    print("({},{}) -> ({},{})".format(currentX, currentY, parentX, parentY))
    #print(center)
    #plt.plot(center[0], center[1], 'bo', markersize=3)
    rel_p2 = np.array([currentX, currentY]) - np.array(center)
    rel_p1 = np.array([parentX, parentY]) - np.array(center)
    angle_ben = np.arctan2(np.linalg.det([rel_p1, rel_p2]), np.dot(rel_p1, rel_p2))
    angle_will = np.arcsin(np.linalg.det([rel_p1, rel_p2]) / np.linalg.norm(rel_p1) / np.linalg.norm(rel_p2))
    angle = angle_will
    x = []
    y = []
    
    segs = 100
    theta = (angle - 2*np.pi * np.sign(angle) * np.sign(radius)) % (2*np.pi)
    print(angle,theta)
    
    rot_mat = np.array([[np.cos(theta/segs), -np.sin(theta/segs)],
                        [np.sin(theta/segs), np.cos(theta/segs)]])
    
    rad = rel_p1
    for i in range(segs):
        rad = rot_mat.dot(rad)
        x_p,y_p = center + rad
        x.append(x_p)
        y.append(y_p)
        
    plt.plot((parentX,currentX),(parentY,currentY),color='green',linewidth=1)
    plt.plot(x, y, color='orange', linewidth=2)
    plt.plot(currentX, currentY, 'ro', markersize=3)
    #unit_head = np.array(newhead) / np.linalg.norm(np.array(newhead))
    #newHead_end = np.array([currentX, currentY]) + unit_head *3
    #plt.plot((currentX, newHead_end[0]), (currentY, newHead_end[1]), color='blue', linewidth=1)

    
    if printMe:
        print('Path stats:')
        print('Length of final path: ', len(points))
        print('X and Y of closest node: ', current["coords"], current["coords"])
        printMe = False

    plt.draw()
    plt.pause(0.0001)
plt.pause(1000)
plt.ioff()
"""
