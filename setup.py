# -*- coding=utf-8 -*-
from os import path as os_path
from setuptools import setup

this_directory = os_path.abspath(os_path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='cqbear',
    python_requires='>=3.4.0',
    version="0.4",
    description="A bear-like bot python module for go-cqhttp.",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    author="ChenSmallX",
    author_email='641751205@qq.com',
    url='https://github.com/ChenSmallX/CqBear',
    packages=['cqbear'],
    install_requires=read_requirements('requirements.txt'),
    include_package_data=True,
    license="GNU",
    keywords=['go-cqhttp', 'qqbot', 'Mirai', 'MiraiGo'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        "Operating System :: OS Independent",
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
    ],
)
