'''
pyDataLogger package setup
'''

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydatalogger",
    version="0.0.1",
    author="Chris Cox",
    author_email="chrisrycx@gmail.com",
    description="A Python based data logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisrycx/pyDataLogger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)