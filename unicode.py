from types import *

def deUTF8(data):
    """This is meant to help with utf-8 data appearing where unicode should apperar."""
    # In particular my DB is returning the wrong thing.
    if type(data) == StringType:
        return data.decode('utf-8')
    return data
