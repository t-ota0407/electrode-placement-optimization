from PyQt5.QtWidgets import QMainWindow, QAction, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTranslator
from pathlib import Path
from functools import partial

import config as config
from tcpip_communication import TcpipCommunication
from views.main_widget import MainWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_communication()
        self._setup_translation()
        self._setup_main_widget()
        self._setup_menu_bar()
        self._check_cache_files()
        self._setup_window_properties()

    def _setup_communication(self):
        """通信関連の初期設定"""
        self.tcpip_communication = TcpipCommunication(config.REMOTE_HOST, config.REMOTE_PORT)

    def _setup_translation(self):
        """翻訳関連の初期設定"""
        self.translator = QTranslator()

    def _setup_main_widget(self):
        """メインウィジェットの設定"""
        self.main_widget = MainWidget(self.tcpip_communication)
        self.setCentralWidget(self.main_widget)

    def _check_cache_files(self):
        """キャッシュファイルの存在確認"""
        if not config.USE_CACHE:
            return

        cache_paths = {
            'Lower Limb': Path(config.LOWER_LIMB_CACHE_DIR_PATH, 'solutions.csv'),
            'Upper Limb': Path(config.UPPER_LIMB_CACHE_DIR_PATH, 'solutions.csv'),
            'Head': Path(config.HEAD_CACHE_DIR_PATH, 'solutions.csv')
        }

        for part_name, path in cache_paths.items():
            if not path.exists():
                self.main_widget.log_console.log(
                    f"Error: The cache setting is activated, but the solutions.csv file was not found in {path.parent}",
                    is_error=True
                )

    def _setup_menu_bar(self):
        """メニューバーの設定"""
        self.menu_bar = self.menuBar()
        self._setup_file_menu()
        self._setup_editor_menu()

    def _setup_file_menu(self):
        """ファイルメニューの設定"""
        self.file_menu = self.menu_bar.addMenu(self.tr('File'))

        # Save Image Action
        self.save_image_action = QAction(self.tr('Save image'), self)
        self.save_image_action.triggered.connect(self.main_widget.save_view)
        self.file_menu.addAction(self.save_image_action)

        # Save Results Action
        self.save_results_action = QAction(self.tr('Save results'), self)
        self.save_results_action.triggered.connect(self.open_config)
        self.file_menu.addAction(self.save_results_action)

    def _setup_editor_menu(self):
        """エディターメニューの設定"""
        self.editor_menu = self.menu_bar.addMenu(self.tr('Editor'))

        # Reconnect Action
        self.reconnect_action = QAction(QIcon('../resources/images/connection_ok_icon.png'), self.tr('Reconnection'), self)
        self.reconnect_action.triggered.connect(
            partial(self.tcpip_communication.connect, config.REMOTE_HOST, config.REMOTE_PORT)
        )
        self.editor_menu.addAction(self.reconnect_action)

        # Language Submenu
        self._setup_language_submenu()

    def _setup_language_submenu(self):
        """言語サブメニューの設定"""
        self.language_sub_menu = QMenu(self.tr('Language'), self)

        # English Action
        english_action = QAction('English', self)
        english_action.triggered.connect(lambda: self.switch_language('en'))
        self.language_sub_menu.addAction(english_action)

        # Japanese Action
        japanese_action = QAction('日本語', self)
        japanese_action.triggered.connect(lambda: self.switch_language('ja'))
        self.language_sub_menu.addAction(japanese_action)

        self.editor_menu.addMenu(self.language_sub_menu)

    def _setup_window_properties(self):
        """ウィンドウプロパティの設定"""
        self.setWindowTitle(self.tr('Electrode placement optimization system'))
        self.setWindowIcon(QIcon('../resources/favicon.ico'))

    def save_image(self):
        """画像保存処理"""
        print('save image')

    def open_config(self):
        """設定を開く処理"""
        print('open config')

    def switch_language(self, language_code):
        """言語切り替え処理"""
        if language_code == 'ja':
            self.translator.load('translations/ja.qm')
        elif language_code == 'en':
            self.translator.load('translations/en.qm')
        
        QApplication.instance().installTranslator(self.translator)
        self.retranslateUI()

    def retranslateUI(self):
        """UI要素の翻訳更新"""
        self.setWindowTitle(self.tr('Electrode placement optimization system'))
        self.file_menu.setTitle(self.tr('File'))
        self.save_image_action.setText(self.tr('Save image'))
        self.save_results_action.setText(self.tr('Save results'))
        self.editor_menu.setTitle(self.tr('Editor'))
        self.reconnect_action.setText(self.tr('Reconnection'))
        self.language_sub_menu.setTitle(self.tr('Language'))
        
        self.main_widget.retranslateUI() 