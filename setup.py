from setuptools import setup, find_packages

with open("requirements.txt") as requirements:
    with open("test_requirements.txt") as test_requirements:
        setup(
                name="pairedmq",
                version="0.0.0",
                packages=find_packages(),
                url="https://github.com/gaggle/pairedmq",
                license="MIT",
                author="gaggle",
                author_email="mail@jonlauridsen.com",
                description="Simple paired client/server RPC",
                long_description=open("README.md").read(),
                install_requires=requirements.read().splitlines(),
                test_suite="test",
                tests_require=test_requirements.read().splitlines(),
        )
