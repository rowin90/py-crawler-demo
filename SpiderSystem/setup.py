from setuptools import setup, find_packages

setup(
    name="spiderSystem",
    version="0.1",
    description="spiderSystem module",
    author='raoju',
    url="url",
    license="license",
    packages=find_packages(exclude=[]),
    install_requires=[
        "tornado >= 5.1",
        "pycurl",
    ]

)
