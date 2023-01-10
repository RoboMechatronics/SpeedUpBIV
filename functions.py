from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QFileDialog
from math import *
import os
import numpy as np
import pandas as pd
import time
import shutil
# from scipy.spatial.distance import euclidean

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

#  Start of ClosestPair class
class ClosestPair:
    def __init__(self, X, Y):
        super().__init__()
        self.min_distance = 0
        self.P = [(X[i], Y[i]) for i in range(len(X))]
        
        n = len(self.P)
        Px = sorted(self.P, key=lambda x: x[0])
        Py = sorted(self.P, key=lambda x: x[1])
        
        self.min_distance = self.Calculate(Px, Py, n)
        
    def Calculate(self, Px, Py, n):
        # Simple case
        if n == 2:
            return dist(self.P[0], self.P[1])
        if n == 3:
            return min(dist(self.P[0], self.P[1]), dist(self.P[0], self.P[2]), dist(self.P[1], self.P[2]))
        
        # Divide 
        mid = n // 2
        d_left = self.Calculate(Px, Py[:mid], mid)
        d_right = self.Calculate(Py, Py[mid:], n - mid)
        
        min_distance = min(d_left, d_right)
        
        S = [] # points list in strip
        for p in Px:
            if abs(p[0] - Px[mid][0]) < min_distance:
                S.append(p)
                
        min_distance_in_strip = float('inf')
        for i in range(min(6, len(S) - 1), len(S)):
            for j in range(max(0, i - 6), i):
                current_dis = dist(S[i], S[j])
                if current_dis < min_distance:
                    min_distance_in_strip = current_dis
        
        return min(min_distance, min_distance_in_strip)

    def min_distance_in_points(self):
        return self.min_distance
# End of ClosestPair class

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

def GET_FILE_PATH(path_file, file_need_find):
    path_file_open = open(path_file, 'r')
    content = path_file_open.readlines()
    path_file_open.close()

    file_name, file_extension = "", ""

    for i in content:
        if file_need_find in i:
            file_name = i[len(file_need_find+"="):i.index(".")]
            if "." in i:
                file_extension = i[i.index("."):]
                file_extension = file_extension[1:]
            break
    file_extension = file_extension.replace("\n", "")
    file_name = file_name.replace("\n", "")
    # completed to get file name, file extension from path.txt file
    return file_name, file_extension

def GET_FOLDER_PATH(path_file, folder_name_to_find):
    # Open paths.txt file
    path_file_open = open(path_file, 'r')
    # Read paths.txt file and store file content to content variable
    content = path_file_open.readlines()
    # Close file
    path_file_open.close()
    # Inital variable
    folder_path = ""
    # Find file name string in content file
    for i in content:
        if folder_name_to_find in i:
            folder_path = i[len(folder_name_to_find+"="):]
            break
    folder_path = folder_path.replace('\n', "")
    # completed to get folder path
    return folder_path

def GET_REVISION_STRING(path_file, string_to_find):
    # Open paths.txt file
    path_file_open = open(path_file, 'r')
    # Read paths.txt file and store file content to content variable
    content = path_file_open.readlines()
    # Close file
    path_file_open.close()
    # Inital variable
    revision_string = ""
    # Find file name string in content file
    for i in content:
        if string_to_find in i:
            revision_string = i[len(string_to_find)+len("="):i.index("\n")]
            break
                
    # completed to get folder path
    return revision_string

# Start of REVISION_CHANGE_TYPE function:
# Input:
# - old_revision: old revision
# - type: Edit, Release or Override
def REVISION_CHANGE_TYPE(old_revision, type = "Edit"): 
    # Check old_revision string if it is empty 
    if old_revision == "":
        return "" 
    
    # Keep revision if type is Override
    if type == "Override":
        return old_revision

    # If old_revision string is not empty:
    # Initial variables
    numeric_revision = "" # from 00 to 99, example: 01, 02, 03. Note: 00 is used to initial
    alpha_revision = "" # from A to Z, AA to ZZ, example: A, B, AA, AB
    mix_revision = "" # include A and 00 or AA and 00, example: A01, AB01

    # Check numberic or alpha or mix type:
    if old_revision.isdigit() == True: # revision value is like "01", "02", or "03"
        numeric_revision = old_revision
        alpha_revision = ""
        mix_revision = ""

    elif old_revision.isalpha() == True: # revision value is like "A" or "AA"
        alpha_revision = old_revision
        numeric_revision = ""
        mix_revision = ""

    else: # Revision value is like "A01" or "AA01"
        mix_revision = old_revision
        alpha_revision = ""
        numeric_revision = ""

    s = [] # Convert revision string into list, like s = ['0','1'] or ['A']
    if numeric_revision != "":
        s = [i for i in numeric_revision]
    elif alpha_revision != "":
        s = [i for i in alpha_revision]
    elif mix_revision != "":
        s = [i for i in mix_revision]
    
    if type == "Edit":
        if s: # if list is not empty
            s.reverse()

            # Case 1: digit, change from 01 to 02, keyword: digit2digit
            if numeric_revision != "" and alpha_revision == "" and mix_revision == "":
                for i, element in enumerate(s):
                    if ord(element) >= 48 and ord(element) < 57:
                        s[i] = chr(ord(element) + 1)
                        break
                    else:
                        s[i] = "0"
                        
            # Case 2: alpha, change from A to A01, keyword: alpha2alphadigit
            if numeric_revision == "" and alpha_revision != "" and mix_revision == "":
                s.reverse()
                s.append("01")
                s.reverse()
                    
            # Case 3: alpha + digit,  change from A01 to A02, or AA01 to AA02, keyword: alphadigit2alphadigit
            if numeric_revision == "" and alpha_revision == "" and mix_revision != "":
                if len(mix_revision) < 3:
                    return ""
                
                if len(mix_revision) == 3:
                    alpha = mix_revision[0]
                    number = [i for i in mix_revision[1:]]
                    number.reverse()
                    for i, element in enumerate(number):
                        if ord(element) >= 48 and ord(element) < 57: # in ACSII, CHAR "A" = 48 in DEC, "Z" = 57
                            number[i] = chr(ord(element) + 1)
                            break
                        else:
                            number[i] = "0"
                    number_ = ""
                    for i in number:
                        number_ = number_ + i
                    number_ = number_ + alpha
                    
                    s = []
                    s = [i for i in number_]
                    
                if len(mix_revision) == 4:
                    alpha = [i for i in mix_revision[:2]]
                    number = [i for i in mix_revision[2:]]
                    number.reverse()
                    for i, element in enumerate(number):
                        if ord(element) >= 48 and ord(element) < 57:
                            number[i] = chr(ord(element) + 1)
                            break
                        else:
                            number[i] = "0"
                    
                    number_ = ""
                    alpha.reverse()
                    number.reverse()
                    for i in number:
                        number_ = number_ + i
                    for i in alpha:
                        number_ = i + number_
                    
                    s = []
                    s = [i for i in number_]
                    s.reverse()
            
            s.reverse()
            new_revision = ""
            for i in s:
                new_revision = new_revision + i
        else:
            return ""
    
    if type == "Release":
        if s:
            s.reverse()
            # Case 1: digit, example: 01 to A, keyword: digit2alpha
            if numeric_revision != "" and alpha_revision == "" and mix_revision == "":
                s = []
                s.append("A")

            # Case 2: mix, example: A01 to B, keyword: alphadigit2alpha
            if numeric_revision == "" and alpha_revision == "" and mix_revision != "":
                alpha   = []
                number  = []

                if len(mix_revision) == 3:
                    alpha.append(mix_revision[0])
                    number  = [i for i in mix_revision[1:]]

                if len(mix_revision) == 4:
                    alpha   = [i for i in mix_revision[:2]]
                    number  = [i for i in mix_revision[2:]]
                
                # Example: A01 to A
                if len(alpha) == 1:
                    if ord(alpha[0]) >= 65 and ord(alpha[0]) < 90:
                        alpha[0] = chr(ord(alpha[0]) + 1)
                    else:
                        alpha[0] = "AA"
                if len(alpha) == 2:
                    alpha.reverse()
                    for i, e in enumerate(alpha):
                        if ord(e) >= 65 and ord(e) < 90:
                            alpha[i] = chr(ord(alpha[0]) + 1)
                            break
                        else:
                            alpha[0] = "A"
                    alpha.reverse()
                s = []
                for i in alpha:
                    s.append(i)
                s.reverse()
            # Case 3: alpha, example: A to B, keyword: 
            if numeric_revision == "" and alpha_revision != "" and mix_revision == "":
                # Example: A to B, Z to AA
                if alpha_revision == "Z":
                    return "AA"
                if alpha_revision == "ZZ":
                    return "AAA"
                
                for i, element in enumerate(s):
                    if ord(element) >= 65 and ord(element) < 90:
                        s[i] = chr(ord(element) + 1)
                        break
                    else:
                        s[i] = "A"
            s.reverse()
            new_revision = ""
            for i in s:
                new_revision = new_revision + i
        else:
            return ""
    
    return new_revision # like: 02, A, B, A02

def EXPORT_XY_FORMAT_FOR_IUA_PLUS_FILE(card_part_number="", X=[], Y=[], status="", unit="mm", sheet_name = 'Sheet1'):
    """
    # Input Parameters:
    #   1.card_part_number as PCX-000000, MSP-000000
    #   2.X coordinates from tab 1 table, like X = [0,1,2,3,4,5,...,n]
    #   3.Y coordinates from tab 1 table, like Y = [0,1,2,3,4,5,...,n]
    #   4.sheet_name is "Sheet1" as default
    #   5.status: Release, Edit or Override
    # Note Unit is mm as default, convert to mm if unit is not 'mm'
    
    # Get file name, file extension from path.txt file
    file_name, file_extension = GET_FILE_PATH('paths.txt', 'XY_FORMAT_FOR_IUA_PLUS_FILENAME')
    # example: file_name = "YYY-XXXXXX_XY input format for IUA_plus_Rev00" and file_extension = "xlsx"
    
    # Get folder template path
    folder_template_location    = GET_FOLDER_PATH('paths.txt', 'folder_template_path')
    
    # Get revision in file name:
    revision_string_format      = GET_REVISION_STRING('paths.txt', "REVISION_FORMAT")
    
    revision_pos_in_file_name   = file_name.index(revision_string_format)
    revision_string             = file_name[revision_pos_in_file_name:]
    
    old_revision = revision_string[len(revision_string_format):]
    new_revision = REVISION_CHANGE_TYPE(old_revision, status) # status  = ["Release", "Edit", "Override"]
    
    new_file_name = file_name.replace("YYY-XXXXXX", card_part_number)
    new_file_name = file_name.replace(old_revision, new_revision)
    new_location = GET_FOLDER_PATH('paths.txt', 'design_folder_path') + "/" + str(card_part_number) + '-xx'
    
    scr = folder_template_location + "/" + file_name + "." + file_extension
    dst = new_location + "/" + new_file_name + "." + file_extension
    
    try:
        shutil.copyfile(scr, dst)
    except:
        # Create new file
        if not os.path.exists(dst):
            return "A folder does not exist"
        else:
            return "Error!"
    
    load_workbook = openpyxl.load_workbook(dst)
    active_sheet = workbook[sheet_name] # active "Sheet1"
    """
    return "EXPORT_XY_FORMAT_FOR_IUA_PLUS_FILE"

def EXPORT_PCB_PAD_LOCATION_FILE():
    return "EXPORT_PCB_PAD_LOCATION_FILE"

def EXPORT_ARRAY_FULL_SITE_FOR_REFERENCE_FILE():
    return "EXPORT_ARRAY_FULL_SITE_FOR_REFERENCE_FILE"

def EXPORT_IUA_PLUS_FILE():
    return "EXPORT_IUA_PLUS_FILE"

def EXPORT_CRD_PLUS_FILE():
    return "EXPORT_CRD_PLUS_FILE"

def EXPORT_PROBE_HEAD_XY_COORDINATES_FOR_APPROVAL_FILE():
    """
    # Create a copy version from template for specify device
    try:
        shutil.copyfile(PROBE_HEAD_XY_TEMPLATE_FULLPATH, PROBE_HEAD_XY_FULLPATH)
    except PermissionError:
        Notification('Error', "This command can not perform. Please check again!")
        return 0, option
    
    # Load workbook
    workbook = openpyxl.load_workbook(PROBE_HEAD_XY_FULLPATH)

    # Active sheet 
    sheet = workbook[PROBE_HEAD_XY_SHEETS_NAME[1]]
    for row in range(1, table_TableWidget.rowCount()):
        for col in range(1,table_TableWidget.columnCount()+1):
            if table_TableWidget.item(row, col-1) is None:
                sheet.cell(row+7, col).value = ""
            else:
                text = table_TableWidget.item(row, col-1).text()
                if text.isdigit()==1:
                    sheet.cell(row+7, col).value = int(text)
                elif text.replace(".","").replace("-", "").isnumeric():
                    sheet.cell(row+7, col).value = float(text)
                else:
                    sheet.cell(row+7, col).value = text

    # Save workbook
    workbook.save(PROBE_HEAD_XY_FULLPATH)
    """
    return "PROBE_HEAD_XY_COORDINATES_FOR_APPROVAL_FILE"