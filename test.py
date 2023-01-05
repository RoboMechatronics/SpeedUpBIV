from math import *
import numpy as np
import time
import matplotlib.pyplot as plt

X_list = [-1,   -7,     5,      2,      -4.5,    0.5]
Y_list = [-1,   -5,     1,      0.5,     3.5,    -5]


def CAL_MIN_PITCH(X, Y):
    start_time = time.time()
    #------------------------------------------------------------------#
    # Check X array and Y array, return -1 if they has only 1 number
    if len(X) == 1 or len(Y) == 1: 
        return -1
    label = []
    label = [("P" + str(i)) for i in range(len(X))]
    # print(label)
    index = [i for i in range(len(X))]
    # print(index)
    P = [(X[i], Y[i]) for i in range(len(X))]
    P = np.array(P)
    N = P.shape[0]
    # """
    plt.subplot(1, 3, 1)
    plt.scatter(X, Y, color = "red")
    
    [plt.annotate(txt, (X_list[i], Y_list[i])) for i, txt in enumerate(label)]
    plt.title("Original")
    # """
    # Convert X and Y list to array type
    index1 = np.lexsort((Y, X))
    print("index 1 = ", index1)
    P1 = [(X[i],Y[i]) for i in index1]
    P1 = np.array(P1)
    X1 = [X[i] for i in index1]
    Y1 = [Y[i] for i in index1]
    # """
    plt.subplot(1, 3, 2)
    plt.scatter(X1, Y1, color='blue')
    [plt.annotate(txt, (P1[i])) for i, txt in enumerate(label)]
    plt.title("Sort Y by X")
    # """
    # Convert X and Y list to array type
    index2 = np.lexsort((X, Y))
    print("index 2 = ", index2)
    P2 = [(X[i],Y[i]) for i in index2]
    P2 = np.array(P2)
    X2 = [X[i] for i in index2]
    Y2 = [Y[i] for i in index2]
    # """
    plt.subplot(1, 3, 3)
    plt.scatter(X2, Y2, color='green')
    [plt.annotate(txt, (P2[i])) for i, txt in enumerate(label)]
    plt.title("Sort X by Y")
    # """
    print("P=\n", P)
    print("P1=\n", P1)
    print("P2=\n", P2)
    min_distance_list = []
    # P0 position in index1 and index
    for i in range(N):
        # i = 2
        Pi_index1_pos = np.where(index1==i)[0][0]
        Pi_index2_pos = np.where(index2==i)[0][0]

        print("Pi_index1_pos=", Pi_index1_pos)
        print("Pi_index2_pos=", Pi_index2_pos)

        near_Pi = []
        if Pi_index1_pos == 0:  
            near_Pi.append(index1[Pi_index1_pos+1])

        elif Pi_index1_pos == (N-1):  
            near_Pi.append(index1[Pi_index1_pos-1])

        elif Pi_index1_pos > 0 and Pi_index1_pos < (N-1):
            near_Pi.append(index1[Pi_index1_pos+1])
            near_Pi.append(index1[Pi_index1_pos-1])

        if Pi_index2_pos == 0:  
            near_Pi.append(index2[Pi_index2_pos+1])

        elif Pi_index2_pos == (N-1):  
            near_Pi.append(index2[Pi_index2_pos-1])

        elif Pi_index2_pos > 0 and Pi_index2_pos < (N-1):
            near_Pi.append(index2[Pi_index2_pos+1])
            near_Pi.append(index2[Pi_index2_pos-1])
        
        near_Pi = list(dict.fromkeys(near_Pi))

        d_list = []
        for j in near_Pi:
            d_list.append(dist(P[i], P[j]))
        
        d = min(d_list)
        minX = P[i][0] - d
        maxX = P[i][0] + d
        minY = P[i][1] - d
        maxY = P[i][1] + d
        print("minX = ", minX)
        print("maxX = ", maxX)
        print("minY = ", minY)
        print("maxY = ", maxY)
   
        near_Pi = []
        for k in range(N):
            if k == i:
                continue
            elif P[k][0] >= minX and P[k][0] <= maxX and P[k][1] >= minY and P[k][1] <= maxY:
                near_Pi.append(k)
        
        near_Pi = list(dict.fromkeys(near_Pi))
        
        d_list = []
        for j in near_Pi:
            d_list.append(dist(P[i], P[j]))
        
        print("near_P[",i,"]= P",near_Pi)

    #------------------------------------------------------------------#
    end_time = time.time() - start_time
    print("duration: ", round(end_time*1000, 2), "ms")
    
    plt.show()
    return 0

CAL_MIN_PITCH(X_list, Y_list)

