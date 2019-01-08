# COmparison with distance-RMSE method
# Li, G., Geng, E., Ye, Z., Xu, Y., Lin, J., & Pang, Y. (2018). Indoor positioning algorithm based on the improved rssi distance model. Sensors (Switzerland), 18(9), 1–15. https://doi.org/10.3390/s18092820
# Jenny Röbesaat 1 , Peilin Zhang 2, *, Mohamed Abdelaal 3 and Oliver Theel 2 An Improved BLE Indoor Localization withKalman-Based Fusion: An Experimental Study
import numpy as np

from plot_results import plot_results,colors
from tools import plot_ellipse

print("Computing Measurements")
from ellipses import Y, Gar, gamma, ap_coordinates as xy, J, I, N, n_configuration, transmitters_coordinates, crlb, \
    estimate
import matplotlib.pyplot as plt

Ymean = np.median(Y, axis=3)
d = np.exp(np.log(10) * (Gar - Ymean) / (10 * gamma))

d = np.moveaxis(d, 2, 1).reshape((-1, J))
D = d[:, -1, None] ** 2 - d[:, :-1] ** 2
A = 2 * (xy[:-1, :] - xy[-1, None, :])
B = np.sum(xy[:-1, :] ** 2 - xy[-1, :] ** 2, axis=1)[None, :] + D

sol = np.reshape([np.linalg.lstsq(A, i)[0] for i in B], (n_configuration, I, 2))
sol = np.moveaxis(sol, 1, 0)

cov = [np.cov(i.T) for i in sol]

axe = plot_results(transmitters_coordinates, np.moveaxis(sol, 1, 0), xy, crlb)
for i,c in zip(np.moveaxis(estimate, 1, 0),colors):
    cov, mean = np.cov(i.T), np.mean(i, axis=0)
    plot_ellipse(cov,axe,mean,color=c[0],ls="-.")
plt.show()
pass