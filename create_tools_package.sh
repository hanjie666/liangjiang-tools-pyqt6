#!/bin/bash
# 创建工具包压缩文件

echo "创建良匠工具箱工具包..."

# 创建临时目录
TEMP_DIR="tools_package"
mkdir -p "$TEMP_DIR"

# 复制工具文件
cp fix_app.sh "$TEMP_DIR/"
cp debug_app.py "$TEMP_DIR/"
cp macOS安装说明.md "$TEMP_DIR/README.md"

# 创建压缩包
zip -r "良匠工具箱-工具包.zip" "$TEMP_DIR"

# 清理临时目录
rm -rf "$TEMP_DIR"

echo "工具包创建完成: 良匠工具箱-工具包.zip"
echo "请将此文件与应用程序一起分发给用户。" 