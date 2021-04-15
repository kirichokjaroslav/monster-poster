#!/bin/bash
##
if [ -f /app/data/employees.sqlite3 ]; then
  rm -f /app/extras/employees.sqlite3
  ln -s /app/data/employees.sqlite3 /app/extras/employees.sqlite3
else
  mv /app/extras/employees.sqlite3 /app/data/employees.sqlite3
  ln -s /app/data/employees.sqlite3 /app/extras/employees.sqlite3
fi

python launch.py -r
