from enum import Enum


class Error(Enum):

    NOTINT = '{} must be int type not {}'
    NOTSTR = '{} must be str type not {}'
    DATAERROR = 'There is no data with datatype {}'
    TYPEERR = 'Data type error. Type must be {}, given {}'
    ATTRERROR = 'Data {} doesn\'t contain any elements'
    KEYERROR = 'A key error occurred. {}.'
