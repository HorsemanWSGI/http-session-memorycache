import os
from setuptools import setup, find_packages, Extension


version = '0.1'

install_requires = [
    'http_session',
    'cromlech.marshallers',
]

tests_require = [
    'pytest',
    'freezegun'
]

setup(
    name='http_session_memorycache',
    version=version,
    description="Cython in-memory cache storage",
    long_description=(
        open("README.rst").read() + "\n" +
        open(os.path.join("docs", "HISTORY.rst")).read()
    ),
    classifiers=[
        'License :: OSI Approved :: BSD License',
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='SQLite, session, HTTP',
    author='Souheil Chelfouh',
    author_email='trollfot@gmail.com',
    url='',
    license_files=(
        'docs/LICENSE.txt',
    ),
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    tests_require=tests_require,
    install_requires=install_requires,
    extras_require={'test': tests_require},
    ext_modules=[
          Extension(
            "http_session_memorycache.store",
            ["src/http_session_memorycache/store.c"],
            extra_compile_args=["-O3"],  # Max optimization when compiling.
        )
    ]
)
