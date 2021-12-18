from setuptools import setup

setup(
    name="notes_mclds",
    version=2.0,
    author="mclds",
    author_email="mclds@protonmail.com",
    description="CRUD solution for note taking.",
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="https://codeberg.org/micaldas/notes",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["notes_mclds"],
    install_requires=[
        "click",
        "colr",
        "loguru",
        "mysql.connector",
        "thefuzz",
        "future",
        "questionary",
        "fire",
        "icecream",
    ],
    include_package_data=True,
)
