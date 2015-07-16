from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='griffin_powermate',
    version='1.0.2',

    description='A simple library to use the Griffin Powermate on Windows',
    long_description='',

    url='https://github.com/crash7/griffin-powermate',
    author='Christian Musa',
    author_email='christianmusa@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='griffin powermate development',
    packages=['griffin_powermate'],

    install_requires=['pywinusb']
)