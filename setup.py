from setuptools import setup

setup(
        name='niq',
        version='0.1',
        description="Nick's library of extraneous utils",
        url='https://gitlab.com/kimegitee/niq',
        author='kimegitee',
        author_email='kimegitee@gmail.com',
        license='MIT',
        packages=setuptools.find_packages(),
        scripts=['bin/niq'],
        zip_safe=False
        )
