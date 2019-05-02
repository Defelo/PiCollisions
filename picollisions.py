from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from physics import calculate_collision


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pi Collisions")
        self.setFixedSize(640, 480)

        self.m1: float = 1
        self.v1: float = 0
        self.x1: float = 150
        self.s1: int = 50

        self.m2: float = 100
        self.v2: float = -1
        self.x2: float = 300
        self.s2: int = 100

        self.timer = QBasicTimer()
        self.timer.start(20, self)

        self.counter = 0

        self.show()

    def timerEvent(self, e: QTimerEvent):
        if e.timerId() == self.timer.timerId():
            self.tick()
            self.repaint()

    def tick(self):
        self.x1 += self.v1
        self.x2 += self.v2

        if self.x1 <= 0:
            self.v1 *= -1
            self.counter += 1
        if self.x1 + self.s1 >= self.x2:
            self.v1, self.v2 = calculate_collision(self.m1, self.v1, self.m2, self.v2)
            self.counter += 1

    def keyReleaseEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Q:
            self.close()

    def paintEvent(self, _: QPaintEvent):
        qp: QPainter = QPainter(self)
        qp.setPen(Qt.white)
        qp.setBrush(Qt.white)
        qp.drawRect(self.rect())

        qp.setPen(QPen(Qt.black, 5))
        qp.drawLine(50, 0, 50, self.height())
        qp.drawLine(0, self.height() - 50, self.width(), self.height() - 50)

        qp.setPen(QPen(Qt.black, 2))
        qp.setBrush(QColor("#444444"))

        x1: int = max(int(self.x1), 0)
        qp.drawRect(50 + x1, self.height() - 52 - self.s1, self.s1, self.s1)
        qp.drawRect(50 + max(x1 + self.s1, int(self.x2)), self.height() - 52 - self.s2, self.s2, self.s2)

        f: QFont = QFont()
        f.setPixelSize(32)
        qp.setFont(f)
        t: str = str(self.counter)
        qp.drawText(self.width() - 10 - QFontMetrics(f).width(t), 32, t)


if __name__ == '__main__':
    qa: QApplication = QApplication([])
    w: Window = Window()
    qa.exec_()
