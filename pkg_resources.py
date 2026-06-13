from importlib import import_module
from pathlib import Path


def resource_filename(package_or_requirement, resource_name):
    package_name = str(package_or_requirement).split()[0]
    package = import_module(package_name)
    return str(Path(package.__file__).resolve().parent / resource_name)
