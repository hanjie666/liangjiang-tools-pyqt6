#!/bin/bash
echo "正在为macOS打包良匠工具箱 (使用py2app)..."

# 安装必要的依赖
echo "安装依赖..."
pip install PyQt6 pymysql requests py2app Pillow

# 清理之前的构建
echo "清理之前的构建..."
rm -rf build dist

# 运行路径修复工具
echo "运行路径修复工具..."
python fix_paths.py

# 创建调试版本
echo "创建调试版本..."
python setup.py py2app --alias

# 如果调试版本成功，创建发布版本
if [ $? -eq 0 ]; then
    echo "调试版本创建成功，正在创建发布版本..."
    rm -rf build dist
    
    # 修改setup.py中的优化级别，可能有助于减少问题
    echo "调整优化级别..."
    sed -i '' 's/'\''optimize'\'': 2/'\''optimize'\'': 1/g' setup.py || echo "无法调整优化级别，继续使用默认设置"
    
    # 构建发布版本
    echo "构建发布版本..."
    python setup.py py2app
    
    # 检查是否成功
    if [ $? -eq 0 ]; then
        echo "打包成功！应用程序位于: dist/良匠工具箱.app"
        
        # 确保应用程序有执行权限
        echo "设置执行权限..."
        chmod -R 755 dist/良匠工具箱.app
        
        # 移除应用程序的隔离属性
        echo "移除应用程序的隔离属性..."
        xattr -d com.apple.quarantine dist/良匠工具箱.app 2>/dev/null || echo "无需移除隔离属性"
        
        # 尝试使用ad-hoc签名
        echo "尝试进行ad-hoc签名..."
        codesign --force --deep --sign - dist/良匠工具箱.app 2>/dev/null || echo "ad-hoc签名失败，这是正常的"
        
        # 验证应用程序结构
        echo "验证应用程序结构..."
        if [ -f "dist/良匠工具箱.app/Contents/MacOS/良匠工具箱" ]; then
            echo "应用程序结构正确"
            
            # 检查可执行文件是否有执行权限
            if [ -x "dist/良匠工具箱.app/Contents/MacOS/良匠工具箱" ]; then
                echo "可执行文件权限正确"
            else
                echo "设置可执行文件权限..."
                chmod +x "dist/良匠工具箱.app/Contents/MacOS/良匠工具箱"
            fi
            
            # 检查Python库是否存在
            if [ -d "dist/良匠工具箱.app/Contents/Resources/lib/python3.11" ]; then
                echo "Python库存在"
            else
                echo "警告: Python库可能不完整，应用程序可能无法正常运行"
            fi
        else
            echo "警告: 应用程序结构可能不正确"
        fi
        
        # 创建分发压缩包
        echo "创建分发压缩包..."
        cd dist
        zip -r "../良匠工具箱-macOS.zip" "良匠工具箱.app"
        cd ..
        
        echo "完成！您可以在当前目录找到 良匠工具箱-macOS.zip 文件"
        echo ""
        echo "注意：首次运行应用程序时，请右键点击应用程序图标，选择'打开'，然后在弹出的对话框中再次点击'打开'。"
        echo "这样可以绕过macOS的安全限制。"
        echo ""
        echo "如果应用程序仍然无法运行，请尝试在终端中执行以下命令查看错误信息："
        echo "  /Applications/良匠工具箱.app/Contents/MacOS/良匠工具箱"
    else
        echo "发布版本创建失败，请检查错误信息"
    fi
else
    echo "调试版本创建失败，请检查错误信息"
fi

echo "按回车键退出..."
read 