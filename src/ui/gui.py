import os
import tkinter as tk
from tkinter import ttk
from db.connection import get_connection
from db.employee_dao import EmployeeDAO
from db.activity_dao import ActivityDAO
from db.contractor_dao import ContractorDAO
from db.temp_employee_dao import TempEmployeeDAO
from db.location_dao import LocationDAO
from db.supervision_dao import SupervisionDAO
from db.report_dao import ReportDAO
from logic.employee_service import EmployeeService
from logic.activity_service import ActivityService
from logic.contractor_service import ContractorService
from logic.temp_employee_service import TempEmployeeService
from logic.location_service import LocationService
from logic.supervision_service import SupervisionService
from logic.report_service import ReportService

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Ops Management")
        top = ttk.Frame(root)
        top.pack(fill=tk.X, padx=8, pady=8)
        self.host = tk.StringVar(value=os.getenv("MYSQL_HOST", "localhost"))
        self.port = tk.StringVar(value=os.getenv("MYSQL_PORT", "3306"))
        self.user = tk.StringVar(value=os.getenv("MYSQL_USER", "root"))
        self.password = tk.StringVar(value=os.getenv("MYSQL_PASSWORD", ""))
        self.database = tk.StringVar(value=os.getenv("MYSQL_DATABASE", "appdb"))
        ttk.Label(top, text="Host").grid(row=0, column=0, sticky="w")
        ttk.Entry(top, textvariable=self.host, width=14).grid(row=0, column=1)
        ttk.Label(top, text="Port").grid(row=0, column=2, sticky="w")
        ttk.Entry(top, textvariable=self.port, width=6).grid(row=0, column=3)
        ttk.Label(top, text="User").grid(row=0, column=4, sticky="w")
        ttk.Entry(top, textvariable=self.user, width=12).grid(row=0, column=5)
        ttk.Label(top, text="Password").grid(row=0, column=6, sticky="w")
        ttk.Entry(top, textvariable=self.password, show="*", width=14).grid(row=0, column=7)
        ttk.Label(top, text="Database").grid(row=0, column=8, sticky="w")
        ttk.Entry(top, textvariable=self.database, width=12).grid(row=0, column=9)
        ttk.Button(top, text="Apply", command=self.apply_env).grid(row=0, column=10, padx=6)
        ttk.Button(top, text="Test", command=self.test_conn).grid(row=0, column=11)
        self.status = tk.StringVar(value="")
        ttk.Label(top, textvariable=self.status).grid(row=1, column=0, columnspan=12, sticky="w")
        nb = ttk.Notebook(root)
        nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.emp_tab = ttk.Frame(nb)
        self.sup_tab = ttk.Frame(nb)
        self.act_tab = ttk.Frame(nb)
        self.con_tab = ttk.Frame(nb)
        self.tmp_tab = ttk.Frame(nb)
        self.loc_tab = ttk.Frame(nb)
        self.rep_tab = ttk.Frame(nb)
        nb.add(self.emp_tab, text="Employees")
        nb.add(self.sup_tab, text="Supervision")
        nb.add(self.act_tab, text="Activities")
        nb.add(self.con_tab, text="Contractors")
        nb.add(self.tmp_tab, text="Temp Employees")
        nb.add(self.loc_tab, text="Locations")
        nb.add(self.rep_tab, text="Reports")
        self.build_employees()
        self.build_supervision()
        self.build_activities()
        self.build_contractors()
        self.build_temp_employees()
        self.build_locations()
        self.build_reports()

    def apply_env(self):
        os.environ["MYSQL_HOST"] = self.host.get()
        os.environ["MYSQL_PORT"] = self.port.get()
        os.environ["MYSQL_USER"] = self.user.get()
        os.environ["MYSQL_PASSWORD"] = self.password.get()
        os.environ["MYSQL_DATABASE"] = self.database.get()
        self.status.set("Applied")

    def test_conn(self):
        try:
            self.apply_env()
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.fetchall()
            cur.close()
            conn.close()
            self.status.set("OK")
        except Exception as e:
            self.status.set(str(e))

    def get_conn(self):
        self.apply_env()
        return get_connection()

    def build_tree(self, parent, cols):
        tv = ttk.Treeview(parent, columns=cols, show="headings", height=10)
        for c in cols:
            tv.heading(c, text=c)
            tv.column(c, width=120)
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=vsb.set)
        tv.grid(row=0, column=0, columnspan=6, sticky="nsew")
        vsb.grid(row=0, column=6, sticky="ns")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        return tv

    def build_employees(self):
        f = self.emp_tab
        self.emp_tv = self.build_tree(f, ["id", "ssn", "name", "gender", "level"])
        ttk.Button(f, text="List", command=self.list_employees).grid(row=1, column=0, pady=6)
        self.emp_ssn = tk.StringVar(); self.emp_name = tk.StringVar(); self.emp_gender = tk.StringVar(); self.emp_level = tk.StringVar()
        ttk.Entry(f, textvariable=self.emp_ssn, width=10).grid(row=1, column=1)
        ttk.Entry(f, textvariable=self.emp_name, width=12).grid(row=1, column=2)
        ttk.Entry(f, textvariable=self.emp_gender, width=8).grid(row=1, column=3)
        ttk.Entry(f, textvariable=self.emp_level, width=10).grid(row=1, column=4)
        ttk.Button(f, text="Add", command=self.add_employee).grid(row=1, column=5)

    def list_employees(self):
        conn = self.get_conn()
        rows = EmployeeService(EmployeeDAO(conn)).list_all()
        for i in self.emp_tv.get_children(): self.emp_tv.delete(i)
        for r in rows: self.emp_tv.insert("", tk.END, values=(r.get("id"), r.get("ssn"), r.get("name"), r.get("gender"), r.get("level")))
        conn.close()

    def add_employee(self):
        conn = self.get_conn()
        EmployeeService(EmployeeDAO(conn)).add(self.emp_ssn.get(), self.emp_name.get(), self.emp_gender.get(), self.emp_level.get())
        conn.close()
        self.list_employees()

    def build_supervision(self):
        f = self.sup_tab
        ttk.Label(f, text="Employee ID").grid(row=0, column=0, sticky="w")
        ttk.Label(f, text="Supervisor ID").grid(row=0, column=2, sticky="w")
        self.sup_eid = tk.StringVar(); self.sup_sid = tk.StringVar()
        ttk.Entry(f, textvariable=self.sup_eid, width=10).grid(row=0, column=1)
        ttk.Entry(f, textvariable=self.sup_sid, width=10).grid(row=0, column=3)
        ttk.Button(f, text="Set", command=self.set_supervision).grid(row=0, column=4)
        ttk.Label(f, text="List Subordinates of").grid(row=1, column=0, sticky="w")
        self.sup_q = tk.StringVar()
        ttk.Entry(f, textvariable=self.sup_q, width=10).grid(row=1, column=1)
        ttk.Button(f, text="List", command=self.list_subordinates).grid(row=1, column=2)
        self.sub_tv = self.build_tree(f, ["employee_id"]) 

    def set_supervision(self):
        conn = self.get_conn()
        SupervisionService(SupervisionDAO(conn)).set_supervision(int(self.sup_eid.get()), int(self.sup_sid.get()))
        conn.close()

    def list_subordinates(self):
        conn = self.get_conn()
        rows = SupervisionService(SupervisionDAO(conn)).list_subordinates(int(self.sup_q.get()))
        for i in self.sub_tv.get_children(): self.sub_tv.delete(i)
        for r in rows: self.sub_tv.insert("", tk.END, values=(r.get("employee_id"),))
        conn.close()

    def build_activities(self):
        f = self.act_tab
        self.act_tv = self.build_tree(f, ["id", "date", "type", "desc"]) 
        ttk.Label(f, text="Manager ID").grid(row=1, column=0)
        ttk.Label(f, text="Location ID").grid(row=1, column=2)
        ttk.Label(f, text="Date").grid(row=1, column=4)
        ttk.Label(f, text="Type").grid(row=2, column=0)
        ttk.Label(f, text="Desc").grid(row=2, column=2)
        self.amid = tk.StringVar(); self.alid = tk.StringVar(); self.adate = tk.StringVar(); self.atype = tk.StringVar(); self.adesc = tk.StringVar(); self.areq = tk.BooleanVar()
        ttk.Entry(f, textvariable=self.amid, width=8).grid(row=1, column=1)
        ttk.Entry(f, textvariable=self.alid, width=8).grid(row=1, column=3)
        ttk.Entry(f, textvariable=self.adate, width=10).grid(row=1, column=5)
        ttk.Entry(f, textvariable=self.atype, width=10).grid(row=2, column=1)
        ttk.Entry(f, textvariable=self.adesc, width=20).grid(row=2, column=3, columnspan=2)
        ttk.Checkbutton(f, text="Chemical", variable=self.areq).grid(row=2, column=5)
        ttk.Button(f, text="Add", command=self.add_activity).grid(row=3, column=5)
        ttk.Label(f, text="Employee ID").grid(row=3, column=0)
        self.aeid = tk.StringVar()
        ttk.Entry(f, textvariable=self.aeid, width=8).grid(row=3, column=1)
        ttk.Button(f, text="List", command=self.list_activities).grid(row=3, column=2)
        ttk.Label(f, text="Assign Emp: AID, EID").grid(row=4, column=0)
        self.as_aid = tk.StringVar(); self.as_eid = tk.StringVar()
        ttk.Entry(f, textvariable=self.as_aid, width=8).grid(row=4, column=1)
        ttk.Entry(f, textvariable=self.as_eid, width=8).grid(row=4, column=2)
        ttk.Button(f, text="Assign", command=self.assign_emp).grid(row=4, column=3)
        ttk.Label(f, text="Assign Con: AID, CID").grid(row=5, column=0)
        self.as_caid = tk.StringVar(); self.as_cid = tk.StringVar()
        ttk.Entry(f, textvariable=self.as_caid, width=8).grid(row=5, column=1)
        ttk.Entry(f, textvariable=self.as_cid, width=8).grid(row=5, column=2)
        ttk.Button(f, text="Assign", command=self.assign_con).grid(row=5, column=3)

    def add_activity(self):
        conn = self.get_conn()
        ActivityDAO(conn).add(int(self.amid.get()), int(self.alid.get()), self.adate.get(), self.atype.get(), self.adesc.get(), self.areq.get())
        conn.close()

    def list_activities(self):
        conn = self.get_conn()
        rows = ActivityService(ActivityDAO(conn)).list_by_employee(int(self.aeid.get()))
        for i in self.act_tv.get_children(): self.act_tv.delete(i)
        for r in rows: self.act_tv.insert("", tk.END, values=(r.get("id"), r.get("activity_date"), r.get("activity_type"), r.get("description")))
        conn.close()

    def assign_emp(self):
        conn = self.get_conn()
        ActivityDAO(conn).assign_employee(int(self.as_aid.get()), int(self.as_eid.get()))
        conn.close()

    def assign_con(self):
        conn = self.get_conn()
        ActivityDAO(conn).assign_contractor(int(self.as_caid.get()), int(self.as_cid.get()))
        conn.close()

    def build_contractors(self):
        f = self.con_tab
        self.con_tv = self.build_tree(f, ["id", "ssn", "name", "company"]) 
        ttk.Button(f, text="List", command=self.list_contractors).grid(row=1, column=0)
        self.con_ssn = tk.StringVar(); self.con_name = tk.StringVar(); self.con_comp = tk.StringVar()
        ttk.Entry(f, textvariable=self.con_ssn, width=10).grid(row=1, column=1)
        ttk.Entry(f, textvariable=self.con_name, width=12).grid(row=1, column=2)
        ttk.Entry(f, textvariable=self.con_comp, width=12).grid(row=1, column=3)
        ttk.Button(f, text="Add", command=self.add_contractor).grid(row=1, column=4)

    def list_contractors(self):
        conn = self.get_conn()
        rows = ContractorService(ContractorDAO(conn)).list_all()
        for i in self.con_tv.get_children(): self.con_tv.delete(i)
        for r in rows: self.con_tv.insert("", tk.END, values=(r.get("id"), r.get("ssn"), r.get("name"), r.get("company")))
        conn.close()

    def add_contractor(self):
        conn = self.get_conn()
        ContractorService(ContractorDAO(conn)).add(self.con_ssn.get(), self.con_name.get(), self.con_comp.get())
        conn.close()
        self.list_contractors()

    def build_temp_employees(self):
        f = self.tmp_tab
        self.tmp_tv = self.build_tree(f, ["id", "ssn", "name", "gender", "company_id", "supervisor_id"]) 
        ttk.Button(f, text="List", command=self.list_temp).grid(row=1, column=0)
        self.tmp_ssn = tk.StringVar(); self.tmp_name = tk.StringVar(); self.tmp_gender = tk.StringVar(); self.tmp_cid = tk.StringVar(); self.tmp_sid = tk.StringVar()
        ttk.Entry(f, textvariable=self.tmp_ssn, width=10).grid(row=1, column=1)
        ttk.Entry(f, textvariable=self.tmp_name, width=12).grid(row=1, column=2)
        ttk.Entry(f, textvariable=self.tmp_gender, width=8).grid(row=1, column=3)
        ttk.Entry(f, textvariable=self.tmp_cid, width=8).grid(row=1, column=4)
        ttk.Entry(f, textvariable=self.tmp_sid, width=8).grid(row=1, column=5)
        ttk.Button(f, text="Add", command=self.add_temp).grid(row=1, column=6)

    def list_temp(self):
        conn = self.get_conn()
        rows = TempEmployeeService(TempEmployeeDAO(conn)).list_all()
        for i in self.tmp_tv.get_children(): self.tmp_tv.delete(i)
        for r in rows: self.tmp_tv.insert("", tk.END, values=(r.get("id"), r.get("ssn"), r.get("name"), r.get("gender"), r.get("company_id"), r.get("supervisor_id")))
        conn.close()

    def add_temp(self):
        conn = self.get_conn()
        TempEmployeeService(TempEmployeeDAO(conn)).add(self.tmp_ssn.get(), self.tmp_name.get(), self.tmp_gender.get(), int(self.tmp_cid.get()), int(self.tmp_sid.get()))
        conn.close()
        self.list_temp()

    def build_locations(self):
        f = self.loc_tab
        self.loc_tv = self.build_tree(f, ["id", "building", "floor", "room"]) 
        ttk.Button(f, text="List", command=self.list_locations).grid(row=1, column=0)
        self.loc_b = tk.StringVar(); self.loc_f = tk.StringVar(); self.loc_r = tk.StringVar()
        ttk.Entry(f, textvariable=self.loc_b, width=12).grid(row=1, column=1)
        ttk.Entry(f, textvariable=self.loc_f, width=8).grid(row=1, column=2)
        ttk.Entry(f, textvariable=self.loc_r, width=8).grid(row=1, column=3)
        ttk.Button(f, text="Add", command=self.add_location).grid(row=1, column=4)

    def list_locations(self):
        conn = self.get_conn()
        rows = LocationService(LocationDAO(conn)).list_all()
        for i in self.loc_tv.get_children(): self.loc_tv.delete(i)
        for r in rows: self.loc_tv.insert("", tk.END, values=(r.get("id"), r.get("building"), r.get("floor"), r.get("room")))
        conn.close()

    def add_location(self):
        conn = self.get_conn()
        LocationService(LocationDAO(conn)).add(self.loc_b.get(), self.loc_f.get(), self.loc_r.get())
        conn.close()
        self.list_locations()

    def build_reports(self):
        f = self.rep_tab
        self.rep_tv = self.build_tree(f, ["employee_id", "employee_name", "activity_count"]) 
        ttk.Button(f, text="Employee Activity", command=self.rep_employee_activity).grid(row=1, column=0)

    def rep_employee_activity(self):
        conn = self.get_conn()
        rows = ReportService(ReportDAO(conn)).employee_activity_summary()
        for i in self.rep_tv.get_children(): self.rep_tv.delete(i)
        for r in rows: self.rep_tv.insert("", tk.END, values=(r.get("employee_id"), r.get("employee_name"), r.get("activity_count")))
        conn.close()

def run():
    root = tk.Tk()
    App(root)
    root.mainloop()
