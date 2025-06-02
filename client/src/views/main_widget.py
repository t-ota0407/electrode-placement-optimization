import os
import json
import numpy as np
from pathlib import Path
from functools import partial
from PIL import Image

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                          QPushButton, QLabel, QButtonGroup, QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, pyqtSlot, pyqtSignal
from vispy import scene
from vispy.geometry import MeshData

import config as config
import fonts as fonts
from tcpip_communication import TcpipCommunication
from widgets.log_console import LogConsole
from widgets.async_transaction_progress_window import AsyncTransactionProgressWindow
from async_transaction_worker import AsyncTransactionWorker
from custom_types.model_type import ModelType
from custom_types.domain_type import DomainType
from custom_types.optimization_mode import OptimizationMode
from widgets.config_area import ConfigArea
from model_data import ModelData
from widgets.active_domain_selector import ActiveDomainSelector
from errors.validation_error import ValidationError
from services.model_service import ModelService
from services.optimization_service import OptimizationService

class MainWidget(QWidget):
    selected_model = ModelType.LOWER_LIMB
    drawing_object_refs = []
    update_log_error_signal = pyqtSignal(str)
    update_log_optimization_result_signal = pyqtSignal(list)
    
    def __init__(self, tcpip_communication: TcpipCommunication):
        super().__init__()
        self.tcpip_communication = tcpip_communication
        self.model_service = ModelService(tcpip_communication)
        self.optimization_service = OptimizationService()
        
        self._setup_ui()
        self._setup_signals()
        self.initialize_layout_state()
        
        self.show()

    def _setup_ui(self):
        """UIコンポーネントの設定"""
        main_layout = QHBoxLayout()
        self._setup_left_panel(main_layout)
        self._setup_right_panel(main_layout)
        self.setLayout(main_layout)

    def _setup_left_panel(self, main_layout):
        """左パネルの設定"""
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        # Body Part Section
        self._setup_body_part_section(left_layout)
        
        # Optimization Mode Section
        self._setup_optimization_mode_section(left_layout)
        
        # Settings Section
        self._setup_settings_section(left_layout)
        
        # Execute Button
        self._setup_execute_button(left_layout)

    def _setup_body_part_section(self, layout):
        """体のパーツ選択セクションの設定"""
        layout.addStretch(1)
        
        self.body_part_label = QLabel(self.tr('Body part'))
        self.body_part_label.setFont(fonts.header_font)
        layout.addWidget(self.body_part_label)

        body_part_images_layout = QHBoxLayout()
        for model_type in [ModelType.LOWER_LIMB, ModelType.UPPER_LIMB, ModelType.HEAD]:
            body_part_image_button = QPushButton()
            body_part_image_button.setIcon(QIcon(str(ModelType.to_icon_img_path(model_type))))
            body_part_image_button.setIconSize(QSize(150, 200))
            body_part_image_button.clicked.connect(partial(self.on_load_model_button_pressed, model_type))
            body_part_images_layout.addWidget(body_part_image_button)
        layout.addLayout(body_part_images_layout)

    def _setup_optimization_mode_section(self, layout):
        """最適化モード選択セクションの設定"""
        layout.addStretch(3)
        
        self.optimization_mode_label = QLabel(self.tr('Optimization mode'))
        self.optimization_mode_label.setFont(fonts.header_font)
        layout.addWidget(self.optimization_mode_label)

        optimization_mode_radio_layout = QVBoxLayout()
        self.optimization_mode_radio_group = QButtonGroup(self)
        for optimization_mode in [OptimizationMode.SIMPLE_OPTIMIZATION, 
                                OptimizationMode.CONDITIONED_OPTIMIZATION,
                                OptimizationMode.COMBINED_STIMULATION]:
            radio_button = QRadioButton(self.tr(OptimizationMode.to_description(optimization_mode)))
            radio_button.setFont(fonts.plain_font)
            radio_button.toggled.connect(partial(self.update_optimization_mode, optimization_mode))
            self.optimization_mode_radio_group.addButton(radio_button, OptimizationMode.to_identical_number(optimization_mode))
            optimization_mode_radio_layout.addWidget(radio_button)
        layout.addLayout(optimization_mode_radio_layout)

    def _setup_settings_section(self, layout):
        """設定セクションの設定"""
        layout.addStretch(3)
        
        self.settings_label = QLabel(self.tr('Optimization settings'))
        self.settings_label.setFont(fonts.header_font)
        layout.addWidget(self.settings_label)

        self.config_area = ConfigArea(DomainType.get_targetable_descriptions(ModelType.LOWER_LIMB))
        layout.addWidget(self.config_area)

    def _setup_execute_button(self, layout):
        """実行ボタンの設定"""
        layout.addStretch(3)
        
        self.button_execute = QPushButton(self.tr('Start optimization'))
        self.button_execute.setFont(fonts.highlighted_font)
        self.button_execute.clicked.connect(self.on_execute_button_pressed)
        layout.addWidget(self.button_execute)
        
        layout.addStretch(1)

    def _setup_right_panel(self, main_layout):
        """右パネルの設定"""
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        right_layout.addStretch(1)

        # 3D View
        self._setup_3d_view(right_layout)

        # Domain Selector
        self.active_domain_selector = ActiveDomainSelector(DomainType.get_viewable_descriptions(ModelType.LOWER_LIMB))
        right_layout.addWidget(self.active_domain_selector)

        right_layout.addStretch(3)

        # Log Console
        self.log_console = LogConsole()
        right_layout.addWidget(self.log_console)

        right_layout.addStretch(1)

    def _setup_3d_view(self, layout):
        """3Dビューの設定"""
        self.canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='white')
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'

        self.canvas.events.mouse_move.connect(self.on_mouse_move)
        self.last_mouse_pos = None

        self.canvas.native.setMinimumSize(400, 400)
        layout.addWidget(self.canvas.native)

    def _setup_signals(self):
        """シグナルの設定"""
        self.update_log_optimization_result_signal.connect(self.handle_update_log_optimization_result_signal)
        self.update_log_error_signal.connect(self.handle_update_log_error_signal)

    def initialize_layout_state(self):
        """レイアウトの初期状態設定"""
        initial_selected_button = self.optimization_mode_radio_group.button(
            OptimizationMode.to_identical_number(OptimizationMode.SIMPLE_OPTIMIZATION)
        )
        initial_selected_button.setChecked(True)
        self.log_console.log('The optimization system has been activated.')

    @pyqtSlot()
    def update_optimization_mode(self, optimization_mode: OptimizationMode):
        """最適化モードの更新"""
        selected_button = self.sender()
        if selected_button.isChecked():
            self.config_area.update_view(optimization_mode)

    @pyqtSlot()
    def on_load_model_button_pressed(self, model_type: ModelType):
        """モデル読み込みボタンのイベントハンドラ"""
        self.selected_model = model_type
        self._start_async_transaction(
            lambda: self._load_model_transaction(model_type)
        )

    def _load_model_transaction(self, model_type: ModelType):
        """モデル読み込みのトランザクション処理"""
        self.model_service.load_model(model_type)
        self.config_area.update_selectable_domain_descriptions(
            DomainType.get_targetable_descriptions(model_type)
        )
        self.active_domain_selector.update_selectable_domain_descriptions(
            DomainType.get_viewable_descriptions(model_type)
        )

    def on_execute_button_pressed(self):
        """実行ボタンのイベントハンドラ"""
        self.button_execute.setEnabled(False)
        
        if config.USE_CACHE:
            optimization_id = self.optimization_mode_radio_group.checkedId()
            optimization_mode = OptimizationMode.from_identical_number(optimization_id)
            
            self._start_async_transaction(
                lambda: self._execute_optimization_transaction(optimization_mode)
            )
        
        self.button_execute.setEnabled(True)

    def _execute_optimization_transaction(self, optimization_mode: OptimizationMode):
        """最適化実行のトランザクション処理"""
        try:
            optimization_condition = self.config_area.get_optimization_condition()
            results = self.optimization_service.execute_optimization(
                self.selected_model,
                optimization_mode,
                optimization_condition,
                self.active_domain_selector.get_active_domain()
            )
            self.update_log_optimization_result_signal.emit(results)
            
        except (ValidationError, FileNotFoundError) as e:
            self.update_log_error_signal.emit(str(e))

    def _start_async_transaction(self, transaction_func):
        """非同期トランザクションの開始"""
        self.setEnabled(False)
        self.progressWindow = AsyncTransactionProgressWindow()
        self.progressWindow.show()
        
        self.async_transaction_worker = AsyncTransactionWorker(transaction_func)
        self.async_transaction_worker.finished.connect(self.finish_progress_window_view)
        self.async_transaction_worker.start()

    def finish_progress_window_view(self):
        """進捗ウィンドウの終了処理"""
        self.setEnabled(True)
        self.progressWindow.close()

    def handle_update_log_error_signal(self, message):
        """エラーログ更新シグナルのハンドラ"""
        self.log_console.log(message=message, is_error=True)

    def handle_update_log_optimization_result_signal(self, results):
        """最適化結果ログ更新シグナルのハンドラ"""
        for message, href_function in results:
            self.log_console.log(message, href_function=href_function)

    def on_mouse_move(self, event):
        """マウス移動イベントのハンドラ"""
        if event.button == 3:  # mouse wheel
            if event.is_dragging:
                if self.last_mouse_pos is not None:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    dx /= self.view.size[0]
                    dy /= self.view.size[1]

                    self.view.camera.center = (
                        self.view.camera.center[0] - dx * 20,
                        self.view.camera.center[1] + dy * 20,
                        self.view.camera.center[2]
                    )
                self.last_mouse_pos = event.pos
            else:
                self.last_mouse_pos = None
        else:
            self.last_mouse_pos = None

    def save_view(self):
        """ビューの保存"""
        image_array = self.canvas.render()
        image = Image.fromarray(image_array)
        image.save('./a.png')

    def retranslateUI(self):
        """UI要素の翻訳更新"""
        self.body_part_label.setText(self.tr('Body part'))
        self.optimization_mode_label.setText(self.tr('Optimization mode'))
        for button in self.optimization_mode_radio_group.buttons():
            id = self.optimization_mode_radio_group.id(button)
            optimization_mode = OptimizationMode.from_identical_number(id)
            button.setText(self.tr(OptimizationMode.to_description(optimization_mode)))
        self.settings_label.setText(self.tr('Optimization settings'))

        self.config_area.retranslateUI()
        self.active_domain_selector.retranslateUI()
        self.log_console.retranslateUI() 