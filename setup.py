from setuptools import setup


# constants ----------

VERSION = "0.3.1"

with open('README.md', 'r') as fp:
    README = fp.read()


# setup -----------

setup(
    name="insult_error",
    version=VERSION,
    description='Intentionally insulting exceptions',
    long_description=README,
    long_description_content_type='text/markdown',
    author="Keith Ma",
    author_email="itsallnans@gmail.com",
    url='https://github.com/keithfma/insult_error',
    py_modules=['insult_error'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        ]
    )
