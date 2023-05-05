from __future__ import annotations


from typing import Union

from PySide6.QtCore import (
    Qt, QAbstractListModel, QModelIndex,
    QPersistentModelIndex, QObject
)

from datamodel.models import AbstractDataCache, AbstractDataModel


class ListModel(QAbstractListModel):

    def __init__(self, data: AbstractDataCache, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._data = data
        self._editor: QObject = None

    def setEditor(self, editor: QObject):
        if isinstance(editor, QObject): self._editor = editor

    def editor(self) -> QObject:
        return self._editor

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int):

        if role == Qt.ItemDataRole.DisplayRole:
            if not index.isValid() : return None
            if not 0 <= index.row() <= len(self._data.data) : return None
            return str(self._data.get(index.row()))
    
    def updateData(self, index: Union[QModelIndex ,QPersistentModelIndex], data: dict) -> bool:

        if not index.isValid() : return False
        if not 0 <= index.row() <= len(self._data.data) : return None
        self._data.update(index.row(), data)
        return True
    
    def getData(self, index: Union[QModelIndex, QPersistentModelIndex]) -> AbstractDataModel | None:
        if not index.isValid() : return False
        if not 0 <= index.row() <= len(self._data.data) : return None
        return self._data.get(index.row())

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    def rowCount(self, index) -> int:
        return len(self._data.data)
