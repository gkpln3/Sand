from setuptools import setup, find_packages

setup(
    name='sand',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sand = sand.main:main'
        ]
    },
    install_requires=[
        "docker"
    ],
    author='Guy Kaplan',
    description='Sand is a Dockerfile generator',
    license='MIT',
    keywords='sand docker dockerfile build',
    url='https://github.com/gkpln3/Sand',
    classifiers=[
    ],
)
