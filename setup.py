from setuptools import setup

setup(
    name='pytest-typhoon-polarion',
    version='0.0.1',
    description='Typhoontest plugin for Polarion',
    author='Tiarles Moralles Guterres',
    author_email='tiarles.moralles@typhoon-hil.com',
    packages=['src'],
    install_requires=[
        "pytest",
    ],
    entry_points={
        'pytest11': [
            'pytest-typhoon-polarion = src.plugin',
        ],
    }
)
