# Main.py
''' Main.py
'''
import os, sys, atexit, datetime, csv, re, time, msvcrt, select, configparser
import sqlite3
import Menu, stop_work, start_work, edit_work, stati
from time import strptime, strftime
from datetime import date, datetime, timedelta

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

cfg = ('''[User data]
UID = 
user name = 
password = 
db_file = WT.db

[Special days]
# formátum: yyyy.mm.dd.

Feast days =
	2019.01.01.
	2019.03.15.
	2019.04.19.
	2019.04.22.
	2019.05.01.
	2019.06.10.
	2019.08.19.
	2019.08.20.
	2019.10.23.
	2019.11.01.
	2019.12.25.
	2019.12.26.

Extra workdays =
	2019.08.10.
	2019.12.07.
	2019.12.14.

Paid holiday =
	2019.01.02.

''')

def main():
	# Config fájl beolvasása
	try:
		config = configparser.ConfigParser()
		config.read('WT_config.ini')

		tmp = config['Special days']['Feast days'].split('\n')
		tmp = list(filter(None, tmp))
		specdays_fd = []
		for item in tmp:
			item.replace(' ', '')
			specdays_fd.append(datetime.date(datetime.strptime(item, "%Y.%m.%d.")))
		
		tmp = config['Special days']['Extra workdays'].split('\n')
		tmp = list(filter(None, tmp))
		specdays_ew = []
		for item in tmp:
			item.replace(' ', '')
			specdays_ew.append(datetime.date(datetime.strptime(item, "%Y.%m.%d.")))

		tmp = config['Special days']['Paid holiday'].split('\n')
		tmp = list(filter(None, tmp))
		specdays_ph = []
		for item in tmp:
			item.replace(' ', '')
			specdays_ph.append(datetime.date(datetime.strptime(item, "%Y.%m.%d.")))

	except Exception as e:
		print(e)
		print('Hiba a WT_config.ini beolvasása közben!')
		print('A program működése leáll, a folytatáshoz nyomjon meg egy gombot...')
		msvcrt.getch()
		return
	
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
				stati.stati(w_list, specdays_fd, specdays_ew, specdays_ph)
				#edit_work.work_stat(w_list)
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
