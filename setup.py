from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name='genepy',
    version='1.0.0b1',

    description='Simple genetic programming library using tree representation for individuals',
    long_description=long_description,

    url='https://github.com/amstuta/genetic.py',

    author='Arthur Amstutz',
    author_email='arthur.amstutz@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='genetic evolution intelligence data learning',

    packages=find_packages(exclude=['contrib','docs','tests','example.py'])
)
