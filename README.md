# dbf_to_sqlite3
A python tool to convert old DBF files to sqlite3.

# Dependencies 
* simpledbf

```
    pip3 install simpledbf
```

* python >= 3.0
* SQLalchemy >= 0.9
* Pandas >= 0.15.2

## Usage

### Positional Arguments
* FILE: The DBF file which you would like to convert

### Optional Arguments
* -f, --file The name of the new database you would like to create
* -d, --database The name of the already existing database you would like to write to
* -t, --table The name of the table you would like to create in the already existing database

### Modes
* Create New Database: Select -f, --file as your optional argument. The script will read in the DBF file and create a new database with the DBF root name as the table name
* Write to Database: Select -d, --database and -t, --table as your optional arguments. The script will connect to the database, and create the table, then write the DBF records to the new table.
