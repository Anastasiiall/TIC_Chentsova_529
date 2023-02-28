#15 варіант
import matplotlib.pyplot as plt
import numpy
import scipy
from scipy import signal, fft

n = 500
Fs = 1000
F_max = 31
F_filter = 38

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

# Дискретизація сигналу
discrete_signals = []
discrete_spectrums = []
signal_after_filers = []
dispersion = []
variance_dif = []

for Dt in [2, 4, 8, 16]:
    discrete_signal = numpy.zeros(n)
    for i in range(0, round(n/Dt)):
        discrete_signal[i * Dt] = y[i * Dt]
    discrete_signals += [list(discrete_signal)]

    # Розрахунок спектру сигналів
    y_s = numpy.abs(scipy.fft.fftshift(scipy.fft.fft(discrete_signal)))
    discrete_spectrums += [list(y_s)]

    # Відновлення аналогового сигналу з дискретного
    w = F_filter/(Fs/2)
    parameters_filter = scipy.signal.butter(3, w, 'low', output='sos')
    discrete_signal_after_filers = scipy.signal.sosfiltfilt(parameters_filter, discrete_signal)
    signal_after_filers += [list(discrete_signal_after_filers)]

    # розрахунок дисперсії
    E1 = discrete_signal_after_filers - y
    dispersion += [numpy.var(E1)]

    # розрахунок співвідношення сигнал-шум
    variance_dif += [numpy.var(y) / numpy.var(E1)]

fig, ax = plt.subplots(2, 2, figsize=(21/2.54, 14/2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(x, discrete_signals[s], linewidth=1)
        s += 1
fig.supxlabel('Час(секунди)', fontsize=14)
fig.supylabel('Амплітуда сигналу', fontsize=14)
fig.suptitle('Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)', fontsize=14)
fig.savefig('./figures/'+'Сигнал з кроком дискретизації'+'.png', dpi=600)

fig, ax = plt.subplots(2, 2, figsize=(21/2.54, 14/2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(x_s, discrete_spectrums[s], linewidth=1)
        s += 1
fig.supxlabel('Частота(Гц)', fontsize=14)
fig.supylabel('Амплітуда спектру', fontsize=14)
fig.suptitle('Спектри сигналів з кроком дискретизації Dt = (2, 4, 8, 16)', fontsize=14)
fig.savefig('./figures/' + 'Спектр сигналів з кроком дискретизації' + '.png', dpi=600)

fig, ax = plt.subplots(2, 2, figsize=(21/2.54, 14/2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(x, signal_after_filers[s], linewidth=1)
        s += 1
fig.supxlabel('Час(секунди)', fontsize=14)
fig.supylabel('Амплітуда сигналу', fontsize=14)
fig.suptitle('Відновлені аналогові сигнали з кроком дискретизації Dt = (2, 4, 8, 16)', fontsize=14)
fig.savefig('./figures/' + 'Відновлені аналогові сигнали з кроком дискретизації' + '.png', dpi=600)

fig,ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot([2, 4, 8, 16], dispersion, linewidth=1)
fig.supxlabel('Крок дискретизації', fontsize=14)
fig.supylabel('Дисперсія', fontsize=14)
fig.suptitle('Залежність дисперсії від кроку дискретизації', fontsize=14)
fig.savefig('./figures/' + 'Залежність дисперсії від кроку дискретизації' + '.png', dpi=600)

fig,ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot([2, 4, 8, 16], variance_dif, linewidth=1)
fig.supxlabel('Крок дискретизації', fontsize=14)
fig.supylabel('ССШ', fontsize=14)
fig.suptitle('Залежність співвідношення сигнал-шум від кроку дискретизації', fontsize=14)
fig.savefig('./figures/' + 'Залежність співвідношення сигнал-шум від кроку дискретизації' + '.png', dpi=600)
