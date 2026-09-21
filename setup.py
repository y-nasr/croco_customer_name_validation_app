from setuptools import find_packages, setup

with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]

# get version from __version__ variable in customer_name_validation/__init__.py
from customer_name_validation import __version__ as version

setup(
    name="customer_name_validation",
    version=version,
    description="Enforces that Customer names contain only letters (any script) plus spaces, hyphens, apostrophes and periods.",
    author="Croco IT",
    author_email="info@crocoit.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
