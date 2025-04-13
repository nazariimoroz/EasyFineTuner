import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from ATuningListModel import ATuningListModel

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from ATuningListModel import ATuningListModel

class AModelsTab(QWidget):
    def __init__(self, tuning_model, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        refresh_layout = QHBoxLayout()
        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        self.refresh_button.setFixedSize(24, 24)
        refresh_layout.addStretch()
        refresh_layout.addWidget(self.refresh_button)
        
        self.models_table = QTableView()
        self.tuning_model = tuning_model
        self.models_table.setModel(self.tuning_model)
        self.models_table.horizontalHeader().setStretchLastSection(False)
        self.models_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.models_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        
        self.models_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.models_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.models_table.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.models_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.refresh_button.clicked.connect(self.tuning_model.refresh_data)
        self.models_table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        left_layout.addLayout(refresh_layout)
        left_layout.addWidget(self.models_table)
        
        self.dataset_view = QTextEdit()
        self.dataset_view.setReadOnly(True)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(self.dataset_view)
        
        splitter.setSizes([self.width() // 2, self.width() // 2])
        
        layout.addWidget(splitter)
        layout.setContentsMargins(0, 0, 0, 0)

        self.models_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.models_table.customContextMenuRequested.connect(self.show_context_menu)

    def on_selection_changed(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            selected_row = indexes[0].row()
            tuning = self.tuning_model.tunings[selected_row]
            #self.dataset_view.setText(str(tuning.training_dataset))

    def show_context_menu(self, position):
        indexes = self.models_table.selectedIndexes()
        if not indexes:
            return
            
        menu = QMenu()
        delete_action = menu.addAction("Delete fine-tune")
        action = menu.exec(self.models_table.viewport().mapToGlobal(position))
        
        if action == delete_action:
            selected_row = indexes[0].row()
            tuning = self.tuning_model.tunings[selected_row]
            self.tuning_model.delete_model(tuning.tuned_model.model)
            self.tuning_model.refresh_data()
        
