# csv2sql
Basic program to convert a csv file with columns and tuples for database into a single insert statement for rdbms.

## Usage
```bash
python3 csv2sql.py SOURCE_FILENAME TABLE_NAME OUTPUT_FILENAME
```

### TODO
- Add error handling for invalid arguments.
- Fix function to convert string to int and float, or else everything is a varchar except dates.
- Unit testing (it might not work correctly or at all 😈)
