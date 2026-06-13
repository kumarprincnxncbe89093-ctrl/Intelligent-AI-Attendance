from importlib import import_module
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


class Distribution:
    def __init__(self, package_name):
        self.project_name = package_name
        self.version = version(package_name)


class DistributionNotFound(Exception):
    pass


def get_distribution(package_name):
    try:
        return Distribution(str(package_name).split()[0])
    except PackageNotFoundError as exc:
        raise DistributionNotFound(package_name) from exc


def resource_filename(package_or_requirement, resource_name):
    package_name = str(package_or_requirement).split()[0]
    package = import_module(package_name)
    return str(Path(package.__file__).resolve().parent / resource_name)
