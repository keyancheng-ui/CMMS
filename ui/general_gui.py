# -----------------------------
# File: quick_query_dao.py
# -----------------------------
"""
Refactored QuickQueryDAO (方案 2)
- Consistent return types (list[dict] for queries; int/bool for updates)
- Basic input validation via Validators
- Avoids printing for normal returns; raises exceptions on bad input when appropriate
- Assumes BaseDAO provides execute_query(query, params=None) and execute_update(query, params=None)
  If BaseDAO doesn't accept params, it should still work because methods fall back to formatted SQL
"""
from typing import List, Dict, Optional, Any
import logging

from .base_dao import BaseDAO
from .validators import Validators

logger = logging.getLogger(__name__)


class QuickQueryDAO(BaseDAO):
    """DAO that centralises quick queries. Methods return consistent types:
    - query methods -> List[Dict[str, Any]] (possibly empty)
    - create/update/delete -> int (number of affected rows) or bool when more appropriate
    """

    def __init__(self, *args, **kwargs):
        # forward args/kwargs (e.g. password) to BaseDAO
        super().__init__(*args, **kwargs)

    # Helper to run parameterized queries if supported by BaseDAO
    def _run_query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        try:
            if params is not None:
                return self.execute_query(sql, params)
            return self.execute_query(sql)
        except TypeError:
            # fallback: BaseDAO may only accept single sql string
            if params:
                sql = sql % tuple(self._escape_for_fallback(p) for p in params)
            return self.execute_query(sql)

    def _run_update(self, sql: str, params: Optional[tuple] = None) -> int:
        try:
            if params is not None:
                return self.execute_update(sql, params)
            return self.execute_update(sql)
        except TypeError:
            if params:
                sql = sql % tuple(self._escape_for_fallback(p) for p in params)
            return self.execute_update(sql)

    def _escape_for_fallback(self, value: Any) -> str:
        # Very conservative fallback escaping to avoid breaking SQL when BaseDAO doesn't support params.
        if value is None:
            return 'NULL'
        s = str(value)
        return "'" + s.replace("'", "''") + "'"

    # --- activity related ---
    def get_activity(self, activity_time: str, activity_building: str, activity_floor: str, activity_room_num: str) -> List[Dict[str, Any]]:
        """Return list with 0 or 1 dicts describing the activity."""
        if not Validators.validate_date(activity_time):
            raise ValueError("Invalid activity_time")
        sql = "SELECT * FROM Activity WHERE Activity_Time = ? AND Activity_Building = ? AND Activity_Floor = ? AND Activity_RoomNum = ?"
        return self._run_query(sql, (activity_time, activity_building, activity_floor, activity_room_num))

    def create_activity(self, activity_time: str, activity_type: str, require_chemical: str, activity_building: str, activity_floor: str, activity_room_num: str) -> int:
        if not (Validators.validate_date(activity_time) and Validators.validate_activity_type(activity_type) and Validators.validate_chemical_requirement(require_chemical) and Validators.validate_floor(activity_floor)[0] and Validators.validate_room(activity_room_num)[0]):
            raise ValueError("Invalid input for creating activity")

        # check existence
        sql_check = "SELECT 1 FROM Activity WHERE Activity_Time = ? AND Activity_Building = ? AND Activity_Floor = ? AND Activity_RoomNum = ?"
        found = self._run_query(sql_check, (activity_time, activity_building, activity_floor, activity_room_num))
        if found:
            return 0

        sql = "INSERT INTO Activity (Activity_Time, Activity_Type, Require_Chemical, Activity_Building, Activity_Floor, Activity_RoomNum) VALUES (?, ?, ?, ?, ?, ?)"
        return self._run_update(sql, (activity_time, activity_type, require_chemical, activity_building, activity_floor, activity_room_num))

    def get_all_activities(self) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM Activity ORDER BY Activity_Time DESC, Activity_Building, Activity_Floor"
        return self._run_query(sql)

    def assign_manager_to_activity(self, manager_ssn: str, activity_time: str, activity_building: str, activity_floor: str, activity_room_num: str) -> int:
        if not Validators.validate_date(activity_time):
            raise ValueError("Invalid activity_time")
        sql_check = "SELECT 1 FROM Mid_Level_Manage_Activity WHERE Manage_Activity_Building = ? AND Manage_Activity_Floor = ? AND Manage_Activity_RoomNum = ? AND Manage_Activity_Time = ?"
        exists = self._run_query(sql_check, (activity_building, activity_floor, activity_room_num, activity_time))
        if exists:
            return 0
        sql = "INSERT INTO Mid_Level_Manage_Activity (Manager_Ssn, Manage_Activity_Building, Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time) VALUES (?, ?, ?, ?, ?)"
        return self._run_update(sql, (manager_ssn, activity_building, activity_floor, activity_room_num, activity_time))

    def assign_employee_to_activity(self, working_time: str, working_building: str, working_floor: str, working_room_number: str, working_worker_ssn: str) -> int:
        if not Validators.validate_date(working_time):
            raise ValueError("Invalid working_time")
        sql_check = "SELECT 1 FROM Employee_Work_On WHERE Working_Building = ? AND Working_Floor = ? AND Working_Room_number = ? AND Working_Time = ?"
        exists = self._run_query(sql_check, (working_building, working_floor, working_room_number, working_time))
        if exists:
            return 0
        sql = "INSERT INTO Employee_Work_On (Working_Time, Working_Building, Working_Floor, Working_Room_number, Working_Worker_Ssn) VALUES (?, ?, ?, ?, ?)"
        return self._run_update(sql, (working_time, working_building, working_floor, working_room_number, working_worker_ssn))

    def assign_temp_employee_to_activity(self, temp_working_time: str, temp_working_building: str, temp_working_floor: str, temp_working_room_number: str, temp_working_worker_ssn: str) -> int:
        if not Validators.validate_date(temp_working_time):
            raise ValueError("Invalid temp_working_time")
        sql_check = "SELECT 1 FROM Temp_Employee_Work_On WHERE Temp_Working_Building = ? AND Temp_Working_Floor = ? AND Temp_Working_Room_number = ? AND Temp_Working_Time = ? AND Temp_Working_Worker_Ssn = ?"
        exists = self._run_query(sql_check, (temp_working_building, temp_working_floor, temp_working_room_number, temp_working_time, temp_working_worker_ssn))
        if exists:
            return 0
        sql = "INSERT INTO Temp_Employee_Work_On (Temp_Working_Time, Temp_Working_Building, Temp_Working_Floor, Temp_Working_Room_number, Temp_Working_Worker_Ssn) VALUES (?, ?, ?, ?, ?)"
        return self._run_update(sql, (temp_working_time, temp_working_building, temp_working_floor, temp_working_room_number, temp_working_worker_ssn))

    def create_applied_to(self, applied_time: str, applied_building: str, applied_floor: str, applied_room_number: str, applied_reason: str) -> int:
        sql = "INSERT INTO Applied_To (Applied_Time, Applied_Building, Applied_Floor, Applied_Room_number, Applied_Reason) VALUES (?, ?, ?, ?, ?)"
        return self._run_update(sql, (applied_time, applied_building, applied_floor, applied_room_number, applied_reason))

    def remove_manager_from_activity(self, manager_ssn: str, activity_time: str, activity_building: str, activity_floor: str, activity_room_num: str) -> int:
        sql_check = "SELECT 1 FROM Mid_Level_Manage_Activity WHERE Manage_Activity_Building = ? AND Manage_Activity_Floor = ? AND Manage_Activity_RoomNum = ? AND Manage_Activity_Time = ? AND Manager_Ssn = ?"
        found = self._run_query(sql_check, (activity_building, activity_floor, activity_room_num, activity_time, manager_ssn))
        if not found:
            return 0
        sql = "DELETE FROM Mid_Level_Manage_Activity WHERE Manager_Ssn = ? AND Manage_Activity_Building = ? AND Manage_Activity_Floor = ? AND Manage_Activity_RoomNum = ? AND Manage_Activity_Time = ?"
        return self._run_update(sql, (manager_ssn, activity_building, activity_floor, activity_room_num, activity_time))

    def remove_employee_from_activity(self, working_time: str, working_building: str, working_floor: str, working_room_number: str, working_worker_ssn: str) -> int:
        sql_check = "SELECT 1 FROM Employee_Work_On WHERE Working_Building = ? AND Working_Floor = ? AND Working_Room_number = ? AND Working_Time = ? AND Working_Worker_Ssn = ?"
        found = self._run_query(sql_check, (working_building, working_floor, working_room_number, working_time, working_worker_ssn))
        if not found:
            return 0
        sql = "DELETE FROM Employee_Work_On WHERE Working_Time = ? AND Working_Building = ? AND Working_Floor = ? AND Working_Room_number = ? AND Working_Worker_Ssn = ?"
        return self._run_update(sql, (working_time, working_building, working_floor, working_room_number, working_worker_ssn))

    def remove_temp_employee_from_activity(self, temp_working_time: str, temp_working_building: str, temp_working_floor: str, temp_working_room_number: str, temp_working_worker_ssn: str) -> int:
        sql_check = "SELECT 1 FROM Temp_Employee_Work_On WHERE Temp_Working_Building = ? AND Temp_Working_Floor = ? AND Temp_Working_Room_number = ? AND Temp_Working_Time = ? AND Temp_Working_Worker_Ssn = ?"
        found = self._run_query(sql_check, (temp_working_building, temp_working_floor, temp_working_room_number, temp_working_time, temp_working_worker_ssn))
        if not found:
            return 0
        sql = "DELETE FROM Temp_Employee_Work_On WHERE Temp_Working_Time = ? AND Temp_Working_Building = ? AND Temp_Working_Floor = ? AND Temp_Working_Room_number = ? AND Temp_Working_Worker_Ssn = ?"
        return self._run_update(sql, (temp_working_time, temp_working_building, temp_working_floor, temp_working_room_number, temp_working_worker_ssn))

    # --- employee related ---
    def get_all_employees(self) -> List[Dict[str, Any]]:
        return self._run_query("SELECT * FROM Employee ORDER BY Name")

    def get_employee_by_ssn(self, ssn: str) -> List[Dict[str, Any]]:
        return self._run_query("SELECT * FROM Employee WHERE Ssn = ?", (ssn,))

    def add_employee(self, ssn: str, name: str, emp_level: str) -> int:
        if not Validators.validate_employee_level(emp_level):
            raise ValueError("Invalid employee level")
        existing = self.get_employee_by_ssn(ssn)
        if existing:
            raise ValueError(f"Employee with SSN {ssn} already exists")
        return self._run_update("INSERT INTO Employee (Ssn, Name, Emp_Level) VALUES (?, ?, ?)", (ssn, name, emp_level))

    def get_employees_by_level(self, level: str) -> List[Dict[str, Any]]:
        if not Validators.validate_employee_level(level):
            return []
        return self._run_query("SELECT * FROM Employee WHERE Emp_Level = ?", (level,))

    def update_employee(self, ssn: str, new_level: str) -> int:
        if not Validators.validate_employee_level(new_level):
            raise ValueError("Invalid new level")
        existing = self.get_employee_by_ssn(ssn)
        if not existing:
            raise ValueError("Employee not exists")
        return self._run_update("UPDATE Employee SET Emp_Level = ? WHERE Ssn = ?", (new_level, ssn))

    def delete_employee(self, ssn: str) -> int:
        existing = self.get_employee_by_ssn(ssn)
        if not existing:
            return 0
        return self._run_update("DELETE FROM Employee WHERE Ssn = ?", (ssn,))

    # --- location & office ---
    def create_location(self, building: str, floor: str, room_number: str) -> int:
        fv, _ = Validators.validate_floor(floor)
        rv, _ = Validators.validate_room(room_number)
        if not (fv and rv):
            raise ValueError("Invalid floor or room")
        existing = self._run_query("SELECT 1 FROM Location WHERE Building = ? AND Floor = ? AND RoomNumber = ?", (building, floor, room_number))
        if existing:
            return 0
        return self._run_update("INSERT INTO Location (Building, Floor, Room_number) VALUES (?, ?, ?)", (building, floor, room_number))

    def check_location(self, building: str, floor: str, room_number: str) -> bool:
        fv, _ = Validators.validate_floor(floor)
        rv, _ = Validators.validate_room(room_number)
        if not (fv and rv):
            raise ValueError("Invalid floor or room")
        exists = self._run_query("SELECT 1 FROM Location WHERE Building = ? AND Floor = ? AND RoomNumber = ?", (building, floor, room_number))
        return bool(exists)

    def get_all_locations(self) -> List[Dict[str, Any]]:
        return self._run_query("SELECT * FROM Location ORDER BY Building, Floor, RoomNumber")

    def get_locations_by_building(self, building: str) -> List[Dict[str, Any]]:
        return self._run_query("SELECT * FROM Location WHERE Building = ? ORDER BY Floor, RoomNumber", (building,))

    def get_vacant_offices(self) -> List[Dict[str, Any]]:
        return self._run_query("SELECT * FROM Office WHERE OwnerSsn IS NULL")

    def assign_office_to_employee(self, building: str, floor: str, room_number: str, owner_ssn: str) -> int:
        fv, _ = Validators.validate_floor(floor)
        rv, _ = Validators.validate_room(room_number)
        if not (fv and rv):
            raise ValueError("Invalid floor or room")
        # check whether owner already has office
        existing_owner = self._run_query("SELECT * FROM Office WHERE OwnerSsn = ?", (owner_ssn,))
        if existing_owner:
            return 0
        return self._run_update("UPDATE Office SET OwnerSsn = ? WHERE Office_Building = ? AND Office_Floor = ? AND Office_RoomNum = ?", (owner_ssn, building, floor, room_number))

    def vacate_office(self, building: str, floor: str, room_number: str) -> int:
        fv, _ = Validators.validate_floor(floor)
        rv, _ = Validators.validate_room(room_number)
        if not (fv and rv):
            raise ValueError("Invalid floor or room")
        return self._run_update("UPDATE Office SET OwnerSsn = NULL WHERE Office_Building = ? AND Office_Floor = ? AND Office_RoomNum = ?", (building, floor, room_number))

    def get_mid_level_managers(self) -> List[Dict[str, Any]]:
        return self._run_query("SELECT Name, Ssn FROM Employee WHERE Emp_Level = ?", ("mid_level manager",))

    def get_activities_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        if not (Validators.validate_date(start_date) and Validators.validate_date(end_date)):
            raise ValueError("Invalid date range")
        return self._run_query("SELECT * FROM Activity WHERE Activity_Time BETWEEN ? AND ? ORDER BY Activity_Time", (start_date, end_date))

    def get_manager_activity_counts(self, manager_ssn: str) -> int:
        res = self._run_query("SELECT COUNT(*) as cnt FROM Mid_Level_Manage_Activity WHERE Manager_Ssn = ?", (manager_ssn,))
        return int(res[0]['cnt']) if res else 0

    def get_employees_in_certain_building(self, activity_date: str, building: str) -> List[Dict[str, Any]]:
        if not Validators.validate_date(activity_date):
            raise ValueError("Invalid activity_date")
        return self._run_query("SELECT Working_Worker_Ssn FROM Employee_Work_On WHERE Working_Building = ? AND Working_Time = ?", (building, activity_date))

    def get_contractor_employee_counts(self) -> int:
        res = self._run_query("SELECT COUNT(*) as cnt FROM Temporary_Employee")
        return int(res[0]['cnt']) if res else 0

    # --- supervision & temp employee ---
    def set_supervision(self, employee_ssn: str, supervisor_ssn: str) -> int:
        if not Validators.ensure_distinct(employee_ssn, supervisor_ssn):
            return 0
        e = self.get_employee_by_ssn(employee_ssn)
        s = self.get_employee_by_ssn(supervisor_ssn)
        if not e or not s:
            raise ValueError("Employee or supervisor not exists")
        # check already exists
        exists = self._run_query("SELECT 1 FROM Employee_Supervision WHERE Supervisor_Ssn = ? AND Supervisee_Ssn = ?", (supervisor_ssn, employee_ssn))
        if exists:
            return 0
        # basic level rules enforced by validators or business logic
        level1 = e[0]['Emp_Level']
        level2 = s[0]['Emp_Level']
        allowed = (level1 == 'base_level worker' and level2 in ('mid_level manager', 'executive officer')) or (level1 == 'mid_level manager' and level2 == 'executive officer')
        if not allowed:
            raise ValueError('Supervision not qualified')
        return self._run_update("INSERT INTO Employee_Supervision (Supervisor_Ssn, Supervisee_Ssn) VALUES (?, ?)", (supervisor_ssn, employee_ssn))

    def list_supervision(self, ssn: str) -> List[Dict[str, Any]]:
        emp = self.get_employee_by_ssn(ssn)
        if not emp:
            raise ValueError("Employee not exists")
        return self._run_query("SELECT * FROM Employee_Supervision WHERE Supervisor_Ssn = ? OR Supervisee_Ssn = ?", (ssn, ssn))

    def delete_supervision(self, supervisor_ssn: str, supervisee_ssn: str) -> int:
        found = self._run_query("SELECT 1 FROM Employee_Supervision WHERE Supervisor_Ssn = ? AND Supervisee_Ssn = ?", (supervisor_ssn, supervisee_ssn))
        if not found:
            return 0
        return self._run_update("DELETE FROM Employee_Supervision WHERE Supervisor_Ssn = ? AND Supervisee_Ssn = ?", (supervisor_ssn, supervisee_ssn))

    # temp supervise
    def set_temp_supervision(self, temp_employee_ssn: str, supervisor_ssn: str) -> int:
        temp = self._run_query("SELECT * FROM Temporary_Employee WHERE TempSsn = ?", (temp_employee_ssn,))
        sup = self.get_employee_by_ssn(supervisor_ssn)
        if not temp or not sup:
            raise ValueError('Temp-employee or supervisor not exists')
        if sup[0]['Emp_Level'] != 'mid_level manager':
            raise ValueError('Only mid level manager can supervise temps')
        exists = self._run_query("SELECT 1 FROM TempSupervise WHERE Supervisor_Ssn_midlevel_manager = ? AND Supervisee_Ssn_temp_employee = ?", (supervisor_ssn, temp_employee_ssn))
        if exists:
            return 0
        return self._run_update("INSERT INTO TempSupervise (Supervisor_Ssn_midlevel_manager, Supervisee_Ssn_temp_employee) VALUES (?, ?)", (supervisor_ssn, temp_employee_ssn))

    def list_temp_supervision(self, supervisee_ssn: str) -> List[Dict[str, Any]]:
        temp = self._run_query("SELECT * FROM Temporary_Employee WHERE TempSsn = ?", (supervisee_ssn,))
        if not temp:
            raise ValueError('Temp-employee not exists')
        return self._run_query("SELECT * FROM TempSupervise WHERE Supervisee_Ssn_temp_employee = ?", (supervisee_ssn,))

    def delete_temp_supervision(self, temp_supervisee_ssn: str) -> int:
        found = self._run_query("SELECT 1 FROM TempSupervise WHERE Supervisee_Ssn_temp_employee = ?", (temp_supervisee_ssn,))
        if not found:
            return 0
        return self._run_update("DELETE FROM TempSupervise WHERE Supervisee_Ssn_temp_employee = ?", (temp_supervisee_ssn,))

    # temporary employees with companies
    def create_temp_employee_with_company(self, temp_ssn: str, company_name: str, contractor_company_name: str) -> int:
        existing = self._run_query("SELECT * FROM Temporary_Employee WHERE TempSsn = ?", (temp_ssn,))
        if existing:
            return 0
        r1 = self._run_update("INSERT INTO Temporary_Employee (TempSsn, Company_name) VALUES (?, ?)", (temp_ssn, company_name))
        r2 = self._run_update("INSERT INTO Contractor_Company (name, Temp_Employee_Ssn) VALUES (?, ?)", (contractor_company_name, temp_ssn))
        return (r1 or 0) + (r2 or 0)

    def get_temp_employee_with_company(self, temp_ssn: str) -> List[Dict[str, Any]]:
        sql = """
            SELECT te.TempSsn, te.Company_name, cc.name as Contractor_Company_Name
            FROM Temporary_Employee te
            LEFT JOIN Contractor_Company cc ON te.TempSsn = cc.Temp_Employee_Ssn
            WHERE te.TempSsn = ?
        """
        res = self._run_query(sql, (temp_ssn,))
        return res

    def get_temp_employee_by_ssn(self, temp_ssn: str) -> List[Dict[str, Any]]:
        return self._run_query("SELECT * FROM Temporary_Employee WHERE TempSsn = ?", (temp_ssn,))

    def get_all_temp_employees(self) -> List[Dict[str, Any]]:
        return self._run_query("SELECT * FROM Temporary_Employee ORDER BY Company_name, TempSsn")

    def get_all_temp_employees_with_companies(self) -> List[Dict[str, Any]]:
        sql = """
            SELECT te.TempSsn, te.Company_name, cc.name as Contractor_Company_Name
            FROM Temporary_Employee te
            LEFT JOIN Contractor_Company cc ON te.TempSsn = cc.Temp_Employee_Ssn
            ORDER BY te.Company_name, te.TempSsn
        """
        return self._run_query(sql)

    def delete_temp_employee(self, temp_ssn: str) -> int:
        exists = self.get_temp_employee_by_ssn(temp_ssn)
        if not exists:
            return 0
        return self._run_update("DELETE FROM Temporary_Employee WHERE TempSsn = ?", (temp_ssn,))

    def update_contractor_company(self, temp_employee_ssn: str, new_company_name: str) -> int:
        company = self._run_query("SELECT * FROM Contractor_Company WHERE Temp_Employee_Ssn = ?", (temp_employee_ssn,))
        if not company:
            return 0
        return self._run_update("UPDATE Contractor_Company SET name = ? WHERE Temp_Employee_Ssn = ?", (new_company_name, temp_employee_ssn))


# -----------------------------
# File: general_gui.py
# -----------------------------
"""
Refactored GUI (方案 2)
- Adapts to the rewritten QuickQueryDAO: methods return list[dict] or ints
- Avoids assuming tuple order; uses dict keys
- Improved dialogs and error handling
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from src.db.quick_query_dao import QuickQueryDAO
from src.db.validators import Validators


class QuickQueryGUI:
    def __init__(self, root, password=None):
        self.root = root
        self.root.title("COMP2411 DATABASE PROJECT")
        self.service = QuickQueryDAO(password=password)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_employee_tab()
        self.create_activity_tab()
        self.create_temp_employee_tab()
        self.create_location_tab()
        self.create_supervision_tab()
        self.create_report_tab()
        self.create_sql_tab()

        self.status = tk.Label(root, text="All set!!!", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, msg: str):
        self.status.config(text=msg)

    def clear_tree(self, tree: ttk.Treeview):
        for item in tree.get_children():
            tree.delete(item)

    # --- employee tab ---
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
        for col, heading in [("SSN", "SSN"), ("Name", "姓名"), ("Level", "等级")]:
            self.emp_tree.heading(col, text=heading)
        self.emp_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def add_employee_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("新增员工")
        dialog.geometry("350x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.focus_set()

        ttk.Label(dialog, text="SSN:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ssn_var = tk.StringVar()
        ssn_entry = ttk.Entry(dialog, textvariable=ssn_var, width=30)
        ssn_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(dialog, text="姓名:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(dialog, textvariable=name_var, width=30)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(dialog, text="等级:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        level_var = tk.StringVar()
        level_combo = ttk.Combobox(dialog, textvariable=level_var, values=["executive officer", "mid_level manager", "base_level worker"], state="readonly", width=27)
        level_combo.grid(row=2, column=1, padx=10, pady=10)
        level_combo.set("base_level worker")

        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)

        def on_submit():
            ssn = ssn_var.get().strip()
            name = name_var.get().strip()
            level = level_var.get().strip()
            if not ssn or not name or not level:
                messagebox.showwarning("输入错误", "所有字段均为必填！", parent=dialog)
                return
            try:
                self.service.add_employee(ssn, name, level)
                messagebox.showinfo("成功", "员工已成功添加！", parent=dialog)
                self.show_all_employees()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("错误", str(e), parent=dialog)

        def on_cancel():
            dialog.destroy()

        ttk.Button(button_frame, text="确定", command=on_submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=on_cancel).pack(side=tk.LEFT, padx=10)
        ssn_entry.focus()

    def show_all_employees(self):
        try:
            self.clear_tree(self.emp_tree)
            emps = self.service.get_all_employees() or []
            for emp in emps:
                values = (emp.get('Ssn', ''), emp.get('Name', ''), emp.get('Emp_Level', ''))
                self.emp_tree.insert("", "end", values=values)
            self.update_status(f"加载 {len(emps)} 名员工")
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    def add_employee_gui(self):
        self.add_employee_dialog()

    def lookup_employee_by_ssn(self):
        ssn = simpledialog.askstring("查询员工", "输入 SSN:", parent=self.root)
        if ssn is None:
            return
        ssn = ssn.strip()
        if not ssn:
            messagebox.showwarning("输入错误", "SSN 不能为空", parent=self.root)
            return
        try:
            result = self.service.get_employee_by_ssn(ssn) or []
            self.clear_tree(self.emp_tree)
            if result:
                emp = result[0]
                values = (emp.get('Ssn', ''), emp.get('Name', ''), emp.get('Emp_Level', ''))
                self.emp_tree.insert("", "end", values=values)
                self.update_status(f"找到员工：{values[1]}")
            else:
                messagebox.showinfo("提示", "未找到该员工", parent=self.root)
                self.update_status("未找到员工")
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)
            self.update_status("查询出错")

    def update_employee_level_gui(self):
        ssn = simpledialog.askstring("更新等级", "员工 SSN:", parent=self.root)
        if not ssn:
            return
        new_level_str = simpledialog.askstring("更新等级", "新等级 (executive officer, mid_level manager, base_level worker):", parent=self.root)
        if not new_level_str:
            return
        try:
            self.service.update_employee(ssn, new_level_str)
            messagebox.showinfo("成功", "等级更新成功", parent=self.root)
            self.show_all_employees()
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    def delete_employee_gui(self):
        ssn = simpledialog.askstring("删除员工", "员工 SSN:", parent=self.root)
        if not ssn:
            return
        if messagebox.askyesno("确认", f"确定删除 SSN 为 {ssn} 的员工？", parent=self.root):
            try:
                self.service.delete_employee(ssn)
                messagebox.showinfo("成功", "员工已删除", parent=self.root)
                self.show_all_employees()
            except Exception as e:
                messagebox.showerror("错误", str(e), parent=self.root)

    # --- activity tab ---
    def create_activity_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="活动管理")
        ttk.Button(frame, text="查看所有活动", command=self.show_all_activities).pack(pady=5)
        self.act_tree = ttk.Treeview(frame, columns=("Time", "Bldg", "Floor", "Room", "Type"), show="headings")
        for col in self.act_tree["columns"]:
            self.act_tree.heading(col, text=col)
        self.act_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def show_all_activities(self):
        try:
            self.clear_tree(self.act_tree)
            acts = self.service.get_all_activities() or []
            for a in acts:
                values = (
                    a.get('Activity_Time', ''),
                    a.get('Activity_Building', ''),
                    a.get('Activity_Floor', ''),
                    a.get('Activity_RoomNum', ''),
                    a.get('Activity_Type', '')
                )
                self.act_tree.insert("", "end", values=values)
            self.update_status(f"加载 {len(acts)} 项活动")
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    # --- temp employees ---
    def create_temp_employee_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="临时工管理")
        ttk.Button(frame, text="查看所有临时工", command=self.show_all_temp_employees).pack(pady=5)
        self.temp_tree = ttk.Treeview(frame, columns=("SSN", "Company", "Contractor"), show="headings")
        for col, txt in [("SSN", "SSN"), ("Company", "公司"), ("Contractor", "承包商")]:
            self.temp_tree.heading(col, text=txt)
        self.temp_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def show_all_temp_employees(self):
        try:
            self.clear_tree(self.temp_tree)
            temps = self.service.get_all_temp_employees_with_companies() or []
            for t in temps:
                values = (t.get('TempSsn', ''), t.get('Company_name', ''), t.get('Contractor_Company_Name', ''))
                self.temp_tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    # --- location tab ---
    def create_location_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="位置管理")
        ttk.Button(frame, text="查看所有位置", command=self.show_all_locations).pack(pady=5)
        ttk.Button(frame, text="查看空闲办公室", command=self.show_vacant_offices).pack(pady=5)
        self.loc_tree = ttk.Treeview(frame, columns=("Bldg", "Floor", "Room"), show="headings")
        for col, txt in [("Bldg", "楼"), ("Floor", "层"), ("Room", "房间")]:
            self.loc_tree.heading(col, text=txt)
        self.loc_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def show_all_locations(self):
        try:
            self.clear_tree(self.loc_tree)
            locs = self.service.get_all_locations() or []
            for l in locs:
                values = (l.get('Building', ''), l.get('Floor', ''), l.get('RoomNumber', l.get('Room_number', '')))
                self.loc_tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    def show_vacant_offices(self):
        try:
            self.clear_tree(self.loc_tree)
            locs = self.service.get_vacant_offices() or []
            for l in locs:
                values = (l.get('Office_Building', ''), l.get('Office_Floor', ''), l.get('Office_RoomNum', ''))
                self.loc_tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    # --- supervision tab ---
    def create_supervision_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="监督关系")
        ttk.Button(frame, text="设置员工监督关系", command=self.set_supervision_gui).pack(pady=5)

    def set_supervision_gui(self):
        employee_ssn = simpledialog.askstring("设置监督", "被监督员工 SSN:", parent=self.root)
        supervisor_ssn = simpledialog.askstring("设置监督", "监督人 SSN:", parent=self.root)
        if employee_ssn and supervisor_ssn:
            try:
                self.service.set_supervision(employee_ssn, supervisor_ssn)
                messagebox.showinfo("成功", "监督关系已设置", parent=self.root)
            except Exception as e:
                messagebox.showerror("错误", str(e), parent=self.root)

    # --- reports ---
    def create_report_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="报表查询")
        ttk.Button(frame, text="中层管理者及办公室", command=self.report_managers_offices).pack(pady=5)
        ttk.Button(frame, text="各承包公司临时工数量", command=self.report_contractor_counts).pack(pady=5)
        self.report_tree = ttk.Treeview(frame, show="headings")
        self.report_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def report_managers_offices(self):
        try:
            data = self.service.get_mid_level_managers() or []
            if not data:
                messagebox.showinfo("提示", "无数据", parent=self.root)
                return
            self.clear_tree(self.report_tree)
            cols = ["Manager SSN", "Name"]
            self.report_tree["columns"] = cols
            for col in cols:
                self.report_tree.heading(col, text=col)
            for row in data:
                self.report_tree.insert("", "end", values=(row.get('Ssn', ''), row.get('Name', '')))
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    def report_contractor_counts(self):
        try:
            count = self.service.get_contractor_employee_counts()
            messagebox.showinfo("结果", f"承包公司临时工总数: {count}", parent=self.root)
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.root)

    # --- custom SQL ---
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
            messagebox.showwarning("警告", "请输入 SQL 语句", parent=self.root)
            return
        try:
            # BaseDAO may expose execute_query / execute_update directly
            res = None
            try:
                res = self.service.execute_query(sql)
            except Exception:
                # fallback: attempt execute_update if not a SELECT
                res = self.service.execute_update(sql)
            self.sql_result.config(state=tk.NORMAL)
            self.sql_result.delete("1.0", tk.END)
            if isinstance(res, list):
                for row in res:
                    self.sql_result.insert(tk.END, str(row) + "\n")
            else:
                self.sql_result.insert(tk.END, str(res))
            self.sql_result.config(state=tk.DISABLED)
            self.update_status("SQL 执行成功")
        except Exception as e:
            messagebox.showerror("SQL 错误", str(e), parent=self.root)
            self.update_status("SQL 执行失败")

    def on_closing(self):
        try:
            # attempt to close underlying resources if available
            if hasattr(self.service, 'close'):
                self.service.close()
        finally:
            self.root.destroy()


# End of file
