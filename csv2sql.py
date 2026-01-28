import sys # For arguments.
import re # Regex.
from dateutil import parser # For date format conversions.


def load_data(file_name):
    """Opens file, stores whole file in variable, along with seperate variable for headers.
    Either returns the data from the file, or None if invalid filename.
    headers is a string of the headers.
    cleaned_data is 2D array, with each internal array being an array of the values that are to be appended to the sql."""
    file_data = []
    with open(file_name,"r") as file:
        for rows in file:
            file_data.append(rows.strip()) # Iterating through each row and appending it to the list.
    
    headers = file_data[0]
    file_data.remove(file_data[0])

    cleaned_data = []
    for entry in file_data:
        cleaned_data.append(entry.split(","))
    return headers, cleaned_data

def generate_insert(table,headers,data):
    """Generates insert statement. Returns inserts in uncleaned format."""
    inserts = [] # List to store the inserts.
    beginning_string = (f"INSERT INTO {table} ({str(headers)}) VALUES")
    inserts.append(beginning_string)
    values_to_insert = []
    for items in data:
        values_to_insert.append(str(items)) # Casts list to string.
    for items in values_to_insert:
        items = items.strip("[]") # Removing python list [] which will be printed otherwise around the items.
        inserts.append(f"({str(items)})")
    return inserts

def fix_int_float(dataset):
    """Finds potential ints and float datatypes in the insert statement, and changes it from '10' to 10, or '6.7777' to 6.7777 to make sure it'll work right with the schema."""
    int_pattern = re.compile(r'^-?\d+$')
    float_pattern = re.compile(r'^-?\d+\.\d+$')

    outside_index_counter = 0
    for insert_line in dataset:
        index_counter = 0
        insert_line = insert_line.split(",")
        for value in insert_line:
                if index_counter > len(insert_line):
                    value = value.split()
                    if re.match(float_pattern,value[index_counter]):
                        try:
                            replace_value = float(value)
                            dataset[outside_index_counter][index_counter] = replace_value
                        except TypeError:
                            continue # Preventing error on date.
                    elif re.match(int_pattern,value[index_counter]):
                        try:
                            replace_value = int(value)
                            dataset[outside_index_counter][index_counter] = replace_value
                        except TypeError:
                            continue # Preventing error on date.

                    index_counter += 1
                else:
                    break
        outside_index_counter += 1
    return dataset # Returns cleaned data.

def fix_dates(dataset):
    """Converts dates to YYYY-MM-DD ISO 8601 format."""
    def convert_non_iso_dates(text):
        def convert_match(match):
            try:
                date_obj = parser.parse(match.group(0))
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                return match.group(0)

        pattern = re.compile(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2} [A-Za-z]{3} \d{4})\b') # Regex for various date formats.
        converted_text = pattern.sub(convert_match, text)
        return converted_text
    index_num = 0
    for lines in dataset: # Iterating through dataset to change any date values.
        dataset[index_num] = convert_non_iso_dates(lines)
        index_num += 1
    return dataset

def print_to_file(filename,final_data):
    """Writes all of the insert statements to a file.
    Arguments:
        filename: filename
        final_data: Final dataset to write to file."""
    with open(filename,"w") as file:
        for tuples in final_data:
            if tuples == final_data[0]: # For printing headers only.
                file.write(tuples)
                file.write("\n")
            elif tuples == final_data[-1]:
                file.write(tuples+";") # Prints ; at end.
            else:
                file.write(tuples+",") # Otherwise, prints comma and starts a new line.
                file.write("\n")

if __name__ == "__main__":
    """Uses sys.argv arguments to build an insert statement.
    Use format source_filename table_name output_filename"""
    try:
        # Various calls to different functions to run parts of the program.
        head, data = load_data(sys.argv[1])
        inserted_array = generate_insert(sys.argv[2],head,data)
        fixed_int_float_array = fix_int_float(inserted_array)
        final_array = fix_dates(fixed_int_float_array)
        print_to_file(sys.argv[3],final_array)
    except Exception as e:
        # Basic error handling, has the downfall that all internal errors in the functions get caught here due to the vague exception clause.
        print(f"An error occured: {e}.")
        print("Arguments: python csv2sql.py.old SOURCE_FILENAME TABLE_NAME OUTPUT_FILENAME")

