from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='docker-sand',
    version='0.0.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sand = sand.internal.main:main'
        ]
    },
    install_requires=[
        "watchdog",
    ],
    author='Guy Kaplan',
    description='Sand is a Dockerfile generator based on python that allows you to write your Dockerfile in a more convenient way.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='sand docker dockerfile build',
    url='https://github.com/gkpln3/Sand',
    classifiers=[
    ],
)
