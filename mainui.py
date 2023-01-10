import sys
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from matplotlib.figure import Figure
from BlurWindow.blurWindow import blur
from variables import *
from functions import *
from xlwt import Workbook
import openpyxl
import shutil
import time
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self, app, new_project, spec=None):
        super().__init__()      

        self.new_project = new_project

        # Variables to store XY coordinates list
        self.X, self.Y = [], []
        # Variables to store XY coordinates list after pattern
        self.X_list_pattern, self.Y_list_pattern = [], []
        
        # Inital input data unit
        self.XY_INPUT_UNIT          = MM_UNIT
        self.XY_INPUT_UNIT_PREVIOUS = ""
        self.STEPPING_DISTANCE_UNIT = UM_UNIT
        self.PAD_SIZE_UNIT          = UM_UNIT

        self.PAD_NAME_LIST          = []
        self.PAD_NUMBER_LIST        = []

        self.DUT_NAME_LIST          = []
        self.DUT_NAME_FORMAT        = ""
        self.DUT_NAME_DELIMITER     = ""
        self.DUT_NAME_POSITION      = -1    # Unsigned integer 0 to 255

        self.PAD_NAME_POSITION      = -1     # Unsigned integer 0 to 255
        self.PAD_NUMBER_POSITION    = -1   # Unsigned integer 0 to 255

        self.XY_Start_Row_Index     = -1    # Unsigned integer 0 to 4,294,967,295
        self.XY_End_Row_Index       = -1      # Unsigned integer 0 to 4,294,967,295

        self.Is_PAD_BUMP            = False

        self.NC_POSITION            = -1
        self.NC_LIST                = []
        self.NC_DENOTE              = ""
        self.KEEP_OUT_TYPE          = KEEP_OUT_TYPE["TYPE"][1]
        self.KEEP_OUT_UNIT          = MM_UNIT
        self.DUTY_CYCLE_TYPE        = DUTY_CYCLE["TYPE"][0]

        self.CURRENT_UNIT           = MAX_CURRENT['UNIT'][0]
        self.FREQUENCY_UNIT         = MAX_FREQUENCY['UNIT'][1]

        self.DIE_CONFIG             = np.array([])
        self.get_info               = []
        
        self.Remember_UNIT          = False

        # Export files option
        self.export_all_files                      = True
        self.export_XY_FORMAT_FOR_IUA_PLUS_file    = True
        self.export_ARRAY_FULL_SIZE_FILE_file      = True
        self.export_ROBE_HEAD_XY_FILE_file         = True
        self.export_PCB_PADS_LOCATION_FILE_file    = True
        self.export_PRELIM_PTP_FOR_SOLDER_PATTERN  = True
        self.export_IUA_PLUS_FILE_file             = True
        self.export_CRD_PLUS_FILE_file             = True

        # Create Table widget for Tab 1
        self.table                  = TableWindow()
        chart                       = Chart(width=5, height=4, dpi=100)
        self.CHART, self.toolbar    = SCATTER_CHART(self.X, self.Y, chart, self.NC_LIST, self.NC_DENOTE)
        self.Tab_content            = Tab_Widget(self, self.table, self.CHART, self.toolbar)

        # Create table in tab2 according to XY list SV format
        self.table_tab2     = TableWindow(NumRow=0, NumCol=0)
        table_tab2_layout   = QVBoxLayout()
        table_tab2_layout.addWidget(self.table_tab2)
        self.Tab_content.tab2.setLayout(table_tab2_layout)

        if CARD_PART_NUMBER['VALUE#'] != "": self.tree_tab3 = QTreeWidget()
            
        # Set main windoe title
        self.setWindowTitle(APP_NAME)
        
        # Set main window size
        self.screen = app.primaryScreen()
        self.setGeometry(0, 0, np.int16(self.screen.size().width()), np.int16(self.screen.size().height()))

        # Show main window as Maximize type
        self.showMaximized()
        
        # Set Main window icon
        self.setWindowIcon(QIcon('icon/card.png'))
        
        # Call elements
        self.Actions()
        self.MenuBar()
        self.CreateToolBars()
        self.Labels()
        self.Buttons()
        self.Layout()

        # Status bar
        self.status = QStatusBar()
        self.status.showMessage("Ready!")
        self.setStatusBar(self.status)
    
    # class MainWindow(QMainWindow):
    def Actions(self):
        self.newAction  = QAction(QIcon('icon/new.png'), NEW_ACTION, self)
        self.openAction = QAction(QIcon('icon/open.png'), OPEN_ACTION, self)
        self.saveAction = QAction(QIcon('icon/save.png'), SAVE_ACTION, self)
        self.exitAction = QAction(QIcon('icon/exit.png'), EXIT_ACTION, self)
        
        self.createChartAction  = QAction(QIcon('icon/scatter.png'), CREATE_CHART_BUTTON, self)
        self.clearChartAction   = QAction(QIcon('icon/clear_scatter.png'), CLEAR_CHART_BUTTON, self)
        
        self.setInputDataUnitAction = QAction(QIcon('icon/set_input_unit.png'), INPUT_UNIT_BUTTON, self)
        self.setDataInfoAction      = QAction(QIcon('icon/set_input_tag.png'), INPUT_INFO_BUTTON, self)

        self.importSpecformAction   = QAction(QIcon('icon/import_Specform_Action.png'), IMPORT_INFO_SPEC_FORM_BUTTON, self)
        self.checkAction            = QAction(QIcon('icon/check.png'), CHECK_BUTTON, self)
        self.exportAction           = QAction(QIcon('icon/export.png'), EXPORT_BUTTON, self)

        self.generate_tab2_Action   = QAction(QIcon('icon/generate_XY_list_SV_format.png'), GENERATE_BUTTON, self)
        self.final_export_Action    = QAction(QIcon('icon/final_export.png'), FINAL_EXPORT_BUTTON, self)

        self.die_pattern_Action     = QAction(QIcon('icon/die_pattern.png'), DIE_PATTERN_BUTTON, self)

        # Set functions
        self.exitAction.triggered.connect(self.EXIT_APP)
        
        self.createChartAction.triggered.connect(self.CALL_CREATE_CHART)
        
        self.clearChartAction.triggered.connect(self.CALL_CLEAR_CHART)
        
        self.setInputDataUnitAction.triggered.connect(self.CALL_SET_INPUT_UNIT)
        
        self.setDataInfoAction.triggered.connect(self.GET_DATA)
        
        self.importSpecformAction.triggered.connect(self.IMPORT_SPEC_FORM)

        self.generate_tab2_Action.triggered.connect(self.CALL_GENERATE_XY_LIST_SV_FORMAT)

        self.exportAction.triggered.connect(self.CALL_EXPORT_FILES)

        self.final_export_Action.triggered.connect(self.FINAL_EXPORT)

        self.die_pattern_Action.triggered.connect(self.CALL_DIE_PATTERN)

    # class MainWindow(QMainWindow):
    def MenuBar(self):
        # Create Menu Bar
        menuBar = self.menuBar()

        # Create File menu
        fileMenu = QMenu(FILE_MENU, self)
        # Add Menu item
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        
        # Create Edit menu
        editMenu = QMenu(EDIT_MENU, self)

        # Add Edit menu item
        editMenu.addAction(self.setInputDataUnitAction)
        editMenu.addAction(self.setDataInfoAction)
        
        # Create Tool menu
        toolMenu = QMenu(TOOL_MENU, self)
        toolMenu.addAction(self.die_pattern_Action)
        toolMenu.addAction(self.generate_tab2_Action)
        toolMenu.addAction(self.importSpecformAction)
        toolMenu.addAction(self.checkAction)
        toolMenu.addAction(self.exportAction)
        toolMenu.addAction(self.final_export_Action)
        
        # Create Help menu
        helpMenu = QMenu(HELP_MENU, self)
        
        # Add to Menu bar
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(toolMenu)
        menuBar.addMenu(helpMenu)
    
    # class MainWindow(QMainWindow):
    def CreateToolBars(self):
        # File toolbar
        ChartToolBar = self.addToolBar(CHART_TOOL)
        ChartToolBar.addAction(self.createChartAction)
        ChartToolBar.addAction(self.clearChartAction)

        EditToolBar = self.addToolBar(EDIT_TOOL)
        EditToolBar.addAction(self.setInputDataUnitAction)
        EditToolBar.addAction(self.setDataInfoAction)
        EditToolBar.addAction(self.die_pattern_Action)

        ExportToolBar = self.addToolBar(EXPORT_TOOLS)
        ExportToolBar.addAction(self.importSpecformAction)
        ExportToolBar.addAction(self.checkAction)
        ExportToolBar.addAction(self.exportAction)
        ExportToolBar.addAction(self.generate_tab2_Action)
        ExportToolBar.addAction(self.final_export_Action)
    
    # class MainWindow(QMainWindow):
    def Labels(self):
        # Welcome label is showed on your UI
        self.Welcome_label = QLabel('Welcome')
        self.Welcome_label.setFont(QFont("3ds", 30))
        
        # XY file name is showed on your UI
        self.XY_file_name_label = QLabel('The XY file name here')
        self.XY_file_name_label.setFont(QFont("3ds", 11))
        self.XY_file_name_label.setAlignment(Qt.AlignLeft)

        # Card part number
        CARD_PART_NUMBER['LABEL'] = QLabel('Card Part Number')
        CARD_PART_NUMBER['VALUE'] = QLabel(CARD_PART_NUMBER['VALUE#'])
        CARD_PART_NUMBER["LABEL"].setFont(QFont("3ds", 10))
        CARD_PART_NUMBER["VALUE"].setFont(QFont("3ds", 10))
        CARD_PART_NUMBER["VALUE"].setAlignment(Qt.AlignRight)
        # End of Card part number variables

        # Customer name
        CUSTOMER_NAME["LABEL"] = QLabel('Customer')
        CUSTOMER_NAME["VALUE"] = QLabel('')
        CUSTOMER_NAME["LABEL"].setFont(QFont("3ds", 10))
        CUSTOMER_NAME["VALUE"].setFont(QFont("3ds", 10))
        CUSTOMER_NAME["VALUE"].setAlignment(Qt.AlignRight)
        # Device name
        DEVICE_NAME["LABEL"] = QLabel('Device')
        DEVICE_NAME["VALUE"] = QLabel('')
        DEVICE_NAME["LABEL"].setFont(QFont("3ds", 10))
        DEVICE_NAME["VALUE"].setFont(QFont("3ds", 10))
        DEVICE_NAME["VALUE"].setAlignment(Qt.AlignRight)
        # End of Customer name and device name

        # Space transformer type
        SPACE_TRANSFORMER_TYPE["LABEL"] = QLabel('Space transformer type')
        SPACE_TRANSFORMER_TYPE["VALUE"] = QLabel('')
        SPACE_TRANSFORMER_TYPE["LABEL"].setFont(QFont("3ds", 10))
        SPACE_TRANSFORMER_TYPE["VALUE"].setFont(QFont("3ds", 10))
        SPACE_TRANSFORMER_TYPE["VALUE"].setAlignment(Qt.AlignRight)
        # End of Space transformer type

        # Die size info
        DIE_SIZE["LABEL"] = QLabel('Die size')
        DIE_SIZE["VALUE"] = QLabel("X = " + str(DIE_SIZE["X"]) + "  and  " + "Y = " + str(DIE_SIZE["Y"]))
        DIE_SIZE["LABEL"].setFont(QFont("3ds", 10))
        DIE_SIZE["VALUE"].setFont(QFont("3ds", 10))
        DIE_SIZE["VALUE"].setAlignment(Qt.AlignRight)
        DIE_SIZE["LABEL"].setStyleSheet("border-top: 1px solid rgb(255,150,0)")
        DIE_SIZE["VALUE"].setStyleSheet("border-bottom: 1px solid rgb(255,150,0)")
        # end of Die size info

        # Total no. of Probe
        PROBE["LABEL"] = QLabel('Probes per die')
        PROBE["VALUE"] = QLabel(str(PROBE["VALUE#"]))
        PROBE["LABEL"].setFont(QFont("3ds", 10))
        PROBE["VALUE"].setFont(QFont("3ds", 10))
        PROBE["VALUE"].setAlignment(Qt.AlignRight)
        # End of Total no. of Probe

        # The smallest pad pitch
        MIN_PITCH["LABEL"] = QLabel('Min pitch (no NC)  |  (with NC)')
        MIN_PITCH["VALUE"] = QLabel("")
        MIN_PITCH["LABEL"].setFont(QFont("3ds", 10))
        MIN_PITCH["VALUE"].setFont(QFont("3ds", 10))
        MIN_PITCH["VALUE"].setAlignment(Qt.AlignRight)
        MIN_PITCH["LABEL"].setStyleSheet("border-top: 1px solid rgb(255,150,0)")
        MIN_PITCH["VALUE"].setStyleSheet("border-bottom: 1px solid rgb(255,150,0)")
        # End of The smallest pad pitch

        # Total no. of dies
        NO_OF_DIES["LABEL"] = QLabel('No of dies')
        NO_OF_DIES["VALUE"] = QLabel(str(NO_OF_DIES["VALUE#"]))
        NO_OF_DIES["LABEL"].setFont(QFont("3ds", 10))
        NO_OF_DIES["VALUE"].setFont(QFont("3ds", 10))
        # End of Total no. of dies

        # The distance between die to die
        STEPPING_DISTANCE['LABEL'] = QLabel('Stepping distance')
        STEPPING_DISTANCE['VALUE'] = QLabel("X = " + str(STEPPING_DISTANCE["X"]) + "  |  " +
                                            "Y = " + str(STEPPING_DISTANCE["Y"]) + " ")
        STEPPING_DISTANCE['LABEL'].setFont(QFont("3ds", 10))
        STEPPING_DISTANCE['VALUE'].setFont(QFont("3ds", 10))
        STEPPING_DISTANCE["VALUE"].setAlignment(Qt.AlignRight)
        STEPPING_DISTANCE["LABEL"].setStyleSheet("border-top: 1px solid rgb(255,150,0)")
        STEPPING_DISTANCE["VALUE"].setStyleSheet("border-bottom: 1px solid rgb(255,150,0)")
        # End of The distance between die to die
        
        # Total number of pads per die
        PADS_PER_DIE["LABEL"] = QLabel('Pads per die')
        PADS_PER_DIE["VALUE"] = QLabel(str(PADS_PER_DIE["VALUE#"]))
        PADS_PER_DIE["LABEL"].setFont(QFont("3ds", 10))
        PADS_PER_DIE["VALUE"].setFont(QFont("3ds", 10))
        # End of Total number of pads per die

        # Die configuration info
        DIE_CONFIG['LABEL'] = QLabel('Die Config')
        DIE_CONFIG['VALUE'] = QLabel("X = " + str(DIE_CONFIG["X_OR_COLUMN"]) + " col  |  " + 
                                     "Y = " + str(DIE_CONFIG["Y_OR_ROW"]) + "row")
        DIE_CONFIG["LABEL"].setFont(QFont("3ds", 10))
        DIE_CONFIG["VALUE"].setFont(QFont("3ds", 10))
        DIE_CONFIG["VALUE"].setAlignment(Qt.AlignRight)
        DIE_CONFIG["VALUE"].setStyleSheet("border-bottom: 1px solid rgb(255,150,0)")
        # End of Die configuration info

        # Minimum pad size is showed on your UI
        MIN_PAD_SIZE["LABEL"] = QLabel('Min PAD size')
        MIN_PAD_SIZE["VALUE"] = QLabel("X = " + str(MIN_PAD_SIZE["X"]) + "  and  " + 
                                       "Y = " + str(MIN_PAD_SIZE["Y"])+ " ")                      
        MIN_PAD_SIZE["LABEL"].setFont(QFont("3ds", 10))
        MIN_PAD_SIZE["VALUE"].setFont(QFont("3ds", 10))
        MIN_PAD_SIZE["VALUE"].setAlignment(Qt.AlignRight)
        MIN_PAD_SIZE["VALUE"].setStyleSheet("border-bottom: 1px solid rgb(255,150,0)")
        # end of Minimum pad size is showed on your UI

        # NC pad per die
        NC_PAD["LABEL"] = QLabel('No. of NC pad per die')
        NC_PAD["VALUE"] = QLabel(str(NC_PAD["VALUE#"]))
        
        NC_PAD["LABEL"].setFont(QFont("3ds", 10))
        NC_PAD["VALUE"].setFont(QFont("3ds", 10))
        # End of NC pad per die

        # Keep out info
        KEEP_OUT_TYPE["LABEL"] = QLabel('Keep out infomation')
        KEEP_OUT_TYPE["VALUE"] = QLabel('')
        
        KEEP_OUT_TYPE["LABEL"].setFont(QFont("3ds", 10))
        KEEP_OUT_TYPE["VALUE"].setFont(QFont("3ds", 10))
        # End of Keep out info

        # Wafer pad info
        WAFER_PAD["LABEL"] = QLabel('Wafer pad material')
        WAFER_PAD["VALUE"] = QLabel(WAFER_PAD["MATERIAL"])
        
        WAFER_PAD["LABEL"].setFont(QFont("3ds", 10))
        WAFER_PAD["VALUE"].setFont(QFont("3ds", 10))
        # End of Wafer pad info

        # Test temperature
        PROBING_TEMP["LABEL"] = QLabel('Test temperature')
        PROBING_TEMP["VALUE"] = QLabel('')
        
        PROBING_TEMP["LABEL"].setFont(QFont("3ds", 10))
        PROBING_TEMP["VALUE"].setFont(QFont("3ds", 10))
        # End of Test temperature

        # Current type and value
        DUTY_CYCLE["LABEL"] = QLabel('Duty cycle')
        DUTY_CYCLE["VALUE"] = QLabel(DUTY_CYCLE["TYPE"][0])
        
        DUTY_CYCLE["LABEL"].setFont(QFont("3ds", 10))
        DUTY_CYCLE["VALUE"].setFont(QFont("3ds", 10))
        # End of Current type and value

        # Maximum Current
        MAX_CURRENT["LABEL"] = QLabel('Max. Current')
        MAX_CURRENT["VALUE"] = QLabel("")
        
        MAX_CURRENT["LABEL"].setFont(QFont("3ds", 10))
        MAX_CURRENT["VALUE"].setFont(QFont("3ds", 10))
        # End of Maximum Current

        # MAX FREQUENCY
        MAX_FREQUENCY["LABEL"] = QLabel('Max. Frequency')
        MAX_FREQUENCY["VALUE"] = QLabel("")
        
        MAX_FREQUENCY["LABEL"].setFont(QFont("3ds", 10))
        MAX_FREQUENCY["VALUE"].setFont(QFont("3ds", 10))
        # End og MAX FREQUENCY

        PROBE_PART_NUMBER['LABEL'] = QLabel('Probe part number')
        PROBE_PART_NUMBER['VALUE'] = QLabel('')
        
        PROBE_PART_NUMBER["LABEL"].setFont(QFont("3ds", 10))
        PROBE_PART_NUMBER["VALUE"].setFont(QFont("3ds", 10))
        
    # class MainWindow(QMainWindow):
    def Buttons(self):
        # Create IMPORT EXCEL button
        self.Import_XY_button = QPushButton('Import XY File')
        self.Import_XY_button.setStyleSheet(IMPORT_XY_BUTTON_STYLE_SHEET)
        
        # Set button function
        self.Import_XY_button.clicked.connect(self.CALL_IMPORT_EXCEL2TABLE_FUNC)
    
    # class MainWindow(QMainWindow):
    def Layout(self):
        # LEFT PANEL of Main window
        left_frame = QFrame()
        left_frame.setFrameShape(QFrame.StyledPanel)

        # Create a layout on left panel of main window
        form_layout = QFormLayout()
        
        form_layout.addRow(self.Welcome_label)
        form_layout.addRow(self.XY_file_name_label)
        form_layout.addRow(self.Import_XY_button)

        line0 = QHBoxLayout()
        line0.addWidget(CARD_PART_NUMBER['LABEL'])
        line0.addStretch(1)
        line0.addWidget(CARD_PART_NUMBER["VALUE"])
        form_layout.addRow(line0)

        line1 = QHBoxLayout()
        line1.addWidget(CUSTOMER_NAME["LABEL"])
        line1.addStretch(1)
        line1.addWidget(CUSTOMER_NAME["VALUE"])
        form_layout.addRow(line1)

        line2 = QHBoxLayout()
        line2.addWidget(DEVICE_NAME["LABEL"])
        line2.addStretch(1)
        line2.addWidget(DEVICE_NAME["VALUE"])
        form_layout.addRow(line2)

        line3 = QHBoxLayout()
        line3.addWidget(SPACE_TRANSFORMER_TYPE["LABEL"])
        line3.addStretch(1)
        line3.addWidget(SPACE_TRANSFORMER_TYPE["VALUE"])
        form_layout.addRow(line3)

        form_layout.addRow(DIE_SIZE["LABEL"])
        form_layout.addRow(DIE_SIZE["VALUE"])

        line11 = QHBoxLayout()
        line11.addWidget(PADS_PER_DIE["LABEL"])
        line11.addStretch(1)
        line11.addWidget(PADS_PER_DIE["VALUE"])
        form_layout.addRow(line11)

        line16 = QHBoxLayout()
        line16.addWidget(NC_PAD["LABEL"])
        line16.addStretch(1)
        line16.addWidget(NC_PAD["VALUE"]) 
        form_layout.addRow(line16)

        line5 = QHBoxLayout()
        line5.addWidget(PROBE["LABEL"])
        line5.addStretch(1)
        line5.addWidget(PROBE["VALUE"])
        form_layout.addRow(line5)

        form_layout.addRow(MIN_PITCH["LABEL"]) # line6
        form_layout.addRow(MIN_PITCH["VALUE"]) # line7

        line8 = QHBoxLayout()
        line8.addWidget(NO_OF_DIES["LABEL"])
        line8.addStretch(1)
        line8.addWidget(NO_OF_DIES["VALUE"])
        form_layout.addRow(line8)
        
        form_layout.addRow(STEPPING_DISTANCE["LABEL"]) #line9
        form_layout.addRow(STEPPING_DISTANCE["VALUE"]) #line10

        form_layout.addRow(DIE_CONFIG["LABEL"]) #line12
        form_layout.addRow(DIE_CONFIG["VALUE"]) #line13

        form_layout.addRow(MIN_PAD_SIZE["LABEL"]) #line14
        form_layout.addRow(MIN_PAD_SIZE["VALUE"]) #line15

        line17 = QHBoxLayout()
        line17.addWidget(KEEP_OUT_TYPE["LABEL"])
        line17.addStretch(1)
        line17.addWidget(KEEP_OUT_TYPE["VALUE"]) 
        form_layout.addRow(line17)

        line18 = QHBoxLayout()
        line18.addWidget(WAFER_PAD["LABEL"])
        line18.addStretch(1)
        line18.addWidget(WAFER_PAD["VALUE"]) 
        form_layout.addRow(line18)

        line19 = QHBoxLayout()
        line19.addWidget(PROBING_TEMP["LABEL"])
        line19.addStretch(1)
        line19.addWidget(PROBING_TEMP["VALUE"]) 
        form_layout.addRow(line19)

        line20 = QHBoxLayout()
        line20.addWidget(DUTY_CYCLE["LABEL"])
        line20.addStretch(1)
        line20.addWidget(DUTY_CYCLE["VALUE"]) 
        form_layout.addRow(line20)

        line21 = QHBoxLayout()
        line21.addWidget(MAX_CURRENT["LABEL"])
        line21.addStretch(1)
        line21.addWidget(MAX_CURRENT["VALUE"]) 
        form_layout.addRow(line21)

        line22 = QHBoxLayout()
        line22.addWidget(MAX_FREQUENCY["LABEL"])
        line22.addStretch(1)
        line22.addWidget(MAX_FREQUENCY["VALUE"]) 
        form_layout.addRow(line22)

        line23 = QHBoxLayout()
        line23.addWidget(PROBE_PART_NUMBER['LABEL'])
        line23.addStretch(1)
        line23.addWidget(PROBE_PART_NUMBER['VALUE'])
        form_layout.addRow(line23)

        left_frame.setLayout(form_layout)
        left_frame.setFixedWidth(250)
        
        # RIGHT PANEL of Main window
        right_frame = QFrame()
        right_frame.setFrameShape(QFrame.StyledPanel)

        ver_box = QVBoxLayout()
        left, top, right, bottom = 5,5,5,5
        ver_box.setContentsMargins(left, top, right, bottom)
        ver_box.addWidget(self.Tab_content.Return())
        
        right_frame.setLayout(ver_box)
        
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(left_frame)
        main_splitter.addWidget(right_frame)
            
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(main_splitter)
        self.setCentralWidget(main_splitter)

    # class MainWindow(QMainWindow):
    def CALL_IMPORT_EXCEL2TABLE_FUNC(self):
        #Reset status
        self.status.showMessage("Ready!")
        self.status.setStyleSheet("color: rgb(255,255,255)")
        self.X, self.Y              = [], []
        self.PAD_NAME_LIST          = []
        self.PAD_NUMBER_LIST        = []
        self.DUT_NAME_LIST          = []
        self.Welcome_label.setText('<font color="#FFFFFF">Nidec</font> <font color="#FFFFFF">SV</font> <font color="#FFFFFF">TCL</font>')
        self.Welcome_label.setFont(QFont("3ds", 30))

        # Get file path and file name
        path, file_name, file_extension = GET_FILE()
        
        if path == "": # Check path if it's empty
            self.status.showMessage("No file")
            self.status.setStyleSheet("color: rgb(50,255,50)")
            return
        else:
            status, sheet_name = IMPORT_EXCEL2TABLE(self.table.TableWidget, path = path, extension = file_extension)
            if status == 0:
                self.status.showMessage("No any sheet's selected!")
                self.status.setStyleSheet("color: red")
                return
            
            self.XY_file_name_label.setText("File Name: \n" + str(file_name) + "\n'" + str(sheet_name) + "' sheet")
            self.XY_file_name_label.setWordWrap(True)
            self.status.showMessage("Ready!")
            self.status.setStyleSheet("color: white")
            
            NO_OF_DIES["VALUE#"] = 1
            NO_OF_DIES["VALUE"].setText(str(NO_OF_DIES["VALUE#"]))
            DIE_CONFIG["X_OR_COLUMN"] = 1
            DIE_CONFIG["Y_OR_ROW"] = 1
            DIE_CONFIG['VALUE'].setText("X = " + str(DIE_CONFIG["X_OR_COLUMN"])+" col  |  " + \
                                        "Y = " + str(DIE_CONFIG["Y_OR_ROW"])+" row")
            
            # self.get_info.Reset_button_clicked()
        
    # class MainWindow(QMainWindow):        
    def CALL_CREATE_CHART(self):
        self.X, self.Y, row_start_end_index, status = GET_XY_FROM_MOUSE(self.table.TableWidget)
        if status == 1:
            self.XY_Start_Row_Index  = row_start_end_index[0]
            self.XY_End_Row_Index    = row_start_end_index[1]
            if self.Remember_UNIT == False:
                question_unit = ASK_UNIT(self.Remember_UNIT, self.XY_INPUT_UNIT)
                self.XY_INPUT_UNIT, self.Remember_UNIT = question_unit.Return_Unit()
            
            chart = Chart(width=5, height=4, dpi=100)
            self.CHART, self.toolbar = SCATTER_CHART(self.X, self.Y, chart, self.NC_LIST, self.NC_DENOTE, self.PAD_NAME_LIST, self.PAD_NUMBER_LIST)
            
            self.Tab_content.chart_tab1.itemAt(0).widget().deleteLater()
            self.Tab_content.chart_tab1.itemAt(1).widget().deleteLater()
            
            self.Tab_content.chart_tab1.addWidget(self.toolbar)
            self.Tab_content.chart_tab1.addWidget(self.CHART)
            
            self.UPDATE_INFO()

    # class MainWindow(QMainWindow):
    def CALL_CLEAR_CHART(self):
        chart = Chart(width=5, height=4, dpi=100)
        self.CHART, self.toolbar = SCATTER_CHART([], [], chart, [], "")

        self.Tab_content.chart_tab1.itemAt(0).widget().deleteLater()
        self.Tab_content.chart_tab1.itemAt(1).widget().deleteLater()

        self.Tab_content.chart_tab1.addWidget(self.toolbar)
        self.Tab_content.chart_tab1.addWidget(self.CHART)

    # class MainWindow(QMainWindow):
    def UPDATE_INFO(self):
        PROBE["VALUE#"] = len(self.X)
        PROBE["VALUE"].setText(str(PROBE["VALUE#"]))
        
        DIE_SIZE['X'], DIE_SIZE['Y'] = CAL_DIE_SIZE(self.X, self.Y)
        DIE_SIZE['X'], DIE_SIZE['Y'] = round(DIE_SIZE['X'],2), round(DIE_SIZE['Y'],2)
        # Update Die size info on left panel
        DIE_SIZE["VALUE"].setText("X = " + str(DIE_SIZE["X"]) + "  and  " + \
                                "Y = " + str(DIE_SIZE["Y"]) + " " + str(self.XY_INPUT_UNIT))
        
        # Reset
        MIN_PITCH["VALUE#"] = 0.0
        MIN_PITCH["VALUE"].setText(str(MIN_PITCH["VALUE#"]) + " " + str(self.XY_INPUT_UNIT) + "  |  " + str(MIN_PITCH_HAS_NC))
        
        # Calculate min pitch
        self.status.showMessage("Ready!")
        start_time = time.time()
        cal_min_distance = ClosestPair(self.X, self.Y)
        MIN_PITCH["VALUE#"] =  cal_min_distance.min_distance_in_points()
        end_time = time.time() - start_time
        
        if MIN_PITCH["VALUE#"] == -1:
            MIN_PITCH["VALUE"].setText('Only 1 point')
        else:
            if self.XY_INPUT_UNIT == MM_UNIT:
                self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT
                MIN_PITCH["VALUE#"] = MIN_PITCH["VALUE#"]*1000 # convert mm to um
                MIN_PITCH["VALUE#"] = round(MIN_PITCH["VALUE#"], 2)
            if self.XY_INPUT_UNIT == MIL_UNIT:
                self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT
                MIN_PITCH["VALUE#"]= MIN_PITCH["VALUE#"]*25.4 # convert mils to um
                MIN_PITCH["VALUE#"] = round(MIN_PITCH, 2)
            if self.XY_INPUT_UNIT == UM_UNIT:
                self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT
                MIN_PITCH["VALUE#"] = round(MIN_PITCH["VALUE#"], 2)
            
            MIN_PITCH["VALUE"].setText(str(MIN_PITCH["VALUE#"]) + " " + UM_UNIT + "  |  " + str(MIN_PITCH_HAS_NC))
            
            self.status.showMessage("Calculation within " + str(round(end_time*1000, 2)) + " ms")
        
        return

    # class MainWindow(QMainWindow):
    def CALL_SET_INPUT_UNIT(self):
        question_unit = ASK_UNIT(self.Remember_UNIT, self.XY_INPUT_UNIT)
        self.XY_INPUT_UNIT, self.Remember_UNIT = question_unit.Return_Unit()
        
        DIE_SIZE["VALUE"].setText("X = " + str(DIE_SIZE["X"]) + "  and  " + \
                                    "Y = " + str(DIE_SIZE["Y"]) + " " + str(self.XY_INPUT_UNIT))
        
        if self.XY_INPUT_UNIT_PREVIOUS  == MM_UNIT and \
            self.XY_INPUT_UNIT          == MM_UNIT:
            
            MIN_PITCH["VALUE#"]         = MIN_PITCH["VALUE#"]
            self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT
        
        if self.XY_INPUT_UNIT_PREVIOUS  == MIL_UNIT and \
            self.XY_INPUT_UNIT          == MM_UNIT:
            
            MIN_PITCH["VALUE#"]         = MIN_PITCH["VALUE#"]/25.4*1000
            self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT
        
        if self.XY_INPUT_UNIT_PREVIOUS  == UM_UNIT and \
            self.XY_INPUT_UNIT          == MM_UNIT:
            
            MIN_PITCH["VALUE#"]         = MIN_PITCH["VALUE#"]*1000
            self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT
        
        if self.XY_INPUT_UNIT_PREVIOUS  == MM_UNIT and \
            self.XY_INPUT_UNIT          == UM_UNIT:
            
            MIN_PITCH["VALUE#"]         = MIN_PITCH["VALUE#"]/1000
            self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT

        if self.XY_INPUT_UNIT_PREVIOUS  == MIL_UNIT and \
           self.XY_INPUT_UNIT           == UM_UNIT:

            MIN_PITCH["VALUE#"]         = MIN_PITCH["VALUE#"]/25.4
            self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT
        
        if self.XY_INPUT_UNIT_PREVIOUS  == UM_UNIT and \
            self.XY_INPUT_UNIT          == UM_UNIT:
            
            MIN_PITCH["VALUE#"]         = MIN_PITCH["VALUE#"]
            self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT

        if self.XY_INPUT_UNIT_PREVIOUS  == MM_UNIT and \
            self.XY_INPUT_UNIT          == MIL_UNIT:
            
            MIN_PITCH["VALUE#"]         = MIN_PITCH["VALUE#"]/1000*25.4
            self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT
            
        if self.XY_INPUT_UNIT_PREVIOUS  == MIL_UNIT and \
            self.XY_INPUT_UNIT          == MIL_UNIT:
            
            MIN_PITCH["VALUE#"]         = MIN_PITCH["VALUE#"]
            self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT
        
        if self.XY_INPUT_UNIT_PREVIOUS  == UM_UNIT and \
            self.XY_INPUT_UNIT          == MIL_UNIT:
            
            MIN_PITCH["VALUE#"]         = MIN_PITCH["VALUE#"]*25.4
            self.XY_INPUT_UNIT_PREVIOUS = self.XY_INPUT_UNIT
        
        MIN_PITCH["VALUE#"] = round(MIN_PITCH["VALUE#"], 2)
        MIN_PITCH["VALUE"].setText(str(MIN_PITCH["VALUE#"]) + " " + UM_UNIT + "  |  " + str(MIN_PITCH_HAS_NC))
    # End of CALL_SET_INPUT_UNIT() function #

    # class MainWindow(QMainWindow):
    def GET_DATA(self):
        # Reset status
        self.status.showMessage("Ready!")
        # Create GetInfo class
        self.get_info = GetInfo([self.PAD_NUMBER_POSITION,       self.PAD_NAME_POSITION,             self.DUT_NAME_POSITION,     self.DUT_NAME_FORMAT,
                            self.DUT_NAME_DELIMITER,        self.NC_POSITION,                   self.NC_DENOTE,             self.PAD_SIZE_UNIT,
                            self.Is_PAD_BUMP,               MIN_PAD_SIZE["D"],                  MIN_PAD_SIZE["X"],          MIN_PAD_SIZE["Y"],
                            self.STEPPING_DISTANCE_UNIT,    STEPPING_DISTANCE['X'],             STEPPING_DISTANCE['Y'],    CUSTOMER_NAME["NAME"],
                            DEVICE_NAME["NAME"],            SPACE_TRANSFORMER_TYPE['TYPE'],     PROBING_TEMP["VALUE#"],     self.DUTY_CYCLE_TYPE,
                            MAX_CURRENT['VALUE#'],          MAX_FREQUENCY["VALUE#"],            self.KEEP_OUT_TYPE,         self.KEEP_OUT_UNIT,
                            KEEP_OUT_TYPE['RECTANGLE_X_SIZE'],  KEEP_OUT_TYPE['RECTANGLE_Y_SIZE'], KEEP_OUT_TYPE['CIRCLE_DIAMETER'], self.CURRENT_UNIT, 
                            self.FREQUENCY_UNIT,            WAFER_PAD['MATERIAL'],              PROBE_PART_NUMBER['PART_NUMBER'],   CARD_PART_NUMBER['VALUE#'],
                            self.DIE_CONFIG])
        # Get info
        self.PAD_NUMBER_POSITION,       self.PAD_NAME_POSITION,             self.DUT_NAME_FORMAT,   self.DUT_NAME_POSITION, \
        self.NC_POSITION,               self.NC_DENOTE,                     CUSTOMER_NAME["NAME"],  DEVICE_NAME["NAME"], \
        SPACE_TRANSFORMER_TYPE["TYPE"], self.KEEP_OUT_TYPE,                 self.KEEP_OUT_UNIT,     self.DUTY_CYCLE_TYPE, \
        WAFER_PAD['MATERIAL'],          PROBE_PART_NUMBER['PART_NUMBER'],   self.DUT_NAME_DELIMITER,  CARD_PART_NUMBER['VALUE#'] = self.get_info.Return()
        
        MIN_PAD_SIZE["D"], MIN_PAD_SIZE["X"], MIN_PAD_SIZE["Y"], self.PAD_SIZE_UNIT = self.get_info.Get_Pad_Size()
        
        self.Is_PAD_BUMP                                                            = self.get_info.Get_Bump_Type()
        
        self.STEPPING_DISTANCE_UNIT                                                 = self.get_info.Get_Stepping_distance_unit()
        
        STEPPING_DISTANCE['X'], STEPPING_DISTANCE['Y']                              = self.get_info.Get_Stepping_distance()

        KEEP_OUT_TYPE['RECTANGLE_X_SIZE'],  KEEP_OUT_TYPE['RECTANGLE_Y_SIZE'], KEEP_OUT_TYPE['CIRCLE_DIAMETER'] = self.get_info.Get_Keep_out_size()

        PROBING_TEMP["VALUE#"], MAX_CURRENT['VALUE#'], MAX_FREQUENCY["VALUE#"], self.CURRENT_UNIT, self.FREQUENCY_UNIT    = self.get_info.other()

        # Update card part number on left panel
        if CARD_PART_NUMBER['VALUE#'] != "": CARD_PART_NUMBER['VALUE'].setText(CARD_PART_NUMBER['VALUE#'])

        # Update customer name on left panel
        if CUSTOMER_NAME["NAME"] != "": CUSTOMER_NAME["VALUE"].setText(CUSTOMER_NAME["NAME"])

        # Update device name on left panel
        if DEVICE_NAME["NAME"] != "": DEVICE_NAME["VALUE"].setText(DEVICE_NAME["NAME"])

        # Update Pad name list
        if self.PAD_NAME_POSITION >= 0: #and self.XY_Start_Row_Index >= 0 and self.XY_End_Row_Index >= 0:
            self.PAD_NAME_POSITION = self.PAD_NAME_POSITION - 1
            if self.XY_Start_Row_Index >= 0 and self.XY_End_Row_Index >= 0 and self.table.TableWidget.item(self.XY_Start_Row_Index, self.PAD_NAME_POSITION) != None:
                self.PAD_NAME_LIST = [self.table.TableWidget.item(row, self.PAD_NAME_POSITION).text() for row in range(self.XY_Start_Row_Index, self.XY_End_Row_Index+1)]
            else:
                self.PAD_NAME_LIST.clear()

        # Update pad number list
        if self.PAD_NUMBER_POSITION >= 0: #and self.XY_Start_Row_Index >= 0 and self.XY_End_Row_Index >= 0:
            self.PAD_NUMBER_POSITION = self.PAD_NUMBER_POSITION - 1
            if self.XY_Start_Row_Index >= 0 and self.XY_End_Row_Index >= 0 and self.table.TableWidget.item(self.XY_Start_Row_Index, self.PAD_NUMBER_POSITION) != None:
                self.PAD_NUMBER_LIST = [self.table.TableWidget.item(row, self.PAD_NUMBER_POSITION).text() for row in range(self.XY_Start_Row_Index, self.XY_End_Row_Index+1)]
            else:
                self.PAD_NUMBER_LIST.clear()

        # Update Dut name list
        if self.DUT_NAME_POSITION >= 0: # and self.XY_Start_Row_Index >= 0 and self.XY_End_Row_Index >= 0:
            self.DUT_NAME_POSITION = self.DUT_NAME_POSITION - 1
            if self.XY_Start_Row_Index >= 0 and self.XY_End_Row_Index >= 0 and self.table.TableWidget.item(self.XY_Start_Row_Index, self.DUT_NAME_POSITION) != None:
                self.DUT_NAME_LIST = [self.table.TableWidget.item(row, self.DUT_NAME_POSITION).text() for row in range(self.XY_Start_Row_Index, self.XY_End_Row_Index+1)]
            else:
                self.DUT_NAME_LIST.clear()

        # Update NC list
        if self.NC_POSITION >= 0: #and self.XY_Start_Row_Index >= 0 and self.XY_End_Row_Index >= 0:
            self.NC_POSITION = self.NC_POSITION - 1
            if self.XY_Start_Row_Index >= 0 and self.XY_End_Row_Index >= 0 and self.table.TableWidget.item(self.XY_Start_Row_Index, self.NC_POSITION) != None:
                self.NC_LIST  = [self.table.TableWidget.item(row, self.NC_POSITION).text() for row in range(self.XY_Start_Row_Index, self.XY_End_Row_Index+1)]
            else:
                self.NC_LIST.clear()

        if len(set(self.DUT_NAME_LIST)) > 1: NO_OF_DIES["VALUE#"] = len(set(self.DUT_NAME_LIST))
        NO_OF_DIES["VALUE"].setText(str(NO_OF_DIES["VALUE#"]))
        
        if MIN_PAD_SIZE["D"] > np.float16(0.0) and self.Is_PAD_BUMP == True:
            MIN_PAD_SIZE["VALUE"].setText(str(MIN_PAD_SIZE["D"]) + self.PAD_SIZE_UNIT)

        if MIN_PAD_SIZE["X"] > np.float16(0.0) and MIN_PAD_SIZE["Y"] > np.float16(0.0) and self.Is_PAD_BUMP == False:
            MIN_PAD_SIZE["VALUE"].setText("X = " + str(MIN_PAD_SIZE["X"]) + "  and  " + \
                                        "Y = " + str(MIN_PAD_SIZE["Y"])+ " " + self.PAD_SIZE_UNIT)
        if STEPPING_DISTANCE["X"] != 0.0 and STEPPING_DISTANCE["Y"] != 0.0:
            STEPPING_DISTANCE['VALUE'].setText("X = " + str(STEPPING_DISTANCE["X"]) + "  |  " +  \
                                            "Y = " + str(STEPPING_DISTANCE["Y"]) + " " + str(self.STEPPING_DISTANCE_UNIT))

        if self.KEEP_OUT_TYPE == KEEP_OUT_TYPE["TYPE"][0] and KEEP_OUT_TYPE['RECTANGLE_X_SIZE'] != 0.0 and KEEP_OUT_TYPE['RECTANGLE_Y_SIZE'] != 0.0:
            KEEP_OUT_TYPE["VALUE"].setText("X:"+str(KEEP_OUT_TYPE['RECTANGLE_X_SIZE'])+" Y:"+str(KEEP_OUT_TYPE['RECTANGLE_Y_SIZE'])+" "+str(self.KEEP_OUT_UNIT))
        elif self.KEEP_OUT_TYPE == KEEP_OUT_TYPE["TYPE"][1] and KEEP_OUT_TYPE['CIRCLE_DIAMETER'] != 0.0:
            KEEP_OUT_TYPE["VALUE"].setText("D:"+str(KEEP_OUT_TYPE['CIRCLE_DIAMETER']) + str(self.KEEP_OUT_UNIT))

        if PROBING_TEMP["VALUE#"] != 0.0:
            PROBING_TEMP["VALUE"].setText(str(PROBING_TEMP["VALUE#"]) + "(Celsius)")
        
        if MAX_CURRENT["VALUE#"] != 0.0:
            MAX_CURRENT["VALUE"].setText(str(MAX_CURRENT["VALUE#"]) + " " + self.CURRENT_UNIT)
        
        if MAX_FREQUENCY["VALUE#"] != 0.0:
            MAX_FREQUENCY["VALUE"].setText(str(MAX_FREQUENCY["VALUE#"]) + " " + self.FREQUENCY_UNIT)

        DUTY_CYCLE["VALUE"].setText(self.DUTY_CYCLE_TYPE)

        PROBE_PART_NUMBER['VALUE'].setText(PROBE_PART_NUMBER['PART_NUMBER'])

        WAFER_PAD['VALUE'].setText(WAFER_PAD['MATERIAL'])

        chart = Chart(width=5, height=4, dpi=100)
        self.CHART, self.toolbar = SCATTER_CHART(self.X, self.Y, chart, self.NC_LIST, self.NC_DENOTE, Pad_name=self.PAD_NAME_LIST, Pad_number=self.PAD_NUMBER_LIST)
        self.Tab_content.chart_tab1.itemAt(0).widget().deleteLater()
        self.Tab_content.chart_tab1.itemAt(1).widget().deleteLater()
        self.Tab_content.chart_tab1.addWidget(self.toolbar)
        self.Tab_content.chart_tab1.addWidget(self.CHART)

        self.DIE_CONFIG = self.get_info.Get_Config_Array()
    # End of GET_DATA() function #

    # class MainWindow(QMainWindow):
    def IMPORT_SPEC_FORM(self):
        self.status.showMessage("Ready!")
        return
    
    # class MainWindow(QMainWindow):
    def CALL_GENERATE_XY_LIST_SV_FORMAT(self):
        self.status.showMessage("Ready!")
        self.status.setStyleSheet("color: rgb(255,255,255)")
        
        self.table_tab2.TableWidget = GENERATE_XY_LIST_SV_FORMAT(self.table_tab2.TableWidget, 
                                                                 self.DUT_NAME_LIST, 
                                                                 self.PAD_NUMBER_LIST,
                                                                 self.X, 
                                                                 self.Y, 
                                                                 self.PAD_NAME_LIST, 
                                                                 self.NC_LIST, 
                                                                 self.XY_INPUT_UNIT, 
                                                                 self.NC_DENOTE)
        return
    
    # class MainWindow(QMainWindow):
    def CALL_EXPORT_FILES(self):
        # Reset status
        self.status.showMessage("Ready!")
        self.status.setStyleSheet("color: rgb(255,255,255)")
        
        # Concate variables
        input_parameters = [self.export_all_files,
                            self.export_XY_FORMAT_FOR_IUA_PLUS_file,
                            self.export_ARRAY_FULL_SIZE_FILE_file,
                            self.export_ROBE_HEAD_XY_FILE_file,
                            self.export_PCB_PADS_LOCATION_FILE_file,
                            self.export_IUA_PLUS_FILE_file,
                            self.export_CRD_PLUS_FILE_file
                            ]
        # Call EXPORT_FILES function and get return value
        # status: 1 or 0
        # a tub: true or false for every elements
        status, [self.export_all_files, \
                self.export_XY_FORMAT_FOR_IUA_PLUS_file, \
                self.export_ARRAY_FULL_SIZE_FILE_file, \
                self.export_ROBE_HEAD_XY_FILE_file, \
                self.export_PCB_PADS_LOCATION_FILE_file, \
                self.export_IUA_PLUS_FILE_file, \
                self.export_CRD_PLUS_FILE_file] = EXPORT_FILES(self.table_tab2.TableWidget, input_parameters)
 
        if status == "Run": 
            self.EXPORT_SPEC_FILE()
            self.status.showMessage("Export Done!")     
        else:
            self.status.showMessage(status)
        # end if
        return
    # End of CALL_EXPORT_FILES function

    # class MainWindow(QMainWindow):
    def EXPORT_SPEC_FILE(self):
        # Reset Status
        self.status.showMessage("Ready!")
        if CARD_PART_NUMBER['VALUE#'] != "":
            path = "result/" + CARD_PART_NUMBER['VALUE#'] + "_spec_file.txt"
            with open(path, "w") as f:
                # Add time to SPEC FILE
                now = datetime.now()
                current_time = now.strftime("%b-%d-%Y %H:%M:%S")
                # SPEC file content:
                f.write('OWNER='                    + os.getlogin() + "\n")
                f.write('TIME='                     + current_time + "\n")
                f.write("CARD_PART_NUMBER="         + CARD_PART_NUMBER['VALUE#'] + "\n")
                f.write("CUSTOMER_NAME="            + CUSTOMER_NAME['VALUE'].text() + "\n")
                f.write("XY_INPUT_UNIT="            + self.XY_INPUT_UNIT + "\n")
                f.write("STEPPING_DISTANCE_UNIT="   + self.STEPPING_DISTANCE_UNIT + "\n")
                f.write("PAD_SIZE_UNIT="            + self.PAD_SIZE_UNIT + "\n")
                f.write("DUT_NAME_FORMAT="          + self.DUT_NAME_FORMAT + "\n")
                f.write("DUT_NAME_DELIMITER="       + self.DUT_NAME_DELIMITER + "\n")
                f.write("DUT_NAME_POSITION="        + str(self.DUT_NAME_POSITION) + "\n")
                f.write("PAD_NAME_POSITION="        + str(self.PAD_NAME_POSITION) + "\n")
                f.write("PAD_NUMBER_POSITION="      + str(self.PAD_NUMBER_POSITION) + "\n")
                f.write("XY_Start_Row_Index="       + str(self.XY_Start_Row_Index) + "\n")
                f.write("XY_End_Row_Index="         + str(self.XY_End_Row_Index)   + "\n")
                f.write("Is_PAD_BUMP="              + str(self.Is_PAD_BUMP)       + "\n")
                f.write("NC_POSITION="              + str(self.NC_POSITION)   + "\n")           
                f.write("NC_DEMOTE="                + self.NC_DENOTE          + "\n")      
                f.write("KEEP_OUT_TYPE="            + self.KEEP_OUT_TYPE      + "\n")  
                f.write("KEEP_OUT_UNIT="            + self.KEEP_OUT_UNIT      + "\n")  
                f.write("DUTY_CYCLE_TYPE="          + self.DUTY_CYCLE_TYPE    + "\n")
        else:
            self.status.showMessage("No Card Number!")
            return

    # class MainWindow(QMainWindow):
    def FINAL_EXPORT(self):
        self.status.showMessage("Ready!")
        # Check before final exporting #
        # ...code here...#

        # self.CALL_EXPORT_FILES()
        # self.EXPORT_SPEC_FILE()
        self.status.showMessage("Final Export Done!")
        self.status.setStyleSheet("color: rgb(255,255,255)")

    # class MainWindow(QMainWindow):
    def CALL_DIE_PATTERN(self):
        Stepping_distance = [STEPPING_DISTANCE["X"], STEPPING_DISTANCE["Y"]]

        self.X_list_pattern, self.Y_list_pattern = DIE_PATTERN(self.X, self.Y, self.DIE_CONFIG, Stepping_distance)
    # end of CALL_DIE_PATTERN function
    
    def EXIT_APP(self):
        self.status.showMessage("Bye")
        self.close()
        return

    # class MainWindow(QMainWindow):
    # this function is enable while the right button mouse was clicked on main window area
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet('''
                            QMenu{
                                background-color: rgba(255, 255, 255, 0.1);
                                color: rgb(255, 255, 255);
                            }
                            QMenu::item:selected{
                                background-color: rgba(255,150,0,0.9);
                                color: rgb(255, 255, 255);
                            } 
                            ''')
        menu.addAction(self.createChartAction)
        menu.addAction(self.setDataInfoAction)
        menu.addAction(self.generate_tab2_Action)
        menu.addAction(self.die_pattern_Action)
        menu.addAction(self.exportAction)
        menu.addAction(self.final_export_Action)
        menu.exec_(event.globalPos())
    # End of contextMenuEvent function
# End of Main Window class #

class Tab_Widget(QWidget): 
    def __init__(self, parent, table, CHART, toolbar):
        super(QWidget, self).__init__(parent)
        
        self.X, self.Y = [], []
        self.table = table
        self.CHART = CHART
        self.toolbar = toolbar
        
        # Initialize tabs
        self.TABs = QTabWidget()

        # Create Tab object
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # Create Tab 1 elements    
        self.table_tab1 = QVBoxLayout()
        self.chart_tab1 = QVBoxLayout()

        # Add TABs
        self.TABs.addTab(self.tab1,"Customer data")
        self.TABs.addTab(self.tab2, "Probe head XY")
        self.TABs.addTab(self.tab3, "Folder Tree")

        # Set front for Tab item
        self.tab1.setFont(QFont("3ds", 8))
        self.tab2.setFont(QFont("3ds", 8))
        self.tab3.setFont(QFont("3ds", 8))
        
        self.Setup()

    def Setup(self):
        # Create table in Tab 1
        self.table_tab1.addWidget(self.table)
        
        # Show scatter chart on Tab 1
        self.chart_tab1.addWidget(self.toolbar)
        self.chart_tab1.addWidget(self.CHART)

        # Table in left side of Tab 1
        left_frame_tab1 = QFrame()
        left_frame_tab1.setFrameShape(QFrame.StyledPanel)
        left_frame_tab1.setLayout(self.table_tab1)
        left_frame_tab1.setMinimumWidth(200)
       
        # Chart in right side of Tab 1
        right_frame_tab1 = QFrame()
        right_frame_tab1.setFrameShape(QFrame.StyledPanel)
        right_frame_tab1.setLayout(self.chart_tab1)

        # Add splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_frame_tab1)
        splitter.addWidget(right_frame_tab1)
        
        # Create a Vertical layout
        table_and_xy_chart = QVBoxLayout()
        table_and_xy_chart.addWidget(splitter)

        # Set Tab 1 layout
        self.tab1.setLayout(table_and_xy_chart)
        
    # class Tab_Widget(QWidget): 
    def Return(self):
        return self.TABs

    def Folder_Tree(path, TreeWidget):
        return
# End of Tab class #

class Chart(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor('None')
        self.fig.patch.set_alpha(0)
        super(Chart, self).__init__(self.fig)
# End of Chart class 

# Start of TableWindow class #
class TableWindow(QWidget):
    def __init__(self, NumRow=0, NumCol=0):
        super().__init__()

        self.TableWidget = QTableWidget(self)
        self.NumRow = NumRow
        self.NumCol = NumCol

        self.CreateTable()
        self.vBox = QVBoxLayout()
        self.vBox.addWidget(self.TableWidget)
        self.setLayout(self.vBox)
        self.show()

    # class TableWindow(QWidget):
    def CreateTable(self):

        # Create table with numer of row and column
        self.TableWidget.setRowCount(self.NumRow)
        self.TableWidget.setColumnCount(self.NumCol)

        # Set column and row size
        [self.TableWidget.setColumnWidth(i, 20) for i in range(self.NumCol)]
        [self.TableWidget.setRowHeight(i, 5) for i in range(self.NumRow)]

    
    # class TableWindow(QWidget):
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        
        if event.key() == Qt.Key_C and(event.modifiers() & Qt.ControlModifier):
            self.copied_cells = sorted(self.TableWidget.selectedIndexes())
        
        elif event.key() == Qt.Key_V and(event.modifiers() & Qt.ControlModifier):
            r = self.currentRow() - self.copied_cells[0].row()
            c = self.currentColumn() - self.copied_cells[0].column()
            [self.setItem(cell.row() + r, cell.column() + c, QTableWidgetItem(cell.data())) for cell in self.copied_cells]
# End of TableWindow class #

class ASK_UNIT(QDialog):
    def __init__(self, remember, unit):
        super().__init__()

        self.unit = unit
        self.ASK_UNIT_Remember_unit = remember

        self.setWindowTitle("What is input data unit?")
        self.setFont(QFont("3ds", 12))
        blur(self.winId())

        # Set framless window
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("background-color:   rgba(50,50,50,0.2);"
                            "border:            1px solid white;"
                            "border-radius:     10px;")
        
        # Create OK and Cancel button
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)

        self.Remember_UNIT_box = QCheckBox("Don't show again")
        self.Remember_UNIT_box.setChecked(self.ASK_UNIT_Remember_unit)

        self.radiobutton_mm = QRadioButton("mm")
        if self.unit == MM_UNIT:
            self.radiobutton_mm.setChecked(True)

        self.radiobutton_um = QRadioButton("um")
        if self.unit == UM_UNIT:
            self.radiobutton_um.setChecked(True)

        self.radiobutton_mil = QRadioButton("mil")
        if self.unit == MIL_UNIT:
            self.radiobutton_mil.setChecked(True)

        self.radiobutton_mm.setStyleSheet(RADIO_BUTTON_STYLE_SHEET)
        self.radiobutton_um.setStyleSheet(RADIO_BUTTON_STYLE_SHEET)
        self.radiobutton_mil.setStyleSheet(RADIO_BUTTON_STYLE_SHEET)
    
        ask_unit_title = QLabel("Set input data unit: ")
        ask_unit_title.setStyleSheet("color:            rgb(255,255,255);"
                                    "background-color:  rgba(0,0,0,0);"
                                    "border:            0px;"
                                    "font:              12px 3ds")
        
        self.Remember_UNIT_box.setStyleSheet("color:            rgb(255,255,255);"
                                            "background-color:  rgba(0,0,0,0);"
                                            "border:            0px;"
                                            "font:              12px 3ds;")
    
        self.radiobutton_mm.toggled.connect(self.radiobutton_mm_Clicked)
        self.radiobutton_um.toggled.connect(self.radiobutton_um_Clicked)
        self.radiobutton_mil.toggled.connect(self.radiobutton_mil_Clicked)
        
        self.Remember_UNIT_box.toggled.connect(self.Remember_UNIT_box_Clicked)    
        
        # Set function for buttons
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        option_layout = QHBoxLayout()
        option_layout.addWidget(self.radiobutton_mm)
        option_layout.addWidget(self.radiobutton_um)
        option_layout.addWidget(self.radiobutton_mil)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(ask_unit_title)
        self.layout.addLayout(option_layout)
        self.layout.addWidget(self.Remember_UNIT_box)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)
        self.show()
        self.exec_()

    # class ASK_UNIT(QDialog):
    def radiobutton_mm_Clicked(self):
        self.unit = MM_UNIT
        return

    # class ASK_UNIT(QDialog):
    def radiobutton_um_Clicked(self):
        self.unit = UM_UNIT
        return

    # class ASK_UNIT(QDialog):
    def radiobutton_mil_Clicked(self):
        self.unit = MIL_UNIT
        return

    # class ASK_UNIT(QDialog):
    def Remember_UNIT_box_Clicked(self):
        self.ASK_UNIT_Remember_unit = not self.ASK_UNIT_Remember_unit
        return

    # class ASK_UNIT(QDialog):
    def Return_Unit(self):
        return self.unit, self.ASK_UNIT_Remember_unit
# End of ASK_UNIT class

class SheetsNameDialog(QDialog):
    def __init__(self, items_list):
        super().__init__()
        # variable to get item name in sheets list
        self.item = ""
        self.unit = MM_UNIT
        # Set window title
        self.setWindowTitle("Information")
        
        # Set blur effect
        blur(self.winId())

        # Set framless window
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("background-color:   rgba(50,50,50,0.2);"
                            "border:            1px solid white;"
                            "border-radius:     10px;")

        # Create OK and Cancel button
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)

        # Set function for buttons
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Create content in dialog
        self.layout = QVBoxLayout()
        self.listwidget = QListWidget()
        self.listwidget.setStyleSheet(SheetsNameDialog_listwidget_StyleSheet)

        self.listwidget.itemClicked.connect(self.Selected_item)

        # Add sheets name to list widget 
        [self.listwidget.addItem(i) for i in items_list]

        # Label
        message = QLabel("Please choose sheet to import and press OK:")
        message.setStyleSheet("QLabel{"
                                "color: rgb(255,255,255);" 
                                "background-color: rgba(0,0,0,0);"
                                "border: 0px;}")
        message.setFont(QFont("3ds", 12))
        
        self.layout.addWidget(message)
        self.layout.addWidget(self.listwidget)
        self.layout.addWidget(self.buttonBox)

        # Set layout
        self.setLayout(self.layout)
    # End of __init__() function

    # class SheetsNameDialog(QDialog):
    def Selected_item(self,item):
        self.item = item.text()
        return

    # class SheetsNameDialog(QDialog):
    def Return(self):
        return self.item
# End if Dialog class #

def IMPORT_EXCEL2TABLE(object_, path="", extension=""):
    # Get sheets name in excel file
    sheet_names = pd.ExcelFile(path).sheet_names
    # Call List Dialog to choose sheet need be imported
    dialog = SheetsNameDialog(sheet_names)
    dialog.show()
    dialog.exec_()

    if dialog.Return() == "": # If Sheet Name is empty
        return 0, ""

    # Read excel data
    df = pd.read_excel(io=path, sheet_name=dialog.Return(), engine=None)
    if df.size == 0:
        return 0, ""

    df.fillna("", inplace=True)

    # Set number of row and column same as exel file
    object_.setRowCount(df.shape[0]+1)
    object_.setColumnCount(df.shape[1])

    [object_.setColumnWidth(i, 60) for i in range(df.shape[1])]
    [object_.setRowHeight(i, 5) for i in range(df.shape[0])]
    
    [object_.setItem(0, col, QTableWidgetItem(str(df.columns[col]))) for col in range(object_.columnCount())]
    
    [[object_.setItem(row+1, col, QTableWidgetItem(str(df.iloc[row, col]))) for col in range(object_.columnCount())] for row in range(object_.rowCount()-1)]
    
    # Return value
    return 1, dialog.Return()
# End of IMPORT_EXCEL_FILE function #

class GetInfo(QDialog):
    def __init__(self, tub_info):
        super().__init__()
        # a tub include "0.pad_number_pos,          1.pad_name_pos,           2.dut_pos,                3.dut_name_format,
        #                4.dut_split,               5.nc_pos,                 6.nc_denote,              7.pad_size_unit,
        #                8.is_pad_bump,             9.bump_dia,               10.pad_x_size,            11.pad_y_size,
        #               12.stepping_distance_unit,  13.stepping_distance_x,   14.stepping_distance_y",  15.customer_name,
        #               16.device_name,             17.space_transformer_type,18.test_temperature,      19.DUTY_CYCLE,
        #               20.max_current,             21.max_frequency,           22. keep_out_type       23. keep_out_unit,
        #               24.keep_out_X_size,         25.keep_out_Y_size,         26. keep_out_diameter   27. current_unit,
        #               28. frequency_unit,         29. wafer_material          30. probe_part_number   31. card_part_number,
        #               32.die_config
        # Get input value
        self.pad_number_pos             = tub_info[0]
        if self.pad_number_pos >= 0:    self.pad_number_pos += 1

        self.pad_name_pos               = tub_info[1]
        if self.pad_name_pos >= 0:      self.pad_name_pos += 1 

        self.dut_pos                    = tub_info[2]
        if self.dut_pos >= 0:           self.dut_pos += 1 

        self.dut_name_format            = tub_info[3]
        self.dut_split = tub_info[4]

        self.nc_pos = tub_info[5]
        if self.nc_pos >= 0:            self.nc_pos += 1 

        self.nc_denote                  = tub_info[6]
        self.Pad_size_unit              = tub_info[7]
        self.is_pad_bump                = tub_info[8]
        self.bump_dia                   = tub_info[9]
        self.pad_x_size                 = tub_info[10]
        self.pad_y_size                 = tub_info[11]
        self.stepping_distance_unit     = tub_info[12]
        self.stepping_distance_x        = tub_info[13]
        self.stepping_distance_y        = tub_info[14]
        self.customer_name              = tub_info[15]
        self.device_name                = tub_info[16]
        self.space_transformer_type     = tub_info[17]
        self.test_temperature           = tub_info[18]
        self.duty_cycle                 = tub_info[19]
        self.max_current                = tub_info[20]
        self.max_frequency              = tub_info[21]
        self.keep_out_type              = tub_info[22]
        self.keep_out_unit              = tub_info[23]
        self.keep_out_X_size            = tub_info[24]
        self.keep_out_Y_size            = tub_info[25]
        self.keep_out_diameter          = tub_info[26]
        self.current_unit               = tub_info[27]
        self.frequency_unit             = tub_info[28]
        self.wafer_material             = tub_info[29]
        self.probe_part_number          = tub_info[30]
        self.card_part_number           = tub_info[31]
        
        self.die_config                 = tub_info[32]

        # Dialog Setup
        self.setWindowTitle("Get Info")
        self.setWindowIcon(QIcon('icon/card.png'))
        blur(self.winId())

        # Set framless window
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("background-color:   rgba(50,50,50,0.2);"
                            "border:            1px solid white;"
                            "border-radius:     10px;")
        # Create content
        title = QLabel("Get info")
        title.setStyleSheet(GET_INFO_ON_DIALOG)
        
        # Create lables on dialog
        CARD_PART_NUMBER_LABEL_ON_DIALOG        = QLabel("Card Part Number")
        CUSTOMER_LABEL_ON_DIALOG                = QLabel("Customer")
        DEVICE_LABEL_ON_DIALOG                  = QLabel("Device")
        SPACE_TRANSFORMER_TYPE_ON_DIALOG        = QLabel("Space transformer type")
        
        PAD_NUMBER_LABEL_ON_DIALOG              = QLabel("Pad# position")
        PAD_NAME_LABEL_ON_DIALOG                = QLabel("Pad Name position")
        
        DUT_LABEL_ON_DIALOG                     = QLabel("Die/Site position")
        DUT_NAME_DELIMITER_BY_LABEL_ON_DIALOG   = QLabel("Split by: ")
        
        NC_INFO_LABEL_ON_DIALOG                 = QLabel("NC position")
        
        PAD_TYPE_LABEL_ON_DIALOG                = QLabel("PAD size/type")
        PAD_BUMP_DIAMETER_LABEL_ON_DIALOG       = QLabel("Pad Bump Dia")
        PAD_X_SIZE_LABEL_ON_DIALOG              = QLabel("Pad size in X")
        PAD_Y_SIZE_LABEL_ON_DIALOG              = QLabel("Pad size in Y")
        
        KEEP_OUT_INFOMATION_LABEL_ON_DIALOG     = QLabel("Keep out shape/size")
        KEEP_OUT_RECTANGLE_X_SIZE_LABEL         = QLabel("Keep out size in X")
        KEEP_OUT_RECTANGLE_Y_SIZE_LABEL         = QLabel("Keep out size in Y")
        KEEP_OUT_DIAMETER_LABEL                 = QLabel("Keep out diameter")
        
        TEST_TEMPERATURE_LABEL_ON_DIALOG        = QLabel("Test temperature (°C)")
        
        DUTY_CYCLE_LABEL_ON_DIALOG              = QLabel("Duty Cycle")
        
        MAX_CURRENT_LABEL_ON_DIALOG             = QLabel("Max. Current")
        MAX_FREQUENCY_LABEL_ON_DIALOG           = QLabel("Max. Frequency")
        
        WAFER_PAD_MATERIAL_LABEL_ON_DIALOG      = QLabel("Wafer pad material")
        PROBE_PART_NUMBER_LABEL_ON_DIALOG       = QLabel("Probe No.")

        # Image for pad type
        pixmap_bump_size                        = QPixmap("icon/circle.png")
        pixmap_bump_size                        = pixmap_bump_size.scaled(30, 30)
        pixmap_pad_size                         = QPixmap("icon/square.png")
        pixmap_pad_size                         = pixmap_pad_size.scaled(30, 30)
        
        self.bump_size_img_on_dialog            = QLabel(self)
        self.bump_size_img_on_dialog.setPixmap(pixmap_bump_size)
        
        self.pad_size_img_on_dialog             = QLabel(self)
        self.pad_size_img_on_dialog.setPixmap(pixmap_pad_size)
        
        self.Pad_Type_Checkbox                  = QCheckBox("Wafer Bump type")
        
        STEPPING_DISTANCE_LABEL                 = QLabel("Stepping distance")
        STEPPING_DISTANCE_IMG                   = QLabel(self)
        pixmap_stepping_distance                = QPixmap("icon/cartesian.png")
        pixmap_stepping_distance                = pixmap_stepping_distance.scaled(70, 70)
        STEPPING_DISTANCE_IMG.setPixmap(pixmap_stepping_distance)
        
        self.CARD_PART_NUMBER_Textbox           = QLineEdit()
        if self.card_part_number != "":         self.CARD_PART_NUMBER_Textbox.setText(self.card_part_number)

        self.CUSTOMER_Textbox                   = QLineEdit()
        if self.customer_name != "":            self.CUSTOMER_Textbox.setText(self.customer_name)

        self.DEVICE_Textbox                     = QLineEdit()
        if self.device_name != "":              self.DEVICE_Textbox.setText(self.device_name)

        self.SPACE_TRANSFORMER_Textbox          = QLineEdit()
        if self.space_transformer_type != "":   self.SPACE_TRANSFORMER_Textbox.setText(self.space_transformer_type) 

        self.PAD_NUMBER_POSITION_Textbox        = QLineEdit()
        if self.pad_number_pos >= 0:            self.PAD_NUMBER_POSITION_Textbox.setText(str(self.pad_number_pos)) 
        
        self.PAD_NAME_POSITION_Textbox          = QLineEdit()
        if self.pad_name_pos >= 0:              self.PAD_NAME_POSITION_Textbox.setText(str(self.pad_name_pos))

        self.DUT_NAME_FORMAT_Textbox = QLineEdit() # Format: DUT.0; 1, argu 1 is DUT number format, argu 2 is column index7
        if self.dut_name_format != "":          self.DUT_NAME_FORMAT_Textbox.setText(self.dut_name_format)

        self.DUT_NAME_POSITION_Textbox = QLineEdit()
        if self.dut_pos >= 0:                   self.DUT_NAME_POSITION_Textbox.setText(str(self.dut_pos))

        self.DUT_NAME_DELIMITER_Textbox = QLineEdit()
        if self.dut_split != "":                self.DUT_NAME_DELIMITER_Textbox.setText(self.dut_split) 
        
        self.NC_POSITION_Textbox = QLineEdit()
        if self.nc_pos >= 0:                    self.NC_POSITION_Textbox.setText(str(self.nc_pos)) 

        self.NC_FILTER_BY_Textbox = QLineEdit()
        if self.nc_denote !="":                 self.NC_FILTER_BY_Textbox.setText(self.nc_denote)

        self.BUMP_DIAMETER_Textbox = QLineEdit()
        if self.bump_dia > 0:                   self.BUMP_DIAMETER_Textbox.setText(str(self.bump_dia))
        
        self.PAD_X_SIZE_Textbox = QLineEdit()
        if self.pad_x_size > 0:                 self.PAD_X_SIZE_Textbox.setText(str(self.pad_x_size))
        
        self.PAD_Y_SIZE_Textbox = QLineEdit()
        if self.pad_y_size > 0:                 self.PAD_Y_SIZE_Textbox.setText(str(self.pad_y_size))
       
        self.TEST_TEMPERATURE_Textbox   = QLineEdit()
        if self.test_temperature != 0.0: 
            self.TEST_TEMPERATURE_Textbox.setText(str(self.test_temperature))

        self.MAX_CURRENT_Textbox= QLineEdit()
        if self.max_current != 0.0: 
            self.MAX_CURRENT_Textbox.setText(str(self.max_current))

        self.MAX_FREQUENCY_Textbox      = QLineEdit()
        if self.max_frequency != 0.0: 
            self.MAX_FREQUENCY_Textbox.setText(str(self.max_frequency))

        self.KEEP_OUT_X_SIZE_Textbox    = QLineEdit()
        if self.keep_out_X_size != 0.0:
            self.KEEP_OUT_X_SIZE_Textbox.setText(str(self.keep_out_X_size))
        
        self.KEEP_OUT_Y_SIZE_Textbox    = QLineEdit()
        if self.keep_out_Y_size != 0.0:
            self.KEEP_OUT_Y_SIZE_Textbox.setText(str(self.keep_out_Y_size))
        
        self.KEEP_OUT_DIAMETER_Textbox    = QLineEdit()
        if self.keep_out_diameter != 0.0:
            self.KEEP_OUT_DIAMETER_Textbox.setText(str(self.keep_out_diameter))

        self.STEP_X_Textbox = QLineEdit()
        self.STEP_Y_Textbox = QLineEdit()
        if self.stepping_distance_x != 0.0:
            self.STEP_X_Textbox.setText(str(self.stepping_distance_x))
        if self.stepping_distance_y != 0.0:
            self.STEP_Y_Textbox.setText(str(self.stepping_distance_y))

        self.WAFER_PAD_MATERIAL_Textbox = QLineEdit()
        if self.wafer_material != "":       self.WAFER_PAD_MATERIAL_Textbox.setText(self.wafer_material)

        self.PROBE_PART_NUMBER_Textbox = QLineEdit()
        if self.probe_part_number != "":    self.PROBE_PART_NUMBER_Textbox.setText(self.probe_part_number)

        self.PAD_SIZE_UNIT_Combo_box = QComboBox()
        self.PAD_SIZE_UNIT_Combo_box.addItem(UM_UNIT)
        self.PAD_SIZE_UNIT_Combo_box.addItem(MM_UNIT)
        self.PAD_SIZE_UNIT_Combo_box.addItem(MIL_UNIT)
        self.PAD_SIZE_UNIT_Combo_box.setCurrentIndex(self.PAD_SIZE_UNIT_Combo_box.findText(self.Pad_size_unit))

        self.STEPPING_DISTANCE_UNIT_Combo_box = QComboBox()
        self.STEPPING_DISTANCE_UNIT_Combo_box.addItem(UM_UNIT)
        self.STEPPING_DISTANCE_UNIT_Combo_box.addItem(MM_UNIT)
        self.STEPPING_DISTANCE_UNIT_Combo_box.addItem(MIL_UNIT)
        self.STEPPING_DISTANCE_UNIT_Combo_box.setCurrentIndex(self.STEPPING_DISTANCE_UNIT_Combo_box.findText(self.stepping_distance_unit))
        
        self.KEEP_OUT_TYPE_ComboBox = QComboBox()
        self.KEEP_OUT_TYPE_ComboBox.addItem(KEEP_OUT_TYPE["TYPE"][0])
        self.KEEP_OUT_TYPE_ComboBox.addItem(KEEP_OUT_TYPE["TYPE"][1])
        self.KEEP_OUT_TYPE_ComboBox.setCurrentIndex(self.KEEP_OUT_TYPE_ComboBox.findText(self.keep_out_type))
        
        self.KEEP_OUT_UNIT_ComboBox = QComboBox()
        self.KEEP_OUT_UNIT_ComboBox.addItem(MM_UNIT)
        self.KEEP_OUT_UNIT_ComboBox.addItem(IN_UNIT)
        self.KEEP_OUT_UNIT_ComboBox.setCurrentIndex(self.KEEP_OUT_UNIT_ComboBox.findText(self.keep_out_unit))

        self.DUTY_CYCLE_TYPE_ComboBox = QComboBox()
        self.DUTY_CYCLE_TYPE_ComboBox.addItem(DUTY_CYCLE["TYPE"][0])
        self.DUTY_CYCLE_TYPE_ComboBox.addItem(DUTY_CYCLE["TYPE"][1]) 
        self.DUTY_CYCLE_TYPE_ComboBox.setCurrentIndex(self.DUTY_CYCLE_TYPE_ComboBox.findText(self.duty_cycle))

        self.CURRENT_UNIT_ComboBox  =   QComboBox()
        self.CURRENT_UNIT_ComboBox.addItem(MAX_CURRENT['UNIT'][0])
        self.CURRENT_UNIT_ComboBox.addItem(MAX_CURRENT['UNIT'][1])
        self.CURRENT_UNIT_ComboBox.setCurrentIndex(self.CURRENT_UNIT_ComboBox.findText(self.current_unit))

        self.FREQUENCY_UNIT_ComboBox    = QComboBox()
        self.FREQUENCY_UNIT_ComboBox.addItem(MAX_FREQUENCY['UNIT'][1])
        self.FREQUENCY_UNIT_ComboBox.addItem(MAX_FREQUENCY['UNIT'][0])
        self.FREQUENCY_UNIT_ComboBox.addItem(MAX_FREQUENCY['UNIT'][2])
        self.FREQUENCY_UNIT_ComboBox.setCurrentIndex(self.FREQUENCY_UNIT_ComboBox.findText(self.frequency_unit))

        self.DUT_NAME_POSITION_Textbox.setToolTip("which's column?")
        self.DUT_NAME_FORMAT_Textbox.setToolTip("Ex: DUT.0 or SITE#1")
        self.PAD_NAME_POSITION_Textbox.setToolTip("which's column?")
        self.PAD_NUMBER_POSITION_Textbox.setToolTip("which's column?")
        self.DUT_NAME_DELIMITER_Textbox.setToolTip("Ex: DUT.0 is splited \n by '.' char")
        self.NC_POSITION_Textbox.setToolTip("which's column?")
        self.NC_FILTER_BY_Textbox.setToolTip("what is NC denoted by?")
        self.STEP_X_Textbox.setToolTip("Distance X")
        self.STEP_Y_Textbox.setToolTip("Distance Y")

        CARD_PART_NUMBER_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        CUSTOMER_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        DEVICE_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        SPACE_TRANSFORMER_TYPE_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        KEEP_OUT_INFOMATION_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        TEST_TEMPERATURE_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        DUTY_CYCLE_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        MAX_CURRENT_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        MAX_FREQUENCY_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        PROBE_PART_NUMBER_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        WAFER_PAD_MATERIAL_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)

        DUT_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        DUT_NAME_DELIMITER_BY_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)

        PAD_NAME_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        PAD_NUMBER_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
    
        NC_INFO_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        STEPPING_DISTANCE_LABEL.setStyleSheet(INFO_LABEL_STYLE_SHEET)
    
        PAD_BUMP_DIAMETER_LABEL_ON_DIALOG.setStyleSheet(Pad_type_label_stylesheet)
        PAD_X_SIZE_LABEL_ON_DIALOG.setStyleSheet(Pad_type_label_stylesheet)
        PAD_Y_SIZE_LABEL_ON_DIALOG.setStyleSheet(Pad_type_label_stylesheet)
        PAD_TYPE_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)

        KEEP_OUT_INFOMATION_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        KEEP_OUT_RECTANGLE_X_SIZE_LABEL.setStyleSheet(Pad_type_label_stylesheet)
        KEEP_OUT_RECTANGLE_Y_SIZE_LABEL.setStyleSheet(Pad_type_label_stylesheet)
        KEEP_OUT_DIAMETER_LABEL.setStyleSheet(Pad_type_label_stylesheet)
        TEST_TEMPERATURE_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        DUTY_CYCLE_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        MAX_CURRENT_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
        MAX_FREQUENCY_LABEL_ON_DIALOG.setStyleSheet(INFO_LABEL_STYLE_SHEET)
                        
        self.bump_size_img_on_dialog.setStyleSheet(small_img_StyleSheet)
        self.pad_size_img_on_dialog.setStyleSheet(small_img_StyleSheet)
        
        STEPPING_DISTANCE_IMG.setStyleSheet(small_img_StyleSheet)

        self.Pad_Type_Checkbox.setStyleSheet("color:            white;"
                                            "font:              12px 3ds;"
                                            "background-color:  transparent;"
                                            "border:            0px;")
                                
        self.DUT_NAME_FORMAT_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        self.DUT_NAME_POSITION_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        self.DUT_NAME_DELIMITER_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)     

        self.PAD_NAME_POSITION_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        self.PAD_NUMBER_POSITION_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)                  
        
        self.NC_POSITION_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        self.NC_FILTER_BY_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)     
        
        self.PAD_SIZE_UNIT_Combo_box.setStyleSheet(Unit_combo_box_style_sheet)
        
        self.STEPPING_DISTANCE_UNIT_Combo_box.setStyleSheet(Unit_combo_box_style_sheet)
        self.STEP_X_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        self.STEP_Y_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        
        self.CARD_PART_NUMBER_Textbox.setStyleSheet(CARD_PART_NUMBER_TEXTBOX_STYLE_SHEET)
        self.CUSTOMER_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        self.DEVICE_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        self.SPACE_TRANSFORMER_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        self.TEST_TEMPERATURE_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        self.MAX_CURRENT_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        self.MAX_FREQUENCY_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        
        self.KEEP_OUT_TYPE_ComboBox.setStyleSheet(Unit_combo_box_style_sheet)
        self.KEEP_OUT_UNIT_ComboBox.setStyleSheet(Unit_combo_box_style_sheet)

        self.DUTY_CYCLE_TYPE_ComboBox.setStyleSheet(Unit_combo_box_style_sheet)
        self.CURRENT_UNIT_ComboBox.setStyleSheet(Unit_combo_box_style_sheet)
        self.FREQUENCY_UNIT_ComboBox.setStyleSheet(Unit_combo_box_style_sheet)

        self.PROBE_PART_NUMBER_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)
        self.WAFER_PAD_MATERIAL_Textbox.setStyleSheet(INFO_TEXTBOX_STYLE_SHEET)

        # Set up for Pad_Type_Checkbox
        self.Pad_Type_Checkbox.setChecked(self.is_pad_bump) # Update Pad_Type_Checkbox status
        self.Pad_Type_Checkbox.stateChanged.connect(self.PAD_BUMP_CHECKBOX_STATE)

        if self.is_pad_bump == True: # if pad type is BUMP
            self.BUMP_DIAMETER_Textbox.setReadOnly(False) # Active BUMP_DIAMETER_Textbox
            self.PAD_X_SIZE_Textbox.setReadOnly(True)
            self.PAD_Y_SIZE_Textbox.setReadOnly(True)

            self.BUMP_DIAMETER_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet)
            self.PAD_X_SIZE_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)
            self.PAD_Y_SIZE_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)  

            self.bump_size_img_on_dialog.setVisible(True)
            self.pad_size_img_on_dialog.setVisible(False)
        else: # if pad type is FLAT
            self.BUMP_DIAMETER_Textbox.setReadOnly(True)
            self.PAD_X_SIZE_Textbox.setReadOnly(False)  # Active PAD_X_SIZE_Textbox
            self.PAD_Y_SIZE_Textbox.setReadOnly(False)  # Active PAD_Y_SIZE_Textbox

            self.BUMP_DIAMETER_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)  
            self.PAD_X_SIZE_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet)  
            self.PAD_Y_SIZE_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet) 

            self.bump_size_img_on_dialog.setVisible(False)
            self.pad_size_img_on_dialog.setVisible(True)
        
        # End: Set up for Pad_Type_Checkbox
        if self.KEEP_OUT_TYPE_ComboBox.currentText() == KEEP_OUT_TYPE["TYPE"][0]:
            self.KEEP_OUT_X_SIZE_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet)
            self.KEEP_OUT_Y_SIZE_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet)
            self.KEEP_OUT_DIAMETER_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)
            self.KEEP_OUT_X_SIZE_Textbox.setVisible(True)
            self.KEEP_OUT_Y_SIZE_Textbox.setVisible(True)
            self.KEEP_OUT_DIAMETER_Textbox.setVisible(False)
        else:
            self.KEEP_OUT_X_SIZE_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)
            self.KEEP_OUT_Y_SIZE_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)
            self.KEEP_OUT_DIAMETER_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet)
            self.KEEP_OUT_X_SIZE_Textbox.setVisible(False)
            self.KEEP_OUT_Y_SIZE_Textbox.setVisible(False)
            self.KEEP_OUT_DIAMETER_Textbox.setVisible(True)

        self.KEEP_OUT_TYPE_ComboBox.currentTextChanged.connect(self.KEEP_OUT_TYPE_CHANGE_STATE)

        # Table for Die Configuration
        self.rowCount = 5
        self.columnCount = 5

        if self.die_config.shape != (0,):
            self.rowCount = self.die_config.shape[0]
            self.columnCount = self.die_config.shape[1]

        self.TableRowCount  = QSpinBox(self)
        self.TableColumnCount  = QSpinBox(self)
        self.TableRowCount.setValue(self.rowCount)
        self.TableColumnCount.setValue(self.columnCount)
        self.TableRowCount.setStyleSheet(Die_config_spin_box_style_sheet)
        self.TableColumnCount.setStyleSheet(Die_config_spin_box_style_sheet)

        self.TableRowCount.valueChanged.connect(self.updateTableRowCount)
        self.TableColumnCount.valueChanged.connect(self.updateTableColumnCount)

        self.die_config_tableWidget = QTableWidget()

        self.die_config_tableWidget.setRowCount(self.rowCount)
        self.die_config_tableWidget.setColumnCount(self.columnCount)

        [self.die_config_tableWidget.setColumnWidth(i, 10) for i in range(self.columnCount)]
        [self.die_config_tableWidget.setRowHeight(i, 10) for i in range(self.rowCount)]

        tableWidget_dialog_label = QLabel('Die Configuration: ')
        tableWidget_dialog_label.setStyleSheet("""QLabel{
                                                    color:                  white;
                                                    font:                  15px 3ds;
                                                    background-color:      transparent;
                                                    border:                0px;
                                                    qproperty-alignment: 'AlignVCenter | AlignLeft';
                                                }""")

        self.die_config_tableWidget.setStyleSheet(Die_config_TableWidget_stylesheet)
        self.die_config_tableWidget_update_value()

        # Create Layout
        self.Glayout = QGridLayout()
        self.Glayout.addWidget(CARD_PART_NUMBER_LABEL_ON_DIALOG,0,0)
        self.Glayout.addWidget(self.CARD_PART_NUMBER_Textbox,0,1)

        self.Glayout.addWidget(CUSTOMER_LABEL_ON_DIALOG,1,0)
        self.Glayout.addWidget(self.CUSTOMER_Textbox,1,1)

        self.Glayout.addWidget(PROBE_PART_NUMBER_LABEL_ON_DIALOG, 1,3)
        self.Glayout.addWidget(self.PROBE_PART_NUMBER_Textbox, 1,4)

        self.Glayout.addWidget(DEVICE_LABEL_ON_DIALOG,2,0)
        self.Glayout.addWidget(self.DEVICE_Textbox,2,1)

        self.Glayout.addWidget(PAD_NUMBER_LABEL_ON_DIALOG,3,0)
        self.Glayout.addWidget(self.PAD_NUMBER_POSITION_Textbox,3,1)
        
        self.Glayout.addWidget(PAD_NAME_LABEL_ON_DIALOG,4,0)
        self.Glayout.addWidget(self.PAD_NAME_POSITION_Textbox,4,1)
        
        self.Glayout.addWidget(DUT_LABEL_ON_DIALOG,5,0)
        self.Glayout.addWidget(self.DUT_NAME_POSITION_Textbox,5,1)
        self.Glayout.addWidget(self.DUT_NAME_FORMAT_Textbox,5,2)
        self.Glayout.addWidget(DUT_NAME_DELIMITER_BY_LABEL_ON_DIALOG,5,3)
        self.Glayout.addWidget(self.DUT_NAME_DELIMITER_Textbox,5,4)

        self.Glayout.addWidget(NC_INFO_LABEL_ON_DIALOG,6,0)
        self.Glayout.addWidget(self.NC_POSITION_Textbox,6,1)
        self.Glayout.addWidget(self.NC_FILTER_BY_Textbox,6,2)

        self.Glayout.addWidget(PAD_TYPE_LABEL_ON_DIALOG,7,0)
        self.Glayout.addWidget(self.PAD_SIZE_UNIT_Combo_box,7,1)
        self.Glayout.addWidget(self.Pad_Type_Checkbox,7,2)

        self.Glayout.addWidget(WAFER_PAD_MATERIAL_LABEL_ON_DIALOG,7,3)
        self.Glayout.addWidget(self.WAFER_PAD_MATERIAL_Textbox,7,4)
      
        self.Glayout.addWidget(PAD_BUMP_DIAMETER_LABEL_ON_DIALOG,8,0)
        self.Glayout.addWidget(self.BUMP_DIAMETER_Textbox,8,1)
        self.Glayout.addWidget(self.bump_size_img_on_dialog, 8, 2)
 
        self.Glayout.addWidget(PAD_X_SIZE_LABEL_ON_DIALOG,9,0)
        self.Glayout.addWidget(self.PAD_X_SIZE_Textbox,9,1)
        self.Glayout.addWidget(self.pad_size_img_on_dialog, 9, 2)
        self.Glayout.addWidget(PAD_Y_SIZE_LABEL_ON_DIALOG,10,0)
        self.Glayout.addWidget(self.PAD_Y_SIZE_Textbox,10,1)

        self.Glayout.addWidget(STEPPING_DISTANCE_LABEL, 11,0)
        self.Glayout.addWidget(self.STEPPING_DISTANCE_UNIT_Combo_box, 11,1)
        self.Glayout.addWidget(self.STEP_Y_Textbox, 12,1)
        self.Glayout.addWidget(STEPPING_DISTANCE_IMG, 11,2)
        self.Glayout.addWidget(self.STEP_X_Textbox, 13,2)

        self.Glayout.addWidget(KEEP_OUT_INFOMATION_LABEL_ON_DIALOG,14,0)
        self.Glayout.addWidget(KEEP_OUT_DIAMETER_LABEL,15,0)
        self.Glayout.addWidget(KEEP_OUT_RECTANGLE_X_SIZE_LABEL,16,0)
        self.Glayout.addWidget(KEEP_OUT_RECTANGLE_Y_SIZE_LABEL,17,0)
        self.Glayout.addWidget(self.KEEP_OUT_DIAMETER_Textbox, 15,1)
        self.Glayout.addWidget(self.KEEP_OUT_X_SIZE_Textbox, 16,1)
        self.Glayout.addWidget(self.KEEP_OUT_Y_SIZE_Textbox, 17,1)
        self.Glayout.addWidget(self.KEEP_OUT_TYPE_ComboBox,14,1)
        self.Glayout.addWidget(self.KEEP_OUT_UNIT_ComboBox, 14,2)
        
        self.Glayout.addWidget(TEST_TEMPERATURE_LABEL_ON_DIALOG,18,0)
        self.Glayout.addWidget(self.TEST_TEMPERATURE_Textbox,18,1)
        
        self.Glayout.addWidget(DUTY_CYCLE_LABEL_ON_DIALOG,19,0)
        self.Glayout.addWidget(self.DUTY_CYCLE_TYPE_ComboBox,19,1)

        self.Glayout.addWidget(MAX_CURRENT_LABEL_ON_DIALOG,20,0)
        self.Glayout.addWidget(self.MAX_CURRENT_Textbox,20,1)
        self.Glayout.addWidget(self.CURRENT_UNIT_ComboBox,20,2)

        self.Glayout.addWidget(MAX_FREQUENCY_LABEL_ON_DIALOG,21,0)
        self.Glayout.addWidget(self.MAX_FREQUENCY_Textbox,21,1)
        self.Glayout.addWidget(self.FREQUENCY_UNIT_ComboBox,21,2)

        self.Vlayout = QVBoxLayout()
        self.HLayout = QHBoxLayout()
        row_label    = QLabel("row:")
        col_label    = QLabel("col:")
        row_label.setStyleSheet("color:rgb(255,255,255);"
                                "background-color:  rgba(0,0,0,0);"
                                "border: 0px")
        col_label.setStyleSheet("color:rgb(255,255,255);"
                                "background-color:  rgba(0,0,0,0);"
                                "border: 0px")
        self.HLayout.addWidget(tableWidget_dialog_label)
        self.HLayout.addStretch(1)
        self.HLayout.addWidget(row_label)
        self.HLayout.addWidget(self.TableRowCount)
        self.HLayout.addWidget(col_label)
        self.HLayout.addWidget(self.TableColumnCount)
        self.Vlayout.addLayout(self.Glayout)
        self.Vlayout.addLayout(self.HLayout)
        self.Vlayout.addWidget(self.die_config_tableWidget)
        groupBox = QGroupBox()
        groupBox.setStyleSheet("""QGroupBox{
                                            border: 0px;
                                            background-color: rgba(0,0,0,0);
                                        }""")
        groupBox.setLayout(self.Vlayout)
        # End of self.Glayout

        # Create OK button
        QBtn = QDialogButtonBox.Ok
        buttonBox = QDialogButtonBox(QBtn)

        QBtn_reset = QDialogButtonBox.Reset
        reset_buttonBox = QDialogButtonBox(QBtn_reset)
                            
        # Set function for buttons
        buttonBox.accepted.connect(self.accept)
        reset_buttonBox.clicked.connect(self.Reset_button_clicked)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_buttonBox)
        button_layout.addStretch(1)
        button_layout.addWidget(buttonBox)

        self.resize(930, 900)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setStyleSheet("""
                            QScrollArea{
                                border: 0px;
                                background-color: rgba(0,0,0,0);
                            }
                            """)
        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(title)
        self.layout.addWidget(scroll)
        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)
        self.show()
        self.exec_()
    
    def updateTableRowCount(self, value):
        self.die_config_tableWidget.setRowCount(value)
        [self.die_config_tableWidget.setRowHeight(i, 10) for i in range(value)]
        return
    
    def updateTableColumnCount(self, value):
        self.die_config_tableWidget.setColumnCount(value)
        [self.die_config_tableWidget.setColumnWidth(i, 10) for i in range(value)]
        return
    
    def die_config_tableWidget_update_value(self):

        if self.die_config.shape != (0,):
            for i in range(self.die_config_tableWidget.rowCount()):
                for j in range(self.die_config_tableWidget.columnCount()):
                    if self.die_config[i,j] < 0.0:
                        self.die_config_tableWidget.setItem(i,j, QTableWidgetItem(""))
                    else:
                        self.die_config_tableWidget.setItem(i,j, QTableWidgetItem(str(np.uint64(self.die_config[i,j]))))

    # class GetInfo(QDialog):
    def Return(self):
        dut_pos             = self.DUT_NAME_POSITION_Textbox.text()
        dut_name_format     = self.DUT_NAME_FORMAT_Textbox.text()
        pad_num_pos         = self.PAD_NUMBER_POSITION_Textbox.text()
        pad_name_pos        = self.PAD_NAME_POSITION_Textbox.text()
        nc_pos              = self.NC_POSITION_Textbox.text()
        nc_denote           = self.NC_FILTER_BY_Textbox.text()
        customer            = self.CUSTOMER_Textbox.text()
        device              = self.DEVICE_Textbox.text()
        space_transformer   = self.SPACE_TRANSFORMER_Textbox.text()
        keep_out_type       = self.KEEP_OUT_TYPE_ComboBox.currentText()
        keep_out_unit       = self.KEEP_OUT_UNIT_ComboBox.currentText()
        duty_cycle          = self.DUTY_CYCLE_TYPE_ComboBox.currentText()
        wafer_material      = self.WAFER_PAD_MATERIAL_Textbox.text()
        probe_part_number   = self.PROBE_PART_NUMBER_Textbox.text().upper()
        dut_name_delimiter  = self.DUT_NAME_DELIMITER_Textbox.text()
        card_part_number    = self.CARD_PART_NUMBER_Textbox.text().upper()
        
        if pad_num_pos      == "" or pad_num_pos == "0":
            pad_num_pos     = -1
        else:
            pad_num_pos     = np.uint8(pad_num_pos)
            
        if pad_name_pos     == "" or pad_name_pos == "0":
            pad_name_pos    = -1
        else:
            pad_name_pos    = np.uint8(pad_name_pos)
        
        if dut_pos          == "" or dut_pos == "0":
            dut_pos         = -1
        else:
            dut_pos         = np.uint8(dut_pos)

        if nc_pos           == "" or nc_pos == "0":
            nc_pos          = -1
        else:
            nc_pos          = np.uint8(nc_pos)

        return  pad_num_pos, \
                pad_name_pos, \
                dut_name_format, \
                dut_pos, \
                nc_pos, \
                nc_denote, \
                customer, \
                device, \
                space_transformer, \
                keep_out_type, \
                keep_out_unit, \
                duty_cycle, \
                wafer_material, \
                probe_part_number, \
                dut_name_delimiter, \
                card_part_number
               
    # class GetInfo(QDialog):
    def Get_Pad_Size(self): # Return Bump diameter,  pad flat size in X, pad flat size in Y, unit
        # Case 1
        if self.Pad_Type_Checkbox.checkState() == Qt.Unchecked and \
            self.PAD_X_SIZE_Textbox.text()!= "" and \
            self.PAD_Y_SIZE_Textbox.text() != "":
            
            return  np.float16(0.0), \
                    np.float32(self.PAD_X_SIZE_Textbox.text()), \
                    np.float32(self.PAD_Y_SIZE_Textbox.text()), \
                    self.PAD_SIZE_UNIT_Combo_box.currentText()
        # Case 2
        if self.Pad_Type_Checkbox.checkState() == Qt.Checked and \
            self.BUMP_DIAMETER_Textbox.text() != "":

            return  np.float16(self.BUMP_DIAMETER_Textbox.text()), \
                    np.float32(0.0), \
                    np.float32(0.0), \
                    self.PAD_SIZE_UNIT_Combo_box.currentText()
        # Default case
        return  np.float16(0.0), \
                np.float16(0.0), \
                np.float16(0.0), \
                self.PAD_SIZE_UNIT_Combo_box.currentText()

    # class GetInfo(QDialog):
    def PAD_BUMP_CHECKBOX_STATE(self):
        if self.Pad_Type_Checkbox.checkState() == Qt.Checked: # if pad type is Bump
            self.BUMP_DIAMETER_Textbox.setReadOnly(False)     # Disable
            self.PAD_X_SIZE_Textbox.setReadOnly(True)   # Enable
            self.PAD_Y_SIZE_Textbox.setReadOnly(True)   # Enable

            self.BUMP_DIAMETER_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet)
            self.PAD_X_SIZE_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)
            self.PAD_Y_SIZE_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)    

            self.bump_size_img_on_dialog.setVisible(True)   
            self.pad_size_img_on_dialog.setVisible(False)   

            self.is_pad_bump = True           
            
        else: # if pad type is Flat
            self.BUMP_DIAMETER_Textbox.setReadOnly(True)      # Enable
            self.PAD_X_SIZE_Textbox.setReadOnly(False)  # Disable
            self.PAD_Y_SIZE_Textbox.setReadOnly(False)  # Disable

            self.BUMP_DIAMETER_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)  
            self.PAD_X_SIZE_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet)  
            self.PAD_Y_SIZE_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet) 
            
            self.bump_size_img_on_dialog.setVisible(False)    
            self.pad_size_img_on_dialog.setVisible(True)    
        
            self.is_pad_bump = False  
        return

    def KEEP_OUT_TYPE_CHANGE_STATE(self):
        # End: Set up for Pad_Type_Checkbox
        if self.KEEP_OUT_TYPE_ComboBox.currentText() == KEEP_OUT_TYPE["TYPE"][0]:
            self.KEEP_OUT_X_SIZE_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet)
            self.KEEP_OUT_Y_SIZE_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet)
            self.KEEP_OUT_DIAMETER_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)
            self.KEEP_OUT_X_SIZE_Textbox.setVisible(True)
            self.KEEP_OUT_Y_SIZE_Textbox.setVisible(True)
            self.KEEP_OUT_DIAMETER_Textbox.setVisible(False)

        else:
            self.KEEP_OUT_X_SIZE_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)
            self.KEEP_OUT_Y_SIZE_Textbox.setStyleSheet(Pad_Size_Disable_styleSheet)
            self.KEEP_OUT_DIAMETER_Textbox.setStyleSheet(Pad_Size_Enable_styleSheet)
            self.KEEP_OUT_X_SIZE_Textbox.setVisible(False)
            self.KEEP_OUT_Y_SIZE_Textbox.setVisible(False)
            self.KEEP_OUT_DIAMETER_Textbox.setVisible(True)
        return

    # class GetInfo(QDialog):
    def Get_Bump_Type(self):
        return self.is_pad_bump

    # class GetInfo(QDialog):
    def Get_Stepping_distance_unit(self):
        return self.STEPPING_DISTANCE_UNIT_Combo_box.currentText()
    
    # class GetInfo(QDialog):
    def Get_Stepping_distance(self):
        step_x = self.STEP_X_Textbox.text()
        step_y = self.STEP_Y_Textbox.text()
        
        if step_x.replace('.', '', 1).isdigit():
            step_x = np.float32(step_x)
        else:
            step_x = 0.0

        if step_y.replace('.', '', 1).isdigit():
            step_y = np.float32(step_y)
        else:
            step_y = 0.0

        return step_x, step_y
    
    # class GetInfo(QDialog):
    def Get_Keep_out_size(self):
        keep_out_x_size = self.KEEP_OUT_X_SIZE_Textbox.text()
        keep_out_y_size = self.KEEP_OUT_Y_SIZE_Textbox.text()
        keep_out_diameter_size = self.KEEP_OUT_DIAMETER_Textbox.text()
        
        if keep_out_x_size.replace('.', '', 1).isdigit() and self.KEEP_OUT_TYPE_ComboBox.currentText() == KEEP_OUT_TYPE['TYPE'][0]:
            keep_out_x_size = np.float32(keep_out_x_size)
        else:
            keep_out_x_size = 0.0

        if keep_out_y_size.replace('.', '', 1).isdigit() and self.KEEP_OUT_TYPE_ComboBox.currentText() == KEEP_OUT_TYPE['TYPE'][0]:
            keep_out_y_size = np.float32(keep_out_y_size)
        else:
            keep_out_y_size = 0.0

        if keep_out_diameter_size.replace('.', '', 1).isdigit() and self.KEEP_OUT_TYPE_ComboBox.currentText() == KEEP_OUT_TYPE['TYPE'][1]:
            keep_out_diameter_size = np.float32(keep_out_diameter_size)
        else:
            keep_out_diameter_size = 0.0
        
        return keep_out_x_size, keep_out_y_size, keep_out_diameter_size
    
    # class GetInfo(QDialog):
    def Get_Config_Array(self):

        table       = self.die_config_tableWidget
        rowCount    = table.rowCount()
        colCount    = table.columnCount()

        config = np.empty((rowCount, colCount), dtype = np.float64)

        for i in range(rowCount):
            for j in range(colCount):
                if table.item(i,j) is None:
                    config[i,j] = -1.0
                else:
                    if table.item(i,j).text() == "":
                        config[i,j] = -1.0
                    else:
                        if np.float64(table.item(i,j).text()) <= -1.0:
                            config[i,j] = -1.0
                        else:
                            config[i,j] = np.uint64(np.float64(table.item(i,j).text()))     

        return config # a numpy array type fit value size
    
    # class GetInfo(QDialog):
    def other(self):
        test_temp           = self.TEST_TEMPERATURE_Textbox.text()
        max_current         = self.MAX_CURRENT_Textbox.text()
        max_frequency       = self.MAX_FREQUENCY_Textbox.text()
        current_unit        = self.CURRENT_UNIT_ComboBox.currentText()
        frequency_unit      = self.FREQUENCY_UNIT_ComboBox.currentText()

        if test_temp        == "" or test_temp == "0":
            test_temp       = 0.0
        else:
            test_temp       = np.float16(test_temp)

        if max_current        == "" or max_current == "0":
            max_current       = 0.0
        else:
            if max_current.replace('.', '', 1).isdigit():
                max_current       = np.float16(max_current)
            else:
                max_current       = 0.0

        if max_frequency        == "" or max_frequency == "0":
            max_frequency       = 0.0
        else:
            if max_frequency.replace('.', '', 1).isdigit():
                max_frequency       = np.float16(max_frequency)
            else:
                max_frequency       = 0.0

        return test_temp, max_current, max_frequency, current_unit, frequency_unit
    
    # class GetInfo(QDialog):
    def Reset_button_clicked(self):
        # Reset all
        self.CUSTOMER_Textbox.setText("")
        self.DEVICE_Textbox.setText("")
        self.SPACE_TRANSFORMER_Textbox.setText("")
        self.PAD_NUMBER_POSITION_Textbox.setText("")
        self.PAD_NAME_POSITION_Textbox.setText("")
        self.DUT_NAME_FORMAT_Textbox.setText("")
        self.DUT_NAME_POSITION_Textbox.setText("")
        self.DUT_NAME_DELIMITER_Textbox.setText("")
        self.NC_POSITION_Textbox.setText("")
        self.NC_FILTER_BY_Textbox.setText("")
        self.BUMP_DIAMETER_Textbox.setText("")
        self.PAD_X_SIZE_Textbox.setText("")
        self.PAD_Y_SIZE_Textbox.setText("")
        self.TEST_TEMPERATURE_Textbox.setText("")
        self.MAX_CURRENT_Textbox.setText("")
        self.MAX_FREQUENCY_Textbox.setText("")
        self.KEEP_OUT_X_SIZE_Textbox.setText("")
        self.KEEP_OUT_Y_SIZE_Textbox.setText("")
        self.KEEP_OUT_DIAMETER_Textbox.setText("")
        self.STEP_X_Textbox.setText("")
        self.STEP_Y_Textbox.setText("")
        self.die_config_tableWidget.clear()
        self.die_config_tableWidget.setRowCount(self.rowCount)
        self.die_config_tableWidget.setColumnCount(self.columnCount)
        [self.die_config_tableWidget.setColumnWidth(i, 10) for i in range(self.rowCount )]
        [self.die_config_tableWidget.setRowHeight(i, 10) for i in range(self.columnCount )]
        self.TableRowCount.setValue(self.rowCount)
        self.TableColumnCount.setValue(self.columnCount)
        self.Pad_Type_Checkbox.setChecked(False)
        return
    # end of Reset_button_clicked function
    
    # class GetInfo(QDialog):
    # Set up move window by clicked mouse
    def mouseMoveEvent(self, event):
        try:
            delta = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except:
            return

    # class GetInfo(QDialog):
    # Set up move window by clicked mouse
    def mousePressEvent(self, event):
        try:
            self.oldPosition = event.globalPos()
        except:
            return
# End of GetInfo class

# Start GENERATE_XY_LIST_SV_FORMAT function
def GENERATE_XY_LIST_SV_FORMAT(table_TableWidget, 
                                DUT_name_list, 
                                PAD_number_list, 
                                X_list_input, 
                                Y_list_input, 
                                Pad_name_list, 
                                Remark, 
                                Input_unit, 
                                nc_denoted):

    # Set number of rows and columns similar as excel file
    X_list = []
    Y_list = []

    if Input_unit == MM_UNIT: # if unit is mm
        X_list = [(X_list_input[i]*1000.0) for i in range(len(X_list_input))]
        Y_list = [(Y_list_input[i]*1000.0) for i in range(len(Y_list_input))]
    
    if Input_unit == MIL_UNIT: # if unit is mil
        X_list = [round((X_list_input[i]/25.4), 5) for i in range(len(X_list_input))]
        Y_list = [round((Y_list_input[i]/25.4), 5) for i in range(len(Y_list_input))]
    
    if Input_unit == UM_UNIT: # if unit is um
        X_list = X_list_input
        Y_list = Y_list_input

    number_of_column = len(XY_LIST_SV_FORMAT_HEADER_LIST)
    table_TableWidget.setRowCount(len(X_list)+1)
    table_TableWidget.setColumnCount(number_of_column)

    [table_TableWidget.setColumnWidth(i, 150) for i in range(number_of_column)]
    [table_TableWidget.setRowHeight(i, 5) for i in range(len(DUT_name_list))]
    
    [table_TableWidget.setItem(0, col, QTableWidgetItem(XY_LIST_SV_FORMAT_HEADER_LIST[col])) for col in range(table_TableWidget.columnCount())]
    
    if len(X_list) > 0:
        col  = XY_LIST_SV_FORMAT_HEADER_LIST.index('X Coordinate (um)')
        [table_TableWidget.setItem(row+1, col, QTableWidgetItem(str(X_list[row]))) for row in range(table_TableWidget.rowCount()-1)]
        col  = XY_LIST_SV_FORMAT_HEADER_LIST.index('Y Coordinate (um)')
        [table_TableWidget.setItem(row+1, col, QTableWidgetItem(str(Y_list[row]))) for row in range(table_TableWidget.rowCount()-1)]
    
    if len(DUT_name_list) > 0:
        col  = XY_LIST_SV_FORMAT_HEADER_LIST.index('SITE#/DUT#')
        [table_TableWidget.setItem(row+1, col, QTableWidgetItem(DUT_name_list[row])) for row in range(table_TableWidget.rowCount()-1)]
    
    if len(PAD_number_list) > 0:
        col  = XY_LIST_SV_FORMAT_HEADER_LIST.index('PAD#')
        [table_TableWidget.setItem(row+1, col, QTableWidgetItem(PAD_number_list[row])) for row in range(table_TableWidget.rowCount()-1)]

    if len(Pad_name_list) > 0:
        col  = XY_LIST_SV_FORMAT_HEADER_LIST.index('Pad name/Signal Name')
        [table_TableWidget.setItem(row+1, col, QTableWidgetItem(Pad_name_list[row])) for row in range(table_TableWidget.rowCount()-1)]

    if len(Remark) > 0:
        Remark_ = []
        Remark_ = [NC_OPTION[0] if i == nc_denoted else i for i in Remark]
        col = XY_LIST_SV_FORMAT_HEADER_LIST.index('Remarks')
        [table_TableWidget.setItem(row+1, col, QTableWidgetItem(Remark_[row])) for row in range(table_TableWidget.rowCount()-1)]
    
    # Completed
    return table_TableWidget
# End of GENERATE_XY_LIST_SV_FORMAT function #

# Start class Notification
class Notification(QDialog):
    def __init__(self, title, content):
        super().__init__()
        self.setWindowTitle("Notification")
        self.setFont(QFont("3ds", 12))
        blur(self.winId())

        # Set framless window
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet(Notification_stylesheet)

         # Create OK and Cancel button
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)

        # Set function for buttons
        self.buttonBox.accepted.connect(self.accept)

        # Set window title on screen
        window_title = QLabel(title)
        window_title.setStyleSheet("color:            rgb(255,255,255);"
                                    "background-color:  rgba(0,0,0,0);"
                                    "border:            0px;"
                                    "font:              20px 3ds")
        # Dialog content
        window_content = QLabel(content)
        window_content.setStyleSheet("color:            rgb(255,255,255);"
                                    "background-color:  rgba(0,0,0,0);"
                                    "border:            0px;"
                                    "font:              15px 3ds")
        # Set layout                            
        self.layout = QVBoxLayout()
        self.layout.addWidget(window_title)
        self.layout.addWidget(window_content)
        self.layout.addWidget(self.buttonBox)
        
        self.setLayout(self.layout)
        self.show()
        self.exec_()

    # Set up move window by clicked mouse
    def mouseMoveEvent(self, event):
        try:
            delta = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except:
            return

    # Set up move window by clicked mouse
    def mousePressEvent(self, event):
        try:
            self.oldPosition = event.globalPos()
        except:
            return
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(255, 255, 255))
        painter.setOpacity(0.3)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRoundedRect(self.rect(), 10.0, 10.0)

# End class Notification

# Start EXPORT_FILES function
def EXPORT_FILES(table_TableWidget , option):
    # export_options include: 
        # [0] = ALL_FILE_CHECK
        # [1] = XY_FORMAT_FOR_IUA_PLUS_CHECKBOX
        # [2] = ARRAY_FULL_SIZE_FILE_CHECKBOX
        # [3] = PROBE_HEAD_XY_FILE_CHECKBOX
        # [4] = PCB_PADS_LOCATION_FILE_CHECKBOX
        # [5] = IUA_PLUS_FILE_CHECKBOX
        # [6] = CRD_PLUS_FILE_CHECKBOX
    
    if not os.path.exists("paths.txt"):
        return "paths.txt file does not existed.", option
    
    # Call ExportOption dialog and get choices
    export_options  = ExportOption(option)
    option          = export_options.Return()

    if option.count(False) == len(option):
        return "No any files were exported!", option # return 0, option (0: no any exported files!)

    if option[0] == True:
        print(EXPORT_XY_FORMAT_FOR_IUA_PLUS_FILE())
        print(EXPORT_PCB_PAD_LOCATION_FILE())
        print(EXPORT_ARRAY_FULL_SITE_FOR_REFERENCE_FILE())
        print(EXPORT_IUA_PLUS_FILE())
        print(EXPORT_CRD_PLUS_FILE())
        print(EXPORT_PROBE_HEAD_XY_COORDINATES_FOR_APPROVAL_FILE())
    else:
        if option[1] == True:
            print(EXPORT_XY_FORMAT_FOR_IUA_PLUS_FILE())
        
        if option[2] == True:
            print(EXPORT_ARRAY_FULL_SITE_FOR_REFERENCE_FILE())
        
        if option[3] == True:
            print(EXPORT_PROBE_HEAD_XY_COORDINATES_FOR_APPROVAL_FILE())
        
        if option[4] == True:
            print(EXPORT_PCB_PAD_LOCATION_FILE())
        
        if option[5] == True:
            print(EXPORT_IUA_PLUS_FILE())
        
        if option[6] == True:
            print(EXPORT_CRD_PLUS_FILE())

    return "Run", option
# End of EXPORT_FILES function

# Start class SplashScreen
class SplashScreen(QDialog):
    def __init__(self, app):
        super().__init__()

        # Set up UI
        self.setWindowTitle('Hello')
        self.setFixedSize(900, 480)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QIcon('icon/card.png'))
        self.setStyleSheet(SplashScreen_stylesheet)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.screen = app.primaryScreen()
        self.setGeometry(np.int16((self.screen.size().width()-900)/2), np.int16((self.screen.size().height()-500)/2),0,0)
        
        # initial variables
        self.run = False
        self.new = True
        self.spec_file_path, self.spec_file_name, self.spec_file_extension = "","",""

        # Run functions
        self.initUI()

    # class SplashScreen
    def initUI(self):
        background_img = QLabel(self)
        background_img.resize(800, 400)
        background_img.move(50, 70)
        background_img.setStyleSheet("border-image: url('icon/splash_background.jpg');"
                                    "border-radius: 20px;")

        labelTitle = QLabel("Hi, " + os.getlogin())
        labelTitle.setStyleSheet(label_stylesheet)
        labelTitle.setAlignment(Qt.AlignCenter)
        labelTitle.adjustSize()

        self.new_radioButton = QRadioButton("New Project")
        self.new_radioButton.setChecked(self.new)

        self.open_radioButton = QRadioButton("Open Project")
        self.new_radioButton.setStyleSheet( "color: rgb(255,255,255);"
                                            "background-color: rgba(0,0,0,0);"
                                            "font: 20px 3ds;")
        self.open_radioButton.setStyleSheet("color: rgb(255,255,255);"
                                            "background-color: rgba(0,0,0,0);"
                                            "font: 20px 3ds;")

        nidec_logo = QPixmap('icon/nidec_logo.png')
        nidec_logo_label = QLabel(self)
        nidec_logo_label.setPixmap(nidec_logo)

        self.ok_button = QPushButton("Ok", self)
        self.ok_button.setStyleSheet(ok_button_stylesheet)
        self.ok_button.clicked.connect(self.Ok_clicked)

        self.close_button = QPushButton("close", self)
        self.close_button.setStyleSheet(close_button_stylesheet)
        self.close_button.clicked.connect(self.Close_clicked) 

        self.card_part_number_textbox = QLineEdit()
        self.card_part_number_textbox.setStyleSheet(CARD_PART_NUMBER_TEXTBOX_STYLE_SHEET)
        self.card_part_number_textbox.setToolTip("Card Part Number, ex: PCX-001234")

        self.open_project_button = QPushButton('Load Project')
        self.open_project_button.setStyleSheet(OPEN_BUTTON_PROJECT_BUTTON_STYLE_SHEET)
        self.open_project_button.clicked.connect(self.LOAD_PROJECT_FILE)

        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(nidec_logo_label)
        hlayout.addStretch(1)
        hlayout.addWidget(self.close_button)

        hlayout5 = QHBoxLayout()
        hlayout5.addStretch(1)
        hlayout5.addWidget(labelTitle)
        hlayout5.addStretch(1)

        hlayout1 = QHBoxLayout()
        hlayout1.addStretch(1)
        hlayout1.addWidget(self.new_radioButton)
        hlayout1.addStretch(1)

        hlayout3 = QHBoxLayout()
        hlayout3.addStretch(1)
        hlayout3.addWidget(self.card_part_number_textbox)
        hlayout3.addStretch(1)

        hlayout2 = QHBoxLayout()
        hlayout2.addStretch(1)
        hlayout2.addWidget(self.open_radioButton)
        hlayout2.addWidget(self.open_project_button)
        hlayout2.addStretch(1)

        hlayout4 = QHBoxLayout()
        hlayout4.addStretch(1)
        hlayout4.addWidget(self.ok_button)
    
        vlayout.addLayout(hlayout)
        vlayout.addLayout(hlayout5)
        vlayout.addLayout(hlayout3)
        vlayout.addLayout(hlayout1)
        vlayout.addLayout(hlayout2)
        vlayout.addLayout(hlayout4)

        self.setLayout(vlayout)
        self.show()
        self.exec_()
    # class SplashScreen
    def Ok_clicked(self):
        # If project is new
        if self.new_radioButton.isChecked() == True and self.open_radioButton.isChecked() == False:
            self.new = True
        # If project is existed
        if self.new_radioButton.isChecked() == False and self.open_radioButton.isChecked() == True:
            self.new = False
        # Get card part number
        CARD_PART_NUMBER['VALUE#'] = self.card_part_number_textbox.text().upper()
        
        # Update parameters value if PROJECT is existed
        if self.new == False:
            if CARD_PART_NUMBER['VALUE#'] != "":
                spec_file_name = UPDATE_PARAMETER_FOR_EXISTED_PROJECT(CARD_PART_NUMBER['VALUE#'])
                self.run = True #set run is True
            else:
                Notification("Error", "Please type card part number!")
                self.run = False #set run is False
        else: 
            self.run = True #set run is True
        
        # close SplashScreen and open Workspace if run = True
        if self.run == True:
            self.close()
    
    # class SplashScreen
    def Close_clicked(self):
        self.run = False
        self.close()
    
    # class SplashScreen
    def LOAD_PROJECT_FILE(self):
        # Open a window to choose spec file from explorer
        self.spec_file_path, self.spec_file_name, self.spec_file_extension = GET_SPEC_FILE()
              
    # class SplashScreen
    def Run(self):
        return self.run, self.new

    def Return(self):
        return

    # class SplashScreen
    # Set up move window by clicked mouse
    def mouseMoveEvent(self, event):
        try:
            delta = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except:
            return
    
    # class SplashScreen
    # Set up move window by clicked mouse
    def mousePressEvent(self, event):
        try:
            self.oldPosition = event.globalPos()
        except:
            return

# Start class ExportOption
class ExportOption(QDialog):
    def __init__(self, option):
        # option parameters, option variable is a list 
        # 0.export_all_files                      1.export_XY_FORMAT_FOR_IUA_PLUS_file
        # 2.export_ARRAY_FULL_SIZE_FILE_file     3.export_PROBE_HEAD_XY_FILE_file
        # 4.export_PCB_PADS_LOCATION_FILE_file   5.export_IUA_PLUS_FILE_file
        # 6.export_CRD_PLUS_FILE_file
        
        super().__init__()
        # Dialog Setup
        self.setWindowTitle("Get Info")
        blur(self.winId())

        # Set framless window
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("background-color:   rgba(50,50,50,0.2);"
                            "border:            1px solid white;"
                            "border-radius:     10px;")

        self.title = QLabel("Choose files to export")
        self.title.setStyleSheet(GET_INFO_ON_DIALOG)

        self.XY_FORMAT_FOR_IUA_PLUS_CHECKBOX    = QCheckBox("XY format for IUA+")
        self.ARRAY_FULL_SIZE_FILE_CHECKBOX      = QCheckBox("Array full sites for reference")
        self.PROBE_HEAD_XY_FILE_CHECKBOX        = QCheckBox("Probe Head XY Coordinates For Approval")
        self.PCB_PADS_LOCATION_FILE_CHECKBOX    = QCheckBox("PCB PADS LOCATION")
        self.IUA_PLUS_FILE_CHECKBOX             = QCheckBox("IUA+")
        self.CRD_PLUS_FILE_CHECKBOX             = QCheckBox("CRD+")

        self.XY_FORMAT_FOR_IUA_PLUS_CHECKBOX.setStyleSheet(EXPORT_OPTION_CHECK_BOX_STYLE_SHEET)
        self.ARRAY_FULL_SIZE_FILE_CHECKBOX.setStyleSheet(EXPORT_OPTION_CHECK_BOX_STYLE_SHEET)
        self.PROBE_HEAD_XY_FILE_CHECKBOX.setStyleSheet(EXPORT_OPTION_CHECK_BOX_STYLE_SHEET)
        self.PCB_PADS_LOCATION_FILE_CHECKBOX.setStyleSheet(EXPORT_OPTION_CHECK_BOX_STYLE_SHEET)
        self.IUA_PLUS_FILE_CHECKBOX.setStyleSheet(EXPORT_OPTION_CHECK_BOX_STYLE_SHEET)
        self.CRD_PLUS_FILE_CHECKBOX.setStyleSheet(EXPORT_OPTION_CHECK_BOX_STYLE_SHEET)

        self.ALL_FILE_CHECK = option[0]
        self.XY_FORMAT_FOR_IUA_PLUS_CHECKBOX.setChecked(option[1])         
        self.ARRAY_FULL_SIZE_FILE_CHECKBOX.setChecked(option[2])  
        self.PROBE_HEAD_XY_FILE_CHECKBOX.setChecked(option[3])    
        self.PCB_PADS_LOCATION_FILE_CHECKBOX.setChecked(option[4])
        self.IUA_PLUS_FILE_CHECKBOX.setChecked(option[5])
        self.CRD_PLUS_FILE_CHECKBOX.setChecked(option[6])

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)

        self.CHOOSE_ALL_BUTTON = QPushButton("All files")
        self.CLEAR_ALL_BUTTON  = QPushButton("Clear all")

        self.buttonBox.setStyleSheet(EXPORT_OPTION_BUTTON_STYLE_SHEET)
        self.CHOOSE_ALL_BUTTON.setStyleSheet(EXPORT_OPTION_BUTTON_STYLE_SHEET)
        self.CLEAR_ALL_BUTTON.setStyleSheet(CLEAR_EXPORT_OPTION_BUTTON_STYLE_SHEET)

        # Set function for buttons
        self.buttonBox.accepted.connect(self.accept)
        self.CHOOSE_ALL_BUTTON.clicked.connect(self.CHOOSE_ALL_FILE)
        self.CLEAR_ALL_BUTTON.clicked.connect(self.CLEAR_ALL_FILE)

        # Layout
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.CLEAR_ALL_BUTTON)
        self.hlayout.addWidget(self.CHOOSE_ALL_BUTTON)
        self.hlayout.addWidget(self.buttonBox)
        
        self.Edit_radioButton = QRadioButton(REVISION_STATUS[0])
        self.Release_radioButton = QRadioButton(REVISION_STATUS[1])
        self.Override_radioButton = QRadioButton(REVISION_STATUS[2])
        self.Edit_radioButton.setStyleSheet(EXPORT_OPTION_RADIO_BUTTON_STYLE_SHEET)
        self.Release_radioButton.setStyleSheet(EXPORT_OPTION_RADIO_BUTTON_STYLE_SHEET)
        self.Override_radioButton.setStyleSheet(EXPORT_OPTION_RADIO_BUTTON_STYLE_SHEET)
        
        self.radioButton = []
        for i in range(len(REVISION_STATUS)):
            self.radioButton.append(self.QRadioButton(REVISION_STATUS[i]))
        
        self.radioButtonGroup = QRadioButtonGroup()
        for i in range(len(option)-1):
            self.radioButtonGroup.append
        
        self.ApplyAll_checkBox = QCheckBox("Apply All")
        self.ApplyAll_checkBox.setStyleSheet(APPLY_ALL_CHECK_BOX_STYLE_SHEET)
        self.ApplyAll_checkBox.setChecked(False)
        
        self.vlayout1 = QVBoxLayout()
        self.vlayout1.addWidget(self.title)
        
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.Edit_radioButton, 0,1)
        self.gridLayout.addWidget(self.Release_radioButton, 0,2)
        self.gridLayout.addWidget(self.Override_radioButton, 0,3)
        self.gridLayout.addWidget(self.ApplyAll_checkBox, 0,4)
        
        self.gridLayout.addWidget(self.XY_FORMAT_FOR_IUA_PLUS_CHECKBOX, 1,0)
        self.gridLayout.addWidget(self.ARRAY_FULL_SIZE_FILE_CHECKBOX, 2, 0)
        self.gridLayout.addWidget(self.PROBE_HEAD_XY_FILE_CHECKBOX, 3, 0)
        self.gridLayout.addWidget(self.PCB_PADS_LOCATION_FILE_CHECKBOX, 4, 0)
        self.gridLayout.addWidget(self.IUA_PLUS_FILE_CHECKBOX, 5, 0)
        self.gridLayout.addWidget(self.CRD_PLUS_FILE_CHECKBOX, 6, 0)
        
        for i in range(len(option)-1):
            self.gridLayout.addWidget(self.radioButton1[i], i+1,1)
            self.gridLayout.addWidget(self.radioButton2[i], i+1,2)
            self.gridLayout.addWidget(self.radioButton3[i], i+1,3)

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.vlayout1)
        self.vlayout.addLayout(self.gridLayout)
        self.vlayout.addLayout(self.hlayout)
        self.setLayout(self.vlayout)
        self.show()
        self.exec_()
        
    # class ExportOption
    def CHOOSE_ALL_FILE(self):
        self.ALL_FILE_CHECK = True
        self.XY_FORMAT_FOR_IUA_PLUS_CHECKBOX.setChecked(self.ALL_FILE_CHECK)         
        self.ARRAY_FULL_SIZE_FILE_CHECKBOX.setChecked(self.ALL_FILE_CHECK)  
        self.PROBE_HEAD_XY_FILE_CHECKBOX.setChecked(self.ALL_FILE_CHECK)    
        self.PCB_PADS_LOCATION_FILE_CHECKBOX.setChecked(self.ALL_FILE_CHECK)
        self.IUA_PLUS_FILE_CHECKBOX.setChecked(self.ALL_FILE_CHECK)
        self.CRD_PLUS_FILE_CHECKBOX.setChecked(self.ALL_FILE_CHECK)
    
    # class ExportOption
    def CLEAR_ALL_FILE(self):
        self.ALL_FILE_CHECK = False
        self.XY_FORMAT_FOR_IUA_PLUS_CHECKBOX.setChecked(self.ALL_FILE_CHECK)         
        self.ARRAY_FULL_SIZE_FILE_CHECKBOX.setChecked(self.ALL_FILE_CHECK)  
        self.PROBE_HEAD_XY_FILE_CHECKBOX.setChecked(self.ALL_FILE_CHECK)    
        self.PCB_PADS_LOCATION_FILE_CHECKBOX.setChecked(self.ALL_FILE_CHECK)
        self.IUA_PLUS_FILE_CHECKBOX.setChecked(self.ALL_FILE_CHECK)
        self.CRD_PLUS_FILE_CHECKBOX.setChecked(self.ALL_FILE_CHECK)
    
    # class ExportOption
    def Return(self):
        # return PARAMETERS: 
        # [0] = ALL_FILE_CHECK
        # [1] = XY_FORMAT_FOR_IUA_PLUS_CHECKBOX
        # [2] = ARRAY_FULL_SIZE_FILE_CHECKBOX
        # [3] = PROBE_HEAD_XY_FILE_CHECKBOX
        # [4] = PCB_PADS_LOCATION_FILE_CHECKBOX
        # [5] = IUA_PLUS_FILE_CHECKBOX
        # [6] = CRD_PLUS_FILE_CHECKBOX
        return self.ALL_FILE_CHECK, \
               self.XY_FORMAT_FOR_IUA_PLUS_CHECKBOX.isChecked(), \
               self.ARRAY_FULL_SIZE_FILE_CHECKBOX.isChecked(), \
               self.PROBE_HEAD_XY_FILE_CHECKBOX.isChecked(), \
               self.PCB_PADS_LOCATION_FILE_CHECKBOX.isChecked(), \
               self.IUA_PLUS_FILE_CHECKBOX.isChecked(), \
               self.CRD_PLUS_FILE_CHECKBOX.isChecked() \
    
    # class ExportOption
    def mouseMoveEvent(self, event):
        # Set up move window by clicked mouse
        try:
            delta = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except:
            return

    # class ExportOption
    def mousePressEvent(self, event):
        # Set up move window by clicked mouse
        try:
            self.oldPosition = event.globalPos()
        except:
            return