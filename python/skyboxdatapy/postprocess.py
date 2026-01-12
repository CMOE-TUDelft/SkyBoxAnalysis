import numpy as np
import xarray as xr

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
