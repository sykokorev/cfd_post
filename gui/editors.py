from __future__ import annotations
import os
import sys


from PySide6.QtWidgets import (
    QDialog, QWidget, QComboBox,
    QLineEdit, QSpinBox, QGridLayout,
    QLabel, QHBoxLayout, QMessageBox,
    QDialogButtonBox, QVBoxLayout,
    QGroupBox
)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QRegularExpressionValidator

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)

from const.dataconsts import*
from gui.widgets import *

LBL_WIDTH = 80


def builder(widgets: dict):

    vbox = QVBoxLayout()
    for l, w in widgets.items():
        hbox = QHBoxLayout()
        lbl = QLabel(l)
        lbl.setFixedSize(QSize(LBL_WIDTH, 24))
        hbox.addWidget(lbl)
        hbox.addWidget(w)
        vbox.addLayout(hbox)
    return vbox



class MacrosEditor(QDialog):

    def __init__(self, parent: QWidget | None = None, f: Qt.WindowType = Qt.WindowType.Dialog) -> None:
        super(MacrosEditor, self).__init__(parent, f)

        self._data: dict = None
        self.mlayout = QGridLayout()
        self.domains = DomainsTree(self)
        self.macros = QComboBox()
        self.name = QLineEdit()
        self.inlet = QComboBox()
        self.outlet = QComboBox()
        self.throat = QComboBox()
        self.blade = QComboBox()
        self.num_baldes = QSpinBox()
        self.axis = QComboBox()
        self.rot_speed = QLineEdit()
        self.throat = QComboBox()

        self.setWindowTitle("Macros editor")
        self.macros.currentIndexChanged.connect(self.itemsEnable)

    def setup(self):

        self.setFixedSize(320, 280)
        h = self.parent().size().height()
        w = self.parent().size().width()
        x = self.parent().pos().x() + w / 2 - 160
        y = self.parent().pos().y() + h / 2 - 140
        self.setGeometry(QRect(x, y, 320, 280))
        self.setModal(True)

        layout1 = QHBoxLayout()
        lbl = QLabel('Macros')
        lbl.setFixedSize(QSize(LBL_WIDTH, 24))
        layout1.addWidget(lbl)
        layout1.addWidget(self.macros)
        layout2 = QHBoxLayout()
        lbl = QLabel('Name')
        lbl.setFixedSize(QSize(LBL_WIDTH, 24))
        layout2.addWidget(lbl)
        layout2.addWidget(self.name)
        self.macros.addItems([m.description() for m in Macros])

        re = QRegularExpressionValidator("-?\\d{1,6}.\\d{1,6}", self)
        self.rot_speed.setValidator(re)
        self.mlayout.addLayout(layout1, 0, 0)
        self.mlayout.addLayout(layout2, 1, 0)
        self.buildEditor(0)

    def buildEditor(self, idx: int) -> QGroupBox:


        gb = QGroupBox(Macros(idx).description())

        if idx in Macros.model1():
            widgets = {
                'Inlet Region': self.inlet, 'Outlet Regoin': self.outlet,
                'Blade Region': self.blade, 'Num. Blades': self.num_baldes,
                'Machine Axis': self.axis, 'Rot. Speed': self.rot_speed
            }
            inlet = PushButton()
            outlet = PushButton()
            blade = PushButton()
            inlet.setObjectName('inlet')
            outlet.setObjectName('outlet')
            blade.setObjectName('blade')
            btns = [inlet, outlet, blade]
        elif idx in Macros.model2():
            widgets = {
                'Inlet Region': self.inlet, 'Outlet Regoin': self.outlet,
                'Throat Region': self.throat, 'Num. Blades': self.num_baldes,
                'Machine Axis': self.axis
            }
            inlet = PushButton()
            outlet = PushButton()
            throat = PushButton()
            inlet.setObjectName('inlet')
            outlet.setObjectName('outlet')
            throat.setObjectName('throat')
            btns = [inlet, outlet, throat]

        self.btns = ButtonGroup(self)
        self.btns.buttonClicked.connect(self.showDomainList)

        for idx, btn in enumerate(btns, 2):
            self.btns.addButton(btn, idx)

        for row, (lbl, widget) in enumerate(widgets.items(), 2):
            if isinstance(widget, QWidget):
                hbox = QHBoxLayout()
                label = QLabel(lbl)
                label.setFixedSize(QSize(LBL_WIDTH, 24))
                hbox.addWidget(label)
                hbox.addWidget(widget)
                mlayout.addLayout(hbox, row, 0)

        for row, btn in enumerate(self.btns.buttons(), 2):
            btn.setup(text='...', size=[24, 24], enabled=False)
            mlayout.addWidget(btn, row, 2)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        btn_layout = QHBoxLayout()

        btn_layout.addWidget(self.buttonBox)
        mlayout.addLayout(btn_layout, len(widgets)+2, 0, 1, 0)
        self.setLayout(mlayout)

    # def setup(self):
    #     self.setFixedSize(320, 280)
    #     h = self.parent().size().height()
    #     w = self.parent().size().width()
    #     x = self.parent().pos().x() + w / 2 - 160
    #     y = self.parent().pos().y() + h / 2 - 140
    #     self.setGeometry(QRect(x, y, 320, 280))
    #     self.setModal(True)

    #     widgets = [self.macros, self.name, self.inlet, self.outlet,
    #                self.blade, self.num_baldes, self.axis, self.rot_speed]
    #     labels = ["Macros", "Name","Inlet Region", "Outlet Region", 
    #             "Blade Region", "Num. Blades", "Machine Axis", "Rot. Speed"]
    #     self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    #     self.buttonBox.accepted.connect(self.accept)
    #     self.buttonBox.rejected.connect(self.reject)
    #     btn_layout = QHBoxLayout()
    #     btn_layout.addWidget(self.buttonBox)

    #     inlet = PushButton()
    #     outlet = PushButton()
    #     blade = PushButton()

    #     inlet.setObjectName('inlet')
    #     self.inlet.setObjectName('inlet')
    #     outlet.setObjectName('outlet')
    #     self.outlet.setObjectName('outlet')     
    #     blade.setObjectName('blade')
    #     self.blade.setObjectName('blade')
    #     self.rot_speed.setObjectName('rot_speed')

    #     self.btns = ButtonGroup(self)
    #     self.btns.addButton(inlet, 2)
    #     self.btns.addButton(outlet, 3)
    #     self.btns.addButton(blade, 4)
    #     self.btns.buttonClicked.connect(self.showDomainList)

    #     layout = QGridLayout()
    #     for row, btn in enumerate(self.btns.buttons(), 2):
    #         btn.setup(text='...', size=[24, 24], enabled=False)
    #         layout.addWidget(btn, row, 2)

    #     for row, (lb, w) in enumerate(zip(labels, widgets)):
    #         layout.addWidget(QLabel(lb), row, 0)
    #         layout.addWidget(w, row, 1)

    #     re = QRegularExpressionValidator("-?\\d{1,6}.\\d{1,6}", self)
    #     self.rot_speed.setValidator(re)

    #     layout.addLayout(btn_layout, row+1, 0, 1, 0)
    #     self.setLayout(layout)

    def clear(self):
        
        # self.macros.clear()
        self.name.clear()
        self.inlet.clear()
        self.outlet.clear()
        self.blade.clear()
        self.num_baldes.setValue(0)
        # self.axis.clear()
        self.rot_speed.setText('0')

    def update(self, data: dict = None) -> None:
        pass
        self.clear()
        # self.axis.addItems(['X', 'Y', 'Z'])
        # self.macros.addItems([m.describe() for m in Macros])

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
                self.rot_speed.setText(str(rs))
            except ValueError:
                self.rot_speed.setText('0')

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data: dict | None):
        if not isinstance(data, dict | None): return None
        self._data = data

    def itemsEnable(self):
        index = self.sender().currentIndex()
        self.buildEditor(index)

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
