from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path

LOCATION = Path(__file__).parent
app_password_path = LOCATION / Path('Files/Settings/settings.txt')
data_path = LOCATION / Path('Files/Data/data.txt')
icon_path = LOCATION / Path('Files/Images/icon.ico')

app_password_open = open(app_password_path)
app_password = app_password_open.read()
app_password_open.close()

data_open = open(data_path)
rough_data = data_open.read()
data_open.close()

rough_data2 = rough_data.split('!!!|!!!')

data = []
for i in rough_data2:
    data_one_part = i.split('||')
    data.append(data_one_part)

if len(app_password) == 0:
    PASSWORD_SET = False
else:
    PASSWORD_SET = True

continue_to_main = False

def enter(entered_password, password):
    global continue_to_main, login_win
    if entered_password == password:
        login_win.destroy()
        continue_to_main = True
    else:
        messagebox.showerror('Prijava', 'Vnesli ste napačno geslo!')

def set_password(password1, password2):
    global continue_to_main, login_win
    if password1 == password2:
        app_password_open = open(app_password_path, 'w')
        app_password_set = app_password_open.write(str(password1))
        app_password_open.close()

        login_win.destroy()
        continue_to_main = True
    else:
        messagebox.showerror('Prijava', 'Gesli se ne ujemata!')

def login():
    global login_win, password_entry, enter_button, password_entry2, no_password_label, password_label
    login_win = Tk()
    login_win.title('Prijava-PasswordSaver')
    login_win.geometry('300x180')
    login_win.iconbitmap(icon_path)
    login_win.resizable(False, False)

    if PASSWORD_SET == True:
        password_label = Label(login_win, text='Vnesite geslo spodaj.')
        password_label.pack(pady=10)

        password_entry = Entry(login_win, width=30, show='*')
        password_entry.pack(pady=30)
        
        enter_button = Button(login_win, text='VZTOPI', command=lambda:enter(password_entry.get(), app_password))
        enter_button.pack()
    else:
        login_win.geometry('300x180')
        no_password_label = Label(login_win, text='Nimate še nastavljenega gesla.\nProsimo nastavite ga spodaj.')
        no_password_label.pack(pady=10)

        password_entry = Entry(login_win, width=30, show='')
        password_entry.pack(pady=10)

        password_entry2 = Entry(login_win, width=30, show='*')
        password_entry2.pack(pady=15)
        
        enter_button = Button(login_win, text='NASTAVI IN VZTOPI', command=lambda:set_password(password_entry.get(), password_entry2.get()))
        enter_button.pack()

    login_win.mainloop()



login()
if continue_to_main == True:
    win = Tk()
    win.title('PasswordSaver')
    win.geometry('1000x500')
    win.state('zoomed')
    win.iconbitmap(icon_path)

    add_image_path = PhotoImage(file = LOCATION / Path('Files/Images/plus.png'))
    remove_image_path = PhotoImage(file = LOCATION / Path('Files/Images/trash.png'))
    show_image_path = PhotoImage(file = LOCATION / Path('Files/Images/show.png'))
    hide_image_path = PhotoImage(file = LOCATION / Path('Files/Images/hidden.png'))

    #Scrollbar
    main_frame = Frame(win)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollebar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollebar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollebar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

    seccond_frame = Frame(my_canvas)

    my_canvas.create_window((0,0), window=seccond_frame, anchor=NW)


    class Data:
        global labels, data
        def __init__(self, web_page, username, password, label_n):
            self.web_page = web_page
            self.username = username
            self.password = password
            self.label_n = label_n

            self.shown_password = str('*'*int(len(self.password)))
            self.password_is_shown = False

            self.DataFrame = Frame(seccond_frame, highlightbackground='black', highlightthickness=2)
            self.DataFrame.grid(row=int(self.label_n), column=1, pady=5)

            self.data_label = Label(self.DataFrame, text=f'Stran: {self.web_page}    Uporabniško ime: {self.username}    Geslo: {self.shown_password}', font=('Arial', 15))
            self.data_label.grid(row=0, column=1, padx=5)

            self.destroy_button = Button(self.DataFrame, image=remove_image_path, borderwidth=0, command=lambda:self.destroy())
            self.destroy_button.grid(row=0, column=3, padx=(30, 0))

            self.show_hide_button = Button(self.DataFrame, image=show_image_path, borderwidth=0, command=lambda:self.show_hide())
            self.show_hide_button.grid(row=0, column=2)
        
        def show_hide(self):
            if self.password_is_shown == False:
                self.shown_password = self.password

                self.data_label['text'] = text=f'Stran: {self.web_page}    Uporabniško ime: {self.username}    Geslo: {self.shown_password}'
                self.show_hide_button['image'] = image=hide_image_path

                self.password_is_shown = True
            else:
                self.shown_password = str('*'*int(len(self.password)))

                self.data_label['text'] = text=f'Stran: {self.web_page}    Uporabniško ime: {self.username}    Geslo: {self.shown_password}'
                self.show_hide_button['image'] = image=show_image_path

                self.password_is_shown = False
        
        def destroy(self):
            global data, labels, data_open
            self.DataFrame.destroy()
            count = 0
            for i in data:
                if i[0] == self.web_page and i[1] == self.username and i[2] == self.password:
                    del data[int(count)]
                count += 1
            
            to_write = ''
            for i in data:
                if i[0] == '':
                    pass
                else:
                    to_write = to_write+'!!!|!!!'+i[0]+'||'+i[1]+'||'+i[2]
            
            data_open = open(data_path, 'w')
            data_open.write(str(to_write))
            data_open.close()
    
    def add_data():
        global data, win2, labels, label_n
        win2 = Tk()
        win2.title('Dodaj podatke')
        win2.geometry('500x500')
        win2.resizable(False, False)

        StranLabel = Label(win2, text='Stran:  ', font=('Arial', 12, 'bold'))
        StranLabel.grid(row=0, column=1, pady=5)
        StranEntry = Entry(win2, width=100, font=('Arial', 12))
        StranEntry.grid(row=0, column=2, pady=5)

        UporabniskoImeLabel = Label(win2, text='Uporabniško ime:  ', font=('Arial', 12, 'bold'))
        UporabniskoImeLabel.grid(row=1, column=1)
        UporabniskoImeEntry = Entry(win2, width=100, font=('Arial', 12))
        UporabniskoImeEntry.grid(row=1, column=2)

        GesloLabel = Label(win2, text='Geslo:  ', font=('Arial', 12, 'bold'))
        GesloLabel.grid(row=2, column=1, pady=5)
        GesloEntry = Entry(win2, width=100, font=('Arial', 12))
        GesloEntry.grid(row=2, column=2, pady=5)

        def apply():
            global win2, label_n, data, labels, data_open
            page = StranEntry.get()
            username = UporabniskoImeEntry.get()
            password = GesloEntry.get()

            data.append([page, username, password])
            labels.append(Data(page, username, password, label_n))
            label_n += 1

            to_write = '!!!|!!!'+page+'||'+username+'||'+password

            data_open = open(data_path, 'a')
            data_open.write(to_write)
            data_open.close()

            win2.destroy()

        ApplyButton = Button(win2, text='POTRDI', bg='lightgreen', fg='black', command=apply)
        ApplyButton.grid(row=3, column=1, pady=40)


    add_button = Button(seccond_frame, image=add_image_path, borderwidth=0, command=add_data)
    add_button.grid(row=0, column=0, padx=20, pady=20)

    label_n = 1
    labels = []
    for i in data:
        try:
            labels.append(Data(i[0], i[1], i[2], label_n))
            label_n += 1
        except:
            pass
    
    def destroy_all_windows():
        try:
            win2.destroy()
        except:
            pass

        try:
            win.destroy()
        except:
            pass

    win.protocol('WM_DELETE_WINDOW', destroy_all_windows)

    win.mainloop()