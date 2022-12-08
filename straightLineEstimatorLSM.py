import matplotlib.pyplot as plt
from math import sqrt
from line import Line
from trajectoryGenerator import TrajectoryGenerator
from dataGenerator import DataGenerator


class StraightLineEstimatorLSM:
    # Получение текущего значения функции потерь (сумма квадратов расстояний от точек данных до текущей оценки прямой)
    @staticmethod
    def calc_loss_func(segment_data, A, C):
        data_x, data_y = segment_data
        loss_func_value = 0
        for xp, yp in zip(data_x, data_y):
            pt = xp, yp
            dist = Line.calc_pt_dist_gen(pt, A, C)
            loss_func_value += dist ** 2
        return loss_func_value

    def __init__(self, data):
        self.data_x, self.data_y = data

    # # Оценка концов отрезка (среза данных для построения текущего отрезка),
    # # чтобы использовать только потенциально принадлежащие текущему отрезку точки
    # def estimate_edges(self, tolerance):
    #     return segment_data

    # Вычисление вспомогательных сумм - требуются в вычислениях
    def calc_sums(self, segment_data):
        data_x, data_y = segment_data
        pts_num = len(data_x)
        x_sum = 0  # сумма всех х координат
        y_sum = 0  # сумма всех у координат
        xy_sum = 0  # сумма произведений всех х и всех у координат соответственно (ху)
        x_sq_sum = 0  # сумма квадратов всех координат х
        y_sq_sum = 0  # сумма квадратов всех координат у
        for i in range(pts_num):
            x_sum += data_x[i]
            y_sum += data_y[i]
            xy_sum += data_x[i] * data_y[i]
            x_sq_sum += data_x[i] ** 2
            y_sq_sum += data_y[i] ** 2
        return x_sum, y_sum, xy_sum, x_sq_sum, y_sq_sum

    # Вычисление аргументов (A, C) для минимума функции потерь
    def calc_loss_func_min_args(self, segment_data):
        data_x, data_y = segment_data
        pts_num = len(data_x)
        x_sum, y_sum, xy_sum, x_sq_sum, y_sq_sum = self.calc_sums(segment_data)
        # Вычисление A для минимумов функции потерь
        phi = xy_sum - x_sum * y_sum / pts_num
        theta = (x_sq_sum - y_sq_sum) / phi + (y_sum ** 2 - x_sum ** 2) / (pts_num * phi)
        D = theta ** 2 + 4  # дискриминант
        A1 = (-theta + sqrt(D))/2
        A2 = (-theta - sqrt(D))/2
        # Вычисление С для минимумов функции потерь
        C1 = (y_sum - x_sum * A1) / pts_num
        C2 = (y_sum - x_sum * A2) / pts_num
        # Подстановка в функцию потерь, выявление лучшего
        lf1 = StraightLineEstimatorLSM.calc_loss_func(segment_data, A1, C1)
        lf2 = StraightLineEstimatorLSM.calc_loss_func(segment_data, A2, C2)
        print(lf1, lf2)
        # Выбор наименьшего значения функции потерь, возврат соответствующих ему параметров А и С
        if lf1 < lf2:
            return A1, C1
        else:
            return A2, C2

    # Визуализация оценки траектории поверх данных: красная точка - начало, синяя - конец
    def plot_est_line(self, pt1, pt2, fig, ax):
        ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]])
        ax.plot(pt1[0], pt1[1], 'r.')
        ax.plot(pt2[0], pt2[1], 'b.')
        fig.show()


ln_seg = 0.1
mess = 1

tg = TrajectoryGenerator(ln_seg)
dg = DataGenerator(tg, mess)
seg_data = dg.messed_pts_x, dg.messed_pts_y
lsm = StraightLineEstimatorLSM(seg_data)

est_A, est_C = lsm.calc_loss_func_min_args(seg_data)
est_k, est_b = Line.get_k_form(est_A, est_C)

st = (seg_data[0][0], est_k * seg_data[0][0] + est_b)
end = (seg_data[0][-1], est_k * seg_data[0][-1] + est_b)

# start_pt, end_pt = lsm.get_init_estimation()
# ln = Line(start_pt, end_pt)
# est_k, est_b = Line.get_k_form(ln.A, ln.C)
# lf_val = LeastSquares.calc_loss_func(data, ln.A, ln.C)
# print(lf_val)
#
idl_k = tg.segments[0].k
idl_b = tg.segments[0].b

print(idl_k, idl_b)
print(est_k, est_b)

# print(lsm.calc_sums())
#
t_fig, t_ax = tg.plot_traj()
d_fig, d_ax = dg.plot_data()
lsm.plot_est_line(st, end, d_fig, d_ax)
lsm.plot_est_line(st, end, t_fig, t_ax)
plt.show()
