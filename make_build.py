import os

import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=MiniEditor',
    '--windowed',
    os.path.join('app.py'),
])
