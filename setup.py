from setuptools import setup


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
