from __future__ import annotations

import os
import sys

from PySide6.QtWidgets import (
    QWidget, QPushButton,
    QTreeWidgetItem, QTreeWidget,
    QButtonGroup, QDialog, QGridLayout,
    QHBoxLayout, QDialogButtonBox
)
from PySide6.QtCore import QSize, QObject
from PySide6.QtGui import Qt

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)


class PushButton(QPushButton):

    def setup(self, **settings):
        if text := settings.get('text'): self.setText(text)
        if slot := settings.get('slot'): self.clicked.connect(slot)
        if size := settings.get('size'): self.setFixedSize(QSize(*size))
        self.setEnabled(settings.get('enabled', True))


class ButtonGroup(QButtonGroup):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

    def addButtons(self, buttons: List[PushButton]) -> None:
        for pos, button in enumerate(buttons):
            if isinstance(button, PushButton): self.addButton(button, pos)


class DomainsTree(QDialog):

    def __init__(self, parent: QWidget | None = None, f: Qt.WindowType = Qt.WindowType.Dialog) -> None:
        super(DomainsTree, self).__init__(parent, f)
        self.setWindowTitle('Domains')
        self.interface = None
        self.view = QTreeWidget()
        self.items = []
        self.view.setColumnCount(1)
        self.view.setHeaderLabel("Domains")
        self.resize(QSize(320, 320))
        btn_layout = QHBoxLayout()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.view.itemDoubleClicked.connect(self.accept)
        btn_layout.addWidget(self.buttonBox)

        layout = QGridLayout()
        layout.addWidget(self.view, 0, 0)
        layout.addLayout(btn_layout, 1, 0)
        self.setLayout(layout)
    
    def setData(self, data: dict):
        if not isinstance(data, dict): return False

        self.view.clear()
        self.items.clear()

        for key, values in data.items():
            item = QTreeWidgetItem([key])
            item.setSelected(False)
            for value in values:
                child = QTreeWidgetItem([value])
                item.addChild(child)
            self.items.append(item)

        self.view.insertTopLevelItems(0, self.items)

    def accept(self) -> None:
        idx = self.view.currentColumn()
        item = self.view.currentItem()
        self.interface = item.text(idx)
        return super().accept()

    def reject(self) -> None:
        self.interface = None
        return super().reject()
