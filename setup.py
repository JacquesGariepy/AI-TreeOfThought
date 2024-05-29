from setuptools import setup, find_packages

setup(
    name='treeofthought',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'graphviz==0.19.1',
        'litellm==1.39.2',
        'requests==2.32.1',
        'unittest2==1.1.0'
    ],
)
