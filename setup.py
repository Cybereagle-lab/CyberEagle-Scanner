from setuptools import setup

setup(
    name="cybereagle",
    version="1.0.0",
    description="An advanced website scanning tool for ethical hacking",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/your-username/CyberEagle-Scanner",
    py_modules=["cybereagle"],
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pyfiglet",
    ],
    entry_points={
        "console_scripts": [
            "cybereagle=cybereagle:main",
        ],
    },
)