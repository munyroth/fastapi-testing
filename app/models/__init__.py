import importlib
import pkgutil

# Automatically import all Python files in this directory
for _, module_name, _ in pkgutil.iter_modules([__path__[0]]):
    importlib.import_module(f"{__name__}.{module_name}")

