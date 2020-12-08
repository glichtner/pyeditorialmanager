from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# read version string from file
exec(open("src/editorialmanager/version.py").read())

setup(
    name="editorialmanager",
    version=version,
    description="Python interface for querying the editorial manager journal submission system",
    long_description=read("README.rst"),
    url="https://github.com/glichtner/pyeditorialmanager",
    author="Gregor Lichtner",
    license="GPL v3",
    packages=find_packages("src"),
    package_dir={"": "src"},
    zip_safe=False,
    install_requires=["pandas", "beautifulsoup4", "html5lib"],
)
