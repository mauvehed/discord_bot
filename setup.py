from setuptools import setup, find_packages

setup(
    name="discord_bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "discord.py>=2.3.2",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
        ],
    },
) 