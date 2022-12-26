import PyInstaller.__main__
from variables import APP_NAME

PyInstaller.__main__.run([
    'main.py',
    '--clean',
    '--onedir',
    '--windowed',
    '--noconfirm',
    '--add-data=icon;icon',
    '--add-data=paths.txt;.',
    '--add-data=templates;templates',
    '--icon=icon/card.ico',
    '--name=' + str(APP_NAME),
])