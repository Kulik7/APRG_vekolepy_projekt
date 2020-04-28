import sys
from random import randint, choice
from _collections import deque

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QApplication, QHeaderView, QFrame
from PyQt5.QtWidgets import QWidget, QAction, QTableWidget, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QPalette
from PyQt5.QtCore import QTimer, QEventLoop


class TBunka(QFrame):
    def __init__(self, x, y):
        super().__init__()  # inicializuj předka
        self.walls = {'T': True, 'B': True, 'L': True, 'R': True}
        self.visited = False
        self.x = x
        self.y = y

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

    def has_wall(self, smer):
        directions = {'T': "B", 'B': "T", 'L': "R", 'R': "L"}
        return self.walls[directions[smer]]

    def was_visited(self):
        self.visited = True

    def was_not_visited(self):
        self.visited = False


class TOkenko(QWidget):  # = objekt typu okénko
    def __init__(self):
        super().__init__()
        self.vel_tabulky = 5  # int(input("Ahoj jak složité bludiště si přeješ? (jakože počet čtverečků na čtvereček) "))
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.tr("Velkolepé bludiště"))
        self.createTable()
        self.resize(self.mazeTable.width(), self.mazeTable.height())
        self.show()
        self.createMaze()
        self.solveMaze()

    def createTable(self):
        vel_ctverce = 30

        # Create table
        self.mazeTable = QTableWidget()
        self.mazeTable.setRowCount(self.vel_tabulky)
        self.mazeTable.setColumnCount(self.vel_tabulky)
        self.mazeTable.setShowGrid(False)
        #self.mazeTable.setStyleSheet("background-color: white")

        # tohle "naplní" prázná pole, aby se dala vybarvit
        for i in range(self.vel_tabulky):
            for j in range(self.vel_tabulky):
                self.mazeTable.setCellWidget(i, j, TBunka(i,j))

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
        # získám slovník směrů s bunkami, kam se můžu vydat (Left, Right, Top, Bottom)
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

    def delaly_program(self, msec):
        self.timer = QtCore.QTimer()
        loop = QEventLoop()
        QTimer.singleShot(msec, loop.quit)
        loop.exec_()

    def createMaze(self):
        zasobnik = deque()
        cx = randint(0, self.vel_tabulky - 1)  # currentx/y
        cy = randint(0, self.vel_tabulky - 1)
        cCell = self.mazeTable.cellWidget(cx, cy)
        zasobnik.append(cCell)

        while len(zasobnik) != 0:
            cCell.setStyleSheet("background-color: pink")
            #self.delaly_program(100) #tím že program pozastavím dělá animaci
            cCell.setStyleSheet("background-color: white")
            un = self.unvisited_neighbours(cCell.x, cCell.y)
            if len(un) == 0:
                cCell = zasobnik.pop()
                continue
            smer = choice(list(un.keys()))  # vylosuj směr k jednomu z nenavštívených sousedů
            cCell.remove_wall(smer)  # probourám se na hranice k vedlejší buňce
            cCell = un[smer] # po směru se posunu na další = nová aktuální buňka
            zasobnik.append(cCell) # novou buňku vložím do zásobníku
            cCell.remove_new_wall(smer) # i v nové buňce probourám hranice
            cCell.was_visited() # a označím jako navštívenou


    def possible_neighbours(self, cx, cy):
        # zkoumám kolika buňkami se můžu vydat
        neigbours = {}
        nCell = self.mazeTable.cellWidget(cx - 1, cy)
        if nCell != None and nCell.has_wall("T") == False and nCell.visited == True:
            neigbours["T"] = nCell
        nCell = self.mazeTable.cellWidget(cx, cy - 1)
        if nCell != None and nCell.has_wall("L") == False and nCell.visited == True:
            neigbours["L"] = nCell
        nCell = self.mazeTable.cellWidget(cx + 1, cy)
        if nCell != None and nCell.has_wall("B") == False and nCell.visited == True:
            neigbours["B"] = nCell
        nCell = self.mazeTable.cellWidget(cx, cy + 1)
        if nCell != None and nCell.has_wall("R") == False and nCell.visited == True:
            neigbours["R"] = nCell
        return neigbours

    def solveMaze(self):
        # stejný princip jako při tvoření bludiště
        # při tvoření se všechny bunky staly navštívenými, takže teď se jen rozhoduje opačně = vejdi pokud buňka byla navštívená a projitou označ nenavštívená
        zasobnik = deque()
        cx = randint(0, self.vel_tabulky - 1)  # first x/y
        cy = randint(0, self.vel_tabulky - 1)
        cCell = self.mazeTable.cellWidget(cx, cy)
        cCell.setStyleSheet("background-color: violet")

        lx = randint(0, self.vel_tabulky - 1)  # last x/y
        ly = randint(0, self.vel_tabulky - 1)
        lCell = self.mazeTable.cellWidget(lx, ly)
        lCell.setStyleSheet("background-color: blue")
        zasobnik.append(cCell)

        while cCell != lCell:
            cCell.setStyleSheet("background-color: red")
            self.delaly_program(500)  # tím že program pozastavím dělá animaci
            cCell.setStyleSheet("background-color: pink")
            pn = self.possible_neighbours(cCell.x, cCell.y)
            if len(pn) == 0:
                cCell = zasobnik.pop()
                continue

            smer = choice(list(pn.keys()))  # vylosuj směr k jednomu z možných sousedů
            cCell = pn[smer]  # po směru se posunu na další = nová aktuální buňka
            zasobnik.append(cCell)  # novou buňku vložím do zásobníku
            cCell.was_not_visited()  # a označím jako nenavštívenou
        lCell.setStyleSheet("background-color: violet")


def main():
    app = QApplication(sys.argv)
    maze = TOkenko()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

#upravit velikost okna podle tabulky
#reakce na stisknutí tlačítka
#vložit obrázek myšky a sýra(nebo cokoliv)