# -*- mode: python -*-

block_cipher = None


a = Analysis(['fet_main.py'],
             pathex=['C:\\Users\\jmetr\\_data\\mandats\\FET_new\\fet_elt_epub\\prg'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='fet_main',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='logo_fet.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='fet_main')
