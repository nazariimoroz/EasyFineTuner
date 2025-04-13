from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from ACacheManager import ACacheManager

class AOptionsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        self.api_key = QLineEdit()
        form.addRow("Gemini API Key:", self.api_key)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        
        layout.addLayout(form)
        layout.addWidget(self.save_button)
        layout.addStretch()
        
        self.cache_manager = ACacheManager()
        self.load_settings()
        
    def load_settings(self):
        self.api_key.setText(self.cache_manager.get_api_key())
                
    def save_settings(self):
        self.cache_manager.set_api_key(self.api_key.text())
        QMessageBox.information(self, "Success", "Settings saved successfully\nRestart the application to apply changes")
