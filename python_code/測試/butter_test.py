# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 14:00:40 2018

@author: owo
"""

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

b, a = signal.butter(4, 100, 'low', analog=True)
w, h = signal.freqs(b, a)
plt.semilogx(w, 20 * np.log10(abs(h)))
plt.title('Butterworth filter frequency response')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
plt.axvline(100, color='green') # cutoff frequency
plt.show()



#

b, a = signal.ellip(4, 0.01, 120, 0.125)  # Filter to be applied

tt = vwoos324GridDataLinear[:,0][~np.isnan(vwoos324GridDataLinear[:,0])]

fgust = signal.filtfilt(b, a, tt, method="gust")


plt.plot(fgust)
plt.plot(vwoos324GridDataLinear[:,0][~np.isnan(vwoos324GridDataLinear[:,0])])