#!/usr/bin/env python3
"""
良匠工具箱 (Liangjiang Tools) - 调试版主入口文件
这个文件是应用程序的调试版主入口点，添加了错误捕获和日志记录功能。
"""
import sys
import os
import importlib.util
import traceback
import datetime
import tempfile

# 设置日志文件路径
log_file = os.path.join(tempfile.gettempdir(), "liangjiang_tools_debug.log")

def write_log(message):
    """写入日志"""
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            f.write(f"{timestamp} {message}\n")
    except Exception as e:
        print(f"写入日志失败: {e}")

# 记录启动信息
write_log("=== 应用程序启动 ===")
write_log(f"Python版本: {sys.version}")
write_log(f"系统平台: {sys.platform}")

# 记录当前目录和可执行文件路径
if getattr(sys, 'frozen', False):
    # 如果是打包后的应用
    application_path = os.path.dirname(sys.executable)
    write_log(f"运行模式: 已打包应用")
    write_log(f"可执行文件路径: {sys.executable}")
else:
    # 如果是开发环境
    application_path = os.path.dirname(os.path.abspath(__file__))
    write_log(f"运行模式: 开发环境")

write_log(f"应用程序路径: {application_path}")
write_log(f"当前工作目录: {os.getcwd()}")

# 添加当前目录到Python路径
if application_path not in sys.path:
    sys.path.insert(0, application_path)
    write_log(f"已添加 {application_path} 到 Python 路径")

# 记录Python路径
write_log("Python路径:")
for path in sys.path:
    write_log(f"  - {path}")

# 记录环境变量
write_log("环境变量:")
for key, value in os.environ.items():
    write_log(f"  - {key}: {value}")

# 记录目录内容
try:
    write_log(f"应用程序目录内容:")
    for item in os.listdir(application_path):
        item_path = os.path.join(application_path, item)
        if os.path.isdir(item_path):
            write_log(f"  - [目录] {item}")
        else:
            write_log(f"  - [文件] {item} ({os.path.getsize(item_path)} 字节)")
except Exception as e:
    write_log(f"列出目录内容失败: {e}")

def show_error_message(title, message):
    """显示错误消息对话框"""
    try:
        from PyQt6.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(None, title, message)
    except Exception as e:
        write_log(f"显示错误对话框失败: {e}")
        print(f"错误: {title}\n{message}")

def main():
    """应用程序主函数"""
    try:
        write_log("正在导入PyQt6...")
        # 导入PyQt6
        try:
            from PyQt6 import QtWidgets
            write_log("PyQt6导入成功")
        except ImportError as e:
            error_msg = f"未找到PyQt6库: {e}"
            write_log(error_msg)
            show_error_message("导入错误", f"{error_msg}\n请确保已安装所有依赖项。")
            sys.exit(1)
        
        write_log("正在导入login模块...")
        # 动态导入login模块
        try:
            # 首先尝试从main目录导入
            main_dir = os.path.join(application_path, 'main')
            if os.path.exists(main_dir):
                write_log(f"main目录存在: {main_dir}")
                login_path = os.path.join(main_dir, 'login.py')
            else:
                write_log(f"main目录不存在，尝试从资源目录导入")
                # 如果是打包后的应用，可能在资源目录
                if getattr(sys, 'frozen', False):
                    resource_dir = os.path.join(os.path.dirname(sys.executable), 'Resources')
                    if os.path.exists(resource_dir):
                        write_log(f"资源目录存在: {resource_dir}")
                        login_path = os.path.join(resource_dir, 'main', 'login.py')
                    else:
                        write_log(f"资源目录不存在")
                        # 尝试在应用包内查找
                        if sys.platform == 'darwin':
                            bundle_dir = os.path.join(os.path.dirname(sys.executable), '..')
                            login_path = os.path.join(bundle_dir, 'Resources', 'main', 'login.py')
                            write_log(f"尝试从应用包加载: {login_path}")
                        else:
                            login_path = os.path.join(application_path, 'main', 'login.py')
                else:
                    login_path = os.path.join(application_path, 'main', 'login.py')
            
            write_log(f"尝试加载login模块: {login_path}")
            
            if not os.path.exists(login_path):
                write_log(f"login.py文件不存在: {login_path}")
                # 尝试列出可能的位置
                possible_locations = [
                    os.path.join(application_path, 'main'),
                    os.path.join(application_path, 'Resources', 'main'),
                    os.path.join(application_path, '..', 'Resources', 'main')
                ]
                for loc in possible_locations:
                    if os.path.exists(loc):
                        write_log(f"目录存在: {loc}")
                        write_log(f"目录内容:")
                        for item in os.listdir(loc):
                            write_log(f"  - {item}")
                    else:
                        write_log(f"目录不存在: {loc}")
                
                raise FileNotFoundError(f"找不到login.py文件: {login_path}")
            
            spec = importlib.util.spec_from_file_location("login", login_path)
            login = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(login)
            LoginForm = login.Ui_LoginForm
            write_log("login模块加载成功")
        except Exception as e:
            error_msg = f"无法加载登录模块: {e}"
            write_log(error_msg)
            write_log(traceback.format_exc())
            show_error_message("加载错误", f"{error_msg}\n\n详细信息已记录到日志: {log_file}")
            sys.exit(1)
        
        write_log("正在创建应用程序和登录窗口...")
        # 创建应用程序和登录窗口
        try:
            app = QtWidgets.QApplication(sys.argv)
            ui = LoginForm()
            ui.show()
            write_log("应用程序和登录窗口创建成功，开始事件循环")
            sys.exit(app.exec())
        except Exception as e:
            error_msg = f"创建窗口失败: {e}"
            write_log(error_msg)
            write_log(traceback.format_exc())
            show_error_message("运行错误", f"{error_msg}\n\n详细信息已记录到日志: {log_file}")
            sys.exit(1)
    
    except Exception as e:
        error_msg = f"应用程序运行失败: {e}"
        write_log(error_msg)
        write_log(traceback.format_exc())
        show_error_message("严重错误", f"{error_msg}\n\n详细信息已记录到日志: {log_file}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_msg = f"未捕获的异常: {e}"
        write_log(error_msg)
        write_log(traceback.format_exc())
        show_error_message("未捕获的异常", f"{error_msg}\n\n详细信息已记录到日志: {log_file}")
        sys.exit(1) 