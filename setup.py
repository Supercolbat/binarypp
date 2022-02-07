from setuptools import setup
from typing import List

import binarypp


def _long_description() -> str:
    with open("README.md", encoding="utf-8") as file:
        return file.read()


def _install_requires() -> List[str]:
    with open("requirements.txt", encoding="utf-8") as file:
        return file.read().strip().splitlines()


# fmt: off
setup(
    name = "binarypp",
    version = binarypp.__version__,
    description = binarypp.__doc__.strip(),
    long_description = _long_description(),
    long_description_content_type = "text/markdown",
    
    download_url="https://github.com/Supercolbat/binarypp/",
    
    author="Joey Lent (Supercolbat)",
    author_email="supercolbat@gmail.com",
    
    license=binarypp.__license__,
    project_urls={"GitHub": "https://github.com/Supercolbat/binarypp"},
    
    # TODO: Check lower versions
    keywords=["language"],
    python_requires=">=3.8",
    install_requires=_install_requires(),
    entry_points={"console_scripts": ["binarypp = binarypp.__main__:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Software Distribution",
    ],
)
