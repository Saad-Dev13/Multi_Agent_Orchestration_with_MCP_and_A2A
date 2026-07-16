#Different Check Later

import os

def load_instructions_file(filename: str, default: str = "") -> str:
    """
    Loads instructions from a file. If a relative path is provided, it safely 
    resolves it relative to this script's directory to prevent path errors.
    
    Args:
        filename (str): The path or filename of the instructions file.
        default (str): Default instructions to return if the file is not found.
        
    Returns:
        str: The content of the file, or the default string if missing.
    """
    # If the path isn't absolute, anchor it to the folder where this script lives
    if not os.path.isabs(filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, filename)
    else:
        file_path = filename

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # A clean, standard warning print (no external dependencies needed)
        print(f"Warning: Instructions file '{filename}' not found at '{file_path}'. Using default.")
        return default