# Main.py
''' Main.py
'''
import os, sys, atexit, datetime, csv, re, time, msvcrt, select, configparser
import sqlite3
import Menu, stop_work, start_work, edit_work

# Az SQLITE3 database elérési útvonala
db_file = r'C:\G\PYTHON\WT\WT.db'
tables = (	'''CREATE TABLE IF NOT EXISTS WorkTime (
	ID              	INTEGER  PRIMARY KEY AUTOINCREMENT,
	StartTime       	DATETIME,
	StopTime        	DATETIME,
	MinusTime			TIME,
	WorkTimeStop      	DATETIME,
	WorkTimeInSec   	INTEGER,
	WorkTimeHour    	TIME,
	ID_Diszpo       	INTEGER  REFERENCES Diszpo (ID) NOT DEFERRABLE INITIALLY IMMEDIATE,
	ID_ModuleName   	INTEGER  REFERENCES ModuleName (ID) NOT DEFERRABLE INITIALLY IMMEDIATE,
	ID_WorkDescription  INTEGER  REFERENCES WorkDescription (ID) NOT DEFERRABLE INITIALLY IMMEDIATE,
	StopDaWork			BOOLEAN);''',
	'''CREATE TABLE IF NOT EXISTS Diszpo (
	ID       INTEGER PRIMARY KEY AUTOINCREMENT,
	DiszpoName   TEXT,
	DiszpoID TEXT,
	Displayable BOOLEAN);''',
	'''CREATE TABLE IF NOT EXISTS WorkDescription (
	ID          INTEGER PRIMARY KEY AUTOINCREMENT,
	Description TEXT,
	Displayable BOOLEAN);''',
	'''CREATE TABLE IF NOT EXISTS ModuleName (
	ID   INTEGER PRIMARY KEY AUTOINCREMENT,
	Name TEXT,
	Displayable BOOLEAN);''',
	'''CREATE TABLE IF NOT EXISTS Version (
	db_ver INTEGER);''',
	'''CREATE VIEW IF NOT EXISTS MainView AS SELECT 
	   WorkTime.StartTime,
	   WorkTime.StopTime,
	   WorkTime.MinusTime,
	   WorkTime.WorkTimeStop,
	   WorkTime.WorkTimeInSec,
	   WorkTime.WorkTimeHour,
	   Diszpo.DiszpoID,
	   Diszpo.DiszpoName,
	   ModuleName.Name,
	   WorkDescription.Description,
	   WorkTime.StopDaWork
  FROM WorkTime
	   LEFT JOIN
	   Diszpo ON WorkTime.ID_Diszpo = Diszpo.ID
	   LEFT JOIN
	   ModuleName ON WorkTime.ID_ModuleName = ModuleName.ID
	   LEFT JOIN
	   WorkDescription ON WorkTime.ID_WorkDescription = WorkDescription.ID;''')

def main():
	# TODO: Config fájl beolvasása

	# Adatbázishoz csatlakozás, inicializálás
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		for item in tables: c.execute(item)
	except Exception as e:
		print(e)
	finally:
		conn.commit()
		conn.close()

	# Start menü
	main_menu = Menu.Menu('Munkaidő nyilvántartó', 0, ['Start','Stop','Folytat','Szerkeszt/Listáz','Statisztika','Export','Kilépés'])
	
	while(True):
		key = main_menu.ShowMenu()

		if(key == 13):
			if(main_menu.cursor == 0):
				# Start: Munkaidő kezdete
				start_work.start_work(db_file)
				pass
			elif(main_menu.cursor == 1):
				# Stop: Munkaidő vége
				stop_work.stop_work(db_file)
				pass
			elif(main_menu.cursor == 2):
				# Munkaidő folytatása: ...
				stop_work.cont_work(db_file)
				pass
			elif(main_menu.cursor == 3):
				# Szerkesztés: ...
				
				#edit_work.list_works(db_file)
				w_list = edit_work.list_works(db_file)
				edit_work.show_list_works(w_list)
				pass
			elif(main_menu.cursor == 4):
				# Statisztika: ...
				w_list = edit_work.list_works(db_file, time_recalc=1)
				edit_work.work_stat(w_list)
				pass
			elif(main_menu.cursor == 5):
				# Adatbázis exportálása txt-be: ...
				pass
			elif(main_menu.cursor == 6):
				# Munkanyilvántartó bezárása: ...
				conn.close()
				return 0
		elif(key == 27):
			pass
		elif(key == 8):
			pass
		
	conn.close()

main()