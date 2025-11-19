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
        print("Successfully saved using hdf5storage (nested structure with additional options)")
    
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
        data = hdf5storage.loadmat(path)
        print("Successfully loaded using hdf5storage")
        return data
    
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
                    continue            

            # Fallback: print repr
            print("  value repr:", repr(l1)[:200])
    
    except Exception as e:
        print(f"Error loading hdf5 nested file: {e}")