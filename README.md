# SkyBoxAnalysis

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://cmoe-tudelft.github.io/SkyBoxAnalysis/)


Multi-language analysis toolbox for FSS datasets (Python, MATLAB, Julia).

## Layout

- `python/` – Python package `fsslib` + helper scripts
- `matlab/` – MATLAB package `+fss` and example scripts
- `julia/` – Julia package `FSSLib` and example scripts
- `data/` – raw and processed data (not versioned by default)
- `notebooks/` – Jupyter and Julia notebooks
- `env/` – environment files (`environment.yml`, etc.)

See `python/scripts/example_analysis.py`, `matlab/scripts/run_example.m`,
and `julia/scripts/run_example.jl` for starting points.

# SkyBox Analysis

Multi-language analysis toolbox for FSS (Floating Submerged Structures) datasets.

## Languages & Documentation

### Python
- **Package**: `skyboxlib`
- **Documentation**: [Python API Docs](docs/python/index.html)
- **Example**: [example_analysis.py](../python/scripts/example_analysis.py)
- **Install**: `pip install -e ./python`

### Julia  
- **Package**: `FSSLib`
- **Source**: [SkyBoxLib.jl](../julia/src/SkyBoxLib.jl)
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
├── python/          # Python package (skyboxlib)
├── julia/           # Julia package (FSSLib) 
├── matlab/          # MATLAB package (+fss)
├── data/            # Raw and processed data
├── notebooks/       # Jupyter and Julia notebooks
└── env/             # Environment files
```

## Contributing

1. Follow existing code style for each language
2. Add tests and documentation  
3. Update this README when adding features

---

For detailed API documentation, see [Python API Docs](python/index.html).