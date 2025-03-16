# 良匠工具箱 (Liangjiang Tools)

这是一个基于PyQt6的Discord自动聊天工具，支持Windows和macOS平台。

## 功能特点

- 登录验证系统，使用卡密进行身份验证
- Discord自动聊天功能，支持AI生成回复
- 可配置的回复延时和语言选择
- 自动保存配置信息

## 打包说明

### 环境要求

- Python 3.6+
- pip (Python包管理器)

### 安装依赖

```bash
# 安装项目依赖
pip install -e .

# 安装打包工具
pip install pyinstaller
```

### 打包应用

#### 自动打包（推荐）

使用提供的打包脚本可以自动完成打包过程：

```bash
python package.py
```

脚本会自动安装依赖、创建图标文件（空文件）、打包应用并创建分发压缩包。

#### 手动打包

如果需要手动打包，可以按照以下步骤操作：

1. 创建图标文件（可选）：
   - Windows: 创建 `app_icon.ico` 文件
   - macOS: 创建 `app_icon.icns` 文件

2. 使用PyInstaller打包：

```bash
pyinstaller --clean liangjiang_tools.spec
```

### 打包输出

打包完成后，将在 `dist` 目录下生成以下文件：

- Windows: `dist/良匠工具箱` 目录
- macOS: `dist/良匠工具箱.app` 应用程序包

同时，脚本会创建一个压缩包：

- Windows: `良匠工具箱-Windows.zip`
- macOS: `良匠工具箱-macOS.zip`

## 使用说明

1. 启动应用程序
2. 在登录界面输入有效的卡密
3. 登录成功后，配置Discord Token、频道ID和API Key
4. 设置回复延时和语言
5. 点击"开始"按钮启动自动聊天功能

## 注意事项

- 请确保您的Discord Token和API Key有效
- 请合理设置回复延时，避免触发Discord的频率限制
- 应用程序会自动保存您的配置信息，下次启动时自动加载

## 开发者信息

如需修改或扩展功能，请参考以下文件：

- `main/login.py`: 登录界面和验证逻辑
- `main/dc-chat.py`: Discord自动聊天功能
- `view/*.ui`: UI设计文件 