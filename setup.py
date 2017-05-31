from setuptools import setup, find_packages

setup(
    name='ababe',
    version='0.1',
    description='A grid structure machine learning tool used in material science.',
    author='Jason Yu',
    author_email='unkcpz.yu@yahoo.com',
    license='MIT',
    packages=find_packages(),
    package_data={"ababe.stru": ["*.json"]}
    )
