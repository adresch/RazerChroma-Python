try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='chromapythonapp',
    version='0.1',
    description='Python Distribution Utilities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    py_modules=[
        'chromapythonapp',
        '__init__',
    ],
)