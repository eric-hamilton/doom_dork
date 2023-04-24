from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QGridLayout,
                        QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QFrame,
                        QSplitter, QSizePolicy, QPushButton, QAction, QDialog,
                        QStyleFactory, QHBoxLayout, QScrollBar, QComboBox,
                        QDialogButtonBox, QStackedWidget, QCheckBox, QFileDialog,
                        QLineEdit, QMessageBox, QMenu, QAbstractItemView,
                        QRadioButton)
                        
from PyQt5.QtCore import Qt, QSize, QUrl, QRect
from PyQt5.QtGui import QPixmap, QIcon, QDesktopServices, QPalette, QColor

import dork.web.doomworld as doomworld_scripts
from dork.ui.widgets import (DividerWidgetItem, AddItemWidget, NoValidIWadMessage,
                        FileBrowseEdit, WadListItem)
from dork.config import warnings
import os
import qdarkstyle


     
class UI:
    def __init__(self, app):
        self.app = app
        self.dork = app.dork
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
        QDesktopServices.openUrl(QUrl("https://github.com/eric-hamilton/doom_dork/issues"))
        
    def launch(self):
        self.main_window.show()
        
        for warning in warnings:
            if warning == "no_valid_iwads":
                msg_box = NoValidIWadMessage()
                response = msg_box.exec_()
                if response == QMessageBox.Close:
                    pass
                else:
                    self.main_window.open_iwad_window()
        
        self.q_app.exec_()
        
    def handle_signal(self, signal):
        if signal == "engine_commit":
            if self.main_window.engine_window:
                self.main_window.engine_window.load_engines()
            self.main_window.load_engines()
                
        if signal == "wad_commit":
            if self.main_window.wad_window:
                self.main_window.wad_window.load_wads()
            
    def show_message(self, message, title, yes_signal, no_signal):
        msg_box = QMessageBox()
        msg_box.setStyleSheet(qdarkstyle.load_stylesheet())
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        response = msg_box.exec_()
        if response == QMessageBox.Yes:
            self.handle_signal(yes_signal)
        else:
            self.handle_signal(no_signal)

class IWadWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parser = parent.ui.app.config.parser
        self.setWindowTitle("IWADs")
        self.setGeometry(parent.geometry().x() + 50, parent.geometry().y() + 50, 400, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        iwad_label = QLabel("IWADs (Internal WADs) are not included with the game and are required to play mods. These files cannot be distributed due to copyright restrictions. Please make sure to provide your own IWAD files.")
        iwad_label.setWordWrap(True)
        iwad_label.setFixedHeight(60)

        
        
        doom_label = QLabel("DOOM.WAD")
        doom_path = parent.ui.app.dork.get_verified_iwad_path("doom")
        doom_path_edit = FileBrowseEdit(self.parser, doom_path, self)
        doom_path_edit.path_selected.connect(lambda path: self.iwad_path_selected(path, "doom"))
        
        doom_2_label = QLabel("DOOM2.WAD")
        doom_2_path = parent.ui.app.dork.get_verified_iwad_path("doom2")
        doom_2_path_edit = FileBrowseEdit(self.parser, doom_2_path, self)
        doom_2_path_edit.path_selected.connect(lambda path: self.iwad_path_selected(path, "doom2"))
        
        hexen_label = QLabel("HEXEN.WAD")
        hexen_path = parent.ui.app.dork.get_verified_iwad_path("hexen")
        hexen_path_edit = FileBrowseEdit(self.parser, hexen_path, self)
        hexen_path_edit.path_selected.connect(lambda path: self.iwad_path_selected(path, "hexen"))
        
        heretic_label = QLabel("HERETIC.WAD")
        heretic_path = parent.ui.app.dork.get_verified_iwad_path("heretic")
        heretic_path_edit = FileBrowseEdit(self.parser,heretic_path, self)
        heretic_path_edit.path_selected.connect(lambda path: self.iwad_path_selected(path, "heretic"))
        
        strife_label = QLabel("STRIFE1.WAD")
        strife_path = parent.ui.app.dork.get_verified_iwad_path("strife")
        strife_path_edit = FileBrowseEdit(self.parser, strife_path, self)
        strife_path_edit.path_selected.connect(lambda path: self.iwad_path_selected(path, "strife"))
        
        strife_voices_label = QLabel("VOICES.WAD (for Strife)")
        strife_voices_path = parent.ui.app.dork.get_verified_iwad_path("strife_voices")
        strife_voices_path_edit = FileBrowseEdit(self.parser,strife_voices_path,  self)
        strife_voices_path_edit.path_selected.connect(lambda path: self.iwad_path_selected(path, "strife_voices"))
        
        finish_button= QPushButton("Finished")
        finish_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        finish_button.setFixedHeight(40) 
        finish_button.setFixedWidth(300)
        finish_button.clicked.connect(self.close)
        
        layout = QGridLayout()
        
        layout.addWidget(iwad_label, 0, 0, 2, 2)
        layout.addWidget(doom_label, 2, 0)
        layout.addWidget(doom_path_edit, 2, 1)
        layout.addWidget(doom_2_label, 3, 0)
        layout.addWidget(doom_2_path_edit, 3, 1)
        layout.addWidget(hexen_label, 4, 0)
        layout.addWidget(hexen_path_edit, 4, 1)
        layout.addWidget(heretic_label, 5, 0)
        layout.addWidget(heretic_path_edit, 5, 1)
        layout.addWidget(strife_label, 6, 0)
        layout.addWidget(strife_path_edit, 6, 1)
        layout.addWidget(strife_voices_label, 7, 0)
        layout.addWidget(strife_voices_path_edit, 7, 1)
        layout.addWidget(finish_button, 8, 0, 2, 2, alignment=Qt.AlignCenter)


        self.setLayout(layout)
    
    def iwad_path_selected(self, file_path, iwad):
        self.parser.set("IWADS",iwad,file_path)
        folder = os.path.dirname(file_path)
        self.parser.set("DATA","last_directory",folder)
        
class EngineWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Engine Manager")

        #self.setGeometry(400, 400, 200, 200)
        self.setGeometry(parent.geometry().x() + 50, parent.geometry().y() + 50, 400, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        browse_button= QPushButton("Browse Online Engines")
        
        installed_engine_label = QLabel('Installed Engines')
        installed_engine_listbox = QListWidget()
        local_engine_label = QLabel('Local Engines')
        self.local_engine_listbox = QListWidget()
        add_local_engine_button = QPushButton('Add Engine')
        add_local_engine_button.clicked.connect(parent.add_engine)
        
        use_steam_checkbox = QCheckBox("Use Steam Folder")
        
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)
        
        
        layout = QGridLayout()
        
        layout.addWidget(browse_button, 0, 0, 1, 2)
        layout.addWidget(installed_engine_label, 1, 0, alignment=Qt.AlignCenter)
        layout.addWidget(installed_engine_listbox, 2, 0)
        layout.addWidget(local_engine_label, 1, 1, alignment=Qt.AlignCenter)
        layout.addWidget(self.local_engine_listbox, 2, 1)
        layout.addWidget(add_local_engine_button,3, 1)
        layout.addWidget(use_steam_checkbox,4,1, alignment=Qt.AlignRight)
        layout.addWidget(close_button, 5, 0, 1, 2)
        self.setLayout(layout)
        self.load_engines()
        
    def load_engines(self):
        self.local_engine_listbox.clear()
        local_engines = self.parent().ui.app.dork.get_local_engines()
        for engine in local_engines:
            engine_item = QListWidgetItem(engine.title)
            self.local_engine_listbox.addItem(engine_item) 
        

class DownloadWadWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Download WADs")
        self.dork = parent.ui.app.dork
        # search [filename, author, email, title, description, credits, editors, whole textfile]
        # sort by [date, filename, title, author, size, rating]
        # descending, ascending
       
        self.wad_listing_index = {}
        self.setGeometry(parent.geometry().x() + 100, parent.geometry().y() + 100, 400, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        title_label = QLabel("Search Doomworld WADs")
        query_label = QLabel("Search Query:")
        self.search_edit = QLineEdit()
        self.search_edit.returnPressed.connect(self.search)
        
        search_label = QLabel("Search:")
        self.search_combo = QComboBox()
        self.search_combo.addItem("Filename")
        self.search_combo.addItem("Author")
        self.search_combo.addItem("E-Mail")
        self.search_combo.addItem("Title")
        self.search_combo.addItem("Description")
        self.search_combo.addItem("Credits")
        self.search_combo.addItem("Editors")
        self.search_combo.addItem("Whole Textfile")
        #self.search_combo.currentIndexChanged.connect(self.search)
        
        

        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("Date")
        self.sort_combo.addItem("Filename")
        self.sort_combo.addItem("Title")
        self.sort_combo.addItem("Author")
        self.sort_combo.addItem("Size")
        self.sort_combo.addItem("Rating")
        #self.sort_combo.currentIndexChanged.connect(self.search)
        
        self.asc_desc_combo = QComboBox()
        self.asc_desc_combo.addItem("Ascending")
        self.asc_desc_combo.addItem("Descending")
        
        
        count_label = QLabel("Count")
        self.count_combo = QComboBox()
        self.count_combo.addItem("5")
        self.count_combo.addItem("10")
        self.count_combo.addItem("25")
        self.count_combo.addItem("50")
        self.count_combo.addItem("100")
        self.count_combo.addItem("200")
        
        check_layout = QHBoxLayout()
        options = ["Doom", "Doom2", "Hexen", "Heretic", "Strife"]
        for option in options:
            checkbox = QCheckBox(option)
            check_layout.addWidget(checkbox)


        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)

        self.results_listbox = QListWidget()
        self.result_context_menu = QMenu()
        
        view_wad_info_action = QAction("View WAD Info", self)
        view_wad_info_action.triggered.connect(self.open_view_wad_window)
        self.result_context_menu.addAction(view_wad_info_action)
        
        download_wad_action = QAction("Download WAD", self)
        download_wad_action.triggered.connect(self.handle_download_wad)
        self.result_context_menu.addAction(download_wad_action)
        
        open_doomworld_page_action = QAction("View on Doomworld", self)
        open_doomworld_page_action.triggered.connect(self.open_doomworld_page)
        self.result_context_menu.addAction(open_doomworld_page_action)
        
        self.results_listbox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.results_listbox.customContextMenuRequested.connect(self.show_result_context_menu)
        self.results_listbox.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.results_listbox.itemDoubleClicked.connect(self.open_view_wad_window)


        search_layout = QHBoxLayout()
        search_layout.addWidget(query_label)
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(search_button)

        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_combo)
        filter_layout.addWidget(sort_label)
        filter_layout.addWidget(self.sort_combo)
        filter_layout.addWidget(self.asc_desc_combo)
        filter_layout.addWidget(count_label)
        filter_layout.addWidget(self.count_combo)
        
        
        separator_layout = QHBoxLayout()
        left_separator = QFrame(self)
        left_separator.setFrameShape(QFrame.HLine)
        left_separator.setFrameShadow(QFrame.Sunken)
        or_label = QLabel("or")
        or_label.setContentsMargins(0, 0, 0, 0)
        right_separator = QFrame(self)
        right_separator.setFrameShape(QFrame.HLine)
        right_separator.setFrameShadow(QFrame.Sunken)
        separator_layout.addWidget(left_separator)
        separator_layout.addWidget(or_label, alignment=Qt.AlignCenter)
        separator_layout.addWidget(right_separator)
        
        
        fun_layout = QHBoxLayout()
        
        newest_wads_button = QPushButton("Get Newest WADs")
        newest_wads_button.clicked.connect(lambda: self.search("new"))
        random_wads_button = QPushButton("Get Random WADs")
        random_wads_button.clicked.connect(lambda: self.search("random"))
        
        fun_layout.addWidget(newest_wads_button)
        fun_layout.addWidget(random_wads_button)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(filter_layout)
        main_layout.addLayout(check_layout)
        main_layout.addLayout(separator_layout)
        main_layout.addLayout(fun_layout)
        main_layout.addWidget(self.results_listbox)

        self.setLayout(main_layout)
        
    def search(self, query_string=None):
        self.results_listbox.clear()
        if query_string:
            if query_string == "random":
                random_wads = doomworld_scripts.get_random_wads(["doom"])
                print(len(random_wads))
                for x in range(len(random_wads)):
                    wad = random_wads[x]
                    wad_info = f"{wad.title} by {wad.author} - {wad.size}"
                    wad_item = QListWidgetItem(wad_info)
                    self.results_listbox.addItem(wad_item)
                    self.wad_listing_index[x] = wad
                return
            elif query_string == "new":
                return
        
        query = self.search_edit.text()
        search_option = self.search_combo.currentText()
        sort_option = self.sort_combo.currentText()
        asc_desc = self.asc_desc_combo.currentText()

        # TODO: Implement search function based on query and filter option

        self.results_listbox.clear()
    
    def show_result_context_menu(self, pos):
        selected_wad_index = self.results_listbox.currentRow()
        if selected_wad_index >=0:
            global_pos = self.results_listbox.mapToGlobal(pos)
            self.result_context_menu.exec(global_pos)
            
    def handle_download_wad(self):
        selected_wad_index = self.results_listbox.currentRow()
        if selected_wad_index >=0:
            wad_listing = self.wad_listing_index[selected_wad_index]
            self.dork.download_wad_from_url(wad_listing.link)
        
    def open_doomworld_page(self):
        selected_wad_index = self.results_listbox.currentRow()
        if selected_wad_index >=0:
            wad_listing = self.wad_listing_index[selected_wad_index]
            QDesktopServices.openUrl(QUrl(wad_listing.link))
    
    def open_view_wad_window(self):
        selected_wad_index = self.results_listbox.currentRow()
        if selected_wad_index >=0:
            wad_listing = self.wad_listing_index[selected_wad_index]
            
            
        
class NewEngineWindow(QDialog):  
    def __init__(self, engine_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Engine")
        self.setGeometry(parent.geometry().x() + 50, parent.geometry().y() + 50, 400, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.engine_path = engine_path
        engine_filename = os.path.basename(engine_path)
        new_engine_label = QLabel(f'Add Engine Details for {engine_filename}')
        
        title_label = QLabel('Title')
        self.title_input = QLineEdit()
        
        description_label = QLabel('Description')
        self.description_input = QLineEdit()
        
        version_label = QLabel('Version')
        self.version_input = QLineEdit()
        
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.close)
        save_button = QPushButton('Save')
        save_button.clicked.connect(lambda: parent.save_engine(self))
        
        
        layout = QGridLayout()
        
        layout.addWidget(new_engine_label, 0, 0, 1, 2)
        layout.addWidget(title_label, 1, 0)
        layout.addWidget(self.title_input, 1, 1)
        layout.addWidget(description_label, 2, 0)
        layout.addWidget(self.description_input, 2, 1)
        layout.addWidget(version_label, 3, 0)
        layout.addWidget(self.version_input, 3, 1)
        layout.addWidget(cancel_button, 4, 0)
        layout.addWidget(save_button, 4, 1)
        
        self.setLayout(layout)
        
class EditWadWindow(QDialog):
    def __init__(self, wad_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit WAD")
        self.setGeometry(parent.geometry().x() + 50, parent.geometry().y() + 50, 400, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        wad = self.parent().ui.app.dork.get_wad(wad_id)
        edit_wad_label = QLabel(f'Add WAD Details for {wad.title}')
        
        title_label = QLabel('Title')
        self.title_input = QLineEdit()
        self.title_input.setText(wad.title)
        
        description_label = QLabel('Description')
        self.description_input = QLineEdit()
        self.description_input.setText(wad.description)
        
        author_label = QLabel('Author')
        self.author_input = QLineEdit()
        self.author_input.setText(wad.author)
        
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.close)
        save_button = QPushButton('Save')
        save_button.clicked.connect(lambda: parent.update_wad(self, wad_id))
        
        
        layout = QGridLayout()
        
        layout.addWidget(edit_wad_label, 0, 0, 1, 2)
        layout.addWidget(title_label, 1, 0)
        layout.addWidget(self.title_input, 1, 1)
        layout.addWidget(description_label, 2, 0)
        layout.addWidget(self.description_input, 2, 1)
        layout.addWidget(author_label, 3, 0)
        layout.addWidget(self.author_input, 3, 1)
        layout.addWidget(cancel_button, 4, 0)
        layout.addWidget(save_button, 4, 1)
        
        self.setLayout(layout)
        
        
class EditEngineWindow(QDialog):  
    def __init__(self, engine_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Engine")
        self.setGeometry(parent.geometry().x() + 50, parent.geometry().y() + 50, 400, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        engine = self.parent().ui.app.dork.get_engine(engine_id)
        new_engine_label = QLabel(f'Add Engine Details for {engine.title}')
        
        title_label = QLabel('Title')
        self.title_input = QLineEdit()
        self.title_input.setText(engine.title)
        
        description_label = QLabel('Description')
        self.description_input = QLineEdit()
        self.description_input.setText(engine.description)
        
        version_label = QLabel('Version')
        self.version_input = QLineEdit()
        self.version_input.setText(engine.version)
        
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.close)
        save_button = QPushButton('Save')
        save_button.clicked.connect(lambda: parent.update_engine(self, engine_id))
        
        
        layout = QGridLayout()
        
        layout.addWidget(new_engine_label, 0, 0, 1, 2)
        layout.addWidget(title_label, 1, 0)
        layout.addWidget(self.title_input, 1, 1)
        layout.addWidget(description_label, 2, 0)
        layout.addWidget(self.description_input, 2, 1)
        layout.addWidget(version_label, 3, 0)
        layout.addWidget(self.version_input, 3, 1)
        layout.addWidget(cancel_button, 4, 0)
        layout.addWidget(save_button, 4, 1)
        
        self.setLayout(layout)
    
class WadWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wad Manager")
        self.setGeometry(parent.geometry().x() + 50, parent.geometry().y() + 50, 400, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        browse_button= QPushButton("Browse Online Wads")

        browse_button.clicked.connect(parent.open_download_wad_window)
        

        installed_wad_label = QLabel('Installed Wads')
        installed_wad_listbox = QListWidget()
        local_wad_label = QLabel('Local Wads')
        self.local_wad_listbox = QListWidget()
        add_local_folder_button = QPushButton('Add Wads')
        add_local_folder_button.clicked.connect(parent.add_wad_folder)
        
        use_steam_checkbox = QCheckBox("Use Steam Folder")
        
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)
        
        
        layout = QGridLayout()
        
        layout.addWidget(browse_button, 0, 0, 1, 2)
        layout.addWidget(installed_wad_label, 1, 0, alignment=Qt.AlignCenter)
        layout.addWidget(installed_wad_listbox, 2, 0)
        layout.addWidget(local_wad_label, 1, 1, alignment=Qt.AlignCenter)
        layout.addWidget(self.local_wad_listbox, 2, 1)
        layout.addWidget(add_local_folder_button,3, 1)
        layout.addWidget(use_steam_checkbox,4,1, alignment=Qt.AlignRight)
        layout.addWidget(close_button, 5, 0, 1, 2)
        self.setLayout(layout)
        self.load_wads()
        
    def load_wads(self):
        self.local_wad_listbox.clear()
        local_wads = self.parent().ui.app.dork.get_local_wads()
        for wad in local_wads:
            wad_item = QListWidgetItem(wad.title)
            self.local_wad_listbox.addItem(wad_item) 

class MainWindow(QMainWindow):
    def __init__(self, ui):
        self.ui = ui
        self.parser = ui.app.config.parser
        self.last_local_folder=self.parser.get("DATA", "last_directory")
        self.wad_index = {}                      # {int>row_index : int>wad_id}
        self.engine_index = {}                   # {int>row_index : int>engine_id}
        self.iwad_index = {}                     # {int>combobox_index : int>iwad_name}
        
        self.engine_window = None
        self.wad_window = None
        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet())

        self.setWindowTitle("Doom Dork")
        self.setWindowIcon(QIcon(self.ui.app.config.get_dork_path("resources/icons/dork_glasses.png")))
        self.setGeometry(300, 300, 450, 400)
        
        self.create_menu_bar()
        
        self.wad_label = QLabel("Wads", self)
        self.wad_listbox = QListWidget(self)
        self.wad_listbox.setFixedSize(300, 300)
        self.wad_scrollbar = QScrollBar(Qt.Vertical, self.wad_listbox)
        self.wad_listbox.setVerticalScrollBar(self.wad_scrollbar)
        
        add_wad_item = AddItemWidget("Add Wads", self.wad_listbox)
        add_item = QListWidgetItem(self.wad_listbox)
        add_item.setSizeHint(add_wad_item.sizeHint())
        self.wad_listbox.setItemWidget(add_item, add_wad_item)
        add_wad_item.add_item.connect(self.on_add_wads_item_clicked)
        
        
        self.wad_context_menu = QMenu()
        
        view_wad_info_action = QAction("View WAD Info", self)
        view_wad_info_action.triggered.connect(self.open_edit_wad_menu)
        self.wad_context_menu.addAction(view_wad_info_action)
        
        edit_wad_action = QAction("Edit WAD", self)
        edit_wad_action.triggered.connect(self.open_edit_wad_menu)
        self.wad_context_menu.addAction(edit_wad_action)
        
        open_wad_folder_action = QAction("Open Folder", self)
        open_wad_folder_action.triggered.connect(self.open_wad_folder)
        
        self.wad_context_menu.addAction(open_wad_folder_action)
        self.wad_listbox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.wad_listbox.customContextMenuRequested.connect(self.show_wad_context_menu)
        self.wad_listbox.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.wad_listbox.itemDoubleClicked.connect(self.open_edit_wad_menu)
        
        
        self.engine_label = QLabel("Engines", self)
        self.engine_listbox = QListWidget(self)
        self.engine_listbox.setFixedSize(200, 300)
        self.engine_scrollbar = QScrollBar(Qt.Vertical, self.engine_listbox)
        self.engine_listbox.setVerticalScrollBar(self.engine_scrollbar)
        self.engine_listbox.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.engine_listbox.itemDoubleClicked.connect(self.open_edit_engine_window)
        
        
        add_engine_item = AddItemWidget("Add Engines", self.engine_listbox)
        add_item = QListWidgetItem(self.engine_listbox)
        add_item.setSizeHint(add_engine_item.sizeHint())
        self.engine_listbox.setItemWidget(add_item, add_engine_item)
        add_engine_item.add_item.connect(self.on_add_engines_item_clicked)
        
        self.engine_context_menu = QMenu()
        edit_engine_action = QAction("Edit Engine", self)
        edit_engine_action.triggered.connect(self.open_edit_engine_window)
        self.engine_context_menu.addAction(edit_engine_action)
        
        open_engine_folder_action = QAction("Open Folder", self)
        open_engine_folder_action.triggered.connect(self.open_engine_folder)
        
        self.engine_context_menu.addAction(open_engine_folder_action)
        self.engine_listbox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.engine_listbox.customContextMenuRequested.connect(self.show_engine_context_menu)
        
        self.iwad_label = QLabel("IWAD", self)
        self.iwad_combobox = QComboBox(self)
        iwads = self.ui.app.dork.get_iwads()
        for x in range(len(iwads)):
            self.iwad_index[x]=iwads[x]
        self.iwad_combobox.addItems(iwads)


        self.run_button = QPushButton("Launch", self)
        self.run_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.run_button.setFixedHeight(40) 
        #self.run_button.setFixedWidth(300)
        
        self.run_button.clicked.connect(self.launch_wad)
        
        # Use the grid layout manager to arrange the widgets
        layout = QGridLayout()
        layout.addWidget(self.wad_label, 0, 1)
        layout.addWidget(self.wad_listbox, 1, 0, 2, 2)
        layout.addWidget(self.engine_listbox, 1, 2, 2, 2)
        layout.addWidget(self.engine_label, 0, 2)
        
        layout.addWidget(self.iwad_label, 3, 0)
        layout.addWidget(self.iwad_combobox, 3, 1)
        layout.addWidget(self.run_button, 3, 2)

        # Add empty columns to the left and right of the listbox and scrollbar
        layout.setColumnMinimumWidth(0, 10)
        layout.setColumnMinimumWidth(5, 10)

        # Add a horizontal separator
        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator, 2, 1, 1, 4)

        self.wads = {}
        self.load_wads()
        self.load_engines()
        self.set_defaults()

        # Configure the grid to expand the file listbox vertically and horizontally
        layout.setRowStretch(0, 1)
        layout.setColumnStretch(1, 1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def launch_wad(self):
        selected_engine_index = self.engine_listbox.currentRow()
        selected_wad_index = self.wad_listbox.currentRow()
        selected_iwad = self.iwad_combobox.currentText()
        if selected_engine_index >=0:
            if selected_wad_index >=0:
                engine_id = self.engine_index[selected_engine_index]
                wad_id = self.wad_index[selected_wad_index]
                self.ui.app.dork.run_selected(engine_id, wad_id, selected_iwad)
        
    def set_defaults(self):
        last_wad = self.parser.getint("DATA", "last_wad")
        last_engine = self.parser.getint("DATA", "last_engine")
        last_iwad = self.parser.get("DATA", "last_iwad")
        
        if last_wad:
            row = list(self.wad_index.keys())[list(self.wad_index.values()).index(last_wad)]
            self.wad_listbox.setCurrentRow(row)
        
        if last_engine:
            row = list(self.engine_index.keys())[list(self.engine_index.values()).index(last_engine)]
            self.engine_listbox.setCurrentRow(row)
        
        if last_iwad:
            index = list(self.iwad_index.keys())[list(self.iwad_index.values()).index(last_iwad)]
            self.iwad_combobox.setCurrentIndex(index)
        
    def load_wads(self):
        self.wad_listbox.clear()
        self.wad_index = {}
        wad_list = self.ui.app.dork.get_all_wads()

        for x in range(len(wad_list)):
            wad = wad_list[x]
            self.wad_index[x]=wad.id
            wad_item = WadListItem(wad, self.ui.app.config)
            add_item = QListWidgetItem()
            add_item.setSizeHint(wad_item.sizeHint())
            self.wad_listbox.addItem(add_item)
            self.wad_listbox.setItemWidget(add_item, wad_item)
            
        divider_item = DividerWidgetItem()
        self.wad_listbox.addItem(divider_item)
        
        add_wad_item = AddItemWidget("Add Wads", self.wad_listbox)
        add_item = QListWidgetItem(self.wad_listbox)
        add_item.setSizeHint(add_wad_item.sizeHint())
        self.wad_listbox.setItemWidget(add_item, add_wad_item)
        add_wad_item.add_item.connect(self.on_add_wads_item_clicked)
    
    def load_engines(self):
        self.engine_listbox.clear()
        self.engine_index = {}
        engine_list = self.ui.app.dork.get_all_engines()

        for x in range(len(engine_list)):
            engine = engine_list[x]
            self.engine_index[x]= engine.id
            engine_item = QListWidgetItem(engine.title)
            self.engine_listbox.addItem(engine_item) 
            
            
        divider_item = DividerWidgetItem()
        self.engine_listbox.addItem(divider_item)
        
        add_engine_item = AddItemWidget("Add Engine", self.engine_listbox)
        add_item = QListWidgetItem(self.engine_listbox)
        add_item.setSizeHint(add_engine_item.sizeHint())
        self.engine_listbox.setItemWidget(add_item, add_engine_item)
        add_engine_item.add_item.connect(self.on_add_engines_item_clicked)
        
    def show_engine_context_menu(self, pos):
        selected_engine_index = self.engine_listbox.currentRow()
        if selected_engine_index == self.engine_listbox.count()-1:
            return
        if selected_engine_index >=0:
            global_pos = self.engine_listbox.mapToGlobal(pos)
            self.engine_context_menu.exec(global_pos)
    
    def show_wad_context_menu(self, pos):
        selected_wad_index = self.wad_listbox.currentRow()
        if selected_wad_index == self.wad_listbox.count()-1:
            return
        if selected_wad_index >=0:
            global_pos = self.wad_listbox.mapToGlobal(pos)
            self.wad_context_menu.exec(global_pos)
        
    def add_wad_folder(self):
        # Default folder is used for the first time, then the last folder selected
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Folder', self.last_local_folder, "WAD File (*.wad)")
        if file_path:
            folder_path = os.path.dirname(file_path)
            self.last_local_folder = folder_path
            self.parser.set("DATA", "last_directory", folder_path)
            folder_name = os.path.basename(os.path.normpath(folder_path))
            
            msg_box = QMessageBox()
            msg_box.setStyleSheet(qdarkstyle.load_stylesheet())
            msg_box.setText(f"Would you like to add the entire '{folder_name}' folder?")
            msg_box.setWindowTitle("Use Entire Folder?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            response = msg_box.exec_()
            if response == QMessageBox.Yes:
                recursive_msg = QMessageBox()
                recursive_msg.setStyleSheet(qdarkstyle.load_stylesheet())
                recursive_msg.setText(f"Include subfolders?")
                recursive_msg.setWindowTitle("Recursive Folder?")
                recursive_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                recursive_msg.setDefaultButton(QMessageBox.No)
                recursive_resp = recursive_msg.exec_()
                if recursive_resp == QMessageBox.Yes:
                    recursive = True
                else:
                    recursive = False
                self.ui.app.dork.add_local_wads_from_folder(folder_path, True, recursive)
            else:
                self.ui.app.dork.add_local_wad(file_path)
    
    def on_add_engines_item_clicked(self):
        self.open_engine_window()
        
    def on_add_wads_item_clicked(self):
        self.open_wad_window()
    
    def open_wad_window(self):
        self.wad_window = WadWindow(self)
        self.wad_window.exec_()    
    
    def open_engine_window(self):
        self.engine_window = EngineWindow(self)
        self.engine_window.exec_() 
    
    def open_new_engine_window(self, engine_path):
        new_engine_window = NewEngineWindow(engine_path, self)
        new_engine_window.exec_()
    
    def open_iwad_window(self):
        iwad_window = IWadWindow(self)
        iwad_window.exec_()
        
    def open_edit_engine_window(self):
        selected_engine_index = self.engine_listbox.currentRow()      
        engine_id = self.engine_index[selected_engine_index]
        edit_engine_window = EditEngineWindow(engine_id, self)
        edit_engine_window.exec_()
    
    def open_download_wad_window(self):

        download_wad_window = DownloadWadWindow(self)
        download_wad_window.exec_()
        
    def open_edit_wad_menu(self):
        selected_wad_index = self.wad_listbox.currentRow()
        wad_id = self.wad_index[selected_wad_index]
        edit_wad_window = EditWadWindow(wad_id, self)
        edit_wad_window.exec_()
    
    def open_wad_folder(self):
        selected_wad_index = self.wad_listbox.currentRow()      
        wad_id = self.wad_index[selected_wad_index]
        wad = self.ui.app.dork.get_wad(wad_id)
        folder_path = os.path.dirname(wad.file_path)
        url = QUrl.fromLocalFile(folder_path)
        QDesktopServices.openUrl(url)
        
    def open_engine_folder(self):
        selected_engine_index = self.engine_listbox.currentRow()      
        engine_id = self.engine_index[selected_engine_index]
        engine = self.ui.app.dork.get_engine(engine_id)
        url = QUrl.fromLocalFile(engine.folder_path)
        QDesktopServices.openUrl(url)
        
    def add_engine(self):
        default_path = self.last_local_folder or "."
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Engine', default_path, "Executable File (*.exe)")
        
        if file_path:

            folder_path = os.path.dirname(file_path)
            self.last_local_folder = folder_path
            self.parser.set("DATA", "last_directory", folder_path)
            self.open_new_engine_window(file_path)

    def save_engine(self, new_engine_window):
        engine_path = new_engine_window.engine_path
        title = new_engine_window.title_input.text()
        description = new_engine_window.description_input.text()
        version = new_engine_window.version_input.text()
        new_engine_window.close()

        details = {
            "engine_path":engine_path,
            "title":title,
            "description":description,
            "version":version,
        }
        self.ui.app.dork.add_local_engine(details)
    
    def update_wad(self, edit_wad_window, wad_id):
        pass
        
    def update_engine(self, edit_engine_window, engine_id):
        title = edit_engine_window.title_input.text()
        description = edit_engine_window.description_input.text()
        version = edit_engine_window.version_input.text()
        edit_engine_window.close()
        
        details = {
            "engine_id":engine_id,
            "title":title,
            "description":description,
            "version":version,
        }
        self.ui.app.dork.update_local_engine(details)
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File
        file_menu = menubar.addMenu('File')
        
        refresh_action = QAction("Refresh", self)
        file_menu.addAction(refresh_action)
        prefs_action = QAction('Preferences', self)
        file_menu.addAction(prefs_action)

        quit_action = QAction('Exit', self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Engines
        engine_menu = menubar.addMenu('Engines')
        manage_engines_action = QAction("Manage Engines", self)
        manage_engines_action.triggered.connect(self.open_engine_window)
        engine_menu.addAction(manage_engines_action)
        
        engine_menu.addSeparator()
        
        refresh_engines_action = QAction("Refresh Engines", self)
        refresh_engines_action.triggered.connect(self.load_engines)
        engine_menu.addAction(refresh_engines_action)
        


        # Wads
        wads_menu = menubar.addMenu('Wads')
        manage_wads_action = QAction("Manage Wads", self)
        manage_wads_action.triggered.connect(self.open_wad_window)
        wads_menu.addAction(manage_wads_action)
        
        iwads_action = QAction("Manage IWADS", self)
        iwads_action.triggered.connect(self.open_iwad_window)
        wads_menu.addAction(iwads_action)
        
        wads_menu.addSeparator()
        
        refresh_wads_action = QAction("Refresh Wads", self)
        refresh_wads_action.triggered.connect(self.load_wads)
        wads_menu.addAction(refresh_wads_action)
        

        

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
        
class Nothing:
    pass