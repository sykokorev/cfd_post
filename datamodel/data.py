import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)

from datamodel.models import *
from utils.errorhandler import Error


class MacroCalc(AbstractDataModel):

    def __init__(self) -> None:
        super(MacroCalc, self).__init__()
        self.name: str = ''
        self.macros: str = ''
        self.inlet: str = ''
        self.outlet: str = ''
        self.blade: str = ''
        self.num_blades: int = 0
        self.axis: str = 'Z'
        self.rot_speed: float = 0.0
        self.tooltip: str = self.macros

    @property
    def data(self) -> dict:
        return {
            'macros': self.macros,
            'name': self.name, 'inlet': self.inlet,
            'outlet': self.outlet, 'blade': self.blade,
            'num_blades': self.num_blades, 'axis': self.axis,
            'rot_speed': self.rot_speed, 'tooltip': self.tooltip
        }

    def add(self, data: dict):
        if not isinstance(data, dict) : return False

        for k, v in data.items():
            if k in self.__dir__() and not str(k).startswith('_'):
                setattr(self, k, v)

        return super().update(data)

    def update(self, data: dict) -> bool:

        if not isinstance(data, dict) : return False

        for k, v in data.items():
            if k in self.__dir__() and not str(k).startswith('_'):
                setattr(self, k, v)

        return super().update(data)

    def view(self) -> str:
        view = f"{self.name} ({self.macros})\n\tInlet Region: {self.inlet}\n\tOutlet Region: {self.outlet}\n\t"
        view += f"Blade Region: {self.blade}\n\tNum. Blades: {self.num_blades}\n\tAxis: {self.axis}\n\t"
        view += f"Rot. Speed: {self.rot_speed}\n"
        return view

    def __str__(self):
        return f'Macros name: {self.name}. Macros type: {self.macros}\n'


class MacroCalcCache(AbstractDataCache):

    def __init__(self) -> None:
        super().__init__()
