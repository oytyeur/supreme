import matplotlib.pyplot as plt
from random import randint, random, uniform
from math import pi, sin, cos
from line import Line


class TrajectoryGenerator:
    def __init__(self):
        # Координаты стартовой точки
        self.start_x = None
        self.start_y = None
        self.get_rand_start_pt()  # получение случайной стартовой точка
        # Параметры ломаной траектории
        self.seg_num = randint(4, 6)  # число сегментов траектории
        self.segments = []  # непосредственно сегменты
        # Создание ломаной траектории
        self.create_traj()

    # Метод для определения случайной стартовой точки траектории в области (определяет, если не определено)
    def get_rand_start_pt(self):
        if not self.start_x and not self.start_y:
            self.start_x = random()/2
            self.start_y = random()/2

    # Метод для продолжения ломаной траектории отрезком, следующим из предыдущей конечной точки
    def prolong_traj(self, start_pt):
        st_x, st_y = start_pt  # координаты начальной точки данного отрезка (конечной - предыдущего)
        length = uniform(0.25, 1.5)
        if not self.segments:  # если пустой список отрезков траектории, в любую сторону направляем первый
            angle = uniform(-pi, pi)
            end_x = st_x + length * cos(angle)
            end_y = st_y + length * sin(angle)
        else:  # если не пустой, поворачиваем отн. направления предыдущего на случайную величину из [-pi/2; pi/2]
            angle = uniform(-pi/2.0, pi/2.0)
            end_x = st_x + length * cos(self.segments[-1].alpha + angle)
            end_y = st_y + length * sin(self.segments[-1].alpha + angle)
            print(self.segments[-1].alpha)
        print(angle)
        print()
        self.segments.append(Line(start_pt, (end_x, end_y)))  # добавляем новый отрезок

    # Построение ломаной траектории путём последовательного присоединения отрезков
    def create_traj(self):
        start_pt = (self.start_x, self.start_y)
        for seg in range(self.seg_num):
            self.prolong_traj(start_pt)
            start_pt = (self.segments[-1].x2, self.segments[-1].y2)


tg = TrajectoryGenerator()

# print(tg.seg_num, tg.segments)
# print(tg.start_x, tg.start_y)

#################### ЗАПИХНУТЬ РИСОВАНИЕ В ОТДЕЛЬНУЮ ФУНКЦИЮ ##############
for seg in tg.segments:
    pts_x, pts_y, _ = seg.get_dotty()
    plt.plot(pts_x, pts_y)  # отображение прямой
    plt.plot(pts_x, pts_y, '.', color='0')  # отображение опорных точек (истинных)

plt.plot(tg.start_x, tg.start_y, 'r.')
plt.grid()
plt.show()

