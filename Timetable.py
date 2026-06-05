import tkinter as tk
from tkinter import ttk
import random

THEORY_ROOMS = []
for number in range(101, 112):
    THEORY_ROOMS.append("E-" + str(number))
for number in range(201, 212):
    THEORY_ROOMS.append("E-" + str(number))
for number in range(301, 312):
    THEORY_ROOMS.append("E-" + str(number))
    
LAB_ROOMS = ["Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 5", "AI Lab", "DLD Lab", "Web Lab", "CN Lab"]

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
    "AI-L": ["AI Lab"],
}

CLASSES = {
    "BSAI-1": {
        "PPE": {"teacher": "Dr. Hassan", "hours_needed": 2, "type": "theory"},
        "IICT-L": {"teacher": "Dr. Imran", "hours_needed": 3, "type": "lab"},
        "IICT": {"teacher": "Ms. Munazza", "hours_needed": 3, "type": "theory"},
        "DM": {"teacher": "Ms. Munazza", "hours_needed": 3, "type": "theory"},
        "CP-L": {"teacher": "Ms. Zahida", "hours_needed": 3, "type": "lab"},
        "Tajweed": {"teacher": "Dr. Nawaz", "hours_needed": 1, "type": "theory"},
        "AP": {"teacher": "Dr. Ali", "hours_needed": 3, "type": "theory"},
        "AP-L(A)": {"teacher": "Sir Fahad", "hours_needed": 3, "type": "lab"},
        "AP-L(B)": {"teacher": "Sir Anas", "hours_needed": 3, "type": "lab"},
        "CP": {"teacher": "Ms. Salas", "hours_needed": 3, "type": "theory"},
        "IS": {"teacher": "Sir Anwar", "hours_needed": 2, "type": "theory"},
    },
    "BSAI-2": {
        "DD": {"teacher": "Ms. Amna", "hours_needed": 3, "type": "theory"},
        "PS": {"teacher": "Engr. Reema", "hours_needed": 3, "type": "theory"},
        "OOP-L": {"teacher": "Dr. Imran", "hours_needed": 3, "type": "lab"},
        "OOP": {"teacher": "Sir Ali", "hours_needed": 3, "type": "theory"},
        "DD-L(A)": {"teacher": "Ms. Amna", "hours_needed": 3, "type": "lab"},
        "DD-L(B)": {"teacher": "Sir Haroon", "hours_needed": 3, "type": "lab"},
        "FE": {"teacher": "Sir Chauhan", "hours_needed": 3, "type": "theory"},
        "PST": {"teacher": "Ms. Farah", "hours_needed": 2, "type": "theory"},
        "UQ-1": {"teacher": "Sir Muneeb", "hours_needed": 1, "type": "theory"},
        "AC&AG": {"teacher": "Ms. Sadia", "hours_needed": 3, "type": "theory"},
    },
    "BSAI-3": {
        "DSA": {"teacher": "Dr. Bilal", "hours_needed": 3, "type": "theory"},
        "DSA-L": {"teacher": "Dr. Bilal", "hours_needed": 3, "type": "lab"},
        "COAL": {"teacher": "Sir Asim", "hours_needed": 2, "type": "theory"},
        "COAL-L": {"teacher": "Sir Asim", "hours_needed": 3, "type": "lab"},
        "PAI": {"teacher": "Dr. Sana", "hours_needed": 3, "type": "theory"},
        "PAI-L": {"teacher": "Dr. Sana", "hours_needed": 3, "type": "lab"},
        "LA": {"teacher": "Dr. Kamran", "hours_needed": 3, "type": "theory"},
        "CS": {"teacher": "Sir Noman", "hours_needed": 2, "type": "theory"},
        "UQ-2": {"teacher": "Dr. Nawaz", "hours_needed": 1, "type": "theory"},
        "CCE": {"teacher": "Ms. Salas", "hours_needed": 2, "type": "theory"},
    },
    "BSAI-4": {
        "DBMS": {"teacher": "Dr. Ayesha", "hours_needed": 3, "type": "theory"},
        "DBMS-L": {"teacher": "Dr. Ayesha", "hours_needed": 3, "type": "lab"},
        "ENT": {"teacher": "Ms. Farah", "hours_needed": 2, "type": "theory"},
        "AI": {"teacher": "Dr. Bilal", "hours_needed": 3, "type": "theory"},
        "AI-L": {"teacher": "Dr. Bilal", "hours_needed": 3, "type": "lab"},
        "CT": {"teacher": "Sir Noman", "hours_needed": 3, "type": "theory"},
        "DCN": {"teacher": "Dr. Kamran", "hours_needed": 3, "type": "theory"},
        "DCN-L(A)": {"teacher": "Dr. Kamran", "hours_needed": 3, "type": "lab"},
        "DCN-L(B)": {"teacher": "Dr. Kamran", "hours_needed": 3, "type": "lab"},
        "UQ-3": {"teacher": "Dr. Nawaz", "hours_needed": 1, "type": "theory"},
    }
}

def generate_timetable_logic(active_days, total_slots_available):
    for attempt in range(200):
        timetable = {}
        for class_name in CLASSES:
            day_map = {}
            for day_name in active_days:
                day_map[day_name] = [None] * total_slots_available
            timetable[class_name] = day_map

        teacher_busy_status = {}
        room_busy_status = {}

        # --- DYNAMIC TARGET DAYS OFF CONFIGURATION ---
        # For each class, pre-determine which days we WANT to use and which days we WANT TO AVOID.
        class_day_priorities = {}
        for class_name in CLASSES:
            if len(active_days) >= 6:
                days_off_target = 2  # Try to give 2 days off if week layout is large
            elif len(active_days) >= 4:
                days_off_target = 1  # Try to give 1 day off for standard 4-5 active days
            else:
                days_off_target = 0

            shuffled_active = random.sample(active_days, len(active_days))
            if days_off_target > 0:
                preferred = shuffled_active[:-days_off_target]
                avoided = shuffled_active[-days_off_target:]
            else:
                preferred = shuffled_active
                avoided = []
            class_day_priorities[class_name] = (preferred, avoided)
        # ---------------------------------------------

        tasks_to_schedule = []
        for class_name, subjects_dict in CLASSES.items():
            for subject_name, subject_info in subjects_dict.items():
                tasks_to_schedule.append((class_name, subject_name, subject_info))
        
        random.shuffle(tasks_to_schedule)

        def check_if_safe(class_name, subject_info, day, start_slot, room, duration):
            if start_slot + duration > total_slots_available:
                return False
            
            current_teacher = subject_info["teacher"]
            for current_slot in range(start_slot, start_slot + duration):
                if timetable[class_name][day][current_slot] is not None:
                    return False
                if (current_teacher, day, current_slot) in teacher_busy_status:
                    return False
                if (room, day, current_slot) in room_busy_status:
                    return False
            return True

        def mark_as_booked(class_name, subject_name, subject_info, day, start_slot, room, duration):
            current_teacher = subject_info["teacher"]
            for current_slot in range(start_slot, start_slot + duration):
                timetable[class_name][day][current_slot] = (subject_name, room)
                teacher_busy_status[(current_teacher, day, current_slot)] = True
                room_busy_status[(room, day, current_slot)] = True

        overall_success_flag = True
        for class_name, subject_name, subject_info in tasks_to_schedule:
            is_lab_class = (subject_info["type"] == "lab")

            if is_lab_class:
                schedule_blocks = [3]  
            else:
                hours = subject_info["hours_needed"]
                if hours == 1:
                    schedule_blocks = [1]
                elif hours == 2:
                    schedule_blocks = [2]  
                elif hours == 3:
                    schedule_blocks = [2, 1]  
                elif hours == 4:
                    schedule_blocks = [2, 2]  
                else:
                    schedule_blocks = [1] * hours

            used_days_for_subject = []

            for current_duration in schedule_blocks:
                subject_was_placed = False

                # --- COMPACTED DAY SELECTION ---
                # Retrieve the preferred and avoided day tiers for this specific class.
                # Shuffle internally so there's still local variation, but preferred always come first.
                pref_days, avoid_days = class_day_priorities[class_name]
                shuffled_days = random.sample(pref_days, len(pref_days)) + random.sample(avoid_days, len(avoid_days))
                # -------------------------------

                shuffled_slots = random.sample(range(total_slots_available), total_slots_available)

                for day in shuffled_days:
                    if len(schedule_blocks) > 1 and current_duration == 1 and day in used_days_for_subject:
                        continue
                    
                    allowed_rooms = LAB_MAPPING.get(subject_name, LAB_ROOMS) if is_lab_class else THEORY_ROOMS
                    shuffled_rooms = random.sample(allowed_rooms, len(allowed_rooms))

                    for slot in shuffled_slots:
                        for room in shuffled_rooms:
                            if check_if_safe(class_name, subject_info, day, slot, room, current_duration):
                                mark_as_booked(
                                    class_name,
                                    subject_name,
                                    subject_info,
                                    day,
                                    slot,
                                    room,
                                    current_duration
                                )
                                used_days_for_subject.append(day)
                                subject_was_placed = True
                                break
                        if subject_was_placed:
                            break
                    if subject_was_placed: break
                
                if not subject_was_placed:
                    overall_success_flag = False
                    break
            if not overall_success_flag: break
        
        if overall_success_flag:
            return timetable
    return None

class SimpleTimetableUI:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("Timetable Generator")
        self.main_window.geometry("1300x850")

        time_options = []
        for hour in range(24):
            time_options.append(f"{hour:02d}:00")
            time_options.append(f"{hour:02d}:30")

        sidebar_frame = ttk.Frame(main_window, padding=20)
        sidebar_frame.pack(side="left", fill="y")

        ttk.Label(sidebar_frame, text="SETTINGS", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Label(sidebar_frame, text="Exclude These Days:").pack(anchor="w")
        self.day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.exclude_check_variables = {}
        for day in self.day_names:
            check_var = tk.BooleanVar(value=False)
            self.exclude_check_variables[day] = check_var
            ttk.Checkbutton(sidebar_frame, text=day, variable=check_var).pack(anchor="w")

        ttk.Label(sidebar_frame, text="\nDay Starts At:").pack(anchor="w")
        self.start_time_dropdown = ttk.Combobox(sidebar_frame, values=time_options, state="readonly")
        self.start_time_dropdown.set("08:30")
        self.start_time_dropdown.pack(fill="x")

        ttk.Label(sidebar_frame, text="Day Ends At:").pack(anchor="w")
        self.end_time_dropdown = ttk.Combobox(sidebar_frame, values=time_options, state="readonly")
        self.end_time_dropdown.set("16:30")
        self.end_time_dropdown.pack(fill="x")

        ttk.Label(sidebar_frame, text="Slot Length (Minutes):").pack(anchor="w")
        self.slot_length_dropdown = ttk.Combobox(sidebar_frame, values=[30, 60, 90], state="readonly")
        self.slot_length_dropdown.set(60)
        self.slot_length_dropdown.pack(fill="x")

        ttk.Button(sidebar_frame, text="GENERATE SCHEDULE", command=self.handle_generate_click).pack(pady=30, fill="x")

        self.display_canvas = tk.Canvas(main_window, bg="white")
        self.display_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(main_window, orient="vertical", command=self.display_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.display_canvas.configure(yscrollcommand=scrollbar.set)

        self.internal_scroll_frame = ttk.Frame(self.display_canvas)
        self.display_canvas.create_window((0, 0), window=self.internal_scroll_frame, anchor="nw")
        self.internal_scroll_frame.bind("<Configure>", lambda event: self.display_canvas.configure(scrollregion=self.display_canvas.bbox("all")))

    def handle_generate_click(self):
        for child in self.internal_scroll_frame.winfo_children():
            child.destroy()

        active_days_list = []
        for day in self.day_names:
            if self.exclude_check_variables[day].get() == False:
                active_days_list.append(day)

        if not active_days_list:
            tk.Label(self.internal_scroll_frame, text="Error: Please keep at least one day active!").pack()
            return

        def get_total_minutes(time_string):
            parts = time_string.split(":")
            return int(parts[0]) * 60 + int(parts[1])

        start_total_minutes = get_total_minutes(self.start_time_dropdown.get())
        end_total_minutes = get_total_minutes(self.end_time_dropdown.get())
        minutes_per_slot = int(self.slot_length_dropdown.get())

        available_minutes = end_total_minutes - start_total_minutes
        total_slots_needed = available_minutes // minutes_per_slot

        if total_slots_needed <= 0:
            tk.Label(self.internal_scroll_frame, text="Error: End time must be later than start time!").pack()
            return

        time_header_labels = []
        for index in range(total_slots_needed):
            minutes_at_this_slot = start_total_minutes + (index * minutes_per_slot)
            hour_display = minutes_at_this_slot // 60
            minute_display = minutes_at_this_slot % 60
            time_header_labels.append(f"{hour_display:02d}:{minute_display:02d}")

        final_timetable = generate_timetable_logic(active_days_list, total_slots_needed)

        if final_timetable is None:
            tk.Label(self.internal_scroll_frame, text="Could not find a valid schedule. Try adding more time or days.").pack(pady=20)
            return

        for class_name, days_data in final_timetable.items():
            tk.Label(self.internal_scroll_frame, text=f"SCHEDULE FOR: {class_name}", font=("Arial", 14, "bold")).pack(pady=(25, 5))
            
            table_container = ttk.Frame(self.internal_scroll_frame)
            table_container.pack(padx=10, pady=10)

            tk.Label(table_container, text="Day / Time", relief="ridge", width=12).grid(row=0, column=0)
            for column_index, time_string in enumerate(time_header_labels):
                tk.Label(table_container, text=time_string, relief="ridge", width=12).grid(row=0, column=column_index + 1)

            for row_index, day_name in enumerate(active_days_list):
                tk.Label(table_container, text=day_name, relief="ridge", width=12).grid(row=row_index + 1, column=0)
                for column_index in range(total_slots_needed):
                    slot_content = days_data[day_name][column_index]
                    
                    cell_text = "-"
                    cell_color = "white"
                    
                    if slot_content is not None:
                        subject_name, room_name = slot_content
                        cell_text = subject_name + "\n" + room_name
                        if "-L" in subject_name:
                            cell_color = "#E1FFD7" 
                        else:
                            cell_color = "#E1F2FF" 

                    cell_label = tk.Label(table_container, text=cell_text, bg=cell_color, relief="solid", 
                                          borderwidth=1, width=12, height=3, font=("Arial", 9))
                    cell_label.grid(row=row_index + 1, column=column_index + 1)

root_window = tk.Tk()
app_instance = SimpleTimetableUI(root_window)
root_window.mainloop()