# AGH UST Medical Informatics 03.2022
# Lab 1 : ECG (Electrocardiography)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks, filtfilt
import wfdb

# --- read data
max_samples = 3600

record = wfdb.io.rdrecord(record_name='101', sampto=max_samples)
ecg = record.p_signal[:, 0]

print('ecg data: ')
print(ecg)

# --- process data

# find peaks in the signal
peaks_all, _ = find_peaks(ecg)
print('\npeaks all: ')
print(peaks_all)

# heart rate
# todo: find R peaks (highest ones) using a threshold for peak height in find_peaks
r_peaks, _ = find_peaks(ecg, height=.4)
print('\nR peaks all: ')
print(r_peaks)

# todo: find time between heart beats using distance between R peaks (sampling frequency = 100Hz)
time_between_heartbeats = []
prev_r = r_peaks[0]
for r_peak in r_peaks[1:]:
    time_between_heartbeats.append((r_peak - prev_r) / record.fs)
    prev_r = r_peak

# todo: find average heart rate given in BPM (beats per minute)
time_between_heartbeats = np.array(time_between_heartbeats)
# divide number of heartbeats by time (in minutes)
average_heart_rate = time_between_heartbeats.shape[0] / (np.sum(time_between_heartbeats) / 60.0)
print(f'Average heart rate: {average_heart_rate:.3f}')


# todo: filter signal with moving average
def moving_average(x, w=5):
    return filtfilt(np.ones(w) / w, 1., x)


filtered_ecg = moving_average(ecg, 5)
filtered_ecg = moving_average(filtered_ecg, 15)

# filtered signal peaks
# todo: find peaks in the filtered signal
filtered_signal_peaks, _ = find_peaks(filtered_ecg)
print('\nfiltered signal peaks all: ')
print(filtered_signal_peaks)

# P,R,T peaks
# todo: find P,R,T peaks (find R peaks in the filtered signal, then find peaks before (P) and after (T))
filtered_r_peaks, _ = find_peaks(filtered_ecg, height=.0, distance=14)
print('\nfiltered R peaks all: ')
print(filtered_r_peaks)

filtered_p_peaks = []
filtered_t_peaks = []
for r_peak in filtered_r_peaks:
    peak_index = np.where(filtered_signal_peaks == r_peak)[0][0]
    filtered_p_peaks.append(filtered_signal_peaks[peak_index - 1])
    filtered_t_peaks.append(filtered_signal_peaks[peak_index + 1])

print('\nfiltered P peaks all: ')
print(filtered_p_peaks)

print('\nfiltered T peaks all: ')
print(filtered_t_peaks)

# --- plots
# plot original ECG with peaks (all)
plt.figure(figsize=(16, 12))
plt.subplot(3, 1, 1)
plt.plot(ecg, '#999999')
plt.plot(peaks_all, ecg[peaks_all], "rx")

# # todo: plot PRT peaks
plt.subplot(3, 1, 2)
plt.plot(filtered_ecg, '#999999')

plt.plot(r_peaks, filtered_ecg[r_peaks], "bo")
plt.plot(filtered_p_peaks, filtered_ecg[filtered_p_peaks], "go")
plt.plot(filtered_t_peaks, filtered_ecg[filtered_t_peaks], "co")

# histogram
plt.subplot(3, 1, 3)
print(time_between_heartbeats)
plt.hist(time_between_heartbeats)
#
# # show plot
plt.show()
