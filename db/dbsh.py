#!/usr/bin/env python
# A minimal SQLite shell for experiments

import sqlite3
import sys

__version__ = "$Id: dbsh.py,v 1.2 2012/12/28 21:39:40 neill Exp $"
# $Source: /users/neill/cvshome/pylib/pydon/db/dbsh.py,v $


if len(sys.argv) < 2:
    print("Usage - dbsh.py <database>")
    sys.exit()

con = sqlite3.connect(sys.argv[1])
con.isolation_level = None
cur = con.cursor()

inbuff = ""

print("Enter your SQL commands to execute in SQLite.")
print("Enter a blank line to exit.")

while True:
    line = raw_input()
    if line == "":
        break
    inbuff += line
    if sqlite3.complete_statement(inbuff):
        try:
            inbuff = inbuff.strip()
            cur.execute(inbuff)
            if inbuff.lstrip().upper().startswith("SELECT"):
                print(cur.fetchall())
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
    inbuff = ""

con.close()
