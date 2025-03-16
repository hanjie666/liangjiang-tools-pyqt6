# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # Main script to execute
    pathex=[],
    binaries=[],
    datas=[
        ('main/dc-chat.py', 'main'),  # Include dc-chat.py
        ('main/login.py', 'main'),    # Include login.py
        ('view/*.ui', 'view'),        # Include UI files
    ],
    hiddenimports=['pymysql', 'pymysql.cursors', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='良匠工具箱',
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
    icon='app_icon.ico',  # You'll need to create this icon file
)

# For macOS
app = BUNDLE(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='良匠工具箱.app',
    icon='app_icon.icns',  # You'll need to create this icon file
    bundle_identifier='com.liangjiang.tools',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '1.0.0',
    },
)

# For Windows
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='良匠工具箱',
) 