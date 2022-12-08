import matplotlib.pyplot as plt
from line import Line
from trajectoryGenerator import TrajectoryGenerator
from dataGenerator import DataGenerator


class LeastSquares:
    def __init__(self, data):
        self.data_x, self.data_y = data
        self.pts_num = len(self.data_x)
        # self.start_pt, self.end_pt, self.est_line = self.get_init_estimation()
        self.est_line = None
        self.get_init_estimation()

    # Первичная оценка прямой: берётся первая и последняя точки данных, по ним строится прямая
    def get_init_estimation(self):
        start_pt = (self.data_x[0], self.data_y[0])  # начальная точка
        end_pt = (self.data_x[-1], self.data_y[-1])  # конечная точка
        self.est_line = Line(start_pt, end_pt)  # отрезок (включает параметры прямой, которые и будем оценивать)
        return start_pt, end_pt

    # # Оценка концов отрезка (среза данных для построения текущего отрезка),
    # # чтобы использовать только потенциально принадлежащие текущему отрезку точки
    # def estimate_edges(self, tolerance):
    #     return seg_data

    # Получение текущего значения функции потерь (сумма квадратов расстояний от точек данных до текущей оценки прямой)
    def get_loss_func(self, segment_data):
        segment_data_x, segment_data_y = segment_data
        loss_func_value = 0
        for xp, yp in zip(segment_data_x, segment_data_y):
            pt = xp, yp
            dist = self.est_line.pt_dist(pt)
            loss_func_value += dist ** 2
        return loss_func_value

    # Вычисление вспомогательных сумм - требуются в вычислениях
    def calc_sums(self):
        x_sum = 0  # сумма всех х координат
        y_sum = 0  # сумма всех у координат
        xy_sum = 0  # сумма произведений всех х и всех у координат соответственно (ху)
        x_sq_sum = 0  # сумма квадратов всех координат х
        y_sq_sum = 0  # сумма квадратов всех координат у
        for i in range(self.pts_num):
            x_sum += self.data_x[i]
            y_sum += self.data_y[i]
            xy_sum += self.data_x[i] * self.data_y[i]
            x_sq_sum += self.data_x[i] ** 2
            y_sq_sum += self.data_y[i] ** 2
        return x_sum, y_sum, xy_sum, x_sq_sum, y_sq_sum

    # Визуализация оценки траектории поверх данных: красная точка - начало, синяя - конец
    def plot_est_line(self, fig, ax):
        ax.plot([self.est_line.x1, self.est_line.x2], [self.est_line.y1, self.est_line.y2])
        ax.plot(self.est_line.x1, self.est_line.y1, 'r.')
        ax.plot(self.est_line.x2, self.est_line.y2, 'b.')
        fig.show()


ln_seg = 0.1
mess = 0.75

tg = TrajectoryGenerator(ln_seg)
dg = DataGenerator(tg, mess)
data = dg.messed_pts_x, dg.messed_pts_y
lsm = LeastSquares(data)

#_, _, est_line = lsm.get_init_estimation()
lf_val = lsm.get_loss_func(data)
# print(lf_val)

idl_k = tg.segments[0].k
idl_b = tg.segments[0].b

est_k = lsm.est_line.k
est_b = lsm.est_line.b

# print(idl_k, idl_b)
# print(est_k, est_b)

print(lsm.calc_sums())

t_fig, t_ax = tg.plot_traj()
d_fig, d_ax = dg.plot_data()

lsm.plot_est_line(d_fig, d_ax)
plt.show()
