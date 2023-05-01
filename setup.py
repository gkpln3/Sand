from setuptools import setup, find_packages

setup(
    name='docker-sand',
    version='0.0.1',
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
    license='MIT',
    keywords='sand docker dockerfile build',
    url='https://github.com/gkpln3/Sand',
    classifiers=[
    ],
)
