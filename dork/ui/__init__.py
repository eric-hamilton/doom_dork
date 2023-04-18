from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QGridLayout,
                        QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QFrame,
                        QSplitter, QSizePolicy, QPushButton, QAction, QDialog,
                        QStyleFactory, QHBoxLayout, QScrollBar, QComboBox,
                        QDialogButtonBox)
from PyQt5.QtCore import Qt, QSize, QUrl, QRect
from PyQt5.QtGui import QPixmap, QIcon, QDesktopServices, QPalette, QColor

from dork.ui.custom import DividerWidgetItem, AddWadsItemWidget
import qdarkstyle

     
class UI:
    def __init__(self, app):
        self.app = app
        self.q_app = QApplication([])
        self.main_window = MainWindow(self)

    def show_about_dialog(self):

        about_dialog = QDialog(self.main_window)
        about_dialog.setWindowTitle("About Doom Dork")
        about_dialog.setWindowFlags(about_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        about_label = QLabel()
        about_label.setText("Doom Dork - An Open-Source Doom Engine and Wad Manager<br><br>"
                            "Created By Eric Hamilton<br>"
                            "Github https://github.com/eric-hamilton/doom_dork<br><br>"
                            "Version 0.1<br><br>"
                            "Copyright (c) 2023")
        about_label.setOpenExternalLinks(True)
        about_label.linkActivated.connect(self.open_link)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(about_dialog.accept)

        layout = QVBoxLayout()
        layout.addWidget(about_label)
        layout.addWidget(button_box)

        about_dialog.setLayout(layout)

        about_dialog.exec_()
    
    def open_link(self, link):
        QDesktopServices.openUrl(QUrl(link))
        
    def launch_github(self):
        github_link = app.config.get(github_link)
        QDesktopServices.openUrl(QUrl(github_link))
        
    def launch(self):
        self.main_window.show()
        self.q_app.exec_()
        
        
class MainWindow(QMainWindow):
    def __init__(self, ui):
        self.ui = ui
        self.engines = {
            "DSDADoom": "",
            "GZDoom": "",
            "Chocolate Doom": "",
            "Brutal Doom": ""
        }
        self.engine_names = list(self.engines.keys())
        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet())

        self.setWindowTitle("Doom Dork")
        self.setWindowIcon(QIcon(self.ui.app.config.get_dork_path("resources/icons/dork_glasses.png")))
        self.setGeometry(300, 300, 450, 400)
        
        self.create_menu_bar()
        
        self.wad_label = QLabel("Wads", self)
        self.file_listbox = QListWidget(self)
        self.file_listbox.setFixedSize(200, 300)
        self.scrollbar = QScrollBar(Qt.Vertical, self.file_listbox)
        self.file_listbox.setVerticalScrollBar(self.scrollbar)
        
        add_wad_item = AddWadsItemWidget(self.file_listbox)
        add_item = QListWidgetItem(self.file_listbox)
        add_item.setSizeHint(add_wad_item.sizeHint())
        self.file_listbox.setItemWidget(add_item, add_wad_item)
        add_wad_item.add_wads.connect(self.on_add_wads_item_clicked)
        
        

        self.engine_label = QLabel("Engine", self)
        self.engine_var = QComboBox(self)
        self.engine_var.addItems(self.engine_names)

        self.search_button = QPushButton("Refresh Wads", self)

        self.run_button = QPushButton("Launch", self)
        
        self.run_button.clicked.connect(self.launch_wad)
        
        # Use the grid layout manager to arrange the widgets
        layout = QGridLayout()
        layout.addWidget(self.wad_label, 0, 1)
        layout.addWidget(self.search_button, 0, 2)
        layout.addWidget(self.file_listbox, 1, 1, 2, 2)
        layout.addWidget(self.engine_label, 3, 2)
        layout.addWidget(self.engine_var, 3, 3)
        
        layout.addWidget(self.run_button, 3, 4)

        # Add empty columns to the left and right of the listbox and scrollbar
        layout.setColumnMinimumWidth(0, 10)
        layout.setColumnMinimumWidth(5, 10)

        # Add a horizontal separator
        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator, 2, 1, 1, 4)

        self.wads = {}
        #self.load_wads()

        # Configure the grid to expand the file listbox vertically and horizontally
        layout.setRowStretch(0, 1)
        layout.setColumnStretch(1, 1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def launch_wad(self):
        selected_wad = self.file_listbox.currentRow()
        selected_engine = self.engine_var.currentIndex()
        
        print(selected_engine, selected_wad)
        index = self.file_listbox.currentRow()
        if index >=0:
            pass
        
    def load_wads(self):
        self.file_listbox.clear()
        return
        self.wad_dict = self.ui.app.dork.get_wads_in_folder("p")
        
        for wad_name in self.wad_dict:
            post_list_item = QListWidgetItem(wad_name)
            self.file_listbox.addItem(post_list_item) 
        divider_item = DividerWidgetItem()
        self.file_listbox.addItem(divider_item)
    
    def on_add_wads_item_clicked(self):
        print("caught")
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File
        file_menu = menubar.addMenu('File')
        
        prefs_action = QAction('Preferences', self)
        file_menu.addAction(prefs_action)

        quit_action = QAction('Exit', self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Engines
        engine_menu = menubar.addMenu('Engines')
        manage_engines_action = QAction("Manage Engines", self)
        engine_menu.addAction(manage_engines_action)

        # Wads
        wads_menu = menubar.addMenu('Wads')
        manage_wads_action = QAction("Manage Wads", self)
        wads_menu.addAction(manage_wads_action)
        

        # Help
        help_menu = menubar.addMenu('Help')
        
        help_action = QAction('Help', self)
        help_icon = QIcon(self.ui.app.config.get_dork_path("resources/icons/external_link.svg"))
        help_action.setIcon(help_icon)
        help_action.triggered.connect(self.ui.launch_github)
        help_menu.addAction(help_action)
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.ui.show_about_dialog)
        help_menu.addAction(about_action)