import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize

error=0.065

def exp(x, y):
    return y[0]*np.exp(-x*y[1])+y[2]

def exp2(x, a, b, c):
    return exp(x, [a, b, c])

def sine(x, y):
    return y[0]*np.sin(x*y[1]-y[2])+y[3]

def sine2(x, a, b, c, d):
    return sine(x, [a, b, c, d])

def chi_squared(data, function):
    def chi(args):
        chi_value=0
        for i in range(len(data[0])):
            chi_value+=((function(data[0][i], args)-data[1][i])/error)**2
        return chi_value
    return chi

def fit_temp_drop_curve():
    my_data=np.loadtxt("40to12")

    values=[[], []]
    my_data=[my_data[0], my_data[1]]
    for i in range(len(my_data[0])):
        if my_data[0][i]>47:
            values[0].append(my_data[0][i])
            values[1].append(my_data[1][i])
    chi_fun=chi_squared(values, exp)
    x=np.linspace(11.90, 12.05, 100)
    y=[chi_fun([27.847, 0.00148282, xs])/len(values[0]) for xs in x]
    plt.plot(x, y)
    plt.show()

def fit_sin_curve():
    my_data=np.loadtxt('target_16')
    chi_min=minimize(chi_squared(my_data, sine), [0.19, 0.0456, 140.4, 16.04])
    fitted=curve_fit(sine2, my_data[0], my_data[1], [0.2, 2*np.pi/150, 140, 15])
    print("Period: {}".format(2*np.pi/fitted[0][1]))
    print(fitted[0])
    print(chi_min)

    x=[i for i in my_data[0]]
    y=[sine2(i, *fitted[0]) for i in x]
    plt.plot(x, y)
    plt.plot(my_data[0], my_data[1])
    plt.show()

#my_data=np.loadtxt('target_16')
#
#chi_fun=chi_squared(my_data, sine)
#print(len(my_data[0]))
#
#x=np.linspace(0.0425, 0.048, 100)
#y=[chi_fun([0.19, xs, 140.4, 16.04])/len(my_data[0]) for xs in x]
#plt.plot(x, y)
#plt.show()

fit_temp_drop_curve()
