from enum import Enum


MACROS = [
    'Axial Gas Compressor',
    'Centrifugal Gas Compressor',
    'Axia Guid Vane',
    'Pipe Diffuser',
    'Compressor Performance'
]

class Macros(Enum):

    AXIAL_COMPRESSOR = 0
    CENTRIFUGAL_COMPRESSOR = 1
    AXIAL_GV = 2
    PIPE_DIFFUSER = 3
    PERFORMANCE = 4

    def description(self) -> str:
        return MACROS[self.value]        
    
    @classmethod
    def model1(cls):
        return [0, 1, 2]

    @classmethod
    def model2(cls):
        return [3]
    
    @classmethod
    def model3(cls):
        return [4]