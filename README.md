# Student Attendance Tracker

A desktop app built with Python and Tkinter that helps students keep track of their attendance in every subject.

## Problem
Colleges require a minimum of 75% attendance, but students rarely know how many classes they can still miss, or how many they must attend to recover.

## Features
- Add subjects and mark Present / Absent for each class
- Attendance percentage per subject with color-coded status
- Shows how many classes you can miss, or must attend, to stay at 75%
- Edit counts to fix mistakes, and delete subjects
- Overall attendance summary
- Data saved automatically in a CSV file

## Technologies Used
- Python 3
- Tkinter (ttk Treeview) for the GUI / front end
- CSV file storage and attendance calculations for the back end

## Project Structure
```
student-attendance-tracker/
├── main.py
├── README.md
└── .gitignore
```

## How to Run
1. Install Python 3 (Tkinter is included with it).
2. Open a terminal in this folder.
3. Run:
```
python main.py
```

## How the Calculation Works
- Percentage = attended / total x 100
- Classes that can still be missed = attended / 0.75 - total
- Classes needed in a row to reach 75% = (0.75 x total - attended) / 0.25, rounded up


## Author
kartik Chaudhary, DYPIU Sem 1
