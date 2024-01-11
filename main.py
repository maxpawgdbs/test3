from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sqlite3
import sys


class CoffeData(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.update = None

        uic.loadUi("main.ui", self)

        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        coffee = cur.execute("SELECT * FROM characteristics").fetchall()
        con.close()

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

        self.button.clicked.connect(self.fnc)

    def fnc(self):
        if self.update is None:
            self.update = UpdateOrNew()
            self.update.show()


class UpdateOrNew(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi("addEditCoffeeForm.ui", self)

        self.pushButton.clicked.connect(self.fnc)

    def fnc(self):
        try:
            global window
            id = self.id.value()
            name = self.name.text()
            degree = self.degree.value()
            milled = self.milled.value()
            taste = self.milled.value()
            price = self.price.value()
            size = self.size.value()

            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()
            if cur.execute("""SELECT * FROM characteristics WHERE ID = ?""", (id,)).fetchone() is not None:
                cur.execute("""UPDATE characteristics
                SET name = ?, degree = ?, milled = ?, taste = ?, price = ?, size = ?
                WHERE ID = ?""",
                            (name, degree, milled, taste, price, size, id))
            else:
                cur.execute("""INSERT INTO characteristics(ID, name, degree, milled, taste, price, size)
                            VALUES(?, ?, ?, ?, ?, ?, ?)""",
                            (id, name, degree, milled, taste, price, size))
            con.commit()

            coffee = cur.execute("SELECT * FROM characteristics").fetchall()
            con.close()
            window.table.clear()

            window.table.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
            window.table.setHorizontalHeaderItem(1, QTableWidgetItem("name"))
            window.table.setHorizontalHeaderItem(2, QTableWidgetItem("degree"))
            window.table.setHorizontalHeaderItem(3, QTableWidgetItem("milled"))
            window.table.setHorizontalHeaderItem(4, QTableWidgetItem("taste"))
            window.table.setHorizontalHeaderItem(5, QTableWidgetItem("price"))
            window.table.setHorizontalHeaderItem(6, QTableWidgetItem("size"))

            window.table.setRowCount(len(coffee))
            for y in range(len(coffee)):
                for x in range(7):
                    item = QTableWidgetItem(str(coffee[y][x]))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    window.table.setItem(y, x, item)
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeData()
    window.show()
    sys.exit(app.exec_())
