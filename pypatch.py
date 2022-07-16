#!env/bin/python3

import os
import convert
import argparse
import hide
import reveal
import info
import rich
from validate import Validator
from file import File
from rich.console import Console

from config import (
    TMP_FOLDER,
    ORIGINAL_WAV_FILE,
    TARGET_WAV_FILE,
    LOGO
)


ORIGINAL_WAV_FILE_PATH = os.path.join(
    os.path.abspath(TMP_FOLDER), ORIGINAL_WAV_FILE
)
TARGET_WAV_FILE_PATH = os.path.join(
    os.path.abspath(TMP_FOLDER), TARGET_WAV_FILE
)


class Parser(argparse.ArgumentParser):
    def _print_message(self, message: str, file) -> None:
        rich.print(message, file=file)


def hide_option(args: argparse.Namespace) -> None:
    """Hide file inside audio."""

    # validate user data
    Validator(args.output).validate_output_file(hide=True)

    if not Validator(args.target).validate_target_file():
        convert.Convert(args.target, TARGET_WAV_FILE_PATH).mp3_to_wav()
        args.target = TARGET_WAV_FILE_PATH

    if not Validator(args.input).validate_input_file():
        convert.Convert(args.input, ORIGINAL_WAV_FILE_PATH).mp3_to_wav()
        args.input = ORIGINAL_WAV_FILE_PATH

    # hide file
    hide.Hide(args.input, args.output, args.target).file_to_audio()

    # set attribute with hidden file size
    File(args.target).setattr(args.output)

    Console(log_time=False, tab_size=10).log(f"\t [bold][red]Done!")


def reveal_option(args: argparse.Namespace) -> None:
    """Get hidden file from audio."""

    # validate user data
    if not Validator(args.input).validate_input_file():
        convert.Convert(args.input, ORIGINAL_WAV_FILE_PATH).mp3_to_wav()
        args.input = ORIGINAL_WAV_FILE_PATH    
    Validator(args.output).validate_output_file()
    
    # get hidden file size from attributes
    reveal_file_bytes_length = File(args.input).getattr()

    # reveal file
    reveal.Reveal(args.input, args.output, reveal_file_bytes_length).get_file()

    Console(log_time=False, tab_size=10).log(f"\t [bold][red]Done!")


def info_option(args: argparse.Namespace) -> None:
    """Show audio file information."""

    # validate user data
    Validator(args.target).validate_input_file()

    # show full info about audio file
    info.Info(args.target).full_info()


def parse() -> argparse.Namespace:
    parser = Parser(description=print(LOGO))
    subparsers = parser.add_subparsers()

    hide_parser = subparsers.add_parser("hide")
    hide_parser.add_argument(
        "-i",
        "--input",
        help="path to source MP3 or WAV file",
        type=str,
        required=True
    )
    hide_parser.add_argument(
        "-o",
        "--output",
        help="path to result patched WAV file",
        required=True
    )
    hide_parser.add_argument(
        "-t",
        "--target",
        help="path to file to hide",
        required=True
    )
    hide_parser.set_defaults(func=hide_option) 

    reveal_parser = subparsers.add_parser("reveal")
    reveal_parser.add_argument(
        "-i",
        "--input",
        help="path to source wav file",
        required=True
    )
    reveal_parser.add_argument(
        "-o",
        "--output",
        help="path to result file",
        required=True
    )
    reveal_parser.set_defaults(func=reveal_option)

    info_parser = subparsers.add_parser("info")
    info_parser.add_argument(
        "-t",
        "--target",
        help="get info about file",
        required=True
    )
    info_parser.set_defaults(func=info_option)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse()
    try:
        args.func(args)
    except AttributeError:
        print(f"Usage: ./pypatch -h")
