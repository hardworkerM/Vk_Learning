"""Setup file for Python extension 'cutils' written on C-language"""
from setuptools import setup, Extension

setup(
    name='cutils',
    version='1.0',
    description='Multiply two matrix on C',
    ext_modules=[
        Extension('cutils', ['cutils.c'])
    ]
)
