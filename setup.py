from setuptools import setup

setup(
    name='indexos-the-great',
    install_requires=[
        'validators==0.15.0',
        'wikipedia==1.4.0',
        'discord.py==1.4.1',
        'webpreview==1.6.0',
        'APScheduler==3.6.3',
        'discord==1.0.1',
        'pycryptodome==3.19.1',
    ],
    py_modules=[
        'core',
    ],
)
