import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "spoiltracker",
    version = "0.0.9",
    author = "psibir",
    author_email = "bloomfieldtm@gmail.com",
    description = "A Simple Product Expiration Date Management Tool",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/psibir/spoiltracker",
    project_urls = {
        "Bug Tracker": "https://github.com/psibir/spoiltracker/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)