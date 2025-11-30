# ui/quick_query_gui.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from src.db.validators import *
from src.db import QuickQueryDAO
from datetime import datetime

class QuickQueryGUI:

    def __init__(self, root, password):
        self.root = root
        self.root.title("COMP2411 DATABASE PROJECT")
        self.service = QuickQueryDAO(password=password)

        # 主 Notebook 分页
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建各功能页
        self.create_employee_tab()
        self.create_activity_tab()
        self.create_temp_employee_tab()
        self.create_location_tab()
        self.create_supervision_tab()
        self.create_general_report_tab()
        self.create_sql_tab()

        # 状态栏
        self.status = tk.Label(root, text="All set!!!", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)



    def update_status(self, msg):
        self.status.config(text=msg)

    def clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    #员工管理有关：
    def create_employee_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="EMP Manage")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Search All", command=self.show_all_employees).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Search by SSN", command=self.lookup_employee_by_ssn).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update EMP", command=self.add_employee_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update level", command=self.update_employee_level_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete EMP", command=self.delete_employee_gui).pack(side=tk.LEFT, padx=5)

        self.emp_tree = ttk.Treeview(frame, columns=("SSN", "Name", "Level"), show="headings")
        self.emp_tree.heading("SSN", text="SSN")
        self.emp_tree.heading("Name", text="Name")
        self.emp_tree.heading("Level", text="Level")
        self.emp_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    # ------ the function to create an adding-employee dialog ------
    def add_employee_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("New Employee")
        dialog.geometry("380x200") # size changed
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.focus_set()

        # Ssn
        ttk.Label(dialog, text="Ssn:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ssn_var = tk.StringVar()
        ssn_entry = ttk.Entry(dialog, textvariable=ssn_var, width=30)
        ssn_entry.grid(row=0, column=1, padx=10, pady=10)

        # Name
        ttk.Label(dialog, text="Name:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(dialog, textvariable=name_var, width=30)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Levels (using a menu)
        ttk.Label(dialog, text="Level:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        level_var = tk.StringVar()
        level_combo = ttk.Combobox(
            dialog,
            textvariable=level_var,
            values=["executive officer", "mid_level manager", "base_level worker"],
            state="readonly",  # only allow choices, not allow inputs
            width=27
        )
        level_combo.grid(row=2, column=1, padx=10, pady=10)
        level_combo.set("base_level worker")  # default value

        # button
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)

        def on_submit():
            ssn = ssn_var.get().strip()
            name = name_var.get().strip()
            level = level_var.get().strip()

            if not ssn or not name or not level:
                messagebox.showwarning("Input Error", "All Sections Require Inputs", parent=dialog)
                return

            try:
                self.service.add_employee(ssn, name, level)
                messagebox.showinfo("Success", "Employee Registered", parent=dialog)
                self.show_all_employees()  # renew the list
                dialog.destroy()
            except ValueError as e:
                # catch errors thrown by DAO
                messagebox.showwarning("Instruction Failed", str(e), parent=dialog)
            except Exception as e:
                # catch other errors
                messagebox.showerror("System Failed", str(e), parent=dialog)

        def on_cancel():
            dialog.destroy()

        ttk.Button(button_frame, text="OK", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=10)

        # focus on this dialog first
        ssn_entry.focus()
        # ------ finish editing ------

    # ------ Below are functions for "Employee" section ------

    # 1. finish
    def show_all_employees(self):
        try:
            self.clear_tree(self.emp_tree)
            emps = self.service.get_all_employees() # return a list of dictionary

            for emp in emps:
                # get qualified tuples ("SSN", "Name", "Level")
                values = (
                    emp.get('Ssn', ''),
                    emp.get('Name', ''),
                    emp.get('Emp_Level', '')
                )
                self.emp_tree.insert("", "end", values=values)

            self.update_status(f"load {len(emps)} employees")
        except Exception as e:
            messagebox.showerror("error", str(e), parent=self.root)
    # settle both gui and cli

    # 2. finish
    def add_employee_gui(self):
        # trigger adding_employee dialog
        self.add_employee_dialog()
    # settle both gui and cli

    # 3. finish
    def lookup_employee_by_ssn(self):
        ssn = simpledialog.askstring("Search Employee", "Input Ssn:", parent=self.root)
        if ssn is None:  # if users click cancel
            return

        ssn = ssn.strip()
        if not ssn:
            messagebox.showwarning("Error", "Empty Ssn", parent=self.root)
            return

        try:
            result = self.service.get_employee_by_ssn(ssn)
            self.clear_tree(self.emp_tree)

            if result and len(result) > 0:
                emp = result[0]
                values = (
                    emp.get('Ssn', ''),
                    emp.get('Name', ''),
                    emp.get('Emp_Level', '')
                )
                self.emp_tree.insert("", "end", values=values)
                self.update_status(f"find employee：{values[1]}")
            else:
                messagebox.showinfo("Attention", "No such employee.", parent=self.root)
                self.update_status("Employee not found")

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)
            self.update_status("Wrong search")
    # settle both gui and cli

    # 4. finish
    def update_employee_level_gui(self):
        ssn = simpledialog.askstring("Update", "Employee Ssn:")
        new_level_str = simpledialog.askstring("Update", "New level (executive officer, mid_level manager, base_level worker):")
        if ssn and new_level_str:
            try:
                new_level = new_level_str
                self.service.update_employee(ssn, new_level)
                messagebox.showinfo("Success", "Level Updated.")
                self.show_all_employees()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    # settle both gui and cli

    # 5. finish
    def delete_employee_gui(self):
        ssn = simpledialog.askstring("Delete", "Employee Ssn:")
        if ssn:
            if messagebox.askyesno("Confirm", f"Sure to delete employee {ssn} ?"):
                try:
                    self.service.delete_employee(ssn)
                    messagebox.showinfo("Success", "Employee deleted")
                    self.show_all_employees()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
    # settle both gui and cli
    # ------ Below are functions for "Activity" section ------
    def create_activity_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Activity Manage")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Show all", command=self.show_all_activities).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Create new", command=self.create_activity_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Assign", command=self.assign_activity_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remove", command=self.remove_activity_gui).pack(side=tk.LEFT, padx=5)

        self.act_tree = ttk.Treeview(frame, columns=("Time", "Type", "Chemical Required", "Building", "Floor", "Room"),
                                     show="headings")
        self.act_tree.heading("Time", text="time")
        self.act_tree.heading("Type", text="type")
        self.act_tree.heading("Chemical Required", text="chemical")
        self.act_tree.heading("Building", text="building")
        self.act_tree.heading("Floor", text="floor")
        self.act_tree.heading("Room", text="room")
        self.act_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    # 1. finish
    def show_all_activities(self):
        try:
            self.clear_tree(self.act_tree)
            activities = self.service.get_all_activities()
            for activity in activities:
                values = (
                    activity.get('Activity_Time', ''),
                    activity.get('Activity_Type', ''),
                    activity.get('Require_Chemical', ''),
                    activity.get('Activity_Building', ''),
                    activity.get('Activity_Floor', ''),
                    activity.get('Activity_RoomNum', '')
                )
                self.act_tree.insert("", "end", values=values)
            self.update_status(f"load {len(activities)} activities")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    # settle both gui and cli

    # 2. finish
    def create_activity_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("create new activities")
        dialog.geometry("500x350") # size changed
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.focus_set()

        # time
        ttk.Label(dialog, text="time:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        time_var = tk.StringVar()
        time_entry = ttk.Entry(dialog, textvariable=time_var, width=30)
        time_entry.grid(row=0, column=1, padx=10, pady=10)

        # type
        ttk.Label(dialog, text="type:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(
            dialog,
            textvariable=type_var,
            values=["daily campus cleaning", "campus ageing", "weather-related issues"],
            state="readonly",
            width=27
        )
        type_combo.grid(row=1, column=1, padx=10, pady=10)

        # chemical needed
        ttk.Label(dialog, text="chemical needed:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        chemical_var = tk.StringVar()
        chemical_combo = ttk.Combobox(
            dialog,
            textvariable=chemical_var,
            values=["yes", "no"],
            state="readonly",
            width=27
        )
        chemical_combo.grid(row=2, column=1, padx=10, pady=10)
        chemical_combo.set("no")

        # building
        ttk.Label(dialog, text="building:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        building_var = tk.StringVar()
        building_entry = ttk.Entry(dialog, textvariable=building_var, width=30)
        building_entry.grid(row=3, column=1, padx=10, pady=10)

        # floor
        ttk.Label(dialog, text="floor:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        floor_var = tk.StringVar()
        floor_entry = ttk.Entry(dialog, textvariable=floor_var, width=30)
        floor_entry.grid(row=4, column=1, padx=10, pady=10)

        # room
        ttk.Label(dialog, text="room:").grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        room_var = tk.StringVar()
        room_entry = ttk.Entry(dialog, textvariable=room_var, width=30)
        room_entry.grid(row=5, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=6, column=0, columnspan=2, pady=15)

        def on_submit():
            time = time_var.get().strip()
            activity_type = type_var.get().strip()
            if chemical_var.get().strip() == 'yes':
                chemical = 1
            else:
                chemical = 0
            building = building_var.get().strip()
            floor = floor_var.get().strip()
            room = room_var.get().strip()

            if not all([time, activity_type, building, floor, room]):
                messagebox.showwarning("Input Error", "All blanks need to be filled.", parent=dialog)
                return

            try:
                self.service.create_activity(time, activity_type, chemical, building, floor, room)
                messagebox.showinfo("Success", "Success creation.", parent=dialog)
                self.show_all_activities()
                dialog.destroy()
            except ValueError as e:
                messagebox.showwarning("Set fail.", str(e), parent=dialog)
            except Exception as e:
                messagebox.showerror("System Error.", str(e), parent=dialog)

        def on_cancel():
            dialog.destroy()

        ttk.Button(button_frame, text="Confirm", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=10)

        time_entry.focus()
    # settle both gui and cli

    def create_activity_gui(self):
        self.create_activity_dialog()

    def assign_activity_gui(self):
        type_dialog = tk.Toplevel(self.root)
        type_dialog.title("assign activity")
        type_dialog.geometry("500x200")
        type_dialog.resizable(False, False)
        type_dialog.transient(self.root)
        type_dialog.grab_set()

        ttk.Label(type_dialog, text="choose type:").pack(pady=10)

        assign_type = tk.StringVar()
        type_combo = ttk.Combobox(
            type_dialog,
            textvariable=assign_type,
            values=["mid_level manager", "employee", "temp_employee"],
            state="readonly",
            width=20
        )
        type_combo.pack(pady=10)
        type_combo.set("mid_level manager")

        def on_type_selected():
            type_dialog.destroy()
            worker_type = assign_type.get()

            if worker_type == "mid_level manager":
                self.assign_manager_dialog()
            elif worker_type == "employee":
                self.assign_employee_dialog()
            elif worker_type == "temp_employee":
                self.assign_temp_employee_dialog()

        ttk.Button(type_dialog, text="next step", command=on_type_selected).pack(pady=10)

    def assign_manager_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("assign mid_level manager")
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        try:
            managers = self.service.get_employees_by_level("mid_level manager")
            manager_ssns = [manager.get('Ssn', '') for manager in managers]
        except Exception as e:
            messagebox.showerror("Error", f"fetch failed: {str(e)}", parent=dialog)
            dialog.destroy()
            return


        ttk.Label(dialog, text="manager Ssn:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ssn_var = tk.StringVar()
        ssn_combo = ttk.Combobox(dialog, textvariable=ssn_var, values=manager_ssns, state="readonly", width=30)
        ssn_combo.grid(row=0, column=1, padx=10, pady=10)


        ttk.Label(dialog, text="time:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        time_var = tk.StringVar()
        time_entry = ttk.Entry(dialog, textvariable=time_var, width=30)
        time_entry.grid(row=1, column=1, padx=10, pady=10)


        ttk.Label(dialog, text="building:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        building_var = tk.StringVar()
        building_entry = ttk.Entry(dialog, textvariable=building_var, width=30)
        building_entry.grid(row=2, column=1, padx=10, pady=10)


        ttk.Label(dialog, text="floor:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        floor_var = tk.StringVar()
        floor_entry = ttk.Entry(dialog, textvariable=floor_var, width=30)
        floor_entry.grid(row=3, column=1, padx=10, pady=10)


        ttk.Label(dialog, text="room:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        room_var = tk.StringVar()
        room_entry = ttk.Entry(dialog, textvariable=room_var, width=30)
        room_entry.grid(row=4, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        def on_submit():
            ssn = ssn_var.get().strip()
            time = time_var.get().strip()
            building = building_var.get().strip()
            floor = floor_var.get().strip()
            room = room_var.get().strip()

            if not all([ssn, time, building, floor, room]):
                messagebox.showwarning("Error", "Blank lines!", parent=dialog)
                return

            try:
                self.service.assign_manager_to_activity(ssn, time, building, floor, room)
                messagebox.showinfo("success", "Set successfully.", parent=dialog)
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="Confirm", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def assign_employee_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("assign base employee")
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 获取所有普通员工
        try:
            employees = self.service.get_employees_by_level("base_level worker")
            employee_ssns = [emp.get('Ssn', '') for emp in employees]
        except Exception as e:
            messagebox.showerror("Error", f"fetch failed: {str(e)}", parent=dialog)
            dialog.destroy()
            return

        # SSN选择
        ttk.Label(dialog, text="employee Ssn:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ssn_var = tk.StringVar()
        ssn_combo = ttk.Combobox(dialog, textvariable=ssn_var, values=employee_ssns, state="readonly", width=30)
        ssn_combo.grid(row=0, column=1, padx=10, pady=10)

        # 活动时间
        ttk.Label(dialog, text="time:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        time_var = tk.StringVar()
        time_entry = ttk.Entry(dialog, textvariable=time_var, width=30)
        time_entry.grid(row=1, column=1, padx=10, pady=10)

        # 楼栋
        ttk.Label(dialog, text="building:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        building_var = tk.StringVar()
        building_entry = ttk.Entry(dialog, textvariable=building_var, width=30)
        building_entry.grid(row=2, column=1, padx=10, pady=10)

        # 楼层
        ttk.Label(dialog, text="floor:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        floor_var = tk.StringVar()
        floor_entry = ttk.Entry(dialog, textvariable=floor_var, width=30)
        floor_entry.grid(row=3, column=1, padx=10, pady=10)

        # 房间
        ttk.Label(dialog, text="room:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        room_var = tk.StringVar()
        room_entry = ttk.Entry(dialog, textvariable=room_var, width=30)
        room_entry.grid(row=4, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        def on_submit():
            ssn = ssn_var.get().strip()
            time = time_var.get().strip()
            building = building_var.get().strip()
            floor = floor_var.get().strip()
            room = room_var.get().strip()

            if not all([ssn, time, building, floor, room]):
                messagebox.showwarning("Error", "Blank lines!", parent=dialog)
                return

            try:
                self.service.assign_employee_to_activity(time, building, floor, room, ssn)
                messagebox.showinfo("Success", "Assign successfully.", parent=dialog)
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="Confirm", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def assign_temp_employee_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("assign temp employee")
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 获取所有临时工
        try:
            temp_employees = self.service.get_all_temp_employees_with_companies()
            temp_ssns = [temp.get('TempSsn', '') for temp in temp_employees]
        except Exception as e:
            messagebox.showerror("Error", f"fetch failed: {str(e)}", parent=dialog)
            dialog.destroy()
            return

        # SSN选择
        ttk.Label(dialog, text="temp employee Ssn:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ssn_var = tk.StringVar()
        ssn_combo = ttk.Combobox(dialog, textvariable=ssn_var, values=temp_ssns, state="readonly", width=30)
        ssn_combo.grid(row=0, column=1, padx=10, pady=10)

        # 活动时间
        ttk.Label(dialog, text="time:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        time_var = tk.StringVar()
        time_entry = ttk.Entry(dialog, textvariable=time_var, width=30)
        time_entry.grid(row=1, column=1, padx=10, pady=10)

        # 楼栋
        ttk.Label(dialog, text="building:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        building_var = tk.StringVar()
        building_entry = ttk.Entry(dialog, textvariable=building_var, width=30)
        building_entry.grid(row=2, column=1, padx=10, pady=10)

        # 楼层
        ttk.Label(dialog, text="floor:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        floor_var = tk.StringVar()
        floor_entry = ttk.Entry(dialog, textvariable=floor_var, width=30)
        floor_entry.grid(row=3, column=1, padx=10, pady=10)

        # 房间
        ttk.Label(dialog, text="room:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        room_var = tk.StringVar()
        room_entry = ttk.Entry(dialog, textvariable=room_var, width=30)
        room_entry.grid(row=4, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        def on_submit():
            ssn = ssn_var.get().strip()
            time = time_var.get().strip()
            building = building_var.get().strip()
            floor = floor_var.get().strip()
            room = room_var.get().strip()

            if not all([ssn, time, building, floor, room]):
                messagebox.showwarning("Error", "Blank lines!", parent=dialog)
                return

            try:
                self.service.assign_temp_employee_to_activity(time, building, floor, room, ssn)
                messagebox.showinfo("Success", "Assign successfully.", parent=dialog)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="Confirm", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def remove_activity_gui(self):
        # 第一步：选择移除类型
        type_dialog = tk.Toplevel(self.root)
        type_dialog.title("remove activities")
        type_dialog.geometry("500x200")
        type_dialog.resizable(False, False)
        type_dialog.transient(self.root)
        type_dialog.grab_set()

        ttk.Label(type_dialog, text="choose type:").pack(pady=10)

        remove_type = tk.StringVar()
        type_combo = ttk.Combobox(
            type_dialog,
            textvariable=remove_type,
            values=["mid_level manager", "employee", "temp_employee"],
            state="readonly",
            width=20
        )
        type_combo.pack(pady=10)
        type_combo.set("mid_level manager")

        def on_type_selected():
            type_dialog.destroy()
            worker_type = remove_type.get()

            if worker_type == "mid_level manager":
                self.remove_manager_dialog()
            elif worker_type == "employee":
                self.remove_employee_dialog()
            elif worker_type == "temp_employee":
                self.remove_temp_employee_dialog()

        ttk.Button(type_dialog, text="next type", command=on_type_selected).pack(pady=10)

    def remove_manager_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("remove mid_level manager")
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 获取所有中层经理
        try:
            managers = self.service.get_employees_by_level("mid_level manager")
            manager_ssns = [manager.get('Ssn', '') for manager in managers]
        except Exception as e:
            messagebox.showerror("Error", f"fetch failed: {str(e)}", parent=dialog)
            dialog.destroy()
            return

        # SSN选择
        ttk.Label(dialog, text="manager Ssn:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ssn_var = tk.StringVar()
        ssn_combo = ttk.Combobox(dialog, textvariable=ssn_var, values=manager_ssns, state="readonly", width=30)
        ssn_combo.grid(row=0, column=1, padx=10, pady=10)

        # 活动时间
        ttk.Label(dialog, text="time:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        time_var = tk.StringVar()
        time_entry = ttk.Entry(dialog, textvariable=time_var, width=30)
        time_entry.grid(row=1, column=1, padx=10, pady=10)

        # 楼栋
        ttk.Label(dialog, text="building:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        building_var = tk.StringVar()
        building_entry = ttk.Entry(dialog, textvariable=building_var, width=30)
        building_entry.grid(row=2, column=1, padx=10, pady=10)

        # 楼层
        ttk.Label(dialog, text="floor:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        floor_var = tk.StringVar()
        floor_entry = ttk.Entry(dialog, textvariable=floor_var, width=30)
        floor_entry.grid(row=3, column=1, padx=10, pady=10)

        # 房间
        ttk.Label(dialog, text="room:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        room_var = tk.StringVar()
        room_entry = ttk.Entry(dialog, textvariable=room_var, width=30)
        room_entry.grid(row=4, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        def on_submit():
            ssn = ssn_var.get().strip()
            time = time_var.get().strip()
            building = building_var.get().strip()
            floor = floor_var.get().strip()
            room = room_var.get().strip()

            if not all([ssn, time, building, floor, room]):
                messagebox.showwarning("Error", "Blank lines!", parent=dialog)
                return

            if messagebox.askyesno("confirm", f"confirm removing {ssn} ?", parent=dialog):
                try:
                    self.service.remove_manager_from_activity(ssn, time, building, floor, room)
                    messagebox.showinfo("Success", "remove successfully", parent=dialog)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="Confirm", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def remove_employee_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("remove base level employee")
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 获取所有普通员工
        try:
            employees = self.service.get_employees_by_level("base_level worker")
            employee_ssns = [emp.get('Ssn', '') for emp in employees]
        except Exception as e:
            messagebox.showerror("Error", f"fetch failed: {str(e)}", parent=dialog)
            dialog.destroy()
            return

        # SSN选择
        ttk.Label(dialog, text="employee Ssn:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ssn_var = tk.StringVar()
        ssn_combo = ttk.Combobox(dialog, textvariable=ssn_var, values=employee_ssns, state="readonly", width=30)
        ssn_combo.grid(row=0, column=1, padx=10, pady=10)

        # 活动时间
        ttk.Label(dialog, text="time:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        time_var = tk.StringVar()
        time_entry = ttk.Entry(dialog, textvariable=time_var, width=30)
        time_entry.grid(row=1, column=1, padx=10, pady=10)

        # 楼栋
        ttk.Label(dialog, text="building:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        building_var = tk.StringVar()
        building_entry = ttk.Entry(dialog, textvariable=building_var, width=30)
        building_entry.grid(row=2, column=1, padx=10, pady=10)

        # 楼层
        ttk.Label(dialog, text="floor:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        floor_var = tk.StringVar()
        floor_entry = ttk.Entry(dialog, textvariable=floor_var, width=30)
        floor_entry.grid(row=3, column=1, padx=10, pady=10)

        # 房间
        ttk.Label(dialog, text="room:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        room_var = tk.StringVar()
        room_entry = ttk.Entry(dialog, textvariable=room_var, width=30)
        room_entry.grid(row=4, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        def on_submit():
            ssn = ssn_var.get().strip()
            time = time_var.get().strip()
            building = building_var.get().strip()
            floor = floor_var.get().strip()
            room = room_var.get().strip()

            if not all([ssn, time, building, floor, room]):
                messagebox.showwarning("Error", "Blank lines!", parent=dialog)
                return

            if messagebox.askyesno("confirm", f"confirm removing {ssn} ?", parent=dialog):
                try:
                    self.service.remove_employee_from_activity(time, building, floor, room, ssn)
                    messagebox.showinfo("Success", "remove successfully", parent=dialog)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="Confirm", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def remove_temp_employee_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("remove temp employee")
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 获取所有临时工
        try:
            temp_employees = self.service.get_all_temp_employees_with_companies()
            temp_ssns = [temp.get('TempSsn', '') for temp in temp_employees]
        except Exception as e:
            messagebox.showerror("Error", f"fetch failed: {str(e)}", parent=dialog)
            dialog.destroy()
            return

        # SSN选择
        ttk.Label(dialog, text="temp Ssn:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ssn_var = tk.StringVar()
        ssn_combo = ttk.Combobox(dialog, textvariable=ssn_var, values=temp_ssns, state="readonly", width=30)
        ssn_combo.grid(row=0, column=1, padx=10, pady=10)

        # 活动时间
        ttk.Label(dialog, text="time:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        time_var = tk.StringVar()
        time_entry = ttk.Entry(dialog, textvariable=time_var, width=30)
        time_entry.grid(row=1, column=1, padx=10, pady=10)

        # 楼栋
        ttk.Label(dialog, text="building:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        building_var = tk.StringVar()
        building_entry = ttk.Entry(dialog, textvariable=building_var, width=30)
        building_entry.grid(row=2, column=1, padx=10, pady=10)

        # 楼层
        ttk.Label(dialog, text="floor:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        floor_var = tk.StringVar()
        floor_entry = ttk.Entry(dialog, textvariable=floor_var, width=30)
        floor_entry.grid(row=3, column=1, padx=10, pady=10)

        # 房间
        ttk.Label(dialog, text="room:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        room_var = tk.StringVar()
        room_entry = ttk.Entry(dialog, textvariable=room_var, width=30)
        room_entry.grid(row=4, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        def on_submit():
            ssn = ssn_var.get().strip()
            time = time_var.get().strip()
            building = building_var.get().strip()
            floor = floor_var.get().strip()
            room = room_var.get().strip()

            if not all([ssn, time, building, floor, room]):
                messagebox.showwarning("Error", "Blank lines!", parent=dialog)
                return

            if messagebox.askyesno("confirm", f"confirm removing {ssn} ?", parent=dialog):
                try:
                    self.service.remove_temp_employee_from_activity(time, building, floor, room, ssn)
                    messagebox.showinfo("Success", "remove successfully", parent=dialog)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="Confirm", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    # ---------- 临时工管理 ----------
    def create_temp_employee_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Temp Employee Management")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Show All Temp Employees", command=self.show_all_temp_employees).pack(side=tk.LEFT,
                                                                                                         padx=5)
        ttk.Button(btn_frame, text="Create New Temp Employee", command=self.create_temp_employee_gui).pack(side=tk.LEFT,
                                                                                                           padx=5)
        ttk.Button(btn_frame, text="Delete Temp Employee", command=self.delete_temp_employee_gui).pack(side=tk.LEFT,
                                                                                                       padx=5)

        self.temp_tree = ttk.Treeview(frame, columns=("TempSSN", "Company"), show="headings")
        self.temp_tree.heading("TempSSN", text="Temp SSN")
        self.temp_tree.heading("Company", text="Company")
        self.temp_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def show_all_temp_employees(self):
        try:
            self.clear_tree(self.temp_tree)
            temp_employees = self.service.get_all_temp_employees()
            for temp_emp in temp_employees:
                values = (
                    temp_emp.get('TempSsn', ''),
                    temp_emp.get('Company_name', '')
                )
                self.temp_tree.insert("", "end", values=values)
            self.update_status(f"Loaded {len(temp_employees)} temp employees")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_temp_employee_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("New Temp Employee")
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.focus_set()

        # Temp SSN
        ttk.Label(dialog, text="Temp SSN:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ssn_var = tk.StringVar()
        ssn_entry = ttk.Entry(dialog, textvariable=ssn_var, width=30)
        ssn_entry.grid(row=0, column=1, padx=10, pady=10)

        # Company
        ttk.Label(dialog, text="Company:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        company_var = tk.StringVar()
        company_entry = ttk.Entry(dialog, textvariable=company_var, width=30)
        company_entry.grid(row=1, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)

        def on_submit():
            ssn = ssn_var.get().strip()
            company = company_var.get().strip()

            if not ssn or not company:
                messagebox.showwarning("Input Error", "Both Temp SSN and Company are required", parent=dialog)
                return

            try:
                # Use the same company name for both company_name and contractor_company_name parameters
                self.service.create_temp_employee_with_company(ssn, company, company)
                messagebox.showinfo("Success", "Temp employee created successfully", parent=dialog)
                self.show_all_temp_employees()
                dialog.destroy()
            except ValueError as e:
                messagebox.showwarning("Creation Failed", str(e), parent=dialog)
            except Exception as e:
                messagebox.showerror("System Error", str(e), parent=dialog)

        def on_cancel():
            dialog.destroy()

        ttk.Button(button_frame, text="OK", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=10)

        ssn_entry.focus()

    def create_temp_employee_gui(self):
        self.create_temp_employee_dialog()

    def delete_temp_employee_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Temp Employee")
        dialog.geometry("300x120")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Get all temp employees for the dropdown
        try:
            temp_employees = self.service.get_all_temp_employees()
            temp_ssns = [temp_emp.get('TempSsn', '') for temp_emp in temp_employees]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load temp employees: {str(e)}", parent=dialog)
            dialog.destroy()
            return

        ttk.Label(dialog, text="Select Temp SSN to delete:").pack(pady=10)

        ssn_var = tk.StringVar()
        ssn_combo = ttk.Combobox(
            dialog,
            textvariable=ssn_var,
            values=temp_ssns,
            state="readonly",
            width=25
        )
        ssn_combo.pack(pady=5)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def on_submit():
            selected_ssn = ssn_var.get().strip()
            if not selected_ssn:
                messagebox.showwarning("Input Error", "Please select a temp employee to delete", parent=dialog)
                return

            if messagebox.askyesno("Confirm", f"Are you sure you want to delete temp employee {selected_ssn}?",
                                   parent=dialog):
                try:
                    self.service.delete_temp_employee(selected_ssn)
                    messagebox.showinfo("Success", "Temp employee deleted successfully", parent=dialog)
                    self.show_all_temp_employees()
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="Delete", command=on_submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def delete_temp_employee_gui(self):
        self.delete_temp_employee_dialog()

    # ---------- 位置管理 ----------------------------------------------------------------------------------------------------------------------------------------------
    # ---------- 位置管理 ----------------------------------------------------------------------------------------------------------------------------------------------
    def create_location_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="位置管理")

        # 功能按钮区（顶部）
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5, fill=tk.X)

        ttk.Button(btn_frame, text="查看所有位置", command=self.show_all_locations).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加新位置", command=self.add_new_location).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="查看空闲办公室", command=self.show_vacant_offices).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="查看所有办公室", command=self.show_all_offices).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="按建筑筛选", command=self.filter_locations_by_building).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="分配办公室", command=self.assign_office_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清退办公室", command=self.vacate_office_gui).pack(side=tk.LEFT, padx=5)

        # 数据显示区（Treeview）
        self.loc_tree = ttk.Treeview(frame, columns=("Bldg", "Floor", "Room"), show="headings")
        self.loc_tree.heading("Bldg", text="楼")
        self.loc_tree.heading("Floor", text="层")
        self.loc_tree.heading("Room", text="房间")
        self.loc_tree.column("Bldg", width=150)
        self.loc_tree.column("Floor", width=80, anchor=tk.CENTER)
        self.loc_tree.column("Room", width=80, anchor=tk.CENTER)

        tree_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.loc_tree.yview)
        self.loc_tree.configure(yscrollcommand=tree_scroll.set)

        self.loc_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # 新增：添加新位置
    def add_new_location(self):
        building = simpledialog.askstring("添加位置", "建筑名称:", parent=self.root)
        if not building:
            return
        try:
            floor = simpledialog.askinteger("添加位置", "楼层（整数）:", parent=self.root)
            room = simpledialog.askinteger("添加位置", "房间号（整数）:", parent=self.root)
            if floor is None or room is None:
                return
            # 调用 service 方法（假设你已有 create_location）
            self.service.create_location(building, floor, room)
            messagebox.showinfo("成功", f"位置 {building} {floor}层-{room} 已添加", parent=self.root)
            self.show_all_locations()  # 自动刷新
        except ValueError:
            messagebox.showerror("输入错误", "楼层和房间号必须为整数", parent=self.root)
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    # 新增：按建筑筛选
    def filter_locations_by_building(self):
        building = simpledialog.askstring("筛选位置", "请输入建筑名称:", parent=self.root)
        if not building:
            return
        try:
            self.clear_tree(self.loc_tree)
            locs = self.service.get_locations_by_building(building)  # 假设你已有此方法
            if not locs:
                messagebox.showinfo("提示", f"建筑 '{building}' 下无位置记录", parent=self.root)
            for l in locs:
                # 假设 locs 中每个元素是 (Building, Floor, Room_number) 元组或字典
                if isinstance(l, dict):
                    values = (l['Building'], l['Floor'], l['Room_number'])
                else:
                    values = l  # 假设是元组
                self.loc_tree.insert("", "end", values=values)
            self.update_status(f"已筛选 {len(locs)} 条记录")
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    # 保留你已有的方法（此处仅示意，你已有）
    def show_all_locations(self):
        try:
            self.clear_tree(self.loc_tree)
            locs = self.service.get_all_locations()
            for l in locs:
                if isinstance(l, dict):
                    values = (l['Building'], l['Floor'], l['Room_number'])
                else:
                    values = l
                self.loc_tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    def show_vacant_offices(self):
        try:
            self.clear_tree(self.loc_tree)
            locs = self.service.get_vacant_offices()
            for l in locs:
                if isinstance(l, dict):
                    values = (l['Office_Building'], l['Office_Floor'], l['Office_RoomNum'])
                else:
                    values = l
                self.loc_tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    def assign_office_gui(self):
        # 输入办公室信息
        building = simpledialog.askstring("分配办公室", "建筑:", parent=self.root)
        if not building:
            return
        try:
            floor = simpledialog.askinteger("分配办公室", "楼层（整数）:", parent=self.root)
            room = simpledialog.askinteger("分配办公室", "房间号（整数）:", parent=self.root)
            if floor is None or room is None:
                return
            # 输入员工 SSN
            ssn = simpledialog.askstring("分配办公室", "员工 SSN:", parent=self.root)
            if not ssn:
                return

            # 调用 service 方法
            result = self.service.assign_office_to_employee(building, floor, room, ssn)
            if result == "The employee has an office.":
                messagebox.showwarning("分配失败", "该员工已分配办公室！", parent=self.root)
            elif result == "Not valid!":
                messagebox.showerror("输入错误", "楼层或房间号格式无效！", parent=self.root)
            else:
                messagebox.showinfo("成功", f"办公室 {building} {floor}-{room} 已分配给 {ssn}", parent=self.root)
                self.show_vacant_offices()  # 自动刷新空闲列表
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)


    def vacate_office_gui(self):
        building = simpledialog.askstring("清退办公室", "建筑:", parent=self.root)
        if not building:
            return
        try:
            floor = simpledialog.askinteger("清退办公室", "楼层（整数）:", parent=self.root)
            room = simpledialog.askinteger("清退办公室", "房间号（整数）:", parent=self.root)
            if floor is None or room is None:
                return

            result = self.service.vacate_office(building, floor, room)
            if result == "Not valid.":
                messagebox.showerror("输入错误", "楼层或房间号格式无效！", parent=self.root)
            else:
                messagebox.showinfo("成功", f"办公室 {building} {floor}-{room} 已清退", parent=self.root)
                self.show_vacant_offices()  # 刷新空闲列表
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    def show_all_offices(self):
        try:
            self.clear_tree(self.loc_tree)
            offices = self.service.get_all_offices()  # 调用你的 DAO 方法
            for row in offices:
                # 注意：Office 表的字段名是带前缀的！
                if isinstance(row, dict):
                    values = (
                        row['Office_Building'],
                        row['Office_Floor'],
                        row['Office_RoomNum']
                    )
                else:
                    # 如果返回的是元组，假设顺序为 (OwnerSsn, Office_Building, Office_Floor, Office_RoomNum)
                    values = (row[1], row[2], row[3])  # 跳过 OwnerSsn
                self.loc_tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)



    # ---------- 监督关系 ------------------------------------------------------------------------------------------------------------------------------------------------------
    def create_supervision_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Supervision Management")

        # 创建两个子框架，分别处理两种监管关系
        emp_supervision_frame = ttk.LabelFrame(frame, text="Employee to Employee Supervision")
        emp_supervision_frame.pack(fill=tk.X, padx=10, pady=5)

        temp_supervision_frame = ttk.LabelFrame(frame, text="Manager to Temp Employee Supervision")
        temp_supervision_frame.pack(fill=tk.X, padx=10, pady=5)

        # 员工间监管按钮
        emp_btn_frame = ttk.Frame(emp_supervision_frame)
        emp_btn_frame.pack(pady=5)

        ttk.Button(emp_btn_frame, text="List Employee Supervision", command=self.list_employee_supervision_gui).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(emp_btn_frame, text="Create Employee Supervision",
                   command=self.create_employee_supervision_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(emp_btn_frame, text="Delete Employee Supervision",
                   command=self.delete_employee_supervision_gui).pack(side=tk.LEFT, padx=5)

        # 临时工监管按钮
        temp_btn_frame = ttk.Frame(temp_supervision_frame)
        temp_btn_frame.pack(pady=5)

        ttk.Button(temp_btn_frame, text="List Temp Supervision", command=self.list_temp_supervision_gui).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(temp_btn_frame, text="Create Temp Supervision", command=self.create_temp_supervision_gui).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(temp_btn_frame, text="Delete Temp Supervision", command=self.delete_temp_supervision_gui).pack(
            side=tk.LEFT, padx=5)

        # 监管关系显示表格
        self.supervision_tree = ttk.Treeview(frame, columns=("Supervisor SSN", "Supervisee SSN"), show="headings")
        self.supervision_tree.heading("Supervisor SSN", text="Supervisor SSN")
        self.supervision_tree.heading("Supervisee SSN", text="Supervisee SSN")
        self.supervision_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ========== 员工间监管功能 ==========

    def list_employee_supervision_gui(self):
        # 获取所有员工SSN
        try:
            employees = self.service.get_all_employees()
            employee_ssns = [emp.get('Ssn', '') for emp in employees]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employees: {str(e)}")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("List Employee Supervision")
        dialog.geometry("300x120")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Select Employee SSN:").pack(pady=10)

        ssn_var = tk.StringVar()
        ssn_combo = ttk.Combobox(
            dialog,
            textvariable=ssn_var,
            values=employee_ssns,
            state="readonly",
            width=25
        )
        ssn_combo.pack(pady=5)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def on_submit():
            selected_ssn = ssn_var.get().strip()
            if not selected_ssn:
                messagebox.showwarning("Input Error", "Please select an employee SSN", parent=dialog)
                return

            try:
                # 清空表格
                self.clear_tree(self.supervision_tree)

                # 调用DAO函数列出监管关系并获取返回结果
                supervision_data = self.service.list_supervision(selected_ssn)

                if supervision_data and len(supervision_data) > 0:
                    # 将监管关系数据添加到表格中
                    for row in supervision_data:
                        supervisor_ssn = row.get('Supervisor_Ssn', '')
                        supervisee_ssn = row.get('Supervisee_Ssn', '')
                        self.supervision_tree.insert("", "end", values=(supervisor_ssn, supervisee_ssn))

                    self.update_status(f"Loaded {len(supervision_data)} supervision relationships")
                else:
                    self.update_status("No supervision relationships found")

                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="List", command=on_submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def create_employee_supervision_dialog(self):
        # 获取所有员工SSN
        try:
            employees = self.service.get_all_employees()
            employee_ssns = [emp.get('Ssn', '') for emp in employees]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employees: {str(e)}")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Create Employee Supervision")
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 监管者SSN
        ttk.Label(dialog, text="Supervisor SSN:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        supervisor_var = tk.StringVar()
        supervisor_combo = ttk.Combobox(dialog, textvariable=supervisor_var, values=employee_ssns, state="readonly",
                                        width=25)
        supervisor_combo.grid(row=0, column=1, padx=10, pady=10)

        # 被监管者SSN
        ttk.Label(dialog, text="Supervisee SSN:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        supervisee_var = tk.StringVar()
        supervisee_combo = ttk.Combobox(dialog, textvariable=supervisee_var, values=employee_ssns, state="readonly",
                                        width=25)
        supervisee_combo.grid(row=1, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)

        def on_submit():
            supervisor_ssn = supervisor_var.get().strip()
            supervisee_ssn = supervisee_var.get().strip()

            if not supervisor_ssn or not supervisee_ssn:
                messagebox.showwarning("Input Error", "Both supervisor and supervisee SSN are required", parent=dialog)
                return

            if supervisor_ssn == supervisee_ssn:
                messagebox.showwarning("Input Error", "Supervisor and supervisee cannot be the same person",
                                       parent=dialog)
                return

            try:
                self.service.set_supervision(supervisee_ssn, supervisor_ssn)
                messagebox.showinfo("Success", "Employee supervision created successfully", parent=dialog)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="Create", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def create_employee_supervision_gui(self):
        self.create_employee_supervision_dialog()

    def delete_employee_supervision_dialog(self):
        # 获取所有员工SSN
        try:
            employees = self.service.get_all_employees()
            employee_ssns = [emp.get('Ssn', '') for emp in employees]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employees: {str(e)}")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Employee Supervision")
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 监管者SSN
        ttk.Label(dialog, text="Supervisor SSN:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        supervisor_var = tk.StringVar()
        supervisor_combo = ttk.Combobox(dialog, textvariable=supervisor_var, values=employee_ssns, state="readonly",
                                        width=25)
        supervisor_combo.grid(row=0, column=1, padx=10, pady=10)

        # 被监管者SSN
        ttk.Label(dialog, text="Supervisee SSN:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        supervisee_var = tk.StringVar()
        supervisee_combo = ttk.Combobox(dialog, textvariable=supervisee_var, values=employee_ssns, state="readonly",
                                        width=25)
        supervisee_combo.grid(row=1, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)

        def on_submit():
            supervisor_ssn = supervisor_var.get().strip()
            supervisee_ssn = supervisee_var.get().strip()

            if not supervisor_ssn or not supervisee_ssn:
                messagebox.showwarning("Input Error", "Both supervisor and supervisee SSN are required", parent=dialog)
                return

            if messagebox.askyesno("Confirm",
                                   f"Are you sure you want to delete supervision between {supervisor_ssn} and {supervisee_ssn}?",
                                   parent=dialog):
                try:
                    self.service.delete_supervision(supervisor_ssn, supervisee_ssn)
                    messagebox.showinfo("Success", "Employee supervision deleted successfully", parent=dialog)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="Delete", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def delete_employee_supervision_gui(self):
        self.delete_employee_supervision_dialog()

    # ========== 临时工监管功能 ==========

    def list_temp_supervision_gui(self):
        # 获取所有临时工SSN
        try:
            temp_employees = self.service.get_all_temp_employees()
            temp_ssns = [temp_emp.get('TempSsn', '') for temp_emp in temp_employees]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load temp employees: {str(e)}")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("List Temp Supervision")
        dialog.geometry("300x120")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Select Temp Employee SSN:").pack(pady=10)

        ssn_var = tk.StringVar()
        ssn_combo = ttk.Combobox(
            dialog,
            textvariable=ssn_var,
            values=temp_ssns,
            state="readonly",
            width=25
        )
        ssn_combo.pack(pady=5)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def on_submit():
            selected_ssn = ssn_var.get().strip()
            if not selected_ssn:
                messagebox.showwarning("Input Error", "Please select a temp employee SSN", parent=dialog)
                return

            try:
                # 清空表格
                self.clear_tree(self.supervision_tree)

                # 调用DAO函数列出监管关系并获取返回结果
                supervision_data = self.service.list_temp_supervision(selected_ssn)

                if supervision_data and len(supervision_data) > 0:
                    # 将监管关系数据添加到表格中
                    for row in supervision_data:
                        supervisor_ssn = row.get('Supervisor_Ssn_midlevel_manager', '')
                        supervisee_ssn = row.get('Supervisee_Ssn_temp_employee', '')
                        self.supervision_tree.insert("", "end", values=(supervisor_ssn, supervisee_ssn))

                    self.update_status(f"Loaded {len(supervision_data)} temp supervision relationships")
                else:
                    self.update_status("No temp supervision relationships found")

                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="List", command=on_submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def create_temp_supervision_dialog(self):
        # 获取所有临时工SSN
        try:
            temp_employees = self.service.get_all_temp_employees()
            temp_ssns = [temp_emp.get('TempSsn', '') for temp_emp in temp_employees]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load temp employees: {str(e)}")
            return

        # 获取所有中层经理SSN
        try:
            managers = self.service.get_employees_by_level("mid_level manager")
            manager_ssns = [manager.get('Ssn', '') for manager in managers]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load managers: {str(e)}")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Create Temp Supervision")
        dialog.geometry("450x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 监管者SSN (中层经理)
        ttk.Label(dialog, text="Manager SSN:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        supervisor_var = tk.StringVar()
        supervisor_combo = ttk.Combobox(dialog, textvariable=supervisor_var, values=manager_ssns, state="readonly",
                                        width=25)
        supervisor_combo.grid(row=0, column=1, padx=10, pady=10)

        # 被监管者SSN (临时工)
        ttk.Label(dialog, text="Temp Employee SSN:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        supervisee_var = tk.StringVar()
        supervisee_combo = ttk.Combobox(dialog, textvariable=supervisee_var, values=temp_ssns, state="readonly",
                                        width=25)
        supervisee_combo.grid(row=1, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)

        def on_submit():
            supervisor_ssn = supervisor_var.get().strip()
            supervisee_ssn = supervisee_var.get().strip()

            if not supervisor_ssn or not supervisee_ssn:
                messagebox.showwarning("Input Error", "Both manager and temp employee SSN are required", parent=dialog)
                return

            try:
                self.service.set_temp_supervision(supervisee_ssn, supervisor_ssn)
                messagebox.showinfo("Success", "Temp supervision created successfully", parent=dialog)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="Create", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def create_temp_supervision_gui(self):
        self.create_temp_supervision_dialog()

    def delete_temp_supervision_dialog(self):
        # 获取所有临时工SSN
        try:
            temp_employees = self.service.get_all_temp_employees()
            temp_ssns = [temp_emp.get('TempSsn', '') for temp_emp in temp_employees]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load temp employees: {str(e)}")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Temp Supervision")
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Select Temp Employee SSN:").pack(pady=10)

        ssn_var = tk.StringVar()
        ssn_combo = ttk.Combobox(
            dialog,
            textvariable=ssn_var,
            values=temp_ssns,
            state="readonly",
            width=25
        )
        ssn_combo.pack(pady=5)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def on_submit():
            selected_ssn = ssn_var.get().strip()
            if not selected_ssn:
                messagebox.showwarning("Input Error", "Please select a temp employee SSN", parent=dialog)
                return

            if messagebox.askyesno("Confirm",
                                   f"Are you sure you want to delete supervision for temp employee {selected_ssn}?",
                                   parent=dialog):
                try:
                    self.service.delete_temp_supervision(selected_ssn)
                    messagebox.showinfo("Success", "Temp supervision deleted successfully", parent=dialog)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=dialog)

        ttk.Button(button_frame, text="Delete", command=on_submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def delete_temp_supervision_gui(self):
        self.delete_temp_supervision_dialog()

    # ---------- 报表查询 ----------

    # ---------- GENERAL REPORT (ENGLISH, same style as your other tabs) ----------
    def create_general_report_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="General Report")

        # Button row (same visual style)
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5, fill=tk.X)

        ttk.Button(btn_frame, text="Activities by Date Range", command=self.report_activities_by_date_range).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Manager Activity Count", command=self.report_manager_activity_count).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Show All Activities", command=self.report_all_activities).pack(side=tk.LEFT,
                                                                                                   padx=5)
        ttk.Button(btn_frame, text="Show All Employees", command=self.report_all_employees).pack(side=tk.LEFT,
                                                                                                 padx=5)
        ttk.Button(btn_frame, text="Show All Temp Employees", command=self.report_all_temp_employees).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Employees by Level", command=self.report_employees_by_level).pack(side=tk.LEFT,
                                                                                                      padx=5)
        ttk.Button(btn_frame, text="Office Vacancy Rate", command=self.report_office_vacancy_rate).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Activities by Building", command=self.report_activities_by_building).pack(
            side=tk.LEFT, padx=5)

        # Treeview for showing results (reuse pattern)
        self.general_tree = ttk.Treeview(frame, show="headings")
        self.general_tree.pack(fill=tk.BOTH, expand=True, pady=5)

        # add vertical scrollbar like other tabs
        tree_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.general_tree.yview)
        self.general_tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # utility to clear and set columns then insert rows
    def _load_into_general_tree(self, columns, rows):
        """
        columns: list of column headings (strings)
        rows: iterable of tuples (values)
        """
        try:
            # clear existing
            for item in self.general_tree.get_children():
                self.general_tree.delete(item)

            # set columns
            self.general_tree["columns"] = columns
            for col in columns:
                self.general_tree.heading(col, text=col)
                # reasonable default width (you can adjust)
                self.general_tree.column(col, width=150, anchor=tk.W)

            # insert rows
            for r in rows:
                # if dict-like, convert to tuple of column order
                if isinstance(r, dict):
                    vals = tuple(r.get(c, "") for c in columns)
                else:
                    vals = r
                self.general_tree.insert("", "end", values=vals)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # 1) Activities by date range
    def report_activities_by_date_range(self):
        start = simpledialog.askstring("Start date", "Enter start date (YYYY-MM-DD):", parent=self.root)
        if start is None:
            return
        end = simpledialog.askstring("End date", "Enter end date (YYYY-MM-DD):", parent=self.root)
        if end is None:
            return

        try:
            activities = self.service.get_activities_by_date_range(start, end)
            if not activities:
                messagebox.showinfo("No Data", f"No activities found between {start} and {end}.", parent=self.root)
                # still clear and show headings
                self._load_into_general_tree(["Time", "Type", "Chemical", "Building", "Floor", "Room"], [])
                return

            rows = []
            for a in activities:
                rows.append((
                    a.get("Activity_Time", ""),
                    a.get("Activity_Type", ""),
                    a.get("Require_Chemical", ""),
                    a.get("Activity_Building", ""),
                    a.get("Activity_Floor", ""),
                    a.get("Activity_RoomNum", "")
                ))

            cols = ["Time", "Type", "Chemical", "Building", "Floor", "Room"]
            self._load_into_general_tree(cols, rows)
            messagebox.showinfo("Success", f"Loaded {len(rows)} activities.", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # 2) Manager activity count
    def report_manager_activity_count(self):
        ssn = simpledialog.askstring("Manager SSN", "Enter the manager SSN:", parent=self.root)
        if ssn is None or ssn.strip() == "":
            return
        try:
            count = self.service.get_manager_activity_counts(ssn.strip())
            # show in tree as single-row table
            self._load_into_general_tree(["Manager SSN", "Activity Count"], [(ssn.strip(), count)])
            messagebox.showinfo("Success", f"Manager {ssn.strip()} manages {count} activities.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # 3) All activities
    def report_all_activities(self):
        try:
            activities = self.service.get_all_activities()
            if not activities:
                messagebox.showinfo("No Data", "No activities found.", parent=self.root)
                self._load_into_general_tree(["Time", "Type", "Chemical", "Building", "Floor", "Room"], [])
                return

            rows = []
            for a in activities:
                rows.append((
                    a.get("Activity_Time", ""),
                    a.get("Activity_Type", ""),
                    a.get("Require_Chemical", ""),
                    a.get("Activity_Building", ""),
                    a.get("Activity_Floor", ""),
                    a.get("Activity_RoomNum", "")
                ))

            cols = ["Time", "Type", "Chemical", "Building", "Floor", "Room"]
            self._load_into_general_tree(cols, rows)
            messagebox.showinfo("Success", f"Loaded {len(rows)} activities.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # 4) All employees
    def report_all_employees(self):
        try:
            emps = self.service.get_all_employees()
            if not emps:
                messagebox.showinfo("No Data", "No employees found.", parent=self.root)
                self._load_into_general_tree(["SSN", "Name", "Level"], [])
                return

            rows = []
            for emp in emps:
                rows.append((
                    emp.get("Ssn", ""),
                    emp.get("Name", ""),
                    emp.get("Emp_Level", "")
                ))

            cols = ["SSN", "Name", "Level"]
            self._load_into_general_tree(cols, rows)
            messagebox.showinfo("Success", f"Loaded {len(rows)} employees.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # 5) All temporary employees with companies
    def report_all_temp_employees(self):
        try:
            temps = self.service.get_all_temp_employees_with_companies()
            if not temps:
                messagebox.showinfo("No Data", "No temporary employees found.", parent=self.root)
                self._load_into_general_tree(["Temp SSN", "Company", "Contractor Company"], [])
                return

            rows = []
            for t in temps:
                rows.append((
                    t.get("TempSsn", ""),
                    t.get("Company_name", ""),
                    t.get("Contractor_Company_Name", "") or ""
                ))

            cols = ["Temp SSN", "Company", "Contractor Company"]
            self._load_into_general_tree(cols, rows)
            messagebox.showinfo("Success", f"Loaded {len(rows)} temporary employees.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # 6) Employees by level (ask for level)
    def report_employees_by_level(self):
        level = simpledialog.askstring("Employee Level",
                                       "Enter level (executive officer, mid_level manager, base_level worker):",
                                       parent=self.root)
        if level is None or level.strip() == "":
            return
        level = level.strip()
        try:
            emps = self.service.get_employees_by_level(level)
            if not emps:
                messagebox.showinfo("No Data", f"No employees at level '{level}'.", parent=self.root)
                self._load_into_general_tree(["SSN", "Name", "Level"], [])
                return

            rows = []
            for emp in emps:
                rows.append((
                    emp.get("Ssn", ""),
                    emp.get("Name", ""),
                    emp.get("Emp_Level", "")
                ))

            cols = ["SSN", "Name", "Level"]
            self._load_into_general_tree(cols, rows)
            messagebox.showinfo("Success", f"Loaded {len(rows)} employees at level '{level}'.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # 7) Office vacancy rate (compute using get_all_offices + get_vacant_offices)
    def report_office_vacancy_rate(self):
        try:
            all_offices = self.service.get_all_offices()
            vacant = self.service.get_vacant_offices()

            total = len(all_offices) if all_offices is not None else 0
            vacant_count = len(vacant) if vacant is not None else 0

            if total == 0:
                messagebox.showinfo("No Data", "No office records found.", parent=self.root)
                self._load_into_general_tree(["Total Offices", "Vacant Offices", "Vacancy Rate"], [])
                return

            rate = (vacant_count / total) * 100
            # present small table
            self._load_into_general_tree(["Total Offices", "Vacant Offices", "Vacancy Rate (%)"],
                                         [(total, vacant_count, f"{rate:.2f}")])
            messagebox.showinfo("Success", f"Total: {total}, Vacant: {vacant_count}, Vacancy Rate: {rate:.2f}%.",
                                parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # 8) Activities by building (aggregate)
    def report_activities_by_building(self):
        try:
            activities = self.service.get_all_activities()
            if not activities:
                messagebox.showinfo("No Data", "No activities found.", parent=self.root)
                self._load_into_general_tree(["Building", "Activity Count"], [])
                return

            agg = {}
            for a in activities:
                b = a.get("Activity_Building", "") or "UNKNOWN"
                agg[b] = agg.get(b, 0) + 1

            rows = [(b, cnt) for b, cnt in agg.items()]
            cols = ["Building", "Activity Count"]
            self._load_into_general_tree(cols, rows)
            messagebox.showinfo("Success", f"Aggregated activities for {len(rows)} building(s).", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # ---------- 自定义 SQL ----------
    def create_sql_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="自定义 SQL")

        ttk.Label(frame, text="输入 SQL 语句：").pack(anchor=tk.W, padx=5)
        self.sql_text = scrolledtext.ScrolledText(frame, height=5)
        self.sql_text.pack(fill=tk.X, padx=5, pady=5)

        run_btn = ttk.Button(frame, text="执行查询", command=self.run_custom_sql)
        run_btn.pack(pady=5)

        self.sql_result = scrolledtext.ScrolledText(frame, height=10, state=tk.DISABLED)
        self.sql_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def run_custom_sql(self):
        sql = self.sql_text.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("警告", "请输入 SQL 语句")
            return
        try:
            result = self.service.execute_custom_sql(sql)
            self.sql_result.config(state=tk.NORMAL)
            self.sql_result.delete("1.0", tk.END)
            if isinstance(result, list):
                for row in result:
                    self.sql_result.insert(tk.END, str(row) + "\n")
            else:
                self.sql_result.insert(tk.END, str(result))
            self.sql_result.config(state=tk.DISABLED)
            self.update_status("SQL 执行成功")
        except Exception as e:
            messagebox.showerror("SQL 错误", str(e))
            self.update_status("SQL 执行失败")

    # ---------- 关闭处理 ----------
    def on_closing(self):
        try:
            self.service.quick_query.close()  # 假设 DAO 有 close 方法
        except:
            pass
        self.root.destroy()