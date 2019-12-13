import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# https://packaging.python.org/tutorials/packaging-projects/

setuptools.setup(
    name="pyson0-lbragues",
    version="0.1",
    author="Leandro Braguês",
    author_email="lbragues@gmail.com",
    description="This package ports the json0-ot-diff and ottypes/json0 to python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lbragues/pyson0",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)