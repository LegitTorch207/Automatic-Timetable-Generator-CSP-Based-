# University Timetable Generator

## Overview

The University Timetable Generator is a Python-based desktop application developed using Tkinter. It automatically generates conflict-free class schedules for multiple academic batches while considering teacher availability, room allocation, laboratory requirements, and customizable working days and timings.

The system is designed to reduce the manual effort required for timetable creation and provide an efficient scheduling solution for educational institutions.

---

## Features

### Automatic Timetable Generation

* Generates complete schedules for multiple classes automatically.
* Uses randomized scheduling with conflict checking.
* Attempts multiple scheduling configurations until a valid timetable is found.

### Teacher Conflict Management

* Prevents a teacher from being assigned to more than one class at the same time.
* Ensures teacher availability across all batches.

### Room Allocation System

* Automatically assigns available theory rooms.
* Allocates specialized laboratories according to subject requirements.
* Prevents room clashes.

### Laboratory Scheduling

* Supports dedicated lab subjects.
* Allocates appropriate laboratories based on predefined mappings.
* Schedules lab sessions as continuous blocks.

### Flexible Scheduling Options

Users can customize:

* Working days
* Start time
* End time
* Slot duration (30, 60, or 90 minutes)

### Day-Off Optimization

* Attempts to provide free days for classes whenever possible.
* Distributes lectures across preferred days while minimizing unnecessary spread.

### Graphical User Interface (GUI)

* Built using Tkinter.
* Simple and user-friendly interface.
* Displays generated timetables in a tabular format.
* Color-coded lecture and laboratory sessions.

---

## Technologies Used

* Python 3
* Tkinter (GUI Development)
* Random Module (Schedule Generation Logic)

---

## Project Structure

```text
Project/
│
├── timetable_generator.py
├── README.md
│
├── Class Definitions
├── Room Definitions
├── Laboratory Mapping
├── Scheduling Algorithm
└── Tkinter GUI
```

---

## Scheduling Constraints

The generator ensures:

### Class Constraints

* A class cannot have two subjects scheduled at the same time.

### Teacher Constraints

* A teacher cannot teach multiple classes simultaneously.

### Room Constraints

* A room cannot be assigned to more than one class during the same time slot.

### Laboratory Constraints

* Lab sessions are scheduled in continuous blocks.
* Only compatible laboratories are assigned to lab subjects.

### Subject Hour Requirements

* Each subject receives its required weekly contact hours.

---

## Input Data

The system currently includes:

### Classes

* BSAI-1
* BSAI-2
* BSAI-3
* BSAI-4

### Subjects

Each class contains:

* Subject name
* Assigned teacher
* Required weekly hours
* Subject type (Theory/Lab)

### Rooms

Theory rooms:

* E-101 to E-111
* E-201 to E-211
* E-301 to E-311

Laboratories:

* Lab 1
* Lab 2
* Lab 3
* Lab 4
* Lab 5
* AI Lab
* DLD Lab
* Web Lab
* CN Lab

---

## How to Run

### Prerequisites

Install Python 3.x from:

https://www.python.org/

### Run the Application

```bash
python timetable_generator.py
```

---

## Usage

1. Launch the application.
2. Select days to exclude if required.
3. Set the start time and end time.
4. Choose the desired slot duration.
5. Click **Generate Schedule**.
6. View the generated timetable for all classes.

---

## Future Improvements

* Export timetable to PDF.
* Export timetable to Excel.
* Faculty timetable generation.
* Room utilization reports.
* Department-wide scheduling.
* Database integration.
* Genetic Algorithm optimization.
* Timetable editing functionality.
* Dark mode UI.
* Print-ready timetable layouts.

---

## Educational Purpose

This project was developed as part of a university semester project to demonstrate the practical application of:

* Data Structures
* Constraint Satisfaction Problems (CSP)
* Scheduling Algorithms
* Python Programming
* Graphical User Interface Development
* Software Engineering Principles

---

## Authors

Developed for academic and educational purposes.

Bachelor of Science in Artificial Intelligence (BSAI)

Bahria University Karachi Campus
