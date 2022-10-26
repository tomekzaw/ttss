import setuptools  # type: ignore

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ttss',
    version='0.5.0',
    author='Tomek Zawadzki',
    author_email='tomekzawadzki98@gmail.com',
    description='A Python wrapper for TTSS API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tomekzaw/ttss',
    project_urls={
        'Bug Tracker': 'https://github.com/tomekzaw/ttss/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_data={
        'ttss': ['py.typed'],
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.8',
    install_requires=['requests', 'pytz'],
    tests_require=['pytest', 'pytest-freezegun', 'requests-mock']
)
