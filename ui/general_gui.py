# ui/quick_query_gui.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext

from src.db import QuickQueryDAO  # 假设你把这个类放在 db/service.py 并导出


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



    # ---------- 员工管理 ----------
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

    def show_all_employees(self):
        try:
            self.clear_tree(self.emp_tree)
            emps = self.service.get_all_employees()
            for e in emps:
                self.emp_tree.insert("", "end", values=e)
            self.update_status(f"加载 {len(emps)} 名员工")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def lookup_employee_by_ssn(self):
        ssn = simpledialog.askstring("查询员工", "输入 SSN:")
        if ssn:
            try:
                emp = self.service.get_employee_by_ssn(ssn)
                self.clear_tree(self.emp_tree)
                if emp:
                    self.emp_tree.insert("", "end", values=emp)
                else:
                    messagebox.showinfo("提示", "未找到该员工")
            except Exception as e:
                messagebox.showerror("错误", str(e))

    def add_employee_gui(self):
        ssn = simpledialog.askstring("新增员工", "SSN:")
        name = simpledialog.askstring("新增员工", "姓名:")
        level_str = simpledialog.askstring("新增员工", "等级 (整数):")
        if ssn and name and level_str:
            try:
                level = level_str
                self.service.add_employee(ssn, name, level)
                messagebox.showinfo("成功", "员工添加成功")
                self.show_all_employees()
            except Exception as e:
                messagebox.showerror("错误", str(e))

    def update_employee_level_gui(self):
        ssn = simpledialog.askstring("更新等级", "员工 SSN:")
        new_level_str = simpledialog.askstring("更新等级", "新等级 (整数):")
        if ssn and new_level_str:
            try:
                new_level = int(new_level_str)
                self.service.update_employee(ssn, new_level)
                messagebox.showinfo("成功", "等级更新成功")
                self.show_all_employees()
            except Exception as e:
                messagebox.showerror("错误", str(e))

    def delete_employee_gui(self):
        ssn = simpledialog.askstring("删除员工", "员工 SSN:")
        if ssn:
            if messagebox.askyesno("确认", f"确定删除 SSN 为 {ssn} 的员工？"):
                try:
                    self.service.delete_employee(ssn)
                    messagebox.showinfo("成功", "员工已删除")
                    self.show_all_employees()
                except Exception as e:
                    messagebox.showerror("错误", str(e))

    # ---------- 活动管理（简化示例）----------
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
            acts = self.service.get_all_activities()
            for a in acts:
                # 假设返回 (time, bldg, floor, room, type)
                self.act_tree.insert("", "end", values=a[:5])
            self.update_status(f"加载 {len(acts)} 项活动")
        except Exception as e:
            messagebox.showerror("错误", str(e))

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