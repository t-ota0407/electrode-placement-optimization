from PyQt5.QtWidgets import QMainWindow, QAction, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTranslator

import config
from tcpip_communication import TcpipCommunication
from views.main_widget import MainWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tcpip_communication = TcpipCommunication(config.REMOTE_HOST, config.REMOTE_PORT)
        self.translator = QTranslator()

        self.main_widget = MainWidget(self.tcpip_communication)
        self.setCentralWidget(self.main_widget)

        self.setup_menu_bar()
        
        self.setWindowTitle(self.tr('Electrode placement optimization system'))
        self.setWindowIcon(QIcon('../resources/favicon.ico'))
    
    def setup_menu_bar(self):
        self.menu_bar = self.menuBar()

        self.file_menu = self.menu_bar.addMenu(self.tr('File'))

        self.save_image_action = QAction(self.tr('Save image'), self)
        self.save_image_action.triggered.connect(self.main_widget.save_view)
        self.file_menu.addAction(self.save_image_action)

        self.save_results_action = QAction(self.tr('Save results'), self)
        self.save_results_action.triggered.connect(self.open_config)
        self.file_menu.addAction(self.save_results_action)

        self.editor_menu = self.menu_bar.addMenu(self.tr('Editor'))

        self.reconnect_action = QAction(QIcon('../resources/images/connection_ok_icon.png'), self.tr('Reconnection'), self)
        self.reconnect_action.triggered.connect(lambda: self.tcpip_communication.connect(config.REMOTE_HOST, config.REMOTE_PORT))
        self.editor_menu.addAction(self.reconnect_action)

        self.language_sub_menu = QMenu(self.tr('Language'), self)

        english_action = QAction('English', self)
        english_action.triggered.connect(lambda: self.switch_language('en'))

        japanese_action = QAction('日本語', self)
        japanese_action.triggered.connect(lambda: self.switch_language('ja'))

        self.language_sub_menu.addAction(english_action)
        self.language_sub_menu.addAction(japanese_action)

        self.editor_menu.addMenu(self.language_sub_menu)
    
    def save_image(self):
        print('save image')

    def open_config(self):
        print('open config')
    
    def switch_language(self, language_code):
        if language_code == 'ja':
            self.translator.load('translations/ja.qm')
        elif language_code == 'en':
            self.translator.load('translations/en.qm')
        
        _app.installTranslator(self.translator)
        self.retranslateUI()
    
    def retranslateUI(self):
        self.setWindowTitle(self.tr('Electrode placement optimization system'))
        self.file_menu.setTitle(self.tr('File'))
        self.save_image_action.setText(self.tr('Save image'))
        self.save_results_action.setText(self.tr('Save results'))
        self.editor_menu.setTitle(self.tr('Editor'))
        self.reconnect_action.setText(self.tr('Reconnection'))
        self.language_sub_menu.setTitle(self.tr('Language'))
        
        self.main_widget.retranslateUI() 