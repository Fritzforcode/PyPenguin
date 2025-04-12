def gimport(path, name=None): # good import using importlib
    import importlib.util
    import os
    import sys

    # If it's a directory, try to use its __init__.py
    if os.path.isdir(path):
        path = os.path.join(path, "__init__.py")

    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")

    if name is None:
        name = os.path.basename(os.path.dirname(path)) if path.endswith("__init__.py") else os.path.splitext(os.path.basename(path))[0]

    # Add containing directory to sys.path so sub-imports work
    module_dir = os.path.dirname(path)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for module at {path}")

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
