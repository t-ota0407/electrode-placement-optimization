from PyQt5.QtWidgets import (QLabel, QComboBox, QWidget, QHBoxLayout)

import fonts as fonts
from custom_types.domain_type import DomainType

class ActiveDomainSelector(QWidget):
    def __init__(self, selectable_domain_descriptions):
        super().__init__()

        self.current_selectable_domain_descriptions = selectable_domain_descriptions

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        main_layout.addStretch(1)
        
        self.active_domain_label = QLabel(self.tr('Active domain'))
        self.active_domain_label.setFont(fonts.plain_font)
        main_layout.addWidget(self.active_domain_label)

        self.active_domain_combobox = QComboBox()
        self.active_domain_combobox.setFont(fonts.plain_font)
        self.active_domain_combobox.addItems(selectable_domain_descriptions)
        main_layout.addWidget(self.active_domain_combobox)

    def update_selectable_domain_descriptions(self, selectable_domain_descriptions):
        self.current_selectable_domain_descriptionst = selectable_domain_descriptions
        self.active_domain_combobox.clear()
        for description in selectable_domain_descriptions:
            self.active_domain_combobox.addItem(self.tr(description))
    
    def get_active_domain(self):
        active_domain_description = self.active_domain_combobox.currentText()
        return DomainType.from_description(active_domain_description)
        
    def retranslateUI(self):
        self.active_domain_label.setText(self.tr('Active domain'))
        self.active_domain_combobox.clear()
        for description in self.current_selectable_domain_descriptions:
            self.active_domain_combobox.addItem(self.tr(description))
