import math
from math import sqrt, atan2, sin, cos


class Line:
    ln_seg = 0.1 # промежуток длины, на которые разбивается отрезок

    # конструктор класса - объявление прямой по 2 точкам
    def __init__(self, pt1, pt2):
        x1, y1 = pt1
        x2, y2 = pt2
        # точка 1
        self.x1 = x1
        self.y1 = y1
        # точка 2
        self.x2 = x2
        self.y2 = y2
        # параметры для формы y = kx + b
        if x1 == x2:
            self.has_general = False  # флаг о возможности полной общей формы уравнения
        else:
            self.k = (y2 - y1)/(x2 - x1)
            self.has_general = True

        self.b = y1 - x1
        # параметры для общей формы Ax + By + C = 0
        if self.has_general:
            self.A = self.k
            self.B = -1
            self.C = self.b
        else:  # форма x = const
            self.A = -1
            self.C = x1
        # длина отрезка
        self.length = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # угол наклона [рад]
        self.alpha = atan2(y2-y1, x2-x1)

    # метод расчёта расстояния от точки до прямой
    def pt_dist(self, pt):
        xp, yp = pt
        if self.has_general:
            distance = abs(xp*self.A + yp*self.B + self.C)/sqrt(self.A ** 2 + self.B ** 2)
        else:
            distance = abs(xp - self.C)
        return distance

    # метод, возвращающий значение y по значению x
    def get_y(self, x):
        if self.has_general:
            y = self.k * x + self.b
        else:
            return None

    # метод, разбивающий отрезок на точки и возвращающий списки координат этих точек и их число
    def get_dotty(self):
        pts_num = int(self.length / Line.ln_seg) + 1  # число вхождения целых сегментов длины ln_seg + нулевая точка
        pts_x = [self.x1]
        pts_y = [self.y1]

        for i in range(1, pts_num):  # вычисление координат каждой такой точки
            pts_x.append(pts_x[-1] + Line.ln_seg * cos(self.alpha))
            pts_y.append(pts_y[-1] + Line.ln_seg * sin(self.alpha))

        # для закрепления концевой точки
        pts_x.append(self.x2)
        pts_y.append(self.y2)

        return pts_x, pts_y, pts_num + 1  # плюс закреплённая конечная точка


p1 = (0, 0)
p2 = (-1, 1)
line = Line(p1, p2)
# print(line.x1, line.y1, line.x2, line.y2, line.k, line.b)
print(line.alpha)
# p = (76.08, 0)
# print(line.get_y(10))



