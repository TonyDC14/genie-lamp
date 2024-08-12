from setuptools import setup, find_packages

setup(
    name='project_enhancer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'project_enhancer=src.main:main',
        ],
    },
)
