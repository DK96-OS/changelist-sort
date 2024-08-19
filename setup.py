"""Setup Package Configuration
"""
from setuptools import setup, find_packages


setup(
    name="changelist-sort",
    version="0.1",
	author='DK96-OS',
	description='CLI Tool for Sorting Android Studio Changelists',
    long_description=open('README.md').read(),
    url="https://github.com/DK96-OS/changelist-sort/",
	project_urls={
        "Issues": "https://github.com/DK96-OS/changelist-sort/issues",
        "Source Code": "https://github.com/DK96-OS/changelist-sort/"
	},
	license='GPLv3',
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts': [
            'changelist-sort=changelist_sort.__main__:main',
            'changelist_sort=changelist_sort.__main__:main',
            'cl-sort=changelist_sort.__main__:main',
            'cl_sort=changelist_sort.__main__:main',
        ],
    },
    python_requires='>=3.10',
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)