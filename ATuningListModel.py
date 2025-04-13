from PyQt6.QtCore import QModelIndex, QAbstractTableModel, Qt
from AGenaiManager import AGenaiManager, TuningWrapper


class ATuningListModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.genai_manager = AGenaiManager()
        self.tunings = []
        self.refresh_data()

    def refresh_data(self):
        self.beginResetModel()
        self.tunings = self.genai_manager.list_tunings()
        self.endResetModel()
        
    def delete_model(self, model_name):
        self.genai_manager.delete_model(model_name)
        self.refresh_data()
        
    def rowCount(self, parent=QModelIndex()):
        return len(self.tunings)
    
    def columnCount(self, parent=QModelIndex()):
        return 4
        
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
            
        if role == Qt.ItemDataRole.DisplayRole:
            wrapper = self.tunings[index.row()]
            if index.column() == 0:
                return wrapper.name
            elif index.column() == 1:
                return wrapper.state
            elif index.column() == 2:
                return str(wrapper.info)
            elif index.column() == 3:
                return str(wrapper.training_dataset_formatted)
        return None
        
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return ["Name", "State", "Model Info", "Training Data"][section]
        return None
    
