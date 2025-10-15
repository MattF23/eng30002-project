from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
from numpy import array, mean, nan, diff, std

def butter_bandpass(lowcut, highcut, fs, order=3):
        nyq = 0.5 * fs
        low, high = lowcut / nyq, highcut / nyq
        b, a = butter(order, [low, high], btype="band")
        return b, a

def bandpass_filter(data, lowcut=0.5, highcut=4.0, fs=25):
    b, a = butter_bandpass(lowcut, highcut, fs)
    return filtfilt(b, a, data)

def calc_hr_and_spo2(ir_data, red_data, fs=25):
        ir_filt = bandpass_filter(array(ir_data), fs=fs)
        red_filt = bandpass_filter(array(red_data), fs=fs)

        # Debounce: require larger distance and signal prominence
        peaks, _ = find_peaks(ir_filt, distance=int(fs * 0.6), prominence=std(ir_filt) * 0.4)
        if len(peaks) > 1:
            period = mean(diff(peaks)) / fs
            hr = 60 / period
        else:
            hr = nan

        ACred, ACir = std(red_filt), std(ir_filt)
        DCred, DCir = mean(red_filt), mean(ir_filt)
        R = (ACred / DCred) / (ACir / DCir)
        spo2 = -45.06 * (R**2) + 30.354 * R + 94.845

        return hr, spo2