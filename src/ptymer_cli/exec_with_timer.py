"""
This module contains the core logic for executing and timing code blocks.

It orchestrates the process of parsing a file, identifying code blocks,
and using the `ptymer` library to time the execution of designated blocks,
while maintaining a shared context for the execution.
"""
from .get_code_blocks import get_code_blocks, CodeBlock
from ptymer import Timer


def control_execution_with_timer(file_name:str):
    """
    Controls the execution and timing of code blocks from a file.

    This function serves as the main entry point for the timing logic. It retrieves
    code blocks from the specified file, cleans up any empty blocks, and then
    iterates through them, executing each one. Timed blocks are executed with a
    timer, while others are executed normally.

    Args:
        file_name (str): The path to the Python file to be executed and timed.

    Notes:
        - A shared dictionary `context_code` is used as the namespace for `exec`
          to maintain state (e.g., variables) across different code blocks.
    """
    # Context for code.
    context_code = {}
    code_blocks = get_code_blocks(file_name)
    
    # Remove blocks without contents.
    _clean_nulls_code_blocks(code_blocks)

    for block in code_blocks:
        if block.time_mode == CodeBlock.TIMED:
            context_code =_exec_code_with_timer(block.contents, context_code)
        else:
            # Exec without timer.
            exec(block.contents, context_code)
    

def _clean_nulls_code_blocks(code_blocks:list[CodeBlock]):
    """
    Removes empty code blocks from a list.

    This private helper function iterates through a list of `CodeBlock` objects
    and removes any that have no content, modifying the list in-place.

    Args:
        code_blocks (list[CodeBlock]): The list of code blocks to be cleaned.
    """
    for i, block in enumerate(code_blocks):
        if block.contents == "":
            del code_blocks[i]

def _exec_code_with_timer(code:str, dict_namespace:dict):
    """
    Executes a block of code with a timer and prints the result.

    This function initializes a `ptymer.Timer`, starts it, executes the provided
    code string using `exec`, stops the timer, and prints the elapsed time and
    the executed code.

    Args:
        code (str): The string of code to be executed and timed.
        dict_namespace (dict): The dictionary to be used as the namespace for the
                               `exec` function, allowing context to be preserved.

    Returns:
        dict: The updated namespace dictionary after the code execution.
    """
    t = Timer()

    # Init timer.
    t.start()

    # Execution.
    exec(code, dict_namespace)

    # Stop timer.
    result = t.stop()

    # Print informations.
    print("===================TIMER_STATUS===================")
    print(f"Elapsed time: {result} seconds")
    print(f"CODE:\n{code}")
    print("==================================================")
    print("--------------------------------------------------")

    return dict_namespace


if __name__ == "__main__":
    control_execution_with_timer("example.py")
