"""
This module provides the command-line interface (CLI) for the ptymer_cli tool.

It uses argparse to define and parse command-line arguments, allowing users to
specify a file whose code blocks should be timed from the terminal.
"""
import argparse
from .exec_with_timer import control_execution_with_timer

def main():
    """
    Sets up and runs the command-line interface.

    This function initializes the argument parser to accept a file path from the
    command line. It then passes this file path to the main control function,
    which handles the execution and timing of the code blocks within the file.
    """
    parser = argparse.ArgumentParser(description="Time code blocks in a Python file.")
    parser.add_argument("file", help="The Python file to execute and time.")
    args = parser.parse_args()

    control_execution_with_timer(args.file)

if __name__ == "__main__":
    main()
