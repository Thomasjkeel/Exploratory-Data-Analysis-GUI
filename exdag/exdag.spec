# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path
block_cipher = None

if sys.platform == 'darwin':
  pathex_path = Path(os.getcwd()[:-len(os.getcwd().split('/')[-1])-1])



a = Analysis(['exdag.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
if sys.platform == 'darwin':
  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='ExDaG',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=True) 
# Package the executable file into .app if on OS X
if sys.platform == 'darwin':
   app = BUNDLE(exe,
                name='ExDaG.app',
                info_plist={
                  'NSHighResolutionCapable': 'True'
                })

# Generate an executable file
# Notice that the icon is a .ico file, unlike macOS
# Also note that console=False
if sys.platform == 'win32' or sys.platform == 'win64' or sys.platform == 'linux':
  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='ExDaG',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ExDaG')


