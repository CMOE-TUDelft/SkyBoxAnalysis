# SkyBox Analysis

Multi-language analysis toolbox for SkyBox wave run-up and impact dataset.

## Languages & Documentation

### Python

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://cmoe-tudelft.github.io/SkyBoxAnalysis/python/skyboxdatapy.html)

- **Package**: `skyboxdatapy`
- **Example**: [example_analysis.py](./notebooks/python/example_analysis.py)
- **Install**: `pip install -e ./python`

### Julia  
- **Package**: `FSSLib`
- **Source**: [SkyBoxData.jl](../julia/src/SkyBoxLib.jl)
- **Example**: [run_example.jl](../julia/scripts/run_example.jl)
- **Setup**: `julia --project=julia`

### MATLAB
- **Package**: `+fss`
- **Functions**: [fss/](../matlab/fss/)
- **Example**: [run_example.m](../matlab/scripts/run_example.m)
- **Setup**: `addpath('matlab')`

## Quick Start

Choose your language:

**Python:**
```bash
pip install -e ./python
python python/scripts/example_analysis.py
```

Create the auto-documentation using
```bash
pdoc -o docs/python/ python/skyboxdatapy
```

**Julia:**
```bash
julia --project=julia
julia julia/scripts/run_example.jl
```

**MATLAB:**
```matlab
addpath('matlab');
run('matlab/scripts/run_example.m');
```

## Project Structure

```
├── python/          # Python package (skyboxdatapy)
├── julia/           # Julia package (SkyBoxData.jl) 
├── matlab/          # MATLAB package (+fss)
├── data/            # Raw and processed data
├── notebooks/       # Jupyter Python and Julia notebooks
└── env/             # Environment files for Anaconda
```

## Contributing

1. Follow existing code style for each language
2. Add tests and documentation  
3. Update this README when adding features

---
