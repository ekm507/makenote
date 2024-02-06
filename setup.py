import os

import setuptools


def get_version():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base_dir, "makenote", "__init__.py")) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.strip().split("=")[1].strip(" '\"")


with open("README.md") as readme:
    long_description = readme.read()

setuptools.setup(
    name="makenote",
    version=get_version(),
    description="command line tool for quickly writing journals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Erfan Kheirollahi",
    author_email="ekm507@gmail.com",
    keywords="makenote",
    url="https://github.com/ekm507/makenote",
    install_requires=[
        "jdatetime",
        "prompt_toolkit",
    ],
    classifiers=[],
    packages=["makenote"],
    package_dir={"makenote": "makenote"},
    include_package_data=True,
    scripts=[
        "bin/makenote",
    ],
    data_files=[(".", ["makenote/makenote.conf"])],
)
