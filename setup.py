import setuptools
from setuptools.config import read_configuration

# Read the configuration from pyproject.toml
config = read_configuration('pyproject.toml')

setuptools.setup(
    **config['metadata'],  # This will automatically fill in the metadata from pyproject.toml
    packages=setuptools.find_packages(),  # Automatically find packages
)
