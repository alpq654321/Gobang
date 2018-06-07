import sqlite3

dbConn = sqlite3.connect('match.db')
if 1==1:
	dbConn.execute('''
					create table tbMatch
				   (username varchar(100) not null,
				    password varchar(100) not null)'''
					)