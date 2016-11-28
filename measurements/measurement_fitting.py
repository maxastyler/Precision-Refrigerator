import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

m_std = 0.25
def fit_temp_drop_curve():
    def exp(x, a, b, c):
        return a*np.exp(-x*b)+c

    my_data=np.loadtxt("40to12")

    values=[[], []]
    my_data=[my_data[0], my_data[1]]
    for i in range(len(my_data[0])):
        if my_data[0][i]>47:
            values[0].append(my_data[0][i])
            values[1].append(my_data[1][i])

    a=curve_fit(exp, values[0], values[1], [100, 1/25, 30])

    x=[i for i in my_data[0]]
    y=[exp(i, a[0][0], a[0][1], a[0][2]) for i in x]
    plt.plot(x, y)
    plt.plot(my_data[0], my_data[1])

    print(a[0])

    plt.show()

def fit_sin_curve():
    def sine(x, a, b, c, d):
        return a*np.sin(x*b-c)+d
    my_data=np.loadtxt('target_16')
    a=curve_fit(sine, my_data[0], my_data[1], [0.2, 2*np.pi/150, 140, 15])
    print("Period: {}".format(2*np.pi/a[0][1]))

    x=[i for i in my_data[0]]
    y=[sine(i, *a[0]) for i in x]
    plt.plot(x, y)
    plt.plot(my_data[0], my_data[1])
    plt.show()

fit_sin_curve()
