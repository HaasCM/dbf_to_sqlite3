#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# python tool to convert old dbf files to sqlite3

import argparse as ap
import sqlite3
import re
import os
from simpledbf import Dbf5


# simplistic function to clean error handling
def handle_error(error_bool, error_message):
  if error_bool:
    print(error_message)
    exit()

parser = ap.ArgumentParser(description='Convert .dbf files to sqlite3')
parser.add_argument('dbf_file', metavar='FILE', help='dbf file to convert')
parser.add_argument('-t', '--table', dest='table_name',metavar='TABLE', help='Name of the destination SQLite table')
parser.add_argument('-d', '--database', dest='data_base', metavar='DATABASE', help='Name of the destination SQLite database')
parser.add_argument('-f', '--file', dest='sql_name', metavar='OUT_FILE', help='Name of the output file for .sql conversion')


# args.table_name: the table where we want to write to
#
# arg.data_base: the database where the table will be created
#
# args.sql_name: if we are just creating a new database
#
args = parser.parse_args()

# regular expression for file endings
fe_regex = re.compile('[.]*')

# check if all modes are enabled
handle_error((args.sql_name is not None and args.data_base is not None and args.table_name is not None), 'multiple modes detected! Use either table and database or just file!')

# check if input is DBF
handle_error(('.DBF' not in args.dbf_file), 'Input file is not a DBF file! aborting conversion!')

# check for .DBF file existance
handle_error((not os.path.exists(args.dbf_file)), 'Input file does not exist!')

# create dbf object
dbf = Dbf5(args.dbf_file, codec='iso-8859-1')

# if mode is convert to sql file
if args.sql_name is not None:
  # check if output file is .sql file
  if fe_regex.search(args.sql_name):
    args.sql_name = os.path.splitext(args.sql_name)[0]

  # create sql and csv file names
  sql_out = args.sql_name + '.sql'
  csv_out = args.sql_name + '.csv'

  # convert dbf file to sql and csv files
  dbf.to_textsql(sql_out, csv_out)

  # creating db file
  db_out = args.sql_name + '.db'

  # check to see if database alread exists
  if not os.path.exists(db_out):
    # alerting user to process
    print('converting %s to %s' % (args.dbf_file, db_out))

    # read sql file into database
    os.system('sqlite3 %s < %s' % (db_out, sql_out))

  else:
    print('could not create %s! database alread exists!' % (db_out))
  # clean up csv and sql file
  os.remove(sql_out)
  os.remove(csv_out)
  exit()

# if other mode
else:
  # check to see if inputs are valid
  handle_error((args.data_base is None), 'no database has been specified! Aborting...')
  handle_error((args.table_name is None), 'no table has been specified! Aborting...')

  # make sure we have the .db file extension
  db_out = os.path.splitext(args.data_base)[0]+'.db'

  # check to see if database file exists
  handle_error((not os.path.exists(db_out)), 'database does not exist! Aborting...')

  # create outs for the database and the table
  table_out = args.table_name

  # alert the user to what is going on
  print('Writing ' + table_out + ' to ' + db_out)

  # writing to the database
  dbf.to_pandassql(('sqlite:///'+db_out), table=table_out)
  exit()
