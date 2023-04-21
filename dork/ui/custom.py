from PyQt5.QtWidgets import (QLabel, QListWidgetItem, QWidget,  QPushButton,
                            QHBoxLayout, QMessageBox, QLineEdit, QFileDialog)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
import qdarkstyle

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
        

        self.setSizeHint(QSize(0, 5)) 
        
        self.setFlags(self.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled) 
        self.setBackground(QColor('#282a36'))

class YesNoMessageBox(QMessageBox):
    yes_signal = pyqtSignal()
    no_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.setText(message)
        self.setWindowTitle(title)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.No)
        response = self.exec_()
        if response == QMessageBox.Yes:
            self.yes_signal.emit()
        else:
            self.no_signal.emit()
            
class NoValidIWadMessage(QMessageBox):

    def __init__(self):
        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.setText("Couldn't find a valid IWAD. Please select at least one.")
        self.setWindowTitle("No IWADs")
        self.setStandardButtons(QMessageBox.Close)

        # Add custom button
        self.custom_button = QPushButton("Open IWADs Menu")
        self.addButton(self.custom_button, QMessageBox.ActionRole)


class FileBrowseEdit(QWidget):
    
    path_selected = pyqtSignal(str)
    
    def __init__(self, parser, default_path=None, parent=None):
        super().__init__(parent)
        self.parser = parser
        self.default_path = default_path
        # Create the line edit widget
        self.edit = QLineEdit(self)
        self.edit.setReadOnly(True)
        if self.default_path:
            self.edit.setText(self.default_path)
        
        # Create the browse button widget
        self.browse_btn = QPushButton("...", self)
        self.browse_btn.setMaximumWidth(30)
        
        # Connect the button click event to open the file dialog
        self.browse_btn.clicked.connect(self.browse_for_file)
        
        # Add the line edit and button widgets to a horizontal layout
        layout = QHBoxLayout(self)
        layout.addWidget(self.edit)
        layout.addWidget(self.browse_btn)
        
    def browse_for_file(self):
        if self.default_path:
            directory = self.default_path
        else:
            directory = self.parser.get("DATA", "last_directory")
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose IWAD File", directory, "WAD Files (*.wad)")
        if file_path:
            self.edit.setText(file_path)
            self.path_selected.emit(file_path)