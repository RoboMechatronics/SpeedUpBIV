import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('PyQt QTreeWidget')
        self.setGeometry(100, 100, 400, 200)

        # tree
        tree = QTreeWidget(self)
        tree.setColumnCount(2)
        tree.setColumnWidth(0, 150)
        tree.setColumnWidth(1, 150)
        tree.setHeaderLabels(['Part Number', 'Files'])

        part_numbers = ['401-XXXXXX-01','PCX-000000-xx','LGP-000000-01']
        employees = {
            '401-XXXXXX-01': ['401-XXXXXX-01.sldprt','401-XXXXXX-01.slddrw'],
            'PCX-000000-xx': ['PCX-000000-xx.sldasm','PCX-000000-xx.slddrw'],
            'LGP-000000-01': ['LGP-000000-01.sldprt','LGP-000000-01.slddrw'],
        }

        # addition data to the tree
        for part_number in part_numbers:
            part_item = QTreeWidgetItem(tree)
            part_item.setText(0, part_number)
            # set the child
            for employee in employees[part_number]:
                employee_item   = QTreeWidgetItem(tree)
                employee_item.setText(1, employee)

                part_item.addChild(employee_item)

        # place the tree on the main window
        self.setCentralWidget(tree)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())