from setuptools import setup, find_packages

setup(
    name="endless-runner",
    version="2.0.0",
    description="Endless Runner Game",
    author="Saravanan Gnanaguru",
    author_email="g.gsaravanan@gmail.com",
    url="https://github.com/chefgs/endless-runner",
    packages=find_packages(),
    scripts=["endless-runner-stickman-sounds.py"],
    install_requires=[
        "pygame>=2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)