import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="data-conversion-app",
    version="1.0.0",
    description="Description!",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Thomasjkeel",
    author="Thomas Keel",
    author_email="thomasjames.keel@googlemail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["exdag"],
    include_package_data=True,
    install_requires=[
        "PyQt5", "numpy", "pandas"
    ],
    entry_points={"console_scripts": ["exdag=exdag.__main__:main"]},
)