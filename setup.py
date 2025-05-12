from setuptools import setup, find_packages

setup(
    name="oml-copilot",
    version="0.1.0",
    description="AI assistant for Ontological Modeling Language",
    author="Ajay Sreekumar",
    author_email="ajaysreekumar@arizona.edu",
    url="https://github.com/ajaysreekumar47/OML-Copilot",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "lark>=1.1.5",
        "sentence-transformers>=2.2.2",
        "tiktoken>=0.5.1",
        "numpy>=1.20.0",
        "scikit-learn>=1.0.0",
        "regex>=2022.0.0",
        "ollama>=0.1.0",
        "tqdm>=4.50.0",
        "pyyaml>=6.0",
        "requests>=2.27.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
