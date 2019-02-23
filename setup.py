from setuptools import setup, find_packages

setup(name='Stackstats',
      version='1.0',
      description='This basic python app consumes the StackExchange API to retrieve data and create basic statistics',
      author='Papavasileiou Lampros',
      author_email='lamprospapav@gmail.com',
      keywords='stackexchange',
      install_requires=['requests','json2html'],
      packages=find_packages(exclude=['test']),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      entry_points={
          "console_scripts": [
              "stacks = stackstats.__main__:main"
          ]
      }

      )
