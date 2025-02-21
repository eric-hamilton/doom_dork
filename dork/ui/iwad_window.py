import os
from PyQt5.QtWidgets import (QLabel, QGridLayout, QSizePolicy, QPushButton, QDialog)
                        
from PyQt5.QtCore import Qt

from dork.ui.widgets import FileBrowseEdit


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