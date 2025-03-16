#!/usr/bin/env python3
"""
开发模式运行脚本
这个脚本用于在开发环境中运行应用程序，方便调试和测试。
"""
import os
import sys
import subprocess

def setup_environment():
    """设置开发环境"""
    print("正在设置开发环境...")
    
    # 安装依赖
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("依赖安装成功")
    except subprocess.CalledProcessError:
        print("警告: 依赖安装失败，可能会影响应用程序运行")

def run_application():
    """运行应用程序"""
    print("正在启动应用程序...")
    
    # 导入并运行主程序
    try:
        import main
        main.main()
    except ImportError as e:
        print(f"错误: 无法导入主模块: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 应用程序运行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # 设置开发环境
    setup_environment()
    
    # 运行应用程序
    run_application() 