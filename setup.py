import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="add_scihub_links",
    url="https://github.com/afrenoy/add-scihub-links",
    version="1.0",
    author="Antoine Frenoy",
    author_email="antoine.frenoy@pasteur.fr",
    description="Add links to sci-hub in the reference section of a scientific article",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
    install_requires=["pdfrw"],
    entry_points={'console_scripts': ["add_scihub_links = add_scihub_links.add_scihub_links:main"]},
    packages=["add_scihub_links"],
    include_package_data=True,
    )
