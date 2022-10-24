from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askdirectory
from customtkinter import *
from PIL import Image, ImageTk
import os

# def center_window(roots, x_width, height):
#     x_window_height = height
#     x_window_width = x_width
#
#     screen_width = roots.winfo_screenwidth()
#     screen_height = roots.winfo_screenheight()
#
#     x_coordinate = int((screen_width / 2) - (x_window_width / 2))
#     y_coordinate = int((screen_height / 2) - (x_window_height / 2))
#
#     roots.geometry('{}x{}+{}+{}'.format(x_window_width, x_window_height, x_coordinate, y_coordinate))


class TBApp:
    def __init__(self):
        self.window = CTk()
        self.window.minsize(1150, 400)
        self.window.title('ТБ100')
        self.window.state('zoomed')
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        self.frame_left = CTkFrame(self.window, width=680, corner_radius=0)

        self.frame_left.grid(row=0, column=0, sticky='nswe')

        self.frame_right = CTkFrame(self.window, width=280, corner_radius=0)

        self.frame_right.grid(row=0, column=2, sticky='nswe')

        self.frame_center = CTkFrame(self.window)
        self.frame_center.grid(row=0, column=1, sticky='nswe', padx=40, pady=20)

        self.remode = Button(self.frame_left, command=self.to_remode)
        self.remode.image = ImageTk.PhotoImage(Image.open('a.png'))
        self.remode['image'] = self.remode.image
        self.remode.grid(row=0, column=0, padx=20, pady=20)

        self.title_label = Button(self.frame_left, width=280, height=150, command=self.open_home)
        self.title_label.image = ImageTk.PhotoImage(Image.open('t.png'))
        self.title_label['image'] = self.title_label.image
        self.title_label.grid(row=1, column=0)

        self.hello_label = CTkLabel(self.frame_center,
                                    text='Добро пожаловать в ТБ100!\nДля начала работы используйте меню.',
                                    text_font=("Roboto Medium", 60))
        self.hello_label.pack(expand=1)

        self.button = CTkButton(self.frame_left, text='Создать инструктаж', command=self.open_new_inst, width=270)
        self.button.grid(pady=30)

        self.window.bind('<Configure>', self.resize_hello_label)

        if not os.path.exists('dir.conf'):
            mb = messagebox.askyesno('Добро пожаловать!',
                                     'Для продолжения работы необходимо выбрать рабочую директорию.')
            if mb:
                direct = askdirectory(title='Выберите директорию...')
                if direct:
                    with open('dir.conf', 'w') as f:
                        f.write(direct + '/TB100 Files')
                        os.mkdir(direct + '/TB100 Files')
        else:
            with open('dir.conf') as f:
                self.PATH = f.read()
        self.save_db_but = None
        self.new_ins = False
        self.open_ins = False
        self.hello = True
        self.text = None
        self.name_inp = None
        self.save_but = None
        self.is_dark = False

    def to_remode(self):
        if self.is_dark:
            self.remode.image = ImageTk.PhotoImage(Image.open('a.png'))
            self.remode['image'] = self.remode.image
            set_appearance_mode('System')
            self.is_dark = False
        else:
            self.remode.image = ImageTk.PhotoImage(Image.open('d.jpg'))
            self.remode['image'] = self.remode.image
            set_appearance_mode('dark')
            self.is_dark = True

    def resize_hello_label(self, par=None):
        if self.hello:
            self.hello_label.configure(text_font=("Roboto Medium", int(self.window.winfo_width() / 60)))
        return par

    def save_new_file(self):
        name = asksaveasfilename(defaultextension='.txt', title='Сохранение')
        if name:
            with open(name, 'w') as fo:
                fo.write(self.text.get('1.0', END))

    def save_new_file_to_db(self):
        with open(f'{self.PATH}/{self.name_inp.get()}.tb', 'w') as fo:
            fo.write(self.text.get('1.0', END))
            messagebox.showinfo('INFO', 'Инструктаж успешно сохранён!')

    def open_new_inst(self):
        if self.hello:
            self.hello_label.destroy()
            self.hello = False
            self.text = CTkTextbox(self.frame_center, width=6000, height=1500)
            self.text.pack(expand=1)

        if not self.new_ins:
            self.new_ins = True
            self.name_inp = CTkEntry(self.frame_right, width=280, placeholder_text='Название инструктажа...')
            self.name_inp.grid(row=0, column=0, padx=10, pady=20, sticky='nswe')

            self.save_but = CTkButton(self.frame_right, text='Сохранить файл', command=self.save_new_file)
            self.save_but.grid(row=1, column=0, padx=10, pady=20, sticky='nswe')

            self.save_db_but = CTkButton(self.frame_right, text='Сохранить в базу', command=self.save_new_file_to_db,
                                         hover_color='#b8b8b8')
            self.save_db_but.grid(row=2, column=0, padx=10, pady=20, sticky='nswe')

    def open_home(self):
        if self.new_ins:
            self.text.destroy()
            self.name_inp.destroy()
            self.save_but.destroy()
            self.save_db_but.destroy()
            self.new_ins = False
        if not self.hello:
            self.hello = True
            self.hello_label = CTkLabel(self.frame_center,
                                        text='Добро пожаловать в ТБ100!\nДля начала работы используйте меню.',
                                        text_font=("Roboto Medium", 60))
            self.hello_label.pack(expand=1)


if __name__ == '__main__':
    app = TBApp()
    app.window.mainloop()
