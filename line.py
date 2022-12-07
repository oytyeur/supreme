import math
from math import inf, sqrt, atan2, sin, cos


class Line:
    # Конструктор класса - объявление прямой по 2 точкам
    def __init__(self, pt1, pt2):
        x1, y1 = pt1
        x2, y2 = pt2
        # Точка 1 (начало)
        self.x1 = x1
        self.y1 = y1
        # Точка 2 (конец)
        self.x2 = x2
        self.y2 = y2
        # Параметры для формы y = kx + b
        if x1 == x2:
            self.is_x_const = True  # флаг формы y = kx + b (k != inf)
            self.k = inf
            self.b = None
        else:
            self.is_x_const = False
            self.k = (y2 - y1)/(x2 - x1)
            self.b = y1 - self.k * x1

        # Параметры для общей формы Ax + By + C = 0
        if not self.is_x_const:
            self.A = self.k
            self.B = -1
            self.C = self.b
        else:  # форма x = const
            self.A = -1
            self.B = 0
            self.C = x1
        # длина отрезка
        self.length = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # угол наклона [рад]
        self.alpha = atan2(y2-y1, x2-x1)

    # Метод расчёта расстояния от точки до прямой (как раз для этого и нужна общая форма уравнения прямой)
    def pt_dist(self, pt):
        xp, yp = pt
        # if self.is_x_dependent:
        #     distance = abs(xp*self.A + yp*self.B + self.C)/sqrt(self.A ** 2 + self.B ** 2)
        # else:
        #     distance = abs(xp - self.C)
        distance = abs(xp * self.A + yp * self.B + self.C) / sqrt(self.A ** 2 + self.B ** 2)
        return distance

    # Метод, возвращающий значение y по значению x
    def get_y(self, x):
        if not self.is_x_const:
            y = self.k * x + self.b
            return y
        else:
            return None

    # Метод, разбивающий отрезок на точки и возвращающий списки координат этих точек и их число
    def get_dotty(self, ln_seg):
        pts_num = int(self.length / ln_seg) + 1  # число вхождения целых сегментов длины ln_seg + нулевая точка
        pts_x = [self.x1]
        pts_y = [self.y1]

        for i in range(1, pts_num):  # вычисление координат каждой такой точки
            pts_x.append(pts_x[-1] + ln_seg * cos(self.alpha))
            pts_y.append(pts_y[-1] + ln_seg * sin(self.alpha))

        # Для закрепления концевой точки
        pts_x.append(self.x2)
        pts_y.append(self.y2)

        return pts_x, pts_y, pts_num + 1  # плюс закреплённая конечная точка


# ln = Line((1, 0), (1, 1))
# print(ln.k, ln.b, ln.A, ln.B, ln.C)
# print(ln.pt_dist((3,1)))
# ln = Line((0, 0), (1, 1))
# print(ln.k, ln.b, ln.A, ln.B, ln.C)
