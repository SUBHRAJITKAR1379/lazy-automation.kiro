"""Setup configuration for File Organization Bot."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="file-organizer-bot",
    version="1.0.0",
    author="Your Name",
    description="Automatically organize files in your Downloads folder by type and date",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/file-organizer-bot",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Filesystems",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "watchdog>=2.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "hypothesis>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "file-organizer=file_organizer.cli:main",
        ],
    },
)
