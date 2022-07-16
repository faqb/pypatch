import sys
import xattr
from utils import Reader
import numpy as np
from rich.console import Console
from config import FILE_ATTRIBUTE


class File(object):
    def __init__(self, file: str) -> None:
        self.file = file
        self.bytes_array = Reader(self.file).read_file()
    
    def sub_array(self, array, offset) -> np.array:
        start = (len(array) * offset) // 8
        stop = (len(array) * offset + len(array)) // 8
        return self.bytes_array[start:stop]
    
    def setattr(self, file_to_set):
        return xattr.setxattr(
            file_to_set,
            FILE_ATTRIBUTE,
            len(self.bytes_array).to_bytes(length=8, byteorder="big")
        )
    
    def getattr(self):
        try:
            return int.from_bytes(
                xattr.getxattr(
                    self.file, FILE_ATTRIBUTE
                ),
                byteorder="big"
            )
        except OSError:
            Console(log_time=False).print("[bold][red]Missing reveal file attribute.")
            sys.exit(1)
