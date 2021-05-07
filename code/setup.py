""" setuptools-based setup module. """

from setuptools import setup, find_packages

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

setup(
    name="technical_tutorial",
    version="0.1",
    description="Speech analysis tools for processing Zoom data",
    url="https://github.com/meghavarshini/Technical_Tutorial",
    packages = find_packages(),
    keywords="speech analysis",
    zip_safe=False,
    install_requires=[
        "wheel",
        "pandas",
        "numpy",
        "webvtt-py"
    ],
    python_requires=">=3.5",
)