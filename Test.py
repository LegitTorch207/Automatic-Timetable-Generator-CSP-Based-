"""
Automatic Timetable Generator
CSP-Based University Scheduler
"""

import tkinter as tk
import random

# =============================================================================
# SECTION 1 — ROOMS
# Theory subjects go in classrooms. Lab subjects go in lab rooms.
# =============================================================================

THEORY_ROOMS = [f"E-{i}" for i in range(101, 112)] + \
               [f"E-{i}" for i in range(201, 212)] + \
               [f"E-{i}" for i in range(301, 312)]

LAB_ROOMS = ["Lab 1", "Lab 2", "Lab 3", "Lab 5", "Lab 6",
             "AI Lab", "DLD Lab", "Web Lab", "AP Lab"]

# Which specific lab(s) each lab subject must use.
# If a subject is not listed here, it can use any lab room.
LAB_MAPPING = {
    "AP-L(A)":  ["AP Lab"],
    "AP-L(B)":  ["AP Lab"],
    "DD-L(A)":  ["DLD Lab"],
    "DD-L(B)":  ["DLD Lab"],
    "DBMS-L":   ["Web Lab"],
    "AI-L":     ["AI Lab"],
    "DCN-L(A)": ["CN Lab"],
    "DCN-L(B)": ["CN Lab"],
    # All others (CP-L, IICT-L, OOP-L, COAL-L, PAI-L, DSA-L) use any lab room
}

# =============================================================================
# SECTION 2 — TIME
# 10 slots per day, each 1 hour, from 08:30 to 17:30
# =============================================================================

TIME_LABELS = ["08:30", "09:30", "10:30", "11:30", "12:30",
               "13:30", "14:30", "15:30", "16:30", "17:30"]
SLOTS       = list(range(10))   # [0, 1, 2, ..., 9]

DAYS_WITH_FRIDAY    = ["Mon", "Tue", "Wed", "Thu", "Fri"]
DAYS_WITHOUT_FRIDAY = ["Mon", "Tue", "Wed", "Thu"]

# =============================================================================
# SECTION 3 — CLASSES
# Each subject needs: teacher, h (hours per week), type (theory or lab)
# Lab subjects are always scheduled as ONE 3-hour block on a single day.
# =============================================================================

CLASSES = {
    "BSAI-1": {
        "PPE":     {"teacher": "Dr. Hassan",  "h": 2, "type": "theory"},
        "IICT-L":  {"teacher": "Dr. Imran",   "h": 3, "type": "lab"},
        "IICT":    {"teacher": "Ms. Munazza", "h": 3, "type": "theory"},
        "DM":      {"teacher": "Ms. Munazza", "h": 3, "type": "theory"},
        "CP-L":    {"teacher": "Ms. Zahida",  "h": 3, "type": "lab"},
        "Tajweed": {"teacher": "Dr. Nawaz",   "h": 1, "type": "theory"},
        "AP":      {"teacher": "Dr. Ali",     "h": 3, "type": "theory"},
        "AP-L(A)": {"teacher": "Sir Fahad",   "h": 3, "type": "lab"},
        "AP-L(B)": {"teacher": "Sir Anas",    "h": 3, "type": "lab"},
        "CP":      {"teacher": "Ms. Salas",   "h": 3, "type": "theory"},
        "IS":      {"teacher": "Sir Anwar",   "h": 2, "type": "theory"},
    },
    "BSAI-2": {
        "DD":      {"teacher": "Ms. Amna",    "h": 3, "type": "theory"},
        "PS":      {"teacher": "Engr. Reema", "h": 3, "type": "theory"},
        "OOP-L":   {"teacher": "Dr. Imran",   "h": 3, "type": "lab"},
        "OOP":     {"teacher": "Sir Ali",     "h": 3, "type": "theory"},
        "DD-L(A)": {"teacher": "Ms. Amna",    "h": 3, "type": "lab"},
        "DD-L(B)": {"teacher": "Sir Haroon",  "h": 3, "type": "lab"},
        "FE":      {"teacher": "Sir Chauhan", "h": 3, "type": "theory"},
        "PST":     {"teacher": "Ms. Farah",   "h": 2, "type": "theory"},
        "UQ-1":    {"teacher": "Sir Muneeb",  "h": 1, "type": "theory"},
        "AC&AG":   {"teacher": "Ms. Sadia",   "h": 3, "type": "theory"},
    },
    "BSAI-3": {
        "DSA":    {"teacher": "Dr. Bilal",  "h": 3, "type": "theory"},
        "DSA-L":  {"teacher": "Dr. Bilal",  "h": 3, "type": "lab"},
        "COAL":   {"teacher": "Sir Asim",   "h": 2, "type": "theory"},
        "COAL-L": {"teacher": "Sir Asim",   "h": 3, "type": "lab"},
        "PAI":    {"teacher": "Dr. Sana",   "h": 3, "type": "theory"},
        "PAI-L":  {"teacher": "Dr. Sana",   "h": 3, "type": "lab"},
        "LA":     {"teacher": "Dr. Kamran", "h": 3, "type": "theory"},
        "CS":     {"teacher": "Sir Noman",  "h": 2, "type": "theory"},
        "UQ-2":   {"teacher": "Dr. Nawaz",  "h": 1, "type": "theory"},
        "CCE":    {"teacher": "Ms. Salas",  "h": 2, "type": "theory"},
    },
    "BSAI-4": {
        "DBMS":    {"teacher": "Dr. Ayesha", "h": 3, "type": "theory"},
        "DBMS-L":  {"teacher": "Dr. Ayesha", "h": 3, "type": "lab"},
        "ENT":     {"teacher": "Ms. Farah",  "h": 2, "type": "theory"},
        "AI":      {"teacher": "Dr. Bilal",  "h": 3, "type": "theory"},
        "AI-L":    {"teacher": "Dr. Bilal",  "h": 3, "type": "lab"},
        "CT":      {"teacher": "Sir Noman",  "h": 3, "type": "theory"},
        "DCN":     {"teacher": "Dr. Kamran", "h": 3, "type": "theory"},
        "DCN-L(A)":{"teacher": "Dr. Kamran", "h": 3, "type": "lab"},
        "DCN-L(B)":{"teacher": "Dr. Kamran", "h": 3, "type": "lab"},
        "UQ-3":    {"teacher": "Dr. Nawaz",  "h": 3, "type": "theory"},
    },
}

# =============================================================================
# SECTION 4 — CSP SOLVER
# =============================================================================

def get_rooms_for(subject, stype):
    """Return the list of allowed rooms for a given subject and type."""
    if stype == "lab":
        return LAB_MAPPING.get(subject, LAB_ROOMS)   # pinned or any lab
    return THEORY_ROOMS


def can_place(timetable, teacher_busy, room_busy, cls, day, start, length, teacher, room):
    """
    Check if 'length' consecutive slots starting at 'start' are free
    for this class, teacher, and room.
    """
    if start + length > len(SLOTS):
        return False
    for s in range(start, start + length):
        if timetable[cls][day][s]:          return False   # class already has a slot here
        if (teacher, day, s) in teacher_busy: return False   # teacher is busy
        if (room,    day, s) in room_busy:    return False   # room is taken
    return True


def place(timetable, teacher_busy, room_busy, cls, day, start, length, teacher, room, subject):
    """Write the subject into all required slots and mark teacher/room as busy."""
    for s in range(start, start + length):
        timetable[cls][day][s] = (subject, room)
        teacher_busy[(teacher, day, s)] = True
        room_busy[(room,    day, s)] = True


def try_schedule(days):
    """
    One attempt to build a full clash-free timetable.
    Returns the timetable dict on success, or None on failure.
    """
    # timetable[class][day] = list of 10 slots, each None or (subject, room)
    timetable    = {cls: {d: [None] * 10 for d in days} for cls in CLASSES}
    teacher_busy = {}   # (teacher, day, slot) -> True
    room_busy    = {}   # (room,    day, slot) -> True

    # Flatten all subjects into one list and shuffle for randomness
    all_subjects = [
        (cls, sub, info)
        for cls, subjects in CLASSES.items()
        for sub, info in subjects.items()
    ]
    random.shuffle(all_subjects)

    for cls, sub, info in all_subjects:
        teacher = info["teacher"]
        rooms   = get_rooms_for(sub, info["type"])

        # ── LAB: place as one 3-hour block ────────────────────────────────
        if info["type"] == "lab":
            placed = False
            for day in random.sample(days, len(days)):
                for start in random.sample(SLOTS, len(SLOTS)):
                    for room in random.sample(rooms, len(rooms)):
                        if can_place(timetable, teacher_busy, room_busy,
                                     cls, day, start, 3, teacher, room):
                            place(timetable, teacher_busy, room_busy,
                                  cls, day, start, 3, teacher, room, sub)
                            placed = True
                            break
                    if placed: break
                if placed: break
            if not placed:
                return None   # this attempt failed — caller will retry

        # ── THEORY: place each hour individually ──────────────────────────
        else:
            for _ in range(info["h"]):
                placed = False
                for day in random.sample(days, len(days)):
                    for start in random.sample(SLOTS, len(SLOTS)):

                        # Hard constraint: no 3 consecutive hours of same subject
                        if start >= 2:
                            prev1 = timetable[cls][day][start - 1]
                            prev2 = timetable[cls][day][start - 2]
                            if prev1 and prev2 and prev1[0] == sub and prev2[0] == sub:
                                continue

                        for room in random.sample(rooms, len(rooms)):
                            if can_place(timetable, teacher_busy, room_busy,
                                         cls, day, start, 1, teacher, room):
                                place(timetable, teacher_busy, room_busy,
                                      cls, day, start, 1, teacher, room, sub)
                                placed = True
                                break
                        if placed: break
                    if placed: break
                if not placed:
                    return None   # this attempt failed — caller will retry

    return timetable   # all subjects placed successfully


def generate_solution(include_friday=True, attempts=200):
    """
    Try up to 'attempts' times to find a valid timetable.
    Returns (timetable, days) — timetable is None if no solution found.
    """
    days = DAYS_WITH_FRIDAY if include_friday else DAYS_WITHOUT_FRIDAY
    for _ in range(attempts):
        result = try_schedule(days)
        if result:
            return result, days
    return None, days


# =============================================================================
# SECTION 5 — GUI
# =============================================================================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic Timetable Generator")

        self.include_friday = tk.BooleanVar(value=True)

        # ── Controls ──────────────────────────────────────────────────────
        top = tk.Frame(root)
        top.pack(fill="x", padx=5, pady=5)

        tk.Label(top, text="Automatic Timetable Generator",
                 font=("TkDefaultFont", 13, "bold")).pack(side="left", padx=5)
        tk.Checkbutton(top, text="Include Friday",
                       variable=self.include_friday).pack(side="left", padx=10)
        tk.Button(top, text="Generate Timetable",
                  command=self.generate).pack(side="left")

        self.status = tk.Label(root, text="", anchor="w")
        self.status.pack(fill="x", padx=5)

        # ── Scrollable display area ───────────────────────────────────────
        canvas    = tk.Canvas(root)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

        self.frame = tk.Frame(canvas)
        self.frame.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def generate(self):
        # Clear previous output
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.status.config(text="Solving... please wait.")
        self.root.update_idletasks()

        timetable, days = generate_solution(self.include_friday.get())

        if timetable is None:
            self.status.config(text="No solution found. Try enabling Friday.")
            tk.Label(self.frame, text="No solution found.").pack()
            return

        total_slots = sum(
            1 for cls_data in timetable.values()
            for day_data in cls_data.values()
            for slot in day_data if slot
        )
        self.status.config(text=f"Timetable Generated Successfully! ({total_slots} slots assigned)")

        # Draw one table per class
        for cls, data in timetable.items():
            # Class heading
            tk.Label(self.frame, text=cls,
                     font=("TkDefaultFont", 11, "bold")).pack(pady=(10, 2))

            table = tk.Frame(self.frame)
            table.pack(pady=(0, 6))

            # Header row: blank corner + one column per time slot
            tk.Label(table, text="Day / Time",
                     borderwidth=1, relief="solid", width=6).grid(row=0, column=0)
            for col, label in enumerate(TIME_LABELS, start=1):
                tk.Label(table, text=label,
                         borderwidth=1, relief="solid", width=11).grid(row=0, column=col)

            # One row per day
            for row, day in enumerate(days, start=1):
                tk.Label(table, text=day,
                         borderwidth=1, relief="solid", width=6).grid(row=row, column=0)

                for col, slot_value in enumerate(data[day], start=1):
                    if slot_value:
                        subject, room = slot_value
                        text = f"{subject}\n{room}"
                    else:
                        text = "-"
                    tk.Label(table, text=text, width=11, height=2,
                             borderwidth=1, relief="solid").grid(row=row, column=col)


# =============================================================================
# SECTION 6 — RUN
# =============================================================================

root = tk.Tk()
App(root)
root.mainloop()