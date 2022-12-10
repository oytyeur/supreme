import matplotlib.pyplot as plt
from trajectoryGenerator import TrajectoryGenerator
from dataGenerator import DataGenerator
from straightLineEstimatorLSM import StraightLineEstimatorLSM
from matplotlib.widgets import Button, Slider


# Визуализация данных
def plot_data(data_gen):
    ax.plot(data_gen.messed_pts_x, data_gen.messed_pts_y, '.', markersize=5, color='0.6')
    # plt.xlim([-5, 5])
    # plt.ylim([-5, 5])
    plt.draw()


# Оценка траектории
def calc_results(data_gen):
    estimator = StraightLineEstimatorLSM(data_gen)
    estimator.estimate_traj(tol)
    traj_corners = estimator.calc_traj_corners()
    return traj_corners

# Визуализация результатов оценки траектории
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


# ===== ОБРАБОТЧИКИ СОБЫТИЙ =====

# При нажатии кнопки Next - сгенерировать новый датасет и оценить траекторию
def estimate_new_traj(event):
    global traj_gen
    global data_gen
    traj_gen = TrajectoryGenerator(ln_seg)
    data_gen = DataGenerator(traj_gen, mess)
    traj_corners = calc_results(data_gen)

    ax.clear()
    plot_data(data_gen)
    plot_results(traj_corners)


def reestimate(event):
    global tol
    tol = tol_sldr.val

    traj_corners = calc_results(data_gen)

    ax.clear()
    plot_data(data_gen)
    plot_results(traj_corners)


if __name__ == '__main__':
    ln_seg = 0.1  # периодичность "съёма измерений"
    mess = 0.25  # мера зашумлённости
    tol = 0.05  # допустимый порог вхождения точки в пределы отрезка

    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.8, bottom=0.3)

    estimate_new_traj(None)

    next_btn_ax = plt.axes([0.85, 0.4, 0.1, 0.05])
    next_btn = Button(next_btn_ax, 'Next')
    next_btn.on_clicked(estimate_new_traj)

    tol_sldr_ax = plt.axes([0.15, 0.1, 0.75, 0.05])
    tol_sldr = Slider(tol_sldr_ax,
                      label='Tolerance',
                      valmin=0.0,
                      valmax=0.25,
                      valinit=tol,
                      valstep=0.001)
    tol_sldr.on_changed(reestimate)

    plt.show()
