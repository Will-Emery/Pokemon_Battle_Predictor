"""Module: file_io.py
This file contains useful functions for reading and writing files. These are primarily used for debugging and gathering data."""

import pandas as pd
import numpy as np
import os
import re


def write_to_file(text, filename):
    """This function will write the text to the file
    Args:
        text: The text to write to the file
        filename: The name of the file to write to
        
    Returns:
        None"""
    #check to see if the file exists
    if not os.path.exists(filename):
        #create the file
        open(filename, "w").close()
    #write to the file
    with open(filename, "w") as file:
        file.write(text)


def append_to_file(text, filename):
    """This function will append the text to the file
    Args:
        text: The text to append to the file
        filename: The name of the file to append to
    
    Returns:
        None"""
    with open(filename, "a") as file:
        file.write(text)


def get_file_contents(filename):
    """This function will return the contents of a file as a string
    Args:
        filename: The name of the file to read
        
    Returns:
        The contents of the file as a string"""
    with open(filename, "r") as file:
        return file.read()

if __name__ == "__main__":
    append_to_file("test", "test.txt")
    append_to_file("test2", "test.txt")

