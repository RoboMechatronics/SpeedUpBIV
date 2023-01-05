from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QFileDialog
from math import *
import os
import numpy as np
import pandas as pd
import time
from scipy.spatial.distance import euclidean

def GET_XY_FROM_MOUSE(Table):
    # Get cells value has been selected
    selected = Table.selectedIndexes()
    # Intial empty lists
    X, Y, selected_list_index = [],[], []

    # Check selected items are empty or not
    if len(selected) != 0: selected_list_index = [([ix.column(), ix.row()]) for ix in selected] # if not
    else: 
        return [], [], [], 0 #Return X, Y, status if yes
        
    X_index, Y_index = [], []

    X_index = [(selected_list_index[i][0]) for i in range(0, len(selected_list_index))]
    Y_index = [(selected_list_index[i][1]) for i in range(0, len(selected_list_index))]
    
    X_index = list(set(X_index)) # Column index
    Y_index = list(set(Y_index)) # Row index
    row_start_index, row_end_index = Y_index[0], Y_index[len(Y_index)-1]

    if (len(X_index) <= 1) or (len(Y_index) < 1): 
        return X, Y, [], 0 #Return X, Y, (row start, row end index) and status
       
    X_coordinates, Y_coordinates = [], []
    X_coordinates = [([Y_index[i], X_index[0]]) for i in range(0,len(Y_index))]
    Y_coordinates = [([Y_index[i], X_index[1]]) for i in range(0,len(Y_index))]
    
    try:
        X = [(float(Table.item(x[0],x[1]).text().replace(",",""))) for x in X_coordinates]
        Y = [(float(Table.item(y[0],y[1]).text().replace(",",""))) for y in Y_coordinates]
    except (ValueError, AttributeError):
        return [], [], [-1, -1], 0 # X, Y, (row start, row end index) and status

    return X, Y, [row_start_index, row_end_index], 1 # X, Y, (row start, end index), status
# End of GET_XY_FROM_MOUSE function #

def SCATTER_CHART(X_list, Y_list, chart, NC_list, NC_split_char, Pad_name=[], Pad_number=[]):
    # Add chart in tab1
    chart.axes.axhline(y=0, color='#FFFFFF', linestyle='-.', linewidth=0.5)
    chart.axes.axvline(x=0, color='#FFFFFF', linestyle='-.', linewidth=0.5)
    
    NC_pos = []
    Probe_pos = []
    First_pad_name = ""

    if len(Pad_name) > 0 and len(Pad_number) > 0: 
        if Pad_name[0] != "" and Pad_number[0] != 0: 
            First_pad_name = "Pad#" + Pad_number[0] + "; " + Pad_name[0]
    if len(Pad_name) > 0 and len(Pad_number) == 0: 
        if Pad_name[0] != "":
            First_pad_name = Pad_name[0]
    if len(Pad_name) == 0 and len(Pad_number) > 0: 
        if Pad_number[0] != 0: 
            First_pad_name = "Pad#" + Pad_number[0]

    if len(X_list) > 0:
        if len(NC_list) > 0 and NC_split_char != "":
            NC_pos = [i for i in range(len(NC_list)) if NC_list[i] == NC_split_char]
            Probe_pos = [i for i in range(len(NC_list)) if NC_list[i] != NC_split_char]

            X_list_NC, Y_list_NC, Annotate_NC = [], [], []
            
            X_list_NC = [X_list[i] for i in NC_pos]
            Y_list_NC = [Y_list[i] for i in NC_pos]
        
            X_list_probe, Y_list_probe =[], []
            
            [X_list_probe.append(X_list[i]) for i in Probe_pos]
            [Y_list_probe.append(Y_list[i]) for i in Probe_pos]

            chart.axes.scatter(X_list_NC, Y_list_NC, color = "white", marker="s", s=10, label="NC")
            chart.axes.scatter(X_list_probe, Y_list_probe, color = "orange", marker="o", s=10, label="Probe")

            if len(Pad_name) > 0 and len(Pad_number) > 0: 
                if Pad_name[Probe_pos[0]] != "" and Pad_number[Probe_pos[0]] != "":
                    First_pad_name = "Pad#" + Pad_number[Probe_pos[0]] + "; " + Pad_name[Probe_pos[0]]
            if len(Pad_name) > 0 and len(Pad_number) == 0: 
                if Pad_name[Probe_pos[0]] != "":
                    First_pad_name = Pad_name[Probe_pos[0]]
            if len(Pad_name) == 0 and len(Pad_number) > 0: 
                if Pad_number[Probe_pos[0]] != "":
                    First_pad_name = "Pad#" + Pad_number[Probe_pos[0]]
            if First_pad_name != "":
                chart.axes.annotate(First_pad_name, 
                                    xy=(X_list_probe[0],Y_list_probe[0]), 
                                    color="orange")
        else:
            chart.axes.scatter(X_list, Y_list, color = "orange", marker="o", s=3, label="Probe")
            if First_pad_name != "":
                chart.axes.annotate(First_pad_name, 
                                    xy = (X_list[0], Y_list[0]), 
                                    color = "white")

        chart.axes.axis('equal')
        chart.axes.set_xlim([min(X_list)-5, max(X_list)+5]) 
        chart.axes.set_ylim([min(Y_list)-5, max(Y_list)+5])
        chart.axes.legend(facecolor="grey", labelcolor="w", frameon=True)

    chart.axes.set_xlabel('X-axis')
    chart.axes.set_ylabel('Y-axis')

    chart.axes.xaxis.label.set_color('#FFFFFF')
    chart.axes.tick_params(axis='x', colors='#FFFFFF')
    chart.axes.yaxis.label.set_color('#FFFFFF')
    chart.axes.tick_params(axis='y', colors='#FFFFFF')

    chart.axes.spines['bottom'].set_color('#FFFFFF')
    chart.axes.spines['top'].set_color(None)   
    chart.axes.spines['left'].set_color('#FFFFFF')
    chart.axes.spines['right'].set_color(None)  

    chart.axes.patch.set_facecolor('None')
    chart.axes.patch.set_alpha(0.0)

    chart.setStyleSheet("background-color:transparent;")
    
    # Add toolbar chart
    toolbar = NavigationToolbar(chart)
    toolbar.setStyleSheet("background-color: rgb(255,255,255);"
                        "border-radius: 8px;"
                        "color: black;"
                        )
    
    return chart, toolbar
# End of SCATTER_CHART function #

def CAL_DIE_SIZE(X, Y):
    # return Size in X and Size in Y
    return (max(X) - min(X)), (max(Y)-min(Y))
# End of CAL_DIE_SIZE function #
"""
def CAL_MIN_PITCH(X, Y):
    start_time = time.time()
    # Check X array and Y array, return -1 if they has only 1 number
    if (X) == 1 or len(Y) == 1: 
        return -1
    
    # Convert X and Y list to array type
    X_arr, Y_arr = np.array(X), np.array(Y)

    P = np.stack((X_arr, Y_arr), axis=1)
    N = P.shape[0]

    groups = 1
    if N > 2000 and N <= 5000:
        groups = 3
    if N > 5000 and N <= 20000:
        groups = 10
    if N > 20000:
        groups = 50

    n = N//groups
    n_rest = N%groups

    groups_list = []
    for g in range(groups):
        sub_list1 = []
        sub_list1 = [P[g*n+i][:] for i in range(n)]
        groups_list.append(sub_list1)
    
    if n_rest > 0:
        sub_list = []
        sub_list = [P[groups*n+i][:] for i in range(n_rest)]
        groups_list.append(sub_list)
    
    min_distance1 = 0
    min_distance2 = 0
    min_distance2_list = []

    for P in groups_list:
        N_in_group = len(P)
        min_distance1_list = []
        for i in range(N_in_group-1):
            list1 = []
            for j in range(i+1, N_in_group):
                a       = (P[i][0] - P[j][0])**2
                b       = (P[i][1] - P[j][1])**2
                sum_    = a+b
                min_distance1 = sqrt(sum_)
                list1.append(min_distance1)

            min_distance1 = min(list1)
            min_distance1_list.append(min_distance1)
                
        min_distance2 = min(min_distance1_list)
        min_distance2_list.append(min_distance2)   # min distance of every groups
    
    n_i = len(groups_list)
    for i in range(n_i-1):
        for j in range(i+1, n_i):
            min_distance2_list = [[euclidean(groups_list[i][k], groups_list[j][m]) for m in range(len(groups_list[j]))] for k in range(len(groups_list[i]))]
    
    end_time = time.time() - start_time
    print("duration: ", round(end_time*1000, 3), "ms")
    return min(min_distance2_list)
"""
#  End of CAL_MIN_PITCH functions
def CAL_MIN_PITCH(X, Y):
    start_time = time.time()
    #------------------------------------------------------------------#
    # Check X array and Y array, return -1 if they has only 1 number
    if len(X) == 1 or len(Y) == 1: 
        return -1
    
    index = [i for i in range(len(X))]
    P = [(X[i], Y[i]) for i in range(len(X))]
    P = np.array(P)
    N = P.shape[0]

    # Convert X and Y list to array type
    index1 = np.lexsort((Y, X))
    index2 = np.lexsort((X, Y))
    min_distance_list = []
    for i in range(N):
        # i = 2
        Pi_index1_pos = np.where(index1==i)[0][0]
        Pi_index2_pos = np.where(index2==i)[0][0]

        near_Pi = []
        # these pointns near P0:
        if Pi_index1_pos == 0:
            near_Pi.append(index1[Pi_index1_pos+1])
            near_Pi.append(index1[Pi_index1_pos+2])
        elif Pi_index1_pos == len(index1)-1:
            near_Pi.append(index1[Pi_index1_pos-1])
            near_Pi.append(index1[Pi_index1_pos-2])
        else:
            near_Pi.append(index1[Pi_index1_pos-1])
            near_Pi.append(index1[Pi_index1_pos+1])
            
        if Pi_index2_pos == 0:
            near_Pi.append(index2[Pi_index2_pos+1])
            near_Pi.append(index2[Pi_index2_pos+2])
        elif Pi_index2_pos == len(index2)-1:
            near_Pi.append(index2[Pi_index2_pos-1])
            near_Pi.append(index2[Pi_index2_pos-2])
        else:
            near_Pi.append(index2[Pi_index2_pos-1])
            near_Pi.append(index2[Pi_index2_pos+1])
            
        near_Pi = list(dict.fromkeys(near_Pi))
        near_Pi.sort()
        
        distance_list = []
        for j in near_Pi:
            distance = dist(P[i], P[j])
            distance_list.append(distance)

        min_distance_list.append(min(distance_list))
    
    #------------------------------------------------------------------#
    end_time = time.time() - start_time # unit: seconds
    return min(min_distance_list), round(end_time*1000, 2) # converted to miliseconds

def GET_FILE(): # No input
    filter_ = "Excel File (*.xlsx *xlsm)"
    file_path = QFileDialog.getOpenFileName(caption='selectFile',
                                            directory="",
                                            filter=filter_,
                                            initialFilter="")
    file_name = file_path[0].split('/')[-1]
    # return:
    # file_path, file_name and file_extension
    return file_path[0], file_name, os.path.splitext(file_name)[1]
# End of GET_FILE function

def GET_SPEC_FILE(): # No input
    filter_ = "Txt File (*.txt)"
    file_path = QFileDialog.getOpenFileName(caption='selectFile',
                                            directory="",
                                            filter=filter_,
                                            initialFilter="")
    file_name = file_path[0].split('/')[-1]

    return file_path[0], file_name, os.path.splitext(file_name)[1]
# End of GET_FILE function

def DIE_PATTERN(X, Y, config_table, Stepping_distance):
    new_X = []
    new_Y = []
    config_array = np.array([])
    return new_X, new_Y

def UPDATE_PARAMETER_FOR_EXISTED_PROJECT(card_part_number):
    spec_file_name = card_part_number + "_spec_file.txt"
    return spec_file_name

def EXPORT_XY_INPUT_FORMAT_FOR_IUA_PLUS_FILE(card_part_number):
    # input:
    # card_part_number as PCX-000000, MSP-000000
    file_name = "YYY-XXXXXX_XY input format for IUA_plus_Rev00.xlsx"
    template_location = "templates/"
    
    numeric_revision = "" # from 00 to 99
    letter_revision = "" # from A to Z and AA to ZZ
    sheet_name = "Sheet1"

    new_file_name = file_name.replace("YYY-XXXXXX", card_part_number)
    new_location = "result/"

    # Create new file
    try:
        shutil.copyfile(template_location+filename, new_location + file_name)
    except:
        return
    # start to update revision
    p = 0
    list_ = []
    list_ = [i for i in numeric_revision]
    list_.reverse()
    if numeric_revision.isnumeric():
        for i, element in enumerate(list_):
            if ord(element) >= 48 and ord(element) < 57 and p == 0:
                list_[i] = chr(ord(element)+1)
                p = 1
                break
            else:
                list_[i] = "0"
    else:
        # print("Not numeric")
        return

    list_.reverse()
    numeric_revision = ""
    numeric_revision = [numeric_revision + i for i in list_]
    # End to update revision

    workbook = openpyxl.load_workbook(location+file_name)
    sheet = workbook[sheet_name] # active "Sheet1"
    return

def EXPORT_PCB_PAD_LOCATION_FILE():
    return

def EXPORT_ARRAY_FULL_SITE_FOR_REFERENCE_FILE():
    return

def EXPORT_IUA_PLUS_FILE():
    return

def EXPORT_CRD_PLUS_FILE():
    return

def EXPORT_PROBE_HEAD_XY_COORDINATES_FOR_APPROVAL_FILE():
    return
