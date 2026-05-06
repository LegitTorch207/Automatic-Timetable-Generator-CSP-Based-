import tkinter as tk
import random

# ---------------------------
# THEORY ROOMS
# ---------------------------

THEORY_ROOMS = [f"E-{i}" for i in range(101, 112)] + \
               [f"E-{i}" for i in range(201, 212)] + \
               [f"E-{i}" for i in range(301, 312)]

# ---------------------------
# LAB ROOMS
# ---------------------------

LAB_ROOMS = [
    "Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 5",
    "AI Lab", "DLD Lab", "Web Lab", "AP Lab, CN Lab"
]

# ---------------------------
# LAB CONSTRAINTS
# ---------------------------

LAB_MAPPING = {
    "AP-L(A)": ["AP Lab"],
    "AP-L(B)": ["AP Lab"],
    "CP-L": ["Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 5", "AI Lab"],
    "IICT-L": ["Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 5", "AI Lab"],
    "OOP-L": ["Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 5", "AI Lab"],
    "DD-L(A)": ["DLD Lab"],
    "DD-L(B)": ["DLD Lab"],
    "COAL-L": ["Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 5", "AI Lab"],
    "PAI-L": ["Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 5", "AI Lab"],
    "DSA-L": ["Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 5", "AI Lab"],
    "DBMS-L": ["Web Lab"],
    "DCN-L(A)": ["CN Lab"],
    "DCN-L(B)": ["CN Lab"],
    "AI-L" : ["AI Lab"],
    }

# ---------------------------
# TIME
# ---------------------------

TIME_SLOTS = list(range(10))
TIME_LABELS = ["08:30","09:30","10:30","11:30","12:30","13:30","14:30","15:30","16:30", "17:30"]

DAYS_FULL = ["Mon", "Tue", "Wed", "Thu", "Fri"]
DAYS_NO_FRIDAY = ["Mon", "Tue", "Wed", "Thu"]

# ---------------------------
# YOUR DATA (UNCHANGED)
# ---------------------------

CLASSES = {
    "BSAI-1": {
        "PPE": {"teacher": "Dr. Hassan", "h": 2, "type": "theory"},
        "IICT-L": {"teacher": "Dr. Imran", "h": 3, "type": "lab"},
        "IICT": {"teacher": "Ms. Munazza", "h": 3, "type": "theory"},
        "DM": {"teacher": "Ms. Munazza", "h": 3, "type": "theory"},
        "CP-L": {"teacher": "Ms. Zahida", "h": 3, "type": "lab"},
        "Tajweed": {"teacher": "Dr. Nawaz", "h": 1, "type": "theory"},
        "AP": {"teacher": "Dr. Ali", "h": 3, "type": "theory"},
        "AP-L(A)": {"teacher": "Sir Fahad", "h": 3, "type": "lab"},
        "AP-L(B)": {"teacher": "Sir Anas", "h": 3, "type": "lab"},
        "CP": {"teacher": "Ms. Salas", "h": 3, "type": "theory"},
        "IS": {"teacher": "Sir Anwar", "h": 2, "type": "theory"},
    },

    "BSAI-2": {
        "DD": {"teacher": "Ms. Amna", "h": 3, "type": "theory"},
        "PS": {"teacher": "Engr. Reema", "h": 3, "type": "theory"},
        "OOP-L": {"teacher": "Dr. Imran", "h": 3, "type": "lab"},
        "OOP": {"teacher": "Sir Ali", "h": 3, "type": "theory"},
        "DD-L(A)": {"teacher": "Ms. Amna", "h": 3, "type": "lab"},
        "DD-L(B)": {"teacher": "Sir Haroon", "h": 3, "type": "lab"},
        "FE": {"teacher": "Sir Chauhan", "h": 3, "type": "theory"},
        "PST": {"teacher": "Ms. Farah", "h": 2, "type": "theory"},
        "UQ-1": {"teacher": "Sir Muneeb", "h": 1, "type": "theory"},
        "AC&AG": {"teacher": "Ms. Sadia", "h": 3, "type": "theory"},
    },

    "BSAI-3": {
        "DSA": {"teacher": "Dr. Bilal", "h": 3, "type": "theory"},
        "DSA-L": {"teacher": "Dr. Bilal", "h": 3, "type": "lab"},
        "COAL": {"teacher": "Sir Asim", "h": 2, "type": "theory"},
        "COAL-L": {"teacher": "Sir Asim", "h": 3, "type": "lab"},
        "PAI": {"teacher": "Dr. Sana", "h": 3, "type": "theory"},
        "PAI-L": {"teacher": "Dr. Sana", "h": 3, "type": "lab"},
        "LA": {"teacher": "Dr. Kamran", "h": 3, "type": "theory"},
        "CS": {"teacher": "Sir Noman", "h": 2, "type": "theory"},
        "UQ-2": {"teacher": "Dr. Nawaz", "h": 1, "type": "theory"},
        "CCE": {"teacher": "Ms. Salas", "h": 2, "type": "theory"},
    },

    "BSAI-4": {
        "DBMS": {"teacher": "Dr. Ayesha", "h": 3, "type": "theory"},
        "DBMS-L": {"teacher": "Dr. Ayesha", "h": 3, "type": "lab"},
        "ENT": {"teacher": "Ms. Farah", "h": 2, "type": "theory"},
        "AI": {"teacher": "Dr. Bilal", "h": 3, "type": "theory"},
        "AI-L": {"teacher": "Dr. Bilal", "h": 3, "type": "lab"},
        "CT": {"teacher": "Sir Noman", "h": 3, "type": "theory"},
        "DCN": {"teacher": "Dr. Kamran", "h": 3, "type": "theory"},
        "DCN-L(A)": {"teacher": "Dr. Kamran", "h": 3, "type": "lab"},
        "DCN-L(B)": {"teacher": "Dr. Kamran", "h": 3, "type": "lab"},
        "UQ-3": {"teacher": "Dr. Nawaz", "h": 1, "type": "theory"},
    }
}

# ---------------------------
# CSP GENERATOR
# ---------------------------

def get_allowed_rooms(sub, typ):
    if typ == "lab":
        return LAB_MAPPING.get(sub, LAB_ROOMS)
    return THEORY_ROOMS

def generate_solution(include_friday=True, attempts=200):
    days = DAYS_FULL if include_friday else DAYS_NO_FRIDAY

    for _ in range(attempts):

        timetable = {cls: {d: [None]*10 for d in days} for cls in CLASSES}
        teacher_busy = {}
        room_busy = {}

        items = []
        for cls, subs in CLASSES.items():
            for sub, info in subs.items():
                items.append((cls, sub, info))

        random.shuffle(items)

        def can_place(cls, sub, info, day, start, room):
            length = 3 if info["type"] == "lab" else info["h"]
            teacher = info["teacher"]

            if start + length > 10:
                return False

            for s in range(start, start+length):
                if timetable[cls][day][s]:
                    return False
                if (teacher, day, s) in teacher_busy:
                    return False
                if (room, day, s) in room_busy:
                    return False

            return True

        def place(cls, sub, info, day, start, room):
            length = 3 if info["type"] == "lab" else info["h"]
            teacher = info["teacher"]

            for s in range(start, start+length):
                timetable[cls][day][s] = (sub, room)
                teacher_busy[(teacher, day, s)] = True
                room_busy[(room, day, s)] = True

        success = True

        for cls, sub, info in items:

            # ---------------------------
            # LABS (UNCHANGED)
            # ---------------------------
            if info["type"] == "lab":
                placed = False

                for day in random.sample(days, len(days)):
                    for start in random.sample(TIME_SLOTS, len(TIME_SLOTS)):
                        rooms = get_allowed_rooms(sub, info["type"])
                        rooms = random.sample(rooms, len(rooms))

                        for r in rooms:
                            if can_place(cls, sub, info, day, start, r):
                                place(cls, sub, info, day, start, r)
                                placed = True
                                break
                        if placed:
                            break
                    if placed:
                        break

                if not placed:
                    success = False
                    break

            # ---------------------------
            # THEORY (NO 3 CONSECUTIVE)
            # ---------------------------
            else:
                hours_needed = info["h"]

                for _ in range(hours_needed):
                    placed = False

                    for day in random.sample(days, len(days)):
                        for start in random.sample(TIME_SLOTS, len(TIME_SLOTS)):

                            # 🚫 Prevent 3 consecutive slots of same subject
                            if start >= 2:
                                prev1 = timetable[cls][day][start-1]
                                prev2 = timetable[cls][day][start-2]
                                if prev1 and prev2 and prev1[0] == sub and prev2[0] == sub:
                                    continue

                            rooms = get_allowed_rooms(sub, info["type"])
                            rooms = random.sample(rooms, len(rooms))

                            for r in rooms:
                                if can_place(
                                    cls, sub,
                                    {"teacher": info["teacher"], "h": 1, "type": "theory"},
                                    day, start, r
                                ):
                                    place(
                                        cls, sub,
                                        {"teacher": info["teacher"], "h": 1, "type": "theory"},
                                        day, start, r
                                    )
                                    placed = True
                                    break

                            if placed:
                                break
                        if placed:
                            break

                    if not placed:
                        success = False
                        break

        if success:
            return timetable, days

    return None, days
# ---------------------------
# SCROLLABLE GUI
# ---------------------------

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CSP Timetable")

        self.include_friday = tk.BooleanVar(value=True)

        top = tk.Frame(root)
        top.pack(fill="x")

        tk.Checkbutton(top, text="Include Friday", variable=self.include_friday).pack(side="left")
        tk.Button(top, text="Generate", command=self.generate).pack(side="left")

        # Scroll setup
        canvas = tk.Canvas(root)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

        self.scroll_frame = tk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def clear(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

    def generate(self):
        self.clear()

        timetable, days = generate_solution(self.include_friday.get())

        if timetable is None:
            tk.Label(self.scroll_frame, text="No solution found").pack()
            return

        for cls, data in timetable.items():

            tk.Label(self.scroll_frame, text=cls, font=("Arial", 12, "bold")).pack()

            frame = tk.Frame(self.scroll_frame)
            frame.pack(pady=5)

            tk.Label(frame, text="Day/Time", borderwidth=1, relief="solid").grid(row=0, column=0)

            for i, t in enumerate(TIME_LABELS):
                tk.Label(frame, text=t, borderwidth=1, relief="solid").grid(row=0, column=i+1)

            for r, d in enumerate(days):
                tk.Label(frame, text=d, borderwidth=1, relief="solid").grid(row=r+1, column=0)

                for c in range(10):
                    val = data[d][c]
                    text = f"{val[0]}\n{val[1]}" if val else "-"

                    tk.Label(frame, text=text, width=11, height=2,
                             borderwidth=1, relief="solid").grid(row=r+1, column=c+1)


# ---------------------------
# RUN
# ---------------------------

root = tk.Tk()
app = App(root)
root.mainloop()