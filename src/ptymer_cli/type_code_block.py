"""
This module defines the CodeBlock class, a data structure for code blocks.
"""


class CodeBlock:
    """
    Represents a block of code from a file.

    This class serves as a data structure to hold the source code content of a block
    and its timing status, indicating whether it should be timed or not.

    Attributes:
        TIMED (str): A constant representing the timed status.
        NOTIMED (str): A constant representing the non-timed status.
        time_mode (str): The current timing mode of the block instance.
        contents (str): The source code content of the block.
    """
    # Constants
    TIMED = "timed"
    NOTIMED = "notimed"

    time_mode = NOTIMED
    contents = ""

    def new_with_other_mode(self):
        """
        Creates a new CodeBlock with an inverted time_mode.

        This method is used to alternate between timed and non-timed blocks when
        parsing a file. It returns a new instance with the opposite timing mode
        of the current instance.

        Returns:
            CodeBlock: A new instance of the `CodeBlock` class with the inverted time_mode.
        """
        new_code_block = CodeBlock()
        if self.time_mode == self.TIMED:
            new_code_block.time_mode = self.NOTIMED
        else:
            new_code_block.time_mode = self.TIMED

        return new_code_block
        
    def add_contents(self, text:str):
        """
        Appends a line of text to the code block's contents.

        Args:
            text (str): The line of code to be added to the contents.
        """
        self.contents = self.contents + text + "\n"
