from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfilename, askdirectory, askopenfilename
from customtkinter import *
from PIL import Image, ImageTk
import os
import sys


def center_window(roots, x_width, height):
    x_window_height = height
    x_window_width = x_width

    screen_width = roots.winfo_screenwidth()
    screen_height = roots.winfo_screenheight()

    x_coordinate = int((screen_width / 2) - (x_window_width / 2))
    y_coordinate = int((screen_height / 2) - (x_window_height / 2))

    roots.geometry('{}x{}+{}+{}'.format(x_window_width, x_window_height, x_coordinate, y_coordinate))


class TBApp:
    def __init__(self):
        if 'main.exe' in sys.argv[0]:
            self.path = sys.argv[0].replace('main.exe', '')
        else:
            self.path = ''
        self.must_dark()
        set_default_color_theme(self.path + 'venv/Lib/site-packages/customtkinter/assets/themes/miha.json')
        self.window = CTk()
        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.window.tk.call('wm', 'iconphoto', '.', PhotoImage(file=self.path + "images/slogo.png"))
        self.window.minsize(1050, 400)

        if self.window.winfo_screenwidth() < 1150:
            self.window.minsize(705, 400)

        self.window.title('ТБ100')
        self.window.state('zoomed')

        self.menu = Menu(self.window)
        self.window.config(menu=self.menu)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label='Новый', command=self.open_new_inst)
        self.file_menu.add_command(label='Открыть', command=self.open_inst)
        self.file_menu.add_command(label='Удалить', command=self.delete)

        self.menu.add_cascade(label='Файл', menu=self.file_menu)
        self.menu.add_command(label='О программе', command=self.get_info)
        self.menu.add_command(label='Выход', command=self.on_closing)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        self.frame_left = CTkFrame(self.window, width=680, corner_radius=0)

        self.frame_left.grid(row=0, column=0, sticky='nswe')

        self.frame_right = CTkFrame(self.window, width=280, corner_radius=0)

        self.frame_right.grid(row=0, column=2, sticky='nswe')

        self.frame_center = CTkFrame(self.window)
        self.frame_center.grid(row=0, column=1, sticky='nswe', padx=40, pady=20)

        self.remode = ttk.Button(self.frame_left, width=22, command=self.to_remode, compound=CENTER)
        self.remode.image = ImageTk.PhotoImage(Image.open(self.path + 'images/night.png'))
        self.remode['image'] = self.remode.image
        self.remode.grid(row=0, column=0, padx=20, pady=10)

        self.title_label = ttk.Button(self.frame_left, width=240, command=self.open_home)
        self.title_label.image = ImageTk.PhotoImage(Image.open(self.path + 'images/logo.png'))
        self.title_label['image'] = self.title_label.image
        self.title_label.grid(row=1, column=0, padx=10, pady=10)

        self.hello_label = CTkLabel(self.frame_center,
                                    text='Добро пожаловать в ТБ100!\nДля начала работы используйте меню.',
                                    text_font=("Roboto Medium", 60))
        self.hello_label.pack(expand=1)

        self.button_1 = CTkButton(self.frame_left, text='Создать инструктаж', command=self.open_new_inst, width=270)
        self.button_1.grid(pady=15, padx=10)

        self.button_2 = CTkButton(self.frame_left, text='Открыть инструктаж', command=self.open_inst, width=270)
        self.button_2.grid(pady=15, padx=10)

        self.button_3 = CTkButton(self.frame_left, text='Удалить инструктаж', command=self.delete, width=270)
        self.button_3.grid(pady=15, padx=10)

        self.window.bind('<Configure>', self.resize_hello_label)

        self.save_db_but = None
        self.new_ins = False
        self.now_ins = False
        self.open_ins = False
        self.hello = True
        self.text = None
        self.name_inp = None
        self.save_but = None
        self.open_but = None
        self.open_frame = None
        self.open_db_but = None
        self.font_wind = None
        self.slider = None
        self.is_dark = False
        self.open = False
        self.PATH = None
        self.memory = None
        self.path_to_open = None

        def choose_dir():
            direct = askdirectory(title='Выберите директорию...')
            if direct:
                with open(self.path + 'dir.tbconf', 'w') as fil:
                    fil.write(direct + '/TB100 Files')
                    os.mkdir(direct + '/TB100 Files')
                    self.PATH = direct + '/TB100 Files'
                    mb.destroy()

        def abort_choose():
            self.window.destroy()

        def get_help():
            messagebox.showinfo('Справка',
                                'Для дальнейшей работы с программой нужно выбрать папку, в которой \
будет создана рабочая директория для размещения в ней файлов базы данных.')

        def passive():
            pass

        if not os.path.exists(self.path + 'dir.tbconf'):
            mb = Toplevel()
            mb.title('Название')
            mb.protocol('WM_DELETE_WINDOW', passive)
            center_window(mb, 290, 110)
            mb.resizable(False, False)
            mb.transient(self.window)
            mb.grab_set()

            mb_lab = Label(mb, text='Выберите рабочую директорию.')
            mb_lab.place(x=20, y=20)

            mb_but_1 = ttk.Button(mb, text='OK', command=choose_dir)
            mb_but_1.place(x=20, y=60)

            mb_but_2 = ttk.Button(mb, text='Отмена', command=abort_choose)
            mb_but_2.place(x=110, y=60)

            mb_but_3 = ttk.Button(mb, text='Справка', command=get_help)
            mb_but_3.place(x=200, y=60)

        else:
            with open(self.path + 'dir.tbconf') as f:
                self.PATH = f.read()
        if os.path.exists(self.path + 'mode.tbconf'):
            self.remode.image = ImageTk.PhotoImage(Image.open(self.path + 'images/day.jpg'))
            self.remode['image'] = self.remode.image
            set_appearance_mode('dark')
            self.is_dark = True

        if len(sys.argv) > 1:
            self.open_new_inst()
            with open(sys.argv[1]) as f:
                if self.text is not None:
                    self.text.insert(1.0, f.read())

    def delete(self):
        self.open_inst(del_=True)

    def must_dark(self):
        if os.path.exists(self.path + 'mode.tbconf'):
            set_appearance_mode('dark')

    def on_closing(self):
        def save_changes_ok():
            with open(self.path_to_open, 'w') as f:
                f.write(self.text.get(1.0, END))
                self.window.destroy()

        def save_ok():
            save_name = asksaveasfilename(title='Сохранить файл', defaultextension='.tb',
                                          filetypes=(('TB file', '*.tb'), ('TXT File', '*.*'), ('All Files', '*.*')))
            if save_name:
                with open(save_name, 'w') as f:
                    f.write(self.text.get(1.0, END))
                    self.window.destroy()

        def save_ok_db():
            def name_ab():
                name_window.destroy()

            def name_ok():
                with open(f'{self.PATH}/{name_input.get()}.tb', 'w') as fi:
                    fi.write(self.text.get(1.0, END))
                    self.window.destroy()

            if self.name_inp.get():
                with open(f'{self.PATH}/{self.name_inp.get()}.tb', 'w') as f:
                    f.write(self.text.get(1.0, END))
                    self.window.destroy()
            else:
                name_window = Toplevel()
                name_window.title('Название')
                center_window(name_window, 230, 160)
                name_window.resizable(False, False)
                name_window.transient(self.window)
                name_window.grab_set()

                name_label = Label(name_window, text='Введите название инструктажа:')
                name_label.place(x=20, y=20)

                name_input = ttk.Entry(name_window, width=28)
                name_input.place(x=20, y=60)

                name_ok_but = ttk.Button(name_window, text='Сохранить', command=name_ok)
                name_ok_but.place(x=20, y=100)

                name_ab_but = ttk.Button(name_window, text='Отмена', command=name_ab)
                name_ab_but.place(x=120, y=100)

        def save_ab():
            save_window.destroy()

        def save_no():
            self.window.destroy()

        if self.is_dark:
            with open(self.path + 'mode.tbconf', 'w'):
                pass
        else:
            try:
                os.remove(self.path + 'mode.tbconf')
            except FileNotFoundError:
                pass

        if self.new_ins and not self.is_empty():
            save_window = Toplevel()
            save_window.title('Завершение работы')
            center_window(save_window, 280, 160)
            save_window.resizable(False, False)
            save_window.transient(self.window)
            save_window.grab_set()

            save_label = Label(save_window, text='Сохранить файл?')
            save_label.place(x=20, y=20)

            save_ok_but = ttk.Button(save_window, text='Сохранить', command=save_ok, width=18)
            save_ok_but.place(x=20, y=60)

            save_okdb_but = ttk.Button(save_window, text='Сохранить в базу', command=save_ok_db, width=18)
            save_okdb_but.place(x=150, y=60)

            save_no_but = ttk.Button(save_window, text='Не сохранять', command=save_no, width=18)
            save_no_but.place(x=20, y=100)

            save_ab_but = ttk.Button(save_window, text='Отмена', command=save_ab, width=18)
            save_ab_but.place(x=150, y=100)

        elif self.now_ins and not self.is_empty() and (self.memory != self.text.get(1.0, END)):
            save_window = Toplevel()
            save_window.title('Завершение работы')
            center_window(save_window, 330, 100)
            save_window.resizable(False, False)
            save_window.transient(self.window)
            save_window.grab_set()

            save_label = Label(save_window, text='Сохранить изменения?')
            save_label.place(x=20, y=20)

            save_ok_but = ttk.Button(save_window, text='Сохранить', command=save_changes_ok, width=13)
            save_ok_but.place(x=20, y=60)

            save_no_but = ttk.Button(save_window, text='Не сохранять', command=save_no, width=13)
            save_no_but.place(x=120, y=60)

            save_ab_but = ttk.Button(save_window, text='Отмена', command=save_ab, width=13)
            save_ab_but.place(x=220, y=60)
        else:
            self.window.destroy()

    def get_info(self):
        def get_ok():
            help_window.destroy()

        help_window = Toplevel()
        center_window(help_window, 460, 220)
        help_window.resizable(False, False)
        help_window.transient(self.window)
        help_window.grab_set()
        im_lab = Label(help_window, text='FUCKER YOU')
        im_lab.image = ImageTk.PhotoImage(Image.open(self.path + 'images/logo.png'))
        im_lab['image'] = im_lab.image
        im_lab.place(x=30, y=35)
        just_lab = Label(help_window, text='ТБ100')
        just_lab.place(x=200, y=30)
        just_lab_1 = Label(help_window, text='Программа для создания, редактирования')
        just_lab_1.place(x=200, y=50)
        just_lab_2 = Label(help_window, text='и сопровождения техник безопасности.')
        just_lab_2.place(x=200, y=70)
        just_lab_3 = Label(help_window, text='Copyright (C) 2022 Власко М. М.')
        just_lab_3.place(x=200, y=90)
        exit_button = ttk.Button(help_window, width=15, text='OK', command=get_ok)
        exit_button.place(x=200, y=150)

    def to_remode(self):
        if self.is_dark:
            self.remode.image = ImageTk.PhotoImage(Image.open(self.path + 'images/night.png'))
            self.remode['image'] = self.remode.image
            set_appearance_mode('System')
            self.is_dark = False
        else:
            self.remode.image = ImageTk.PhotoImage(Image.open(self.path + 'images/day.jpg'))
            self.remode['image'] = self.remode.image
            set_appearance_mode('dark')
            self.is_dark = True

    def resize_hello_label(self, par=None):
        if self.hello:
            self.hello_label.configure(text_font=("Roboto Medium", int(self.window.winfo_width() / 65)))
        if self.window.winfo_screenwidth() < 1150:
            self.title_label.configure(width=165)
            self.button_1.configure(width=140)
            self.button_2.configure(width=140)
            self.frame_right.configure(width=165)
        if self.window.winfo_screenwidth() < 1150 and self.new_ins:
            self.name_inp.configure(width=140)
            self.save_but.configure(width=140)
            self.save_db_but.configure(width=140)
            return par

    def save_new_file(self):
        name = asksaveasfilename(title='Сохранить файл', defaultextension='.tb',
                                 filetypes=(('TB file', '*.tb'), ('TXT File', '*.*'), ('All Files', '*.*')))
        if name:
            with open(name, 'w') as fo:
                incl = self.text.get('1.0', END)
                fo.write(incl)
                self.open_new_inst(flag=True, title=os.path.basename(name), path=name)
                self.text.insert(1.0, incl)

    def is_empty(self):
        for i in self.text.get(1.0, END):
            if i not in (' ', '\n'):
                return False
        return True

    def save_new_file_to_db(self):
        if not self.is_empty():
            if self.name_inp.get() == '':
                messagebox.showwarning('INFO', 'Введите название инструктажа!')
            else:
                with open(f'{self.PATH}/{self.name_inp.get()}.tb', 'w') as fo:
                    incl = self.text.get('1.0', END)
                    fo.write(incl)
                    self.open_new_inst(flag=True, title=f'{self.name_inp.get()}.tb',
                                       path=f'{self.PATH}/{self.name_inp.get()}.tb')
                    self.text.insert(1.0, incl)
        else:
            messagebox.showwarning('INFO', 'Вы пытаетесь сохранить пустой инструктаж!')

    def slider_event(self, par):
        self.text.configure(text_font=('Roboto', -int(self.slider.get())))
        self.font_wind.configure(text=f'Размер шрифта: {int(self.slider.get())}')
        return par

    def open_new_inst(self, flag=False, title=None, path=None):
        def save_changes():
            with open(path, 'w') as f:
                f.write(self.text.get(1.0, END))
                messagebox.showinfo('INFO', 'Изменения успешно сохранены.')

        self.is_open_inst()
        self.is_home()
        self.is_now_inst()
        self.is_new_inst()
        self.path_to_open = path
        if not self.new_ins:
            if flag:
                self.now_ins = True
                self.window.title(f'ТБ100 - {title}')
                self.save_but = CTkButton(self.frame_right, text='Сохранить изменения', width=280,
                                          command=save_changes)
                self.save_but.grid(row=1, column=0, padx=10, pady=20, sticky='nswe')

                self.text = CTkTextbox(self.frame_center, width=6000, height=1500, text_font=('Roboto', -13))
                self.text.pack(expand=1)

                self.slider = CTkSlider(self.frame_right, from_=1, to=100, command=self.slider_event)
                self.slider.set(13)
                self.slider.grid(row=2, column=0, padx=10, pady=20, sticky='nswe')

                self.font_wind = CTkLabel(self.frame_right, text='Размер шрифта: 13', text_font=('Roboto', -16))
                self.font_wind.grid(row=3, column=0, padx=10, pady=15, sticky='nswe')

            else:
                self.new_ins = True
                self.name_inp = CTkEntry(self.frame_right, width=280, placeholder_text='Название...')
                self.name_inp.grid(row=0, column=0, padx=10, pady=20, sticky='nswe')

                self.save_but = CTkButton(self.frame_right, text='Сохранить файл', command=self.save_new_file)
                self.save_but.grid(row=1, column=0, padx=10, pady=20, sticky='nswe')

                self.save_db_but = CTkButton(self.frame_right, text='Сохранить в базу',
                                             command=self.save_new_file_to_db)
                self.save_db_but.grid(row=2, column=0, padx=10, pady=20, sticky='nswe')

                self.text = CTkTextbox(self.frame_center, width=6000, height=1500, text_font=('Roboto', -13))
                self.text.pack(expand=1)

                self.slider = CTkSlider(self.frame_right, from_=1, to=100, command=self.slider_event)
                self.slider.set(13)
                self.slider.grid(row=3, column=0, padx=10, pady=20, sticky='nswe')

                self.font_wind = CTkLabel(self.frame_right, text='Размер шрифта: 13', text_font=('Roboto', -16))
                self.font_wind.grid(row=4, column=0, padx=10, pady=10, sticky='nswe')

    def open_inst(self, del_=False):
        def is_file():
            file_name = askopenfilename(title='Открыть', defaultextension='.tb',
                                        filetypes=(('TB file', '*.tb'), ('TXT File', '*.*'), ('All Files', '*.*')))
            if file_name:
                with open(file_name) as f:
                    self.is_open_inst()
                    self.open_new_inst(flag=True, title=os.path.basename(file_name), path=file_name)
                    self.text.insert(1.0, f.read())
                    self.memory = self.text.get(1.0, END)

        def is_db():
            def open_ch_db():
                name = list_box.get()
                with open(f'{self.PATH}/{name}') as f:
                    self.is_open_inst()
                    self.open_new_inst(flag=True, title=name, path=f'{self.PATH}/{name}')
                    self.text.insert(1.0, f.read())
                    self.memory = self.text.get(1.0, END)

            open_but.destroy()
            open_db_but.destroy()
            list_box = CTkComboBox(self.open_frame, values=os.listdir(self.PATH), state='readonly', width=200)

            list_box.grid(pady=30, padx=30)
            ok_but = CTkButton(self.open_frame, text='Открыть', width=100, command=open_ch_db)
            ok_but.grid(pady=30, padx=30)

        def is_del():
            def del_ch_db():
                name = list_box.get()
                os.remove(f'{self.PATH}/{name}')
                messagebox.showinfo('INFO', f'Инструктаж "{name}" успешно удалён.')

            list_box = CTkComboBox(self.open_frame, values=os.listdir(self.PATH), state='readonly', width=200)
            list_box.grid(pady=30, padx=30)

            ok_but = CTkButton(self.open_frame, text='Удалить', width=100, command=del_ch_db)
            ok_but.grid(pady=30, padx=30)

        self.is_open_inst()
        self.is_home()
        self.is_now_inst()
        self.is_new_inst()
        if not self.open and not del_:
            self.open_frame = CTkFrame(self.frame_center, height=400)
            self.open_frame.pack(expand=1)
            open_but = CTkButton(self.open_frame, text='Выбрать файл', width=200, command=is_file)
            open_but.grid(pady=30, padx=30)
            open_db_but = CTkButton(self.open_frame, text='Выбрать из базы', width=200, command=is_db)
            open_db_but.grid(pady=30, padx=30)
            self.open = True
        if del_:
            self.open_frame = CTkFrame(self.frame_center, height=400)
            self.open_frame.pack(expand=1)
            self.open = True
            is_del()

    def open_home(self):
        self.is_now_inst()
        self.is_open_inst()
        self.is_new_inst()
        if not self.hello:
            self.hello = True
            self.hello_label = CTkLabel(self.frame_center,
                                        text='Добро пожаловать в ТБ100!\nДля начала работы используйте меню.',
                                        text_font=("Roboto Medium", 60))
            self.hello_label.pack(expand=1)

    def is_home(self):
        if self.hello:
            self.hello_label.destroy()
            self.hello = False

    def is_new_inst(self):
        if self.new_ins:
            self.text.destroy()
            self.name_inp.destroy()
            self.save_but.destroy()
            self.save_db_but.destroy()
            self.slider.destroy()
            self.font_wind.destroy()
            self.new_ins = False

    def is_now_inst(self):
        if self.now_ins:
            self.text.destroy()
            self.save_but.destroy()
            self.window.title('ТБ100')
            self.slider.destroy()
            self.font_wind.destroy()
            self.now_ins = False

    def is_open_inst(self):
        if self.open:
            self.open_frame.destroy()
            self.open = False


if __name__ == '__main__':
    app = TBApp()
    app.window.mainloop()
