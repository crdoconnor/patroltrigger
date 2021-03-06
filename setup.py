from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import re
import codecs


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()

long_description = read('README.rst')


setup(name="patroltrigger",
      version="0.3",
      description="Trigger custom commands from filesystem events.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Build Tools',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
      ],
      keywords='development environment tool pyuv epoll build',
      author='Colm O\'Connor',
      author_email='colm.oconnor.github@gmail.com',
      packages=find_packages(exclude=["example.py", ]),
      url='https://github.com/crdoconnor/patroltrigger',
      license='MIT',
      install_requires=['pyuv'],
      package_data={},
      zip_safe=False,
)
