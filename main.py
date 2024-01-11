from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sqlite3
import sys


class CoffeData(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.update = None

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle("Coffe Data")

        self.table = QTableWidget(self)
        self.table.setGeometry(10, 10, 480, 380)

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

        self.button = QPushButton("update/new", self)
        self.button.setGeometry(10, 400, 100, 50)
        self.button.clicked.connect(self.fnc)

    def fnc(self):
        if self.update is None:
            self.update = UpdateOrNew()
            self.update.show()


class UpdateOrNew(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle("Coffe Update")

        self.pushButton = QPushButton("ok", self)
        self.pushButton.setGeometry(440, 440, 50, 50)
        self.pushButton.clicked.connect(self.fnc)

        self.id = QSpinBox(self)
        self.id.setMaximum(999999)
        self.id.setMinimum(1)
        self.id.setGeometry(10, 10, 30, 30)
        self.label1 = QLabel("id", self)
        self.label1.setGeometry(10, 50, 30, 10)

        self.degree = QSpinBox(self)
        self.degree.setMaximum(10)
        self.degree.setMinimum(1)
        self.degree.setGeometry(50, 10, 30, 30)
        self.label2 = QLabel("degree", self)
        self.label2.setGeometry(50, 50, 30, 10)

        self.milled = QSpinBox(self)
        self.milled.setMaximum(1)
        self.milled.setMinimum(0)
        self.milled.setGeometry(90, 10, 30, 30)
        self.label3 = QLabel("milled", self)
        self.label3.setGeometry(90, 50, 30, 10)

        self.price = QSpinBox(self)
        self.price.setMaximum(999999)
        self.price.setMinimum(1)
        self.price.setGeometry(130, 10, 30, 30)
        self.label4 = QLabel("price", self)
        self.label4.setGeometry(130, 50, 30, 10)

        self.size = QSpinBox(self)
        self.size.setMaximum(999999)
        self.size.setMinimum(1)
        self.size.setGeometry(170, 10, 30, 30)
        self.label5 = QLabel("size", self)
        self.label5.setGeometry(170, 50, 30, 10)

        self.name = QLineEdit(self)
        self.name.setGeometry(210, 10, 50, 30)
        self.label6 = QLabel("name", self)
        self.label6.setGeometry(210, 50, 50, 10)

        self.taste = QLineEdit(self)
        self.taste.setGeometry(270, 10, 50, 30)
        self.label7 = QLabel("taste", self)
        self.label7.setGeometry(270, 50, 50, 10)

    def fnc(self):
        global window
        id = self.id.value()
        name = self.name.text()
        degree = self.degree.value()
        milled = self.milled.value()
        taste = self.taste.text()
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeData()
    window.show()
    sys.exit(app.exec_())
