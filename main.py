# -*- coding: utf-8 -*-
from finder import Finder
from gui import Gui
from tkinter.constants import CENTER, LEFT
import requests
from task import Task

def search(win, text):
	if not win.is_searching:
		win.is_searching = True
		win.label_status.config(text="Initiation ...", foreground='green')
		try:
			finder = Finder()
			finder.max_page=2
			win.label_status.config(text="Searching in https://www.pdfdrive.com ...")
			win.progress_bar_reset(50)
			win.progress_bar.start()
			win.update()
			finder.pdfdrive(text)
			win.label_status.config(text="Searching in http://www.allitebooks.org ...")
			win.update()
			finder.allitebooks(text)
			win.progress_bar.stop()
			win.label_status.config(text="Loading data ...")
			win.progress_bar_reset(len(finder.result))
			win.update()
			for data in finder.result:
				win.progress_bar.step(1)
				win.label_status.config(text="Loading title ...")
				win.update()
				win.insert_text(data["TITLE"].decode(), 'title')
				win.update()
				data.pop('TITLE')
				win.insert_text('\n')
				if win.show_img:
					win.label_status.config(text="Downloading img ...")
					win.update()
					re = requests.get(data["IMG"].decode())
					data.pop('IMG')
					if re.status_code == 200:
						#This text permet to center the image
						win.insert_text('.', 'title')
						win.label_status.config(text="Loading img ...")
						#We insert the image after the text
						win.insert_img(data=re.content)
						win.insert_text('\n')
					else:
						win.insert_text('IMG NOT FOUND', 'error')
						win.insert_text('\n')
						win.label_status.config(text="Loading img failed ...", foreground='red')
					win.update()
				win.label_status.config(text="Loading others data ...", foreground='green')
				win.update()
				for key in data:
					win.insert_text("%s: %s" % (key, data[key].decode()))
					win.insert_text('\n')
					win.update()
		except requests.exceptions.ConnectionError:
			win.label_status.config(text="Connection Error", foreground="red")
		except Exception as err:
			win.label_status.config(text=str(err), foreground="red")
		else:
			win.label_status.config(text="Success")
		win.progress_bar.stop()
		win.update()
		win.is_searching = False
	else:
		print("Searching is running")

win = Gui()
win.is_searching = False
win.show_img = True
#We init the task manager
task_manager = Task()
task_manager.run()

##############################################################################
#this code is to review, because can be x-x
#We pass the task who represent the command of search associate to task manager
win.cmd1 = lambda text:task_manager.add(lambda:search(win,text))
win.cmd2 = lambda:win.__setattr__('show_img', False if win.show_img else True)
##############################################################################

win.label_status.config(text="What do you search?", foreground='green')
win.create_tag('title', underline=1, justify=CENTER, font=('Arial', 16))
win.create_tag('url', justify=LEFT, font=('Arial', 12), foreground='green')
win.create_tag('error', justify=LEFT, font=('Arial', 12), foreground='red')
win.mainloop()
#We stop the task manager
task_manager.stop()