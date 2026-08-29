"""
This module is responsible for parsing a source file into code blocks.

It reads a specified file and splits its content into a list of `CodeBlock`
objects, distinguishing between timed and non-timed blocks based on "#!"
delimiters.
"""
from .type_code_block import CodeBlock


def get_code_blocks(file_name:str) -> list[CodeBlock]:
    """
    Parses a file into a list of timed and non-timed code blocks.

    This function reads the content of a given file and iterates through its lines
    to identify blocks of code separated by "#!" delimiters. It then constructs a
    list of `CodeBlock` objects, each representing a distinct section of the file.

    Args:
        file_name (str): The path to the Python file to be parsed.

    Returns:
        list[CodeBlock]: A list of `CodeBlock` objects representing the parsed file.
    """
    # Get code from file.
    code = _get_file_contents(file_name)

    list_blocks = []
    code_block = CodeBlock()
    for line in code.splitlines():
        if not _is_delimeter(line):
            code_block.add_contents(line)
        else:
            list_blocks.append(code_block)
            code_block = code_block.new_with_other_mode()
            
    return list_blocks

def _get_file_contents(file_name) -> str:
    """
    Reads and returns the contents of a file.

    This is a private helper function that opens a file in read mode and returns
    its entire content as a single string.

    Args:
        file_name (str): The path to the file to be read.

    Returns:
        str: The complete content of the file.
    """
    with open(file_name, "r") as f:
        return f.read()
    
def _is_delimeter(line_contents:str):
    """
    Checks if a line is a ptymer delimiter.

    This private helper function determines if a given line of text starts with
    the "#!" delimiter, which is used to separate code blocks.

    Args:
        line_contents (str): The line of text to check.

    Returns:
        bool: True if the line is a delimiter, False otherwise.
    """
    return line_contents.startswith("#!")


if __name__ == '__main__':
    blocks = get_code_blocks('example.py')
    for block in blocks:
        print(f"TYPE: {block.time_mode}")
        print("Contents:")
        print(block.contents)
