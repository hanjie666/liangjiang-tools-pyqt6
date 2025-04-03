#!/usr/bin/env python3
"""
良匠工具箱 (Liangjiang Tools) - 主入口文件
这个文件是应用程序的主入口点，用于启动登录界面。
"""
import sys
import os
import importlib.util
import traceback
import shutil
import glob
import time
import json
import types

# 确定是否是打包后的应用
is_frozen = getattr(sys, 'frozen', False)

# 设置日志文件
log_file = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "liangjiang_tools_log.txt")
def log_message(message, print_to_console=False):
    """记录日志消息"""
    if print_to_console:
        print(message)
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    except Exception as e:
        if print_to_console:
            print(f"写入日志失败: {e}")

log_message("=" * 50)
log_message(f"应用程序启动时间: {__import__('datetime').datetime.now()}")
log_message(f"Python版本: {sys.version}")
log_message(f"系统平台: {sys.platform}")
log_message(f"运行模式: {'打包应用' if is_frozen else '开发环境'}")
log_message("=" * 50)

# 确定应用程序路径
if is_frozen:
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
                log_message(f"添加macOS资源路径: {resources_path}")
else:
    # 如果是开发环境
    application_path = os.path.dirname(os.path.abspath(__file__))

# 添加应用程序路径到Python路径
if application_path not in sys.path:
    sys.path.insert(0, application_path)

# 处理main目录路径
main_path = os.path.join(application_path, 'main')
if not is_frozen:
    # 在开发环境中，确保main目录存在并添加到路径
    if os.path.exists(main_path) and main_path not in sys.path:
        sys.path.insert(0, main_path)
    else:
        log_message(f"警告: main目录不存在: {main_path}")
        # 尝试创建main目录
        try:
            os.makedirs(main_path, exist_ok=True)
            log_message(f"已创建main目录: {main_path}")
            if main_path not in sys.path:
                sys.path.insert(0, main_path)
        except Exception as e:
            log_message(f"创建main目录失败: {e}")
else:
    # 在打包环境中，不需要创建main目录，直接从内部资源加载
    log_message(f"打包环境: 将从内部资源加载模块")
    # 但仍将main路径添加到Python路径，以便importlib可以找到模块
    if main_path not in sys.path:
        sys.path.insert(0, main_path)

# 导入PyQt6
try:
    from PyQt6 import QtWidgets, QtCore, QtGui
    from PyQt6.QtWidgets import QMessageBox, QApplication
    log_message("成功导入PyQt6")
except ImportError as e:
    error_msg = f"错误: 未找到PyQt6库。请确保已安装所有依赖项。\n详细错误: {e}"
    log_message(error_msg)
    log_message("可以使用以下命令安装依赖: pip install PyQt6 pymysql requests")
    sys.exit(1)

def show_error(title, message):
    """显示错误对话框"""
    log_message(f"显示错误对话框: {title} - {message}")
    try:
        app = QtWidgets.QApplication.instance()
        if not app:
            app = QtWidgets.QApplication(sys.argv)
        QMessageBox.critical(None, title, message)
    except Exception as e:
        log_message(f"显示错误对话框失败: {e}")
        print(f"错误: {title}\n{message}")

# 在打包环境中提取模块文件
def extract_module_file(module_name):
    """从打包环境中提取模块文件"""
    if not is_frozen:
        return None
    
    # 源文件路径（在打包文件内部）
    source_path = f"main/{module_name}.py"
    
    # 目标文件路径（在临时目录中）
    temp_dir = os.path.join(application_path, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    target_path = os.path.join(temp_dir, f"{module_name}.py")
    
    try:
        # 从打包文件中提取模块文件
        from importlib.resources import files, as_file
        resource_path = files('main').joinpath(f"{module_name}.py")
        with as_file(resource_path) as extracted_file:
            with open(target_path, 'wb') as f:
                with open(extracted_file, 'rb') as source:
                    f.write(source.read())
        
        log_message(f"从打包环境提取模块文件: {source_path} -> {target_path}")
        return target_path
    except Exception as e:
        log_message(f"从打包环境提取模块文件失败: {e}")
        log_message(traceback.format_exc())
        
        # 尝试使用备用方法提取
        try:
            # 检查是否可以直接访问文件系统
            from PyInstaller import compat
            from PyInstaller.archive.readers import CArchiveReader
            
            # 获取打包文件路径
            executable = sys.executable
            
            # 尝试从打包文件中读取数据
            archive = CArchiveReader(executable)
            data = archive.extract(f"main/{module_name}.py")[1]
            
            # 将数据写入临时文件
            with open(target_path, 'wb') as f:
                f.write(data)
            
            log_message(f"使用备用方法从打包环境提取模块文件: {source_path} -> {target_path}")
            return target_path
        except Exception as e2:
            log_message(f"备用方法提取模块文件失败: {e2}")
            log_message(traceback.format_exc())
            
            # 最后尝试直接从resources目录读取文件
            try:
                # 直接复制打包时添加的数据文件
                source_in_pkg = os.path.join(application_path, source_path)
                if os.path.exists(source_in_pkg):
                    with open(source_in_pkg, 'rb') as src, open(target_path, 'wb') as dst:
                        dst.write(src.read())
                    log_message(f"从打包路径直接复制模块文件: {source_in_pkg} -> {target_path}")
                    return target_path
                else:
                    log_message(f"模块文件在打包路径中不存在: {source_in_pkg}")
            except Exception as e3:
                log_message(f"直接复制模块文件失败: {e3}")
            
            return None

# 创建占位符模块的函数
def create_placeholder_module(module_name):
    """创建占位符模块"""
    log_message(f"创建占位符模块: {module_name}")
    
    if module_name == "login":
        # 创建一个简单的登录模块
        class PlaceholderLoginForm:
            def __init__(self):
                self.app = QtWidgets.QApplication.instance()
                if not self.app:
                    self.app = QtWidgets.QApplication(sys.argv)
                
            def show(self):
                QMessageBox.critical(None, "模块错误", f"找不到登录模块 {module_name}。\n请联系开发者获取帮助。")
                sys.exit(1)
        
        return type('PlaceholderModule', (), {'Ui_LoginForm': PlaceholderLoginForm})
    
    elif module_name == "dc-chat":
        # 创建一个简单的dc-chat模块
        class PlaceholderChatForm:
            def __init__(self):
                self.app = QtWidgets.QApplication.instance()
                if not self.app:
                    self.app = QtWidgets.QApplication(sys.argv)
                
            def show(self):
                QMessageBox.critical(None, "模块错误", f"找不到DC-Chat模块 {module_name}。\n请联系开发者获取帮助。")
                
        return type('PlaceholderModule', (), {'Ui_Form': PlaceholderChatForm})
    
    return None

def load_module_from_code(module_name, module_code):
    """从字符串代码加载模块"""
    log_message(f"从代码加载模块: {module_name}")
    
    try:
        # 创建一个新的模块对象
        module = types.ModuleType(module_name)
        
        # 将模块添加到sys.modules
        sys.modules[module_name] = module
        
        # 编译并执行代码
        exec(module_code, module.__dict__)
        
        log_message(f"成功从代码加载模块: {module_name}")
        return module
    except Exception as e:
        log_message(f"从代码加载模块失败: {module_name} - {e}")
        log_message(traceback.format_exc())
        return None

def load_module_from_file(module_name, file_path):
    """从文件加载模块（开发环境或提取的文件）"""
    log_message(f"从文件加载模块: {module_name} - {file_path}")
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            log_message(f"无法创建模块规范: {module_name} - {file_path}")
            return None
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        log_message(f"成功加载模块: {module_name}")
        return module
    except Exception as e:
        log_message(f"加载模块失败: {module_name} - {e}")
        log_message(traceback.format_exc())
        return None

def find_and_load_module(module_name):
    """查找并加载模块"""
    log_message(f"查找并加载模块: {module_name}")
    
    if is_frozen:
        # 在打包环境中，尝试从内部资源加载
        try:
            # 首先尝试直接导入（如果模块已经被包含在打包中）
            if module_name == "login":
                # 尝试导入login模块
                try:
                    import login
                    log_message(f"成功导入login模块")
                    return login
                except ImportError as e:
                    log_message(f"导入login模块失败: {e}")
                    # 尝试使用importlib导入
                    try:
                        import importlib
                        login = importlib.import_module("login")
                        log_message(f"使用importlib成功导入login模块")
                        return login
                    except ImportError as e2:
                        log_message(f"使用importlib导入login模块失败: {e2}")
                        
                        # 尝试从打包环境提取并加载模块文件
                        extracted_path = extract_module_file(module_name)
                        if extracted_path and os.path.exists(extracted_path):
                            return load_module_from_file(module_name, extracted_path)
                        
                        return create_placeholder_module("login")
            elif module_name == "dc-chat":
                try:
                    # 由于模块名包含连字符，无法直接导入，使用importlib
                    import importlib
                    dc_chat = importlib.import_module("dc-chat")
                    log_message(f"成功导入dc-chat模块")
                    return dc_chat
                except ImportError as e:
                    log_message(f"导入dc-chat模块失败: {e}")
                    
                    # 尝试使用连字符替换后的模块名
                    try:
                        dc_chat = importlib.import_module("dc_chat")
                        log_message(f"使用替换连字符后的名称导入dc_chat模块成功")
                        return dc_chat
                    except ImportError as e2:
                        log_message(f"使用替换连字符后的名称导入dc_chat模块失败: {e2}")
                    
                    # 尝试从打包环境提取并加载模块文件
                    extracted_path = extract_module_file(module_name)
                    if extracted_path and os.path.exists(extracted_path):
                        return load_module_from_file(module_name.replace('-', '_'), extracted_path)
                    
                    log_message(f"创建dc-chat占位符模块")
                    return create_placeholder_module("dc-chat")
            else:
                # 其他模块
                try:
                    module = __import__(module_name)
                    log_message(f"成功导入模块: {module_name}")
                    return module
                except Exception as e:
                    log_message(f"导入模块失败: {module_name} - {e}")
                    
                    # 尝试从打包环境提取并加载模块文件
                    extracted_path = extract_module_file(module_name)
                    if extracted_path and os.path.exists(extracted_path):
                        return load_module_from_file(module_name, extracted_path)
                    
                    # 创建占位符模块
                    return create_placeholder_module(module_name)
        except Exception as e:
            # 如果导入失败，尝试从打包文件数据中提取模块
            log_message(f"导入模块时发生异常: {module_name} - {e}")
            
            # 尝试从打包环境提取并加载模块文件
            extracted_path = extract_module_file(module_name)
            if extracted_path and os.path.exists(extracted_path):
                return load_module_from_file(module_name, extracted_path)
            
            # 如果提取失败，创建一个占位符模块
            log_message(f"创建占位符模块: {module_name}")
            return create_placeholder_module(module_name)
    else:
        # 在开发环境中，从文件加载
        file_path = os.path.join(main_path, f"{module_name}.py")
        if os.path.exists(file_path):
            return load_module_from_file(module_name, file_path)
        
        # 如果文件不存在，尝试查找备份文件
        backup_path = file_path + ".bak"
        if os.path.exists(backup_path):
            # 复制备份文件
            try:
                shutil.copy2(backup_path, file_path)
                log_message(f"已复制备份文件: {backup_path} -> {file_path}")
                return load_module_from_file(module_name, file_path)
            except Exception as e:
                log_message(f"复制备份文件失败: {e}")
        
        # 如果仍然找不到，创建占位符模块
        log_message(f"找不到模块文件，创建占位符: {module_name}")
        return create_placeholder_module(module_name)

def main():
    """应用程序主函数"""
    try:
        log_message("开始执行主函数...")
        
        # 加载登录模块（无论是打包环境还是开发环境）
        login_module = find_and_load_module("login")
        if login_module is None:
            error_msg = "无法加载登录模块，请查看日志文件了解详情。\n日志文件位置: " + log_file
            show_error("模块错误", error_msg)
            sys.exit(1)
        
        # 获取登录表单类
        try:
            LoginForm = login_module.Ui_LoginForm
            log_message("成功获取登录表单类")
        except AttributeError:
            error_msg = "登录模块缺少必要的类: Ui_LoginForm"
            log_message(error_msg)
            show_error("模块错误", error_msg + "\n请查看日志文件了解详情。\n日志文件位置: " + log_file)
            sys.exit(1)
        
        # 创建应用程序和登录窗口
        log_message("创建应用程序和登录窗口...")
        app = QtWidgets.QApplication(sys.argv)
        ui = LoginForm()
        ui.show()
        log_message("应用程序启动成功，显示登录窗口")
        sys.exit(app.exec())
    
    except Exception as e:
        error_msg = f"应用程序启动失败: {e}"
        log_message(error_msg)
        log_message(traceback.format_exc())
        show_error("启动错误", error_msg + "\n请查看日志文件了解详情。\n日志文件位置: " + log_file)
        sys.exit(1)

if __name__ == "__main__":
    main() 