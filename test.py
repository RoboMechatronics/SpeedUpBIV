# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *

# app = QApplication(sys.argv)
# widget = QMainWindow()
# widget.resize(510, 210)

# parents_list = ['A', 'B', 'C', 'D']
# items_list = {'A': ['A1','A2'], 'B':['B1','B2'], 'C': ['C1','C2','C3'],'D':['D1']}
# items_list_ = {'A': ['A1','A2'], 'B':['B1','B2'], 'C': ['C1','C2','C3'],'D':['D1']}

# tree = QTreeWidget()
# # tree.setStyleSheet("""QTreeWidget {
# #                         color: rgb(255,255,255);
# #                         background-color: rgba(255,255,255,0);
# #                         font: 15px 3ds;
# #                     }""")        
# tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
# tree.setColumnCount(3)
# tree.setColumnWidth(0, 150)
# tree.setColumnWidth(1, 150)
# tree.setHeaderLabels(['Part Number', 'File name', 'Status'])

# # addition data to the tree
# for part_number in parents_list:
#     part_item = QTreeWidgetItem(tree)
#     part_item.setText(0, part_number)
#     # Set the childs
#     for element in items_list[part_number]:
#         print(element)
#         element_item   = QTreeWidgetItem(tree)
#         element_item.setText(1, element)
#         part_item.addChild(element_item)

# widget.setCentralWidget(tree)
# widget.show()
# sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QWidget

if __name__ == '__main__':
    app = 0
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)

    w = QWidget()
    w.resize(510, 210)
    tree = QTreeWidget(w)
    
    tree.resize(500, 200)
    tree.setColumnCount(2)
    tree.setHeaderLabels(["File name", "Latest Saved"])

    parents = ["PCX-000000-xx", "401-000000-xx"]

    list_0 = [['PCX-000000-xx.slddrw', '10-1-2023'],
              ['PCX-000000-xx.sldprt', '9-10-2023']]

    list_1 = [['401-000000-xx.sldprt','20-8-2022'],
              ['401-000000-xx.sldasm','10-12-2022']]
    
    dict0 = {parents[0]: list_0[0], 
              parents[1]: list_1[0]}

    dict1 = {parents[0]: list_0[1], 
              parents[1]: list_1[1]}

    for parent in parents:
        parent_tree = QTreeWidgetItem(tree)
        parent_tree.setText(0, parent)
        l1_child = QTreeWidgetItem(dict0[parent])
        l2_child = QTreeWidgetItem(dict1[parent])
        parent_tree.addChild(l1_child)
        parent_tree.addChild(l2_child)
    
    tree.expandAll()
    w.show()
    sys.exit(app.exec_())