import os, sys, atexit, datetime, csv, re, time, msvcrt, select, configparser, calendar
import sqlite3
import Menu, stop_work, start_work
from time import strptime, strftime
from datetime import datetime, timedelta

def edit_work(Edit_Work):
	#conn = sqlite3.connect(db_file)
	#id = 27

	#Edit_Work = stop_work.Work()
	#Edit_Work.db_conn = conn
	#Edit_Work.LastRowID = id

	#stop_work.load_from_db(Edit_Work)

	conn = Edit_Work.db_conn

	key = 0
	menu_num = 0
	while(True):
		# itt visszalépünk a főmenübe
		if(menu_num == -1): 
			conn.close()
			return -1
		# Diszpó kiválasztása (Diszpo Name, Diszpo ID)
		elif(menu_num == 0): key = stop_work.get_diszpo(Edit_Work)
		# Module kiválasztása (WorkOn)
		elif(menu_num == 1): key = stop_work.get_module(Edit_Work)
		# Munkaleírás kiválasztása (WorkDescription)
		elif(menu_num == 2): key = stop_work.get_work(Edit_Work)
		# Új munka összegzése (Summary)
		elif(menu_num == 3): 
			pass
			#key = summary(Edit_Work)

		if(menu_num == 4): break
		elif(key == 27): menu_num = -1
		elif(key == 8): menu_num -= 1
		else: menu_num += 1
		
	stop_work.comit_to_db(Edit_Work)
	#conn.close()
	pass

def list_works(db_file, time_recalc=0, beg=None, end=None):
	# TODO: ki kell választani azokat a munkákat, amik a két dátum között vannak és egyenkét be kell tenni ezeket
	conn = sqlite3.connect(db_file)

	if(beg != None and end != None):
		# itt helyes formátumú beg és end paraméterre számítunk
		pass
	else:
		# itt nem adott meg beg és end paramétert
		while(True):
			print('Adja meg a listázandó évet és hónapot (formátum: yyyy-mm):')
			tmp = input()
			try:
                		date = tmp.split('-')
                		r = calendar.monthrange(int(date[0]), int(date[1]))
                		beg = date[0] + '-' + date[1] + '-01 00:00:00'
                		end = date[0] + '-' + date[1] + '-' + str(r[1]) + ' 23:59:59'    
				break
			except Exception as e:
				print(e)

	rows = conn.execute("SELECT ID FROM WorkTime WHERE StartTime BETWEEN (?) AND (?)", [beg, end]).fetchall()

	# ha nem sikerült egy recordot sem betölteni, akkor hibát jelzünk
	if(len(rows) == 0):
		os.system('cls' if os.name == 'nt' else 'clear')
		print('{:#^80s}'.format(' Munka szerkesztése '))
		print('Nincs a keresésnek megfelelő találat!\n')
		print('A folytatáshoz nyomjon meg egy gombot...')
		msvcrt.getch()
		conn.close()
		return -1

	# készítünk egy listát, amiben Work objektumokat tárolunk
	Work_list = []
	for row in rows:
		# létrehozunk egy Work objektumot
		Work = stop_work.Work()
		Work.LastRowID = row[0]
		Work.db_conn = conn

		# Work objektum feltöltése az adatbázisból
		stop_work.load_from_db(Work)
		# itt újra számolódnak az idők (Start és Stop time-ból)
		if(time_recalc != 0 and Work.Time_Start != None and Work.Time_Stop != None):
			stop_work.time_calc(Work)
		Work_list.append(Work)
	return Work_list

def show_list_works(Work_list):
	key = 0
	i = 0
	while(True):
		if(i > len(Work_list)-1 or i == -1 or key == 27):
			break

		title = ' Munka szerkesztése: ' + str(i+1) + '/' + str(len(Work_list)) + ' '
		key = stop_work.summary(Work_list[i], title, En_Edit=True)
		if(key == 13):      # ENTER - továbblépés
			i += 1
		elif(key == 8):     # BACKSPACE - visszalépés
			i -= 1
		elif(key == 62):    # F4 - szerkesztés
			edit_work(Work_list[i])
			pass
	# itt bezárjuk a db connectiont
	Work_list[0].db_conn.close()

def work_stat(Work_list):
	# összes havi munkaidő
	w_time = timedelta(hours=0)
	for w in Work_list:
		#print(w.WorkTime)
		if(w.WorkTime != None): w_time += w.WorkTime
	
	# az teljes havi munkaidő formázása
	h = int(w_time.total_seconds() // 3600)
	m = int(w_time.total_seconds() % 3600 // 60)
	s = int(w_time.total_seconds() % 3600 % 60)
	w_time_str = '{:02d}:{:02d}:{:02d}'.format(h, m, s)

	os.system('cls' if os.name == 'nt' else 'clear')
	title = ' Statisztika: ' + str(w.Time_Start)[:7] + ' '
	print('{:#^80s}'.format(title))
	print('Összes munkaidő: ' + w_time_str)
	print('')
	print('#'*80)
	print('A folytatáshoz nyomjon meg egy gombot...')
	msvcrt.getch()
