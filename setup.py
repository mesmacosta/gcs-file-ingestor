from setuptools import find_namespace_packages, setup

packages = [package for package in find_namespace_packages(where='./src',
                                                           include='gcs_file_ingestor.*')]

setup(
    name='gcs-file-ingestor',
    version='0.0.1',
    author='Marcelo Costa',
    author_email='mesmacosta@gmail.com',
    description='Library for ingesting files into Google Cloud Storage buckets',
    platforms='Posix; MacOS X; Windows',
    packages=packages,
    package_dir={
        '': 'src'
    },
    include_package_data=True,
    install_requires=(
        'pandas',
        'google-cloud-storage',
        'gcsfs',
    ),
    setup_requires=(
        'pytest-runner',
    ),
    tests_require=(
        'pytest-cov',
    ),
    classifiers=(
        'Development Status :: 1 - Alpha',
        'Programming Language :: Python :: 3.7',
    ),
)
