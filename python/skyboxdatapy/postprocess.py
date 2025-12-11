import numpy as np

# ==============================================================================

def updated_LED_transition_indices(dfIn):
    """       
    This function identifies the indices where LED signal transitions occur (from 0 to 1 and from 1 to 0)
    and adds them to the input dictionary.
    
    Parameters
    ----------
    dfIn : dict
        Input dictionary containing 'Time' and 'LED-chan100' keys with array-like values.
        The dictionary is modified in-place.
    
    Returns
    -------
    None
        The function modifies dfIn in-place by adding two new keys:
        - 'LED_index_0_to_1': int
            Index of the first occurrence where LED signal transitions from 0 to 1
        - 'LED_index_1_to_0': int
            Index of the last occurrence where LED signal transitions from 1 to 0
    """
    
    t = dfIn['Time']
    led = dfIn['LED-chan100']

    ind = np.where(led > 0)
    ind = ind[0]

    dfIn.update(
        {
            'LED_index_0_to_1': ind[0], 
            'LED_index_1_to_0': ind[-1]            
        } )


# ==============================================================================

def update_set_tare(dfIn, probe, start_time, end_time):

    t = dfIn['Time']
    data = dfIn[probe]

    ind_start = np.argmin(np.abs(t - start_time))
    ind_end = np.argmin(np.abs(t - end_time))

    tare_value = np.mean(data[ind_start:ind_end])
    
    data = data - tare_value
    dfIn[probe] = data