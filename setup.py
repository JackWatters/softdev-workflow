from setuptools import setup

setup(
    name='Software_Dev',
    version='0.1',
    packages=['softdev_model'],
    package_dir={'': '.'},
    url='https://github.com/twsswt/software-dev',
    license='',
    author='Tim Storer',
    author_email='timothy.storer@glasgow.ac.uk',
    description='A socio-technical model of software development work flows developed for the Fuzzi_Moss '
                'framework.',
    setup_requires=['fuzzi_moss', 'nose'],
    test_suite='nose.collector',
    tests_require=['mock', 'nose']
)
