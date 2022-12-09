import matplotlib.pyplot as plt
from trajectoryGenerator import TrajectoryGenerator
from dataGenerator import DataGenerator
from straightLineEstimatorLSM import StraightLineEstimatorLSM
from matplotlib.widgets import Button, Slider


global ln_seg
global mess
global tol

global fig
global ax


def plot_data(data_generator):
    ax.plot(data_generator.messed_pts_x, data_generator.messed_pts_y, '.', markersize=5, color='0.6')
    plt.draw()


def plot_results(corners):
    start_pt = corners[0]
    end_pt = corners[-1]
    for i in range(len(corners) - 1):
        x1 = corners[i][0]
        y1 = corners[i][1]
        x2 = corners[i + 1][0]
        y2 = corners[i + 1][1]
        ax.plot([x1, x2], [y1, y2])
    ax.plot(start_pt[0], start_pt[1], 'r.')
    ax.plot(end_pt[0], end_pt[1], 'b.')


def approximate_new_traj(event):
    ax.clear()

    traj_generator = TrajectoryGenerator(ln_seg)
    data_generator = DataGenerator(traj_generator, mess)
    plot_data(data_generator)

    lsm = StraightLineEstimatorLSM(data_generator)
    lsm.estimate_traj(tol)
    traj_corners = lsm.calc_traj_corners()
    plot_results(traj_corners)


if __name__ == '__main__':
    ln_seg = 0.1  # периодичность "съёма измерений"
    mess = 0.2  # мера зашумлённости
    tol = 0.05  # допустимый порог вхождения точки в пределы отрезка

    # tg = TrajectoryGenerator(ln_seg)  # генерация траектории

    # dg = DataGenerator(tg, mess)  # генерация зашумлённых данных

    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.8, bottom=0.3)

    approximate_new_traj(None)

    next_btn_ax = plt.axes([0.85, 0.4, 0.1, 0.05])
    next_btn = Button(next_btn_ax, 'Next')

    next_btn.on_clicked(approximate_new_traj)

    plt.show()
