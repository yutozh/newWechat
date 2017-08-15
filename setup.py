#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
 name='newWechat',# 此处填写包名
 version='1.0.0',
 author='zyt',
 author_email='545023318@qq.com',
 description='',
 license='GPL',
 packages=find_packages(),
 install_requires=[
'mysql-python',
'redis',
'flask'
 ],
)