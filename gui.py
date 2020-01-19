# -*- coding: utf-8 -*-
from PIL import ImageTk
from tkinter import Tk, Toplevel, Menu, END
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Label, Button, Entry, Progressbar

class Gui:
    def __init__(self, master=None):
        self.master = Tk() if not master else master
        self.master.title("Book Finder")
        self.master.resizable(0,0)
        #We change the window icon directly with Tk
        self.master.tk.call('wm', 'iconphoto', self.master, '::tk::icons::question')
        self.stext = ScrolledText(master=self.master, bg='white', height=25, width=100)
        #We disable the edition
        self.stext.config(state="disabled")
        menu = Menu()
        menu_tools = Menu(tearoff=0)
        menu_tools.add_command(label="Search book", command=lambda:self.search_book())
        menu_tools.add_command(label="Exit", command=self.master.destroy)
        menu.add_cascade(label="Menu", menu=menu_tools)
        menu_option = Menu(tearoff=0)
        menu_option.add_checkbutton(label="Don't download img", command=lambda:self.cmd2() if self.cmd2 else print("cmd2 not configured"))
        menu.add_cascade(label="Option", menu=menu_option)
        #We create a message box with Tk
        menu.add_command(label="About", command=lambda:self.master.tk.eval("tk_messageBox -message {Book Finder} -detail {Make by pythonbrad} -icon info -title About"))
        self.master.config(menu=menu)
        self.stext.pack()
        #This widget will print status
        self.label_status = Label(self.master, text="STATUS", font=('Arial', 14))
        self.label_status.pack()
        self.progress_bar = Progressbar()
        self.progress_bar.pack()
        self.is_searching = False
        #It will contains widget in memory
        self.temp = []
        #It will contains an external function
        #Who will be used by the function search_book
        self.cmd1 = None
        self.cmd2 = None
    def insert_img(self, data):
        #We convert image date in tk image data
        self.stext.image_create(END, image=self.get_img_tk(data))
    def insert_text(self, text, tag=None):
        #We insert the text
        self.stext.config(state="normal")
        self.stext.insert(END, text, tag)
        self.stext.config(state="disabled")
    def create_tag(self, tag_name, **args):
        self.stext.tag_config(tag_name, **args)
    def get_img_tk(self, data):
        img = ImageTk.PhotoImage(data=data)
        self.temp.append(img)
        return img
    def progress_bar_reset(self, max_value):
        self.progress_bar.config(max=max_value, value=0)
    def progress_bar_step(self):
        self.progress_bar.step(1)
    def search_book(self):
        try:
            self.win_search_book.destroy()
        except:
            pass
        if  not self.is_searching:
            self.win_search_book = Toplevel()
            self.win_search_book.tk.call('wm', 'iconphoto', self.win_search_book, '::tk::icons::question')
            Label(self.win_search_book, image='::tk::icons::question').pack()
            Label(self.win_search_book, text="Enter a keyword").pack()
            search_entry = Entry(self.win_search_book)
            search_entry.pack()
            def _(self, search_entry):
                #the data will return in the arg data to this command 
                self.cmd1(search_entry.get())
                self.win_search_book.destroy()
            Button(self.win_search_book, text="Search",
                #We given the self and the search text
                #The self will give the access to this object
                command=lambda:_(self, search_entry) if self.cmd1 else print("cmd1 not configured")).pack()
            self.win_search_book.mainloop()
        else:
            self.master.tk.eval("tk_messageBox -message {A research aleady running} -icon warning")
    def update(self):
        self.master.update()
    def mainloop(self):
        self.master.mainloop()

if __name__ == '__main__':
    win = Gui()
    win.mainloop()