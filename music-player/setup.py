from setuptools import setup

APP_NAME = 'Galaxy'
APP = ['main.py']
DATA_FILES = [('music',['music/']),
            ('src', ['./src/'])]
OPTIONS =   {
    'packages':['pygame', 'PyQt6'],
    'iconfile': 'src/icon.icns',
    'argv_emulation': True,
    'plist':{
                'CFBundleName': APP_NAME,
                'CFBundleDisplayName': APP_NAME,
                'CFBundleVersion': '0.1.1 beta',
                'CFBundleGetInfoString': 'Desktop Founds Control',
                'CFBundleShortVersionString': '0.1.1',
                'NSHumanReadableCopyright': 'Copyright (c) 2022, NearlyQ, All Rights Reserved'
            }
            }

setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
