import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk

# functions

# enter task to the list if valid
def taskAdd():
    taskText = enterTask.get().strip()
    if not taskText:
        messagebox.showwarning("Empty Task", "Please type in a task before adding.")
        return
    idx = taskListBox.size() + 1
    taskListBox.insert(tk.END, f"{idx}. {taskText}")
    enterTask.delete(0, tk.END)
    
def taskRemove():
    try:
        selectedIdx = taskListBox.curselection()[0]
        taskListBox.delete(selectedIdx)
        listRenumber()
    except IndexError:
        messagebox.showinfo("Nothing Selected", "Please select a task to remove.")
        
def clearAll():
    if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all tasks?"):
        taskListBox.delete(0, tk.END)
        messagebox.showinfo("All tasks have been removed.")

# renumber the tasks when added/removed and moved up/down
def listRenumber():
    current_items = [taskListBox.get(i) for i in range(taskListBox.size())]
    taskListBox.delete(0, tk.END)
    for i, text in enumerate(current_items, start=1):
        raw = text
        if raw.startswith("• "):
            raw = raw[2:]
        elif ". " in raw:
            parts = raw.split('. ', 1)
            if parts[0].isdigit():
                raw = parts[1]
        taskListBox.insert(tk.END, f"{i}. {raw}")

# select task and move it up in the list
def moveUp():
    sel = taskListBox.curselection()
    if not sel:
        messagebox.showinfo("Nothing Selected", "Please select a task to move.")
        return
    idx = sel[0]
    if idx == 0:
        return
    a = taskListBox.get(idx)
    b = taskListBox.get(idx - 1)
    taskListBox.delete(idx)
    taskListBox.delete(idx - 1)
    taskListBox.insert(idx - 1, a)
    taskListBox.insert(idx, b)
    taskListBox.selection_clear(0, tk.END)
    taskListBox.selection_set(idx - 1)
    listRenumber()

# select task and move it down in the list
def moveDown():
    sel = taskListBox.curselection()
    if not sel:
        messagebox.showinfo("Nothing Selected", "Please select a task to move.")
        return
    idx = sel[0]
    last = taskListBox.size() - 1
    if idx == last:
        return
    a = taskListBox.get(idx)
    b = taskListBox.get(idx + 1)
    taskListBox.delete(idx + 1)
    taskListBox.delete(idx)
    taskListBox.insert(idx, b)
    taskListBox.insert(idx + 1, a)
    taskListBox.selection_clear(0, tk.END)
    taskListBox.selection_set(idx + 1)
    listRenumber()

# window
window = tk.Tk()
window.title("To-Do List")
window.geometry("600x500")
window.resizable(False, False)
window.configure(bg="#f0f4f8")

defafultFont = font.nametofont("TkDefaultFont")
defafultFont.configure(size=12)

# label instructions (widget 1)
labelInstruction = tk.Label(
    window,
    text="Enter a task and click Add",
    bg="#f0f4f8",
    fg="#2d3748",
    font=("Helvetica", 12),
)
labelInstruction.pack(pady=(12, 6))

# user input (widget 2)
enterTask = tk.Entry(
    window,
    width=40,
    font=("Helvetica", 12),
    bg="#f0f4f8",
    fg="#1a202c",
    relief="flat",
    highlightthickness=1,
    highlightbackground="#cbd5e0",
    highlightcolor="#4299e1",
)
enterTask.pack(pady=6, padx=20, ipadx=8)
enterTask.focus_set()

enterTask.bind("<Return>", lambda e:taskAdd())

# listbox display (widget 3)
frameList = tk.Frame(window, bg="#f0f4f8")
frameList.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frameList)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

taskListBox = tk.Listbox(
    frameList,
    height=12,
    font=("Helvetica", 12),
    bg="#f0f4f8",
    fg="#1a202c",
    selectbackground="#4299e1",
    selectforeground="#f0f4f8",
    relief="flat",
    highlightthickness=0,
    yscrollcommand=scrollbar.set,
)
taskListBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=taskListBox.yview)

# buttons (event triggers)
frameActButtons = tk.Frame(window, bg="#f0f4f8")
frameActButtons.pack(pady=12)

# ttk styles for colored buttons
style = ttk.Style()
try:
    style.theme_use('clam')
except tk.TclError:
    pass

style.configure('Green.TButton', background='#69346a', foreground='#f0f4f8', font=("Helvetica", 10))
style.map('Green.TButton', background=[('active', "#69346a")])

style.configure('Orange.TButton', background='#2B7974', foreground='#f0f4f8', font=("Helvetica", 10))
style.map('Orange.TButton', background=[('active', "#2B7974")])

style.configure('Red.TButton', background='#873333', foreground='#f0f4f8', font=("Helvetica", 10))
style.map('Red.TButton', background=[('active', "#873333")])

style.configure('Blue.TButton', background='#1a202c', foreground='#f0f4f8', font=("Helvetica", 10))
style.map('Blue.TButton', background=[('active', '#1a202c')])

addBtn = ttk.Button(
    frameActButtons,
    text="Add Task",
    command=taskAdd,
    style='Green.TButton',
    padding=(16, 6),
    cursor="hand2",
)
addBtn.pack(side=tk.LEFT, padx=6)

removeBtn = ttk.Button(
    frameActButtons,
    text="Remove Task",
    command=taskRemove,
    style='Orange.TButton',
    padding=(16, 6),
    cursor="hand2",
)
removeBtn.pack(side=tk.LEFT, padx=6)

clearBtn = ttk.Button(
    frameActButtons,
    text="Clear All",
    command=clearAll,
    style='Red.TButton',
    padding=(16, 6),
    cursor="hand2",
)
clearBtn.pack(side=tk.LEFT, padx=6)

# move buttons on their own row
frameMoveButtons = tk.Frame(window, bg="#f0f4f8")
frameMoveButtons.pack(pady=(6, 12))

moveUpBtn = ttk.Button(
    frameMoveButtons,
    text="Move Up",
    command=lambda: moveUp(),
    style='Blue.TButton',
    padding=(12, 6),
    cursor="hand2",
)
moveUpBtn.pack(side=tk.LEFT, padx=6)

moveDownBtn = ttk.Button(
    frameMoveButtons,
    text="Move Down",
    command=lambda: moveDown(),
    style='Blue.TButton',
    padding=(12, 6),
    cursor="hand2",
)
moveDownBtn.pack(side=tk.LEFT, padx=6)


# start the GUI
if __name__ == "__main__":
    window.mainloop()
    
    
'''
1. What does your program do?
    My program allows users to add new tasks, remove a selected task, clear all tasks, 
    and move them up or down. The task list is displayed in a scrollable listbox. Empty
    inputs are rejected by the program with a warning message displayed afterwards.
    
2. How does the user interact with it?
    The user is able to:
    - Type in a task in the entry box at the top and either presses the Enter key or 
    clicks "Add Task" to add it to the list.
    - Remove a selected task by selecting the desired task and then clicking on "Remove 
    Task" to remove that task.
    - Clear all tasks by clicking "Clear All" then yes to ensure that the user doesn't
    accidently clear the task list.
    - Move tasks up and down by selecting the desired task and then clicking either "Move
    Up" or "Move Down" to rearrange the position of the task on the list.

3. Where is user input handled?
    User input is handled in the taskAdd() function through enterTask.get(). The text is
    stripped of leading & trailing blank spaces before validation. The Remove, Clear All,
    Move Up, and Move Down actions use thet listbox selection (curselection()) or the full 
    list's content (no typing required for those).

4. Where is program logic implemented?
    - taskAdd() has input validation where it checks if the taskText is empty, if it is then
    it shows a warning and returns to the progam without adding.
    - taskRemove() uses try and except on curselection() to handle the case when nothing has
    been selected.
    - clearAll() clears all tasks in the list after confirmation.
    - listRenumber() renumbers the tasks after either adding, removing, or reordering tasks.
    - moveUp() and moveDown() move the selected task up or down in the list.
'''