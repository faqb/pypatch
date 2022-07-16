import sys
import numpy as np
from utils import Reader, Writer
from wave import Wave
from file import File
from rich.console import Console


class Hide(File, Wave):
	"""Get original file and hide file_to_hide to result file."""

	def __init__(
		self,
		original_file: str,
		result_file: str,
		file_to_hide: str
	) -> None:

		self.original_file = original_file
		self.result_file = result_file
		self.file_to_hide = file_to_hide

		Wave.__init__(self, self.original_file)
		File.__init__(self, self.file_to_hide)

		self.console = Console()

	def file_to_audio(self) -> None:
		"""Iterate over channels and hide file bytes inside channel bytes."""

		# get file to hide bytes and load them to array
		file_to_hide_bytes = Reader(self.file_to_hide).read_file()


		# if not enough space to hide the file -> exit
		if not self.check_free_space(file_to_hide_bytes):
			Console(stderr=True).print(f"[bold][red]Not enough space to hide file!")
			sys.exit(1)
			
		for channel in range(self.channels):

			# get channel bytes
			channel_bytes = self.channel_bytes(channel)

			# if nothing left to hide -> exit
			if ((len(channel_bytes) // 8) * channel) > len(file_to_hide_bytes):
				break
			
			# file to hide bytes sub array
			bytes_sub_array = self.sub_array(channel_bytes, channel)

			patched_bytes = self.patch(channel, bytes_sub_array)
		
			if self.channels > 1:

				# if patched bytes > then free space in channel -> trim them 
				if self.data[:, channel].size != len(patched_bytes):
					self.data[:, channel] = patched_bytes[:self.data[:, channel].size]
				else:
					self.data[:, channel] = patched_bytes[:]

			else:
				self.data = np.asarray(patched_bytes)
  
 
		# write patched data to result file
		Writer(self.result_file).write_wav(self.data, self.samplerate)


	def check_free_space(self, file_to_hide_bytes):
		if len(file_to_hide_bytes) > self.free_space():
			return False
		return True

	def patch(self, channel, bytes_to_hide) -> list:
		"""Patch channel bytes."""

		data = []

		size_to_hide = len(bytes_to_hide)
		bytes_array = self.reshape_channel(channel)


		with self.console.status(
			f"[bold green]Patching {channel+1} channel bytes..."
		) as status:
			for n, sub_array_bytes in enumerate(bytes_array):
				if size_to_hide > n:
					byte = bytes_to_hide[n]
					data.extend(self.hide(sub_array_bytes, byte))
				else:
					data.extend(sub_array_bytes)
				status.update(spinner_style="blue")

			self.console.log(f"[green]Finish patching {channel+1} channel[/green]")
	
		return data 

	@staticmethod
	def hide(array: np.ndarray, byte: np.uint8) -> np.ndarray:
		"""Hide byte inside sub array from channel bytes."""

		bits = "{:08b}".format(byte)
		for i, byte in enumerate(array):
			array[i] = (byte & ~1) | (int(bits[i]))

		return array
