import os, msvcrt, calendar
from time import strptime, strftime
from datetime import date, datetime, timedelta

def stati(Work_list, specdays_fd, specdays_ew, specdays_ph):
	most = datetime.now()

	# összes havi munkaidő
	w_time = timedelta(hours=0)
	w_minustime = timedelta(hours=0)
	elozo = 0
	cnt_worked_days = 0
	for w in Work_list:
		#print(w.WorkTime)
		if(w.WorkTime != None): 
			w_time += w.WorkTime
			w_minustime += w.Time_Minus
		
		# mennyi a ledolgozott munkanapok száma?
		if elozo != w.Time_Start.day: cnt_worked_days += 1
		elozo = w.Time_Start.day	
	
	# az teljes havi munkaidő formázása
	w_time_str = timedelta_to_str(w_time)

	# az adott hónap vizsgálata
	w_year = Work_list[0].Time_Start.year
	w_month = Work_list[0].Time_Start.month
	w_max_day = calendar.monthrange(w_year, w_month)[1]
	
	# munkanapok és szabadnapok összegyűjtése az adott hónapban
	workdays = []
	offday = []
	cnt_paidholidays = 0
	cnt_workdays_bynow = 0
	for i in range(1, w_max_day+1):
		new_date = date(year=w_year, month=w_month, day=int(i))
		# munkanap
		if new_date.isoweekday() <= 5 and new_date not in specdays_fd or new_date in specdays_ew:
			workdays.append(new_date)
			if new_date in specdays_ph: cnt_paidholidays += 1
			if most.year == w_year and most.month == w_month and i <= most.day: cnt_workdays_bynow += 1
		# hétvége vagy ünnepnap
		else:
			offday.append(new_date)
	
	cnt_workdays = len(workdays)

	os.system('cls' if os.name == 'nt' else 'clear')
	title = ' Statisztika: ' + str(w.Time_Start)[:7] + ' '
	print('{:#^80s}'.format(title))

	print('Napok száma:                   ' + str(w_max_day))
	print('Munkanapok száma:              ' + str(len(workdays)), ' (' + str(len(workdays)*8) + ' óra)')
	print('Szabadnapok száma:             ' + str(len(offday)))
	print('Felhasznált szabadságok száma: ' + str(cnt_paidholidays))
	print('Csúsztatós napok száma:        ' + str(len(workdays) - cnt_paidholidays - len(offday)))
	
	# ha az adott hónapban járunk
	if most.year == w_year and most.month == w_month and most.day > 1:
		print('')
		w_time_bynow = timedelta(hours = cnt_workdays_bynow * 8)
		w_time_bynow_str = timedelta_to_str(w_time_bynow)
		
		# ha az eddig ledolgozott órák száma nagyobb, mint a szükséges
		if w_time_bynow <= (w_time + timedelta(hours = cnt_paidholidays * 8)):
			deltat = (w_time + timedelta(hours = cnt_paidholidays * 8)) - w_time_bynow
			deltat_str = timedelta_to_str(deltat)
		# ha kevesebbet dolgoztunk, mint kellett volna
		else:
			deltat = w_time_bynow - (w_time + timedelta(hours = cnt_paidholidays * 8))
			deltat_str = '-' + timedelta_to_str(deltat)

		print('Eddigi munkaórák száma:        ' + w_time_bynow_str)
		print('Eddig ledolgozott órák száma:  ' + w_time_str)
		print('Munkaidő különbözet:           ' + deltat_str)
		pass
	# ha egy régebbi hónapban járunk
	else:
		print('')
		w_time_bynow = timedelta(hours = cnt_workdays * 8)
		w_time_bynow_str = timedelta_to_str(w_time_bynow)
		
		# ha az eddig ledolgozott órák száma nagyobb, mint a szükséges
		if w_time_bynow <= (w_time + timedelta(hours = cnt_paidholidays * 8)):
			deltat = (w_time + timedelta(hours = cnt_paidholidays * 8)) - w_time_bynow
			deltat_str = timedelta_to_str(deltat)
		# ha kevesebbet dolgoztunk, mint kellett volna
		else:
			deltat = w_time_bynow - (w_time + timedelta(hours = cnt_paidholidays * 8))
			deltat_str = '-' + timedelta_to_str(deltat)
		print('Ledolgozott órák száma:        ' + w_time_str)
		print('Munkaidő különbözet:           ' + deltat_str)

	w_time_avg = w_time / cnt_worked_days
	w_time_avg_str = timedelta_to_str(w_time_avg)
	w_minustime_avg = w_minustime / cnt_worked_days
	w_minustime_avg_str = timedelta_to_str(w_minustime_avg)
	print('Átlagos munkaidő:              ' + w_time_avg_str)
	print('Átlagos ebédszünet:            ' + w_minustime_avg_str)
	print('')
	print('#'*80)
	print('A folytatáshoz nyomjon meg egy gombot...')
	msvcrt.getch()

def timedelta_to_str(tim):
	h = int(tim.total_seconds() // 3600)
	m = int(tim.total_seconds() % 3600 // 60)
	s = int(tim.total_seconds() % 3600 % 60)
	return '{:02d}:{:02d}:{:02d}'.format(h, m, s)
