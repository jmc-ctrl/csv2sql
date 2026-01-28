import sys # For arguments
import re # Regex


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

head, data = load_data("test_file.csv")

# Attempt at cleaning data.
'''for items,item in data:
    try: # Converting any single number to an int. If it can be cast to int, its an int. Otherwise exception is triggered and its left as varchar.
        if int(item) and float(item):
            #items[item] = float(item)
            changed_item = float(item)

        elif int(item):
            #items[item] = int(item)
            changed_item = int(item)

        items[item] = changed_item
        new_items = items
        data.remove(items)
        data.append(new_items)

    except TypeError:
        pass # TLDR, leaves as string.'''

print(data)

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

    pass
final_array = generate_insert("test",head,data)
print_to_file("test_output.sql",final_array)



pass
