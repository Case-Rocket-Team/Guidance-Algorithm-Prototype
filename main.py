import time
from matplotlib.collections import LineCollection
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from mpl_toolkits.mplot3d import Axes3D

import rust_funcs
from parafoil_sim import State

DRAW_STUFF = False
PRINT = False


def assign_default_values(params):
    defaults = {
        'K1': 10**-6.879246683841699,
        'K2': 10**4.359176252927491,
        'Kp': 10**-6.142565465487603,
        'Ki': 10**-5.654462105276744,
        'Kd': 10**-0.5169318449780845,
        'error_limit': 10**7.4021520473769735,
        'integral_limit': 10**-9.303342958541146
    }
    
    for key in defaults:
        if key not in params:
            params[key] = defaults[key]
    
    return params

def Main(plot=False, start = [10,30],goal=[450,450],tang=[1,3],gas=600, max_wind=0, input_params = {}):
    start_x, start_y = start
    goal_x, goal_y = goal
    tang_x, tang_y = tang
    glide_ratio = 6.5
    gas = gas*glide_ratio
    points = []
    MIN_TURN = 13
    params = assign_default_values(input_params)
    

    #start_coords = start_x, start_y

    #goal_coords = goal_x, goal_y

    printMe = False

    ##----##
    num_tries = 0
    while True:
        try:
            reet = rust_funcs.rrt(start_x, start_y, tang_x, tang_y, goal_x, goal_y, gas, min_turn=13,max_curve=int(1e4))
            for x in reet:
                points.append(x)
        except:
            print(f"RRT failed going from {start}, {goal}, {tang} with {gas} ft of altitude. running again")
            num_tries += 1
            if num_tries > 1000:
                raise Exception("tried too many times, path is impossible")
        else:
            break
    ##----##

    # separate waypoints by height
    waypoints = []
    for point in points:
        waypoints.append((point,point.to_dict()["gas"]/glide_ratio))
    if plot:
        ax = plt.figure()

    payload = State(max_wind=max_wind)
    payload.pos = np.array((start_x,start_y,gas/glide_ratio),dtype='float64')
    payload.vel = np.array((0,0,0),dtype='float64')
    payload.setHeadingRad(np.arctan2(tang_y,tang_x))

    x = []
    y = []
    z = []
    c = []
    d = []
    g = []
    arcs = []
    rads = []
    des_arcs = []
    des_rads =[]
    payload_rads = []


    integral = 0
    cheat_in_error_previous = 0


    payload.turningRadius = 0
    w_idx = 0 #index of the current waypoint
    if plot:
        pos = ax.add_subplot(222, projection='3d')
        plt.plot(goal_x, goal_y,0, 'y*',markersize=10)


    current_waypoint = waypoints[w_idx][0].to_dict()


    start = rust_funcs.new_point(payload.pos[0], payload.pos[1],
                            np.real(payload.heading)*100,np.imag(payload.heading)*100,
                            payload.pos[2])
    if plot:
        plt.plot(current_waypoint["coords"][0], current_waypoint["coords"][1],current_waypoint["gas"]/glide_ratio, 'ro',markersize=10)
            #plot tangent vector
        plt.plot([current_waypoint["coords"][0],current_waypoint["coords"][0]+np.real(payload.heading)*5],
            [current_waypoint["coords"][1],current_waypoint["coords"][1]+np.imag(payload.heading)*5],
            [current_waypoint["gas"]/glide_ratio,current_waypoint["gas"]/glide_ratio], color='orange',markersize=10)
            
    desired_radius, desired_arclen, _, desired_center = rust_funcs.circle_from(start, waypoints[w_idx][0])


    while payload.pos[2] > 0:
        #create a new PyPoint out of the current position
        current_pos = rust_funcs.new_point(payload.pos[0], payload.pos[1],
                            np.real(payload.heading),np.imag(payload.heading),
                            payload.pos[2])
        
        threshold = 0.5
        close_enough = abs(payload.pos[0] - current_waypoint["coords"][0]) < threshold and...
        abs(payload.pos[1] - current_waypoint["coords"][1]) < threshold
        
        
        if (payload.pos[2] < waypoints[w_idx][1]) and w_idx < len(waypoints)-1:
            if plot:
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
            integral = 0
            cheat_in_error_previous = 0
            
            if plot:
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

        # use circle_from to find new turning radius:
        radius, arclen, newhead, center = rust_funcs.circle_from(current_pos, waypoints[w_idx][0])
        
        # -- Pathfinding -- #
        center_dist = np.linalg.norm(np.array(desired_center) - np.array(payload.pos[0],payload.pos[1])) # absolute distance from the center of the desired
        d_error = (abs(desired_radius) - center_dist) # difference in distance from the desired radius
        error_gas = ((payload.pos[2] - waypoints[w_idx][1])*glide_ratio - arclen) # Whether too much (if positive) or too little (if negative) gas will be left at the end of the turn
        desired_cheat_in = -params['K1'] * error_gas #scaling error gas
        cheat_in_error = (desired_cheat_in - d_error)
        
        
        #PID
        proportional = params['Kp'] * cheat_in_error
        derivative = params['Kd'] * (cheat_in_error - cheat_in_error_previous)
        integral = np.clip(integral + params['Ki'] * (cheat_in_error) * payload.dt, -params['integral_limit'], params['integral_limit'])
        correction = proportional + derivative + integral
        
        
        #error_ratio = abs(d_error/error_gas)
        rad_to_use = desired_radius #(1-np.exp(-error_ratio))*radius + (np.exp(-error_ratio))*desired_radius
        desired_turn = max(MIN_TURN, abs(rad_to_use) - correction)
        
        
        if desired_turn == 0:
            payload.turningRadius = 0
        else:
            payload.turningRadius =  desired_turn * np.sign(rad_to_use)
        cheat_in_error_previous = cheat_in_error
        ## --- End Pathfinding --- ##
        
        x.append(payload.pos[0])
        y.append(payload.pos[1])
        z.append(payload.pos[2])
        rads.append(radius)
        arcs.append(arclen)
        des_rads.append(desired_radius)
        des_arcs.append(desired_arclen)
        payload_rads.append(payload.turningRadius)
        c.append(cheat_in_error)
        d.append(d_error)
        g.append(desired_cheat_in)
        
        payload.update()
    
    if plot:
        plt.plot(goal_x, goal_y,0, 'y*',markersize=10)
        pos.plot(x, y, z, label='parametric curve')
        error_chart = ax.add_subplot(223)
        error_chart.plot(c,color='blue',linewidth=1, label="cheat_in_error")
        error_chart.plot(d,color='red',linewidth=1 ,label="d_error")
        error_chart.plot(g,color='green',linewidth=1, label="error_gas")
        error_chart.legend()


    def moving_average(data, window_size):
        window = np.ones(window_size) / window_size
        smoothed_data = np.convolve(data, window, mode='same')
        return smoothed_data

    if plot:
        value_chart = ax.add_subplot(221,sharex=error_chart)
        value_chart.plot(moving_average(rads,15),color='blue',linewidth=1, label="radius")
        value_chart.plot(arcs,color='red',linewidth=1 ,label="arclen")
        value_chart.plot(des_arcs,color='purple',linewidth=1, label="desired_arclen")
        value_chart.plot(des_rads,color='orange',linewidth=1, label="desired_radius")
        value_chart.plot(payload_rads,color='green',linewidth=1, label="payload_radius")
        value_chart.legend()
        value_chart.set_ylim([-1e4,1e4])




        flat = ax.add_subplot(224)
        flat.plot(start_x, start_y, 'ko',markersize=10)
        flat.plot([start_x,start_x+tang_x*5], [start_y,start_y+tang_y*5], color='blue',linewidth=2)
        flat.plot(goal_x, goal_y, 'ys',markersize=10)
        #flat.plot(x,y,color='blue',linewidth=1)
        #points.append(rust_funcs.new_point(goal_x, goal_y, 0, 0, 0))
    #print("num points:", len(points))
    des_xs = []
    des_ys = []
    for i in range(len(points)-1):
        radius, arclen, newhead, center = rust_funcs.circle_from(points[i], points[i+1])
        current = points[i].to_dict()
        currentX = current["coords"][0]
        currentY = current["coords"][1]
        next = points[i + 1].to_dict()
        nextX = next["coords"][0]
        nextY = next["coords"][1]
        if plot:
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
        des_xs.extend(des_x)
        des_ys.extend(des_y)
        if plot:   
            flat.plot(des_x, des_y, color='orange', linewidth=2)
        #unit_head = np.array(newhead) / np.linalg.norm(np.array(newhead))
        #newHead_end = np.array([currentX, currentY]) + unit_head *3
        #plt.plot((currentX, newHead_end[0]), (currentY, newHead_end[1]), color='blue', linewidth=1)
        
        if printMe:
            print('Path stats:')
            print('Length of final path: ', len(points))
            print('X and Y of closest node: ', current["coords"], current["coords"])
            printMe = False
    
    if plot:
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, cmap='viridis')
        lc.set_array(c)
        lc.set_linewidth(2)
        flat.add_collection(lc)

        plt.show()
    
    return des_xs,des_ys,x,y 
        
if __name__ == "__main__":
    Main(plot=True)