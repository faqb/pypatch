import os
import sys
import ffmpy
from rich.console import Console


class Convert(object):
    """Convert file to supported format."""

    def __init__(self, source_file: str, destination_file: str) -> None:
        self.source_file = source_file
        self.destination_file = destination_file

    def mp3_to_wav(self) -> None:
        """Convert mp3 -> wav. 
        Parameter "-y" is used to overwrite wav file.
        Parameter "-loglevel quite" is used to hide extra output."""

        console = Console()
        with console.status(
            f"[bold green]Converting {os.path.abspath(self.source_file)} -> "
            f"{self.destination_file}"
        ) as status:
            try:
                ff = ffmpy.FFmpeg(
                    global_options="-y -loglevel quiet",
                    inputs={self.source_file: None},
                    outputs={self.destination_file: None} 
                )
                status.update(spinner_style="blue")
                ff.run()
            except ffmpy.FFRuntimeError as err:
                console.print(f"[bold][red] {repr(err)}")
                sys.exit(1)
            except ffmpy.FFExecutableNotFoundError as err:
                console.print(f"[bold][red] {repr(err)}")
                sys.exit(1)
            else:
                console.log(
                    f"[green]Finish converting "
                    f"{os.path.abspath(self.source_file)} -> "
                    f"{self.destination_file} [/green]"
                )
