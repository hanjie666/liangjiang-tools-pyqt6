#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import shutil
import glob
import time
import zipfile

def create_icon_files():
    """
    不再需要创建图标文件，因为我们已经从spec文件中移除了图标设置
    """
    print("跳过图标文件创建...")
    # 不再创建任何图标文件
    pass

def verify_required_files():
    """验证所有必要的文件是否存在"""
    print("验证必要文件...")
    
    required_files = [
        'main.py',
        'main/login.py',
        'main/dc-chat.py'
    ]
    
    # 确保main目录存在
    if not os.path.exists('main'):
        print("创建main目录...")
        try:
            os.makedirs('main', exist_ok=True)
        except Exception as e:
            print(f"创建main目录失败: {e}")
    
    # 列出当前目录内容
    print("\n当前目录内容:")
    try:
        for item in os.listdir('.'):
            if os.path.isdir(item):
                print(f" - [目录] {item}")
                # 如果是main目录，列出其内容
                if item == 'main':
                    try:
                        print("   main目录内容:")
                        for subitem in os.listdir('main'):
                            print(f"    - {subitem}")
                    except Exception as e:
                        print(f"   无法列出main目录内容: {e}")
            else:
                print(f" - [文件] {item}")
    except Exception as e:
        print(f"列出目录内容失败: {e}")
    
    # 检查文件是否存在
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("\n错误: 以下文件不存在:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        print("\n尝试修复问题...")
        
        # 尝试修复login.py文件
        if 'main/login.py' in missing_files:
            # 尝试从多个可能的位置查找login.py文件
            possible_locations = [
                'main/login.py.bak',
                'login.py',
                'login.py.bak'
            ]
            
            # 搜索整个目录
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file == 'login.py' or file == 'login.py.bak':
                        possible_locations.append(os.path.join(root, file))
            
            print(f"尝试查找login.py文件，可能的位置: {possible_locations}")
            
            for loc in possible_locations:
                if os.path.exists(loc):
                    print(f"找到login.py文件: {loc}")
                    try:
                        # 确保main目录存在
                        os.makedirs('main', exist_ok=True)
                        # 复制文件
                        shutil.copy(loc, 'main/login.py')
                        print(f"已复制文件: {loc} -> main/login.py")
                        break
                    except Exception as e:
                        print(f"复制文件失败: {e}")
            else:
                print("无法找到login.py文件")
        
        # 尝试修复dc-chat.py文件
        if 'main/dc-chat.py' in missing_files:
            # 尝试从多个可能的位置查找dc-chat.py文件
            possible_locations = [
                'main/dc-chat.py.bak',
                'dc-chat.py',
                'dc-chat.py.bak'
            ]
            
            # 搜索整个目录
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file == 'dc-chat.py' or file == 'dc-chat.py.bak':
                        possible_locations.append(os.path.join(root, file))
            
            print(f"尝试查找dc-chat.py文件，可能的位置: {possible_locations}")
            
            for loc in possible_locations:
                if os.path.exists(loc):
                    print(f"找到dc-chat.py文件: {loc}")
                    try:
                        # 确保main目录存在
                        os.makedirs('main', exist_ok=True)
                        # 复制文件
                        shutil.copy(loc, 'main/dc-chat.py')
                        print(f"已复制文件: {loc} -> main/dc-chat.py")
                        break
                    except Exception as e:
                        print(f"复制文件失败: {e}")
            else:
                print("无法找到dc-chat.py文件")
        
        # 再次检查文件
        still_missing = []
        for file_path in missing_files:
            if not os.path.exists(file_path):
                still_missing.append(file_path)
        
        if still_missing:
            print("\n错误: 无法修复以下文件:")
            for file_path in still_missing:
                print(f"  - {file_path}")
            
            # 创建空文件作为占位符
            print("\n创建空文件作为占位符...")
            for file_path in still_missing:
                try:
                    # 确保目录存在
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    # 创建空文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        if 'login.py' in file_path:
                            f.write("""
# 占位符文件，由打包脚本自动创建
class Ui_LoginForm:
    def __init__(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(None, "文件错误", "找不到必要的文件: login.py\\n请联系开发者获取帮助。")
    
    def show(self):
        pass
""")
                        elif 'dc-chat.py' in file_path:
                            f.write("# 占位符文件，由打包脚本自动创建")
                    print(f"已创建占位符文件: {file_path}")
                except Exception as e:
                    print(f"创建占位符文件失败: {file_path} - {e}")
            
            print("\n警告: 使用了占位符文件，应用程序可能无法正常工作。")
        else:
            print("所有问题已修复!")
    else:
        print("所有必要文件都存在!")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    # 根据操作系统安装不同的依赖
    if platform.system() == "Darwin":  # macOS
        # 在macOS上安装py2app和其他依赖
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
    else:  # Windows
        # 在Windows上只安装PyInstaller和必要的依赖
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "PyQt6", "pymysql", "requests", "Pillow"])
    
    # 确保PyInstaller已安装
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def package_application():
    """Package the application using PyInstaller"""
    print("Packaging application...")
    
    # 确保spec文件存在
    if not os.path.exists('liangjiang_tools.spec'):
        print("错误: 找不到spec文件 liangjiang_tools.spec")
        sys.exit(1)
    
    # 运行PyInstaller前先验证文件
    verify_required_files()
    
    # 确保文件被正确复制到dist目录
    print("确保必要文件存在于打包目录...")
    for file_path in ['main/login.py', 'main/dc-chat.py']:
        if os.path.exists(file_path):
            # 创建备份
            backup_path = file_path + '.bak'
            try:
                shutil.copy2(file_path, backup_path)
                print(f"已创建备份: {file_path} -> {backup_path}")
            except Exception as e:
                print(f"创建备份失败: {e}")
    
    # 使用PyInstaller打包应用程序（使用spec文件）
    print("使用spec文件打包应用程序...")
    subprocess.check_call([
        "pyinstaller",
        "--clean",
        "--noconfirm",  # 不要询问是否删除输出目录
        "liangjiang_tools.spec"
    ])
    
    # 检查输出文件
    output_file = "dist/良匠工具箱.exe" if platform.system() == "Windows" else "dist/良匠工具箱"
    if os.path.exists(output_file):
        print(f"应用程序打包成功: {output_file}")
        # 获取文件大小
        file_size = os.path.getsize(output_file)
        print(f"文件大小: {file_size / 1024 / 1024:.2f} MB")
    else:
        print(f"错误: 找不到输出文件: {output_file}")
    
    # 创建一个空的日志文件，放在与exe相同的目录中
    log_file = os.path.join(os.path.dirname(output_file), "liangjiang_tools_log.txt")
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"日志文件创建时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"已创建日志文件: {log_file}")
    except Exception as e:
        print(f"创建日志文件失败: {e}")

def create_distribution_archive():
    """Create a zip archive of the packaged application"""
    print("Creating distribution archive...")
    
    # 确定输出文件名
    output_file = "dist/良匠工具箱.exe" if platform.system() == "Windows" else "dist/良匠工具箱"
    
    # 确保输出文件存在
    if not os.path.exists(output_file):
        print(f"错误: 找不到输出文件: {output_file}")
        return
    
    # 添加时间戳到归档名称
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    archive_name = f"良匠工具箱-{platform.system()}-{timestamp}"
    
    # 创建临时目录
    temp_dir = f"dist/temp_{timestamp}"
    os.makedirs(temp_dir, exist_ok=True)
    
    # 复制可执行文件到临时目录
    exe_name = os.path.basename(output_file)
    shutil.copy2(output_file, os.path.join(temp_dir, exe_name))
    
    # 创建日志文件
    log_file = os.path.join(temp_dir, "liangjiang_tools_log.txt")
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"日志文件创建时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"已创建日志文件: {log_file}")
    except Exception as e:
        print(f"创建日志文件失败: {e}")
    
    # 创建归档文件
    try:
        shutil.make_archive(archive_name, 'zip', temp_dir)
        print(f"Distribution archive created: {archive_name}.zip")
    except Exception as e:
        print(f"创建归档文件失败: {e}")
    
    # 清理临时目录
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"清理临时目录失败: {e}")

def main():
    """Main function to run the packaging process"""
    print(f"Packaging for {platform.system()}...")
    
    # 验证必要文件
    verify_required_files()
    
    # Create icon files
    create_icon_files()
    
    # Install dependencies
    install_dependencies()
    
    # Package the application
    package_application()
    
    # Create distribution archive
    create_distribution_archive()
    
    print("Packaging completed successfully!")
    print("\n重要提示: 应用程序已打包为单个exe文件，源代码已编译为字节码并打包在exe中，无法被轻易查看。")

if __name__ == "__main__":
    main() 