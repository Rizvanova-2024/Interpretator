from PyQt5.QtGui import (
    QPaintEvent, 
    QPainter,
    QBrush,
    QColor
)
from PyQt5.QtWidgets import QWidget

class FieldPainter(QWidget):
    position = [0, 0]
    def __init__(self, parent : QWidget) -> None:
        super().__init__(parent)
        self.move(450, 60)
        self.resize(425, 425)
    
    def paintEvent(self, event: QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)
        # Drawing grid
        for y in range(21):
            for x in range(21):
                if x == self.position[0] and y == self.position[1]:
                    qp.setBrush(QBrush(QColor(255, 0, 0)))
                else:
                    qp.setBrush(QBrush(QColor(255, 255, 255)))
                qp.drawRect(x*20, y*20, 20, 20)
        qp.end()

    def CanMoveDown(self) -> bool:
        return self.position[1] != 20
    
    def CanMoveUp(self) -> bool:
        return self.position[1] != 0
    
    def CanMoveLeft(self) -> bool:
        return self.position[0] != 0
    
    def CanMoveRight(self) -> bool:
        return self.position[0] != 20
        
    def MoveRight(self) -> None:
        if self.position[0] < 20:
            self.position[0] += 1
            self.update()

    def MoveLeft(self) -> None:
        if self.position[0] > 0:
            self.position[0] -= 1
            self.update()

    def MoveDown(self) -> None:
        if self.position[1] < 20:
            self.position[1] += 1
            self.update()

    def MoveUp(self) -> None:
        if self.position[1] > 0:
            self.position[1] -= 1
            self.update()

    def Reset(self):
        self.position = [0, 0]
        self.update()



if __name__ == "__main__":
    print('This module can\'t be executed')
    exit(1)