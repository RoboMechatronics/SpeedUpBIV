# START #
#---------------------------------------------------------------------------------------------------#
APP_NAME = "SpeedUp B I V"

FILE_MENU = "&File"
EDIT_MENU = "&Edit"
TOOL_MENU = "&Tool"
HELP_MENU = "&Help"

NEW_ACTION = "&New"
OPEN_ACTION = "&Open"
SAVE_ACTION = "&Save"
EXIT_ACTION = "&Exit"

CREATE_CHART_BUTTON = "&Import XY and Create chart"
CLEAR_CHART_BUTTON = "&Clear chart"
INPUT_UNIT_BUTTON = "&Input unit"
INPUT_INFO_BUTTON = "&Get Info"
IMPORT_INFO_SPEC_FORM_BUTTON = "&Import Spec form"
CHECK_BUTTON = "&Check"
EXPORT_BUTTON = "&Export XY files"
GENERATE_BUTTON = "&Generate Probe head XY for review"
FINAL_EXPORT_BUTTON = "&Final Export"

DIE_PATTERN_BUTTON = "&Die Pattern"

CHART_TOOL = "&Chart tools"
EDIT_TOOL = "&Edit tools"
EXPORT_TOOLS = "Export Tools"
#---------------------------------------------------------------------------------------------------#
CARD_PART_NUMBER = {
    "LABEL": "", # QLabel on main window
    "VALUE": "", # QLabel on main window
    "VALUE#": "", # Value
}
CUSTOMER_NAME = {
    "LABEL": "", # QLabel
    "VALUE": "", # QLabel
    "NAME": "",

} # help to read input and write output value

DEVICE_NAME = {
    "LABEL": "",
    "VALUE": "",
    "NAME": "",
} # help to read input and write output value

DIE_CONFIGURATION = [] # help to read input and write output value

MIN_PITCH_HAS_NC = 0.0

SPACE_TRANSFORMER_TYPE = {
    "LABEL": "",
    "VALUE": "",
    "TYPE": "",
} # Wired, DirectAttach, MLO-MLC

# Data unit #
MM_UNIT     = "mm"
UM_UNIT     = "um"
MIL_UNIT    = "mil"
IN_UNIT     = "inch"

DIE_SIZE = { # Die size info
    "X":        0.0,
    "Y":        0.0,
    'VALUE':    "",
    "LABEL":    "",
}

PROBE = { # Total no. of Probe
    "LABEL":    "",
    "VALUE":    "",
    "VALUE#":   0,
}

MIN_PITCH = { # The smallest pad pitch
    "LABEL":    "",
    "VALUE":    "",
    "VALUE#":   0.0,
}

NO_OF_DIES = { # Total no. of dies
    "LABEL":    "",
    "VALUE":    "",
    "VALUE#":   0,
} 

STEPPING_DISTANCE = { # The distance between die to die
    "LABEL":    "", # label on your UI
    "Y":        0.0, # no skip state
    "X":        0.0, # no skip state
    "VALUE":    "", # value is showed on your UI
}

PADS_PER_DIE = { # Total number of pads per die
    "LABEL":    "",
    "VALUE":    "",
    "VALUE#":   0,
}

DIE_CONFIG = { # End of Die configuration info
    "LABEL":           "",
    "VALUE":           "",
    "X_OR_COLUMN":     0,
    "Y_OR_ROW":        0,
    "SKIP_ROW":        0,
    "SKIP_COLUM":      0,
}

MIN_PAD_SIZE = { #Minimum pad size is showed on your UI
    "LABEL":"", # Label on UI
    "VALUE":"", # a value as label on UI
    "X": 0.0,  # Flat pad size in X direction
    "Y": 0.0, # Flat pad size in Y direction
    "D": 0.0, # Bump diameter for Bump pad type
}

NC_PAD = {
    "LABEL":"",
    "VALUE":"",
    "VALUE#": 0,
}

KEEP_OUT_TYPE = {
    "LABEL": "",
    "VALUE": "",
    "RECTANGLE_X_SIZE": 0.0,
    "RECTANGLE_Y_SIZE": 0.0,
    "CIRCLE_DIAMETER": 0.0,
    "TYPE": ["Rectangle","Circle"],
}

WAFER_PAD = {
    "LABEL": "", # QLabel on UI
    "VALUE": "", # QLabel on UI
    "MATERIAL": "", # String type
}

PROBING_TEMP = {
    "LABEL":"",
    "VALUE": "", # QLabel on UI
    "VALUE#": 0.0, # UNIT: CELSIUS
}

DUTY_CYCLE = {
    "LABEL": "",
    "VALUE": "", # Label on UI
    "TYPE": ["Continuous","Pulse"], # default
}

MAX_CURRENT = {
    "LABEL": "",
    "VALUE": "",
    "VALUE#": 0.0, # UNIT: mA
    "UNIT": ["mA","A"]
}

MAX_FREQUENCY = {
    "LABEL": "",
    "VALUE": "", # Label on UI
    "VALUE#": 0.0, # Unit Hz, Mhz, GHz
    "UNIT": ["GHz", "MHz", "Hz"]
}

PROBE_PART_NUMBER = {
    "LABEL": "",
    "VALUE": "",
    "PART_NUMBER": "",
}
# Styles
MainStyleSheet = """
    QMainWindow {
        background-image: url(icon/background.jpg);
        background-position: center;
        background-color: rbga(0,0,0,0);
        color: rbga(0,0,0,0);
        }

    QMenuBar {
        /*background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 lightgray, stop:1 darkgray);*/
        background-color: rgb(0,0,0);
    }

    QMenuBar::item {
        spacing: 3px;           
        padding: 2px 10px;
        background-color: rgb(0, 0, 0);
        color: rgb(255,255,255);  
        border-radius: 5px;
    }

    QMenuBar::item:selected {    
        background-color: rgb(255,100,0);
    }

    QMenuBar::item:pressed {
        background: rgb(255,50,0);
    }

    QMenu {
        font: 10pt;
        background-color: rbg(0,0,0);
        color: rbg(0,0,0);
    }

    QMenu::item:selected {
        background-color: rbg(0,0,0);
        color: rbg(0,0,0);
    }

    QSplitter::handle:horizontal {
        width: 2px;
        background-color : rgba(0,0,0,0);
        border: 0px;
    }

    /*QSplitter::handle:vertical {
        height: 10px;
        background-color : rbg(200,255,255);
    }*/

    QLabel {
        background-color : rgba(0,0,0,0);
        color: rgb(255,255,255);
    }

    QPushButton {
        color: white;
        min-width: 36px;
        min-height: 36px;
        border-radius: 7px;
        background-color: rgba(255,255,255,0.3);
    }

    QPushButton:hover {
        color: black;
        background: #999;
    }

    QPushButton:pressed {
        background-color: rgba(255,255,255,0.5);
        color: white;
    }

    QStatusBar{
        color: rgb(255,255,255);
    }

    QTabWidget::pane {
        background: rgba(255,255,255,0.1);
        color: rgb(255,255,255);
        border:0px;
        border-radius: 10px;
    }

    QTabBar {
        background: rgba(255,255,255,0.3);
        color: rgb(255,255,255);
        border-radius: 10px;
        spacing: 5px;           
        padding: 5px 10px;
    }

    QTabBar::tab {
        background: rgba(100,255,100,0);
        border-radius: 10px;
        color: rgb(255,255,255);
        spacing: 5px;           
        padding: 5px 10px;
    }

    QTabBar::tab::selected {
        background: rgba(255,150,0,1);
        color: rgb(255,255,255);
        border-radius: 10px;
        spacing: 5px;           
        padding: 5px 10px;
    }

    QToolBar{
        border: 1px;
    }

    QTableWidget{
        background-color: rgba(255,255,255,0.2);
        border-radius: 10px;
    }

    QTableWidget::item{
        color: white;
    }

    QFrame{
        border: 0px;
    }
    """

FOLDER_LABEL_STYLE_SHEET = """
    QLabel{
        font: 15px 3ds;
        background-color: transparent;
        color: white;
    }
    """
INFO_LABEL_STYLE_SHEET = """
    QLabel{
        color: white;
        font: 15px 3ds;
        background-color: transparent;
        border: 0px;
        qproperty-alignment: 'AlignVCenter | AlignRight';
    }
    """
INFO_TEXTBOX_STYLE_SHEET = """
    QLineEdit{
        color: rgb(255,255,255);
        border-radius: 5px;
        background-color: rgba(0,0,0,0.3);
        font: 15px 3ds;
        padding: 5px 20px
    }
    QToolTip{
        color: #606060;
        border-radius: 5px;
        background-color: #EAEAEA;
        font: 15px 3ds;
        border: 5px;
    }
    """
IMPORT_XY_BUTTON_STYLE_SHEET = """
    QPushButton {
        min-width: 36px;
        min-height: 36px;
        border-radius: 7px;
        background: rgba(255,150,0,0.9);
        color: white;
    }
    QPushButton:hover {
        color: white;
        background: rgba(255,150,0,1);
    }
    QPushButton:pressed {
        color: white;
        background: rgba(255,150,0,0.3);
    }
    """
FOLDER_TREE_STYLE_SHEET = """
    QHeaderView{
        color: black;
    }
    QTreeWidget{
        color: white;
    }
    """

RADIO_BUTTON_STYLE_SHEET = """
    QRadioButton {
        color: rgb(255,255,255); 
        background-color: rgba(0, 0, 0, 0); 
        font: 12px 3ds;
        border: 2px;
        }
    """

Pad_Size_Enable_styleSheet = """
                                QLineEdit{
                                color: rgb(255,255,255);
                                border-radius: 5px;
                                background-color: rgba(0,0,0,0.3);
                                font: 15px 3ds;
                                }
                                QToolTip{
                                color: #606060;
                                border-radius: 5px;
                                background-color: #EAEAEA;
                                font: 15px 3ds;
                                border: 5px;
                                }
                            """      
Pad_Size_Disable_styleSheet = """
                                QLineEdit{
                                    color: rgb(255,255,255);
                                    border-radius: 5px;
                                    background-color: rgba(0,0,0,0);
                                    font: 15px 3ds;
                                    border: 0px;
                                }
                                QToolTip{
                                    color: #606060;
                                    border-radius: 5px;
                                    background-color: #EAEAEA;
                                    font: 15px 3ds;
                                    border: 5px;
                                }
                            """
Pad_type_label_stylesheet = """
                                QLabel{
                                    color:                  white;
                                    font:                  12px 3ds;
                                    background-color:      transparent;
                                    border:                0px;
                                    qproperty-alignment: 'AlignVCenter | AlignRight';
                                }
                            """
Unit_combo_box_style_sheet = """
                                QComboBox
                                {
                                    background-color: rgb(100,100,100);
                                    border-radius: 2px;                             
                                    selection-color: white;
                                    padding: 1px 1px 1px 10px;
                                    border-radius: 2px;
                                    border: 0px;
                                }
                                QComboBox:!on
                                {
                                    color: white;
                                    background-color: rgb(51,153,51);
                                    font: 15px;
                                    border-radius: 2px;
                                    border: 0px;
                                }
                            """
small_img_StyleSheet = """
                            QLabel{
                                color:                 white;
                                font:                  12px 3ds;
                                background-color:      transparent;
                                border:                0px;
                                qproperty-alignment:   AlignCenter;
                            }
                        """
SheetsNameDialog_listwidget_StyleSheet = """
                                            QListWidget
                                            {
                                                color:             rgb(255,255,255);
                                                background-color:  rgba(0,0,0,0);
                                                border:            1px solid white;
                                                border-radius:     5px;
                                                font:              15px Courier New;
                                            }
                                            QListWidget::item::selected
                                            {
                                                background-color:  rgba(255,150,0,0.9);
                                            }
                                        """
Die_config_spin_box_style_sheet = """
                                    QSpinBox{
                                        color:rgb(255,255,255);
                                        background-color:  rgba(0,0,0,0);
                                    }
                                    """
Die_config_TableWidget_stylesheet = """
                                    QTableWidget {
                                        background-color: rgba(100,100,100,0.2);
                                        border-radius: 10px;
                                    }
                                    QTableWidget::item{
                                        color: white;
                                    }

                                    QFrame{
                                        border: 0px;
                                    }
                                    """
GET_INFO_ON_DIALOG = """QLabel{
                                    color:             white;
                                    font:              25px 3ds;
                                    background-color:  transparent;
                                    border:            0px;
                        }
                        """     


SplashScreen_stylesheet = """
                            background-color:   rgba(0,0,0,0);
                            border-radius:  10px;
                            """

label_stylesheet = """
                        QLabel{
                            font:               35px 3ds;
                            color:              rgb(255,255,255);
                            background-color:   rgba(0,0,0,0);
                        }
"""

close_button_stylesheet="""
                            QPushButton {
                                color: white;
                                min-width: 36px;
                                min-height: 36px;
                                border-radius: 7px;
                                background-color: rgba(100,100,100,0.5);
                            }

                            QPushButton:hover {
                                color: black;
                                background: #FF0066;
                            }

                            QPushButton:pressed {
                                background-color: rgba(255,255,255,0.5);
                                color: white;
                            }
                        """
ok_button_stylesheet="""
                        QPushButton {
                            color: white;
                            min-width: 36px;
                            min-height: 36px;
                            border-radius: 7px;
                            background-color: rgba(100,100,100,0.5);
                        }

                        QPushButton:hover {
                            color: white;
                            background: #33CC33;
                        }

                        QPushButton:pressed {
                            background-color: rgba(255,255,255,0.5);
                            color: white;
                        }
                    """
CARD_PART_NUMBER_TEXTBOX_STYLE_SHEET = """
                                        QLineEdit{
                                            color: rgb(255,255,255);
                                            border-radius: 10px;
                                            background-color: rgba(200,200,200,0.3);
                                            font: 20px 3ds;
                                            min-width: 36px;
                                            min-height: 36px;
                                            qproperty-alignment: 'AlignVCenter | AlignCenter';
                                            text-transform: uppercase;
                                        }
                                        QToolTip{
                                            color: #606060;
                                            border-radius: 20px;
                                            background-color: #EAEAEA;
                                            font: 15px 3ds;
                                        }"""

OPEN_BUTTON_PROJECT_BUTTON_STYLE_SHEET = """
                                            QPushButton {
                                                font: 15px 3ds;
                                                color: white;
                                                border-radius: 5px;
                                                background-color: rgba(100,100,100,0.5);
                                                min-width: 36px;
                                                min-height: 36px;
                                            }

                                            QPushButton:hover {
                                                color: white;
                                                background: #33CC33;
                                            }

                                            QPushButton:pressed {
                                                background-color: rgba(255,255,255,0.5);
                                                color: white;
                                            }"""
EXPORT_OPTION_STYLE_SHEET = """
                            QLabel{
                                    color:             white;
                                    font:              25px 3ds;
                                    background-color:  transparent;
                                    border:            0px;
                                    border-radius:     10px;
                            }
                            """    

EXPORT_OPTION_CHECK_BOX_STYLE_SHEET = """
                                QCheckBox
                                {
                                    color: white;
                                    font: 18px 3ds;
                                    background-color: rgba(0,0,0,0);                        
                                    border-radius: 10px;
                                    border: 0px;
                                }
                                QCheckBox:checked
                                {
                                    font: 18px 3ds;
                                    background-color: rgba(100,255,100, 0.5);
                                    border-radius:10px;
                                    border: 0px;
                                }
                            """  
EXPORT_OPTION_BUTTON_STYLE_SHEET="""
                                    QPushButton {
                                        font: 15px 3ds;
                                        background-color: rgba(100,100,100,0);
                                        min-width: 36px;
                                        min-height: 36px;
                                        border: 0px;
                                    }

                                    QPushButton:hover {
                                        background: #33CC33;
                                        border: 0px;
                                    }

                                    QPushButton:pressed {
                                        background-color: rgba(255,255,255,0.5);
                                        border: 0px;
                                    }"""    
CLEAR_EXPORT_OPTION_BUTTON_STYLE_SHEET="""
                                            QPushButton {
                                                font: 15px 3ds;
                                                background-color: rgba(100,100,100,0);
                                                min-width: 36px;
                                                min-height: 36px;
                                                border: 0px;
                                            }

                                            QPushButton:hover {
                                                background: rgba(255,50,50,0.5);
                                                border: 0px;
                                            }

                                            QPushButton:pressed {
                                                background-color: rgba(255,255,255,0.5);
                                                border: 0px;
                                            }"""       
Tab2_foldertree_stylesheet = """
                                QTreeView {
                                    font: 15px 3ds;
                                    background-color: rgba(0,0,0,0);
                                    color: white;
                                }"""
                                                                                                

Notification_stylesheet = """
                            QDialog{
                                    background-color:   rgba(0,0,0,0);
                                    border:            2px solid white;
                                    border-radius:     10px;
                                    }
                        """
# End of Styles

# Paths
# XY_LIST_SV_FORMAT_HEADER_LIST similar PROBE_HEAD_XY header list
XY_LIST_SV_FORMAT_HEADER_LIST = ['SITE#/DUT#', 'PAD#', 'X Coordinate (um)', 'Y Coordinate (um)', 'Pad name/Signal Name', 'Remarks']

# EXPORTED FILES FORMAT
PROBE_HEAD_XY_SHEETS_NAME = ['History of Revision', 'XY Coordinates']
PROBE_HEAD_XY_TEMPLATE_FILENAME = 'YYY-XXXXXX-xx-Probe Head XY Coordinates For Approval Rev00.xlsx'
PROBE_HEAD_XY_TEMPLATE_FULLPATH = 'templates/' + PROBE_HEAD_XY_TEMPLATE_FILENAME
PROBE_HEAD_XY_FULLPATH = 'result/PART-NUMBER-xx-Probe Head XY Coordinates For Approval Rev00.xlsx'

ARRAY_FULL_SITE_SHEET_NAME = ['Revision', 'XY list']
ARRAY_FULL_SITE_TEMPLATE_FILENAME = 'YYY-XXXXXX_Array full sites for reference_Rev00.xlsx'
ARRAY_FULL_SITE_TEMPLATE_FULLPATH = 'templates/' + ARRAY_FULL_SITE_TEMPLATE_FILENAME
ARRAY_FULL_SITE_FULLPATH = 'result/PART-NUMBER-xx_Array full sites for reference_Rev00.xlsx'

# NC (not connect) Definition
NC_OPTION = ['No Probe, No Drill Hole', "No Probe, Drill Hole"]
#--------------------------------------------------------#

# Read paths.txt file to get path
with open('paths.txt', encoding='utf8') as f:
    paths = f.readlines()
# End read paths.txt file to get path

# END #
