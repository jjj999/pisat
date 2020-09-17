from setuptools import setup, find_packages

setup(
    name="pisat",
    version="0.0.0",
    description="framework for making cansat models",
    author="Yunhyeon Jeong",
    author_email="spaceship2021@gmail.com",
    license=license,
    packages=find_packages(exclude=("docs", "tests", "sample")),
    install_requires=[
        "im920 @ git+https://github.com/jjj999/im920_py.git",
        "numpy",
        "pigpio",
        "pyserial"
    ]
)