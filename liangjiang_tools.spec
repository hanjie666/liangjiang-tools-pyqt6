# -*- mode: python ; coding: utf-8 -*-
import os
import glob

# 不使用加密（PyInstaller 6.0+已移除加密功能）
block_cipher = None

# 获取必要的资源文件（非Python源代码）
resource_files = []
if os.path.exists('view'):
    for file in os.listdir('view'):
        if file.endswith('.ui'):
            resource_files.append(('view/' + file, 'view'))

# 只包含必要的资源文件，不包含源代码
all_datas = [
    # 只包含UI文件和其他资源，不包含Python源代码
    ('view/*.ui', 'view'),        # 包含UI文件
    ('config.json', '.'),         # 包含配置文件
    ('app_icon.ico', '.'),        # 包含图标文件
]

# 添加UI文件
all_datas.extend(resource_files)

# 添加main目录的模块作为二进制文件
binaries = []

a = Analysis(
    ['main.py'],  # Main script to execute
    pathex=[
        os.path.abspath('.'),
        os.path.abspath('./main'),
        os.path.abspath('./view'),
    ],
    binaries=binaries,
    datas=all_datas,
    hiddenimports=[
        'pymysql', 
        'pymysql.cursors', 
        'PyQt6.QtCore', 
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'PyQt6.QtSql',
        'PyQt6.QtNetwork',
        'datetime',
        'json',
        'os',
        'sys',
        'importlib',
        'traceback',
        'shutil',
        'glob',
        'time',
        'login',           # 添加login模块作为隐藏导入
        'dc-chat',         # 添加dc-chat模块作为隐藏导入
        'requests',        # 添加requests模块
        'threading',       # 添加threading模块
        'random',          # 添加random模块
        'main',            # 添加main模块自身
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 将模块文件直接添加到打包文件中
a.datas += [('main/dc-chat.py', os.path.join(os.path.abspath('./main'), 'dc-chat.py'), 'DATA')]
a.datas += [('main/login.py', os.path.join(os.path.abspath('./main'), 'login.py'), 'DATA')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,       # 将二进制文件直接包含在exe中
    a.zipfiles,       # 将zip文件直接包含在exe中
    a.datas,          # 将数据文件直接包含在exe中
    [],
    name='良匠工具箱',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,    # 隐藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# For macOS
app = BUNDLE(
    exe,
    name='良匠工具箱.app',
    bundle_identifier='com.liangjiang.tools',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '1.0.0',
    },
)