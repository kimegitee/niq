from setuptools import setup

setup(
        name='niq',
        version='0.5.0',
        description="Nick's library of extraneous utils",
        url='https://gitlab.com/kimegitee/niq',
        author='kimegitee',
        author_email='kimegitee@gmail.com',
        license='MIT',
        packages=setuptools.find_packages(),
        install_requires=[
            'xxhash>=1.2',
        ],
        scripts=['bin/niq'],
        zip_safe=False
        )
