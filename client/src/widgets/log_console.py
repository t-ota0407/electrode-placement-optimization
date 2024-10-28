import re
import uuid
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QCheckBox, QSpacerItem, QSizePolicy)

import fonts as fonts

class LogConsole(QWidget):

    href_key_to_function = {}

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        
        self.checkbox_layout = QHBoxLayout()

        self.error_checkbox = QCheckBox(self.tr("Error"))
        self.message_checkbox = QCheckBox(self.tr("Message"))

        self.error_checkbox.setFont(fonts.small_font)
        self.message_checkbox.setFont(fonts.small_font)
        
        self.error_checkbox.setChecked(True)
        self.message_checkbox.setChecked(True)
        
        self.error_checkbox.stateChanged.connect(self.update_log_display)
        self.message_checkbox.stateChanged.connect(self.update_log_display)
        
        checkbox_spacer = QSpacerItem(16, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.checkbox_layout.addWidget(self.error_checkbox)
        self.checkbox_layout.addItem(checkbox_spacer)
        self.checkbox_layout.addWidget(self.message_checkbox)
        self.checkbox_layout.addStretch(1)

        self.main_layout.addLayout(self.checkbox_layout)

        self.log_text_edit = LogTextEdit()
        self.main_layout.addWidget(self.log_text_edit)
        
        self.logs = {'error': [], 'message': []}
    
    def log(self, message, is_error=False, href_function=None):
        if href_function and callable(href_function):
            href_uuid_key = str(uuid.uuid4())
            href_added_message = f'<span>{message}<a style="color: pink" href="{href_uuid_key}">[View]</a></span>'
            LogConsole.href_key_to_function[href_uuid_key] = href_function
            self.logs[('error' if is_error else 'message')].append(href_added_message)
        else:
            self.logs[('error' if is_error else 'message')].append(message)
        self.update_log_display()
    
    def update_log_display(self):
        self.log_text_edit.clear()
        if self.error_checkbox.isChecked():
            for log in self.logs['error']:
                self.log_text_edit.append(f"<font color='red'>{log}</font>")
        if self.message_checkbox.isChecked():
            for log in self.logs['message']:
                self.log_text_edit.append(f"<font color='black'>{log}</font>")

        self.log_text_edit.moveCursor(self.log_text_edit.textCursor().End)
    
    def retranslateUI(self):
        self.error_checkbox.setText(self.tr('Error'))
        self.message_checkbox.setText(self.tr('Message'))

class LogTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

        self.setFont(fonts.small_font)
        self.setReadOnly(True)

    def mousePressEvent(self, e):
        self.selected_href_link = self.anchorAt(e.pos())

    def mouseReleaseEvent(self, e):
        if self.selected_href_link:
            href_value = self.selected_href_link
            href_function = LogConsole.href_key_to_function[href_value]
            href_function()
            self.selected_href_link = None
