from uptime import boottime
from datetime import datetime
import sqlite3, msvcrt, os

def start_work(db_file):
    ''' 
    start_work() függvény
    # Működés: az adatbázisba felvesz egy új sort, és ennek a sornak a StartTime értékét feltölti
     - ha a Boot idő előbb történt, mint a jelenlegi idő, akkor a Time_boot kerül az AB-be
     - ha a ...
    
    # Paraméterek: db_file (str)
    # Visszatérési értékek: nincs
    # TODO: nincs
    '''
    os.system('cls' if os.name == 'nt' else 'clear')
    # Boottime meghatározása, megjegyzés: Ehhez Windows-ban ki kell kapcsolni a hibernációt???
    Time_Boot = boottime().replace(microsecond=0, second=0)
    print('Boot idő:     ' + str(Time_Boot))

    # Aktuális idő meghatározása
    Time_Act = datetime.now().replace(microsecond=0, second=0)
    print('Aktuális idő: ' + str(Time_Act))

    # Utolsó (legnagyobb ID-jű) start idő (StartTime) lekérése. Ilyenből csak egy lehet, mert az ID mindenhol egyedi.
    conn = sqlite3.connect(db_file)
    Time_LastStart_str = conn.execute("SELECT StartTime FROM WorkTime WHERE ID = (SELECT MAX(ID) FROM WorkTime WHERE StartTime IS NOT NULL)").fetchone()[0]
    
    # nincs még egyetlen StartTime érték sem
    if(Time_LastStart_str == None):
        Time_Start = Time_Act
    # ha már volt StartTime érték az AB-ban
    else:
        # a stringet átalakítjuk datetime értékre
        Time_LastStart = datetime.strptime(Time_LastStart_str, "%Y-%m-%d %H:%M:%S")
        # ha az utolsó start korábban volt mint a boot idő
        if(Time_Boot <= Time_LastStart):
            Time_Start = Time_Act
        # ha az utolsó start később volt mint a boot idő
        else:
            Time_Start = Time_Boot
    print('StartTime:    ' + str(Time_Start))
    print('#'*80)
    print('Elvet [ESC], Jóváhagy [ENTER]')

    while(True):
        key = ord(msvcrt.getch())
        # Nem = ESC -> Nem írunk semmit az AB-ba, vissza a főmenübe
        if(key == 27): return 27
        # Igen = ENTER -> végrehajtódik az AB-be a beírás
        elif(key == 13): break
        elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
            key = ord(msvcrt.getch())

    conn.execute("INSERT INTO WorkTime (StartTime) VALUES (?)", [str(Time_Start)])
    conn.commit()
    conn.close()