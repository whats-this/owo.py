from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open('README.md') as f:
    long_description = f.read()

setup(
    name='owo',

    version='1.1.0',

    description='Python API wrapper for api.awau.moe',
    long_description=long_description,

    url='https://github.com/whats-this/owo.py',

    author='martmists',
    author_email='martmists@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: API Wrapper',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 3.5+',
    ],
    install_requires=[],
    packages=find_packages(),
	scripts=["owo/owo-cli", "owo/owo-bg"],
    keywords='api wrapper owo',
)
