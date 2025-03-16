#!/usr/bin/env python3
"""
路径修复工具 - 修复login.py和dc-chat.py文件中的路径问题
"""
import os
import sys
import shutil

def fix_login_py():
    """修复login.py文件中的路径问题"""
    print("修复login.py文件中的路径问题...")
    
    # 获取login.py文件路径
    login_py_path = os.path.join('main', 'login.py')
    if not os.path.exists(login_py_path):
        print(f"错误: 找不到login.py文件: {login_py_path}")
        return False
    
    # 创建备份
    backup_path = login_py_path + '.bak'
    shutil.copy2(login_py_path, backup_path)
    print(f"已创建备份: {backup_path}")
    
    # 读取文件内容
    with open(login_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修改动态导入dc-chat.py的代码
    old_import_code = """# 动态导入 dc-chat.py 模块
current_dir = os.path.dirname(os.path.abspath(__file__))
dc_chat_path = os.path.join(current_dir, 'dc-chat.py')
spec = importlib.util.spec_from_file_location("dc_chat", dc_chat_path)
dc_chat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dc_chat)
DCChatForm = dc_chat.Ui_Form"""

    new_import_code = """# 动态导入 dc-chat.py 模块
current_dir = os.path.dirname(os.path.abspath(__file__))
dc_chat_path = os.path.join(current_dir, 'dc-chat.py')

# 如果文件不存在，尝试其他可能的路径
if not os.path.exists(dc_chat_path):
    # 如果是打包后的应用
    if getattr(sys, 'frozen', False):
        # 尝试从Resources目录加载
        if sys.platform == 'darwin':
            # macOS应用程序包
            executable_dir = os.path.dirname(sys.executable)
            if 'Contents/MacOS' in executable_dir:
                resources_dir = os.path.join(os.path.dirname(os.path.dirname(executable_dir)), 'Resources')
                dc_chat_path = os.path.join(resources_dir, 'main', 'dc-chat.py')
                print(f"尝试从Resources目录加载dc-chat.py: {dc_chat_path}")

# 如果仍然找不到文件，尝试在当前目录查找
if not os.path.exists(dc_chat_path):
    dc_chat_path = os.path.join(os.getcwd(), 'main', 'dc-chat.py')
    print(f"尝试从当前目录加载dc-chat.py: {dc_chat_path}")

# 如果仍然找不到文件，尝试相对路径
if not os.path.exists(dc_chat_path):
    dc_chat_path = 'main/dc-chat.py'
    print(f"尝试使用相对路径加载dc-chat.py: {dc_chat_path}")

print(f"使用dc-chat.py路径: {dc_chat_path}")
spec = importlib.util.spec_from_file_location("dc_chat", dc_chat_path)
dc_chat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dc_chat)
DCChatForm = dc_chat.Ui_Form"""

    # 替换导入代码
    content = content.replace(old_import_code, new_import_code)
    
    # 修改配置文件路径
    old_config_code = """# 配置文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(current_dir, 'config.json')"""
        
    new_config_code = """# 配置文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(current_dir, 'config.json')
        
        # 如果配置文件不存在，尝试其他可能的路径
        if not os.path.exists(self.config_file):
            # 如果是打包后的应用
            if getattr(sys, 'frozen', False):
                # 尝试从Resources目录加载
                if sys.platform == 'darwin':
                    # macOS应用程序包
                    executable_dir = os.path.dirname(sys.executable)
                    if 'Contents/MacOS' in executable_dir:
                        resources_dir = os.path.join(os.path.dirname(os.path.dirname(executable_dir)), 'Resources')
                        self.config_file = os.path.join(resources_dir, 'main', 'config.json')
                        print(f"尝试从Resources目录加载config.json: {self.config_file}")
        
        # 如果仍然找不到文件，使用当前目录
        if not os.path.exists(self.config_file):
            self.config_file = os.path.join(os.getcwd(), 'config.json')
            print(f"使用当前目录的config.json: {self.config_file}")"""
    
    # 替换配置文件代码
    content = content.replace(old_config_code, new_config_code)
    
    # 写入修改后的内容
    with open(login_py_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"login.py文件修复完成")
    return True

def fix_dc_chat_py():
    """修复dc-chat.py文件中的路径问题"""
    print("修复dc-chat.py文件中的路径问题...")
    
    # 获取dc-chat.py文件路径
    dc_chat_py_path = os.path.join('main', 'dc-chat.py')
    if not os.path.exists(dc_chat_py_path):
        print(f"错误: 找不到dc-chat.py文件: {dc_chat_py_path}")
        return False
    
    # 创建备份
    backup_path = dc_chat_py_path + '.bak'
    shutil.copy2(dc_chat_py_path, backup_path)
    print(f"已创建备份: {backup_path}")
    
    # 读取文件内容
    with open(dc_chat_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修改配置文件路径
    old_config_code = """# 配置文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(current_dir, 'dc_chat_config.json')"""
        
    new_config_code = """# 配置文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(current_dir, 'dc_chat_config.json')
        
        # 如果配置文件不存在，尝试其他可能的路径
        if not os.path.exists(self.config_file):
            # 如果是打包后的应用
            if getattr(sys, 'frozen', False):
                # 尝试从Resources目录加载
                if sys.platform == 'darwin':
                    # macOS应用程序包
                    executable_dir = os.path.dirname(sys.executable)
                    if 'Contents/MacOS' in executable_dir:
                        resources_dir = os.path.join(os.path.dirname(os.path.dirname(executable_dir)), 'Resources')
                        self.config_file = os.path.join(resources_dir, 'main', 'dc_chat_config.json')
                        print(f"尝试从Resources目录加载dc_chat_config.json: {self.config_file}")
        
        # 如果仍然找不到文件，使用当前目录
        if not os.path.exists(self.config_file):
            self.config_file = os.path.join(os.getcwd(), 'dc_chat_config.json')
            print(f"使用当前目录的dc_chat_config.json: {self.config_file}")"""
    
    # 替换配置文件代码
    content = content.replace(old_config_code, new_config_code)
    
    # 修改view.login导入
    if "from view.login import Ui_LoginForm" in content:
        old_import = "from view.login import Ui_LoginForm"
        new_import = """# 尝试动态导入login模块
try:
    import importlib.util
    
    # 尝试不同的可能路径
    login_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'login.py'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'main', 'login.py')
    ]
    
    # 如果是打包后的应用
    if getattr(sys, 'frozen', False):
        # 尝试从Resources目录加载
        if sys.platform == 'darwin':
            # macOS应用程序包
            executable_dir = os.path.dirname(sys.executable)
            if 'Contents/MacOS' in executable_dir:
                resources_dir = os.path.join(os.path.dirname(os.path.dirname(executable_dir)), 'Resources')
                login_paths.append(os.path.join(resources_dir, 'main', 'login.py'))
    
    # 尝试所有可能的路径
    login_path = None
    for path in login_paths:
        if os.path.exists(path):
            login_path = path
            print(f"找到login.py: {login_path}")
            break
    
    if login_path:
        spec = importlib.util.spec_from_file_location("login", login_path)
        login = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(login)
        Ui_LoginForm = login.Ui_LoginForm
    else:
        print("错误: 找不到login.py文件")
        raise ImportError("找不到login.py文件")
except Exception as e:
    print(f"导入login模块失败: {e}")
    raise"""
        
        content = content.replace(old_import, new_import)
    
    # 写入修改后的内容
    with open(dc_chat_py_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"dc-chat.py文件修复完成")
    return True

def main():
    """主函数"""
    print("=== 路径修复工具 ===")
    
    # 修复login.py文件
    fix_login_py()
    
    # 修复dc-chat.py文件
    fix_dc_chat_py()
    
    print("修复完成！请重新打包应用程序。")

if __name__ == "__main__":
    main() 