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

"""This module contains common elements for UI."""
from contextlib import contextmanager
from typing import Dict, List, Optional, Union

from PySide2 import QtUiTools
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QWidget


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


def mk_stylesheet(rules: Dict[str, str], selector: Union[str, List[str]] = None) -> str:
    """
    Make a stylesheet
    Args:
        rules: The key value pairs for the rules of the stylesheet
        selector: The selector(s) of the stylesheet

    Returns:
        The stylesheet string
    """
    body = '{%s}' % ' '.join(f'{key}: {val};' for key, val in rules.items())
    if selector:
        if isinstance(selector, str):
            selector = (selector,)
        return f'{", ".join(selector)} {body}'
    else:
        return body


def mk_padding(top=0, right=0, bottom=0, left=0, unit='px') -> str:
    """
    Make padding value for stylesheet
    Args:
        top: Top padding
        right: Right padding
        bottom: Bottom padding
        left: Left padding
        unit: Padding unit

    Returns:
        Padding stylesheet rule
    """
    return f'{top}{unit} {right}{unit} {bottom}{unit} {left}{unit}'
