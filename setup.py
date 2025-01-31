# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="aqi_monitor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pytest",
        "requests-mock"
    ],
    author="Sam",
    author_email="SamanHamidishal@gmail.com",
    description="A Python package to fetch PM2.5 air quality data using the AQICN API.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/samanhmd/aqi_monitor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
