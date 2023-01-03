from math import *
import numpy as np

X_list = [1,2,3,4,5,6,7]
Y_list = [1,2,3,4,5,6,7]

def CAL_MIN_PITCH(X, Y):
    # Check X array and Y array, return -1 if they has only 1 number
    if (X) == 1 or len(Y) == 1: 
        return -1

    # Convert X and Y list to array type
    X_arr, Y_arr = np.array(X), np.array(Y)

    P = np.stack((X_arr, Y_arr), axis=1)
    print("P=\n", P)
    N = P.shape[0]

    groups = 3
    n = N//groups
    n_rest = N%3

    print("groups = ", groups)
    print("n = ", n)
    print("n_rest = ", n_rest)

    groups_list = []
    for g in range(groups):
        sub_list1 = []
        for i in range(n):
            print("i = ", i, "   P[", g*n + i, "][:] = ", P[g*n+i][:])
            sub_list1.append(P[g*n+i][:])
        groups_list.append(sub_list1)
    
    if n_rest > 0:
        sub_list1 = []
        for i in range(n_rest):
            print("i = ", i, "   P[", groups*n + i, "][:] = ", P[groups*n+i][:])
            sub_list1.append(P[groups*n+i][:])
        groups_list.append(sub_list1)
    
    print(groups_list)
    print(len(groups_list))
    
    return 0

CAL_MIN_PITCH(X_list, Y_list)