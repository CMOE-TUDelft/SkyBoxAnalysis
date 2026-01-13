import numpy as np

def get_single_sided_spectrum(wv_ele, fs):
    """
    Compute the single-sided amplitude and power spectrum of a signal.

    Parameters
    ----------
    - wv_ele : array-like <br>
        Input signal samples (1D array).
    - fs : float <br>
        Sampling frequency of the input signal in Hz.

    Returns
    -------
    - fHalf : ndarray <br>
        Array of frequency (Hz) for the single-sided spectrum.
    - fAmp : ndarray <br>
        Single-sided amplitude spectrum of the input signal.
    - fS : ndarray <br>
        Single-sided power spectral density (PSD) of the input signal.

    Notes
    -----
    - The function ensures the input signal length is even for FFT computation.
    - The amplitude spectrum is normalized and scaled for single-sided representation.
    - The power spectral density is computed per frequency bin.
    - Also prints sample length, frequency resolution, and maximum frequency.

    """

    sz = (len(wv_ele) // 2) * 2  # Make it even
    wv_ele = wv_ele[:sz]

    print("Sample Len =", sz)
    print("Least count Hz =", fs / sz)
    print("Max Freq (Half band) Hz =", fs / 2)

    fAmp = np.fft.fft(wv_ele)
    fAmp = np.abs(fAmp / sz)
    fAmp = fAmp[:sz // 2 + 1]
    fAmp[1:-1] = 2 * fAmp[1:-1]
    fHalf = fs * np.arange(sz // 2 + 1) / sz

    # # Alternative code using rfft
    # # I'll keep it commented since I like to know 
    # # whats happening under the hood

    # fAmp = np.fft.rfft(wg01)
    # fAmp = np.abs(fAmp)/len(wg01)
    # fAmp[1:-1] = 2 * fAmp[1:-1]
    # fFreq = np.fft.rfftfreq(len(wg01), d=1/fSampling)

    fS = fAmp ** 2 / 2 / (fHalf[1] - fHalf[0])

    return fHalf, fAmp, fS
