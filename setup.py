from setuptools import setup, find_packages

setup(
    name="mp3_converter",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pydub",
        "mutagen",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "mp3_converter=mp3_converter.mp3_converter:main",
        ],
    },
    author="Renier Botha",
    author_email="r.botha91@gmail.com",
    description="A tool to convert FLAC, AIFF, and WAV files to MP3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rendiere/mp3_converter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)