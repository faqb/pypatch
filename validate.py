import os
import sys
from pathlib import Path
from rich.console import Console


INPUT_FILE_ALLOWED_EXTENSIONS = {".mp3", ".wav"}
INPUT_FILE_EXTENSIONS_REQUIRED_CONVERTING = {".mp3"}
OUTPUT_FILE_ALLOWED_EXTENSIONS = {".wav"}


class Validator(object):
    """Validate user file types."""

    def __init__(self, file):
        self.file = file
        
    def validate_input_file(self) -> bool:
        """
        Return: 
            True if validation was successful
            False if it needs conversion
            otherwise sys.exit
        """
        
        try:
            input_file_path = Path(self.file)
            input_file_ext = input_file_path.suffix
        except TypeError as err:
            Console().print(f"[bold][red]{repr(err)}")
            sys.exit(1)
        
        if input_file_path.is_file():
            if os.access(self.file, os.R_OK):
                if input_file_ext in INPUT_FILE_ALLOWED_EXTENSIONS:
                    if input_file_ext in INPUT_FILE_EXTENSIONS_REQUIRED_CONVERTING:
                        return False
                    return True
                else:
                    Console(stderr=True).print(
                        f"[bold][red]This file type is not allowed.[/red]\n"
                        f"Allowed extensions: {list(INPUT_FILE_ALLOWED_EXTENSIONS)}."
                    )
                    sys.exit(1)
            else:
                Console(stderr=True).print(
                    f"[bold][red]Check {self.file}file permissions.[/red]"
                )
                sys.exit(1)
        else:
            Console(stderr=True).print(
                f"[bold][red]Missing {self.file}.[/red]"
            )
            sys.exit(1)

    def validate_output_file(self, hide=None):
        try:
            output_file_path = Path(self.file)
            output_file_ext = output_file_path.suffix
        except TypeError as err:
            Console().print(f"[bold][red]{repr(err)}")
            sys.exit(1)

        if os.access(os.path.dirname(os.path.abspath(self.file)), os.W_OK):
            if hide:
                if output_file_ext in OUTPUT_FILE_ALLOWED_EXTENSIONS:
                    return True
                else:
                    Console(stderr=True).print(
                        f"[bold][red]This file type for output file is not allowed.[/red]\n"
                        f"Allowed extensions: {list(OUTPUT_FILE_ALLOWED_EXTENSIONS)}."
                    )
                    sys.exit(1)
            else:
                return True
        else:
            Console(stderr=True).print(
                f'[bold][red]Check directory permissions.[/red]'
            )
            sys.exit(1)

    def validate_target_file(self):
        try:
            target_file_path = Path(self.file)
            target_file_ext = target_file_path.suffix
        except TypeError as err:
            Console().print(f"[bold][red]{repr(err)}")
            sys.exit(1)
        
        if target_file_path.is_file():
            if os.access(self.file, os.R_OK):
                if target_file_ext in INPUT_FILE_EXTENSIONS_REQUIRED_CONVERTING:
                    return False
                return True
            else:
                Console(stderr=True).print(
                    f"[bold][red]Check {self.file}file permissions.[/red]"
                )
                sys.exit(1)
        else:
            Console(stderr=True).print(
                f"[bold][red]Missing {self.file}.[/red]"
            )
            sys.exit(1)
