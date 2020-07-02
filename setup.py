import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-api-tools",
    version="1.0.8",
    author="ScholarPack",
    author_email="dev@scholarpack.com",
    description="Tooling to assist with building Flask APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ScholarPack/flask-api-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["flask >= 1.1", "flask-limiter >= 1.3", "redis >= 2.10"],
)
