import Menu, edit_work

from uptime import boottime
from time import strptime, strftime
from datetime import datetime, timedelta


#from datetime import timedelta

#import datetime
import sqlite3, sys, os, msvcrt

class Work:
	def __init__(self, db_conn = None, LastRowID=None, Time_Start=None, Time_Stop=None, Time_Minus=None, Time_WorkStop=None, WorkTime=None, WorkTime_InSec=None, WorkTime_InHour=None, Diszpo_ID=None, Diszpo_Name=None, Work_On=None, Work_Desc=None):
		self.db_conn = db_conn
		self.LastRowID = LastRowID
		self.Time_Start = Time_Start
		self.Time_Stop = Time_Stop
		self.Time_Minus = Time_Minus
		self.Time_WorkStop = Time_WorkStop
		self.WorkTime = WorkTime
		self.WorkTime_InSec = WorkTime_InSec
		self.WorkTime_InHour = WorkTime_InHour
		self.Diszpo_ID = Diszpo_ID
		self.Diszpo_Name = Diszpo_Name
		self.Work_On = Work_On
		self.Work_Desc = Work_Desc

def load_from_db(Work):
	view_WorkTime = """ SELECT StartTime, StopTime, MinusTime, WorkTimeStop, WorkTimeInSec, WorkTimeHour, ID_Diszpo, ID_ModuleName, ID_WorkDescription
						FROM WorkTime
						WHERE ID = (?) 
					"""
	view_Diszpo = "SELECT DiszpoName, DiszpoID FROM Diszpo WHERE ID = (?)"
	view_ModuleName = "SELECT Name FROM ModuleName WHERE ID = (?)"
	view_WorkDescription = "SELECT Description FROM WorkDescription WHERE ID = (?)"

	s = Work.db_conn.execute(view_WorkTime, [Work.LastRowID]).fetchone()
	if(s[0] != None): Work.Time_Start = datetime.strptime(s[0], "%Y-%m-%d %H:%M:%S")
	if(s[1] != None): Work.Time_Stop = datetime.strptime(s[1], "%Y-%m-%d %H:%M:%S")
	if(s[2] != None):
		time = s[2].split(':')
		Work.Time_Minus = timedelta(hours=int(time[0]), minutes=int(time[1]), seconds=int(time[2]))
	if(s[3] != None): Work.Time_WorkStop = datetime.strptime(s[3], "%Y-%m-%d %H:%M:%S")
	if(s[4] != None): Work.WorkTime_InSec = s[4]
	if(s[5] != None): Work.WorkTime_InHour = s[5]
	
	tmp = Work.db_conn.execute(view_Diszpo, [s[6]]).fetchone()
	if(tmp != None): 
		Work.Diszpo_Name = tmp[0]
		Work.Diszpo_ID = tmp[1]
	tmp = Work.db_conn.execute(view_ModuleName, [s[7]]).fetchone()
	if(tmp != None): Work.Work_On = tmp[0]
	tmp = Work.db_conn.execute(view_WorkDescription, [s[8]]).fetchone()
	if(tmp != None): Work.Work_Desc = tmp[0]

def load_from_db_old(Work):
	# StartTime
	db_str = Work.db_conn.execute("SELECT StartTime FROM WorkTime WHERE ID = (?)", [Work.LastRowID]).fetchone()[0]
	if(db_str != None): Work.Time_Start = datetime.strptime(db_str, "%Y-%m-%d %H:%M:%S")
	# StopTime
	db_str = Work.db_conn.execute("SELECT StopTime FROM WorkTime WHERE ID = (?)", [Work.LastRowID]).fetchone()[0]
	if(db_str != None): Work.Time_Stop = datetime.strptime(db_str, "%Y-%m-%d %H:%M:%S")
	# MinusTime
	db_str = Work.db_conn.execute("SELECT MinusTime FROM WorkTime WHERE ID = (?)", [Work.LastRowID]).fetchone()[0]
	if(db_str != None):
		time = db_str.split(':')
		Work.Time_Minus = timedelta(hours=int(time[0]), minutes=int(time[1]), seconds=int(time[2]))
	# WorkTimeStop
	db_str = Work.db_conn.execute("SELECT WorkTimeStop FROM WorkTime WHERE ID = (?)", [Work.LastRowID]).fetchone()[0]
	if(db_str != None): Work.Time_WorkStop = datetime.strptime(db_str, "%Y-%m-%d %H:%M:%S")
	# WorkTime: ez egy számolt érték és nincs benne az AB-ban
	# WorkTimeInSec
	db_str = Work.db_conn.execute("SELECT WorkTimeInSec FROM WorkTime WHERE ID = (?)", [Work.LastRowID]).fetchone()[0]
	if(db_str != None): Work.WorkTime_InSec = db_str
	# WorkTimeHour
	db_str = Work.db_conn.execute("SELECT WorkTimeHour FROM WorkTime WHERE ID = (?)", [Work.LastRowID]).fetchone()[0]
	if(db_str != None): Work.WorkTime_InHour = db_str
		
	# DiszpoName, DiszpoID
	db_str = Work.db_conn.execute("SELECT DiszpoName, DiszpoID FROM Diszpo WHERE ID = (SELECT ID_Diszpo FROM WorkTime WHERE ID = (?))", [Work.LastRowID]).fetchone()
	Work.Diszpo_Name = db_str[0]
	Work.Diszpo_ID = db_str[0]
	# ModuleName
	db_str = Work.db_conn.execute("SELECT Name FROM ModuleName WHERE ID = (SELECT ID_ModuleName FROM WorkTime WHERE ID = (?))", [Work.LastRowID]).fetchone()
	Work.Work_On = db_str[0]
	# WorkDescription
	db_str = Work.db_conn.execute("SELECT Description FROM WorkDescription WHERE ID = (SELECT ID_WorkDescription FROM WorkTime WHERE ID = (?))", [Work.LastRowID]).fetchone()
	Work.Work_Desc = db_str[0]
	pass

def FindLastCursor(Work, col_list, MainTable, MainCol, SubTable, SubCol):
	# Megkeresi az utolsó érvényes cellát a 'table' táblában, a 'col' oszlopban
	# A visszatérési érték a cella tartalma lesz vagy 0
	try:
		cursor = Work.db_conn.execute("SELECT " + ", ".join(SubCol) + " FROM {} WHERE ID=(SELECT {} FROM {} WHERE ID=(SELECT MAX(ID) FROM {} WHERE {} IS NOT NULL))".format(SubTable, MainCol, MainTable, MainTable, MainCol))
		menu_cursor = col_list.index(cursor.fetchone())
		return menu_cursor 
	except:
		return 0

def get_diszpo(ActWork):
	# Diszpó, Diszpó ID kiválasztása vagy új felvétele

	# Itt kellene az AB-ből kiolvasni a meglévőeket
	col_list = ActWork.db_conn.execute("SELECT DiszpoName, DiszpoID FROM Diszpo ORDER BY ID ASC").fetchall()
	# itt az utolsó diszpóra ugorhatna a cursor
	if((ActWork.Diszpo_ID, ActWork.Diszpo_Name) in col_list):
		last_cursor = col_list.index((ActWork.Diszpo_ID, ActWork.Diszpo_Name))
	else:
		last_cursor = FindLastCursor(ActWork, col_list, 'WorkTime', 'ID_Diszpo', 'Diszpo', ('DiszpoName','DiszpoID'))

	diszpo_menu = Menu.Menu(['Diszpó név', 'Diszpó ID'], last_cursor, list(col_list), En_New=True, En_Edit=True, En_Del=False)
	# Bővíthető lista -> ha az 'ÚJ ELEM'-re léptek, akkor fel kell venni egy új elemet
	while(True):
		key = diszpo_menu.ShowMenu()
		if(key == 13): # elem kiválasztása - ENTER
			break
		elif(key == 8): # Backspace
			return 8
		elif(key == 65): # új elem felvétele - F7
			new_item = diszpo_menu.Item_New()
			ActWork.db_conn.execute("INSERT INTO Diszpo (DiszpoName, DiszpoID) VALUES (?,?)", new_item)
			ActWork.db_conn.commit()
		elif(key == 62): # elem szerkesztése - F4
			old_item = diszpo_menu.col_list[diszpo_menu.cursor]
			new_item = diszpo_menu.Item_Edit()
			ActWork.db_conn.execute("UPDATE Diszpo SET DiszpoName=?, DiszpoID=? WHERE DiszpoName=? AND DiszpoID=?",new_item + old_item)
			ActWork.db_conn.commit()
		elif(key == 66): # elem törlése - F8
			diszpo_menu.Item_Del()
		elif(key == 27): # vissza lépés - ESC
			return 27

	# Work class feltöltése
	ActWork.Diszpo_Name = diszpo_menu.col_list[diszpo_menu.cursor][0]
	ActWork.Diszpo_ID = diszpo_menu.col_list[diszpo_menu.cursor][1]
	return 0

def get_module(ActWork):
	#col_list = ['UPS', 'Adatgyűjtő', 'Csipi', 'Csupi']
	
	# Itt kellene az AB-ből kiolvasni a meglévőeket
	col_list = ActWork.db_conn.execute("SELECT Name FROM ModuleName ORDER BY ID ASC").fetchall()
	# itt az utolsó diszpóra ugorhatna a cursor
	if((ActWork.Work_On, ) in col_list):
		last_cursor = col_list.index((ActWork.Work_On, ))
	else:
		last_cursor = FindLastCursor(ActWork, col_list, 'WorkTime', 'ID_ModuleName', 'ModuleName', ('Name',))
	module_menu = Menu.Menu('Module', last_cursor, list(col_list), En_New=True, En_Edit=True, En_Del=False)

	while(True):
		key = module_menu.ShowMenu()
		if(key == 13): # elem kiválasztása - ENTER
			break
		elif(key == 8): # Backspace
			return 8
		elif(key == 65): # új elem felvétele - F7
			new_item = module_menu.Item_New()
			ActWork.db_conn.execute("INSERT INTO ModuleName (Name) VALUES (?)", new_item)
			ActWork.db_conn.commit()
		elif(key == 62): # elem szerkesztése - F4
			old_item = module_menu.col_list[module_menu.cursor]
			new_item = module_menu.Item_Edit()
			ActWork.db_conn.execute("UPDATE ModuleName SET Name=? WHERE Name=?",new_item + old_item)
			ActWork.db_conn.commit()
		elif(key == 66): # elem törlése - F8
			module_menu.Item_Del()
		elif(key == 27): # kilépés a menübe - ESC
			return 27

	# Work class feltöltése
	ActWork.Work_On = module_menu.col_list[module_menu.cursor][0]
	return 0

def get_work(ActWork):
	#col_list = ['kapcsi rajz', 'nyákterv', 'doku készít', 'takarít']
	col_list = ActWork.db_conn.execute("SELECT Description FROM WorkDescription ORDER BY ID ASC").fetchall()
	if((ActWork.Work_Desc, ) in col_list):
		last_cursor = col_list.index((ActWork.Work_Desc, ))
	else:
		last_cursor = FindLastCursor(ActWork, col_list, 'WorkTime', 'ID_WorkDescription', 'WorkDescription', ('Description',))
	work_menu = Menu.Menu('Munkaleírás', last_cursor, list(col_list), En_New=True, En_Edit=True, En_Del=False)

	while(True):
		key = work_menu.ShowMenu()
		if(key == 13): # elem kiválasztása - ENTER
			break
		elif(key == 8): # Backspace
			return 8
		elif(key == 65): # új elem felvétele - F7
			new_item = work_menu.Item_New()
			ActWork.db_conn.execute("INSERT INTO WorkDescription (Description) VALUES (?)", new_item)
			ActWork.db_conn.commit()
		elif(key == 62): # elem szerkesztése - F4
			old_item = work_menu.col_list[work_menu.cursor]
			new_item = work_menu.Item_Edit()
			ActWork.db_conn.execute("UPDATE WorkDescription SET Description=? WHERE Description=?", new_item + old_item)
			ActWork.db_conn.commit()
		elif(key == 66): # elem törlése - F8
			work_menu.Item_Del()
		elif(key == 27): # vissza lépés - ESC
			return 27

	# Work class feltöltése
	ActWork.Work_Desc = work_menu.col_list[work_menu.cursor][0]
	return 0

def time_calc(ActWork, time_opt=True):
	
	# az utolsó Time_Start lekérdezése
	#db_str = ActWork.db_conn.execute("SELECT StartTime FROM WorkTime WHERE ID = (?)", [ActWork.LastRowID]).fetchone()[0]
	#ActWork.Time_Start = datetime.strptime(db_str, "%Y-%m-%d %H:%M:%S")
	# aktuális idő lekérdezése
	#ActWork.Time_Stop = datetime.now().replace(microsecond=0, second=0)
	#ActWork.Time_Start = datetime(2018, 11, 9, 9, 0, 0)
	#ActWork.Time_Stop = datetime(2018, 11, 9, 17, 59, 0)

	# ebédidő kiszámítása, formátum: HH:MM:SS
	# munkaidő optimalizáció
	if time_opt == True or ActWork.Time_Minus == None:
		wt = ActWork.Time_Stop - ActWork.Time_Start
		if(wt <= timedelta(hours=3, minutes=0)):
			ActWork.Time_Minus = timedelta(minutes=0)
		elif(wt > timedelta(hours=3, minutes=0) and wt <= timedelta(hours=8, minutes=35)):
			ActWork.Time_Minus = timedelta(minutes=35)
		elif(wt > timedelta(hours=8, minutes=35) and wt <= timedelta(hours=9, minutes=0)): 
			ActWork.Time_Minus = wt - timedelta(hours=8)
		else:
			ActWork.Time_Minus = timedelta(hours=1)
	else:
		pass
	
	# munkaidő kiszámítása
	ActWork.Time_WorkStop = ActWork.Time_Stop - ActWork.Time_Minus
	ActWork.WorkTime = ActWork.Time_WorkStop - ActWork.Time_Start
	ActWork.WorkTime_InSec = str(int(ActWork.WorkTime.total_seconds()))
	# formátum: HH:MM:SS
	h = int(ActWork.WorkTime.total_seconds() // 3600)
	m = int(ActWork.WorkTime.total_seconds() % 3600 // 60)
	s = int(ActWork.WorkTime.total_seconds() % 3600 % 60)
	assert(h*3600 + m*60 + s == int(ActWork.WorkTime.total_seconds()))
	ActWork.WorkTime_InHour = '{:02d}:{:02d}:{:02d}'.format(h, m, s)

def summary(Work, title=' --- ', En_Edit=False):
	# az adott munka kiiratása
	os.system('cls' if os.name == 'nt' else 'clear')
	print('{:#^80s}'.format(title))
	print('Munkaidő kezdete:', Work.Time_Start)
	print('Munkaidő vége:   ', Work.Time_Stop)
	print('Ebédidő:         ', Work.Time_Minus, '(HH:MM:SS)')
	print('Munkaidő:        ', Work.WorkTime_InSec,'s')
	print('Munkaidő:        ', Work.WorkTime_InHour,'(HH:MM:SS)')
	print()
	print('Diszpó név:      ', Work.Diszpo_Name)
	print('Diszpó ID:       ', Work.Diszpo_ID)
	print('Module:          ', Work.Work_On)
	print('Munkaleírás:     ', Work.Work_Desc)
	print('#'*80)
	print('\nFőmenü (ESC), Vissza (BACKSPACE), Tovább (ENTER)',end='')
	if(En_Edit == True): print(', Szerkesztés [F4]')

	while(True):
		key = ord(msvcrt.getch())
		# Nem = ESC -> Nem írunk semmit az AB-ba, vissza a főmenübe
		if(key == 27): return 27
		# Igen = ENTER -> végrehajtódik az AB-be a beírás
		elif(key == 13): return 13
		# Igen = ENTER -> végrehajtódik az AB-be a beírás
		elif(key == 8): return 8
		elif(key == 62 and En_Edit == True): return 62
		elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
			key = ord(msvcrt.getch())

def comit_to_db(ActWork):
	time_stop = None
	time_minus = None
	time_workstop = None

	# Ha nincsenek értékek, akkor None-t kell adni az AB-nak
	if(ActWork.Time_Stop != None): time_stop = datetime.strftime(ActWork.Time_Stop, "%Y-%m-%d %H:%M:%S")
	if(ActWork.Time_Minus != None): time_minus = str(ActWork.Time_Minus)
	if(ActWork.Time_WorkStop != None): time_workstop = str(ActWork.Time_WorkStop)

	# WorkTime tábla feltöltése az időkkel
	ActWork.db_conn.execute("UPDATE WorkTime SET StopTime=?, MinusTime=?, WorkTimeStop=?, WorkTimeInSec=?, WorkTimeHour=? WHERE ID=?", 
		[time_stop,                                         # StopTime
		time_minus,                                         # Ebédidő
		time_workstop,                                      # A munka vége - ebédidő
		ActWork.WorkTime_InSec,							    # WorkTimeInSec
		ActWork.WorkTime_InHour,							# WorkTimeHour
		ActWork.LastRowID])									# WHERE
	
	# WorkTime tábla feltöltése a Diszpóval
	#cursor = conn.execute("SELECT ID FROM Diszpo WHERE DiszpoName = ? AND DiszpoID = ?", (ActWork.Diszpo_Name, ActWork.Diszpo_ID))
	#DiszpoID = cursor.fetchone()[0]
	ActWork.db_conn.execute("UPDATE WorkTime SET ID_Diszpo = (SELECT ID FROM Diszpo WHERE DiszpoName = ? AND DiszpoID = ?) WHERE ID = ?",
		(ActWork.Diszpo_Name, 
		ActWork.Diszpo_ID, 
		ActWork.LastRowID))
	
	# WorkTime tábla feltöltése az Modullal
	ActWork.db_conn.execute("UPDATE WorkTime SET ID_ModuleName=(SELECT ID FROM ModuleName WHERE Name=?) WHERE ID=?",
		(ActWork.Work_On, 
		ActWork.LastRowID))

	# WorkTime tábla feltöltése a munkaleírással
	ActWork.db_conn.execute("UPDATE WorkTime SET ID_WorkDescription=(SELECT ID FROM WorkDescription WHERE Description=?) WHERE ID=?",
		(ActWork.Work_Desc, 
		ActWork.LastRowID))

	# beírás az adatbázisba
	ActWork.db_conn.commit()

def stop_work(db_file):
	# adatbázis
	conn = sqlite3.connect(db_file)
	
	# Az utolsó ID (azaz utolsó sor) lekérdezése (a következőkben ezt töltjük fel)
	LastRowID = conn.execute("SELECT MAX(ID) FROM WorkTime").fetchone()[0]
	# Ha még nem volt elindítva munka, akkor vissza a főmenübe
	if(LastRowID == None):
		print('Még nincs megkezdett munka az adatbázisban!')
		print('\nPress any key to continue...',end='')
		msvcrt.getch()
		conn.close()
		return -1
	
	# munka részletek bevitele
	ActWork = Work()
	ActWork.db_conn = conn
	ActWork.LastRowID = LastRowID

	# Ha már volt valamilyen érték felvéve ehhez a recordhoz
	load_from_db(ActWork)
	# Ha már volt StopTime, akkor már egyszer le volt zárva!
	# ezt nem kellene elrontani, erre a Folytatás menüpontot kell használni
	if(ActWork.Time_Stop != None):
		print('\nAz utolsó munka már le van zárva!')
		print('Ha ezt a munkát szeretné folytatni, akkor a folytatás menüpontot válassza!')
		print('Ha új munkát szeretne indítani, akkor az Új munka menüpontot válassza!\n')
		print('Nyomjon meg egy gombot a folytatáshoz!')
		msvcrt.getch()
		conn.close()
		return -1

	key = 0
	menu_num = 0
	while(True):
		# itt visszalépünk a főmenübe
		if(menu_num == -1): 
			conn.close()
			return -1
		# Diszpó kiválasztása (Diszpo Name, Diszpo ID)
		elif(menu_num == 0): key = get_diszpo(ActWork)
		# Module kiválasztása (WorkOn)
		elif(menu_num == 1): key = get_module(ActWork)
		# Munkaleírás kiválasztása (WorkDescription)
		elif(menu_num == 2): key = get_work(ActWork)
		# Új munka összegzése (Summary)
		elif(menu_num == 3): 
			ActWork.Time_Stop = datetime.now().replace(microsecond=0, second=0)
			time_calc(ActWork)
			key = summary(ActWork, ' SUMMÁRUM ')

		if(menu_num == 4): break
		elif(key == 27): menu_num = -1
		elif(key == 8): menu_num -= 1
		else: menu_num += 1
		
	comit_to_db(ActWork)
	ActWork.db_conn.close()
	# itt lehet feltölteni a munkanaplóba
	#up.up(ActWork)

	return 0

def cont_work(db_file):
