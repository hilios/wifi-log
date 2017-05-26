from setuptools import setup, find_packages


setup(
    name="wifi-apc",
    version="0.0.2",
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'scapy',
        'zmq',
    ],
    entry_points='''
        [console_scripts]
        wifi-apc=main:run
    ''',
)
