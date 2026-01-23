# csv2sql
Basic program to convert a csv file with columns and tuples for database into a single insert statement for rdbms.

## Usage
```bash
python3 csv2sql.py SOURCE_FILENAME TABLE_NAME OUTPUT_FILENAME
```

### TODO
- Add error handling for invalid arguments.
- Make option to format sql file as seperate lines, not one big long line.
- Unit testing (it might not work correctly or at all 😈)