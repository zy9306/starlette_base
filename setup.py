from setuptools import find_packages, setup

setup(
    name="starlette_base",
    version="0.1.0",
    author="z",
    author_email="",
    description="A base project for Starlette",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "aiosqlite==0.20.0",
        "asyncmy==0.2.10",
        "pendulum==3.0.0",
        "pydantic==2.10.5",
        "redis==5.2.1",
        "spectree==1.4.4",
        "starlette==0.45.2",
        "tortoise-orm==0.23.0",
        "uvicorn==0.34.0",
    ],
)
