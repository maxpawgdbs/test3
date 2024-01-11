from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sqlite3
import sys


class CoffeData(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi("main.ui", self)

        # self.setWindowTitle("Coffe Database")
        # self.setGeometry(300, 300, 500, 300)

        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        # cur.execute("""INSERT INTO characteristics(ID, name, degree, milled, taste, price, size)
        # VALUES(1, 'coffee1', 3, 0, 'sweet', 100, 1000)""")
        # cur.execute("""INSERT INTO characteristics(ID, name, degree, milled, taste, price, size)
        #         VALUES(2, 'coffee2', 2, 1, 'solt', 300, 300)""")
        # cur.execute("""INSERT INTO characteristics(ID, name, degree, milled, taste, price, size)
        #         VALUES(3, 'coffee3', 1, 1, 'ostriy', 180, 1800)""")
        # con.commit()
        coffee = cur.execute("SELECT * FROM characteristics").fetchall()
        con.close()

        # self.table = QTableWidget(self)
        # self.table.setGeometry(10, 10, 480, 280)

        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("name"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("degree"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("milled"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem("taste"))
        self.table.setHorizontalHeaderItem(5, QTableWidgetItem("price"))
        self.table.setHorizontalHeaderItem(6, QTableWidgetItem("size"))
        self.table.setRowCount(len(coffee))
        for y in range(len(coffee)):
            for x in range(7):
                item = QTableWidgetItem(str(coffee[y][x]))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(y, x, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeData()
    window.show()
    sys.exit(app.exec_())
