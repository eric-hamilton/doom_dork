from PyQt5.QtWidgets import QLabel, QListWidgetItem, QWidget,  QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QSize, pyqtSignal


class AddWadsItemWidget(QWidget):
    
    add_wads = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the button with the + sign
        self.add_wad_button = QPushButton("+", self)
        self.add_wad_button.setObjectName("addButton")
        self.add_wad_button.setMinimumWidth(60)
        self.add_wad_button.clicked.connect(self.on_add_wads_clicked)

        self.add_wad_label = QLabel("Add Wads", self)
        self.add_wad_label.setObjectName("add_wad_label")

        layout = QHBoxLayout()
        layout.addWidget(self.add_wad_button)
        layout.addWidget(self.add_wad_label)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.setLayout(layout)

        self.setStyleSheet("""
            #add_wad_button {
                border: 2px solid #C8C8C8;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
                color: #ffb86c;
            }
            #add_wad_button:hover {
                background-color: #282a36;
            }
        """)
        
    def on_add_wads_clicked(self):
        self.add_wads.emit()

class DividerWidgetItem(QListWidgetItem):
    def __init__(self):
        super().__init__()
        
        # set a smaller height for the divider item
        self.setSizeHint(QSize(0, 10)) 
        
        # make the item not selectable and not enabled
        self.setFlags(self.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled) 
   