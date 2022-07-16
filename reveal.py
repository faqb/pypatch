from wave import Wave
from utils import Writer
from rich.console import Console
import numpy as np


class Reveal(Wave):
    def __init__(
        self,
        original_file: str,
        result_file: str,
        reveal_file_bytes_length: int
    ) -> None:
        self.original_file = original_file
        self.result_file = result_file
        self.reveal_file_bytes_length = reveal_file_bytes_length

        Wave.__init__(self, original_file)

        self.console = Console()
    
    def get_file(self) -> None:
        data = []

        # get hidden data size
        secret_bytes = self.reveal_file_bytes_length

        for channel in range(self.channels):
            if secret_bytes < 1:
                break

            channel_bytes = self.channel_bytes(channel)

            if secret_bytes >= len(channel_bytes) // 8:
                secret_bytes -= len(channel_bytes) // 8
                not_revealed_bytes = len(channel_bytes) // 8
            else:
                not_revealed_bytes = secret_bytes
                secret_bytes = 0

            revealed_bytes = self.reveal(channel, not_revealed_bytes)
            data.extend(revealed_bytes)
        
        # write data to result_file
        Writer(self.result_file).write_file(data)
 
    def reveal(self, channel: int, bytes_number: int):
        data = []
        bytes_array = self.reshape_channel(channel)
        with self.console.status(
            f"[bold green]Revealing data from {channel+1} channel..."
        ) as status:
            for n, sub_array_bytes in enumerate(bytes_array):
                if n >= bytes_number:
                    break

                data.append(self.get(sub_array_bytes))

                status.update(spinner_style="blue")
        
            self.console.log(
                f"[green]Finish revealing data from {channel+1} channel[/green]"
            )

        return data 
    
    def get(self, array: np.ndarray) -> list:
        data = []
        for byte in array:
            bits = "{:08b}".format(byte)
            data.append(bits[-1])

        data = int(''.join(str(x) for x in data), 2)
        return data
