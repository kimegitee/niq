from setuptools import setup

setup(
    name='niq',
    version='1.2.0',
    description="Nick's library of extraneous utils",
    url='https://github.com/Cinnamon/niq',
    author='kimegitee',
    author_email='kimegitee@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['xxhash>=1.4.0,<2', 'joblib>=0.14.0,<1'],
    scripts=['bin/niq'],
    zip_safe=False,
)
