from setuptools import setup, find_packages

setup(
    name='ababe',
    version='0.1.0',
    description='A grid structure machine learning tool used in material science.',
    author='Jason Yu',
    author_email='unkcpz.yu@yahoo.com',
    license='MIT',
    packages=find_packages(),
    package_data={"ababe.stru": ["*.json"]},
    install_requires=["nose2", "numpy==1.12", 
                     "spglib==1.9.9.18", "PyYAML==3.11",
                     "scipy==0.18.1", "progressbar2"],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Science/Research",
        "License :: MIT License",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics"]
    )
