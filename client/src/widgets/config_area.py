from typing import List
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel,
    QPushButton, QScrollArea, QVBoxLayout, QLineEdit
)

import fonts as fonts
from custom_types.optimization_mode import OptimizationMode
from custom_types.optimization_condition import OptimizationCondition
from custom_types.domain_type import DomainType
from errors.validation_error import ValidationError

class ConfigArea(QWidget):

    current_optimization_mode = OptimizationMode.SIMPLE_OPTIMIZATION

    def __init__(self, selectable_domain_descriptions):
        super().__init__()

        self.selectable_domain_descriptions = selectable_domain_descriptions

        self.main_layout = QVBoxLayout(self)
        self.setMaximumHeight(260)
        self.setMinimumHeight(260)

        self.mode1view = Mode1View(selectable_domain_descriptions)
        self.mode2view = Mode2View(selectable_domain_descriptions)
        self.mode2view.add_condition()

        self.main_layout.addWidget(self.mode1view)
        self.main_layout.addWidget(self.mode2view)

        self.setLayout(self.main_layout)

        self.update_view(self.current_optimization_mode)

    def update_view(self, optimization_mode: OptimizationMode):

        self.current_optimization_mode = optimization_mode
        
        self.mode1view.hide()
        self.mode2view.hide()

        if (optimization_mode == OptimizationMode.SIMPLE_OPTIMIZATION):
            self.mode1view.show()
        
        if (optimization_mode == OptimizationMode.CONDITIONED_OPTIMIZATION):
            self.mode2view.show()
    
    def update_selectable_domain_descriptions(self, selectable_domain_descriptions):
        self.mode1view.update_selectable_domain_descriptions(selectable_domain_descriptions)
        self.mode2view.update_selectable_domain_descriptions(selectable_domain_descriptions)
    
    def get_optimization_condition(self):
        print(self.current_optimization_mode)
        
        if self.current_optimization_mode == OptimizationMode.SIMPLE_OPTIMIZATION:
            optimization_condition = OptimizationCondition(self.current_optimization_mode,
                                                           self.mode1view.get_target_domain())

        elif self.current_optimization_mode == OptimizationMode.CONDITIONED_OPTIMIZATION:
            optimization_condition = OptimizationCondition(self.current_optimization_mode,
                                                           self.mode2view.get_target_domain(),
                                                           self.mode2view.get_constraints())
        print(optimization_condition)
        return optimization_condition
    
    def retranslateUI(self):
        self.mode1view.retranslateUI()
        self.mode2view.retranslateUI()


class Mode1View(QWidget):
    
    current_selectable_domain_descriptions = []
    
    def __init__(self, selectable_domain_descriptions):
        super().__init__()

        self.current_selectable_domain_descriptions = selectable_domain_descriptions

        self.layout = QVBoxLayout()

        horizontal_layout = QHBoxLayout()
        self.layout.addLayout(horizontal_layout)

        self.target_domain_label = QLabel(self.tr('Target Domain'))
        self.target_domain_label.setFont(fonts.plain_font)
        horizontal_layout.addWidget(self.target_domain_label)

        self.combo_box = QComboBox(self)
        for description in selectable_domain_descriptions:
            self.combo_box.addItem(self.tr(description))
        #self.combo_box.addItems(selectable_domain_descriptions)
        self.combo_box.setFont(fonts.plain_font)
        horizontal_layout.addWidget(self.combo_box)

        self.setLayout(self.layout)
    
    def update_selectable_domain_descriptions(self, selectable_domain_descriptions):
        self.current_selectable_domain_descriptions = selectable_domain_descriptions
        self.combo_box.clear()
        for description in selectable_domain_descriptions:
            self.combo_box.addItem(self.tr(description))
    
    def get_target_domain(self):
        return DomainType.from_description(self.combo_box.currentText())
    
    def retranslateUI(self):
        self.target_domain_label.setText(self.tr('Target Domain'))
        self.combo_box.clear()
        for description in self.current_selectable_domain_descriptions:
            self.combo_box.addItem(self.tr(description))

class Mode2View(QWidget):
    def __init__(self, selectable_domain_descriptions):
        super().__init__()

        self.selectable_domain_descriptions = selectable_domain_descriptions

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        target_domain_layout = QHBoxLayout()
        self.layout.addLayout(target_domain_layout)

        self.target_domain_label = QLabel(self.tr('Target Domain'))
        self.target_domain_label.setFont(fonts.plain_font)
        target_domain_layout.addWidget(self.target_domain_label)

        self.target_domain_combo_box = QComboBox()
        self.target_domain_combo_box.setFont(fonts.plain_font)
        self.target_domain_combo_box.addItems(selectable_domain_descriptions)
        target_domain_layout.addWidget(self.target_domain_combo_box)

        condition_layout = QVBoxLayout()
        self.layout.addLayout(condition_layout)

        condition_header_layout = QHBoxLayout()
        condition_layout.addLayout(condition_header_layout)

        self.condition_label = QLabel(self.tr('Constraints'))
        self.condition_label.setFont(fonts.plain_font)
        condition_header_layout.addWidget(self.condition_label)

        condition_header_layout.addStretch(1)

        self.condition_add_button = QPushButton(self.tr('Add constraints'))
        self.condition_add_button.setFont(fonts.plain_font)
        self.condition_add_button.clicked.connect(self.add_condition)
        condition_header_layout.addWidget(self.condition_add_button)

        condition_scroll_area = QScrollArea()
        condition_scroll_area.setWidgetResizable(True)
        condition_scroll_area.setMaximumHeight(160)
        condition_layout.addWidget(condition_scroll_area)

        condition_content_widget = QWidget()
        self.condition_content_layout = QVBoxLayout(condition_content_widget)
        self.condition_content_layout.setContentsMargins(0, 0, 0, 0)
        condition_scroll_area.setWidget(condition_content_widget)
    
    def add_condition(self):
        new_condition = Condition(self.selectable_domain_descriptions)
        self.condition_content_layout.addWidget(new_condition)
    
    def update_selectable_domain_descriptions(self, selectable_domain_descriptions):
        self.target_domain_combo_box.clear()
        self.target_domain_combo_box.addItems(selectable_domain_descriptions)

        conditions = self._get_all_conditions()
        
        for condition in conditions:
            condition.update_selectable_domain_descriptions(selectable_domain_descriptions)
    
    def get_target_domain(self):
        return DomainType.from_description(self.target_domain_combo_box.currentText())
    
    def get_constraints(self):
        conditions = self._get_all_conditions()
        return [condition.get_constraint() for condition in conditions]

    def _get_all_conditions(self):
        conditions: List[Condition] = []
        for i in range(self.condition_content_layout.count()):
            widget_item = self.condition_content_layout.itemAt(i).widget()
            if isinstance(widget_item, Condition):
                conditions.append(widget_item)
        return conditions
    
    def retranslateUI(self):
        self.target_domain_label.setText(self.tr('Target Domain'))
        self.condition_label.setText(self.tr('Constraints'))
        self.condition_add_button.setText(self.tr('Add constraints'))
        for condition in self._get_all_conditions():
            condition.update_selectable_domain_descriptions(self.selectable_domain_descriptions)

class Condition(QWidget):

    condition_num = 0

    def __init__(self, selectable_domain_descriptions):
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.combo_box = QComboBox()
        self.combo_box.setFixedWidth(240)
        self.combo_box.setFixedHeight(44)
        self.combo_box.setFont(fonts.plain_font)
        for description in selectable_domain_descriptions:
            self.combo_box.addItem(self.tr(description))
        self.layout.addWidget(self.combo_box)

        self.line_edit = QLineEdit()
        self.line_edit.setFixedWidth(160)
        self.line_edit.setFixedHeight(44)
        self.line_edit.setFont(fonts.plain_font)
        self.layout.addWidget(self.line_edit)

        self.delete_button = QPushButton('-')
        self.delete_button.setFixedWidth(100)
        self.delete_button.setFixedHeight(44)
        self.delete_button.setFont(fonts.plain_font)
        self.delete_button.clicked.connect(self.delete_self)
        self.layout.addWidget(self.delete_button)

        Condition.condition_num += 1

    def delete_self(self):
        if (Condition.condition_num > 1) and self.parent():
            self.setParent(None)
            Condition.condition_num -= 1
    
    def update_selectable_domain_descriptions(self, selectable_domain_descriptions):
        self.combo_box.clear()
        for description in selectable_domain_descriptions:
            self.combo_box.addItem(self.tr(description))

    def get_constraint(self):
        domain = DomainType.from_description(self.combo_box.currentText())
        value = self.line_edit.text()
        try:
            value = float(value)
        except ValueError:
            raise ValidationError('Please enter a numeric value for the constraints.')
        return (domain, float(value))
