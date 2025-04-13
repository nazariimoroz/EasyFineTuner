from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from ATuningListModel import ATuningListModel
from AGenaiManager import AGenaiManager


class AChatTab(QWidget):
    def __init__(self, tuning_model, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        splitter = QSplitter(Qt.Orientation.Vertical)
        self.user_input = QTextEdit()
        self.model_output = QTextEdit()
        self.model_output.setReadOnly(True)
        
        splitter.addWidget(self.user_input)
        splitter.addWidget(self.model_output)
        
        model_layout = QHBoxLayout()
        self.model_selector = QComboBox()
        self.tuning_model = tuning_model
        self.model_selector.setModel(self.tuning_model)
        
        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        self.refresh_button.setFixedSize(24, 24)
        self.refresh_button.clicked.connect(self.tuning_model.refresh_data)
        
        model_layout.addWidget(self.model_selector)
        model_layout.addWidget(self.refresh_button)
        model_layout.setSpacing(2)
        
        self.send_button = QPushButton("Send Request")
        self.send_button.clicked.connect(self.send_request)
        
        layout.addWidget(splitter)
        layout.addLayout(model_layout)
        layout.addWidget(self.send_button)

    def send_request(self):
        try:
            selected_index = self.model_selector.currentIndex()
            if selected_index < 0:
                QMessageBox.warning(self, "Warning", "Please select a model first")
                return
                
            model = self.tuning_model.tunings[selected_index].tuned_model.model
            content = self.user_input.toPlainText()
            
            if not content.strip():
                QMessageBox.warning(self, "Warning", "Please enter some text first")
                return
                
            genai_manager = AGenaiManager()
            response = genai_manager.generate_content(model=model, content=content)
            
            self.model_output.setText(response.text)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate response: {str(e)}")
