"""Input/Output utilities for SkyBox data analysis.

This module provides functions for handling data paths and saving/loading
data files in various formats, particularly HDF5 MATLAB files.
"""

import pathlib
import hdf5storage
import numpy as np
import xarray as xr
import pandas as pd
from pathlib import Path


# ==============================================================================

all_probe_names = [
    "WG01", "WG02", "WG03", "WG04",
    "WG05", "WG06", "WG07", "WG08", "WG09",
    "Mo01", "Mo02", "Mo03", "Mo04",
    "Mo05", "Mo06", "Mo07", "Mo08",
    "WM", "L1", "L2", "L3",
    "PS01", "PS02", "PS03", "PS04",
    "PS05", "PS06", "PS07", "PS08",
    "PS09", "PS10", "PS11", "PS12",
    "PS13", "PS14", "PS15", "PS16",
    "PS17", "PS18", "PS19", "PS20",
    "PS21", "PS22", "PS23", "PS24",
    "LED-chan100" ]

# ==============================================================================

def find_unique_file(
        root_dir: str, 
        testName: str, 
        ext :str ="*") -> str:
    """Find a single file matching a pattern in a directory tree.
    
    Recursively searches through a directory and its subdirectories for files 
    matching the specified test name and extension. Expects exactly one match.
    
    Args:
    - root_dir: Root directory to start the recursive search from
    - testName: Test name pattern to match at the beginning of filenames
    - ext: File extension to match (default: "*" for any extension)
        
    Returns:
    - Path to the single file found matching the pattern
        
    Raises:
    - ValueError: If no files or multiple files are found
    
    Examples:

        >>> find_unique_file("/data", "experiment_001", "csv")
        '/data/experiment_001_results.csv'
        
        >>> find_unique_file("/data", "test_", "txt")
        ValueError: Expected 1 file for test case test_, found 0
    """
    
    pattern = f"{testName}*.{ext}" 
    files = list(Path(root_dir).rglob(pattern))
    files = [str(f) for f in files]

    if len(files) != 1:
        error_msg = f"Expected 1 file for test case {testName}, found {len(files)}"
        if files:
            error_msg += f"\nFiles found:\n"
            error_msg += "\n".join(files)
        raise ValueError(error_msg)

    return files[0]


# ==============================================================================

def save_hdf5_mat(path: pathlib.Path, data: dict):
    """Save data to an HDF5 MATLAB file.
    
    Args:
    - path: Output file path.
    - data: Dictionary containing data to save.
        
    Raises:
    - Exception: If saving fails.
    """
    try:
        hdf5storage.savemat(
            str(path),
            data,
            format="7.3",
            oned_as="column",
            store_python_metadata=False,
            matlab_compatible=True,
            truncate_existing=True
        )
        print("=== Successfully saved using hdf5storage (nested structure with additional options) ===\n")
    
    except Exception as e:
        raise RuntimeError(f"hdf5storage (nested with options) failed:\n{e}")


# ==============================================================================

def load_hdf5_mat(path: pathlib.Path) -> dict:
    """Load data from an HDF5 MATLAB file.
    
    Args:
    - path: Input file path.

    Returns:
    - Dictionary containing loaded data. Returns empty dict if loading fails.
    
    Raises:
    - Exception: If loading fails.
    """
    try:
        print("\n=== Reading MAT ===")
        data = hdf5storage.loadmat(path)
        data2 = {}

        print("Top-level keys:", list(data.keys()))

        for l1key,l1 in data.items():
            data2.update({ l1key: cleanAttributes(l1) })                
        
        print("=== Successfully loaded using hdf5storage ===\n")                
        return data2
    
    except Exception as e:
        raise RuntimeError(f"hdf5storage (with options) failed:\n{e}")



# ==============================================================================

def load_case(file,
    *,probe_names=all_probe_names) -> dict:
    """
    Load a case from an HDF5 MAT file and convert probe data to xarray format.
    Args:
    - file: Path to the HDF5 MAT file to load.
    - probe_names: Names of probes to use when converting to xarray format.
    Returns:
    - dict: Dictionary containing the loaded data, with DefaultData and MP3 entries
              converted to xarray datasets, and other entries preserved as-is.
    """

    
    loaded_mat = load_hdf5_mat(file)

    ret_mat = {}

    for l1key, l1val in loaded_mat.items():
        
        if (l1key == "DefaultData") or ("MP3" in l1key):
            ds_xr = convert_dict_to_xarray(l1val, 
                probe_names=probe_names)
            ret_mat.update({l1key: ds_xr})
        
        else:
            ret_mat.update({l1key: l1val})
    
    return ret_mat


# ==============================================================================

def convert_dict_to_xarray(ds: dict, 
    * , probe_names = all_probe_names ) -> xr.Dataset:        
    """
    Convert a dictionary to an xarray Dataset.
    
    Args:
    - ds: Dictionary containing time series data with 'Time' key and probe data
    - probe_names: List of probe names to be converted to data variables in the xarray Dataset
        - Default value: predefined list of probe names
    
    Returns:
    - xr.Dataset: Dataset with Time coordinate, probe data as variables, and other keys as attributes
    """
    

    ds_xr = xr.Dataset( coords={'Time': ds['Time']} )

    for l1key, l1val in ds.items():
        if l1key == 'Time':
            continue
        elif l1key in probe_names:
            ds_xr[l1key] = ( 'Time', l1val )
        else:
            ds_xr.attrs[l1key] = l1val

    return ds_xr
    
    
# ==============================================================================

def cleanAttributes(l1: np.ndarray) -> dict:
    """
    Flatten all arrays and convert the character arrays to strings.
    Needed because of the way HDF5 stores data.
    Additionaly export
    - allAttributes: list of all attribute names
    - convertedAttributes: list of attributes converted to strings
    - unconvertedAttributes: list of attributes not converted to strings

    Args:
    - l1: np.ndarray, usually each struct in the .mat
    
    Returns:
    - dict: With all arrays flattened to 1D
    """        
        
    l2 = {}
    convertedAttributes = []

    names = getattr(l1.dtype, "names", None)

    for f in names:
        lattr = l1[f].flatten()
        if( type(lattr[0]) == np.str_):
            convertedAttributes.append(f)
    
    allAttributes = list(names)                
    unconvertedAttributes = [f for f in names if f not in convertedAttributes]   

    # l2.update({
    #     'allAttributes': allAttributes,
    #     'convertedAttributes': convertedAttributes,
    #     'unconvertedAttributes': unconvertedAttributes
    # })

    for f in convertedAttributes:
        lattr = l1[f].flatten()
        newval = ''.join(lattr)
        l2.update({f: newval})
    
    for f in unconvertedAttributes:
        lattr = l1[f].flatten()
        if(lattr.size ==1):
            newval = lattr[0]
        else:
            newval = lattr
        l2.update({f: newval})
    
    return l2


# ==============================================================================
