from setuptools import setup, find_packages

setup(
    name='freshman2019',
    version='0.1.0',
    description='新人課題2019',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'freshman2019=app.__main__:main',
        ],
    },
)
