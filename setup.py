from setuptools import setup, find_packages

setup(
    name='gs2video',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'google-auth-oauthlib',
        'gtts',
        'moviepy',
    ],
    entry_points={
        'console_scripts': [
            'gs2video=gs2video.cli:main',
        ],
    },
)