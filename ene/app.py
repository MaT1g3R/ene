#  ENE, Automatically track and sync anime watching progress
#  Copyright (C) 2018 Peijun Ma, Justin Sedge
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from PySide2 import QtUiTools
from PySide2.QtCore import QFile, Qt
from PySide2.QtWidgets import QAction, QApplication, QFileDialog, QMainWindow, QWidget

import ene.ui
from ene.config import Config
from ene.constants import APP_NAME, IS_37, IS_WIN

if IS_37:
    from importlib.resources import path
else:
    from importlib_resources import path

QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)


@contextmanager
def open_ui_file(filename: str) -> QFile:
    """
    Context manager to open a Qt ui file
    Args:
        filename: Filename of the ui file

    Returns:
        The ui file opened, and closes the file afterwards
    """
    uifile = QFile(str(filename))
    try:
        uifile.open(QFile.ReadOnly)
        yield uifile
    finally:
        uifile.close()


def load_ui_widget(ui_file: str, parent: Optional[QWidget] = None) -> QWidget:
    """
    Load a ui widget from file
    Args:
        ui_file: The ui file name
        parent: The parent of that widget

    Returns:
        The loaded ui widget
    """
    loader = QtUiTools.QUiLoader()
    with open_ui_file(ui_file) as uifile:
        ui = loader.load(uifile, parent)
    uifile.close()
    return ui


class MainForm(QMainWindow):
    """
    Main form of the application
    """

    def __init__(self):
        """
        Initialize the ui files for the application
        """
        super().__init__()
        self.config = Config()
        self.setWindowTitle(APP_NAME)

        with path(ene.ui, 'ene.ui') as p:
            self.main_window = load_ui_widget(p)
        with path(ene.ui, 'settings.ui') as p:
            self.prefences_window = load_ui_widget(p)

        self.main_window.setWindowTitle(APP_NAME)
        self.prefences_window.setWindowTitle('Preferences')
        self.setup_children()

    def setup_children(self):
        """
        Setup all the child widgets of the main window
        """
        self.act_prefences = self.main_window.findChild(QAction, '﻿action_prefences')
        assert self.act_prefences
        self.act_prefences.triggered.connect(self.prefences_window.show)
        self.act_open_folder = self.main_window.findChild(QAction, '﻿action_open_folder')
        self.act_open_folder.triggered.connect(self.choose_dir)
        self.act_source_code = self.main_window.findChild(QAction, '﻿action_source_code')
        self.act_source_code.triggered.connect(self.open_source_code)

    def choose_dir(self) -> Path:
        """
        Choose a directory from a file dialog

        Returns: The directory path
        """
        args = [self, self.tr("Open Directory"), str(Path.home())]
        if IS_WIN:
            args.append(QFileDialog.DontUseNativeDialog)
        dir_ = QFileDialog.getExistingDirectory(*args)
        # TODO do something with this
        return Path(dir_)

    @classmethod
    def launch(cls):
        """
        Launch the Application
        """
        app = QApplication([APP_NAME])
        form = cls()
        form.main_window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    MainForm.launch()
