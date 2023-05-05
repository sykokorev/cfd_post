from __future__ import annotations


from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout,
    QHBoxLayout, QLabel, QFileDialog,
    QGroupBox, QVBoxLayout
)
from PySide6.QtCore import Qt, QSize, Slot

from gui.model import *
from gui.widgets import *
from gui.editors import *
from datamodel.data import *
from utils.parse_out import *



CURDIR = os.curdir



class View(QMainWindow):

    def __init__(self, parent: QWidget | None = None, flags: Qt.WindowType = Qt.WindowType.Window) -> None:
        super(View, self).__init__(parent, flags)

        # Properties
        self.res_files: tuple = None
        self.out_file: str = None
        self.domains: dict = None
        self.data = MacroCalcCache()

        # Setup
        h = 24
        width = 960
        height = 720
        self.resize(QSize(width, height))
        self.setWindowTitle("ANSYS Post Macro Calculator")

        # Buttons
        self.buttons = ButtonGroup()
        res = PushButton()
        out = PushButton()
        macros = PushButton()
        res.setup(text='Open ANSYS res files')
        out.setup(text='Open ANSYS out file')
        macros.setup(text='Add macros', enabled=False)
        res.setFixedHeight(h)
        out.setFixedHeight(h)
        macros.setFixedHeight(h)
        self.buttons.addButtons(buttons=[res, out, macros])
        self.buttons.buttonClicked.connect(self.buttonClicked)

        # Macros list and info
        self.macro_model = ListModel(data=self.data)
        self.macro_list = MacrosListView(parent=self)
        self.macro_list.setModel(self.macro_model)
        self.macro_list.setEditor(MacrosEditor(self.macro_list))
        self.macro_list.editor().setup()
        self.macro_list.setEnabled(False)
        self.macro_list.clicked.connect(self.setInfo)

        info_layout = QHBoxLayout()
        self.info = QLabel()
        self.info.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.info.setWordWrap(True)
        self.info.setTextFormat(Qt.TextFormat.PlainText)
        info_layout.addWidget(self.info)
        groupbox = QGroupBox("Info")
        groupbox.setFixedSize(QSize(width/2, height/2))
        groupbox.setLayout(info_layout)

        files_layout = QHBoxLayout()
        self.files_info = QLabel()
        self.files_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.files_info.setTextFormat(Qt.TextFormat.PlainText)
        self.files_info.setWordWrap(True)
        files_layout.addWidget(self.files_info)
        group_files_box = QGroupBox("Files")
        group_files_box.setFixedSize(QSize(width/2, height/2))
        group_files_box.setLayout(files_layout)

        layout = QGridLayout()
        btn_layout = QHBoxLayout()
        layout.addWidget(self.macro_list, 0, 0, 2, 1)
        layout.addWidget(groupbox, 0, 1)
        layout.addWidget(group_files_box, 1, 1)
        for btn in self.buttons.buttons():
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout, 2, 0)
        layout.addWidget(QWidget(), 2, 1)
        layout.setObjectName('main_layout')

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    @Slot(QPushButton, result=None)
    def buttonClicked(self, button: QPushButton):
        btn_idx = self.buttons.id(button)
        dlg = QFileDialog(self, Qt.WindowType.Dialog)

        match btn_idx:
            case 0:
                self.res_files = None
                self.res_files = dlg.getOpenFileNames(
                    self, 'Select ANSYS res files',
                    filter="ANSYS res (*.res)", dir=CURDIR)
                if self.res_files[0]:
                    text = ''
                    for file in self.res_files[0]:
                        text += f'{os.path.split(file)[1]}\n'
                    self.files_info.setText(text)
            case 1:
                self.out_file = dlg.getOpenFileName(
                self, 'Select ANSYS out file',
                filter="ANSYS out (*.out)", dir=CURDIR)
                if self.out_file[0]:
                    self.buttons.button(2).setEnabled(True)
                    self.macro_list.setEnabled(True)
                    self.domains = get_domains(self.out_file[0])
            case 2:
                editor = self.macro_list.editor()
                data = {'domains': self.domains}
                editor.update(data)
                editor.exec()
                macros = MacroCalc()
                if data := editor.data:
                    macros.add(data)
                    self.data.add(macros)
                    self.macro_list.model().layoutChanged.emit()

    def setInfo(self):
        text = self.macro_model.getData(self.macro_list.currentIndex())
        if text:
            view = text.view()
            self.info.setText(view)
