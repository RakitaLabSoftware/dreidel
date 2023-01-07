from setuptools import setup, find_packages

setup(
    name="core",
    version="0.0.1",
    description="Setting up a python package",
    packages=find_packages(include=["core", "core.*"]),
    install_requires=["PyYAML", "opencv", "pandas==0.23.3", "numpy>=1.14.5"],
    extras_require={"plotting": ["matplotlib>=2.2.0", "jupyter"]},
    setup_requires=["pytest-runner", "black"],
    tests_require=["pytest"],
    package_data={"core": ["data/schema.json"]},
)
