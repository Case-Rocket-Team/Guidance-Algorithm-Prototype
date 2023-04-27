import time
import numpy as np
import matplotlib.pyplot as plt
import rust_funcs

DRAW_STUFF = True
PRINT = False

start_x, start_y = 10, 40
goal_x, goal_y = 450, 450
tang_x, tang_y = 1, 3
gas = 1500
points = []

start_coords = start_x, start_y

goal_coords = goal_x, goal_y

if DRAW_STUFF:
    plt.figure(figsize=(20, 14))

    plt.plot(start_x, start_y, 'ko',markersize=10)
    plt.plot(goal_x, goal_y, 'ys',markersize=10)

printMe = False

##----##
reet = rust_funcs.rrt(start_x, start_y, tang_x, tang_y, goal_x, goal_y, gas, min_turn=13,max_curve=100)
for x in reet:
    points.append(x)
##----##

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
    angle = angle_ben
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

plt.pause(100)