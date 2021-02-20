from distutils.core import setup

setup(
    name='pyplot_over_ip',
    version='1.0',
    entry_points={
        'console_scripts': ['pyplot-over-ip=pyplot_over_ip.receiver:main'],
    },
    install_requires=[
        "requests",
        "matplotlib"
    ],
)
