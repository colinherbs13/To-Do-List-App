from tkinter import *
from ListFunctions import *
from ToDoClass import *

class MainWindow(Tk):
    '''Main Window that comes up on launch'''
    def __init__(self):
        # Call init function of window
        super().__init__()

        # pointer to the list displayed on the screen as well as linked list of all to-do-lists
        self.cur_list = None
        self.all_lists = None
        self.checkbox_states = []

        # Attributes of the window
        self.title("To-Do-Lists")
        self.geometry('%dx%d+%d+%d' % (500, 500, 50, 100))
        self.resizable(False, False)

        # create area that displays the list with scrollbar
        self.wrapper = LabelFrame(self)

        self.canvas = Canvas(self.wrapper, bg='white')
        self.canvas.place(bordermode=OUTSIDE, height=270, width=340, x=2, y=2)

        self.scrollbar = Scrollbar(self.wrapper, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))

        self.frame = Frame(self.canvas, bg='white')
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')

        self.wrapper.place(bordermode=OUTSIDE, height=275, width=350, x=75, y=100)

        # create list title over box
        self.l_title = StringVar()
        self.list_title = Label(self, textvariable=self.l_title, font=20)
        self.l_title.set("Press 'Add' to add a new list.")
        self.list_title.place(bordermode=OUTSIDE, height=50, width=350, x=75, y=50)

        # create arrow buttons
        self.left = Button(self, text="<", command = lambda: self.perform_command('<'))
        self.left.place(bordermode=OUTSIDE, height=50, width=50, x=75, y=400)

        self.right = Button(self, text=">", command = lambda: self.perform_command('>'))
        self.right.place(bordermode=OUTSIDE, height=50, width=50, x=375, y=400)

        # create add/remove/save & load buttons
        self.add_stuff = Menubutton(self, text="Add", relief=RAISED)
        self.add_stuff.place(bordermode=OUTSIDE, height=50, width=83, x=125, y=400)
        self.add_stuff.menu = Menu(self.add_stuff, tearoff=0)
        self.add_stuff["menu"] = self.add_stuff.menu
        self.add_stuff.menu.add_command(label="List", command= lambda: self.perform_command('a'))
        self.add_stuff.menu.add_command(label="Task", command= lambda: self.perform_command('e'))

        self.remove_stuff = Menubutton(self, text="Remove", relief=RAISED)
        self.remove_stuff.place(bordermode=OUTSIDE, height=50, width=83, x=208, y=400)
        self.remove_stuff.menu = Menu(self.remove_stuff, tearoff=0)
        self.remove_stuff["menu"] = self.remove_stuff.menu
        self.remove_stuff.menu.add_command(label="List", command= lambda: self.perform_command('r'))
        self.remove_stuff.menu.add_command(label="Task", command= lambda: self.perform_command('d'))

        self.save_load = Menubutton(self, text="Save/Load", relief=RAISED)
        self.save_load.place(bordermode=OUTSIDE, height=50, width=83, x=292, y=400)
        self.save_load.menu = Menu(self.save_load, tearoff=0)
        self.save_load["menu"] = self.save_load.menu
        self.save_load.menu.add_command(label="Save", command= lambda: self.perform_command('s'))
        self.save_load.menu.add_command(label="Load", command= lambda: self.perform_command('l'))

    def perform_command(self, command):
        # update completion status in list
        if self.all_lists is not None:
            self.check_completion()
        '''Executes command called by button press'''
        if command in 'Aa':
            list_name = AddListWindow(self)
            list_name.grab_set()
        elif command in 'Rr':
            if self.all_lists is None:
                return
            self.all_lists, self.cur_list = remove_list(self.all_lists, self.cur_list)
            self.update_window()
        elif command in 'Ee':
            task_window = AddTaskWindow(self)
            task_window.grab_set()
        elif command in 'Dd':
            if self.cur_list is None:
                return
            remove_task(self.cur_list)
            self.update_window()
        elif command in 'Ss':
            save_window = SaveWindow(self, 'save')
            save_window.grab_set()
        elif command in 'Ll':
            load_window = SaveWindow(self, 'load')
            load_window.grab_set()
        elif command == '<':
            if self.all_lists is None:
                return
            self.all_lists, self.cur_list = go_back(self.all_lists, self.cur_list)
            self.update_window()
        elif command == '>':
            if self.all_lists is None:
                return
            self.all_lists, self.cur_list = go_next(self.all_lists, self.cur_list)
            self.update_window()
        else:
            print("ERROR: Invalid Input!")
        return

    def check_completion(self):
        for i in range(len(self.checkbox_states)):
            if self.checkbox_states[i].get() == 1:
                self.cur_list.list[i].completed = True
            else:
                self.cur_list.list[i].completed = False

    def update_window(self):
        '''Updates the list box on the main screen'''
        # clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.grid_forget()

        # Update List Box
        count = 0
        if self.cur_list is None:
            self.l_title.set('No Lists Available')
        else:
            self.checkbox_states = []
            # update current list title
            self.l_title.set(self.cur_list.name)
            # put list in frame
            for item in self.cur_list.list:
                state = IntVar()
                task = Label(self.frame, text=item.get_description(), bg='white')
                deadline = item.get_deadline()

                self.checkbox_states.append(state)
                # Change label depending on if deadline is set, or if the deadline has passed.
                if deadline is None:
                    deadline_label = Label(self.frame, text='No Deadline Set', bg='white')
                    checkbox = Checkbutton(self.frame, variable=self.checkbox_states[count], onvalue=1, offvalue=0, bg='white')
                elif date.today() > date(deadline[2], deadline[0], deadline[1]):
                    deadline_label = Label(self.frame, text="Deadline Passed!", bg='white')
                    checkbox = Checkbutton(self.frame, variable=self.checkbox_states[count], onvalue=1, offvalue=0, bg='red', state=DISABLED)
                else:
                    deadline_label = Label(self.frame, text=(str(deadline[0]) + '/' + str(deadline[1]) + '/' + str(deadline[2])), bg='white')
                    checkbox = Checkbutton(self.frame, variable=self.checkbox_states[count], onvalue=1, offvalue=0, bg='white')

                # if task is completed, select the checkbox
                if item.completed == True:
                    checkbox.select()

                # Put widgets on screen
                task.grid(row=count, column=0)
                deadline_label.grid(row=count, column=1)
                checkbox.grid(row=count, column=2)
                count += 1

class AddListWindow(Toplevel):
    # window gets name of list to add with option to submit or cancel operation
    def __init__(self, parent):
        # init function of window
        super().__init__(parent)
        self.parent = parent

        # window attributes
        self.title("Add List")
        self.geometry('155x100')
        self.resizable(False, False)

        # widgets including entry box, ok and cancel buttons
        self.label = Label(self, text='Enter New List Name:')

        self.name = StringVar()
        self.input = Entry(self, width=20, bd=5, textvariable=self.name)

        self.ok = Button(self, text='OK', command=lambda: self.submit(self.name.get()))
        self.cancel = Button(self, text='Cancel', command=self.destroy)

        # place widgets on screen
        self.input.place(x=15, y=20)
        self.ok.place(x=40, y=45)
        self.cancel.place(x=80, y=45)
        self.label.place(x=16, y=0)

    def submit(self, name):
        if name == '':
            return
        self.parent.all_lists, self.parent.cur_list = add_list(self.parent.all_lists, name)
        self.parent.update_window()
        self.destroy()

class AddTaskWindow(Toplevel):
    # window gets name and deadline of new task
    def __init__(self, parent):
        # init function of new window
        super().__init__(parent)
        self.parent = parent

        # window attributes
        self.title("Add Task")
        self.resizable(False, False)

        # Widgets

        # Handle if no lists are added currently
        if self.parent.all_lists is None:
            self.geometry('200x80')
            self.label = Label(self, text="ERROR: No lists created.")
            self.label2 = Label(self, text="Would you like to add a list now?")
            self.yes_button = Button(self, text='Yes', command = self.yes)
            self.no_button = Button(self, text='No', command = self.destroy)

            self.label.pack()
            self.label2.pack()
            self.yes_button.place(x=60, y=50)
            self.no_button.place(x=110, y=50)
        else:
            self.geometry('200x200')
            self.task_name = StringVar()

            self.task_name_label = Label(self, text="Task Name:")
            self.enter_task_name = Entry(self, bd=5, textvariable=self.task_name)

            self.month_label = Label(self, text="Month:")
            self.month = StringVar()
            self.month_select = Spinbox(self, from_=1, to=12, textvariable=self.month)

            self.day_label = Label(self, text="Day:")
            self.day = StringVar()
            self.day_select = Spinbox(self, from_=1, to=31, textvariable=self.day)

            self.year_label = Label(self, text="Year:")
            self.year = StringVar()
            self.year_select = Spinbox(self, from_=date.today().year, to=2100, textvariable=self.year)

            self.ok_button = Button(self, text='OK', command=self.submit_data)
            self.cancel_button = Button(self, text='Cancel', command=self.destroy)

            # put widgets on screen
            self.task_name_label.pack()
            self.enter_task_name.pack()
            self.month_label.pack()
            self.month_select.pack()
            self.day_label.pack()
            self.day_select.pack()
            self.year_label.pack()
            self.year_select.pack()
            self.ok_button.place(x=50, y=170)
            self.cancel_button.place(x=100, y=170)

    def yes(self):
        self.parent.perform_command('a')
        self.destroy()

    def submit_data(self):
        self.date = (int(self.month.get()), int(self.day.get()), int(self.year.get()))
        if self.task_name.get() == '':
            return
        else:
            add_task(self.parent.cur_list, self.task_name.get(), self.date)
            self.parent.update_window()
            self.destroy()

class SaveWindow(Toplevel):
    # Window for entering the name of your save/load file
    def __init__(self, parent, save_load):
        # init function for parent window
        super().__init__(parent)
        self.parent = parent

        self.title("Add Task")
        self.geometry("200x80")
        self.resizable(False, False)

        self.file_name = StringVar()

        self.enter_file_name = Entry(self, bd=5, textvariable=self.file_name)

        # see if you are saving or loading a file and open window accordingly
        if save_load == 'save':
            self.command_label = Label(self, text="Enter name for save file:").pack()
            self.enter_file_name.pack()
            self.save_button = Button(self, text="Save", command = self.save).place(x=60, y=50)
        else:
            self.command_label = Label(self, text="Enter name for file to load:").pack()
            self.enter_file_name.pack()
            self.load_button = Button(self, text="Load", command = self.load).place(x=60, y=50)

        self.cancel_button = Button(self, text="Cancel", command = self.destroy).place(x=110, y=50)

    def save(self):
        if self.file_name.get() == '':
            return
        save_progress(self.parent.all_lists, self.file_name.get())
        self.parent.update_window()
        self.destroy()

    def load(self):
        if self.file_name.get() == '':
            return
        self.parent.all_lists = self.parent.cur_list = load_progress(self.file_name.get())
        self.parent.update_window()
        self.destroy()

def create_main_window():
    # creates the main window on startup
    main = MainWindow()
    main.mainloop()


create_main_window()
