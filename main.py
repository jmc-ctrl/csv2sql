### Reads .csv file and converts to single SQL insert statement.

import sys # For arguments

def open_file(file_name):
    """Opens file, stores whole file in variable.
    Either returns the data from the file, or None if invalid filename."""
    file_data = []
    with open(file_name,"r"):
        for rows in file:
            file_data.append(rows) # Iterating through each row and appending it to the list.
        return file_data # Returns data and closes file due to with.
    return None # None is returned for an invalid file type.