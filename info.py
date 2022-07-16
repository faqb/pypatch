import os
from pydub.utils import mediainfo
from datetime import timedelta

from rich.console import Console
from rich.table import Table


class Info(object):
    def __init__(self, file: str) -> None:
        self.f = file
        self.file = mediainfo(self.f)
        self.table = Table(title="File Info")

        self.table.add_column("Parameters", style="green", no_wrap=True)
        self.table.add_column("Values", style="", no_wrap=True)
        
    @property
    def name(self) -> str:
        return os.path.abspath(self.file["filename"])

    @property
    def samplerate(self) -> str:
        return self.file["sample_rate"]

    @property
    def size(self) -> float:
        return int(self.file["size"]) / 1e6

    @property
    def channels(self) -> str:
        return self.file["channels"]

    @property
    def duration_sec(self) -> str:
        return self.file["duration"]

    @property
    def duration_min(self) -> str:
        td = str(timedelta(seconds=float(self.duration_sec)))
        return ":".join(str(td).split(".")[:1])

    @property
    def max_size_to_hide(self):
        return float(self.duration_sec) *\
            float(self.channels) * float(self.samplerate) / 8 / 1e6

    def full_info(self):
        self.table.add_row("File", self.name)
        self.table.add_row("Duration", self.duration_min)
        self.table.add_row("Size (MB)", "{:.2f}".format(self.size))
        self.table.add_row("Sample rate (Hz)", self.samplerate)
        self.table.add_row("Channels", self.channels)
        self.table.add_row("Can be hidden (MB)", "{:.2f}".format(self.max_size_to_hide))

        return Console().print(self.table)
