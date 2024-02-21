'''
Author: Vincent Young
Date: 2023-04-27 00:42:10
LastEditors: Vincent Young
LastEditTime: 2024-02-21 13:07:28
FilePath: /PyDeepLX/setup.py
Telegram: https://t.me/missuo

Copyright © 2023 by Vincent, All Rights Reserved. 
'''
from setuptools import setup, find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name="PyDeepLX",
    author="missuo",
    version="1.0.7",
    license='MIT',
    long_description= long_description,
    long_description_content_type="text/markdown",
    author_email="i@yyt.moe",
    description="A Python package for unlimited DeepL translation",
    url='https://github.com/OwO-Network/PyDeepLX',
    packages=find_packages(),
    include_package_data=False,
    platforms='any',
    zip_safe=False,

    install_requires=['httpx[socks,brotli]'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]

)
