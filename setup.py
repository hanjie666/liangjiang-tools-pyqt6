"""
使用 py2app 打包良匠工具箱应用

使用方法:
    python setup.py py2app
"""

from setuptools import setup
import os
import sys
import platform
import glob

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取Python版本
python_version = f"{sys.version_info.major}.{sys.version_info.minor}"

# 定义应用程序入口
APP = ['main.py']

# 定义需要包含的数据文件
DATA_FILES = [
    ('main', ['main/dc-chat.py', 'main/login.py']),
]

# 定义 py2app 选项
OPTIONS = {
    'argv_emulation': False,  # 不使用 argv 模拟
    'iconfile': 'app_icon.icns' if os.path.exists('app_icon.icns') else None,  # 图标文件
    'plist': {
        'CFBundleName': '良匠工具箱',
        'CFBundleDisplayName': '良匠工具箱',
        'CFBundleIdentifier': 'com.liangjiang.tools',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2023 良匠工具箱',
        'NSHighResolutionCapable': True,
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'LSMinimumSystemVersion': '10.13',  # 最低系统要求
    },
    'packages': ['PyQt6', 'pymysql', 'requests'],  # 需要包含的包
    'includes': [
        'importlib', 'datetime', 'json', 'random', 'time', 'threading', 'traceback',
        'importlib.util', 'os', 'sys', 'tempfile'
    ],  # 需要包含的模块
    'excludes': ['tkinter', 'matplotlib', 'numpy', 'scipy'],  # 排除不需要的模块
    'resources': [],  # 移除view目录
    'frameworks': [],  # 额外的框架
    'strip': True,  # 去除调试符号
    'optimize': 1,  # 优化级别 (1比2更安全)
    'semi_standalone': False,  # 完全独立的应用程序
    'site_packages': True,  # 包含site-packages
    'arch': platform.machine(),  # 架构
    'qt_plugins': ['platforms', 'styles'],  # 包含Qt插件
    'matplotlib_backends': '-',  # 不包含matplotlib后端
}

setup(
    name='良匠工具箱',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'PyQt6',
        'pymysql',
        'requests',
    ],
    python_requires=f'>={python_version}',
)
