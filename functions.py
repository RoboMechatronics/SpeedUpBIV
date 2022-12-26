from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QFileDialog
from math import *
import os
import numpy as np

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

def CAL_MIN_PITCH(X, Y):
    # Check X array and Y array, return -1 if they has only 1 number
    if (X) == 1 or len(Y) == 1: 
        return -1

    # Convert X and Y list to array type
    X_arr, Y_arr = np.array(X), np.array(Y)
    X_sort, Y_sort = [],[]

    index = np.lexsort((Y_arr, X_arr))

    X_sort = [X[i] for i in index]
    Y_sort = [Y[i] for i in index]
    X_sort = np.array(X_sort)
    Y_sort = np.array(Y_sort)

    P = np.stack((X_sort, Y_sort), axis=1)

    N = P.shape[0]
    print(N)
    dist_list = []
    dist_ = 0

    for i in range(N):    
        if i == 0:              dist_ = dist(P[i], P[i+1]) 
        if (i > 0 and i < N-1): dist_ = min(dist(P[i], P[i+1]), dist(P[i-1], P[i]))
        if i == N-1:            dist_ = dist(P[i-1], P[i])

        x_max = P[i][0] + dist_
        x_min = P[i][0] + dist_
        y_max = P[i][1] + dist_
        y_min = P[i][1] - dist_

        distance_list = []
        distance = 0
        for j in range(N):
            if P[j][0] >= x_min and P[j][0] <= x_max and P[j][1] >= y_min and P[j][1] <= y_max and j != i:
                distance = dist(P[i], P[j])
                distance_list.append(distance)
                print('j=',j)
        
        dist_list.append(min(distance_list))
    print(P)
    return min(dist_list)
    # return d1_arr.min()
#  End of CAL_MIN_PITCH function

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
        print("Not numeric")
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