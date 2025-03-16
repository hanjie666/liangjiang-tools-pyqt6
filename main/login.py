# Form implementation generated from reading ui file 'view/login.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
import os
import importlib.util
import json
import pymysql
from datetime import datetime

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor

class Ui_LoginForm(QWidget):
    def __init__(self):
        super(Ui_LoginForm, self).__init__()
        self.setupUi(self)
        
        # 设置窗口标题
        self.setWindowTitle("良匠工具箱 - 登录")
        
        # 设置窗口图标（如果存在）
        self.set_window_icon()
        
        # 根据平台调整样式
        self.adjust_platform_style()
        
        # 居中显示窗口
        self.center_on_screen()
        
        # MySQL 数据库配置
        self.db_config = {
            'host': '43.134.117.111',
            'user': 'root',
            'port': 3306,
            'password': 'Chjwudi008...',  # 请修改为您的 MySQL 密码
            'database': 'dc_chat_app',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        
        # 初始化数据库
        try:
            self.init_database()
        except Exception as e:
            print(f"数据库初始化失败，将使用本地模式: {e}")
            # 数据库连接失败时不阻止应用程序启动
        
        # 连接登录按钮的点击事件
        self.loginButton.clicked.connect(self.login)
        
        # 创建 DC-Chat 窗口实例但不显示
        self.dc_chat_window = None
        
        # 配置文件路径
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
            print(f"使用当前目录的config.json: {self.config_file}")
        
        # 检查是否有保存的卡密
        self.check_saved_password()
    
    def set_window_icon(self):
        """设置窗口图标"""
        # 尝试查找图标文件
        icon_paths = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app_icon.png'),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app_icon.ico'),
            'app_icon.png',
            'app_icon.ico'
        ]
        
        # 如果是打包后的应用
        if getattr(sys, 'frozen', False):
            if sys.platform == 'darwin':
                # macOS应用程序包
                executable_dir = os.path.dirname(sys.executable)
                if 'Contents/MacOS' in executable_dir:
                    resources_dir = os.path.join(os.path.dirname(os.path.dirname(executable_dir)), 'Resources')
                    icon_paths.append(os.path.join(resources_dir, 'app_icon.png'))
                    icon_paths.append(os.path.join(resources_dir, 'app_icon.icns'))
        
        # 尝试设置图标
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
                break
    
    def center_on_screen(self):
        """将窗口居中显示在屏幕上"""
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)
    
    def adjust_platform_style(self):
        """根据平台调整样式，使其在不同平台上保持一致"""
        # 设置窗口固定大小
        if sys.platform == 'darwin':  # macOS
            self.setFixedSize(480, 200)
        else:  # Windows 和其他平台
            self.setFixedSize(450, 180)
        
        # 设置应用程序样式表
        style_sheet = """
        QWidget {
            font-family: 'Microsoft YaHei', 'Segoe UI', 'Helvetica', sans-serif;
            font-size: 10pt;
            color: #333333;
            background-color: #f5f5f7;
        }
        
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            min-width: 80px;
        }
        
        QPushButton:hover {
            background-color: #45a049;
        }
        
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        
        QLineEdit {
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 8px;
            background-color: white;
            selection-background-color: #4CAF50;
            selection-color: white;
        }
        
        QLineEdit:focus {
            border: 1px solid #4CAF50;
            box-shadow: 0 0 3px #4CAF50;
        }
        
        QLabel {
            color: #333333;
        }
        
        QLabel#titleLabel {
            font-weight: bold;
            color: #2c3e50;
        }
        
        QFrame#headerFrame {
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
        }
        
        QFrame#contentFrame {
            background-color: #ffffff;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        """
        
        # 根据不同平台进行微调
        if sys.platform == 'darwin':  # macOS
            # 在macOS上增加字体大小和控件大小
            style_sheet += """
            QWidget {
                font-size: 13pt;
            }
            
            QPushButton {
                min-height: 32px;
                font-size: 13pt;
            }
            
            QLineEdit {
                min-height: 28px;
                font-size: 13pt;
            }
            
            QLabel#titleLabel {
                font-size: 24pt;
            }
            """
        elif sys.platform == 'win32':  # Windows
            # 在Windows上使用更适合Windows的字体和控件大小
            style_sheet += """
            QWidget {
                font-family: 'Microsoft YaHei UI', 'Segoe UI', sans-serif;
                font-size: 10pt;
            }
            
            QPushButton {
                min-height: 28px;
            }
            
            QLineEdit {
                min-height: 24px;
            }
            
            QLabel#titleLabel {
                font-size: 22pt;
                font-family: 'Segoe UI Light', 'Microsoft YaHei UI Light', sans-serif;
            }
            """
        
        # 应用样式表
        self.setStyleSheet(style_sheet)

    def setupUi(self, LoginForm):
        # 创建主布局
        self.mainLayout = QVBoxLayout(LoginForm)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        
        # 创建标题区域
        self.headerFrame = QFrame(LoginForm)
        self.headerFrame.setObjectName("headerFrame")
        self.headerFrame.setMinimumHeight(60)
        self.headerLayout = QVBoxLayout(self.headerFrame)
        self.headerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 标题标签
        self.titleLabel = QtWidgets.QLabel("良匠工具箱", self.headerFrame)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 设置标题字体
        titleFont = QFont()
        if sys.platform == 'darwin':
            titleFont.setFamily("Helvetica Neue")
        else:
            titleFont.setFamily("Segoe UI Light")
        titleFont.setPointSize(24)
        self.titleLabel.setFont(titleFont)
        
        self.headerLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.headerFrame)
        
        # 创建内容区域
        self.contentFrame = QFrame(LoginForm)
        self.contentFrame.setObjectName("contentFrame")
        self.contentLayout = QVBoxLayout(self.contentFrame)
        self.contentLayout.setContentsMargins(20, 20, 20, 20)
        
        # 创建表单布局
        self.formLayout = QGridLayout()
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(10)
        
        # 卡密标签和输入框
        self.codeLabel = QtWidgets.QLabel("请输入卡密：", self.contentFrame)
        self.CodeLineEdit = QtWidgets.QLineEdit(self.contentFrame)
        self.CodeLineEdit.setPlaceholderText("输入卡密进行登录")
        self.CodeLineEdit.setClearButtonEnabled(True)
        
        # 登录按钮
        self.loginButton = QtWidgets.QPushButton("登录", self.contentFrame)
        
        # 添加到表单布局
        self.formLayout.addWidget(self.codeLabel, 0, 0)
        self.formLayout.addWidget(self.CodeLineEdit, 0, 1)
        self.formLayout.addWidget(self.loginButton, 0, 2)
        
        # 设置列的拉伸因子
        self.formLayout.setColumnStretch(0, 1)  # 标签列
        self.formLayout.setColumnStretch(1, 3)  # 输入框列
        self.formLayout.setColumnStretch(2, 1)  # 按钮列
        
        # 添加表单布局到内容布局
        self.contentLayout.addLayout(self.formLayout)
        
        # 添加内容区域到主布局
        self.mainLayout.addWidget(self.contentFrame)
        self.mainLayout.setStretch(0, 1)  # 标题区域
        self.mainLayout.setStretch(1, 2)  # 内容区域
        
        # 设置回车键触发登录
        self.CodeLineEdit.returnPressed.connect(self.login)
        
        # 设置对象名称
        LoginForm.setObjectName("LoginForm")
        self.CodeLineEdit.setObjectName("CodeLineEdit")
        self.loginButton.setObjectName("loginButton")
        self.codeLabel.setObjectName("codeLabel")

    def retranslateUi(self, LoginForm):
        _translate = QtCore.QCoreApplication.translate
        LoginForm.setWindowTitle(_translate("LoginForm", "良匠工具箱 - 登录"))
        self.codeLabel.setText(_translate("LoginForm", "请输入卡密："))
        self.titleLabel.setText(_translate("LoginForm", "良匠工具箱"))
        self.loginButton.setText(_translate("LoginForm", "登录"))

    def get_db_connection(self):
        """获取数据库连接"""
        try:
            conn = pymysql.connect(**self.db_config)
            return conn
        except pymysql.Error as e:
            print(f"数据库连接错误: {e}")
            return None

    def init_database(self):
        """初始化数据库，创建表并插入测试数据"""
        try:
            # 尝试连接到 MySQL 服务器（不指定数据库）
            conn = pymysql.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                charset='utf8mb4',
                connect_timeout=5  # 添加连接超时
            )
            
            with conn.cursor() as cursor:
                # 创建数据库（如果不存在）
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
            
            conn.close()
            
            # 连接到指定的数据库
            conn = self.get_db_connection()
            if not conn:
                print("无法连接到数据库")
                return
                
            with conn.cursor() as cursor:
                # 创建卡密表
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS activation_codes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    code VARCHAR(255) NOT NULL UNIQUE,
                    is_active TINYINT NOT NULL DEFAULT 1,
                    expiry_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                
                # 检查是否已有测试数据
                cursor.execute("SELECT COUNT(*) as count FROM activation_codes")
                result = cursor.fetchone()
                count = result['count']
                
                # 如果没有数据，插入测试数据
                if count == 0:
                    cursor.execute('''
                    INSERT INTO activation_codes (code, is_active, expiry_date) VALUES 
                    ('hanjie', 1, '2023-12-31'),
                    ('test123', 1, '2023-06-01'),
                    ('inactive', 0, '2023-12-31')
                    ''')
            
            conn.commit()
            conn.close()
            print("数据库初始化成功")
        except Exception as e:
            print(f"初始化数据库出错: {e}")
            raise
    
    def validate_code(self, code):
        """验证卡密是否有效"""
        # 开发环境中的测试卡密
        test_codes = {
            'test': {'is_active': 1, 'expiry_date': '2099-12-31'},
            'hanjie': {'is_active': 1, 'expiry_date': '2099-12-31'},
            'admin': {'is_active': 1, 'expiry_date': '2099-12-31'},
            'inactive': {'is_active': 0, 'expiry_date': '2099-12-31'},
            'expired': {'is_active': 1, 'expiry_date': '2020-01-01'}
        }
        
        try:
            # 首先尝试使用本地测试卡密
            if code in test_codes:
                test_code = test_codes[code]
                is_active = test_code['is_active']
                expiry_date = datetime.strptime(test_code['expiry_date'], '%Y-%m-%d').date()
                
                # 检查卡密是否激活
                if not is_active:
                    return False, "卡密未激活"
                
                # 检查卡密是否过期
                today = datetime.now().date()
                if today > expiry_date:
                    return False, "卡密已过期"
                
                return True, "卡密有效"
            
            # 如果不是测试卡密，尝试连接数据库验证
            conn = self.get_db_connection()
            if not conn:
                # 如果无法连接数据库，但卡密是"test"，允许登录
                if code == "test":
                    return True, "测试卡密有效"
                return False, "无法连接到数据库，请使用测试卡密"
            
            with conn.cursor() as cursor:
                # 查询卡密
                cursor.execute('''
                SELECT is_active, expiry_date FROM activation_codes 
                WHERE code = %s
                ''', (code,))
                
                result = cursor.fetchone()
            
            conn.close()
            
            if not result:
                return False, "卡密不存在"
            
            is_active = result['is_active']
            expiry_date = result['expiry_date']
            
            # 检查卡密是否激活
            if not is_active:
                return False, "卡密未激活"
            
            # 检查卡密是否过期
            today = datetime.now().date()
            if today > expiry_date:
                return False, "卡密已过期"
            
            return True, "卡密有效"
        
        except Exception as e:
            print(f"验证卡密出错: {e}")
            # 如果验证过程出错，但卡密是"test"，允许登录
            if code == "test":
                return True, "测试卡密有效"
            return False, f"验证卡密时发生错误: {e}"

    def check_saved_password(self):
        """检查是否有保存的卡密，如果有则自动登录"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    saved_password = config.get('password', '')
                    
                    if saved_password:
                        # 验证保存的卡密
                        is_valid, message = self.validate_code(saved_password)
                        if is_valid:
                            # 有保存的有效卡密，自动登录
                            QtCore.QTimer.singleShot(500, self.auto_login)
            except Exception as e:
                print(f"读取配置文件出错: {e}")
    
    def auto_login(self):
        """自动登录"""
        # 在这里动态导入dc-chat.py模块，避免循环导入
        try:
            # 动态导入 dc-chat.py 模块
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
            
            self.dc_chat_window = dc_chat.Ui_Form()
            self.dc_chat_window.show()
            self.hide()
        except Exception as e:
            print(f"加载DC-Chat窗口失败: {e}")
            QMessageBox.critical(self, "错误", f"加载DC-Chat窗口失败: {e}")
    
    def save_password(self, password):
        """保存卡密到配置文件"""
        config = {'password': password}
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"保存配置文件出错: {e}")

    def login(self):
        """验证卡密并在验证成功后跳转到 DC-Chat 窗口"""
        entered_password = self.CodeLineEdit.text()
        
        if not entered_password:
            QMessageBox.warning(self, "登录失败", "请输入卡密！")
            return
        
        # 显示加载状态
        self.loginButton.setEnabled(False)
        self.loginButton.setText("验证中...")
        QtWidgets.QApplication.processEvents()
        
        # 验证卡密
        is_valid, message = self.validate_code(entered_password)
        
        # 恢复按钮状态
        self.loginButton.setEnabled(True)
        self.loginButton.setText("登录")
        
        if is_valid:
            # 密码正确，保存卡密
            self.save_password(entered_password)
            
            # 在这里动态导入dc-chat.py模块，避免循环导入
            try:
                # 动态导入 dc-chat.py 模块
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
                
                # 创建并显示 DC-Chat 窗口
                self.dc_chat_window = dc_chat.Ui_Form()
                self.dc_chat_window.show()
                # 隐藏登录窗口
                self.hide()
            except Exception as e:
                print(f"加载DC-Chat窗口失败: {e}")
                QMessageBox.critical(self, "错误", f"加载DC-Chat窗口失败: {e}")
        else:
            # 密码错误，显示错误消息
            QMessageBox.warning(self, "登录失败", f"卡密验证失败: {message}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_LoginForm()
    ui.show()
    sys.exit(app.exec())