from setuptools import find_packages
from setuptools import setup


setup(
    name='amigonnadie',
    version='0.1',
    description='CLI for NYC Open Data',
    url='https://github.com/borisuvarov/amigonnadie',
    packages=find_packages(),
    entry_points={'console_scripts': ['amigonnadie = app:main']},
    install_requires=[
        'colorama==0.3.9',
        'fire==0.1.3',
        'sodapy==1.4.6'
    ],
)

