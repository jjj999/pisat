from setuptools import setup, find_packages

setup(
    name="pisat",
    version="0.0.0",
    description="framework for building cansat models",
    author="Yunhyeon Jeong",
    author_email="spaceship2021@gmail.com",
    license=license,
    packages=find_packages(exclude=("docs", "tests", "sample")),
    install_requires=[
        "numpy",
        "pigpio",
        "pyserial"
    ]
)