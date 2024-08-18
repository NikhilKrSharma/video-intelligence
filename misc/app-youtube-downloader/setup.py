from setuptools import setup

APP = ['youtube-video-downloader.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter'],
    'includes': [
        'jaraco.path',
        'jaraco.test',
        'jaraco.test.cpython',
        '_io._WindowsConsoleIO',
        '_overlapped',
        'itertools.batched',
        'pytest',
        '_manylinux',
        '_typeshed',
        'android',
        'jnius',
        'mod',
        'mod2',
        'nspkg',
        'pdp517',
        'pkg1',
        'pkg1.pkg2'
        'tkinter', 
        'pytube'
    ],
    'iconfile': './icon.png',  # Optional: Path to your .icns icon file
    'plist': {
        'CFBundleName': 'YouTube-Video-Downloader-Bundle',
        'CFBundleDisplayName': 'YouTube-Video-Downloader-App',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSHumanReadableCopyright': '© 2023 Nikhil Sharma',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
