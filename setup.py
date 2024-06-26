import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MBT-pkg-sundr007",
    version="0.0.1",
    author="sundr007",
    author_email="esundry@gmail.com",
    description="A model based Tester generator.  Inputs a model - expands it to all states, and writes tests to verify it.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sundr007/Model-Based-Test-Generator",
    project_urls={
        "Bug Tracker": "https://github.com/sundr007/ModelBasedTester-AllPaths/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
    'numpy',
    'networkx',
    'PyPDF2',

    ],
    include_package_data=True,
    package_data={
                    '':['Editor/*','newProject/*'],
                    },
)
