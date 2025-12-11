import numpy as np
import xarray as xr

# ==============================================================================

def updated_LED_transition_indices(dfIn: xr.Dataset):
    """
    Identifies LED transition indices and adds them as dataset attributes.
    
    Parameters
    ----------
    dfIn : xr.Dataset
        Dataset with 'Time' and 'LED-chan100' variables. Modified in-place.
    
    Attributes Added
    ----------------
    LED_index_0_to_1 : int
        Index of LED transition from 0 to 1
    LED_index_1_to_0 : int
        Index of LED transition from 1 to 0
    LED_time_0_to_1 : float
        Time value at LED transition from 0 to 1
    LED_time_1_to_0 : float
        Time value at LED transition from 1 to 0
    """

    
    t = dfIn['Time'].values
    led = dfIn['LED-chan100'].values

    ind = np.where(led > 0)
    ind = ind[0]

    dfIn.attrs['LED_index_0_to_1'] = ind[0]
    dfIn.attrs['LED_index_1_to_0'] = ind[-1]
    dfIn.attrs['LED_time_0_to_1'] = t[ind[0]]
    dfIn.attrs['LED_time_1_to_0'] = t[ind[-1]]


# ==============================================================================

def update_set_tare(dfIn, probe, start_time, end_time):

    t = dfIn['Time']
    data = dfIn[probe]

    ind_start = np.argmin(np.abs(t - start_time))
    ind_end = np.argmin(np.abs(t - end_time))

    tare_value = np.mean(data[ind_start:ind_end])
    
    data = data - tare_value
    dfIn[probe] = data