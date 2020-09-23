
from setuptools import setup, find_packages


def is_raspberry_pi() -> bool:

    try:
        with open('/proc/cpuinfo', 'r') as cpuinfo:
            found = False
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    found = True
                    label, value = line.strip().split(':', 1)
                    value = value.strip()
                    if value not in (
                        'BCM2708',
                        'BCM2709',
                        'BCM2835',
                        'BCM2836'
                    ):
                        return False
            if not found:
                return False
    except IOError:
        return False

    return True


install_requires = ["numpy", "pyserial"]
if is_raspberry_pi():
    install_requires.append("pigpio")
    install_requires.append("RPi.GPIO")

setup(
    name="pisat",
    version="0.0.0",
    description="framework for building cansat models",
    author="Yunhyeon Jeong",
    author_email="spaceship2021@gmail.com",
    license=license,
    packages=find_packages(exclude=("docs", "tests", "sample")),
    install_requires=install_requires
)