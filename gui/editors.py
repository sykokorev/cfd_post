from __future__ import annotations
import os
import sys


from PySide6.QtWidgets import (
    QDialog, QWidget, QComboBox,
    QLineEdit, QSpinBox, QGridLayout,
    QLabel, QHBoxLayout, QMessageBox,
    QDialogButtonBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QRegularExpressionValidator

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)

from const.dataconsts import MACROS as macros
from gui.widgets import PushButton, ButtonGroup, DomainsTree


class MacrosEditor(QDialog):

    def __init__(self, parent: QWidget | None = None, f: Qt.WindowType = Qt.WindowType.Dialog) -> None:
        super(MacrosEditor, self).__init__(parent, f)

        self._data: dict = None
        self.domains = DomainsTree(self)
        self.macros = QComboBox()
        self.name = QLineEdit()
        self.inlet = QComboBox()
        self.outlet = QComboBox()
        self.blade = QComboBox()
        self.num_baldes = QSpinBox()
        self.axis = QComboBox()
        self.rot_speed = QLineEdit()

        self.setWindowTitle("Macros editor")


    def setup(self):

        widgets = [self.macros, self.name, self.inlet, self.outlet,
                   self.blade, self.num_baldes, self.axis, self.rot_speed]
        labels = ["Macros", "Name","Inlet Region", "Outlet Region", 
                "Blade Region", "Num. Blades", "Machine Axis", "Rot. Speed"]
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.buttonBox)

        inlet = PushButton()
        outlet = PushButton()
        blade = PushButton()

        inlet.setObjectName('inlet')
        self.inlet.setObjectName('inlet')
        outlet.setObjectName('outlet')
        self.outlet.setObjectName('outlet')     
        blade.setObjectName('blade')
        self.blade.setObjectName('blade')

        self.btns = ButtonGroup(self)
        self.btns.addButton(inlet, 2)
        self.btns.addButton(outlet, 3)
        self.btns.addButton(blade, 4)
        self.btns.buttonClicked.connect(self.showDomainList)

        layout = QGridLayout()
        for row, btn in enumerate(self.btns.buttons(), 2):
            btn.setup(text='...', size=[24, 24], enabled=False)
            layout.addWidget(btn, row, 2)

        for row, (lb, w) in enumerate(zip(labels, widgets)):
            layout.addWidget(QLabel(lb), row, 0)
            layout.addWidget(w, row, 1)

        re = QRegularExpressionValidator("-?\\d{1,6}.\\d{1,6}", self)
        self.rot_speed.setValidator(re)

        layout.addLayout(btn_layout, row+1, 0, 1, 0)
        self.setLayout(layout)

    def clear(self):

        self.macros.clear()
        self.name.clear()
        self.inlet.clear()
        self.outlet.clear()
        self.blade.clear()
        self.num_baldes.setValue(0)
        self.axis.clear()
        self.rot_speed.setText('0')

    def update(self, data: dict = None) -> None:
        self.clear()
        self.axis.addItems(['X', 'Y', 'Z'])
        self.macros.addItems(macros)

        if not data:
            return None
        domains = data.get('domains', {})

        for interface in domains.values():
            self.inlet.addItems(interface)
            self.outlet.addItems(interface)
            self.blade.addItems(interface)
        
        if domains:
            self.domains.setData(domains)
            for btn in self.btns.buttons(): btn.setEnabled(True)
        if name := data.get('name', None):
            self.name.setText(name)
        if nb := data.get('num_blades', 0):
            try:
                nb = int(nb)
                self.num_baldes.setValue(nb)
            except ValueError:
                self.num_baldes.setValue(0)
        if rs := data.get('rot_speed', None):
            try:
                rs = float(rs)
                self.rot_speed(str(rs))
            except ValueError:
                self.rot_speed('0')

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data: dict | None):
        if not isinstance(data, dict | None): return None
        self._data = data

    def showDomainList(self, btn: PushButton):

        self.domains.exec()

        if not (i := self.domains.interface): return None
        name = btn.objectName()
        parent: QComboBox = self.findChild(QComboBox, name)

        if parent:
            idx = parent.findText(i)
            parent.setCurrentIndex(idx)

    def accept(self) -> None:
        if not self.name.text():
            msg = 'Name can\'t be empty.'
            msgbox = QMessageBox(self)
            msgbox.setText(msg)
            msgbox.setStandardButtons(QMessageBox.StandardButton.Close)
            msgbox.exec()
            return None
        
        if not self.rot_speed.text(): 
            self.rot_speed.setText('0')
        
        self.data = {
            'macros': self.macros.currentText(), 'name': self.name.text(),
            'inlet': self.inlet.currentText(), 'outlet': self.outlet.currentText(),
            'blade': self.blade.currentText(), 'num_blades': self.num_baldes.value(),
            'rot_speed': self.rot_speed.text(), 'axis': self.axis.currentText()
        }
        return super().accept()
    
    def reject(self) -> None:
        self.data = None
        return super().reject()
