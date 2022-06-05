from setuptools import setup, find_packages
from setuptools import find_namespace_packages

github = ""

with open(file="README.md", mode="r") as readme_handle:
    long_description = readme_handle.read()

setup(
    name="auto-bujo",
    author="Alex Biosa",
    author_email="mochittodeveloper@gmail.com",
    description="A python CLI app that works as an addon to Simplenote that utilises mongoDB as database, "
                "to keep your notes organized in a fast and efficient way",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=github,
    install_requires=[
        "bson==0.5.10",
        "pymongo==4.1.",
        "python-dateutil==2.8.2",
        "python-dotenv==0.20.0",
        "simplenote==2.1.4",
        "six==1.16.0",
    ],
    keywords="simplenote, productivity",
    license="MIT",

    version="0.1.0",
    packages=find_packages(
        where="auto_bujo"
    )
)
