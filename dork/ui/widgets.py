from PyQt5.QtWidgets import (QLabel, QListWidgetItem, QWidget,  QPushButton,
                            QHBoxLayout, QMessageBox, QLineEdit, QFileDialog,
                            QSpacerItem, QSizePolicy)
from PyQt5.QtSvg import QSvgRenderer                            
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QColor, QPalette, QPixmap, QIcon, QFont
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

class WadListItem(QWidget):

    def __init__(self, wad, config):
        super().__init__()
        self.config = config
        self.wad = wad
        is_local_path = config.get_dork_path("resources/icons/user.svg")
        is_wad_path = config.get_dork_path("resources/icons/check.svg")
        is_fav_path = config.get_dork_path("resources/icons/star.svg")
        self.icon_index = {
            "local": {
                "tooltip": "Local Wad",
                "icon_path": is_local_path
            },
            "is_iwad": {
                "tooltip": "IWAD",
                "icon_path": is_wad_path
            },
            "favorite": {
                "tooltip": "Favorite Wad",
                "icon_path": is_fav_path
            },
        }
        
        self.wad_label = QLabel(wad.title, self)
        font = QFont("Garamond", 10)
        self.wad_label.setFont(font)
        
        widget_list = []
        for attr, details in self.icon_index.items():
            if getattr(self.wad, attr):
                label = QLabel(self)
                label.setToolTip(details["tooltip"])
                icon_pixmap = QPixmap(details["icon_path"])
                icon_pixmap = icon_pixmap.scaled(QSize(20, 20))
                label.setPixmap(icon_pixmap)
                widget_list.append(label)
            else:
                empty_label = QLabel(self)
                empty_label.setFixedSize(QSize(20, 20))
                widget_list.append(empty_label)

        layout = QHBoxLayout()
        
        for widget in widget_list:
            layout.addWidget(widget)
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)
        layout.addWidget(self.wad_label)
        self.setLayout(layout)
          
        
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