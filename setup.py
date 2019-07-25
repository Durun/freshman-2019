from setuptools import setup, find_packages

setup(
    name='freshman2019',
    version='0.1.0',
    description='新人課題2019',
    packages=find_packages(),
    install_requires=[
        'slackclient',
        'rpi.gpio',
        'opencv-python',
        'requests',
        'pyocr',
    ],
    entry_points={
        'console_scripts': [
            'freshman2019=freshman2019.__main__:main',
        ],
    },
)
