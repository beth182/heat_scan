import numpy as np
from scipy.interpolate import CubicHermiteSpline
import matplotlib.pyplot as plt
import os
import matplotlib as mpl

mpl.rcParams.update({'font.size': 15})

# eye-ball turning-point coordinates from Fig. 5 in Coutts et al. (2013)
# doi: 10.1016/J.BUILDENV.2013.08.021
x_roof = np.array([-900, 600, 1600, 2800])
y_steel = np.array([26, 16, 34, 15])
y_white = np.array([25.8, 15.8, 30, 15.8])

x_tair = [-900, 300, 1400, 2800]
y_tair = [32, 17, 26, 18]

p_steel = CubicHermiteSpline(x=x_roof, y=y_steel, dydx=np.zeros_like(y_steel))  # interpolator
p_white = CubicHermiteSpline(x=x_roof, y=y_white, dydx=np.zeros_like(y_white))
p_tair = CubicHermiteSpline(x=x_tair, y=y_tair, dydx=np.zeros_like(y_tair))

# plt.plot(x_roof, y_steel, 'o')
# plt.plot(x_roof, y_white, 'o')
# plt.plot(x_tair, y_tair, 'o')

xx = np.linspace(0, 3000, 1000)

plt.figure(figsize=(10, 10))

plt.plot(xx, p_steel(xx), color='r', label='Steel')
plt.plot(xx, p_white(xx), color='b', label='White')
plt.plot(xx, p_tair(xx), color='k', label='$T_{air}$')

max_error = 1.5
elems = np.arange(0, max_error, max_error / (len(xx) / 2))
error = np.array(list(elems) + list(elems[::-1]))

plt.fill_between(xx, p_white(xx) - error, p_white(xx) + error, alpha=0.2, color='b')
plt.fill_between(xx, p_steel(xx) - error, p_steel(xx) + error, alpha=0.2, color='r')
plt.fill_between(xx, p_tair(xx) - error, p_tair(xx) + error, alpha=0.2, color='k')

plt.xlim(0, 2400)
plt.ylim(14, 38)

plt.legend()

x_tick_labels = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
x_ticks = np.array(x_tick_labels) * 100

plt.xticks(x_ticks, labels=x_tick_labels)

plt.ylabel('Temperature ($^\circ$C)')
plt.xlabel('Time (h)')

save_path = os.getcwd().replace('\\', '/') + '/'
plt.savefig(save_path + 'coutts_plot.png', bbox_inches='tight', dpi=300)

plt.show()
print('end')
