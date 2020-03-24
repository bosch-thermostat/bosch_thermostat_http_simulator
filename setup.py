#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup

with open("bosch_thermostat_http_simulator/version.py") as f:
    exec(f.read())


REQUIRES = [
    'pyaes>=1.6.1',
    'flask',
    'click>=7',
    'waitress'
]

with open("README.md", "r") as fh:
    long_description = fh.read()
author="Pawel Szafer"
email="pszafer@gmail.com"
setup(
    name='bosch-thermostat-http-simulator',
    version=__version__,  # type: ignore # noqa: F821,
    description='Python app simulating Bosch™ Heating gateway using HTTP protocol',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    url='https://github.com/pszafer/bosch_thermostat_http_simulator',
    download_url='https://github.com/pszafer/bosch_thermostat_http_simulator/archive/{}.zip'.format(__version__),
    packages=["bosch_thermostat_http_simulator"],
    install_requires=REQUIRES,
    include_package_data=True,
    license='Apache License 2.0',
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ],
    entry_points={
        "console_scripts": [
            "bosch_simulator=bosch_thermostat_http_simulator.bosch_run:cli"
        ]
    }
)