import soundfile as sf
import numpy as np


class Reader(object):
	def __init__(self, file: str):
		self.file = file

	def read_wav(self) -> tuple[list, int]:
		return sf.read(self.file, dtype="int16")

	def read_file(self) -> np.ndarray:
		return np.fromfile(self.file, dtype="uint8")


class Writer(object):
	def __init__(self, file: str) -> None:
		self.file = file
	
	def write_wav(self, data: np.ndarray, samplerate: int) -> None:
		return sf.write(self.file, data, samplerate)
	
	def write_file(self, data: np.ndarray) -> None:
		with open(self.file, "wb") as file:
			file.write(bytearray(data))
