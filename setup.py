from setuptools import setup

with open('README.rst', 'r') as fp:
    readme=fp.read()

setup(
    name="insult_error",
    version="0.3.0",
    description='Intentionally insulting exceptions',
    long_description=readme,
    author="Keith Ma",
    author_email="itsallnans@gmail.com",
    url='https://github.com/keithfma/insult_error',
    py_modules=['insult_error'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        ]
    )
