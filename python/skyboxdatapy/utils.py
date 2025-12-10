import xarray as xr

# ==============================================================================

def print_all_headers(data: dict):
    """
    Print a short, human-readable summary of all top-level entries in an HDF5-like dict.

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
            if isinstance(l1, dict):
                for key in l1:
                    print("   -", key)
            elif isinstance(l1, xr.Dataset):
                print(l1.keys())
            else:
                # Fallback: print repr
                print("  value repr:", repr(l1))
            
            print("-----")            

        print("=== End of headers ===\n")
    
    except Exception as e:
        raise RuntimeError(f"Error loading hdf5 nested file:\n{e}")



# ==============================================================================


def print_top_headers(data: dict | xr.Dataset):
    """
    Print a short, human-readable summary of all top-level entries in an HDF5-like dict.

    Args:
        data (dict or xarray.Dataset): mapping of top-level names to values (e.g., groups/arrays).

    Notes:
        Shows key names, value types, and structured-array field names when present.
    """
    
    print("\n=== Listing headers ===")
    try:        
        print("Object type:", type(data))

        if isinstance(data, dict):
            for l1Key, l1 in data.items():
                print("   - Key:", l1Key, "-> type:", type(l1))        
        elif isinstance(data, xr.Dataset):
            print(data.keys())
            
        print("=== End of headers ===\n")
    
    except Exception as e:
        raise RuntimeError(f"Error printing headers: \n{e}")
    

# ==============================================================================


def print_test_properties(data: dict):
    """
    Print the TestProperties section of the loaded data.

    Args:
        data (dict): mapping of top-level names to values (e.g., groups/arrays).

    Notes:
        Extracts and prints the 'TestProperties' entry if present.
    """

    print_order = [
        'testName', 'testType', 'repeatType',
        'useTest', 'fSampling', 'calibrationFile', 
        'depthAtWM', 'depthAtMPL', 'airGapAtMPL',
        'waveType', 'waveAmplitude', 'wavePeriod',
        'focusingLocation',
        'remarks' ]
    
    ignore_order = [
        'allAttributes', 'convertedAttributes',
        'unconvertedAttributes' ]
    
    
    print("\n=== Test Properties ===")

    test_props = data.get('TestProperties', None)

    for key in print_order:
        if key in test_props:
            value = test_props[key]
            print(f"   - {key}: {value}")            
    
    for l1Key, l1 in test_props.items():
        if l1Key not in print_order and l1Key not in ignore_order:
            print(f"   - {l1Key}: {l1}")

    print("=== End of Test Properties ===\n")
    
# ==============================================================================