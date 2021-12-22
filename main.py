import sys
from random import randint, choice
from _collections import deque

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QHeaderView, QFrame, QWidget, QTableWidget, QGridLayout, QPushButton, QLineEdit, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QColor, QIntValidator
from PyQt5.QtCore import QTimer, QEventLoop


class TBunka(QFrame):
    def __init__(self, x, y):
        super().__init__()  # inicializuj předka
        self.walls = {'T': True, 'B': True, 'L': True, 'R': True}
        self.visited = False
        self.x = x
        self.y = y
        self.way = False # myšleno finální cesta


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


    def right_way(self):
        self.way = True


    def wrong_way(self):
        self.way = False


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
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.tr("Velkolepé bludiště"))
        self.prepareForm()
        self.show()


    def prepareForm(self):
        self.layout = QGridLayout()
        self.horLayout = QHBoxLayout()

        # Create label (edited comment for git purspouse)
        self.label = QLabel("Table size:")
        self.horLayout.addWidget(self.label)

        # input window
        self.input = QLineEdit()
        self.input.setMaxLength(2)
        self.input.setValidator(QIntValidator())
        self.horLayout.addWidget(self.input)

        # Create pushbutton1
        self.bTable = QPushButton("Create table")
        self.bTable.clicked.connect(lambda: self.createTable())
        self.horLayout.addWidget(self.bTable)

        # Create pushbutton2
        self.bGenMaze = QPushButton("Generate maze")
        self.bGenMaze.clicked.connect(lambda: self.createMaze())
        self.horLayout.addWidget(self.bGenMaze)

        # Create pushbutton2
        self.bRun = QPushButton("Drop the mouse!")
        self.bRun.clicked.connect(lambda: self.solveMaze())
        self.horLayout.addWidget(self.bRun)

        self.layout.addLayout(self.horLayout, 0,0)
        self.setLayout(self.layout)


    def createTable(self):
        self.vel_tabulky = self.input.text()

        if self.vel_tabulky == "":
            QMessageBox.information(self,"Info","Zero sized table. Try it again.")
            self.prepareForm()
            return

        self.vel_tabulky = int(self.vel_tabulky)

        vel_ctverce = 50

        # Create table
        self.mazeTable = QTableWidget()
        self.mazeTable.setRowCount(self.vel_tabulky)
        self.mazeTable.setColumnCount(self.vel_tabulky)
        self.mazeTable.setShowGrid(False)
        self.mazeTable.setStyleSheet("background-color: white")

        # tohle "naplní" prázná pole, aby se dala vybarvit
        for i in range(self.vel_tabulky):
            for j in range(self.vel_tabulky):
                self.mazeTable.setCellWidget(i, j, TBunka(i,j))

        # nastaví výšku a šířku bunek (section size), zmizí popisky po stranách (header)
        self.mazeTable.verticalHeader().setMinimumSectionSize(vel_ctverce)
        self.mazeTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.mazeTable.verticalHeader().setVisible(False)

        self.mazeTable.horizontalHeader().setMinimumSectionSize(vel_ctverce)
        self.mazeTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.mazeTable.horizontalHeader().setVisible(False)

        # vlož do okénka a vycentruj
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


    def shorter_way(self, cx, cy):
        next_cell = 0
        nCell = self.mazeTable.cellWidget(cx - 1, cy)
        if nCell != None and nCell.way == True and nCell.has_wall("T") == False and nCell.visited == False:
            next_cell = nCell
        nCell = self.mazeTable.cellWidget(cx, cy - 1)
        if nCell != None and nCell.way == True and nCell.has_wall("L") == False and nCell.visited == False:
            next_cell = nCell
        nCell = self.mazeTable.cellWidget(cx + 1, cy)
        if nCell != None and nCell.way == True and nCell.has_wall("B") == False and nCell.visited == False:
            next_cell = nCell
        nCell = self.mazeTable.cellWidget(cx, cy + 1)
        if nCell != None and nCell.way == True and nCell.has_wall("R") == False and nCell.visited == False:
            next_cell = nCell
        return next_cell


    def wait(self):
        self.setWindowTitle(self.tr("Velkolepé bludiště         5"))
        self.delaly_program(1000)
        self.setWindowTitle(self.tr("Velkolepé bludiště         4"))
        self.delaly_program(1000)
        self.setWindowTitle(self.tr("Velkolepé bludiště         3"))
        self.delaly_program(1000)
        self.setWindowTitle(self.tr("Velkolepé bludiště         2"))
        self.delaly_program(1000)
        self.setWindowTitle(self.tr("Velkolepé bludiště         1"))
        self.delaly_program(1000)
        self.setWindowTitle(self.tr("Velkolepé bludiště"))


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
            self.delaly_program(100) #tím že program pozastavím dělá animaci
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


    def solveMaze(self):
        # stejný princip jako při tvoření bludiště
        # při tvoření se všechny bunky staly navštívenými, takže teď se jen rozhoduje opačně = vejdi pokud buňka byla navštívená a projitou označ nenavštívená
        zasobnik = deque()
        cx = randint(0, self.vel_tabulky - 1)  # current x/y
        cy = randint(0, self.vel_tabulky - 1)
        cCell = self.mazeTable.cellWidget(cx, cy)
        firstCell = cCell

        lx = randint(0, self.vel_tabulky - 1)  # last x/y
        ly = randint(0, self.vel_tabulky - 1)
        lCell = self.mazeTable.cellWidget(lx, ly)
        zasobnik.append(cCell)
        cCell.was_not_visited()

        while cCell != lCell:
            pn = self.possible_neighbours(cCell.x, cCell.y)
            if len(pn) == 0:
                cCell.wrong_way()
                cCell = zasobnik.pop()
                continue

            cCell.right_way()
            smer = choice(list(pn.keys()))  # vylosuj směr k jednomu z možných sousedů
            cCell = pn[smer]  # po směru se posunu na další = nová aktuální buňka
            zasobnik.append(cCell)  # novou buňku vložím do zásobníku
            cCell.was_not_visited()  # a označím jako nenavštívenou
        self.go_through_maze(firstCell, lCell)


    def go_through_maze(self, firstCell, lCell):
        cCell = firstCell
        cCell.setStyleSheet('background-image: url("mouse.png"); background-position: center; background-repeat: no-repeat')
        lCell.setStyleSheet('background-image: url("cheese.jpg"); background-position: center; background-repeat: no-repeat')
        self.wait()

        while cCell != 0:
            cCell.was_visited() # a označím jako navštívenou
            cCell.setStyleSheet('background-image: url("mouse.png"); background-position: center; background-repeat: no-repeat')
            self.delaly_program(500) #tím že program pozastavím dělá animaci
            cCell.setStyleSheet("background-color: lightgrey")
            cCell = self.shorter_way(cCell.x, cCell.y)

        lCell.setStyleSheet('background-image: url("mouse_and_cheese.jpg"); background-position: center; background-repeat: no-repeat')


def main():
    app = QApplication(sys.argv)
    maze = TOkenko()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()