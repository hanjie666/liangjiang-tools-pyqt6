#!/usr/bin/env python3
"""
良匠工具箱 - 应用程序调试工具

这个脚本用于检查打包后的应用程序是否正确，并帮助诊断可能的问题。
"""
import os
import sys
import platform
import subprocess
import shutil
import tempfile
import datetime

# 设置日志文件
log_file = os.path.join(tempfile.gettempdir(), "liangjiang_tools_debug_check.log")

def write_log(message):
    """写入日志"""
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            f.write(f"{timestamp} {message}\n")
        print(message)
    except Exception as e:
        print(f"写入日志失败: {e}")

def check_app_bundle(app_path):
    """检查应用程序包结构"""
    write_log(f"检查应用程序包: {app_path}")
    
    if not os.path.exists(app_path):
        write_log(f"错误: 应用程序包不存在: {app_path}")
        return False
    
    # 检查基本结构
    contents_dir = os.path.join(app_path, "Contents")
    if not os.path.exists(contents_dir):
        write_log(f"错误: Contents 目录不存在")
        return False
    
    # 检查Info.plist
    info_plist = os.path.join(contents_dir, "Info.plist")
    if not os.path.exists(info_plist):
        write_log(f"错误: Info.plist 不存在")
        return False
    
    # 检查可执行文件
    macos_dir = os.path.join(contents_dir, "MacOS")
    if not os.path.exists(macos_dir):
        write_log(f"错误: MacOS 目录不存在")
        return False
    
    executable = os.path.join(macos_dir, "良匠工具箱")
    if not os.path.exists(executable):
        write_log(f"错误: 可执行文件不存在")
        return False
    
    if not os.access(executable, os.X_OK):
        write_log(f"错误: 可执行文件没有执行权限")
        return False
    
    # 检查资源目录
    resources_dir = os.path.join(contents_dir, "Resources")
    if not os.path.exists(resources_dir):
        write_log(f"错误: Resources 目录不存在")
        return False
    
    # 检查Python库
    python_lib = os.path.join(resources_dir, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}")
    if not os.path.exists(python_lib):
        write_log(f"警告: Python库目录不存在: {python_lib}")
        # 尝试查找其他Python版本
        lib_dir = os.path.join(resources_dir, "lib")
        if os.path.exists(lib_dir):
            python_dirs = [d for d in os.listdir(lib_dir) if d.startswith("python")]
            if python_dirs:
                write_log(f"找到其他Python版本: {python_dirs}")
            else:
                write_log(f"错误: 未找到任何Python库目录")
                return False
        else:
            write_log(f"错误: lib目录不存在")
            return False
    
    # 检查main目录
    main_dir = os.path.join(resources_dir, "main")
    if not os.path.exists(main_dir):
        write_log(f"错误: main目录不存在")
        return False
    
    # 检查login.py和dc-chat.py
    login_py = os.path.join(main_dir, "login.py")
    dc_chat_py = os.path.join(main_dir, "dc-chat.py")
    
    if not os.path.exists(login_py):
        write_log(f"错误: login.py不存在")
        return False
    
    if not os.path.exists(dc_chat_py):
        write_log(f"错误: dc-chat.py不存在")
        return False
    
    # 检查view目录
    view_dir = os.path.join(resources_dir, "view")
    if not os.path.exists(view_dir):
        write_log(f"错误: view目录不存在")
        return False
    
    # 检查UI文件
    ui_files = [f for f in os.listdir(view_dir) if f.endswith(".ui")]
    if not ui_files:
        write_log(f"错误: 未找到UI文件")
        return False
    
    write_log(f"应用程序包结构检查通过")
    return True

def check_dependencies():
    """检查系统依赖"""
    write_log(f"检查系统依赖...")
    
    # 检查Python版本
    write_log(f"Python版本: {sys.version}")
    
    # 检查操作系统
    write_log(f"操作系统: {platform.platform()}")
    
    # 检查PyQt6
    try:
        import PyQt6
        write_log(f"PyQt6版本: {PyQt6.QtCore.PYQT_VERSION_STR}")
    except ImportError:
        write_log(f"错误: 未安装PyQt6")
        return False
    
    # 检查pymysql
    try:
        import pymysql
        write_log(f"pymysql版本: {pymysql.__version__}")
    except ImportError:
        write_log(f"错误: 未安装pymysql")
        return False
    
    # 检查requests
    try:
        import requests
        write_log(f"requests版本: {requests.__version__}")
    except ImportError:
        write_log(f"错误: 未安装requests")
        return False
    
    write_log(f"系统依赖检查通过")
    return True

def run_app_in_terminal(app_path):
    """在终端中运行应用程序"""
    write_log(f"尝试在终端中运行应用程序...")
    
    executable = os.path.join(app_path, "Contents", "MacOS", "良匠工具箱")
    if not os.path.exists(executable):
        write_log(f"错误: 可执行文件不存在: {executable}")
        return False
    
    try:
        write_log(f"运行命令: {executable}")
        process = subprocess.Popen(executable, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=5)
        
        if stdout:
            write_log(f"标准输出:\n{stdout.decode('utf-8', errors='ignore')}")
        
        if stderr:
            write_log(f"错误输出:\n{stderr.decode('utf-8', errors='ignore')}")
        
        write_log(f"应用程序退出代码: {process.returncode}")
        
        if process.returncode != 0:
            write_log(f"警告: 应用程序异常退出")
            return False
        
        write_log(f"应用程序启动成功")
        return True
    except subprocess.TimeoutExpired:
        write_log(f"应用程序启动超时，这可能是正常的（如果应用程序已经显示界面）")
        return True
    except Exception as e:
        write_log(f"运行应用程序时出错: {e}")
        return False

def check_code_signature(app_path):
    """检查代码签名"""
    write_log(f"检查代码签名...")
    
    try:
        result = subprocess.run(["codesign", "-vv", "-d", app_path], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            write_log(f"代码签名信息:\n{result.stdout.decode('utf-8', errors='ignore')}")
            write_log(f"应用程序已签名")
        else:
            write_log(f"应用程序未签名或签名无效:\n{result.stderr.decode('utf-8', errors='ignore')}")
            
            # 尝试进行ad-hoc签名
            write_log(f"尝试进行ad-hoc签名...")
            sign_result = subprocess.run(["codesign", "--force", "--deep", "--sign", "-", app_path],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if sign_result.returncode == 0:
                write_log(f"ad-hoc签名成功")
            else:
                write_log(f"ad-hoc签名失败:\n{sign_result.stderr.decode('utf-8', errors='ignore')}")
                return False
        
        return True
    except Exception as e:
        write_log(f"检查代码签名时出错: {e}")
        return False

def fix_quarantine(app_path):
    """修复隔离属性"""
    write_log(f"检查隔离属性...")
    
    try:
        result = subprocess.run(["xattr", "-l", app_path], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        output = result.stdout.decode('utf-8', errors='ignore')
        if "com.apple.quarantine" in output:
            write_log(f"应用程序有隔离属性，尝试移除...")
            
            remove_result = subprocess.run(["xattr", "-d", "com.apple.quarantine", app_path],
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if remove_result.returncode == 0:
                write_log(f"隔离属性移除成功")
            else:
                write_log(f"隔离属性移除失败:\n{remove_result.stderr.decode('utf-8', errors='ignore')}")
                return False
        else:
            write_log(f"应用程序没有隔离属性")
        
        return True
    except Exception as e:
        write_log(f"检查隔离属性时出错: {e}")
        return False

def main():
    """主函数"""
    write_log("=== 良匠工具箱应用程序调试工具 ===")
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        app_path = sys.argv[1]
    else:
        # 默认路径
        app_path = "dist/良匠工具箱.app"
        if not os.path.exists(app_path):
            app_path = "/Applications/良匠工具箱.app"
    
    write_log(f"使用应用程序路径: {app_path}")
    
    # 检查系统依赖
    if not check_dependencies():
        write_log("系统依赖检查失败，请安装缺少的依赖")
        return
    
    # 检查应用程序包结构
    if not check_app_bundle(app_path):
        write_log("应用程序包结构检查失败，请重新打包")
        return
    
    # 检查代码签名
    if not check_code_signature(app_path):
        write_log("代码签名检查失败，但这可能不影响应用程序运行")
    
    # 修复隔离属性
    if not fix_quarantine(app_path):
        write_log("修复隔离属性失败，但这可能不影响应用程序运行")
    
    # 在终端中运行应用程序
    if not run_app_in_terminal(app_path):
        write_log("应用程序运行测试失败")
    
    write_log(f"调试完成，日志文件位置: {log_file}")
    write_log("如果应用程序仍然无法运行，请查看日志文件获取更多信息")

if __name__ == "__main__":
    main() 