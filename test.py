from math import *
import numpy as np
import time
import matplotlib.pyplot as plt

X_list = [-1,   -7,     5,      2,      -4.5,    0.5]
Y_list = [-1,   -5,     1,      0.5,     3.5,    -5]

label = []
for i in range(len(X_list)):
    label.append("P" + str(i))
    
print(label)
    
def CAL_MIN_PITCH(X, Y):
    start_time = time.time()
    #------------------------------------------------------------------#
    # Check X array and Y array, return -1 if they has only 1 number
    if len(X) == 1 or len(Y) == 1: 
        return -1
    
    P = [(X[i], Y[i]) for i in range(len(X))]
    P = np.array(P)
    
    plt.subplot(1, 3, 1)
    plt.scatter(X, Y, color = "red")
    for i, txt in enumerate(label):
        plt.annotate(txt, (X_list[i], Y_list[i]))
    plt.title("Original")

    # Convert X and Y list to array type
    index = np.lexsort((Y, X))
    print("index 1 = ", index)
    
    P1 = [(X[i],Y[i]) for i in index]
    P1 = np.array(P1)
    
    X1 = [X[i] for i in index]
    Y1 = [Y[i] for i in index]
    
    plt.subplot(1, 3, 2)
    plt.scatter(X1, Y1, color='blue')
    for i, txt in enumerate(label):
        plt.annotate(txt, (P1[i]))
    plt.title("Sort Y by X")
    
    # Convert X and Y list to array type
    index = np.lexsort((X, Y))
    print("index 2 = ", index)
    
    P2 = [(X[i],Y[i]) for i in index]
    P2 = np.array(P2)
    
    X2 = [X[i] for i in index]
    Y2 = [Y[i] for i in index]
    plt.subplot(1, 3, 3)
    plt.scatter(X2, Y2, color='green')
    for i, txt in enumerate(label):
        plt.annotate(txt, (P2[i]))
    plt.title("Sort X by Y")
    
    print("P=\n", P)
    print("P1=\n", P1)
    print("P2=\n", P2)
    
    #------------------------------------------------------------------#
    end_time = time.time() - start_time
    print("duration: ", round(end_time*1000, 2), "ms")
    
    plt.show()
    return 0

CAL_MIN_PITCH(X_list, Y_list)

