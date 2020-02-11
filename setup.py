import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jrnl-backup",
    version="0.0.1",
    author="Gurkirpal Singh",
    author_email="gurkirpal204@gmail.com",
    description="Script to backup your jrnl.sh journal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gpalsingh/jrnl-backup",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'jrnl-backup=jrnl_backup:main',
            'jrnlbackup=jrnl_backup:main',
        ],
    },
)