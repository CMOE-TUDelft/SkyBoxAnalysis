# SkyBox Library Documentation

This directory contains the automated documentation generation setup for the SkyBox Library.

## 📚 Viewing Documentation

Once deployed, documentation will be available at:
- **GitHub Pages**: `https://shagun751.github.io/SkyBox/docs/`
- **Direct HTML**: Browse the `html/` folder in this repository

## 🔄 Automatic Generation

Documentation is automatically generated and deployed when:
- Code is pushed to `main`/`master` branch
- Pull requests are created
- Manual workflow dispatch is triggered

## 🛠️ Local Generation

To generate documentation locally:

```bash
cd python
pip install pdoc
pdoc skyboxlib -o docs/html --html
```

## 📖 Documentation Coverage

The workflow automatically checks:
- ✅ All public functions have docstrings
- ✅ Docstring style compliance
- ✅ API completeness

## 🚀 GitHub Pages Setup

To enable GitHub Pages:
1. Go to repository Settings → Pages
2. Select "Deploy from a branch"
3. Choose `gh-pages` branch
4. Set folder to `/ (root)`

## 📝 Improving Documentation

To enhance the generated docs:
1. Add detailed docstrings to functions in `skyboxlib/`
2. Include usage examples in docstrings
3. Add type hints to function signatures
4. Update module-level documentation in `__init__.py`

## 🔧 Workflow Files

- `docs.yml`: Simple documentation generation
- `docs-full.yml`: Comprehensive documentation with quality checks