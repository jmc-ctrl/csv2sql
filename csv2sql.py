import sys # For arguments
import re
from dateutil import parser


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
    '''columns_string = str
    headers = headers.split(",")
    for column in headers:
        columns_string = column
        if not column == headers[-1]:
            columns_string = columns_string,","'''
    columns_string = str(headers)
    final_array = []
    beginning_string = (f"INSERT INTO {table} ({columns_string}) VALUES")
    final_array.append(beginning_string)
    values_to_insert = []
    for items in data:
        values_to_insert.append(str(items))
    for items in values_to_insert:
        items = items.strip("[]")
        '''print(f"({str(items)})", end ="")
        print(",")'''
        final_array.append(f"({str(items)})")
    return final_array

def fix_int_float(dataset):
    """Finds potential ints and float datatypes in the insert statement, and changes it from '10' to 10, or '6.7777' to 6.7777 to make sure it'll work right with the schema."""
    int_pattern = re.compile(r'^-?\d+$')
    float_pattern = re.compile(r'^-?\d+\.\d+$')

    outside_index_counter = 0
    for insert_line in dataset:
        index_counter = 0
        for value in insert_line:
            value = value.split(",")
            if re.match(int_pattern,value[index_counter]):
                replace_value = int(value)
                dataset[outside_index_counter][index_counter] = replace_value
            elif re.match(float_pattern,value[index_counter]):
                replace_value = float(value)
                dataset[outside_index_counter][index_counter] = replace_value
            index_counter += 1
        outside_index_counter += 1
    return dataset # Returns cleaned data.

def fix_dates(dataset):
    def convert_non_iso_dates(text):
        def convert_match(match):
            try:
                date_obj = parser.parse(match.group(0))
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                return match.group(0)

        pattern = re.compile(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2} [A-Za-z]{3} \d{4})\b')
        converted_text = pattern.sub(convert_match, text)
        return converted_text
    index_num = 0
    for lines in dataset:
        dataset[index_num] = convert_non_iso_dates(lines)
        index_num += 1
    return dataset

#final_array = fix_int_float(generate_insert("test",head,data))
def print_to_file(filename,final_data):
    with open(filename,"w") as file:
        for tuples in final_data:
            if tuples == final_data[0]: # For printing headers only.
                file.write(tuples)
                file.write("\n")
            elif tuples == final_data[-1]:
                file.write(tuples+";")
            else:
                file.write(tuples+",")
                file.write("\n")

if __name__ == "__main__":
    """Uses sys.argv arguments to build an insert statement."""
    try:
        head, data = load_data(sys.argv[1])
        inserted_array = generate_insert(sys.argv[2],head,data)
        final_array = fix_dates(inserted_array)
        print_to_file(sys.argv[3],final_array)
    except Exception as e:
        print(f"An error occured: {e}.")
        print("Arguments: python csv2sql.py SOURCE_FILENAME TABLE_NAME OUTPUT_FILENAME")

