import setuptools
from setuptools import setup

setup(name='cfv',
      version='0.2',
      description='Management framework for distributed virtualized camera functions',
      url='https://github.com/wontoniii/cfv',
      author='Francesco Bronzino, Shubham Jain',
      author_email='wontoniii@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False,
      classifiers=[
            "Programming Language :: Python :: 3.7",
            "Operating System :: OS Independent",
      ],
      install_requires=[
            'asyncio',
            'opencv-python',
            'aiohttp'
      ],
      scripts=['cfv.py']
      )
