#!/bin/bash
# 良匠工具箱 - 应用程序修复工具
# 这个脚本用于修复已安装应用程序的权限和隔离属性

# 默认应用程序路径
APP_PATH="/Applications/良匠工具箱.app"

# 如果提供了参数，使用参数作为应用程序路径
if [ "$1" != "" ]; then
    APP_PATH="$1"
fi

echo "===== 良匠工具箱应用程序修复工具 ====="
echo "使用应用程序路径: $APP_PATH"

# 检查应用程序是否存在
if [ ! -d "$APP_PATH" ]; then
    echo "错误: 应用程序不存在: $APP_PATH"
    echo "请确保应用程序已安装，或提供正确的路径作为参数"
    exit 1
fi

# 修复权限
echo "修复权限..."
chmod -R 755 "$APP_PATH"
if [ $? -eq 0 ]; then
    echo "权限修复成功"
else
    echo "权限修复失败，可能需要管理员权限"
    echo "尝试使用sudo运行..."
    sudo chmod -R 755 "$APP_PATH"
    if [ $? -eq 0 ]; then
        echo "权限修复成功"
    else
        echo "权限修复失败"
    fi
fi

# 修复可执行文件权限
EXECUTABLE="$APP_PATH/Contents/MacOS/良匠工具箱"
if [ -f "$EXECUTABLE" ]; then
    echo "修复可执行文件权限..."
    chmod +x "$EXECUTABLE"
    if [ $? -eq 0 ]; then
        echo "可执行文件权限修复成功"
    else
        echo "可执行文件权限修复失败，尝试使用sudo..."
        sudo chmod +x "$EXECUTABLE"
    fi
else
    echo "警告: 可执行文件不存在: $EXECUTABLE"
fi

# 移除隔离属性
echo "移除隔离属性..."
xattr -d com.apple.quarantine "$APP_PATH" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "隔离属性移除成功"
else
    echo "隔离属性移除失败或不存在，尝试使用sudo..."
    sudo xattr -d com.apple.quarantine "$APP_PATH" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "隔离属性移除成功"
    else
        echo "隔离属性移除失败或不存在"
    fi
fi

# 尝试进行ad-hoc签名
echo "尝试进行ad-hoc签名..."
codesign --force --deep --sign - "$APP_PATH" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "ad-hoc签名成功"
else
    echo "ad-hoc签名失败，尝试使用sudo..."
    sudo codesign --force --deep --sign - "$APP_PATH" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "ad-hoc签名成功"
    else
        echo "ad-hoc签名失败，但这可能不影响应用程序运行"
    fi
fi

echo ""
echo "修复完成！现在您可以尝试运行应用程序了。"
echo "如果应用程序仍然无法运行，请尝试以下步骤："
echo "1. 右键点击应用程序图标，选择'打开'"
echo "2. 在弹出的对话框中点击'打开'"
echo ""
echo "或者在终端中运行以下命令查看错误信息："
echo "$EXECUTABLE"
echo "" 