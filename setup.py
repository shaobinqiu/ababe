from setuptools import setup, find_packages

setup(
    name='ababe',
    # Remenber change version in ababe.cmdline.runabalib.exec_from_cmdline()
    version='0.1.0',
    description='A grid structure machine learning tool used\
                 in material science.',
    author='Jason Yu',
    author_email='unkcpz.yu@yahoo.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={"ababe.stru": ["*.json"]},
    install_requires=["nose2", "numpy==1.12", "aenum", "hat-trie",
                      "spglib==1.9.9.18", "PyYAML==3.11",
                      "scipy==0.18.1", "progressbar2", "xxhash"],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Science/Research",
        "License :: MIT License",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics"],
    scripts=[],
    entry_points={
        'console_scripts': [
            'runaba=ababe.cmdline.runabalib:run'
        ]
    }
    )
