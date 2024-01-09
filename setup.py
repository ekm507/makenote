import setuptools
from makenote import __version__
import os

with open("README.md") as readme:
    long_description = readme.read()

setuptools.setup(
    name="makenote",
    version=__version__,
    description="command line tool for quickly writing journals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Erfan Kheirollahi",
    author_email="ekm507@gmail.com",
    keywords="makenote",
    url="https://github.com/ekm507/makenote",
    install_requires=[],
    classifiers=[],
    packages=["makenote"],
    package_dir={"makenote": "makenote"},
    include_package_data=True,
    scripts=[
        "bin/makenote",
    ],
    data_files = [('.', ["makenote/makenote.conf"])],
)
