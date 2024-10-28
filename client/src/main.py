import os
import sys
import json
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QButtonGroup, QRadioButton, QMainWindow, QAction,
    QMenu)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, pyqtSlot, pyqtSignal, QTranslator
from vispy import scene, app
from vispy.geometry import MeshData
from functools import partial
from PIL import Image
from pathlib import Path

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

app.use_app('pyqt5')

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.tcpip_communication = TcpipCommunication(config.REMOTE_HOST, config.REMOTE_PORT)

        self.translator = QTranslator()

        self.main_widget = MainWidget(self.tcpip_communication)
        self.setCentralWidget(self.main_widget)

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
        self.reconnect_action.triggered.connect(partial(self.tcpip_communication.connect, config.REMOTE_HOST, config.REMOTE_PORT))
        self.editor_menu.addAction(self.reconnect_action)

        self.language_sub_menu = QMenu(self.tr('Language'), self)

        english_action = QAction('English', self)
        english_action.triggered.connect(lambda: self.switch_language('en'))

        japanese_action = QAction('日本語', self)
        japanese_action.triggered.connect(lambda: self.switch_language('ja'))

        self.language_sub_menu.addAction(english_action)
        self.language_sub_menu.addAction(japanese_action)

        self.editor_menu.addMenu(self.language_sub_menu)

        self.setWindowTitle(self.tr('Electrode placement optimization system'))
        self.setWindowIcon(QIcon('../resources/favicon.ico'))
    
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

class MainWidget(QWidget):

    selected_model = ModelType.LOWER_LIMB
    drawing_object_refs = []
    update_log_error_signal = pyqtSignal(str)
    update_log_optimization_result_signal = pyqtSignal(list)
    
    def __init__(self, tcpip_communication: TcpipCommunication):
        super().__init__()

        self.tcpip_communication = tcpip_communication

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
            self.load_model(model_type)
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
                    solutions_csv_path = (Path(config.LOWER_LIMB_CACHE_DIR_PATH, 'solutions.csv') if self.selected_model == ModelType.LOWER_LIMB
                                    else Path(config.UPPER_LIMB_CACHE_DIR_PATH, 'solutions.csv') if self.selected_model == ModelType.UPPER_LIMB
                                    else Path(config.HEAD_CACHE_DIR_PATH, 'solutions.csv'))
                    solutions_df = pd.read_csv(solutions_csv_path)
                except FileNotFoundError as e:
                    self.update_log_error_signal.emit('The solution file was not found')
                    return

                try:
                    optimization_condition = self.config_area.get_optimization_condition()
                except ValidationError as e:
                    self.update_log_error_signal.emit(e.message)
                    return

                if optimization_mode == OptimizationMode.CONDITIONED_OPTIMIZATION:
                    for constraint_domain, constraint_value in optimization_condition.constraints:
                        solutions_df = solutions_df[solutions_df[constraint_domain.name] <= constraint_value]

                result_df = solutions_df.nlargest(3, optimization_condition.target_domain.name)

                results = []
                for iter_idx, (index, row) in enumerate(result_df.iterrows()):
                    active_domain = self.active_domain_selector.get_active_domain()
                    anode = int(row.Anode)
                    cathode = int(row.Cathode)
                    print(iter_idx, '   ', index, '   ', anode, '   ', cathode)
                    
                    
                    cache_dir_path = (config.LOWER_LIMB_CACHE_DIR_PATH if self.selected_model == ModelType.LOWER_LIMB
                                      else config.UPPER_LIMB_CACHE_DIR_PATH if self.selected_model == ModelType.UPPER_LIMB
                                      else config.HEAD_CACHE_DIR_PATH)

                    for file in os.listdir(cache_dir_path):
                        if f'{anode}-{cathode}-{active_domain.name}' in file:
                            cache_path = Path(cache_dir_path, file)
                            with open(cache_path, 'r', encoding='utf-8') as file:
                                cached_data = file.read()
                            cached_data = json.loads(cached_data)
                            model_data = ModelData.from_json(cached_data)
                            
                            if iter_idx == 0:
                                self.draw_model(model_data, draw_plot_group=True, clear_view=False)

                            results.append((f'Solution{iter_idx+1}  Anode:{anode}, Cathode:{cathode}', partial(self.on_href_button_pressed, partial(self.draw_model, model_data, True, True))))

                self.update_log_optimization_result_signal.emit(results)

            self.update_log_optimization_result_signal.connect(self.handle_update_log_optimization_result_signal)
            self.update_log_error_signal.connect(self.handle_update_log_error_signal)
            self.async_transaction_worker = AsyncTransactionWorker(asyncTransaction)
            self.async_transaction_worker.finished.connect(self.finish_progress_window_view)
            self.async_transaction_worker.start()
        else:
            pass

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

    def load_model(self, model_type: ModelType):
        
        if config.USE_CACHE:
            cache_path = ModelType.to_initial_model_cache_path(model_type)            
            with open(cache_path, 'r', encoding='utf-8') as file:
                cached_data = file.read()
            cached_data = json.loads(cached_data)

            model_data = ModelData.from_json(cached_data)
            self.draw_model(model_data)
            
        else:
            model_data_json = self.tcpip_communication.load_model(model_type)
            model_data = ModelData.from_json(model_data_json)
            pass
    
    def draw_model(self, model_data: ModelData, draw_plot_group=False, clear_view=True):
        if clear_view:
            self.clar_view()

        points = scene.visuals.Markers()
        points.set_data(model_data.points.T, face_color=(.1, .1, .1, .5), edge_width=0, size=0.5)
        self.view.add(points)
        self.drawing_object_refs.append(points)

        lines = model_data.get_lines()
        line = scene.visuals.Line(lines, color=(.1, .1, .1, .4), connect='segments', width=1)
        self.view.add(line)
        self.drawing_object_refs.append(line)

        if draw_plot_group:
            mesh_data = MeshData(vertices=model_data.plot_group_points.T, faces=model_data.plot_group_edges.T, vertex_colors=model_data.get_plot_group_colors())
            mesh_visual = scene.visuals.Mesh(meshdata=mesh_data, mode='triangles')
            self.view.add(mesh_visual)
            self.drawing_object_refs.append(mesh_visual)

            colormap = model_data.get_color_map()
            clim = (round(model_data.plot_group_c_min_max[0], 2), round(model_data.plot_group_c_min_max[1], 2))
            colorbar = scene.visuals.ColorBar(cmap=colormap, orientation='right',
                                              size=(280, 40), parent=self.view, clim=clim)
            colorbar.transform = scene.transforms.STTransform(translate=(580, 300))
            self.drawing_object_refs.append(colorbar)
        
        x_min, x_max = np.min(model_data.points[0, :]), np.max(model_data.points[0, :])
        y_min, y_max = np.min(model_data.points[1, :]), np.max(model_data.points[1, :])
        z_min, z_max = np.min(model_data.points[2, :]), np.max(model_data.points[2, :])
        self.view.camera.center = ((x_min+x_max)/2, (y_min+y_max)/2, (z_min+z_max)/2)
    
    def clar_view(self):
        for drawing_object in self.drawing_object_refs:
            drawing_object.parent = None
        self.drawing_object_refs.clear()
    
    def save_view(self):
        image_array = self.canvas.render()
        image = Image.fromarray(image_array)
        image.save('./a.png')
    
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

if __name__ == '__main__':
    _app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(_app.exec_())
