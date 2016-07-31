from distutils.core import setup

setup(
    name="jdsnap",
    version="1.0",
    packages=['jdsnap'],
    scripts=['bin/jdsnap'],
    description="Tarsnap-based backup",
    long_description=open('README.rst').read(),
    url="http://github.com/jdswinbank/jdsnap",
    author="John Swinbank",
    author_email="john@jdsnap.swinbank.org"
)
