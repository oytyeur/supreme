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

    # Вычисление вспомогательных сумм - требуются в вычислениях
    @staticmethod
    def calc_sums(segment_data):
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
    @staticmethod
    def calc_loss_func_argmin(segment_data):
        data_x, data_y = segment_data
        pts_num = len(data_x)
        x_sum, y_sum, xy_sum, x_sq_sum, y_sq_sum = StraightLineEstimatorLSM.calc_sums(segment_data)
        # Вычисление A для минимумов функции потерь
        phi = xy_sum - x_sum * y_sum / pts_num
        theta = (x_sq_sum - y_sq_sum) / phi + (y_sum ** 2 - x_sum ** 2) / (pts_num * phi)
        D = theta ** 2 + 4  # дискриминант
        A1 = (-theta + sqrt(D)) / 2
        A2 = (-theta - sqrt(D)) / 2
        # Вычисление С для минимумов функции потерь
        C1 = (y_sum - x_sum * A1) / pts_num
        C2 = (y_sum - x_sum * A2) / pts_num
        # Подстановка в функцию потерь, выявление лучшего
        lf1 = StraightLineEstimatorLSM.calc_loss_func(segment_data, A1, C1)
        lf2 = StraightLineEstimatorLSM.calc_loss_func(segment_data, A2, C2)
        # Выбор наименьшего значения функции потерь, возврат соответствующих ему параметров А и С
        if lf1 < lf2:
            return A1, C1
        else:
            return A2, C2

    # # Визуализация оценки траектории поверх данных: красная точка - начало, синяя - конец
    # @staticmethod
    # def plot_est_line(corners, fig, ax):
    #     # ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]])
    #     start_pt = corners[0]
    #     end_pt = corners[-1]
    #     for i in range(len(corners) - 1):
    #         x1 = corners[i][0]
    #         y1 = corners[i][1]
    #         x2 = corners[i+1][0]
    #         y2 = corners[i+1][1]
    #         ax.plot([x1, x2], [y1, y2])
    #
    #     ax.plot(start_pt[0], start_pt[1], 'r.')
    #     ax.plot(end_pt[0], end_pt[1], 'b.')
    #     fig.show()

    def __init__(self, data_genetator):
        self.data_x = data_genetator.messed_pts_x
        self.data_y = data_genetator.messed_pts_y
        self.data_length = len(self.data_x)
        self.last_end_idx = 0  # последний найденный конец отрезка
        self.est_segments_params_gen = []  # параметры оценок отрезков траектории в общей форме (A, C)

    # Оценка концов отрезка (среза данных для построения текущего отрезка),
    # чтобы использовать для оценки только потенциально принадлежащие текущему отрезку точки
    def calc_segment_data_edges(self, tolerance):
        # Срезы непроверенных данных
        rest_data_x = self.data_x[self.last_end_idx:]
        rest_data_y = self.data_y[self.last_end_idx:]
        # Объявление выходных наборов координат
        segment_data_x = []
        segment_data_y = []
        rest_pts_num = len(rest_data_x)  # число оставшихся точек
        # Если точек больше двух, строим прямую, оцениваем расстояние до третьей, сравниваем с tolerance
        if rest_pts_num > 2:
            segment_data_x.extend(rest_data_x[:2])  # первая пара принимается принадщлежной отрезку (чтобы больше одной)
            segment_data_y.extend(rest_data_y[:2])
            for i in range(rest_pts_num - 2):
                # По двум соседним точкам строим прямую
                line = Line((rest_data_x[i], rest_data_y[i]), (rest_data_x[i+1], rest_data_y[i+1]))
                # Определяем расстояние до этой прямой от следующей после пары точки
                dist = Line.calc_pt_dist_gen((rest_data_x[i+2], rest_data_y[i+2]), line.A, line.C)
                if dist <= tolerance:  # если меньше порога, относим к текущему отрезку
                    segment_data_x.append(rest_data_x[i+2])
                    segment_data_y.append(rest_data_y[i+2])
                    if i == rest_pts_num - 3:
                        self.last_end_idx += rest_pts_num
                else:  # иначе не относим определяем найденный конец отрезка, заканчиваем поиск
                    self.last_end_idx += i + 1
                    break
        # Если точек меньше трёх, то весть остаток принимается отрезком
        else:
            segment_data_x.extend(rest_data_x)
            segment_data_y.extend(rest_data_y)
            self.last_end_idx += rest_pts_num

        return segment_data_x, segment_data_y

    # Вычисление координат изломов траектории, а также начала и конца
    def calc_traj_corners(self):
        corners = []
        start_pt = (self.data_x[0], self.data_y[0])  # первая точка в данных
        end_pt = (self.data_x[-1], self.data_y[-1])  # последняя точка в данных
        # Параметры первого отрезка
        A1 = self.est_segments_params_gen[0][0]
        C1 = self.est_segments_params_gen[0][1]
        A2, C2 = Line.calc_normal(start_pt, A1, C1)  # вычисление перпендикуляра из первой точки к первому отрезку
        x, y = Line.calc_intersection(A1, C1, A2, C2)  # вычисление координат точки пересечения нормали и отрезка
        corners.append((x, y))  # добавление стартовой точки траектории
        # Вычисление углов пересечения отрезков
        for i in range(len(self.est_segments_params_gen) - 1):
            A1 = self.est_segments_params_gen[i][0]
            C1 = self.est_segments_params_gen[i][1]
            A2 = self.est_segments_params_gen[i+1][0]
            C2 = self.est_segments_params_gen[i+1][1]
            x, y = Line.calc_intersection(A1, C1, A2, C2)
            corners.append((x, y))

        # Параметры последнего отрезка
        A1 = self.est_segments_params_gen[-1][0]
        C1 = self.est_segments_params_gen[-1][1]
        A2, C2 = Line.calc_normal(end_pt, A1, C1)  # вычисление перпендикуляра из последней точки к последнему отрезку
        x, y = Line.calc_intersection(A1, C1, A2, C2)  # вычисление координат точки пересечения нормали и отрезка
        corners.append((x, y))  # добавление стартовой точки траектории

        return corners

    def estimate_traj(self, tolerance):
        while self.last_end_idx < self.data_length - 1:
            seg_data = self.calc_segment_data_edges(tolerance)
            est_A, est_C = StraightLineEstimatorLSM.calc_loss_func_argmin(seg_data)
            self.est_segments_params_gen.append((est_A, est_C))

            # est_k, est_b = Line.get_k_form(est_A, est_C)
