import tkinter as tk
from tkinter import messagebox
from tkinter import font

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
window.geometry("600x360")
window.resizable(False, True)
window.configure(bg="#f0f4f8")

defafultFont = font.nametofont("TkDefaultFont")
defafultFont.configure(size=12)

# label instructions (widget 1)
labelInstruction = tk.Label(
    window,
    text="Enter a task and click Add, or select one to Remove",
    bg="#f0f4f8",
    fg="#2d3748",
    font=("Helvetica", 10),
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
frameButtons = tk.Frame(window, bg="#f0f4f8")
frameButtons.pack(pady=12)

addBtn = tk.Button(
    frameButtons,
    text="Add Task",
    command=taskAdd,
    font=("Helvetica", 10),
    bg="#48bb78",
    fg="#f0f4f8",
    activebackground="#38a169",
    activeforeground="#f0f4f8",
    relief="flat",
    padx=16,
    pady=6,
    cursor="hand2",
)
addBtn.pack(side=tk.LEFT, padx=6)

removeBtn = tk.Button(
    frameButtons,
    text="Remove Selected",
    command=taskRemove,
    font=("Helvetica", 10),
    bg="#ed8936",
    fg="#f0f4f8",
    activebackground="#dd6b20",
    activeforeground="#f0f4f8",
    relief="flat",
    padx=16,
    pady=6,
    cursor="hand2",
)
removeBtn.pack(side=tk.LEFT, padx=6)

clearBtn = tk.Button(
    frameButtons,
    text="Clear All",
    command=clearAll,
    font=("Helvetica", 10),
    bg="#e53e3e",
    fg="#f0f4f8",
    activebackground="#c53030",
    activeforeground="#f0f4f8",
    relief="flat",
    padx=16,
    pady=6,
    cursor="hand2",
)
clearBtn.pack(side=tk.LEFT, padx=6)

# move buttons
moveUpBtn = tk.Button(
    frameButtons,
    text="Move Up",
    command=lambda: moveUp(),
    font=("Helvetica", 10),
    bg="#63b3ed",
    fg="#f0f4f8",
    activebackground="#4299e1",
    activeforeground="#f0f4f8",
    relief="flat",
    padx=12,
    pady=6,
    cursor="hand2",
)
moveUpBtn.pack(side=tk.LEFT, padx=6)

moveDownBtn = tk.Button(
    frameButtons,
    text="Move Down",
    command=lambda: moveDown(),
    font=("Helvetica", 10),
    bg="#63b3ed",
    fg="#f0f4f8",
    activebackground="#4299e1",
    activeforeground="#f0f4f8",
    relief="flat",
    padx=8,
    pady=6,
    cursor="hand2",
)
moveDownBtn.pack(side=tk.LEFT, padx=6)


# start the GUI
if __name__ == "__main__":
    window.mainloop()