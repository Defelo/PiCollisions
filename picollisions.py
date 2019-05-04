from decimal import Decimal

from PyQt5.QtCore import Qt, QBasicTimer, QTimerEvent
from PyQt5.QtGui import QPainter, QPaintEvent, QKeyEvent, QPen, QColor, QFont, QFontMetrics
from PyQt5.QtWidgets import QWidget, QApplication

from physics import calculate_collision


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pi Collisions")
        self.setFixedSize(640, 480)

        self.m1: int = 1
        self.v1: Decimal = Decimal(0)
        self.x1: Decimal = Decimal(150)
        self.s1: int = 50

        self.m2: int = 100 ** 1
        self.v2: Decimal = Decimal(-1)
        self.x2: Decimal = Decimal(300)
        self.s2: int = 100

        self.t: Decimal = Decimal(0)
        self.wall: bool = False

        self.timer: QBasicTimer = QBasicTimer()
        self.timer.start(20, self)

        self.counter: int = 0

        self.show()

    def timerEvent(self, e: QTimerEvent):
        if e.timerId() == self.timer.timerId():
            self.tick()
            self.repaint()

    def tick(self):
        target_time: Decimal = self.t + 1

        while self.t < target_time:
            if 0 <= self.v1 <= self.v2:
                self.x1 += self.v1
                self.x2 += self.v2
                self.t += 1
                break
            if self.wall:
                # left block collides with wall
                time_wall_collision: Decimal = self.x1 / -self.v1
                if time_wall_collision > 1:
                    self.x1 += self.v1
                    self.x2 += self.v2
                    self.t += 1
                    break
                self.x1 += time_wall_collision * self.v1
                self.x2 += time_wall_collision * self.v2
                self.v1 *= -1
                self.t += time_wall_collision
            else:
                # blocks collide with each other
                time_block_collision: Decimal = (self.s1 + self.x1 - self.x2) / (self.v2 - self.v1)
                if time_block_collision > 1:
                    self.x1 += self.v1
                    self.x2 += self.v2
                    self.t += 1
                    break
                self.x1 += time_block_collision * self.v1
                self.x2 += time_block_collision * self.v2
                self.v1, self.v2 = calculate_collision(self.m1, self.v1, self.m2, self.v2)
                self.t += time_block_collision
            self.counter += 1
            self.wall = not self.wall

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

        qp.drawRect(50 + int(self.x1), self.height() - 52 - self.s1, self.s1, self.s1)
        qp.drawRect(50 + int(self.x2), self.height() - 52 - self.s2, self.s2, self.s2)

        f: QFont = QFont()
        f.setPixelSize(32)
        qp.setFont(f)
        t: str = str(self.counter)
        qp.drawText(self.width() - 10 - QFontMetrics(f).width(t), 32, t)

        f.setPixelSize(20)
        qp.setFont(f)
        t: str = f"{self.v1:.2f}"
        w: int = QFontMetrics(f).width(t)
        qp.drawText(50 + int(self.x1) + self.s1 // 2 - w // 2, self.height() - 60 - self.s1, t)
        t: str = f"{self.v2:.2f}"
        w: int = QFontMetrics(f).width(t)
        qp.drawText(50 + int(self.x2) + self.s2 // 2 - w // 2, self.height() - 60 - self.s2, t)


if __name__ == '__main__':
    qa: QApplication = QApplication([])
    w: Window = Window()
    qa.exec_()
