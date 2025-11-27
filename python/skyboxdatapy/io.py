"""Input/Output utilities for SkyBox data analysis.

This module provides functions for handling data paths and saving/loading
data files in various formats, particularly HDF5 MATLAB files.
"""

import pathlib
import hdf5storage
import numpy as np


# ==============================================================================

def save_hdf5_mat(path: pathlib.Path, data: dict):
    """Save data to an HDF5 MATLAB file.
    
    Args:
        path: Output file path.
        data: Dictionary containing data to save.
        
    Raises:
        Exception: If saving fails.
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
        print(f"hdf5storage (nested with options) failed: {e}")


# ==============================================================================

def load_hdf5_mat(path: pathlib.Path) -> dict:
    """Load data from an HDF5 MATLAB file.
    
    Args:
        path: Input file path.

    Returns:
        Dictionary containing loaded data. Returns empty dict if loading fails.
    
    Raises:
        Exception: If loading fails.
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
        print(f"hdf5storage (with options) failed: {e}")
        return {}


# ==============================================================================

def print_headers(data: dict):
    """
    Print a short, human-readable summary of top-level entries in an HDF5-like dict.

    Args:
        data (dict): mapping of top-level names to values (e.g., groups/arrays).

    Notes:
        Shows key names, value types, and structured-array field names when present.
    """
    
    print("\n=== Listing headers ===")
    try:        
        print("Top-level keys:", list(data.keys()))
        
        for l1Key, l1 in data.items():
            print("\nTop-level:", l1Key, "-> type:", type(l1))        

            # If it's a numpy structured array, dtype.names contains field names
            if isinstance(l1, np.ndarray):
                names = getattr(l1.dtype, "names", None)
                if names:
                    print("  structured array fields:", names)
                    for f in names:
                        print("   -", f)
            elif isinstance(l1, dict):
                for key in l1:
                    print("   -", key)
            else:
                # Fallback: print repr
                print("  value repr:", repr(l1)[:200])

        print("=== End of headers ===\n")
    
    except Exception as e:
        print(f"Error loading hdf5 nested file: {e}")


# ==============================================================================

def convert_matStrArray_to_str(matStrArray) -> str:
    """
    Convert MATLAB character array loaded from HDF5 to Python string.
    
    Args:
        matStrArray: MATLAB character array (e.g., numpy array of chars).  
    """

    try:
        # MATLAB char arrays are often 2D arrays of single-character strings
        if isinstance(matStrArray, np.ndarray):
            # Flatten and join characters        
            chars = matStrArray.flatten()
            return ''.join(chars)
        else:
            return str(matStrArray)
    
    except Exception as e:
        print(f"Error converting MATLAB string array: {e}")
        return ""
    
    
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
        np.ndarray: Usually each struct in the .mat
    
    Returns:
        dict: With all arrays flattened to 1D
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

    l2.update({
        'allAttributes': allAttributes,
        'convertedAttributes': convertedAttributes,
        'unconvertedAttributes': unconvertedAttributes
    })

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