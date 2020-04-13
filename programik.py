import sys
from random import randint, choice
from _collections import deque

from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QApplication, QHeaderView, QFrame
from PyQt5.QtWidgets import QWidget, QAction, QTableWidget, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QPalette
from PyQt5.QtCore import QTimer


class TBunka(QFrame):
    def __init__(self, x, y):
        super().__init__()  # inicializuj předka
        self.walls = {'T': True, 'B': True, 'L': True, 'R': True}
        self.visited = False
        self.x = x
        self.y = y
        # self.walls[wall] = False
        # other.walls[Cell.wall_pairs[wall]] = False

    # self.setFrameShape(QFrame)

    def paintEvent(self, event):
        QFrame.paintEvent(self, event)
        p = QtGui.QPainter(self)
        pblack = QtGui.QPen(QColor("black"))
        pwhite = QtGui.QPen(QColor("white"))
        rect = QFrame.contentsRect(self)

        for wall in self.walls:
            if self.walls[wall] == True:
                p.setPen(pblack)
            else:
                p.setPen(pwhite)

            if wall == "T":
                # čára z prava do leva
                p.drawLine(rect.topLeft(), rect.topRight())
            elif wall == "B":
                p.drawLine(rect.bottomLeft(), rect.bottomRight())
            elif wall == "R":
                p.drawLine(rect.topRight(), rect.bottomRight())
            else:
                p.drawLine(rect.bottomLeft(), rect.topLeft())

    def remove_new_wall(self, smer):
        directions = {'T': "B", 'B': "T", 'L': "R", 'R': "L"}
        self.walls[directions[smer]] = False

    def remove_wall(self, smer):
        self.walls[smer] = False

    def was_visited(self):
        self.visited = True


class TOkenko(QWidget):  # = objekt typu okénko
    def __init__(self):
        super().__init__()

        self.vel_tabulky = 10  # int(input("Ahoj jak složité bludiště si přeješ? (jakože počet čtverečků na čtvereček) "))

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.tr("Velolepé bludiště"))
        self.createTable()
        self.show()
        self.createMaze()

    def createTable(self):
        vel_ctverce = 30

        # Create table
        self.mazeTable = QTableWidget()
        self.mazeTable.setRowCount(self.vel_tabulky)
        self.mazeTable.setColumnCount(self.vel_tabulky)
        self.mazeTable.setShowGrid(False)

        # tohle "naplní" prázná pole, aby se dala vybarvit
        for i in range(self.vel_tabulky):
            for j in range(self.vel_tabulky):
                # self.mazeTable.setItem(i, j, QTableWidgetItem())
                self.mazeTable.setCellWidget(i, j, TBunka(i,
                                                          j))

        # nastaví výšku a šířku bunek (section size), zmizí popisky po stranách (header)
        self.mazeTable.verticalHeader().setMaximumSectionSize(vel_ctverce)
        self.mazeTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.mazeTable.verticalHeader().setVisible(False)

        self.mazeTable.horizontalHeader().setMaximumSectionSize(vel_ctverce)
        self.mazeTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.mazeTable.horizontalHeader().setVisible(False)

        # vlož do okénka a vycentruj
        self.layout = QGridLayout()
        self.layout.addWidget(self.mazeTable)
        self.setLayout(self.layout)

    def unvisited_neighbours(self, cx, cy):
        # zkoumám kolik neighbouring cells = nCell patří do unvisited neighbours
        neigbours = {}
        nCell = self.mazeTable.cellWidget(cx - 1, cy)
        if nCell != None and nCell.visited == False:
            neigbours["T"] = nCell
        nCell = self.mazeTable.cellWidget(cx, cy - 1)
        if nCell != None and nCell.visited == False:
            neigbours["L"] = nCell
        nCell = self.mazeTable.cellWidget(cx + 1, cy)
        if nCell != None and nCell.visited == False:
            neigbours["B"] = nCell
        nCell = self.mazeTable.cellWidget(cx, cy + 1)
        if nCell != None and nCell.visited == False:
            neigbours["R"] = nCell
        return neigbours

    def createMaze(self):
        zasobnik = deque()
        cx = randint(0, self.vel_tabulky - 1)  # currentx/y
        cy = randint(0, self.vel_tabulky - 1)
        cCell = self.mazeTable.cellWidget(cx, cy)
        zasobnik.append(cCell)

        while len(zasobnik) != 0:
            # cCell.setStyleSheet("background-color: pink;")
            un = self.unvisited_neighbours(cCell.x, cCell.y)
            if len(un) == 0:
                cCell = zasobnik.pop()
                continue
            smer = choice(list(un.keys()))  # vylosuj směr k jednomu z nenavštívených sousedů
            cCell.remove_wall(smer)  # probourám se na hranice k vedlejší buňce
            cCell = un[smer]  # po směru se posunu na další = nová aktuální buňka
            zasobnik.append(cCell)  # novou buňku vložím do zásobníku
            cCell.remove_new_wall(smer)  # i v nové buňce probourám hranice
            cCell.was_visited()  # a označím jako navštívenou


def main():
    app = QApplication(sys.argv)
    maze = TOkenko()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

