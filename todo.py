import tkinter as tk
from tkinter import messagebox
import json

FILE_NAME = "tasks_by_date.json"
tasks = {}

# ---------- File Handling ----------
def load_tasks():
    global tasks
    try:
        with open(FILE_NAME, "r") as f:
            tasks = json.load(f)
    except:
        tasks = {}

def save_tasks():
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

# ---------- Date Helper ----------
def get_selected_date():
    day = day_var.get()
    month = month_var.get()
    year = year_var.get()

    if day == "Day" or month == "Month" or year == "Year":
        return None

    month_num = months.index(month) + 1
    return f"{year}-{month_num:02d}-{int(day):02d}"

# ---------- UI Helpers ----------
def refresh_listbox(date):
    listbox.delete(0, tk.END)
    if date in tasks:
        for i, task in enumerate(tasks[date]):
            status = "✔" if task["completed"] else "✗"
            listbox.insert(tk.END, f"[{status}] {task['text']}")
            if task["completed"]:
                listbox.itemconfig(i, fg="green")

# ---------- Core Features ----------
def load_date_tasks():
    date = get_selected_date()
    if not date:
        messagebox.showwarning("Warning", "Please select day, month, and year")
        return
    refresh_listbox(date)

def add_task():
    date = get_selected_date()
    text = task_entry.get().strip()

    if not date or text == "":
        messagebox.showwarning("Warning", "Select a date and enter a task")
        return

    tasks.setdefault(date, []).append({
        "text": text,
        "completed": False
    })

    save_tasks()
    refresh_listbox(date)
    task_entry.delete(0, tk.END)

def toggle_complete():
    date = get_selected_date()
    try:
        index = listbox.curselection()[0]
        tasks[date][index]["completed"] = not tasks[date][index]["completed"]
        save_tasks()
        refresh_listbox(date)
    except:
        messagebox.showwarning("Warning", "Select a task")

def delete_task():
    date = get_selected_date()
    try:
        index = listbox.curselection()[0]
        tasks[date].pop(index)
        if not tasks[date]:
            del tasks[date]
        save_tasks()
        refresh_listbox(date)
    except:
        messagebox.showwarning("Warning", "Select a task to delete")

def clear_tasks_for_date():
    date = get_selected_date()
    if date in tasks and messagebox.askyesno(
        "Confirm", "Clear all tasks for this date?"
    ):
        del tasks[date]
        save_tasks()
        refresh_listbox(date)

# ---------- GUI ----------
root = tk.Tk()
root.title("Monthly To-Do Planner")
root.geometry("620x680")  # 🔧 increased height
root.resizable(False, False)
root.configure(bg="#f4f6f8")

# ---------- Header ----------
header = tk.Frame(root, bg="#2c7be5")
header.pack(fill=tk.X)

tk.Label(
    header,
    text="Monthly To-Do Planner",
    bg="#2c7be5",
    fg="white",
    font=("Arial", 18, "bold")
).pack(pady=15)

# ---------- Main Container ----------
container = tk.Frame(root, bg="#f4f6f8")
container.pack(pady=10)

# ---------- Date Section ----------
date_frame = tk.LabelFrame(
    container, text=" Select Date ",
    font=("Arial", 10, "bold"),
    bg="#f4f6f8", padx=10, pady=10
)
date_frame.pack(fill="x", pady=8)

days = [str(i) for i in range(1, 32)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
years = [str(y) for y in range(2024, 2031)]

day_var = tk.StringVar(value="Day")
month_var = tk.StringVar(value="Month")
year_var = tk.StringVar(value="Year")

row = tk.Frame(date_frame, bg="#f4f6f8")
row.pack()

tk.OptionMenu(row, day_var, *days).pack(side=tk.LEFT, padx=5)
tk.OptionMenu(row, month_var, *months).pack(side=tk.LEFT, padx=5)
tk.OptionMenu(row, year_var, *years).pack(side=tk.LEFT, padx=5)

tk.Button(date_frame, text="Load Tasks", command=load_date_tasks).pack(pady=6)

# ---------- Task Input ----------
task_frame = tk.LabelFrame(
    container, text=" Task ",
    font=("Arial", 10, "bold"),
    bg="#f4f6f8", padx=10, pady=10
)
task_frame.pack(fill="x", pady=8)

task_entry = tk.Entry(task_frame, width=55)
task_entry.pack(pady=5)

tk.Button(
    task_frame, text="Add Task",
    bg="#2c7be5", fg="white",
    width=20, command=add_task
).pack(pady=5)

# ---------- Action Buttons (⬅ MOVED ABOVE LISTBOX) ----------
action_frame = tk.Frame(container, bg="#f4f6f8")
action_frame.pack(pady=8)

tk.Button(
    action_frame, text="Mark Complete / Incomplete",
    width=30, command=toggle_complete
).pack(pady=3)

tk.Button(
    action_frame, text="Delete Selected Task",
    width=30, command=delete_task
).pack(pady=3)

tk.Button(
    action_frame, text="Clear All Tasks for Date",
    width=30, bg="#dc3545", fg="white",
    command=clear_tasks_for_date
).pack(pady=3)

# ---------- Task List ----------
list_frame = tk.LabelFrame(
    container, text=" Tasks ",
    font=("Arial", 10, "bold"),
    bg="#f4f6f8", padx=10, pady=10
)
list_frame.pack(pady=8)

listbox = tk.Listbox(list_frame, width=70, height=12)
listbox.pack()

load_tasks()
root.mainloop()

