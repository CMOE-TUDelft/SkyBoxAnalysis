import numpy as np
import xarray as xr
import scipy as sp
import matplotlib.pyplot as plt

# ==============================================================================

def update_LED_transition_indices(dfIn: xr.Dataset):
    """
    Identifies LED transition indices and adds them as dataset attributes.
    
    Parameters
    ----------
    - dfIn : xr.Dataset
        - Dataset with 'Time' and 'LED-chan100' variables. Modified in-place.
    
    Attributes Added
    ----------------
    - LED_index_0_to_1 : int
        - Index of LED transition from 0 to 1
    - LED_index_1_to_0 : int
        - Index of LED transition from 1 to 0
    - LED_time_0_to_1 : float
        - Time value at LED transition from 0 to 1
    - LED_time_1_to_0 : float
        - Time value at LED transition from 1 to 0
    """

    
    t = dfIn['Time'].values
    led = dfIn['LED-chan100'].values

    ind = np.where(led > 0)
    ind = ind[0]

    if(len(ind) == 0):
        print("No LED transitions found in 'LED-chan100' data.")
        dfIn.attrs['LED_index_0_to_1'] = 0
        dfIn.attrs['LED_index_1_to_0'] = 0
        dfIn.attrs['LED_time_0_to_1'] = 0
        dfIn.attrs['LED_time_1_to_0'] = 0
    else:
        dfIn.attrs['LED_index_0_to_1'] = ind[0]
        dfIn.attrs['LED_index_1_to_0'] = ind[-1]
        dfIn.attrs['LED_time_0_to_1'] = t[ind[0]]
        dfIn.attrs['LED_time_1_to_0'] = t[ind[-1]]
        


# ==============================================================================

def set_all_probe_tare(dsIn, start_time, end_time):
    """
    Tare all probes in the dataset using the mean value over a specified time range.
    
    Parameters
    ----------
    - dsIn : xarray.Dataset
        - Input dataset containing probe data.
    - start_time : datetime-like
        - Start time for calculating tare values.
    - end_time : datetime-like
        - End time for calculating tare values.
    
    Returns
    -------
    - xarray.Dataset
        - Dataset with tare values subtracted from all probes, with `tare_values` stored in attributes.
    """


    dsub = dsIn.sel(Time=slice(start_time, end_time))
    tare_vals = dsub.mean(dim='Time')

    dsOut = dsIn - tare_vals    

    if 'tare_values' in dsIn.attrs:
        tv = dsIn.attrs['tare_values']
    else:
        tv = {}
            
    for name, val in tare_vals.data_vars.items():
        tv.update({name: val.item()})
    
    dsOut.attrs['tare_values'] = tv

    return dsOut

# ==============================================================================

def set_probe_tare(dsIn: xr.Dataset, probe, start_time, end_time):
    """
    Tare specified probes in the dataset using the mean value over a specified time range.
    
    Parameters
    ----------
    - dsIn : xarray.Dataset
        - Input dataset containing probe data.
    - probe : single string or list of strings
        - List of probe names to apply tare correction to.
    - start_time : datetime-like
        - Start time for calculating tare values.
    - end_time : datetime-like
        - End time for calculating tare values.
    
    Returns
    -------
    - xarray.Dataset
        - Dataset with tare values subtracted from specified probes. Tare values for each 
        probe are stored in the dataset's `tare_values` attribute as a dictionary. If 
        `tare_values` already exists in the input dataset attributes, new tare values 
        are added to the existing dictionary.    

    Example
    -------

        >>> set_probe_tare(ds, ['WG01', 'WG02'], start_time=0, end_time=0.5)
        >>> set_probe_tare(ds, 'WG01', start_time=0, end_time=0.5)   
    """


    dsub = dsIn.sel(Time=slice(start_time, end_time))
    tare_vals = dsub.mean(dim='Time')

    dsOut = dsIn.copy()
    
    if(isinstance(probe, str)):
        probe = [probe]    

    if 'tare_values' in dsIn.attrs:
        tv = dsIn.attrs['tare_values']
    else:
        tv = {}
    
    for iprobe in probe:
        dsOut[iprobe] = dsIn[iprobe] - tare_vals[iprobe]
        tv.update({iprobe: tare_vals[iprobe].item()})

    dsOut.attrs['tare_values'] = tv

    return dsOut

# ==============================================================================

def sync_signals_crosscorr_downsample( da1 : xr.DataArray, fSampling1, da2 : xr.DataArray, fSampling2, plotflag = False):
    """
    Synchronize two signals using cross-correlation.
    If the sampling frequencies differ, downsample both signals to the minimum frequency.
    
    Parameters
    ----------
    - da1 : xr.DataArray
        - First signal to be synchronized.
    - fSampling1 : float
        - Sampling frequency of the first signal (in Hz).    
    - da2 : xr.DataArray
        - Second signal to be synchronized.
    - fSampling2 : float
        - Sampling frequency of the second signal (in Hz).        
    - plotflag : bool, optional
        - If True, plot the cross-correlation result. Default is False.
    
    Returns
    -------
    - float
        - Time shift to apply to ds2 to synchronize with ds1.
    """

    
    # Convert Time from Float64 to timedelta64[ns] to enable resampling
    da1_resampled = da1.assign_coords(
        Time_ns = (da1.Time * 1e9).astype('timedelta64[ns]') )
    da2_resampled = da2.assign_coords(
        Time_ns = (da2.Time * 1e9).astype('timedelta64[ns]') )
    
    fSampling = fSampling1 # Default    

    if fSampling1 != fSampling2:
        fSampling = min(fSampling1, fSampling2)
        dt_ns = 1/fSampling*1e9 # in ns
        print(f"Warning: Sampling frequencies differ. Using minimum: {fSampling} Hz, dt = {dt_ns} ns")

        if fSampling1 != fSampling:                                            
            da1_resampled = da1_resampled.resample(Time_ns=f'{dt_ns}ns').mean()
            da1_resampled = da1_resampled.assign_coords(
                Time = (da1_resampled.Time_ns / np.timedelta64(1, 's')).astype('float64') )

        if fSampling2 != fSampling:    
            da2_resampled = da2_resampled.resample(Time_ns=f'{dt_ns}ns').mean()
            da2_resampled = da2_resampled.assign_coords(
                Time = (da2_resampled.Time_ns / np.timedelta64(1, 's')).astype('float64') )
    

    dt = 1/fSampling

    sig1 = da1_resampled.values
    sig2 = da2_resampled.values

    n1 = len(sig1)
    n2 = len(sig2)

    N = min(n1, n2)
    sig1 = sig1[0:N]
    sig2 = sig2[0:N]

    corr = sp.signal.correlate(sig1 - np.mean(sig1), sig2 - np.mean(sig2), mode='full')
    lags = sp.signal.correlation_lags(N, N, mode='full')

    lag_maxCorr = lags[np.argmax(corr)]
    tShift_maxCorr = lag_maxCorr * dt

    lag_mat_peaks, _ = sp.signal.find_peaks(corr, 
        height=np.max(corr)*0.9)
    tShift_array = lags[lag_mat_peaks]*dt
    print(f"Peaks in cross-corr: {tShift_array}")


    if(plotflag):
        plt.figure(figsize=(10, 4))
        # da1_use.plot(x='Time', label='Signal 1')
        # da2_use.plot(x='Time', label='Signal 2')
        plt.plot(da1_resampled.Time[0:N], sig1, label='Signal 1')
        plt.plot(da2_resampled.Time[0:N], sig2, label='Signal 2')
        plt.title('Resampled Signals')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.grid()
        plt.show()

        plt.figure(figsize=(10, 4))
        plt.plot(lags * dt, corr)
        plt.scatter(tShift_array, corr[lag_mat_peaks], color='orange', label='Peaks')
        plt.title('Cross-correlation between signals')
        plt.xlabel('Lag (s)')
        plt.ylabel('Correlation')
        plt.axvline(x=tShift_maxCorr, color='r', linestyle='--', label=f'Max corr at Shift: {tShift_maxCorr:.4f} s')
        plt.legend()
        plt.grid()
        plt.show()

    return tShift_maxCorr, tShift_array


# ==============================================================================

def sync_signals_crosscorr_upsample( da1 : xr.DataArray, fSampling1, da2 : xr.DataArray, fSampling2, plotflag = False):
    """
    Synchronize two signals using cross-correlation.
    If the sampling frequencies differ, upsample both signals to the maximum frequency.
    I upsample to get a better resolution in the lag estimation.
    
    Parameters
    ----------
    - da1 : xr.DataArray
        - First signal to be synchronized.
    - fSampling1 : float
        - Sampling frequency of the first signal (in Hz).    
    - da2 : xr.DataArray
        - Second signal to be synchronized.
    - fSampling2 : float
        - Sampling frequency of the second signal (in Hz).        
    - plotflag : bool, optional
        - If True, plot the cross-correlation result. Default is False.
    
    Returns
    -------
    - float
        - Time shift to apply to ds2 to synchronize with ds1.
    """

    
    da1_use = da1.copy()
    da2_use = da2.copy()
    
    fSampling = fSampling1 # Default    


    if fSampling1 != fSampling2:
        fSampling = max(fSampling1, fSampling2)        
        dt = 1/fSampling
        print(f"Warning: Sampling frequencies differ. Using maximum: {fSampling} Hz, dt = {dt} ns")        

        if fSampling1 != fSampling:                                            
            tArray = np.arange(da1.Time.min(), da1.Time.max(), 1/fSampling)
            da1_use = da1.interp(Time=tArray, method = 'linear')

        if fSampling2 != fSampling:    
            tArray = np.arange(da2.Time.min(), da2.Time.max(), 1/fSampling)
            da2_use = da2.interp(Time=tArray, method = 'linear')
    

    dt = 1/fSampling

    sig1 = da1_use.values
    sig2 = da2_use.values

    n1 = len(sig1)
    n2 = len(sig2)

    N = min(n1, n2)
    sig1 = sig1[0:N]
    sig2 = sig2[0:N]

    corr = sp.signal.correlate(sig1 - np.mean(sig1), sig2 - np.mean(sig2), mode='full')
    lags = sp.signal.correlation_lags(N, N, mode='full')

    lag_maxCorr = lags[np.argmax(corr)]
    tShift_maxCorr = lag_maxCorr * dt

    lag_mat_peaks, _ = sp.signal.find_peaks(corr, 
        height=np.max(corr)*0.9)
    tShift_array = lags[lag_mat_peaks]*dt
    print(f"Peaks in cross-corr: {tShift_array}")


    if(plotflag):
        plt.figure(figsize=(10, 4))
        # da1_use.plot(x='Time', label='Signal 1')
        # da2_use.plot(x='Time', label='Signal 2')
        plt.plot(da1_use.Time[0:N], sig1, label='Signal 1')
        plt.plot(da2_use.Time[0:N], sig2, label='Signal 2')
        plt.title('Resampled Signals')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.grid()
        plt.show()

        plt.figure(figsize=(10, 4))
        plt.plot(lags * dt, corr)
        plt.scatter(tShift_array, corr[lag_mat_peaks], color='orange', label='Peaks')
        plt.title('Cross-correlation between signals')
        plt.xlabel('Lag (s)')
        plt.ylabel('Correlation')
        plt.axvline(x=tShift_maxCorr, color='r', linestyle='--', label=f'Max corr at Shift: {tShift_maxCorr:.4f} s')
        plt.legend()
        plt.grid()
        plt.show()

    return tShift_maxCorr, tShift_array


     