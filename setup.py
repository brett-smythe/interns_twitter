"""Setup for interns_twitter service"""
from codecs import open as cod_open
from setuptools import setup, find_packages


with cod_open('README.md', encoding='utf-8') as inf:
    long_description = inf.read()

reqs = []
with open('requirements.txt') as inf:
    for line in inf:
        line = line.strip()
        reqs.append(line)

setup(
    name='interns-twitter',
    version='0.1.7',
    description='Worker to gather twitter text sources',
    long_description=long_description,
    author='Brett Smythe',
    author_email='smythebrett@gmail.com',
    maintainer='Brett Smythe',
    maintainer_email='smythebrett@gmail.com',
    url='https://github.com/brett-smythe/interns_twitter',
    packages=find_packages(),
    install_requires=reqs,
    entry_points={
        'console_scripts': [
            'interns-twitter = interns_twitter.main:run'
        ]
    }
)
