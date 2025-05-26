from setuptools import setup, find_packages

setup(
    name="bellabeat_analysis",
    version="1.0.0",
    description="Analysis of FitBit data for Bellabeat marketing strategy",
    author="Huy Ha",
    author_email="quanghuyha098@gmail.com",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.3",
        "pandas>=2.0.3",
        "matplotlib>=3.7.2",
        "seaborn>=0.12.2",
        "scikit-learn>=1.3.0",
        "jupyter>=1.0.0",
        "plotly>=5.15.0"
    ],
    python_requires=">=3.8",
) 