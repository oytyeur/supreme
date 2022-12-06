import matplotlib.pyplot as plt
from math import sqrt, sin, cos
from random import normalvariate
from line import Line


pt1 = (-1, 1)
pt2 = (1, 0)
line = Line(pt1, pt2)
pts_x, pts_y, pts_num = line.get_dotty()

mess = 0.25  # мера разброса? пусть будет СКО (для нормально распределённого шума)
messed_pts_x = []
messed_pts_y = []

for pt in range(pts_num):
    x_offset = 0
    y_offset = 0
    course_offset = normalvariate(0.0, mess*Line.ln_seg)
    side_offset = normalvariate(0.0, mess*Line.ln_seg)
    x_offset += course_offset * cos(line.alpha) - side_offset * sin(line.alpha)
    y_offset += course_offset * sin(line.alpha) + side_offset * cos(line.alpha)
    messed_pts_x.append(pts_x[pt] + x_offset)
    messed_pts_y.append(pts_y[pt] + y_offset)

# print(line.k, line.b, line.alpha)
print(line.length, pts_num)

plt.plot(pts_x, pts_y)  # отображение прямой
plt.plot(pts_x, pts_y, '.', color='0')  # отображение опорных точек (истинных)
plt.plot(messed_pts_x, messed_pts_y, '.', color='0.6')  # отображение смещённых точек (зашумлённых)
plt.plot(line.x1, line.x2, 'r.')
plt.show()


