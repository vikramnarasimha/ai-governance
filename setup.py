from setuptools import setup, find_packages

setup(
    name="ai-governance",
    version="0.1.0",
    description="AI Governance tool for Financial Services Institutions",
    author="AI Governance Team",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "sqlalchemy>=2.0.23",
        "python-dotenv>=1.0.0",
        "jinja2>=3.1.2",
        "pandas>=2.1.3",
        "numpy>=1.25.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
        ]
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)