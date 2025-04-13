from PyQt6.QtWidgets import *
from AGenaiManager import AGenaiManager
from google.genai import types
from PyQt6.QtCore import Qt
import json
from AJsonHighlighter import AJsonHighlighter


class AFineTuneTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        splitter_container = QWidget()
        splitter_layout = QHBoxLayout(splitter_container)
        splitter_layout.setContentsMargins(0, 0, 0, 0)
        
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.training_data = QTextEdit()
        self.highlighter = AJsonHighlighter(self.training_data.document())
        
        default_data = [
                ["1", "2"],
                ["3", "4"],
                ["-3", "-2"],
                ["twenty two", "twenty three"],
                ["two hundred", "two hundred one"],
                ["ninety nine", "one hundred"],
                ["8", "9"],
                ["-98", "-97"],
                ["1,000", "1,001"],
                ["10,100,000", "10,100,001"],
                ["thirteen", "fourteen"],
                ["eighty", "eighty one"],
                ["one", "two"],
                ["three", "four"],
                ["seven", "eight"],
        ]
        self.training_data.setText(json.dumps(default_data, indent=2))
        left_layout.addWidget(self.training_data)
        
        right_widget = QWidget()
        right_layout = QFormLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.base_model = QLineEdit('models/gemini-1.5-flash-001-tuning')
        self.tuned_model_name = QLineEdit('test tuned model')
        self.epoch_count = QSpinBox()
        self.epoch_count.setValue(5)
        self.epoch_count.setRange(1, 100)
        self.batch_size = QSpinBox()
        self.batch_size.setValue(4)
        self.batch_size.setRange(1, 100)
        self.learning_rate = QDoubleSpinBox()
        self.learning_rate.setDecimals(4)
        self.learning_rate.setValue(0.001)
        self.learning_rate.setRange(0.0001, 1.0)
        self.learning_rate.setSingleStep(0.001)
        
        right_layout.addRow("Base Model:", self.base_model)
        right_layout.addRow("Model Name:", self.tuned_model_name)
        right_layout.addRow("Epoch Count:", self.epoch_count)
        right_layout.addRow("Batch Size:", self.batch_size)
        right_layout.addRow("Learning Rate:", self.learning_rate)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        
        splitter_layout.addWidget(splitter)
        
        self.fine_tune_button = QPushButton("Fine Tune New Model")
        self.fine_tune_button.clicked.connect(self.create_fine_tune)
        
        layout.addWidget(splitter_container)
        layout.addWidget(self.fine_tune_button)
        
    def create_fine_tune(self):
        try:
            training_data = json.loads(self.training_data.toPlainText())
            
            training_dataset = types.TuningDataset(
                examples=[
                    types.TuningExample(
                        text_input=i,
                        output=o,
                    )
                    for i, o in training_data
                ]
            )
            
            tuning_config = types.CreateTuningJobConfig(
                epoch_count=self.epoch_count.value(),
                batch_size=self.batch_size.value(),
                learning_rate=self.learning_rate.value(),
                tuned_model_display_name=self.tuned_model_name.text()
            )
            
            genai_manager = AGenaiManager()
            tuning_job = genai_manager.create_tuning(
                base_model=self.base_model.text(),
                training_dataset=training_dataset,
                config=tuning_config
            )
            
            QMessageBox.information(
                self,
                "Success",
                f"Fine-tuning job started successfully.\nJob name: {tuning_job.name}"
            )
            
        except json.JSONDecodeError:
            QMessageBox.critical(
                self,
                "Error",
                "Invalid JSON format. Please check your input."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to create fine-tuning job: {str(e)}"
            )
