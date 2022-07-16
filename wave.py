import math
from utils import Reader
import numpy as np


class Wave(object):
    def __init__(self, file: str) -> None:
        self.file = file
        self.data, self.samplerate = Reader(self.file).read_wav()
        self.transpose = np.transpose(np.array(self.data))

    @property
    def channels(self) -> int:
        """Get number of channels."""

        if len(self.data) == 1:
            return 1
        return self.data.shape[1]

    def channel_bytes(self, channel: int) -> np.ndarray:
        """Bytes per channel."""
 
        return self.transpose[channel]
    
    def free_space(self) -> float:
        """Bytes that can be hidden."""

        return (self.data.shape[0] * self.channels) / 8
    
    def reshape_channel(self, channel: int) -> np.ndarray:
        """
        Reshape channel array: 
            [0 1 1 ... 0 1 0]
        to:
            [[0 1 1 ... 1 0 1]
             [1 0 0 ... 0 1 0]
             ...
             [1 0 1 ... 0 1 0]]

        End of array fill with 0.
        """
        arr = self.channel_bytes(channel)
        columns = 8
        rows = math.ceil(arr.size / columns)
        return np.pad(arr, (0, rows*columns - arr.size), 
            mode="constant", constant_values=0).reshape(rows, columns)