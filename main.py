import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from AChatTab import AChatTab
from AFineTuneTab import AFineTuneTab
from AModelsTab import AModelsTab
from AOptionsTab import AOptionsTab
from ATuningListModel import ATuningListModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Easy Fine Tuner")
        self.setGeometry(100, 100, 800, 600)
        
        self.tuning_model = ATuningListModel()

        self.setup_dock()
        self.setup_tabs()
        
    def setup_dock(self):
        dock = QDockWidget("Tools", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        dock_content = QWidget()
        layout = QVBoxLayout(dock_content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        self.chat_button = QPushButton("Chat")
        self.chat_button.setCheckable(True)
        self.chat_button.setChecked(True)
        self.chat_button.clicked.connect(lambda: self.tabs.setCurrentIndex(0))
        layout.addWidget(self.chat_button)
        self.button_group.addButton(self.chat_button)

        self.fine_tune_button = QPushButton("Fine Tune")
        self.fine_tune_button.setCheckable(True)
        self.fine_tune_button.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        layout.addWidget(self.fine_tune_button)
        self.button_group.addButton(self.fine_tune_button)

        self.model_list_button = QPushButton("Model List")
        self.model_list_button.setCheckable(True)
        self.model_list_button.clicked.connect(lambda: self.tabs.setCurrentIndex(2))
        layout.addWidget(self.model_list_button)
        self.button_group.addButton(self.model_list_button)

        self.options_button = QPushButton("Options")
        self.options_button.setCheckable(True)
        self.options_button.clicked.connect(lambda: self.tabs.setCurrentIndex(3))
        layout.addWidget(self.options_button)
        self.button_group.addButton(self.options_button)

        layout.addStretch()
        
        dock.setWidget(dock_content)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()
        self.setCentralWidget(self.tabs)
        
        self.chat_tab = AChatTab(tuning_model=self.tuning_model)
        self.fine_tune_tab = AFineTuneTab()
        self.models_tab = AModelsTab(tuning_model=self.tuning_model)
        self.options_tab = AOptionsTab()
        
        self.tabs.addTab(self.chat_tab, "")
        self.tabs.addTab(self.fine_tune_tab, "")
        self.tabs.addTab(self.models_tab, "")
        self.tabs.addTab(self.options_tab, "")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


