import os, msvcrt

class Menu:
    def __init__(self, title, cursor, col_list, En_New=False, En_Edit=False, En_Del=False):
        self.title = title
        self.cursor = int(cursor)
        self.col_list = col_list
        
        #self.const_begin = '{:#^80s}'.format(' ' + self.title + ' ')
        # ha nem kapunk 1D-s tömböt akkor itt elkészítjük
        titles = ''
        j = 0
        if type(self.title) == str:
            self.title = [self.title]
        for item in self.title:
            titles = titles + item
            if(len(self.title) > 1 and j < len(self.title) - 1):
                    titles = titles + '; '
            j = j + 1
        self.const_begin = '{:#^80s}'.format(' ' + titles + ' ')

        self.const_end = '#'*80
        self.En_New = En_New
        self.En_Edit = En_Edit
        self.En_Del = En_Del

    def Item_New(self):
        '''
        Item_New függvény
        TODO
        '''
        i = 0
        be_list = []
        for item in self.title:            
            while(True):
                msg = '> új ' + item + ': '
                be = input(msg)

                # ismétlődés keresése
                ism = False
                for item2 in self.col_list:
                    if(item2[i] == be): 
                        ism = True
                        # az első találat után nem keresünk tovább
                        break

                if(be == ""):
                    print("Nem lehet üres!")
                elif(ism == True):
                    print("Nem lehet azonos")
                else:
                    #self.col_list[self.cursor][i] = be
                    be_list.append(be)
                    break
            i = i + 1
        self.col_list.append(tuple(be_list))
        self.cursor = len(self.col_list) - 1
        return tuple(be_list)

    def Item_Edit(self):
        '''
        Item_Edit függvény
        TODO
        '''
        #if type(msg) is not list: to_select = [ to_select ]
        i = 0
        new_items = []
        for item in self.title:            
            while(True):
                msg = '> ' + item + ' szerkesztése: '
                be = input(msg)

                # ismétlődés keresése
                ism = False
                for item2 in self.col_list:
                    if(item2[i] == be): 
                        ism = True
                        # az első találat után nem keresünk tovább
                        break

                if(be == ""):
                    print("Nem lehet üres!")
                elif(ism == True):
                    print("Nem lehet azonos")
                else:
                    #self.col_list[self.cursor][i] = be
                    break
            new_items.append(be)
            i = i + 1
        self.col_list[self.cursor] = tuple(new_items)
        return tuple(new_items)

    def Item_Del(self):
        '''
        Item_Del függvény
        TODO
        '''
        if(input('> Biztosan törlöd a kijelölt elemet? (i/n) ') == 'i'):
            del self.col_list[self.cursor]
            if(self.cursor == len(self.col_list)): 
                self.cursor -= 1

    def ShowMenu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        # TODO: En_New menu
        #if(self.En_New == True): self.col_list.append('[ÚJ ELEM]')
        self.RefreshMenu()
        
        while True:
            key = ord(msvcrt.getch())
            if key == 27: #ESC
                return key
            elif key == 8: # Backspace
                return key
            elif key == 13: #Enter
                # TODO: itt ellenőrizni kellene a duplikációt új elemnél
                return key
            elif(key == 62 and self.En_Edit == True): #F4 szerkesztés
                if(len(self.col_list) != 0): 
                    return key
                else: print('Nincs elem a listában!')
            elif(key == 65 and self.En_New == True): #F7 új elem
                return key
            elif(key == 66 and self.En_Del == True): #F8 törlés
                if(len(self.col_list) != 0):
                    return key
                else: 
                    print('Nincs elem a listában!')
            elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
                key = ord(msvcrt.getch())
                if key == 80: #Down arrow
                    if(self.cursor == len(self.col_list)-1):
                        pass # itt nem kell menüt frissíteni
                    else:
                        self.cursor = self.cursor + 1
                        self.RefreshMenu()
                elif key == 72: #Up arrow
                    if(self.cursor == 0): 
                        pass # itt nem kell menüt frissíteni
                    else:
                        self.cursor = self.cursor - 1
                        self.RefreshMenu()
            
    def RefreshMenu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        # ha nem kapunk 2D tömböt akkor itt elkészítjük
        i = 0 
        for item in self.col_list:
            if type(self.col_list[i]) == str:
                self.col_list[i] = [self.col_list[i]]
            i = i + 1
        print(self.const_begin)
        
        i = 0
        # sorok kiiratása
        for item in self.col_list:
            row = ''
            j = 0
            for item_in_row in item:
                row = row + item_in_row
                if(len(item) > 1 and j < len(item) - 1):
                    row = row + '; '
                j = j + 1
            # számozás hozzáadása
            row = '{:5}{}'.format((str(i+1) + '.'), row)
            # amin áll a kurzor azt a sor kiszínezzük
            if(self.cursor == i): 
                print('\x1b[6;30;42m' + row + '\x1b[0m')
            # amin nem azt normálisan íratjuk ki
            else:
                print(row)
            i = i + 1
        print(self.const_end)
        
        # Ha engedélyezve vannak a lista menüelemek módosításai
        if(self.En_New or self.En_Edit or self.En_Del):
            if(self.En_New): print('#     SZERKESZTÉS (F4)     |',end='')
            else: print('#' + ' '*26 + '|',end='')
            if(self.En_Edit): print('       ÚJ ELEM (F7)      |',end='')
            else: print(' '*25 + '|',end='')
            if(self.En_Del): print('       TÖRLÉS (F8)       #',end='')
            else: print(' '*25 + '#',end='')
            print('\n' + self.const_end)
            