from setuptools import setup

import os
import codecs
from setuptools import setup

def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()

setup(
    name='pytest-typhoon-polarion',
    version='1.0.0',
    description='Typhoontest plugin for Siemens Polarion',
    author='Tiarles Moralles Guterres',
    author_email='tiarles.moralles@typhoon-hil.com',
    maintainer='Tiarles Moralles Guterres',
    maintainer_email='tiarles.moralles@typhoon-hil.com',
    license='MIT',
    url='https://github.com/typhoon-hil/pytest-typhoon-polarion',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=['src'],
    python_requires='>=3.8',
    install_requires=[
        "typhoontest>=1.27.0",
        "polarion==1.3.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'pytest11': [
            'pytest-typhoon-polarion = src.plugin',
        ],
    }
)
