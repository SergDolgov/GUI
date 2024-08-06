
import json
import sys
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTextEdit, QSystemTrayIcon, QMenu, QLabel, QLineEdit
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
import subprocess
import os
from PyQt6.QtCore import QThread, pyqtSignal

from linkensphere_api import LinkenSphereApi
from selenium_api import SeleniumApi
from totalcontrol_api import TotalControlApi
from utils import find_by_key

class RestartThread(QThread):
    finished = pyqtSignal()

    def run(self):
        os.system("py main.py")
        self.finished.emit()

class MainWindow(QMainWindow):
    
    linken_sphere_api = None
    total_control_api = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My GUI")
        self.setGeometry(100, 100, 900, 700)

        # self.linken_sphere_api = LinkenSphereApi(self)    
        # self.total_control_api = TotalControlApi(self)    
        
        # Настраиваем логирование
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler(self)
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)

        # Создаем виджеты
        self.start_button = QPushButton("Start Linken Sphere")
        self.minimize_button = QPushButton("Minimize to tray")
        self.restart_button = QPushButton("Restart")
        
        self.signin_button = QPushButton("sign in")
        self.signout_button = QPushButton("sign out")
        self.getsessions_button = QPushButton("get sessions")
        self.createsessions_button = QPushButton("create session")
        self.delete_button = QPushButton("delete session")
        self.getdesktops_button = QPushButton("get desktops")
        self.setactivedesktop_button = QPushButton("set active desktop")
        self.getproviders_button = QPushButton("get providers")
        self.setactiveprovider_button = QPushButton("set active provider")

        self.input_uuid = QLineEdit("uuid")
        
        self.get_license_button = QPushButton("get_license")
        self.get_settings_button = QPushButton("get_settings")
        self.get_tasks_button = QPushButton("get_tasks")
        self.gensessions_button = QPushButton("gen sessions")
        self.cleansessions_button = QPushButton("clean sessions")

        self.find_button = QPushButton("find")

        self.log_text_edit = QTextEdit()
        
        # Создаем главный вертикальный layout
        main_layout = QVBoxLayout()

        # Создаем горизонтальные layout для кнопок
        buttons_layout = QHBoxLayout()
        
        buttons_layout_1 = QVBoxLayout()
        buttons_layout_2 = QVBoxLayout()
        buttons_layout_3 = QVBoxLayout()
        buttons_layout_4 = QVBoxLayout()

        # Создаем надписи для колонок
        column_1_label = QLabel("Main")
        column_2_label = QLabel("Linked Sphere API")
        column_3_label = QLabel("Total control API")
        column_4_label = QLabel("Selenium API")
        
        # Устанавливаем выравнивание надписей и кнопок по верхнему краю
        buttons_layout_1.setAlignment(Qt.AlignmentFlag.AlignTop)
        buttons_layout_2.setAlignment(Qt.AlignmentFlag.AlignTop)
        buttons_layout_3.setAlignment(Qt.AlignmentFlag.AlignTop)
        buttons_layout_4.setAlignment(Qt.AlignmentFlag.AlignTop)
        column_1_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        column_2_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        column_3_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        column_4_label.setAlignment(Qt.AlignmentFlag.AlignTop)
                
        # Добавляем надписи в колонки
        buttons_layout_1.addWidget(column_1_label)
        buttons_layout_2.addWidget(column_2_label)
        buttons_layout_3.addWidget(column_3_label)
        buttons_layout_4.addWidget(column_4_label)
       
        # Добавляем кнопки в layout
        buttons_layout_1.addWidget(self.start_button)
        buttons_layout_1.addWidget(self.minimize_button)
        buttons_layout_1.addWidget(self.restart_button)

        # LinkenSphere
        buttons_layout_2.addWidget(self.signin_button)
        buttons_layout_2.addWidget(self.signout_button)
        buttons_layout_2.addWidget(self.getsessions_button)
        buttons_layout_2.addWidget(self.createsessions_button)
        buttons_layout_2.addWidget(self.delete_button)
        buttons_layout_2.addWidget(self.getdesktops_button)
        buttons_layout_2.addWidget(self.setactivedesktop_button)
        buttons_layout_2.addWidget(self.getproviders_button)
        buttons_layout_2.addWidget(self.setactiveprovider_button)

        # TotalControl
        buttons_layout_3.addWidget(self.get_license_button)
        buttons_layout_3.addWidget(self.get_settings_button)
        buttons_layout_3.addWidget(self.get_tasks_button)
        buttons_layout_3.addWidget(self.gensessions_button)
        buttons_layout_3.addWidget(self.cleansessions_button)

        # Selenium
        buttons_layout_4.addWidget(self.find_button)

       # Создаем поля ввода в нижней части каждой колонки
        buttons_layout_2.addWidget(self.input_uuid)
        
        # Добавляем горизонтальные layout в главный вертикальный layout
        buttons_layout.addLayout(buttons_layout_1)
        buttons_layout.addLayout(buttons_layout_2)
        buttons_layout.addLayout(buttons_layout_3)
        buttons_layout.addLayout(buttons_layout_4)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.log_text_edit)

        # Создаем central widget и устанавливаем main_layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Подключаем сигналы к слотам
        self.start_button.clicked.connect(self.start_button_clicked)
        self.minimize_button.clicked.connect(self.minimize_button_clicked)
        self.restart_button.clicked.connect(self.restart_button_clicked)
         
         # LinkenSphere
        self.signin_button.clicked.connect(self.signin_button_clicked)
        self.signout_button.clicked.connect(self.signout_button_clicked)
        self.getsessions_button.clicked.connect(self.getsessions_button_clicked)
        self.createsessions_button.clicked.connect(self.createsessions_button_clicked)
        self.delete_button.clicked.connect(self.delete_button_clicked)
        self.getdesktops_button.clicked.connect(self.getdesktops_button_clicked)
        self.setactivedesktop_button.clicked.connect(self.setactivedesktop_button_clicked)
        self.getproviders_button.clicked.connect(self.getproviders_button_clicked)
        self.setactiveprovider_button.clicked.connect(self.setactiveprovider_button_clicked)
      
         # TotalControl  
        self.get_license_button.clicked.connect(self.get_license_button_clicked)
        self.get_settings_button.clicked.connect(self.get_settings_button_clicked)
        self.get_tasks_button.clicked.connect(self.get_tasks_button_clicked)
        self.gensessions_button.clicked.connect(self.gensessions_button_clicked)
        self.cleansessions_button.clicked.connect(self.cleansessions_button_clicked)

         # Selenium
        self.find_button.clicked.connect(self.find_button_clicked)

        # Настраиваем системный трей
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))
        tray_menu = QMenu()
        restore_action = QAction("Restore", self)
        restore_action.triggered.connect(self.show)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(restore_action)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def write(self, record):
        # msg = self.formatter.format(record)
        self.log_text_edit.append(record)

    def start_button_clicked(self):
        try:
            # Путь до исполняемого файла Linken Sphere
            # exe_path = r"C:\Program Files (x86)\Linken Sphere\Linken Sphere.exe"

            # Запуск процесса
            # subprocess.run([exe_path], creationflags=subprocess.CREATE_NO_WINDOW, check=True)
            
            shortcut_path = r"C:\Users\Public\Desktop\Linken Sphere.lnk"

            # Запуск ярлыка
            process = subprocess.Popen(["explorer.exe", shortcut_path])
            process.wait()       
            
            self.logger.info("Started Linken Sphere successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start Linken Sphere: {e}")

    def minimize_button_clicked(self):
        self.logger.info("Minimized to tray")
        self.hide()
        self.tray_icon.showMessage("Application minimized", "The application is running in the tray")

    def restart_button_clicked(self):
        self.logger.info("Restart")
        self.restart_thread = RestartThread()
        self.restart_thread.finished.connect(QApplication.instance().quit)
        self.restart_thread.start()
        self.hide()

# LinkenSphere

    def signin_button_clicked(self):
        user = "7771755+beta@gmail.com"
        password = "QwErTy54321+++"
        self.linken_sphere_api.signin(user=user, password=password)

    def signout_button_clicked(self):
        response = self.linken_sphere_api.signout()
        if response == "":
            self.logger.info("Sign outed in successfully")

    def getsessions_button_clicked(self):
        self.linken_sphere_api.get_sessions()

    def createsessions_button_clicked(self):
        self.linken_sphere_api.create_sessions()

    def delete_button_clicked(self):
        self.linken_sphere_api.delete_session(uuid=self.input_uuid.text)

    def getdesktops_button_clicked(self):
        self.linken_sphere_api.get_desktops()

    def setactivedesktop_button_clicked(self):
        self.linken_sphere_api.set_active_desktop(uuid=self.input_uuid.text)

    def getproviders_button_clicked(self):
        self.linken_sphere_api.get_providers()

    def setactiveprovider_button_clicked(self):
        self.linken_sphere_api.set_active_provider(uuid=self.input_uuid.text)

 # TotalControl 
 
    def get_license_button_clicked(self):
        self.total_control_api.get_license()

    def get_settings_button_clicked(self):
        self.total_control_api.get_settings(lic="", )

    def get_tasks_button_clicked(self):
        tasks = self.total_control_api.get_tasks(lic="666", )
        
    def gensessions_button_clicked(self):
    
        settings_str = self.total_control_api.get_settings(lic="666")
        settings_dict = json.loads(settings_str)
        provider = settings_dict["provider"]
        pipeline = settings_dict["pipeline"]
        connection = settings_dict["connection"]
        count = settings_dict["count"]
        
        for i in range(count):
            session_str = self.linken_sphere_api.create_sessions()
            session = json.loads(session_str)[0]
            uuid=session["uuid"]
            name=session["name"]
            self.linken_sphere_api.set_connection(uuid=uuid, connection=connection)
            self.total_control_api.confirm_session(session=session, pipeline=pipeline) 
            self.logger.info(f"confirm_session: {name}")
            
        
    def cleansessions_button_clicked(self):
        
        response = self.linken_sphere_api.get_sessions()
        sessions = json.loads(response)

        payload = []
        
        for session in sessions:
            payload.append({"uuid":session["uuid"]})
        
        response = self.total_control_api.clean_sessions(lic="666", payload=payload) 
        clean_sessions = json.loads(response)
        
        for session in clean_sessions:
            
            clean_session = find_by_key(sessions, key="uuid", value=session["uuid"])
            
            if clean_session:
                
                name = clean_session["name"]
                
                if clean_session["status"] == "running":
                    self.linken_sphere_api.stop_session(uuid=session["uuid"])  
                    self.logger.info(f"stoped_session: {name}")
                
                self.linken_sphere_api.delete_session(uuid=session["uuid"])  
                self.logger.info(f"deleted_session: {name}")


# Selenium

    def find_button_clicked(self):
        selenium = SeleniumApi(self)
        selenium.find("http://www.python.org")

      
        
