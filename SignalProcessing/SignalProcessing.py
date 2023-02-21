#15 варіант
import numpy
import scipy
from scipy import signal,fft
import matplotlib.pyplot as plt

n = 500
Fs = 1000
F_max = 31

#генерація сигналу
random = numpy.random.normal(0, 10, n)

#Визначення відліків часу, які відображатимуться на осі ОХ графіку
x = numpy.arange(n)/Fs

#Розрахунок парамерів фільтру
w = F_max/(Fs/2)
parameter = scipy.signal.butter(3, w, 'low', output='sos')

#Фільтрація сигналу
y = scipy.signal.sosfiltfilt(parameter, random)

#Відображення результатів
fig,ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot(x, y, linewidth=1)
ax.set_xlabel("Час(секунди)", fontsize=14)
ax.set_ylabel("Амплітуда сигналу", fontsize=14)
plt.title("Сигнал з максимальною частотою F_max = 31 Гц", fontsize=14)
fig.savefig('./figures/'+'Сигнал з максимальною частотою F_max = 31 Гц'+'.png', dpi=600)

#Розрахунок спектру сигналу
y_s = numpy.abs(scipy.fft.fftshift(scipy.fft.fft(y)))
x_s = scipy.fft.fftshift(scipy.fft.fftfreq(n, 1/n))

fig,ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot(x_s, y_s, linewidth=1)
ax.set_xlabel("Частота (Герци)", fontsize=14)
ax.set_ylabel("Амплітуда спектру", fontsize=14)
plt.title("Спектр сигналу", fontsize=14)
fig.savefig('./figures/'+'Спектр сигналу'+'.png', dpi=600)

