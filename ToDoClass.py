"""
'To Do List App'
Author: Colin Herbert
File: ToDoClass.py
Purpose: Classes for App (Linked list of to-do lists, to-do list class, list node class)"""
from datetime import date

class ToDoTask:
    # Task object. Used in array to put in
    def __init__(self, desc, deadline):
        """Arguments:
            desc (description of task)
            deadline (deadline of task)
        """
        assert type(deadline) == tuple or deadline == None
        if type(deadline) == tuple:
            assert len(deadline) == 3
        assert type(desc) == str
        self._desc = desc
        if deadline == None:
            self._deadline = None
        else:
            self._deadline = date(int(deadline[2]), int(deadline[0]), int(deadline[1]))
        self.completed = False
    def get_description(self):
        return self._desc
    def get_deadline(self):
        if self._deadline == None:
            return None
        return (self._deadline.month, self._deadline.day, self._deadline.year)
    def complete_task(self):
        if self.completed == True:
            self.completed == False
            print(self.completed)
            return
        self.completed = True
    def is_completed(self):
        if self._deadline is not None:
            if (date.today() > self._deadline):
                self.completed = 'NA'
        return self.completed

class ListsNode:
    # Linked list (double) containing set of lists. Main way to navigate between lists.
    def __init__(self, list, name):
        self.list = list
        assert type(name) == str
        self.name = name
        self.next = None
        self.prev = None

    def __str__(self):
        ret_val = self.name + '\n'
        for task in self.list:
            ret_val += '* '
            ret_val += task.get_description()
            deadline = task.get_deadline()
            if deadline == None:
                ret_val += '|#No Deadline Set#|'
            else:
                ret_val += f'|{deadline[0]}/{deadline[1]}/{deadline[2]}|'
            if task.is_completed() == True:
                ret_val += 'X'
            elif task.is_completed() == 'NA':
                ret_val += 'Deadline Passed!'
            else:
                ret_val += 'O'
            ret_val += '\n'
        return ret_val


