"""
'To Do List App'
Author: Colin Herbert
File: ListFunctions.py
Purpose: Operations that can be performed on a list (functions to call)"""
from ToDoClass import *
from datetime import *

def get_task_details():
    # get details of task you are adding
    description = input("Enter a description for your task: ")
    has_deadline = None
    while has_deadline != 'Y' and has_deadline != 'N' and has_deadline != 'y' and has_deadline != 'n':
        has_deadline = input("Do you have a deadline? Enter Y/N: ")
    if has_deadline == 'y' or has_deadline == 'Y':
        deadline = ''
        while len(deadline) != 10:
            deadline = input("Enter deadline in format mm/dd/yyyy: ")
            month = deadline[0:2]
            day = deadline[3:5]
            year = deadline[6:]
            if len(deadline) != 10:
                print('Invalid Format')
        deadline = (month, day, year)
    else:
        deadline = None
    return description, deadline

def add_task(t_list, desc, deadline, is_complete = 0):
    # Add task to current selected list
    """Purpose: Add task to a list, set initial values and insert into the list"""
    new_task = ToDoTask(desc, deadline)
    if t_list is None:
        t_list.list = [new_task]
        return
    if is_complete == 1:
        new_task.completed = True
    t_list.list.append(new_task)

def remove_task(t_list):
    # Removes specified node from list
    length = len(t_list.list)
    if length == 0:
        return
    # if length of list is 1, delete only item in the list
    if length == 1:
        index = 1
        t_list.list.remove(t_list.list[0])
        return
    else:
        index = -1
        while int(index) not in range(1, length + 1):
            index = int(input("Enter task number to remove: "))
            if index not in range(1, length + 1):
                print("\nERROR: index out of range\n")
        t_list.list.remove(t_list.list[index - 1])

def add_list(head, new_name):
    # Add new list
    if head is None:
        head = ListsNode([], new_name)
        return head, head
    else:
        cur = head
        while cur.next is not None:
            cur = cur.next
        cur.next = ListsNode([], new_name)
        cur.next.prev = cur
        return head, cur.next

def remove_list(head, list):
    # Remove specified list
    if list is head:
        if head.next is None:
            return None, None
        else:
            head = head.next
            head.prev = None
            return head, head
    else:
        cur = head
        while cur.next is not list:
            cur = cur.next
        cur.next.prev = cur
        cur.next = cur.next.next
        return head, cur

def go_next(head, cur_list):
    # Traverse to the next list
    if head is None:
        return None
    if cur_list.next is not None:
        return head, cur_list.next
    else:
        return head, head

def go_back(head, cur_list):
    # Go back to previous list
    if head is None:
        return None
    if cur_list.prev is not None:
        return head, cur_list.prev
    else:
        cur = head
        while cur.next is not None:
            cur = cur.next
        return head, cur

def save_progress(head, file_name):
    # Save lists to a text file with specified name
    file = open(file_name + '.txt', 'w')
    cur = head
    while cur is not None:
        file.write(str(cur))
        file.write('\n')
        cur = cur.next
    print("Data Saved.")

def load_progress(file_name):
    # Load lists from file with specified name
    try:
        file = open(file_name + '.txt', 'r')
    except:
        print("ERROR: No such file exists with that name!")
        return None

    head = None
    cur_list = None
    for line in file.readlines():
        if line == '\n':
            continue
        elif line[0] != '*':
            head, cur_list = add_list(head, line)
        else:
            desc = line.split('|')[0][2:]
            if (line.split('|')[1] == '#No Deadline Set#'):
                deadline = None
            else:
                deadline = (line.split('|')[1].split('/')[0], line.split('|')[1].split('/')[1], line.split('|')[1].split('/')[2])
            if (line.split('|')[2] == 'X'):
                add_task(cur_list, desc, deadline, 1)
            else:
                add_task(cur_list, desc, deadline)
    return head



