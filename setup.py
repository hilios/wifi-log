"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="wifi-apc",
    version="0.3",
    packages=find_packages(here),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'scapy',
        'zmq',
    ],
    data_files=[
        ('/etc/systemd/system', ['resources/wifi-apc.service'])
    ],
    entry_points={
        'console_scripts': [
            'wifi-apc=main:run',
        ],
    },
)
