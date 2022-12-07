import matplotlib.pyplot as plt
from line import Line
from trajectoryGenerator import TrajectoryGenerator
from dataGenerator import DataGenerator


class LeastSquares:
    def __init__(self, data):
        self.data_x, self.data_y = data
        # self.start_pt, self.end_pt, self.est_line = self.get_init_estimation()
        self.est_line = None

    # Первичная оценка прямой: берётся первая и последняя точки данных, по ним строится прямая
    def get_init_estimation(self):
        start_pt = (self.data_x[0], self.data_y[0])  # начальная точка
        end_pt = (self.data_x[-1], self.data_y[-1])  # конечная точка
        line = Line(start_pt, end_pt)  # отрезок (включает параметры прямой, которые и будем оценивать)
        return start_pt, end_pt, line

    # # Оценка концов отрезка (среза данных для построения текущего отрезка),
    # # чтобы использовать только потенциально принадлежащие текущему отрезку точки
    # def estimate_edges(self, tolerance):
    #     return seg_data

    # Получение текущего значения функции потерь (сумма квадратов расстояний от точек данных до текущей оценки прямой)
    def get_loss_func(self, line, segment_data):
        segment_data_x, segment_data_y = segment_data
        loss_func_value = 0
        for xp, yp in zip(segment_data_x, segment_data_y):
            pt = xp, yp
            dist = line.pt_dist(pt)
            loss_func_value += dist ** 2
        return loss_func_value

    # Визуализация оценки траектории поверх данных: красная точка - начало, синяя - конец
    def plot_est_line(self, line, fig, ax):
        ax.plot([line.x1, line.x2], [line.y1, line.y2])
        ax.plot(line.x1, line.y1, 'r.')
        ax.plot(line.x2, line.y2, 'b.')
        fig.show()


ln_seg = 0.1
mess = 0.75

tg = TrajectoryGenerator(ln_seg)
dg = DataGenerator(tg, mess)
data = dg.messed_pts_x, dg.messed_pts_y
lsm = LeastSquares(data)

_, _, est_line = lsm.get_init_estimation()
lf_val = lsm.get_loss_func(est_line, data)
print(lf_val)

idl_k = tg.segments[0].k
idl_b = tg.segments[0].b

est_k = est_line.k
est_b = est_line.b

print(idl_k, idl_b)
print(est_k, est_b)

t_fig, t_ax = tg.plot_traj()
d_fig, d_ax = dg.plot_data()

lsm.plot_est_line(est_line, d_fig, d_ax)
plt.show()
