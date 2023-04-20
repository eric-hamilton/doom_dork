from PyQt5.QtWidgets import QLabel, QListWidgetItem, QWidget,  QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QSize, pyqtSignal


class AddItemWidget(QWidget):
    
    add_item = pyqtSignal()
    
    def __init__(self, button_text, parent=None):
        super().__init__(parent)
        
        # Create the button with the + sign
        self.add_item_button = QPushButton("+", self)
        self.add_item_button.setObjectName("addButton")
        self.add_item_button.setMinimumWidth(60)
        self.add_item_button.clicked.connect(self.on_add_item_clicked)

        self.add_item_label = QLabel(button_text, self)
        self.add_item_label.setObjectName("add_item_label")

        layout = QHBoxLayout()
        layout.addWidget(self.add_item_button)
        layout.addWidget(self.add_item_label)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.setLayout(layout)

        self.setStyleSheet("""
            #add_item_button {
                border: 2px solid #C8C8C8;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
                color: #ffb86c;
            }
            #add_item_button:hover {
                background-color: #282a36;
            }
        """)
        
    def on_add_item_clicked(self):
        self.add_item.emit()

class DividerWidgetItem(QListWidgetItem):
    def __init__(self):
        super().__init__()
        
        # set a smaller height for the divider item
        self.setSizeHint(QSize(0, 10)) 
        
        # make the item not selectable and not enabled
        self.setFlags(self.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled) 
   