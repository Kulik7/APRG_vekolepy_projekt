import sys
from random import randint
from _collections import deque

from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QWidget, QApplication, QHeaderView
from PyQt5.QtWidgets import QWidget, QAction, QTableWidget, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QTimer


class TTabulka(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.x = 1
        self.y = 1
        self.vel_tabulky = int(input("Ahoj jak složité bludiště si přeješ? (jakože počet čtverečků na čtvereček) "))

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.tr("Velolepé bludiště"))
        self.createTable()
        self.show()


    def createTable(self):
        vel_ctverce = 20

        # Create table
        self.mazeTable = QTableWidget()
        self.mazeTable.setRowCount(self.vel_tabulky)
        self.mazeTable.setColumnCount(self.vel_tabulky)


        #tohle "naplní" prázná pole, aby se dala vybarvit
        for i in range(self.vel_tabulky):
            for j in range(self.vel_tabulky):
                self.mazeTable.setItem(i, j, QTableWidgetItem())


        #nastaví výšku a šířku bunek (section size), zmizí popisky po stranách (header)
        self.mazeTable.verticalHeader().setMaximumSectionSize(vel_ctverce)
        self.mazeTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.mazeTable.verticalHeader().setVisible(False)

        self.mazeTable.horizontalHeader().setMaximumSectionSize(vel_ctverce)
        self.mazeTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents )
        self.mazeTable.horizontalHeader().setVisible(False)
        
        #vlož do okénka a vycentruj
        self.layout = QGridLayout()
        self.layout.addWidget(self.mazeTable)
        self.setLayout(self.layout)

    # tady bude funkce na opravdové bludiště
    def createMaze(self):
        cell = self.mazeTable.item
        zasobnik = deque()
        cx = randint(self.vel_tabulky)
        cy = randint(self.vel_tabulky)


        self.mazeTable.item(self.x, self.y).setBackground(QBrush(QColor("black")))


def main():
    app = QApplication(sys.argv)
    maze = TTabulka()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

