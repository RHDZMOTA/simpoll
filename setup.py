from setuptools import setup


with open("requirements.txt", "r") as file:
    reqs = file.read().splitlines()


setup(
    name="simpoll",
    version="0.1.0",
    description="Simple Poll Application",
    package_dir={
        "": "src"
    },
    install_requires=reqs
)
