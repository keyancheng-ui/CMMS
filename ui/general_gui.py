# ui/quick_query_gui.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from src.db.validators import *
from src.db import QuickQueryDAO


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
        self.create_report_tab()
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
        self.notebook.add(frame, text="员工管理")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="查看所有员工", command=self.show_all_employees).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="按 SSN 查询", command=self.lookup_employee_by_ssn).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="新增员工", command=self.add_employee_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="更新等级", command=self.update_employee_level_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除员工", command=self.delete_employee_gui).pack(side=tk.LEFT, padx=5)

        self.emp_tree = ttk.Treeview(frame, columns=("SSN", "Name", "Level"), show="headings")
        self.emp_tree.heading("SSN", text="SSN")
        self.emp_tree.heading("Name", text="姓名")
        self.emp_tree.heading("Level", text="等级")
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

            if not all([time, activity_type, chemical, building, floor, room]):
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
        self.notebook.add(frame, text="临时工管理")

        ttk.Button(frame, text="查看所有临时工", command=self.show_all_temp_employees).pack(pady=5)
        self.temp_tree = ttk.Treeview(frame, columns=("SSN", "Company", "Contractor"), show="headings")
        self.temp_tree.heading("SSN", text="SSN")
        self.temp_tree.heading("Company", text="公司")
        self.temp_tree.heading("Contractor", text="承包商")
        self.temp_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def show_all_temp_employees(self):
        try:
            self.clear_tree(self.temp_tree)
            temps = self.service.get_all_temp_employees_with_companies()
            for t in temps:
                self.temp_tree.insert("", "end", values=t)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    # ---------- 位置管理 ----------
    def create_location_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="位置管理")

        ttk.Button(frame, text="查看所有位置", command=self.show_all_locations).pack(pady=5)
        ttk.Button(frame, text="查看空闲办公室", command=self.show_vacant_offices).pack(pady=5)
        self.loc_tree = ttk.Treeview(frame, columns=("Bldg", "Floor", "Room"), show="headings")
        self.loc_tree.heading("Bldg", text="楼")
        self.loc_tree.heading("Floor", text="层")
        self.loc_tree.heading("Room", text="房间")
        self.loc_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def show_all_locations(self):
        try:
            self.clear_tree(self.loc_tree)
            locs = self.service.get_all_locations()
            for l in locs:
                self.loc_tree.insert("", "end", values=l)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def show_vacant_offices(self):
        try:
            self.clear_tree(self.loc_tree)
            locs = self.service.get_vacant_offices()
            for l in locs:
                self.loc_tree.insert("", "end", values=l)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    # ---------- 监督关系 ----------
    def create_supervision_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="监督关系")

        ttk.Button(frame, text="设置员工监督关系", command=self.set_supervision_gui).pack(pady=5)
        # 可扩展：显示监督关系树等

    def set_supervision_gui(self):
        employee_ssn = simpledialog.askstring("设置监督", "被监督员工 SSN:")
        supervisor_ssn = simpledialog.askstring("设置监督", "监督人 SSN:")
        if employee_ssn and supervisor_ssn:
            try:
                self.service.set_supervision(employee_ssn, supervisor_ssn)
                messagebox.showinfo("成功", "监督关系已设置")
            except Exception as e:
                messagebox.showerror("错误", str(e))

    # ---------- 报表查询 ----------
    def create_report_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="报表查询")

        ttk.Button(frame, text="中层管理者及办公室", command=self.report_managers_offices).pack(pady=5)
        ttk.Button(frame, text="各承包公司临时工数量", command=self.report_contractor_counts).pack(pady=5)
        self.report_tree = ttk.Treeview(frame, show="headings")
        self.report_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def report_managers_offices(self):
        try:
            data = self.service.get_mid_level_managers_with_offices()
            if not data:
                messagebox.showinfo("提示", "无数据")
                return
            self.clear_tree(self.report_tree)
            cols = ["Manager SSN", "Name", "Office"]
            self.report_tree["columns"] = cols
            for col in cols:
                self.report_tree.heading(col, text=col)
            for row in data:
                self.report_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def report_contractor_counts(self):
        try:
            data = self.service.get_contractor_employee_counts()
            if not data:
                messagebox.showinfo("提示", "无数据")
                return
            self.clear_tree(self.report_tree)
            cols = ["Contractor Company", "Employee Count"]
            self.report_tree["columns"] = cols
            for col in cols:
                self.report_tree.heading(col, text=col)
            for row in data:
                self.report_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("错误", str(e))

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