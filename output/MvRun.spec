# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\JTWhitney\\PycharmProjects\\MvRun\\MvRun.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\JTWhitney\\PycharmProjects\\MvRun\\lib', 'lib/'), ('C:\\Users\\JTWhitney\\PycharmProjects\\MvRun\\ui', 'ui/'), ('C:\\Users\\JTWhitney\\PycharmProjects\\MvRun\\eof.bat', '.'), ('C:\\Users\\JTWhitney\\PycharmProjects\\MvRun\\nada.iwp', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MvRun',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\JTWhitney\\PycharmProjects\\MvRun\\MvRun.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MvRun',
)
