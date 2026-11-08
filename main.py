# Student Attendance Tracker
# Mini project using Python and Tkinter

import csv
import math
import os
from tkinter import *
from tkinter import ttk, messagebox

BASE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE, "attendance.csv")
REQUIRED = 75  # minimum attendance percentage

subjects = []  # each item: [name, attended, total]

BG = "#f3f6fb"
BLUE = "#2563eb"
DARK = "#0f172a"
GRAY = "#64748b"


def load_data():
    subjects.clear()
    if not os.path.exists(FILE):
        return
    with open(FILE, newline="") as f:
        for row in csv.reader(f):
            if len(row) == 3 and row[0] != "subject":
                try:
                    subjects.append([row[0], int(row[1]), int(row[2])])
                except ValueError:
                    continue


def save_data():
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["subject", "attended", "total"])
        writer.writerows(subjects)


def percentage(attended, total):
    if total == 0:
        return 0
    return attended / total * 100


def get_status(attended, total):
    """Returns (status text, color tag)."""
    if total == 0:
        return "No classes yet", "none"
    pct = percentage(attended, total)
    r = REQUIRED / 100
    if pct >= REQUIRED:
        # classes that can be missed while staying at or above REQUIRED
        can_miss = int(attended / r - total + 1e-9)
        tag = "ok" if pct >= REQUIRED + 5 else "warn"
        return "Safe: can miss " + str(can_miss) + " more", tag
    # classes needed in a row to reach REQUIRED
    need = math.ceil((r * total - attended) / (1 - r) - 1e-9)
    return "Low: attend next " + str(need) + " classes", "low"


def refresh(select_index=None):
    for row in tree.get_children():
        tree.delete(row)

    for i, (name, att, tot) in enumerate(subjects):
        status, tag = get_status(att, tot)
        tree.insert("", END, iid=str(i), tags=(tag,),
                    values=(name, att, tot, str(round(percentage(att, tot), 1)) + "%", status))

    total_att = sum(s[1] for s in subjects)
    total_cls = sum(s[2] for s in subjects)
    overall = round(percentage(total_att, total_cls), 1)
    lbl_overall.config(text="Overall attendance: " + str(overall) + "%   (" +
                       str(total_att) + " / " + str(total_cls) + " classes)")

    if select_index is not None and select_index < len(subjects):
        tree.selection_set(str(select_index))


def add_subject():
    name = e_subject.get().strip()
    if name == "":
        messagebox.showerror("Error", "Enter a subject name")
        return
    for s in subjects:
        if s[0].lower() == name.lower():
            messagebox.showerror("Error", "Subject already exists")
            return
    subjects.append([name, 0, 0])
    save_data()
    e_subject.delete(0, END)
    refresh(len(subjects) - 1)


def mark(present):
    sel = tree.selection()
    if not sel:
        messagebox.showerror("Error", "Select a subject first")
        return
    i = int(sel[0])
    subjects[i][2] += 1
    if present:
        subjects[i][1] += 1
    save_data()
    refresh(i)


def edit_counts():
    sel = tree.selection()
    if not sel:
        messagebox.showerror("Error", "Select a subject first")
        return
    i = int(sel[0])

    win = Toplevel(root)
    win.title("Edit counts - " + subjects[i][0])
    win.geometry("300x200")
    win.config(bg="white")
    win.resizable(False, False)

    Label(win, text="Classes attended", bg="white").pack(pady=(15, 2))
    e_att = Entry(win, justify=CENTER)
    e_att.pack()
    e_att.insert(0, str(subjects[i][1]))

    Label(win, text="Total classes held", bg="white").pack(pady=(10, 2))
    e_tot = Entry(win, justify=CENTER)
    e_tot.pack()
    e_tot.insert(0, str(subjects[i][2]))

    def save_edit():
        try:
            a = int(e_att.get())
            t = int(e_tot.get())
        except ValueError:
            messagebox.showerror("Error", "Enter whole numbers")
            return
        if a < 0 or t < 0 or a > t:
            messagebox.showerror("Error", "Attended cannot be more than total")
            return
        subjects[i][1] = a
        subjects[i][2] = t
        save_data()
        refresh(i)
        win.destroy()

    Button(win, text="Save", command=save_edit, bg=BLUE, fg="white", bd=0,
           padx=20, pady=6).pack(pady=18)


def delete_subject():
    sel = tree.selection()
    if not sel:
        messagebox.showerror("Error", "Select a subject first")
        return
    i = int(sel[0])
    if messagebox.askyesno("Confirm", "Delete " + subjects[i][0] + "?"):
        subjects.pop(i)
        save_data()
        refresh()


# ---------- GUI ----------
root = Tk()
root.title("Student Attendance Tracker")
root.geometry("900x560")
root.config(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

header = Frame(root, bg=BLUE, height=70)
header.pack(fill=X)
header.pack_propagate(False)
Label(header, text="Student Attendance Tracker", font=("Segoe UI", 18, "bold"),
      bg=BLUE, fg="white").pack(side=LEFT, padx=24)
Label(header, text="Required: " + str(REQUIRED) + "%", font=("Segoe UI", 11),
      bg=BLUE, fg="#dbeafe").pack(side=RIGHT, padx=24)

top = Frame(root, bg=BG)
top.pack(fill=X, padx=18, pady=(16, 8))
Label(top, text="New subject:", bg=BG, fg=GRAY, font=("Segoe UI", 10)).pack(side=LEFT)
e_subject = Entry(top, font=("Segoe UI", 11), bd=1, relief=SOLID, width=28)
e_subject.pack(side=LEFT, padx=8, ipady=4)
Button(top, text="Add Subject", command=add_subject, bg=BLUE, fg="white",
       font=("Segoe UI", 10, "bold"), bd=0, padx=14, pady=6, cursor="hand2").pack(side=LEFT)

table = Frame(root, bg=BG)
table.pack(fill=BOTH, expand=True, padx=18, pady=8)

cols = ("Subject", "Attended", "Total", "Percent", "Status")
tree = ttk.Treeview(table, columns=cols, show="headings", selectmode="browse")
widths = (200, 80, 80, 80, 300)
for c, w in zip(cols, widths):
    tree.heading(c, text=c)
    tree.column(c, width=w, anchor=W if c in ("Subject", "Status") else CENTER)
tree.tag_configure("ok", foreground="#16a34a")
tree.tag_configure("warn", foreground="#d97706")
tree.tag_configure("low", foreground="#dc2626")
tree.tag_configure("none", foreground=GRAY)

scroll = Scrollbar(table, command=tree.yview)
tree.config(yscrollcommand=scroll.set)
scroll.pack(side=RIGHT, fill=Y)
tree.pack(side=LEFT, fill=BOTH, expand=True)

btns = Frame(root, bg=BG)
btns.pack(fill=X, padx=18, pady=8)
Button(btns, text="Mark Present", command=lambda: mark(True), bg="#16a34a", fg="white",
       font=("Segoe UI", 10, "bold"), bd=0, padx=16, pady=8, cursor="hand2").pack(side=LEFT)
Button(btns, text="Mark Absent", command=lambda: mark(False), bg="#dc2626", fg="white",
       font=("Segoe UI", 10, "bold"), bd=0, padx=16, pady=8, cursor="hand2").pack(side=LEFT, padx=8)
Button(btns, text="Edit counts", command=edit_counts, bg="#e0e7ff", fg="#3730a3",
       font=("Segoe UI", 10, "bold"), bd=0, padx=14, pady=8, cursor="hand2").pack(side=LEFT)
Button(btns, text="Delete Subject", command=delete_subject, bg="#fee2e2", fg="#b91c1c",
       font=("Segoe UI", 10, "bold"), bd=0, padx=14, pady=8, cursor="hand2").pack(side=LEFT, padx=8)

lbl_overall = Label(root, text="", bg=BG, fg=DARK, font=("Segoe UI", 11, "bold"))
lbl_overall.pack(pady=(4, 14))

load_data()
refresh()
root.mainloop()
