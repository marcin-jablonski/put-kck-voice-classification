import copy
import numpy as np
import scipy.io.wavfile
import sys
from scipy.signal import kaiser, decimate


def get_lead_frequency(signal, samples_count, audio_duration, no=0, mono=0):
    signal = signal if mono else [s[no] for s in signal]

    signal = signal * kaiser(samples_count, 100)

    spectrum = np.log(abs(np.fft.rfft(signal)))
    spectrum_enriched = copy.copy(spectrum)

    for beta in range(2, 6):
        decimated_spectrum = decimate(spectrum, beta)
        spectrum_enriched[:len(decimated_spectrum)] += decimated_spectrum

    peak_start = 50 * audio_duration
    peak = np.argmax(spectrum_enriched[peak_start:])
    lead_frequency = (peak_start + peak) / audio_duration
    return lead_frequency


def verify_speaker_gender(filename):
    sampling_frequency, signal = scipy.io.wavfile.read(filename)
    samples_count = len(signal)
    audio_duration = float(samples_count) / sampling_frequency

    mono = 1
    if not isinstance(signal[0], np.int16):
        mono = 0

    if mono:
        lead_frequency = get_lead_frequency(signal, samples_count, audio_duration, mono=1)
    else:
        lead_frequency = (get_lead_frequency(signal, samples_count, audio_duration, no=0) + get_lead_frequency(signal,
                                                                                                               samples_count,
                                                                                                               audio_duration,
                                                                                                               no=1)) / 2

    if lead_frequency < 165:
        result = 'M'
    else:
        result = 'K'

    print("%s : %s" % (filename, result))
    return result


if __name__ == "__main__":
    print(verify_speaker_gender(sys.argv[1]))
