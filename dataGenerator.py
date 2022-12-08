import matplotlib.pyplot as plt
from math import sqrt, sin, cos
from random import normalvariate
from trajectoryGenerator import TrajectoryGenerator


class DataGenerator:
    def __init__(self, traj_gen, mess):
        self.traj_gen = traj_gen  # сгенерированная траектория
        self.mess = mess  # мера беспорядка, пусть будет 3 x СКО (правило трёх сигм) для нормально распределённого шума
        self.messed_pts_x, self.messed_pts_y = self.mess_up()

    # Зашумление точек и помещение координат всех отрезков в единые списки (по осям х и у)
    def mess_up(self):
        messed_pts_x = []
        messed_pts_y = []
        for seg in self.traj_gen.segments:
            pts_x, pts_y, pts_num = seg.get_dotty(self.traj_gen.ln_seg)  # разбиений отрезка (дискретизация)
            for pt in range(pts_num):
                x_offset = 0  # смещение по оси х
                y_offset = 0  # смещение по оси у
                course_offset = normalvariate(0.0, self.mess * self.traj_gen.ln_seg/3)  # смещение по курсу
                side_offset = normalvariate(0.0, self.mess * self.traj_gen.ln_seg/3)  # смещение по борту
                # Переход от системы координат объекта, к системе координат мира
                x_offset += course_offset * cos(seg.alpha) - side_offset * sin(seg.alpha)
                y_offset += course_offset * sin(seg.alpha) + side_offset * cos(seg.alpha)
                messed_pts_x.append(pts_x[pt] + x_offset)
                messed_pts_y.append(pts_y[pt] + y_offset)
        return messed_pts_x, messed_pts_y

    # Визуализация зашумлённых данных
    def plot_data(self):
        fig, ax = plt.subplots()
        ax.plot(self.messed_pts_x, self.messed_pts_y, '.', markersize=5, color='0.6')
        # ax.axis('scaled')
        fig.show()
        return fig, ax


