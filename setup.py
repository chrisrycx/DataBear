'''
DataBear package setup
'''

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="databear",
    version="2.1",
    author="Chris Cox",
    author_email="chrisrycx@gmail.com",
    description="A Python based data logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisrycx/DataBear",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pyyaml'],
    include_package_data=True,
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        databear=databear.databearCLI:main_cli
    '''
)
