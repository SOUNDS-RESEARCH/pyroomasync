import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name='pyroomasync',
  version='0.0.25',
  description='Simulate asyncronous microphone array recordings',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/ImperialCollegeLondon/sap-pyroomasync',
  author='Eric Grinstein',
  author_email='e.grinstein@imperial.ac.uk',
  license='MIT',
  packages=["pyroomasync", "pyroomasync.utils"],
  zip_safe=False,
  install_requires=[
    'matplotlib',
    'librosa',
    'pyroomacoustics'
  ]
)
