from setuptools import setup, find_packages

setup(
    name="pakistan-digital-validator",
    version="1.0.0",
    author="516 Hackers",
    author_email="your-email@example.com",
    description="Ethical toolkit for Pakistani CNIC and phone number validation",
    long_description="A comprehensive, ethical toolkit for Pakistani CNIC and phone number validation",
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "pak_validator": ["data/*.json"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "phonenumbers>=8.12.0",
        "pytesseract>=0.3.8",
        "opencv-python>=4.5.0", 
        "Pillow>=8.3.0",
        "numpy>=1.21.0",
    ],
)
