from setuptools import setup

setup(
    name="jdsnap",
    version="1.0",
    packages=["jdsnap"],
    entry_points={"console_scripts": ["jdsnap = jdsnap:main"]},
    description="Tarsnap-based backup",
    long_description=open("README.rst").read(),
    url="http://github.com/jdswinbank/jdsnap",
    author="John Swinbank",
    author_email="john@jdsnap.swinbank.org",
    install_requires=["klaxon"],
)
