from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QButtonGroup, QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, pyqtSlot, pyqtSignal
from vispy import scene
from functools import partial

import config
import fonts
from tcpip_communication import TcpipCommunication
from widgets.log_console import LogConsole
from widgets.async_transaction_progress_window import AsyncTransactionProgressWindow
from async_transaction_worker import AsyncTransactionWorker
from custom_types.model_type import ModelType
from custom_types.domain_type import DomainType
from custom_types.optimization_mode import OptimizationMode
from widgets.config_area import ConfigArea
from widgets.active_domain_selector import ActiveDomainSelector
from services.model_renderer import ModelRenderer
from services.optimization_service import OptimizationService
from errors.validation_error import ValidationError

class MainWidget(QWidget):
    selected_model = ModelType.LOWER_LIMB
    update_log_error_signal = pyqtSignal(str)
    update_log_optimization_result_signal = pyqtSignal(list)
    
    def __init__(self, tcpip_communication: TcpipCommunication):
        super().__init__()

        self.tcpip_communication = tcpip_communication
        self.optimization_service = OptimizationService()

        self.set_layouts()
        self.initialize_layout_state()

        self.show()

    def set_layouts(self):
        main_layout = QHBoxLayout()

        # Set left layout
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        left_layout.addStretch(1)

        self.body_part_label = QLabel(self.tr('Body part'))
        self.body_part_label.setFont(fonts.header_font)
        left_layout.addWidget(self.body_part_label)

        body_part_images_layout = QHBoxLayout()
        for model_type in [ModelType.LOWER_LIMB, ModelType.UPPER_LIMB, ModelType.HEAD]:
            body_part_image_button = QPushButton()
            body_part_image_button.setIcon(QIcon(str(ModelType.to_icon_img_path(model_type))))
            body_part_image_button.setIconSize(QSize(150, 200))
            body_part_image_button.clicked.connect(partial(self.on_load_model_button_pressed, model_type))
            body_part_images_layout.addWidget(body_part_image_button)
        left_layout.addLayout(body_part_images_layout)

        left_layout.addStretch(3)

        self.optimization_mode_label = QLabel(self.tr('Optimization mode'))
        self.optimization_mode_label.setFont(fonts.header_font)
        left_layout.addWidget(self.optimization_mode_label)

        optimization_mode_radio_layout = QVBoxLayout()
        self.optimization_mode_radio_group = QButtonGroup(self)
        for optimization_mode in [OptimizationMode.SIMPLE_OPTIMIZATION, OptimizationMode.CONDITIONED_OPTIMIZATION]:
            radio_button = QRadioButton(self.tr(OptimizationMode.to_description(optimization_mode)))
            radio_button.setFont(fonts.plain_font)
            radio_button.toggled.connect(partial(self.update_optimization_mode, optimization_mode))
            self.optimization_mode_radio_group.addButton(radio_button, OptimizationMode.to_identical_number(optimization_mode))
            optimization_mode_radio_layout.addWidget(radio_button)
        left_layout.addLayout(optimization_mode_radio_layout)

        left_layout.addStretch(3)

        self.settings_label = QLabel(self.tr('Optimization settings'))
        self.settings_label.setFont(fonts.header_font)
        left_layout.addWidget(self.settings_label)

        self.config_area = ConfigArea(DomainType.get_targetable_descriptions(ModelType.LOWER_LIMB))
        left_layout.addWidget(self.config_area)

        left_layout.addStretch(3)

        self.button_execute = QPushButton(self.tr('Start optimization'))
        self.button_execute.setFont(fonts.highlighted_font)
        self.button_execute.clicked.connect(self.on_execute_button_pressed)
        left_layout.addWidget(self.button_execute)

        left_layout.addStretch(1)

        # Set right layout
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        right_layout.addStretch(1)

        self.canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='white')
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'

        self.canvas.events.mouse_move.connect(self.on_mouse_move)
        self.last_mouse_pos = None

        self.canvas.native.setMinimumSize(400, 400)
        right_layout.addWidget(self.canvas.native)

        self.model_renderer = ModelRenderer(self.canvas, self.view)

        self.active_domain_selector = ActiveDomainSelector(DomainType.get_viewable_descriptions(ModelType.LOWER_LIMB))
        right_layout.addWidget(self.active_domain_selector)

        right_layout.addStretch(3)

        self.log_console = LogConsole()
        right_layout.addWidget(self.log_console)

        right_layout.addStretch(1)
        
        self.setLayout(main_layout)
    
    def initialize_layout_state(self):
        initial_selected_button = self.optimization_mode_radio_group.button(OptimizationMode.to_identical_number(OptimizationMode.SIMPLE_OPTIMIZATION))
        initial_selected_button.setChecked(True)

        self.log_console.log('The optimization system has been activated.')

    def on_mouse_move(self, event):
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
    
    @pyqtSlot()
    def update_optimization_mode(self, optimization_mode: OptimizationMode):
        selected_button = self.sender()
        if selected_button.isChecked():
            self.config_area.update_view(optimization_mode)
    
    @pyqtSlot()
    def on_load_model_button_pressed(self, model_type: ModelType):
        self.selected_model = model_type

        self.setEnabled(False)
        self.progressWindow = AsyncTransactionProgressWindow()
        self.progressWindow.show()

        def asyncTransaction():
            model_data = self.optimization_service.load_model(model_type, self.tcpip_communication)
            self.model_renderer.draw_model(model_data)
            self.config_area.update_selectable_domain_descriptions(DomainType.get_targetable_descriptions(model_type))
            self.active_domain_selector.update_selectable_domain_descriptions(DomainType.get_viewable_descriptions(model_type))

        self.async_transaction_worker = AsyncTransactionWorker(asyncTransaction)
        self.async_transaction_worker.finished.connect(self.finish_progress_window_view)
        self.async_transaction_worker.start()
    
    def on_execute_button_pressed(self):
        self.button_execute.setEnabled(False)
        
        if config.USE_CACHE:
            self.setEnabled(False)
            self.progressWindow = AsyncTransactionProgressWindow()
            self.progressWindow.show()

            optimization_id = self.optimization_mode_radio_group.checkedId()
            optimization_mode = OptimizationMode.from_identical_number(optimization_id)

            def asyncTransaction():
                try:
                    optimization_condition = self.config_area.get_optimization_condition()
                    active_domain = self.active_domain_selector.get_active_domain()
                    
                    results = self.optimization_service.execute_optimization(
                        self.selected_model,
                        optimization_mode,
                        optimization_condition,
                        active_domain,
                        self.model_renderer.draw_model
                    )
                    
                    self.update_log_optimization_result_signal.emit(results)
                except ValidationError as e:
                    self.update_log_error_signal.emit(e.message)

            self.update_log_optimization_result_signal.connect(self.handle_update_log_optimization_result_signal)
            self.update_log_error_signal.connect(self.handle_update_log_error_signal)
            self.async_transaction_worker = AsyncTransactionWorker(asyncTransaction)
            self.async_transaction_worker.finished.connect(self.finish_progress_window_view)
            self.async_transaction_worker.start()

        self.button_execute.setEnabled(True)
    
    def on_href_button_pressed(self, partial_func):
        self.setEnabled(False)
        self.progressWindow = AsyncTransactionProgressWindow()
        self.progressWindow.show()
        
        def asyncTransaction():
            partial_func()

        self.async_transaction_worker = AsyncTransactionWorker(asyncTransaction)
        self.async_transaction_worker.finished.connect(self.finish_progress_window_view)
        self.async_transaction_worker.start()
        
    def finish_progress_window_view(self):
        self.setEnabled(True)
        self.progressWindow.close()
    
    def handle_update_log_error_signal(self, message):
        self.log_console.log(message=message, is_error=True)
    
    def handle_update_log_optimization_result_signal(self, results):
        for message, href_function in results:
            self.log_console.log(message, href_function=href_function)
    
    def save_view(self):
        self.model_renderer.save_view('./a.png')
    
    def retranslateUI(self):
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