#!/usr/bin/env python3
"""
良匠工具箱 (Liangjiang Tools) - 主入口文件
这个文件是应用程序的主入口点，用于启动登录界面。
"""
import sys
import os
import importlib.util
import traceback

# 确定应用程序路径
if getattr(sys, 'frozen', False):
    # 如果是打包后的应用
    application_path = os.path.dirname(sys.executable)
    # 对于macOS应用程序包，需要特殊处理
    if sys.platform == 'darwin':
        # 检查是否在应用程序包内
        if 'Contents/MacOS' in application_path:
            # 获取Resources目录
            resources_path = os.path.join(os.path.dirname(os.path.dirname(application_path)), 'Resources')
            # 添加Resources目录到Python路径
            if resources_path not in sys.path:
                sys.path.insert(0, resources_path)
else:
    # 如果是开发环境
    application_path = os.path.dirname(os.path.abspath(__file__))

# 添加应用程序路径到Python路径
if application_path not in sys.path:
    sys.path.insert(0, application_path)

# 打印路径信息，帮助调试
print(f"应用程序路径: {application_path}")
print(f"Python路径: {sys.path}")

# 导入PyQt6
try:
    from PyQt6 import QtWidgets
    from PyQt6.QtWidgets import QMessageBox
except ImportError:
    print("错误: 未找到PyQt6库。请确保已安装所有依赖项。")
    print("可以使用以下命令安装依赖: pip install PyQt6 pymysql requests")
    sys.exit(1)

def show_error(title, message):
    """显示错误对话框"""
    try:
        app = QtWidgets.QApplication.instance()
        if not app:
            app = QtWidgets.QApplication(sys.argv)
        QMessageBox.critical(None, title, message)
    except:
        print(f"错误: {title}\n{message}")

def find_login_module():
    """查找login模块"""
    # 可能的路径列表
    possible_paths = [
        os.path.join(application_path, 'main', 'login.py'),
        os.path.join(application_path, 'Resources', 'main', 'login.py')
    ]
    
    # 如果是macOS打包应用
    if sys.platform == 'darwin' and getattr(sys, 'frozen', False):
        bundle_dir = os.path.join(os.path.dirname(sys.executable), '..')
        possible_paths.append(os.path.join(bundle_dir, 'Resources', 'main', 'login.py'))
    
    # 尝试所有可能的路径
    for path in possible_paths:
        if os.path.exists(path):
            print(f"找到login模块: {path}")
            return path
    
    # 如果找不到，返回默认路径
    default_path = os.path.join(application_path, 'main', 'login.py')
    print(f"使用默认login模块路径: {default_path}")
    return default_path

def main():
    """应用程序主函数"""
    try:
        # 动态导入login模块
        login_path = find_login_module()
        
        if not os.path.exists(login_path):
            error_msg = f"找不到login.py文件: {login_path}"
            print(error_msg)
            # 尝试列出可能的位置
            print("尝试列出可能的位置:")
            for base_dir in [application_path, os.path.join(application_path, 'Resources')]:
                if os.path.exists(os.path.join(base_dir, 'main')):
                    print(f"main目录存在于: {os.path.join(base_dir, 'main')}")
                    print(f"内容: {os.listdir(os.path.join(base_dir, 'main'))}")
            
            show_error("文件错误", error_msg)
            sys.exit(1)
        
        try:
            spec = importlib.util.spec_from_file_location("login", login_path)
            login = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(login)
            LoginForm = login.Ui_LoginForm
        except Exception as e:
            error_msg = f"无法加载登录模块: {e}"
            print(error_msg)
            print(traceback.format_exc())
            show_error("加载错误", error_msg)
            sys.exit(1)
        
        # 创建应用程序和登录窗口
        app = QtWidgets.QApplication(sys.argv)
        ui = LoginForm()
        ui.show()
        sys.exit(app.exec())
    
    except Exception as e:
        error_msg = f"应用程序启动失败: {e}"
        print(error_msg)
        print(traceback.format_exc())
        show_error("启动错误", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main() 