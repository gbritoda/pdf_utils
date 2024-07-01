import os
import sys
import importlib
from pathlib import Path

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

MAIN_FILE = Path(__file__).absolute()
COMMANDS_DIR = MAIN_FILE.parent / 'commands'

class PdfUtilsException(Exception):
    pass

def parse_args(available_commands):
    main_parser = ArgumentParser(prog="pdf-utils", formatter_class=ArgumentDefaultsHelpFormatter)

    subparsers = main_parser.add_subparsers(dest="command", required=True, help="command - Command to execute")

    for subcommand in available_commands:
        # Do NOT call sub_par.parse_args anywhere
        # New commands must be with format pdfutils/commands/<subcommand>.py
        sub_par = subparsers.add_parser(subcommand, formatter_class=ArgumentDefaultsHelpFormatter)
        feature = importlib.import_module(f"pdfutils.commands.{subcommand}")
        feature.subargs(sub_par)

    parsed = main_parser.parse_args()
    feature = importlib.import_module(f"pdfutils.commands.{parsed.command}")

    return feature, parsed

def load_available_commands() -> list[str]:
    possible_commands = COMMANDS_DIR.glob(f"*.py")
    ret = []
    for cmd_path in possible_commands:
        # If the main file is of format main_<parent_folder>.py
        # That also means that <parent_folder> is the command name
        ret.append(Path(cmd_path).name.removesuffix('.py'))
    return ret

def main():
    available_commands = load_available_commands()
    feature, args = parse_args(available_commands)
    feature.main(args)


if __name__ == "__main__":
    try:
        main()
    except PdfUtilsException as e:
        if os.getenv("PYTHON_TRACEBACK", "false").lower() == "true":
            raise
        else:
            print(e, file=sys.stderr)
