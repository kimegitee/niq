import setuptools
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='niq',
    version='1.2.2',
    description="Nick's library of extraneous utils",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kimegitee/niq',
    author='kimegitee',
    author_email='kimegitee@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['xxhash>=1.4.0,<2', 'joblib>=0.14.0,<0.15'],
    zip_safe=False,
)
