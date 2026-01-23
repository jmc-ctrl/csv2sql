### Reads .csv file and converts to single SQL insert statement.

import sys # For arguments

def open_file(file_name):
    """Opens file, stores whole file in variable.
    Either returns the data from the file, or None if invalid filename."""
    file_data = []
    with open(file_name,"r") as file:
        for rows in file:
            file_data.append(rows) # Iterating through each row and appending it to the list.
        return file_data # Returns data and closes file due to with.
    return None # None is returned for an invalid file type.

def preprocess_data(data):
    """Splits data into 2D array, index 0 is headers, index 1 is the data for inserts."""
    headers = data[0]
    actual_data = data[0:] # All things in list > index 0.

    return [[headers],[actual_data]]

def write_sql_file(output_filename,data):
    with open(output_filename,"w") as output:
        output.writelines(data) # Dumps all data to the file.

class InsertStatement:
    def __init__(self, table_name, entities, data):
        self.table_name = table_name
        self.entities = entities
        self.data = data
        self.modified_data = [] # Has to be here to work.
        self.format_values()
    
    def format_values(self):
        modified_data = []
        for i, items in enumerate(self.data): # Switched to enumerated list.
            if i == len(self.data) - 1:  # Last item can't have ,
                modified_data.append(f"({items})")
            else:
                modified_data.append(f"({items}),") 
        
        self.modified_data = modified_data  # Stored as instance variable part of class.
    
    def create_statement(self):
        # Join all formatted data elements
        values = ''.join(self.modified_data) # Variable to store inserts. Also changed to '' as per SQL syntax instead of "".
        statement = f"INSERT INTO {self.table_name} {self.entities} VALUES {values};"
        return statement


if __name__ == "__main__":
    try:
        raw_data = preprocess_data(open_file(str(sys.argv[0])))
        statement_data = InsertStatement(str(sys.argv[1]),raw_data[0],raw_data[1])
        write_sql_file(str(sys.argv[2]),statement_data.create_statement())
    except Exception as e:
        print(f"An error occured: {e}.")
        print("Arguments: python csv2sql.py SOURCE_FILENAME TABLE_NAME OUTPUT_FILENAME")