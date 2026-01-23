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

def preprocess_data(data):
    """Splits data into 2D array, index 0 is headers, index 1 is the data for inserts."""
    headers = data[0]
    actual_data = data[0:] # All things in list > index 0.

    return [[headers],[actual_data]]



class InsertStatement:
    string(table_name)
    string(entities) 
    list(data) 

    def __init__(self, table_name, entities, data):
        self.table_name = table_name
        self.entities = entities
        self.data = format_values(data)

    def format_values(data):
        modified_data = []
        for items in data:
            if items == data[-1]:
                modified_data.append(f"({items})") # No , allowed for last values.
            else:
                modified_data.append(f"({items}),\n") # Otherwise allow the , for multiple inserts.


        data = modified_data # Overwriting original data with modified data.

    def create_statement(self):
        statement = f"INSERT INTO {table_name} {entities} VALUES {data};"
        return statement


# Testing functionality.
testing = preprocess_data(open_file("test_file.csv"))
statement_data = InsertStatement("sample_table",testing[0],testing[1])
print(statement_data.create_statement)