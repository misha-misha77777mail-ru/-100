from tkinter import *
from _tkinter import TclError
from tkinter import messagebox, ttk
from tkinter.font import families
from tkinter.filedialog import asksaveasfilename, askdirectory, askopenfilename
from json import load, loads, dump
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
            self.path = sys.argv[0].replace('main.exe', '') + '/'
        else:
            self.path = ''
        self.must_dark()
        set_default_color_theme(self.path + 'style/miha.json')
        self.window = CTk()
        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.window.tk.call('wm', 'iconphoto', '.', PhotoImage(file=self.path + "images/slogo.png"))
        self.window.minsize(1100, 400)

        if self.window.winfo_screenwidth() < 1150:
            self.window.minsize(705, 400)

        self.window.title('ТБ100')
        self.window.state('zoomed')

        self.menu = Menu(self.window)
        self.window.config(menu=self.menu)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.edit_menu = Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label='Назад      (Ctrl+z)', command=self.control_z)
        self.edit_menu.add_command(label='Вперёд   (Ctrl+b)', command=self.control_s_z)
        self.file_menu.add_command(label='Новый', command=self.open_new_inst)
        self.file_menu.add_command(label='Открыть', command=self.open_inst)
        self.file_menu.add_command(label='Удалить', command=self.delete)

        self.menu.add_cascade(label='Файл', menu=self.file_menu)
        self.menu.add_cascade(label='Редактировать', menu=self.edit_menu)
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

        self.title_button = ttk.Button(self.frame_left, width=240, command=self.open_home)
        self.title_button.image = ImageTk.PhotoImage(Image.open(self.path + 'images/logo.png'))
        self.title_button['image'] = self.title_button.image
        self.title_button.grid(row=1, column=0, padx=10, pady=10)

        self.hello_label = CTkLabel(self.frame_center,
                                    text='Добро пожаловать в ТБ100!\nДля начала работы используйте меню.',
                                    text_font=("Roboto Medium", 60))
        self.hello_label.pack(expand=1)

        self.button_1 = CTkButton(self.frame_left, text='Создать документ', command=self.open_new_inst, width=270)
        self.button_1.grid(pady=15, padx=10)

        self.button_2 = CTkButton(self.frame_left, text='Открыть документ', command=self.open_inst, width=270)
        self.button_2.grid(pady=15, padx=10)

        self.button_3 = CTkButton(self.frame_left, text='Удалить документ', command=self.delete, width=270)
        self.button_3.grid(pady=15, padx=10)

        self.window.bind('<Configure>', self.resize_hello_label)
        self.inf_flag = False
        self.help_window = None
        self.window.bind('<F1>', self.get_info)

        self.save_to_db_button = None
        self.text = None
        self.font_box = None
        self.name_input = None
        self.save_button = None
        self.open_button = None
        self.open_frame = None
        self.open_from_db_button = None
        self.font_info = None
        self.font_slider = None
        self.list_box = None

        self.is_new_doc = False
        self.is_opened_doc = False
        self.is_hello_page = True
        self.is_dark_mode = False
        self.is_open_request = False

        self.HOME_PATH = None
        self.memory = None
        self.path_to_open = None
        self.now_font = None
        self.return_ = [None]
        self.ret_index = -1

        def choose_dir():
            direct = askdirectory(title='Выберите директорию...')
            if direct:
                with open(self.path + 'dir.tbconf', 'w') as fil:
                    fil.write(direct + '/TB100 Files')
                    os.mkdir(direct + '/TB100 Files')
                    self.HOME_PATH = direct + '/TB100 Files'
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

            mb.iconbitmap("images/icon.ico")

        else:
            with open(self.path + 'dir.tbconf') as f:
                self.HOME_PATH = f.read()
        if os.path.exists(self.path + 'mode.tbconf'):
            self.remode.image = ImageTk.PhotoImage(Image.open(self.path + 'images/day.jpg'))
            self.remode['image'] = self.remode.image
            set_appearance_mode('dark')
            self.is_dark_mode = True
        if len(sys.argv) > 1:
            if '.tb' in sys.argv[1]:
                with open(sys.argv[1]) as file:
                    self.open_new_inst(flag=True, is_tb=True, title=os.path.basename(sys.argv[1]), path=sys.argv[1])
                    if self.text is not None and self.font_slider is not None and self.font_box is not None \
                            and self.font_info is not None:
                        data = load(file)
                        self.open_new_inst(flag=True, is_tb=True, title=os.path.basename(sys.argv[1]), path=sys.argv[1])
                        self.text.insert(1.0, data['text'])
                        self.text.configure(text_font=(data['font'], -data['font-size']))
                        self.font_slider.set(data['font-size'])
                        self.font_info.configure(text=f'Размер шрифта: {int(self.font_slider.get())}')
                        self.font_box.entry.delete(0, END)
                        self.font_box.entry.insert(0, data['font'])
                        self.memory = (self.text.get(1.0, END), int(self.font_slider.get()), self.font_box.entry.get())
            else:
                self.open_new_inst(flag=True, title=os.path.basename(sys.argv[1]), path=sys.argv[1])
                if self.text is not None and self.font_slider is not None and self.font_box is not None:
                    with open(sys.argv[1]) as f:
                        self.is_open_inst()
                        self.text.insert(1.0, f.read())
                        self.memory = (self.text.get(1.0, END), int(self.font_slider.get()), self.font_box.entry.get())

    def delete(self):
        self.open_inst(del_=True)

    def must_dark(self):
        if os.path.exists(self.path + 'mode.tbconf'):
            set_appearance_mode('dark')

    def get_json(self):
        return {
                'text': self.text.get(1.0, END),
                'font-size': int(self.font_slider.get()),
                'font': self.font_box.entry.get()
                    }

    def on_closing(self):
        def save_changes_ok():
            if '.tb' in self.path_to_open:
                dump_data = self.get_json()
                with open(self.path_to_open, 'w') as f:
                    dump(dump_data, f)
                    self.window.destroy()
            else:
                with open(self.path_to_open, 'w') as f:
                    f.write(self.text.get(1.0, END))
                    self.window.destroy()

        def save_ok():
            save_name = asksaveasfilename(title='Сохранить файл', defaultextension='.tb',
                                          filetypes=(('TB file', '*.tb'), ('TXT File', '*.*'), ('All Files', '*.*')))
            if save_name:
                if '.tb' in save_name:
                    dump_data = self.get_json()

                    with open(save_name, 'w') as f:
                        dump(dump_data, f)
                        self.window.destroy()
                else:
                    with open(save_name, 'w') as f:
                        f.write(self.text.get(1.0, END))
                        self.window.destroy()

        def save_ok_db():
            def name_ab():
                name_window.destroy()

            dump_data = self.get_json()

            def name_ok():
                try:
                    with open(f'{self.HOME_PATH}/{name_input.get()}.tb', 'w') as fi:
                        dump(dump_data, fi)
                        self.window.destroy()
                except OSError:
                    messagebox.showwarning('INFO', 'Недопустимое имя файла!')

            if self.name_input.get():
                try:
                    with open(f'{self.HOME_PATH}/{self.name_input.get()}.tb', 'w') as f:
                        dump(dump_data, f)
                        self.window.destroy()
                except OSError:
                    messagebox.showwarning('INFO', 'Недопустимое имя файла!')
            else:
                name_window = Toplevel()
                name_window.title('Название')
                center_window(name_window, 230, 160)
                name_window.resizable(False, False)
                name_window.transient(self.window)
                name_window.grab_set()

                name_label = Label(name_window, text='Введите название документа:')
                name_label.place(x=20, y=20)

                name_input = ttk.Entry(name_window, width=28)
                name_input.place(x=20, y=60)

                name_ok_but = ttk.Button(name_window, text='Сохранить', command=name_ok)
                name_ok_but.place(x=20, y=100)

                name_ab_but = ttk.Button(name_window, text='Отмена', command=name_ab)
                name_ab_but.place(x=120, y=100)

                name_window.iconbitmap("images/icon.ico")

        def save_ab():
            save_window.destroy()

        def save_no():
            self.window.destroy()

        if self.is_dark_mode:
            with open(self.path + 'mode.tbconf', 'w'):
                pass
        else:
            try:
                os.remove(self.path + 'mode.tbconf')
            except FileNotFoundError:
                pass

        if self.is_new_doc and not self.is_empty():
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

            save_window.iconbitmap("images/icon.ico")

        elif self.is_opened_doc and not self.is_empty() and (
                self.memory != (self.text.get(1.0, END), int(self.font_slider.get()), self.font_box.entry.get())):
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

            save_window.iconbitmap("images/icon.ico")
        else:
            self.window.destroy()

    def get_info(self, par=None):
        def get_ok():
            self.help_window.destroy()
        if not self.inf_flag:
            self.inf_flag = True
            self.help_window = Toplevel()
            center_window(self.help_window, 460, 220)
            self.help_window.resizable(False, False)
            self.help_window.transient(self.window)
            self.help_window.grab_set()
            im_lab = Label(self.help_window, text='FUCKER YOU')
            im_lab.image = ImageTk.PhotoImage(Image.open(self.path + 'images/logo.png'))
            im_lab['image'] = im_lab.image
            im_lab.place(x=30, y=35)
            just_lab = Label(self.help_window, text='ТБ100')
            just_lab.place(x=200, y=30)
            just_lab_1 = Label(self.help_window, text='Программа для создания, редактирования')
            just_lab_1.place(x=200, y=50)
            just_lab_2 = Label(self.help_window, text='и сопровождения техник безопасности.')
            just_lab_2.place(x=200, y=70)
            just_lab_3 = Label(self.help_window, text='Copyright (C) 2022 Власко М. М.')
            just_lab_3.place(x=200, y=90)
            exit_button = ttk.Button(self.help_window, width=15, text='OK', command=get_ok)
            exit_button.place(x=200, y=150)
            self.help_window.iconbitmap("images/icon.ico")

        else:
            self.inf_flag = False
            get_ok()

        return par

    def to_remode(self):
        if self.is_dark_mode:
            self.remode.image = ImageTk.PhotoImage(Image.open(self.path + 'images/night.png'))
            self.remode['image'] = self.remode.image
            set_appearance_mode('System')
            self.is_dark_mode = False
        else:
            self.remode.image = ImageTk.PhotoImage(Image.open(self.path + 'images/day.jpg'))
            self.remode['image'] = self.remode.image
            set_appearance_mode('dark')
            self.is_dark_mode = True

    def resize_hello_label(self, par=None):
        if self.is_hello_page:
            self.hello_label.configure(text_font=("Roboto Medium", int(self.window.winfo_width() / 65)))
        if self.window.winfo_screenwidth() < 1150:
            self.title_button.configure(width=165)
            self.button_1.configure(width=140)
            self.button_2.configure(width=140)
            self.frame_right.configure(width=165)
        if self.window.winfo_screenwidth() < 1150 and self.is_new_doc:
            self.name_input.configure(width=140)
            self.save_button.configure(width=140)
            self.save_to_db_button.configure(width=140)
            return par

    def save_new_file(self):
        name = asksaveasfilename(title='Сохранить файл', defaultextension='.tb',
                                 filetypes=(('TB file', '*.tb'), ('TXT File', '*.*'), ('All Files', '*.*')))
        if name:
            if '.tb' in name:
                dump_data = self.get_json()
                with open(name, 'w') as file:
                    dump(dump_data, file)
                    self.open_new_inst(flag=True, is_tb=True, title=os.path.basename(name), path=name)
                    self.text.insert(1.0, dump_data['text'])
                    self.text.configure(text_font=(dump_data['font'], -dump_data['font-size']))
                    self.font_slider.set(dump_data['font-size'])
                    self.font_info.configure(text=f'Размер шрифта: {int(self.font_slider.get())}')
                    self.font_box.entry.delete(0, END)
                    self.font_box.entry.insert(0, dump_data['font'])
            else:
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
            if self.name_input.get() == '':
                messagebox.showwarning('INFO', 'Введите название документа!')
            else:
                try:
                    dump_data = self.get_json()
                    with open(f'{self.HOME_PATH}/{self.name_input.get()}.tb', 'w') as file:
                        dump(dump_data, file)
                        self.open_new_inst(flag=True, is_tb=True, title=f'{self.name_input.get()}.tb',
                                           path=f'{self.HOME_PATH}/{self.name_input.get()}.tb')
                        self.text.insert(1.0, dump_data['text'])
                        self.text.configure(text_font=(dump_data['font'], -dump_data['font-size']))
                        self.font_slider.set(dump_data['font-size'])
                        self.font_info.configure(text=f'Размер шрифта: {int(self.font_slider.get())}')
                        self.font_box.entry.delete(0, END)
                        self.font_box.entry.insert(0, dump_data['font'])
                except OSError:
                    messagebox.showwarning('INFO', 'Недопустимое имя файла!')
        else:
            messagebox.showwarning('INFO', 'Вы пытаетесь сохранить пустой документ!')

    def slider_event(self, par):
        self.text.configure(text_font=(self.now_font, -int(self.font_slider.get())))
        self.font_info.configure(text=f'Размер шрифта: {int(self.font_slider.get())}')
        return par

    def control_z(self, par=None):
        try:
            if abs(self.ret_index) != len(self.return_):
                self.ret_index -= 1
                self.text.textbox.delete(1.0, END)
                self.text.insert(1.0, self.return_[self.ret_index])
        except IndexError:
            pass
        except TclError:
            pass
        return par

    def control_s_z(self, par=None):
        try:
            if self.ret_index < -1:
                self.ret_index += 1
                self.text.textbox.delete(1.0, END)
                self.text.insert(1.0, self.return_[self.ret_index])
        except IndexError:
            pass
        except TclError:
            pass
        return par

    def open_new_inst(self, is_tb=False, flag=False, title=None, path=None):
        def change_font():
            if self.font_box.entry.get() in families():
                self.text.configure(text_font=(self.font_box.entry.get(), -int(self.font_slider.get())))
                self.now_font = self.font_box.entry.get()

        def save_changes():
            dump_data = self.get_json()
            if self.memory != (self.text.get(1.0, END), int(self.font_slider.get()), self.font_box.entry.get()):
                if is_tb:
                    with open(path, 'w') as f:
                        self.memory = (self.text.get(1.0, END), int(self.font_slider.get()), self.font_box.entry.get())
                        dump(dump_data, f)
                        messagebox.showinfo('INFO', 'Изменения успешно сохранены.')
                else:
                    with open(path, 'w') as f:
                        self.memory = (self.text.get(1.0, END), int(self.font_slider.get()), self.font_box.entry.get())
                        f.write(self.text.get(1.0, END))
                        messagebox.showinfo('INFO', 'Изменения успешно сохранены.')

        self.is_open_inst()
        self.is_home()
        self.is_now_inst()
        self.is_new_inst()
        self.path_to_open = path
        self.return_ = [None]
        self.ret_index = -1

        def change_event(par=None):
            try:
                ind = self.return_[-1]
            except IndexError:
                ind = None
            if self.text.get(1.0, END)[:-1] != ind:
                if self.ret_index < -1:
                    mas = []
                    for i in range(0, len(self.return_) - abs(self.ret_index) + 1):
                        mas.append(self.return_[i])
                    self.return_ = mas
                    self.return_.append(self.text.get(1.0, END)[:-1])
                    self.ret_index = -1
                else:
                    self.return_.append(self.text.get(1.0, END)[:-1])
            return par

        if not self.is_new_doc:
            if flag:
                self.is_opened_doc = True
                self.window.title(f'ТБ100 - {title}')
                self.save_button = CTkButton(self.frame_right, text='Сохранить изменения', width=280,
                                             command=save_changes)
                self.save_button.grid(row=1, column=0, padx=10, pady=20, sticky='nswe')

                self.text = CTkTextbox(self.frame_center, width=6000, height=1500, text_font=('Roboto', -13))
                self.text.pack(expand=1)

                self.font_slider = CTkSlider(self.frame_right, from_=1, to=100, command=self.slider_event)
                self.font_slider.set(13)
                self.font_slider.grid(row=2, column=0, padx=10, pady=20, sticky='nswe')

                self.font_info = CTkLabel(self.frame_right, text='Размер шрифта: 13', text_font=('Roboto', -16))
                self.font_info.grid(row=3, column=0, padx=10, pady=15, sticky='nswe')

                self.font_box = CTkComboBox(self.frame_right, values=families(), command=change_font)
                self.font_box.entry.delete(0, END)
                self.font_box.entry.insert(0, 'Roboto')
                self.font_box.grid(row=4, column=0, padx=10, pady=15, sticky='nswe')

                self.window.bind('<KeyPress>', change_event)
                self.window.bind('<Control-Z>', self.control_z)
                self.window.bind('<Control-KeyPress-b>', self.control_s_z)

            else:
                self.is_new_doc = True
                self.name_input = CTkEntry(self.frame_right, width=280, placeholder_text='Название...')
                self.name_input.grid(row=0, column=0, padx=10, pady=20, sticky='nswe')

                self.save_button = CTkButton(self.frame_right, text='Сохранить файл', command=self.save_new_file)
                self.save_button.grid(row=1, column=0, padx=10, pady=20, sticky='nswe')

                self.save_to_db_button = CTkButton(self.frame_right, text='Сохранить в базу',
                                                   command=self.save_new_file_to_db)
                self.save_to_db_button.grid(row=2, column=0, padx=10, pady=20, sticky='nswe')

                self.text = CTkTextbox(self.frame_center, width=6000, height=1500, text_font=('Roboto', -13))
                self.text.pack(expand=1)

                self.font_slider = CTkSlider(self.frame_right, from_=1, to=100, command=self.slider_event)
                self.font_slider.set(13)
                self.font_slider.grid(row=3, column=0, padx=10, pady=20, sticky='nswe')

                self.font_info = CTkLabel(self.frame_right, text='Размер шрифта: 13', text_font=('Roboto', -16))
                self.font_info.grid(row=4, column=0, padx=10, pady=10, sticky='nswe')

                self.font_box = CTkComboBox(self.frame_right, values=families(), command=change_font)
                self.font_box.entry.delete(0, END)
                self.font_box.entry.insert(0, 'Roboto')
                self.font_box.grid(row=5, column=0, padx=10, pady=15, sticky='nswe')
                self.window.bind('<Control-KeyPress-z>', self.control_z)
                self.window.bind('<Control-KeyPress-b>', self.control_s_z)
                self.window.bind('<KeyPress>', change_event)

    def open_inst(self, del_=False):
        def is_file():
            file_name = askopenfilename(title='Открыть', defaultextension='.tb',
                                        filetypes=(('TB file', '*.tb'), ('TXT File', '*.*'), ('All Files', '*.*')))
            if file_name:
                if '.tb' in file_name:
                    with open(file_name, encoding='utf-8') as file:
                        fuck = file.read()
                        data = loads(fuck)
                        self.open_new_inst(flag=True, is_tb=True, title=os.path.basename(file_name), path=file_name)
                        self.text.insert(1.0, data['text'])
                        self.text.configure(text_font=(data['font'], -data['font-size']))
                        self.font_slider.set(data['font-size'])
                        self.font_info.configure(text=f'Размер шрифта: {int(self.font_slider.get())}')
                        self.font_box.entry.delete(0, END)
                        self.font_box.entry.insert(0, data['font'])
                        self.memory = (self.text.get(1.0, END), int(self.font_slider.get()), self.font_box.entry.get())
                else:
                    with open(file_name) as f:
                        self.is_open_inst()
                        self.open_new_inst(flag=True, title=os.path.basename(file_name), path=file_name)
                        self.text.insert(1.0, f.read())
                        self.memory = (self.text.get(1.0, END), int(self.font_slider.get()), self.font_box.entry.get())

        def is_db():
            def open_ch_db():
                name = list_box.get()
                try:
                    with open(f'{self.HOME_PATH}/{name}') as file:
                        data = load(file)
                        self.open_new_inst(flag=True, is_tb=True, title=name, path=f'{self.HOME_PATH}/{name}')
                        self.text.insert(1.0, data['text'])
                        self.text.configure(text_font=(data['font'], -data['font-size']))
                        self.font_slider.set(data['font-size'])
                        self.font_info.configure(text=f'Размер шрифта: {int(self.font_slider.get())}')
                        self.font_box.entry.delete(0, END)
                        self.font_box.entry.insert(0, data['font'])
                        self.memory = (self.text.get(1.0, END), int(self.font_slider.get()), self.font_box.entry.get())
                except FileNotFoundError:
                    messagebox.showwarning('INFO', 'Файл не найден!')

            if not os.listdir(self.HOME_PATH + '/'):
                messagebox.showinfo('INFO', 'В базе данных отсутствуют сохранённые документы.')

            else:
                open_but.destroy()
                open_db_but.destroy()
                list_box = CTkComboBox(self.open_frame, values=os.listdir(self.HOME_PATH), width=200)

                list_box.grid(pady=30, padx=30)
                ok_but = CTkButton(self.open_frame, text='Открыть', width=100, command=open_ch_db)
                ok_but.grid(pady=30, padx=30)

        def is_del():
            def make_list():
                self.list_box = CTkComboBox(self.open_frame, values=os.listdir(self.HOME_PATH), width=200)
                self.list_box.grid(row=0, pady=30, padx=30)

            def del_ch_db():
                try:
                    name = self.list_box.get()
                    os.remove(f'{self.HOME_PATH}/{name}')
                    messagebox.showinfo('INFO', f'Документ "{name}" успешно удалён.')
                    self.list_box.destroy()
                    make_list()

                except FileNotFoundError:
                    messagebox.showwarning('INFO', 'Файл не найден!')
            if not os.listdir(self.HOME_PATH + '/'):
                messagebox.showinfo('INFO', 'В базе данных отсутствуют сохранённые документы.')
            else:
                self.is_open_inst()
                self.is_home()
                self.is_now_inst()
                self.is_new_inst()

                self.open_frame = CTkFrame(self.frame_center, height=400)
                self.open_frame.pack(expand=1)
                self.is_open_request = True

                make_list()

                ok_but = CTkButton(self.open_frame, text='Удалить', width=100, command=del_ch_db)
                ok_but.grid(row=1, pady=30, padx=30)

        if not del_:
            self.is_open_inst()
            self.is_home()
            self.is_now_inst()
            self.is_new_inst()

            self.open_frame = CTkFrame(self.frame_center, height=400)
            self.open_frame.pack(expand=1)
            open_but = CTkButton(self.open_frame, text='Выбрать файл', width=200, command=is_file)
            open_but.grid(pady=30, padx=30)
            open_db_but = CTkButton(self.open_frame, text='Выбрать из базы', width=200, command=is_db)
            open_db_but.grid(pady=30, padx=30)
            self.is_open_request = True
        if del_:
            is_del()

    def open_home(self):
        self.is_now_inst()
        self.is_open_inst()
        self.is_new_inst()
        if not self.is_hello_page:
            self.is_hello_page = True
            self.hello_label = CTkLabel(self.frame_center,
                                        text='Добро пожаловать в ТБ100!\nДля начала работы используйте меню.',
                                        text_font=("Roboto Medium", 60))
            self.hello_label.pack(expand=1)

    def is_home(self):
        if self.is_hello_page:
            self.hello_label.destroy()
            self.is_hello_page = False

    def is_new_inst(self):
        if self.is_new_doc:
            self.text.destroy()
            self.name_input.destroy()
            self.save_button.destroy()
            self.save_to_db_button.destroy()
            self.font_slider.destroy()
            self.font_info.destroy()
            self.font_box.destroy()
            self.window.unbind('<Control-KeyPress-z>')
            self.window.unbind('<Control-KeyPress-b>')
            self.window.unbind('<KeyPress>')
            self.is_new_doc = False

    def is_now_inst(self):
        if self.is_opened_doc:
            self.text.destroy()
            self.save_button.destroy()
            self.window.title('ТБ100')
            self.font_slider.destroy()
            self.font_info.destroy()
            self.font_box.destroy()
            self.window.unbind('<Control-KeyPress-z>')
            self.window.unbind('<Control-KeyPress-b>')
            self.window.unbind('<KeyPress>')
            self.is_opened_doc = False

    def is_open_inst(self):
        if self.is_open_request:
            self.open_frame.destroy()
            self.is_open_request = False


if __name__ == '__main__':
    app = TBApp()
    app.window.mainloop()
