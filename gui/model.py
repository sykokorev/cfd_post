from __future__ import annotations


from typing import Union

from PySide6.QtWidgets import (
    QWidget, QStyleOptionViewItem,
    QListView, QItemDelegate, QMenu,
)
from PySide6.QtCore import (
    Qt, QAbstractListModel, QModelIndex,
    QPersistentModelIndex, QObject, QRect
)
from PySide6.QtGui import QMouseEvent, QKeyEvent, QKeySequence

from datamodel.models import AbstractDataCache, AbstractDataModel
from datamodel.data import *
from gui.editors import *



class ListViewItemDelegate(QItemDelegate):

    def __init__(self, parent: ListView) -> None:
        super(ListViewItemDelegate, self).__init__(parent)
        self.setParent(parent)
        self.model: ListModel = self.parent().data_model

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> QWidget:
        editor = MacrosEditor(parent=self.parent())
        editor.setup()
        self.commitData.connect(self.closeAndUpdate)
        return editor

    def setEditorData(self, editor: MacrosEditor, index: QModelIndex | QPersistentModelIndex) -> None:

        if parent := self.parent():
            editor.setFixedSize(320, 280)
            h = editor.parent().size().height()
            w = editor.parent().size().width()
            x = editor.parent().pos().x() + w / 2 - 160
            y = editor.parent().pos().y() + h / 2 - 140
            editor.setGeometry(QRect(x, y, 320, 280))
            model = parent.data_model
            data: dict = model.get(index).data
            data.update({'domains': parent.domains})
            editor.update(data)
        return None

    def closeAndUpdate(self, editor: MacrosEditor) -> None:

        data = editor.data
        index = self.parent().data_view.currentIndex()
        if data:
            self.model.update(index, data)
        
        return None


class ListModel(QAbstractListModel):

    def __init__(self, data: AbstractDataCache, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._data = data

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int):

        if not index.isValid() : return None
        if not 0 <= index.row() <= len(self._data.data) : return None

        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.get(index.row()))

    def update(self, index: Union[QModelIndex, QPersistentModelIndex], data) -> None:
        if not index.isValid() : return False
        if not 0 <= index.row() <= len(self._data.data) : return None
        self._data.update(index.row(), data)
        return None

    def get(self, index: Union[QModelIndex, QPersistentModelIndex]) -> AbstractDataModel | None:
        if not index.isValid() : return False
        if not 0 <= index.row() <= len(self._data.data) : return None
        return self._data.get(index.row())

    def delete(self, index: Union[QModelIndex, QPersistentModelIndex]):
        if not index.isValid() : return False
        if not 0 <= index.row() <= len(self._data.data) : return None
        self._data.delete(index.row())

    def moveUp(self, index: Union[QModelIndex, QPersistentModelIndex]) -> bool:
        if not index.isValid() : return False
        if not 0 <= index.row() <= len(self._data.data) : return None
        self._data.moveUp(index.row())

    def moveDown(self, index: Union[QModelIndex, QPersistentModelIndex]) -> bool:
        if not index.isValid() : return False
        if not 0 <= index.row() <= len(self._data.data) : return None
        self._data.moveDown(index.row())

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    def rowCount(self, index) -> int:
        return len(self._data.data)


class ListView(QListView):

    def __init__(self, parent: QWidget | None = None) -> None:
        super(ListView, self).__init__(parent)
        if parent : self.setParent(parent)
        self.setItemDelegate(ListViewItemDelegate(parent=self.parent()))

    def keyPressEvent(self, event: QKeyEvent) -> None:

        if event == QKeySequence.StandardKey.Delete:
            self.delete(self.currentIndex())

        return super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        
        if event.button() == Qt.MouseButton.RightButton:
            menu = QMenu(self.parent())
            menu.addAction('Edit', lambda: self.edit(self.currentIndex()))
            menu.addAction('Delete', lambda: self.delete(self.currentIndex()))
            menu.addAction('MoveUp', lambda: self.moveUp(self.currentIndex()))
            menu.addAction('MoveDown', lambda: self.moveDown(self.currentIndex()))
            menu.exec(event.globalPos())

        return super().mousePressEvent(event)

    def delete(self, index: Union[QModelIndex, QPersistentModelIndex], parent: QWidget = None) -> bool:
        try:
            self.model().delete(index)
            return True
        except:
            return False

    def moveUp(self, index: Union[QModelIndex, QPersistentModelIndex], parent: QWidget = None) -> bool:
        try:
            self.model().moveUp(index)
            return True
        except:
            return False

    def moveDown(self, index: Union[QModelIndex, QPersistentModelIndex], parent: QWidget = None) -> bool:
        try:
            self.model().moveDown(index)
            return True
        except:
            return False
