from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Stack exchange stats extractor'

setup(
    name="stats",
    version=VERSION,
    author="Dimitris Oikonomou",
    author_email="dimoiko100@gmail.com",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "pandas ~= 1.1.5", 
        "loguru ~= 0.6.0", 
        "flatten_json ~= 0.1.13", 
        "json2html ~= 1.3.0", 
        "requests ~= 2.27.1"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.1",
            "pytest-mock>=3.6.0",
            "mkdocs>=1.3.1",
            "mkdocs-material>=8.2.11",
            "mkdocstrings[python]>=0.17.0"
        ]
    },
    packages=find_packages(),
    entry_points={
        'console_scripts': ['stats = stats.cmd.cmd:run']
    },
)