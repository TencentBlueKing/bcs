# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

BASE_DIR = os.path.realpath(os.path.dirname(__file__))


def parse_requirements():
    """
    @summary: 获取依赖
    """
    reqs = []
    if os.path.isfile(os.path.join(BASE_DIR, "requirements.txt")):
        with open(os.path.join(BASE_DIR, "requirements.txt"), 'r') as fd:
            for line in fd.readlines():
                line = line.strip()
                if line:
                    reqs.append(line)
    return reqs


if __name__ == "__main__":
    setup(
        version="1.0.0",
        name="bcs",
        description="",

        cmdclass={},
        packages=find_packages(),
        package_data={'': ['*.txt', '*.TXT', '*.JS', 'test/*']},
        install_requires=parse_requirements(),

        entry_points={'console_scripts': ['bcs = bcs.command_line:main']},

        author="bcs",
        author_email="bcs@tencent.com",
        license="Copyright(c)2010-2018 bcs All Rights Reserved."
    )
